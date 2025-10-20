"""
The test suit for the XTinyAvrTarget class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
from unittest.mock import  MagicMock, call, create_autospec
from unittest import TestCase

from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.util import binary

from pyavrocd.xavr8target import XMegaAvrJtagTarget
from pyavrocd.deviceinfo.devices.atmega644 import DEVICE_INFO


class TestXAvr8TargetJtag(TestCase):

    def setUp(self):
        self.xa = None

    def set_up(self):
        self.xa = XMegaAvrJtagTarget(MagicMock())
        self.xa.protocol = create_autospec(Avr8Protocol)

    def test_memtype_read_from_string(self):
        self.set_up()
        self.assertEqual(self.xa.memtype_read_from_string('flash'), Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE)
        self.assertEqual(self.xa.memtype_read_from_string('eeprom'), Avr8Protocol.AVR8_MEMTYPE_EEPROM)
        self.assertEqual(self.xa.memtype_read_from_string('internal_sram'), Avr8Protocol.AVR8_MEMTYPE_SRAM)
        self.assertEqual(self.xa.memtype_read_from_string('signatures'), Avr8Protocol.AVR8_MEMTYPE_SIGNATURE)

    def test_memtype_write_from_string(self):
        self.set_up()
        self.assertEqual(self.xa.memtype_write_from_string('flash'), Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE)
        self.assertEqual(self.xa.memtype_write_from_string('eeprom'), Avr8Protocol.AVR8_MEMTYPE_EEPROM)
        self.assertEqual(self.xa.memtype_write_from_string('internal_sram'), Avr8Protocol.AVR8_MEMTYPE_SRAM)
        self.assertEqual(self.xa.memtype_write_from_string('signatures'), Avr8Protocol.AVR8_MEMTYPE_SIGNATURE)

    def test_switch_to_progmode(self):
        self.set_up()
        self.xa.switch_to_progmode()
        self.xa.protocol.detach.assert_called_once()
        self.xa.protocol.deactivate_physical.assert_called_once()
        self.xa.protocol.activate_physical.assert_called_once()
        self.xa.protocol.enter_progmode()

    def test_setup_config(self):
        self.set_up()
        self.xa.setup_config(DEVICE_INFO)
        self.xa.protocol.write_device_data.assert_has_calls([call(bytearray([0x00, 0x01, # flash page bytes
                                                                             0x00, 0x00, 0x01, 0x00, # flash bytes
                                                                             0x00, 0x00, 0x00, 0x00, # flash base
                                                                             0x00, 0xff, 0x00, 0x00, # boot base
                                                                             0x00, 0x01, # sram base
                                                                             0x00, 0x08, # eeprom bytes
                                                                             0x08, # eeprom page bytes
                                                                             0x03, # OCD rev.
                                                                             0x01, # page buffers/flash block
                                                                             0x00, 0x00, 0x00, # gap
                                                                             0x31, # OCD addr
                                                                             0x22, # EEARH
                                                                             0x21, # EEARL
                                                                             0x1F, # EECR
                                                                             0x20, # EEDR
                                                                             0x57, # SPMCSR
                                                                             0x46 # OSCCAL
                                                                             ]))])

    def test_regfile_read(self):
        self.set_up()
        rfile = bytearray(list(range(32)))
        self.xa.protocol.memory_read.return_value=rfile
        self.assertEqual(self.xa.regfile_read(),rfile)
        self.xa.protocol.memory_read.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0, 32)

    def test_regfile_write(self):
        self.set_up()
        rfile = bytearray(list(range(32)))
        self.xa.regfile_write(rfile)
        self.xa.protocol.memory_write.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0, rfile)

    def test_statreg_read(self):
        self.set_up()
        self.xa.protocol.memory_read.return_value=bytearray([0x7F])
        self.assertEqual(self.xa.statreg_read(), b'\x7F')
        self.xa.protocol.memory_read.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5F, 1)

    def test_statreg_write(self):
        self.set_up()
        self.xa.statreg_write(b'\x06')
        self.xa.protocol.memory_write.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5F, b'\x06')

    def test_stack_pointer_read(self):
        self.set_up()
        self.xa.protocol.memory_read.return_value='b\x23\x01'
        self.assertEqual(self.xa.stack_pointer_read(),'b\x23\x01')
        self.xa.protocol.memory_read.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5D, 2)

    def test_stack_pointer_write(self):
        self.set_up()
        self.xa.stack_pointer_write('b\x23\x01')
        self.xa.protocol.memory_write.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5D, 'b\x23\x01')

    def test_hardware_breakpoint_set_fail(self):
        self.set_up()
        self.assertEqual(self.xa.hardware_breakpoint_set(4, 0x200),0)

    def test_hardware_breakpoint_set_right(self):
        self.set_up()
        self.xa.protocol.check_response.return_value = None
        self.assertEqual(self.xa.hardware_breakpoint_set(2, 0x200), None)
        self.xa.protocol.jtagice3_command_response.assert_called_with(bytearray([Avr8Protocol.CMD_AVR8_HW_BREAK_SET, Avr8Protocol.CMD_VERSION0, 1, 2]) +
            binary.pack_le32(0x200) +
            bytearray([3]))

    def test_hardware_breakpoint_clear_right(self):
        self.set_up()
        self.xa.protocol.check_response.return_value = None
        self.assertEqual(self.xa.hardware_breakpoint_clear(3), None)
        self.xa.protocol.jtagice3_command_response.assert_called_with(bytearray([Avr8Protocol.CMD_AVR8_HW_BREAK_CLEAR, Avr8Protocol.CMD_VERSION0, 3]))

    def test_breakpoint_clear(self):
        self.set_up()
        self.assertEqual(self.xa.breakpoint_clear(),None)
        self.xa.protocol.jtagice3_command_response.assert_has_calls([
            call(bytearray([Avr8Protocol.CMD_AVR8_HW_BREAK_CLEAR, Avr8Protocol.CMD_VERSION0, 1])),
            call(bytearray([Avr8Protocol.CMD_AVR8_HW_BREAK_CLEAR, Avr8Protocol.CMD_VERSION0, 2])),
            call(bytearray([Avr8Protocol.CMD_AVR8_HW_BREAK_CLEAR, Avr8Protocol.CMD_VERSION0, 3]))])
        self.assertEqual(self.xa.protocol.jtagice3_command_response.call_count,3)
