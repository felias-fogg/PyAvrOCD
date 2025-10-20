"""
The test suit for the Memory class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
from unittest.mock import Mock, MagicMock, call, create_autospec
from unittest import TestCase
from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.errors import FatalError
from pyavrocd.memory import Memory
from pyavrocd.monitor import MonitorCommand

class TestMemory(TestCase):

    def setUp(self):
        self.mem = None

    def set_up(self):
        mock_dbg = create_autospec(XAvrDebugger, spec_set=False, instance=True)
        mock_mon = create_autospec(MonitorCommand, specSet=True, instance=True)
        mock_dbg.memory_info = MagicMock()
        mock_dbg.device_info = MagicMock()
        mock_dbg.transport = MagicMock()
        mock_dbg.device = Mock()
        mock_dbg.device.avr = Mock()
        mock_dbg.get_iface.return_value = "debugwire"
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
        self.mem._eeprom_size = 10
        self.mem._flashmemtype = 123
        self.mem.programming_mode = False

    def test_init_flash_True(self):
        self.set_up()
        self.assertEqual(self.mem._flash,bytearray())
        self.assertEqual(self.mem._flashmem_start_prog,0)

    def test_is_flash_empty_False(self):
        self.set_up()
        self.assertTrue(self.mem.is_flash_empty())
        self.mem._flash = bytearray(1)
        self.assertFalse(self.mem.is_flash_empty())

    def test_flash_filled(self):
        self.set_up()
        self.assertEqual(self.mem.flash_filled(), 0)
        self.mem._flash = bytearray(12)
        self.assertEqual(self.mem.flash_filled(), 12)

    def test_readmem_sram(self):
        self.set_up()
        sram = list(reversed(range(15)))
        def access_sram(ix, length):
            return bytearray(sram[ix:ix+length])
        self.mem.dbg.sram_read = MagicMock(side_effect=access_sram)
        self.assertEqual(self.mem.readmem("800000", "4"), bytearray([14, 13, 12, 11]))

    def test_readmem_sram_masked_register_one_byte(self):
        self.set_up()
        self.mem._masked_registers = [15, 1, 6]
        self.assertEqual(self.mem.readmem("800001", "1"), bytearray([0x00]))
        self.mem.dbg.sram_read.assert_not_called()

    def test_readmem_sram_masked_register_bytearray(self):
        self.set_up()
        self.mem._masked_registers = [15, 1, 6]
        sram = list(reversed(range(15)))
        def access_sram(ix, length):
            return bytearray(sram[ix:ix+length])
        self.mem.dbg.sram_read = MagicMock(side_effect=access_sram)
        self.assertEqual(self.mem.readmem("800005", "3"), bytearray([9, 0x00, 7]))
        self.assertEqual(self.mem.readmem("800004", "3"), bytearray([10, 9, 0x00]))

    def test_readmem_eeprom(self):
        self.set_up()
        self.mem.dbg.device.read.return_value=bytearray([1,2,3])
        self.assertEqual(self.mem.readmem("810001", "3"), bytearray([1, 2, 3]))

    def test_readmem_flash_cached(self):
        self.set_up()
        self.mem._flash = bytearray([10,11,12,13])
        self.mem.dbg.flash_read.return_value = bytearray([21,22])
        self.assertEqual(self.mem.readmem("0001", "3"), bytearray([11, 12, 13]))
        self.assertEqual(self.mem.readmem("0003", "2"), bytearray([22, 21]))
        self.mem.dbg.flash_read.assert_has_calls([call(2,2), call(4,2)])

    def test_readmem_fuse(self):
        self.set_up()
        self.assertEqual(self.mem.readmem("820000", "3"),bytearray([0xFF, 0xFF, 0xFF]))

    def test_readmem_lock(self):
        self.set_up()
        self.assertEqual(self.mem.readmem("830000", "1"),bytearray([0xFF]))

    def test_readmem_sig(self):
        self.set_up()
        self.assertEqual(self.mem.readmem("840000", "2"),bytearray([0xFF, 0xFF]))

    def test_readmem_usig(self):
        self.set_up()
        self.assertEqual(self.mem.readmem("850000", "4"),bytearray([0xFF, 0xFF, 0xFF, 0xFF]))

    def test_readmem_undef(self):
        self.set_up()
        self.assertEqual(self.mem.readmem("890000", "1"),bytearray([0xFF]))

    # flash_read has been tested above already

    def test_flash_read_word(self):
        self.set_up()
        self.mem._flash = bytearray([0x10, 0x11, 0x12, 0x13])
        self.assertEqual(self.mem.flash_read_word(2), 0x1312)

    def test_writemem_sram_ronly_register_one_byte(self):
        self.set_up()
        self.mem._ronly_registers = [15, 1, 6]
        self.assertEqual(self.mem.writemem("800001", bytearray([0x55])), "OK")
        self.mem.dbg.sram_write.assert_not_called()

    def test_writemem_sram_ronly_register_bytearray(self):
        self.set_up()
        self.mem._ronly_registers = [15, 1, 6]
        self.assertEqual(self.mem.writemem("800001", bytearray([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07])), "OK")
        self.mem.dbg.sram_write.assert_has_calls([call(2,bytearray([0x02, 0x03, 0x04, 0x05])), call(7,bytearray([0x07]))])
        self.assertEqual(self.mem.dbg.sram_write.call_count, 2)

    def test_writemem_eeprom(self):
        self.set_up()
        self.mem.dbg.device.write.return_value = None
        self.assertEqual(self.mem.writemem("810002", bytearray([1,2,3])), "OK")

    def test_writemem_fuse(self):
        self.set_up()
        self.assertEqual(self.mem.writemem("820000", bytearray([1,2,3])), "OK")

    def test_writemem_lock(self):
        self.set_up()
        self.assertEqual(self.mem.writemem("830000", bytearray([1])), "OK")

    def test_writemem_sig_wrong(self):
        self.set_up()
        self.mem.programming_mode = True
        self.mem.dbg.device_info.__getitem__.return_value = 0x1e950f
        self.assertRaises(FatalError, self.mem.writemem, "840000", bytearray([1,2,3]))

    def test_writemem_sig_right(self):
        self.set_up()
        self.mem.programming_mode = True
        self.mem.dbg.device_info.__getitem__.return_value = 0x1e950f
        self.assertEqual(self.mem.writemem("840000", bytearray([0x0f, 0x95, 0x1e])), "OK")

    def test_writemem_no_data(self):
        self.set_up()
        self.assertEqual(self.mem.writemem("810022", bytearray()), "OK")

    def test_writemem_flash_fail(self):
        self.set_up()
        self.mem.programming_mode = False
        self.assertEqual(self.mem.writemem("100", bytearray(1)), "E13")

    def test_writemem_flash_ok(self):
        self.set_up()
        self.mem.programming_mode = True
        self.assertEqual(self.mem.writemem("100", bytearray(1)), "OK")

    def test_store_to_cache_error(self):
        self.set_up()
        self.mem._flash = bytearray(10)
        with self.assertRaises(FatalError):
            self.mem.store_to_cache(9, bytearray([1,2,3]))

    def test_store_to_cache_error_ok(self):
        self.set_up()
        self.mem._flash = bytearray(5)
        self.mem.store_to_cache(10, bytearray([0x88]*3))
        self.assertEqual(self.mem._flash, bytearray([0, 0, 0, 0, 0, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x88, 0x88, 0x88]))

    def test_flash_pages_no_write(self):
        self.set_up()
        self.mem.dbg.device.avr.write_memory_section = Mock()
        self.mem.mon.is_read_before_write.return_value = True
        self.mem.mon.is_erase_before_load.return_value = False
        self.mem._flash = bytearray(range(4))
        self.mem.dbg.flash_read.side_effect = [bytearray([0,1]), bytearray([2,3]),
                                                   bytearray([0,1]), bytearray([2,3]), bytearray([0xFF,0xFF])]
        self.mem.flash_pages()
        self.assertEqual(self.mem.dbg.flash_read.call_count, 3)

    def test_flash_pages_write(self):
        self.set_up()
        self.mem.dbg.device.avr.write_memory_section = Mock()
        self.mem._flash = bytearray(range(4))
        self.mem.mon.is_read_before_write.return_value = True
        self.mem.mon.is_erase_before_load.return_value = False
        self.mem.dbg.flash_read.side_effect = [bytearray([0,0]), bytearray([2,3]), bytearray([0,0]),
                                                   bytearray([0,1]), bytearray([2,3]), bytearray([0xFF,0xFF])]
        self.mem.flash_pages()
        self.assertEqual(self.mem.dbg.flash_read.call_count, 6)
        fmt = self.mem.dbg.device.avr.memtype_write_from_string('flash')
        self.mem.dbg.device.avr.write_memory_section.assert_called_with(fmt, 0, bytearray([0,1,2,3,0xFF,0xFF]),
                                                                            2, allow_blank_skip=False)

    def test_flash_pages_error(self):
        self.set_up()
        self.mem.mon.is_verify.return_value = True
        self.mem.mon.is_read_before_write.return_value = False
        self.mem.mon.is_erase_before_load.return_value = False
        self.mem.dbg.device.avr.write_memory_section = Mock()
        self.mem._flash = bytearray(range(4))
        self.mem.dbg.flash_read.return_value = bytearray(2)
        with self.assertRaises(FatalError):
            self.mem.flash_pages()

    def test_memory_map(self):
        self.set_up()
        self.assertEqual(self.mem.memory_map(), 'l<memory-map><memory type="ram" start="0x800000" length="0x60000"/>' + \
                             '<memory type="flash" start="0x0" length="0xC">' + \
                             '<property name="blocksize">0x6</property>' + \
                             '</memory></memory-map>')
