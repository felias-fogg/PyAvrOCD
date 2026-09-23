"""
The test suit for the XTinyAvrTarget class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
from unittest.mock import  MagicMock, create_autospec
from unittest import TestCase

from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.util import binary

from pyavrocd.xavr8target import XTinyXAvrTarget, XXmegaAvrTarget
from pyavrocd.deviceinfo.devices.attiny3217 import DEVICE_INFO as DEVICE_INFO_3217
from pyavrocd.deviceinfo.devices.avr128da48 import DEVICE_INFO as DEVICE_INFO_DA48


class TestXAvr8TargetUpdi(TestCase):

    def setUp(self):
        self.xa = None

    def set_up(self):
        self.xa = XTinyXAvrTarget(MagicMock())
        self.xa.protocol = create_autospec(Avr8Protocol)

    def test_memtype_write_from_string(self):
        self.set_up()
        self.assertEqual(self.xa.memtype_write_from_string('flash'), Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE)
        self.assertEqual(self.xa.memtype_write_from_string('eeprom'), Avr8Protocol.AVR8_MEMTYPE_EEPROM_ATOMIC)
        self.assertEqual(self.xa.memtype_write_from_string('internal_sram'), Avr8Protocol.AVR8_MEMTYPE_SRAM)

    def test_regfile_read(self):
        self.set_up()
        self.xa.protocol.regfile_read.return_value=bytearray(range(32))
        self.assertEqual(self.xa.regfile_read(), bytearray(range(32)))

    def test_regfile_write(self):
        self.set_up()
        self.xa.regfile_write(bytearray(range(32)))
        self.xa.protocol.regfile_write.assert_called_with(bytearray(range(32)))

    def test_statreg_read(self):
        self.set_up()
        self.xa.protocol.memory_read.return_value=bytearray([0x7F])
        self.assertEqual(self.xa.statreg_read(), b'\x7F')
        self.xa.protocol.memory_read.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM,
                                                            0x3F, 1)

    def test_statreg_write(self):
        self.set_up()
        self.xa.statreg_write(b'\x06')
        self.xa.protocol.memory_write.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM,
                                                            0x3F, b'\x06')

    def test_stack_pointer_write(self):
        self.set_up()
        self.xa.stack_pointer_write('b\x23\x01')
        self.xa.protocol.memory_write.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x3D, 'b\x23\x01')

    def test_hardware_breakpoint_set_fail(self):
        self.set_up()
        self.assertEqual(self.xa.hardware_breakpoint_set(2, 0x200),None)

    def test_hardware_breakpoint_set_right(self):
        self.set_up()
        self.xa.protocol.check_response.return_value = None
        self.assertEqual(self.xa.hardware_breakpoint_set(1, 0x200), None)
        self.xa.protocol.jtagice3_command_response.assert_called_with(bytearray([Avr8Protocol.CMD_AVR8_HW_BREAK_SET, Avr8Protocol.CMD_VERSION0, 1, 1]) +
            binary.pack_le32(0x200) +
            bytearray([3]))

    def test_hardware_breakpoint_clear_right(self):
        self.set_up()
        self.xa.protocol.check_response.return_value = None
        self.assertEqual(self.xa.hardware_breakpoint_clear(1), None)
        self.xa.protocol.jtagice3_command_response.assert_called_with(bytearray([Avr8Protocol.CMD_AVR8_HW_BREAK_CLEAR, Avr8Protocol.CMD_VERSION0, 1]))

    # --- memory access and address transformation ---------------------------

    def set_up_with_device_info(self):
        self.xa = XTinyXAvrTarget(MagicMock(), DEVICE_INFO_3217)
        self.xa.protocol = create_autospec(Avr8Protocol)

    def test_memory_read_transforms_address(self):
        self.set_up_with_device_info()
        for memtype, base in ((Avr8Protocol.AVR8_MEMTYPE_FUSES, 0x1280),
                                  (Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, 0x128A),
                                  (Avr8Protocol.AVR8_MEMTYPE_SIGNATURE, 0x1100),
                                  (Avr8Protocol.AVR8_MEMTYPE_USER_SIGNATURE, 0x1300)):
            self.xa.memory_read(memtype, 2, 1)
            self.xa.protocol.memory_read.assert_called_with(memtype, base + 2, 1)

    def test_memory_read_leaves_other_memtypes_alone(self):
        self.set_up_with_device_info()
        self.xa.memory_read(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x3F00, 4)
        self.xa.protocol.memory_read.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x3F00, 4)

    def test_memory_write_transforms_address(self):
        self.set_up_with_device_info()
        self.xa.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, 5, bytearray([0xC8]))
        self.xa.protocol.memory_write.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_FUSES, 0x1285, bytearray([0xC8]))

    def test_memory_write_leaves_other_memtypes_alone(self):
        self.set_up_with_device_info()
        self.xa.memory_write(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x3F00, bytearray([1, 2]))
        self.xa.protocol.memory_write.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x3F00, bytearray([1, 2]))

    def test_address_transform_without_device_info(self):
        self.set_up()                                  # constructed without device info
        self.xa.memory_read(Avr8Protocol.AVR8_MEMTYPE_FUSES, 2, 1)
        self.xa.protocol.memory_read.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_FUSES, 2, 1)

    # --- remaining register and breakpoint access ---------------------------

    def test_stack_pointer_read(self):
        self.set_up()
        self.xa.protocol.memory_read.return_value = bytearray([0xFF, 0x3F])
        self.assertEqual(self.xa.stack_pointer_read(), bytearray([0xFF, 0x3F]))
        self.xa.protocol.memory_read.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x3D, 0x02)

    def test_hardware_breakpoint_clear_fail(self):
        self.set_up()
        self.assertIsNone(self.xa.hardware_breakpoint_clear(2))
        self.xa.protocol.software_breakpoint_clear.assert_not_called()

    # --- session handling ---------------------------------------------------

    def test_attach(self):
        self.set_up()
        self.xa.attach()
        self.xa.protocol.attach.assert_called_once()

    def test_reactivate(self):
        self.set_up()
        self.xa.deactivate_physical = MagicMock()
        self.xa.activate_physical = MagicMock()
        calls = []
        self.xa.protocol.detach.side_effect = lambda *a: calls.append('detach')
        self.xa.deactivate_physical.side_effect = lambda *a: calls.append('deactivate')
        self.xa.activate_physical.side_effect = lambda *a: calls.append('activate')
        self.xa.protocol.attach.side_effect = lambda *a: calls.append('attach')
        self.xa.reactivate()
        self.assertEqual(calls, ['detach', 'deactivate', 'activate', 'attach'])

    def test_switch_to_progmode(self):
        self.set_up()
        calls = []
        self.xa.protocol.detach.side_effect = lambda *a: calls.append('detach')
        self.xa.protocol.enter_progmode.side_effect = lambda *a: calls.append('enter')
        self.xa.switch_to_progmode()
        self.assertEqual(calls, ['detach', 'enter'])

    def test_switch_to_debmode(self):
        self.set_up()
        calls = []
        self.xa.protocol.leave_progmode.side_effect = lambda *a: calls.append('leave')
        self.xa.protocol.attach.side_effect = lambda *a: calls.append('attach')
        self.xa.switch_to_debmode()
        self.assertEqual(calls, ['leave', 'attach'])

    def test_setup_debug_session(self):
        self.set_up()
        self.xa.setup_debug_session()
        self.xa.protocol.set_le16.assert_not_called()
        self.xa.protocol.set_byte.assert_called_with(Avr8Protocol.AVR8_CTXT_OPTIONS,
                                                         Avr8Protocol.AVR8_OPT_HV_UPDI_ENABLE, 0)
        self.xa.protocol.set_variant.assert_called_with(Avr8Protocol.AVR8_VARIANT_TINYX)
        self.xa.protocol.set_function.assert_called_with(Avr8Protocol.AVR8_FUNC_DEBUGGING)
        self.xa.protocol.set_interface.assert_called_with(Avr8Protocol.AVR8_PHY_INTF_PDI_1W)

    def test_setup_debug_session_with_speed_limit(self):
        self.set_up()
        self.xa.setup_debug_session(kbps=100)
        self.xa.protocol.set_le16.assert_called_with(Avr8Protocol.AVR8_CTXT_PHYSICAL,
                                                         Avr8Protocol.AVR8_PHY_XM_PDI_CLK, 100)

    # --- the device data structure handed to the tool -----------------------

    def devdata(self, device_info):
        self.xa = XTinyXAvrTarget(MagicMock(), device_info)
        self.xa.protocol = create_autospec(Avr8Protocol)
        self.xa.setup_config(device_info)
        self.xa.protocol.write_device_data.assert_called_once()
        return self.xa.protocol.write_device_data.call_args[0][0]

    def test_setup_config_attiny3217(self):
        d = self.devdata(DEVICE_INFO_3217)
        self.assertEqual(len(d), 0x30)
        self.assertEqual(binary.unpack_le16(d[0x00:0x02]), 0x8000)    # flash base
        self.assertEqual(d[0x02], 128)                                # flash page size
        self.assertEqual(d[0x03], 64)                                 # eeprom page size
        self.assertEqual(binary.unpack_le16(d[0x04:0x06]), 0x1000)    # nvmctrl
        self.assertEqual(binary.unpack_le16(d[0x06:0x08]), 0x0F80)    # ocd
        self.assertEqual(binary.unpack_le32(d[0x12:0x16]), 0x8000)    # flash size
        self.assertEqual(binary.unpack_le16(d[0x16:0x18]), 0x100)     # eeprom size
        self.assertEqual(d[0x1A], 9)                                  # fuse bytes (the whole fuse area)
        self.assertEqual(binary.unpack_le16(d[0x20:0x22]), 0x1400)    # eeprom base
        self.assertEqual(binary.unpack_le16(d[0x22:0x24]), 0x1300)    # user row base
        self.assertEqual(binary.unpack_le16(d[0x24:0x26]), 0x1100)    # signature row base
        self.assertEqual(binary.unpack_le16(d[0x26:0x28]), 0x1280)    # fuses base
        self.assertEqual(binary.unpack_le16(d[0x28:0x2A]), 0x128A)    # lockbits base
        self.assertEqual(binary.unpack_le16(d[0x2A:0x2C]), 0x9522)    # device id, lower two bytes
        self.assertEqual(d[0x2C], 0x00)                               # flash base, high byte
        self.assertEqual(d[0x2D], 0x00)                               # flash page size, high byte
        self.assertEqual(d[0x2E], 0x00)                               # 16-bit addressing
        self.assertEqual(d[0x2F], 0x00)                               # no HV implementation

    def test_setup_config_24bit_addressing(self):
        d = self.devdata(DEVICE_INFO_DA48)
        self.assertEqual(binary.unpack_le16(d[0x00:0x02]), 0x0000)    # flash base, lower bytes
        self.assertEqual(d[0x2C], 0x80)                               # flash base, high byte
        self.assertEqual(d[0x02], 512 & 0xFF)                         # flash page size, low byte
        self.assertEqual(d[0x2D], 512 >> 8)                           # flash page size, high byte
        self.assertEqual(binary.unpack_le32(d[0x12:0x16]), 0x20000)   # flash size
        self.assertEqual(d[0x2E], 0x01)                               # 24-bit addressing
        self.assertEqual(d[0x2F], 0x01)                               # HV implementation

    def test_setup_config_without_device_info(self):
        self.set_up()
        for empty in ({}, None):                       # None is turned into {} first
            with self.assertRaises(KeyError):
                self.xa.setup_config(empty)


class TestXAvr8TargetXmega(TestCase):
    """
    The XMEGA class is not reachable through PyAvrOCD yet, since PDI targets are not
    supported. These tests pin its behavior for the day they are.
    """

    def setUp(self):
        self.xa = XXmegaAvrTarget(MagicMock())
        self.xa.protocol = create_autospec(Avr8Protocol)

    def test_setup_debug_session(self):
        self.xa.setup_debug_session()
        self.xa.protocol.set_variant.assert_called_with(Avr8Protocol.AVR8_VARIANT_XMEGA)
        self.xa.protocol.set_function.assert_called_with(Avr8Protocol.AVR8_FUNC_DEBUGGING)
        self.xa.protocol.set_interface.assert_called_with(Avr8Protocol.AVR8_PHY_INTF_PDI)

    def test_regfile_read(self):
        self.xa.protocol.regfile_read.return_value = bytearray(range(32))
        self.assertEqual(self.xa.regfile_read(), bytearray(range(32)))

    def test_regfile_write(self):
        self.xa.regfile_write(bytearray(range(32)))
        self.xa.protocol.regfile_write.assert_called_with(bytearray(range(32)))
