"""
The test suit for the Memory class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
import logging
from unittest.mock import Mock, MagicMock, call, create_autospec
from unittest import TestCase
from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.errors import FatalError
from pyavrocd.memory import Memory
from pyavrocd.monitor import MonitorCommand

logging.basicConfig(level=logging.CRITICAL)

class TestMemory(TestCase):

    def setUp(self):
        mock_dbg = create_autospec(XAvrDebugger, spec_set=False, instance=True)
        mock_mon = create_autospec(MonitorCommand, specSet=True, instance=True)
        mock_dbg.memory_info = MagicMock()
        mock_dbg.device_info = MagicMock()
        mock_dbg.transport = MagicMock()
        mock_dbg.device = Mock()
        mock_dbg.device.avr = Mock()

        mock_dbg.memory_info.memory_info_by_name('flash')['size'].__gt__ = lambda self, compare: False
        # setting up the GbdHandler instance we want to test
        self.mem = Memory(mock_dbg, mock_mon)
        self.mem._flash_start = 0
        self.mem._flash_page_size = 2
        self.mem._flash_size = 12
        self.mem._multi_buffer = 3
        self.mem._multi_page_size = self.mem._multi_buffer*self.mem._flash_page_size
        self.mem._sram_start = 10
        self.mem._sram_size = 15
        self.mem._eeprom_start = 0
        self.mem._eeprom_size = 5
        self.mem._flashmemtype = 123

    def test_init_flash_True(self):
        self.assertEqual(self.mem._flash,bytearray())
        self.assertEqual(self.mem._flashmem_start_prog,0)

    def test_is_flash_empty_False(self):
        self.assertTrue(self.mem.is_flash_empty())
        self.mem._flash = bytearray(1)
        self.assertFalse(self.mem.is_flash_empty())

    def test_flash_filled(self):
        self.assertEqual(self.mem.flash_filled(), 0)
        self.mem._flash = bytearray(12)
        self.assertEqual(self.mem.flash_filled(), 12)

    def test_readmem_sram(self):
        sram = list(reversed(range(15)))
        def access_sram(ix, length):
            return bytearray(sram[ix:ix+length])
        self.mem.dbg.sram_read = MagicMock(side_effect=access_sram)
        self.assertEqual(self.mem.readmem("800000", "4"), bytearray([14, 13, 12, 11]))

    def test_readmem_sram_masked_register_one_byte(self):
        self.mem._masked_registers = [15, 1, 6]
        self.assertEqual(self.mem.readmem("800001", "1"), bytearray([0xFF]))
        self.mem.dbg.sram_read.assert_not_called()

    def test_readmem_sram_masked_register_bytearray(self):
        self.mem._masked_registers = [15, 1, 6]
        sram = list(reversed(range(15)))
        def access_sram(ix, length):
            return bytearray(sram[ix:ix+length])
        self.mem.dbg.sram_read = MagicMock(side_effect=access_sram)
        self.assertEqual(self.mem.readmem("800005", "3"), bytearray([9, 0xFF, 7]))
        self.assertEqual(self.mem.readmem("800004", "3"), bytearray([10, 9, 0xFF]))

    def test_readmem_eprom(self):
        eeprom = list(range(5))
        def access_eeprom(ix, length):
            return bytearray(eeprom[ix:ix+length])
        self.mem.dbg.eeprom_read = MagicMock(side_effect=access_eeprom)
        self.assertEqual(self.mem.readmem("810001", "3"), bytearray([1, 2, 3]))

    def test_readmem_flash_cached(self):
        self.mem._flash = bytearray([10,11,12,13])
        self.mem.dbg.flash_read.return_value = bytearray([21,22])
        self.assertEqual(self.mem.readmem("0001", "3"), bytearray([11, 12, 13]))
        self.assertEqual(self.mem.readmem("0003", "2"), bytearray([22, 21]))
        self.mem.dbg.flash_read.assert_has_calls([call(2,2), call(4,2)])

    def test_readmem_undef(self):
        self.assertEqual(self.mem.readmem("820000", "2"),bytearray())

    # flash_read has been tested above already

    def test_flash_read_word(self):
        self.mem._flash = bytearray([0x10, 0x11, 0x12, 0x13])
        self.assertEqual(self.mem.flash_read_word(2), 0x1312)

    def test_store_to_cache_error(self):
        self.mem._flash = bytearray(10)
        with self.assertRaises(FatalError):
            self.mem.store_to_cache(9, bytearray([1,2,3]))

    def test_store_to_cache_error_ok(self):
        self.mem._flash = bytearray(5)
        self.mem.store_to_cache(10, bytearray([0x88]*3))
        self.assertEqual(self.mem._flash, bytearray([0, 0, 0, 0, 0, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x88, 0x88, 0x88]))

    def test_flash_pages_no_write(self):
        self.mem.dbg.device.avr.write_memory_section = Mock()
        self.mem._flash = bytearray(range(4))
        self.mem.dbg.flash_read.side_effect = [bytearray([0,1]), bytearray([2,3]),
                                                   bytearray([0,1]), bytearray([2,3]), bytearray([0xFF,0xFF])]
        self.mem.flash_pages()
        self.assertEqual(self.mem.dbg.flash_read.call_count, 3)

    def test_flash_pages_write(self):
        self.mem.dbg.device.avr.write_memory_section = Mock()
        self.mem._flash = bytearray(range(4))
        self.mem.dbg.flash_read.side_effect = [bytearray([0,0]), bytearray([2,3]), bytearray([0,0]),
                                                   bytearray([0,1]), bytearray([2,3]), bytearray([0xFF,0xFF])]
        self.mem.flash_pages()
        self.assertEqual(self.mem.dbg.flash_read.call_count, 6)
        fmt = self.mem.dbg.device.avr.memtype_write_from_string('flash')
        self.mem.dbg.device.avr.write_memory_section.assert_called_with(fmt, 0, bytearray([0,1,2,3,0xFF,0xFF]),
                                                                            2, allow_blank_skip=False)

    def test_flash_pages_error(self):
        self.mem.dbg.device.avr.write_memory_section = Mock()
        self.mem._flash = bytearray(range(4))
        self.mem.dbg.flash_read.return_value = bytearray(2)
        with self.assertRaises(FatalError):
            self.mem.flash_pages()

    def test_memory_map(self):
        self.assertEqual(self.mem.memory_map(), 'l<memory-map><memory type="ram" start="0x800000" length="0x10005"/>' + \
                             '<memory type="flash" start="0x0" length="0xC">' + \
                             '<property name="blocksize">0x6</property>' + \
                             '</memory></memory-map>')
