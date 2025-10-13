"""
The test suit for the XNvmAccessProviderCmsisDapDebugwire class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
import logging
from unittest.mock import Mock, MagicMock, patch, call, create_autospec
from unittest import TestCase

from pymcuprog.deviceinfo import deviceinfo

from pyedbglib.protocols.avr8protocol import Avr8Protocol

from pyavrocd.xnvmmegaavrjtag import XNvmAccessProviderCmsisDapMegaAvrJtag
from pyavrocd.xavr8target import XMegaAvrJtagTarget
from pyavrocd.deviceinfo.devices.atmega644 import DEVICE_INFO

logging.basicConfig(level=logging.DEBUG)

class TestXNvmAccessProviderCmsisDapDebugwire(TestCase):

    @patch('pyavrocd.xnvmdebugwire.XTinyAvrTarget',MagicMock())
    def setUp(self):
        self.nvm = XNvmAccessProviderCmsisDapMegaAvrJtag(MagicMock(), DEVICE_INFO, manage=None)
        self.nvm.avr = create_autospec(XMegaAvrJtagTarget)
        self.device_info = deviceinfo.getdeviceinfo("pyavrocd.deviceinfo.devices." + "atmega644")
        self.memory_info = deviceinfo.DeviceMemoryInfo(self.device_info)
        self.nvm.logger_local.info = Mock()

    def test_read_flash_page(self):
        rpage = bytearray(list(range(0x40)))
        self.nvm.avr.read_memory_section.return_value=rpage
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE
        self.assertEqual(self.nvm.read(self.memory_info.memory_info_by_name('flash'), 0x100, 0x40), rpage)
        self.nvm.avr.memtype_read_from_string.assert_called_with('flash')
        self.nvm.avr.read_memory_section.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SPM, 0x100, 0x40, 0x40)

    def test_read_flash_arbitrary(self):
        rpage = bytearray(list(range(0x60)))
        self.nvm.avr.read_memory_section.return_value=rpage
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE
        self.assertEqual(self.nvm.read(self.memory_info.memory_info_by_name('flash'), 0x100, 0x60), rpage)
        self.nvm.avr.memtype_read_from_string.assert_called_with('flash')
        self.nvm.avr.read_memory_section.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SPM, 0x100, 0x60, 0x60)

    def test_read_flash_page_prog_mode(self):
        rpage = bytearray(list(range(0x40)))
        self.nvm.avr.read_memory_section.return_value=rpage
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE
        self.assertEqual(self.nvm.read(self.memory_info.memory_info_by_name('flash'), 0x100, 0x40,prog_mode=True), rpage)
        self.nvm.avr.memtype_read_from_string.assert_called_with('flash')
        self.nvm.avr.read_memory_section.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE, 0x100, 0x40, 0x40)

    def test_read_eeprom(self):
        rpage = bytearray(list(range(0x2)))
        self.nvm.avr.read_memory_section.return_value=rpage
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_EEPROM
        self.assertEqual(self.nvm.read(self.memory_info.memory_info_by_name('eeprom'), 0x100, 0x02), rpage)
        self.nvm.avr.memtype_read_from_string.assert_called_with('eeprom')
        self.nvm.avr.read_memory_section.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_EEPROM, 0x100, 0x02, 0x02)

    def test_read_eeprom_prog_mode(self):
        rpage = bytearray(list(range(0x2)))
        self.nvm.avr.read_memory_section.return_value=rpage
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_EEPROM
        self.assertEqual(self.nvm.read(self.memory_info.memory_info_by_name('eeprom'), 0x100, 0x02,prog_mode=True), rpage)
        self.nvm.avr.memtype_read_from_string.assert_called_with('eeprom')
        self.nvm.avr.read_memory_section.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_EEPROM_PAGE, 0x100, 0x02, 0x02)

    def test_read_sram(self):
        rpage = bytearray(list(range(0x9)))
        self.nvm.avr.read_memory_section.return_value=rpage
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_SRAM
        self.assertEqual(self.nvm.read(self.memory_info.memory_info_by_name('internal_sram'), 0x200-0x100, 0x09), rpage)
        self.nvm.avr.memtype_read_from_string.assert_called_with('internal_sram')
        self.nvm.avr.read_memory_section.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x200, 0x09, 0x09)

    def test_write_flash_page(self):
        wpage = bytearray(list(range(0x100)))
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE
        self.nvm.write(self.memory_info.memory_info_by_name('flash'), 0x200, wpage)
        self.nvm.avr.write_memory_section.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE,
                                                                 0x200, wpage, 0x100, allow_blank_skip=True)


    def test_write_eeprom(self):
        wpage = bytearray(list(range(0x07)))
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_EEPROM_PAGE
        self.nvm.write(self.memory_info.memory_info_by_name('eeprom'), 0x100, wpage)
        self.nvm.avr.write_memory_section.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_EEPROM,
                                                                 0x100, wpage, 0x07, allow_blank_skip=False)

    def test_write_sram(self):
        wpage = bytearray(list(range(0x05)))
        self.nvm.avr.memtype_read_from_string.return_value=Avr8Protocol.AVR8_MEMTYPE_SRAM
        self.nvm.write(self.memory_info.memory_info_by_name('internal_sram'), 0x200-0x100, wpage)
        self.nvm.avr.write_memory_section.assert_has_calls([call(Avr8Protocol.AVR8_MEMTYPE_SRAM,
                                                                 0x200, wpage, len(wpage), allow_blank_skip=False)],any_order=True)

    def test_erase_page(self):
        self.nvm.avr.protocol = Mock()
        self.assertTrue(self.nvm.erase_page(0x100, False))
        self.nvm.avr.switch_to_debmode.assert_not_called()
        self.nvm.avr.switch_to_progmode.assert_not_called()
        self.nvm.avr.protocol.jtagice3_command_response.assert_called_once_with(b'P\x00\x00\x01\x00\x00')

    def test_erase_page_progmode(self):
        self.nvm.avr.protocol = Mock()
        self.assertTrue(self.nvm.erase_page(0x100, True))
        self.nvm.avr.switch_to_debmode.assert_called_once()
        self.nvm.avr.switch_to_progmode.assert_called_once()
        self.nvm.avr.protocol.jtagice3_command_response.assert_called_once_with(b'P\x00\x00\x01\x00\x00')

    def test_erase_chip(self):
        self.assertTrue(self.nvm.erase_chip(False))
        self.nvm.avr.switch_to_progmode.assert_called_once()
        self.nvm.avr.switch_to_debmode.assert_called_once()
        self.nvm.avr.erase.assert_called_once_with(0,0)

    def test_erase_chip_progmode(self):
        self.assertTrue(self.nvm.erase_chip(True))
        self.nvm.avr.switch_to_progmode.assert_not_called()
        self.nvm.avr.switch_to_debmode.assert_not_called()
        self.nvm.avr.erase.assert_called_once_with(0,0)

    def test_erase_chip_progmode_eesave(self):
        self.nvm.manage = [ 'eesave' ]
        self.nvm.avr.memory_read.return_value = bytearray([0xFF])
        self.assertTrue(self.nvm.erase_chip(True))
        self.nvm.avr.memory_read.assert_called_once_with(Avr8Protocol.AVR8_MEMTYPE_FUSES, 1, 1)
        self.nvm.avr.memory_write.assert_has_calls([call(Avr8Protocol.AVR8_MEMTYPE_FUSES, 1, bytearray([0xF7])),
                                                    call(Avr8Protocol.AVR8_MEMTYPE_FUSES, 1, bytearray([0xFF]))])
        self.nvm.avr.switch_to_progmode.assert_not_called()
        self.nvm.avr.switch_to_debmode.assert_not_called()
        self.nvm.avr.erase.assert_called_once_with(0,0)
