"""
The test suit for the XTinyAvrTarget class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
from unittest.mock import  MagicMock, create_autospec
from unittest import TestCase

from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.util import binary

from pyavrocd.xavr8target import XTinyXAvrTarget
#from pyavrocd.deviceinfo.devices.atmega4809 import DEVICE_INFO


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

    def test_statreg_read(self):
        self.set_up()
        self.xa.protocol.memory_read.return_value=bytearray([0x7F])
        self.assertEqual(self.xa.statreg_read(), b'\x7F')
        self.xa.protocol.memory_read.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_OCD,
                                                            Avr8Protocol.AVR8_MEMTYPE_OCD_SREG, 1)

    def test_statreg_write(self):
        self.set_up()
        self.xa.statreg_write(b'\x06')
        self.xa.protocol.memory_write.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_OCD,
                                                            Avr8Protocol.AVR8_MEMTYPE_OCD_SREG, b'\x06')

    def test_stack_pointer_write(self):
        self.set_up()
        self.xa.stack_pointer_write('b\x23\x01')
        self.xa.protocol.memory_write.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_OCD, 0x18, 'b\x23\x01')

    def test_hardware_breakpoint_set_fail(self):
        self.set_up()
        self.assertEqual(self.xa.hardware_breakpoint_set(2, 0x200),0)

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
