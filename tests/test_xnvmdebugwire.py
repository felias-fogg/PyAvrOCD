"""
The test suit for the XNvmAccessProviderCmsisDapDebugwire class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
from unittest.mock import MagicMock, patch, call, create_autospec
from unittest import TestCase

from pymcuprog.deviceinfo import deviceinfo

from pyedbglib.protocols.avr8protocol import Avr8Protocol

from pyavrocd.xnvmdebugwire import XNvmAccessProviderCmsisDapDebugwire
from pyavrocd.xavr8target import XTinyAvrTarget
from pyavrocd.deviceinfo.devices.attiny85 import DEVICE_INFO

class TestXNvmAccessProviderCmsisDapDebugwire(TestCase):

    def setUp(self):
        self.nvm = None
        self.device_info = None
        self.memory_info = None

    @patch('pyavrocd.xnvmdebugwire.XTinyAvrTarget',MagicMock())
    def set_up(self):
        self.nvm = XNvmAccessProviderCmsisDapDebugwire(MagicMock(), DEVICE_INFO)
        self.nvm.avr = create_autospec(XTinyAvrTarget)
        self.device_info = deviceinfo.getdeviceinfo("pyavrocd.deviceinfo.devices." + "attiny85")
        self.memory_info = deviceinfo.DeviceMemoryInfo(self.device_info)

    def test_read_flash_page(self):
        self.set_up()
        rpage = bytearray(list(range(0x40)))
        self.nvm.avr.read_memory_section.return_value=rpage
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE
        self.assertEqual(self.nvm.read(self.memory_info.memory_info_by_name('flash'), 0x100, 0x40), rpage)
        self.nvm.avr.memtype_read_from_string.assert_called_with('flash')
        self.nvm.avr.read_memory_section.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE, 0x100, 0x40, 0x40)

    def test_read_flash_arbitrary(self):
        self.set_up()
        rpage = bytearray(list(range(0x60)))
        self.nvm.avr.read_memory_section.return_value=rpage
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE
        self.assertEqual(self.nvm.read(self.memory_info.memory_info_by_name('flash'), 0x100, 0x60), rpage)
        self.nvm.avr.memtype_read_from_string.assert_called_with('flash')
        self.nvm.avr.read_memory_section.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SPM, 0x100, 0x60, 0x60)

    def test_read_eeprom(self):
        self.set_up()
        rpage = bytearray(list(range(0x2)))
        self.nvm.avr.read_memory_section.return_value=rpage
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_EEPROM
        self.assertEqual(self.nvm.read(self.memory_info.memory_info_by_name('eeprom'), 0x100, 0x02), rpage)
        self.nvm.avr.memtype_read_from_string.assert_called_with('eeprom')
        self.nvm.avr.read_memory_section.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_EEPROM, 0x100, 0x02, 0x02)

    def test_read_sram(self):
        self.set_up()
        rpage = bytearray(list(range(0x9)))
        self.nvm.avr.read_memory_section.return_value=rpage
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_SRAM
        self.assertEqual(self.nvm.read(self.memory_info.memory_info_by_name('internal_sram'), 0x100-0x60, 0x09), rpage)
        self.nvm.avr.memtype_read_from_string.assert_called_with('internal_sram')
        self.nvm.avr.read_memory_section.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x100, 0x09, 0x09)

    def test_write_flash_page(self):
        self.set_up()
        wpage = bytearray(list(range(0x40)))
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE
        self.nvm.write(self.memory_info.memory_info_by_name('flash'), 0x100, wpage)
        self.nvm.avr.write_memory_section.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE,
                                                                 0x100, wpage, 0x40, allow_blank_skip=True)

    def test_write_flash_arbitrary(self):
        self.set_up()
        wpage = bytearray(list(range(0x70)))
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE
        self.nvm.write(self.memory_info.memory_info_by_name('flash'), 0xF0, wpage)
        self.nvm.avr.write_memory_section.assert_has_calls([call(Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE,
                                                                 0xC0, bytearray([0xFF])*0x30+wpage[:0x10], 0x40, allow_blank_skip=True),
                                                            call(Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE,
                                                                 0x100, wpage[0x10:]+bytearray([0xFF])*0x20, 0x40, allow_blank_skip=True)])

    def test_write_eeprom(self):
        self.set_up()
        wpage = bytearray(list(range(0x03)))
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_EEPROM
        self.nvm.write(self.memory_info.memory_info_by_name('eeprom'), 0x100, wpage)
        self.nvm.avr.write_memory_section.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_EEPROM,
                                                                 0x100, wpage, 0x04, allow_blank_skip=False)

    def test_write_sram(self):
        self.set_up()
        wpage = bytearray(list(range(0x05)))
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_SRAM
        self.nvm.write(self.memory_info.memory_info_by_name('internal_sram'), 0x100-0x60, wpage)
        self.nvm.avr.write_memory_section.assert_has_calls([call(Avr8Protocol.AVR8_MEMTYPE_SRAM,
                                                                 0x100, wpage, len(wpage), allow_blank_skip=False)],any_order=True)

    def test_erase_page(self):
        self.set_up()
        self.assertFalse(self.nvm.erase_page(0,False))

    def test_erase_chip(self):
        self.set_up()
        self.assertFalse(self.nvm.erase_chip(False))
