"""
The test suit for the XNvmAccessProviderCmsisDapDebugwire class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
from unittest.mock import Mock, MagicMock, patch, create_autospec, call
from unittest import TestCase

from pyedbglib.protocols.avr8protocol import Avr8Protocol

from pymcuprog.deviceinfo import deviceinfo
from pymcuprog.pymcuprog_errors import PymcuprogError

from pyavrocd.xnvmupdi import XNvmAccessProviderCmsisDapUpdi
from pyavrocd.xavr8target import XTinyXAvrTarget
from pyavrocd.deviceinfo.devices.atmega4809 import DEVICE_INFO

class TestXNvmAccessProviderCmsisDapDebugwire(TestCase):

    def setUp(self):
        self.nvm = None
        self.device_info = None
        self.memory_info = None

    @patch('pyavrocd.xnvmdebugwire.XTinyAvrTarget',MagicMock())
    def set_up(self):
        self.nvm = XNvmAccessProviderCmsisDapUpdi(MagicMock(), DEVICE_INFO, manage=None)
        self.nvm.avr = create_autospec(XTinyXAvrTarget)
        self.device_info = deviceinfo.getdeviceinfo("pyavrocd.deviceinfo.devices." + "atmega4809")
        self.memory_info = deviceinfo.DeviceMemoryInfo(self.device_info)
        self.nvm.logger_local.info = Mock()

    def test_init(self):
        self.set_up()
        self.assertTrue(self.nvm.avr is not None)

    # --- helpers ---

    def _real_memtypes(self):
        self.nvm.avr.memtype_write_from_string.side_effect = XTinyXAvrTarget.memtype_write_from_string
        self.nvm.avr.memtype_read_from_string.side_effect = XTinyXAvrTarget.memtype_read_from_string

    # --- read ---

    @patch('pymcuprog.nvmupdi.NvmAccessProviderCmsisDapUpdi.read')
    def test_read_drops_prog_mode(self, mock_read):
        self.set_up()
        mock_read.return_value = bytearray(b'ab')
        mi = self.memory_info.memory_info_by_name('flash')
        self.assertEqual(self.nvm.read(mi, 5, 2, prog_mode=True), bytearray(b'ab'))
        mock_read.assert_called_once_with(mi, 5, 2)

    # --- write ---

    def test_write_flash_aligned_single_page(self):
        self.set_up()
        self._real_memtypes()
        mi = self.memory_info.memory_info_by_name('flash')
        data = bytearray(range(0x80))
        self.nvm.write(mi, 0x100, data)
        self.nvm.avr.write_memory_section.assert_called_once_with(
            Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE, 0x100, data, 0x80, allow_blank_skip=True)

    def test_write_flash_unaligned_two_pages(self):
        self.set_up()
        self._real_memtypes()
        mi = self.memory_info.memory_info_by_name('flash')
        data = bytearray(range(0x80))
        self.nvm.write(mi, 0x104, data)
        padded = bytearray([0xFF]*4) + data + bytearray([0xFF]*0x7C)
        self.assertEqual(self.nvm.avr.write_memory_section.call_args_list,
                         [call(Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE, 0x100, padded[:0x80], 0x80,
                                   allow_blank_skip=True),
                          call(Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE, 0x180, padded[0x80:], 0x80,
                                   allow_blank_skip=True)])

    def test_write_eeprom_no_alignment_no_padding(self):
        self.set_up()
        self._real_memtypes()
        mi = self.memory_info.memory_info_by_name('eeprom')
        data = bytearray([1, 2, 3, 4, 5])
        self.nvm.write(mi, 3, data)
        self.nvm.avr.write_memory_section.assert_called_once_with(
            Avr8Protocol.AVR8_MEMTYPE_EEPROM_ATOMIC, 0x1403, data, 0x40, allow_blank_skip=False)

    def test_write_user_row_unlocked(self):
        # characterizes the USER_ROW workaround: chunk size = data length, split at chunk boundary
        self.set_up()
        self._real_memtypes()
        mi = self.memory_info.memory_info_by_name('user_row')
        data = bytearray([1, 2, 3, 4])
        self.nvm.write(mi, 2, data)
        memtype = XTinyXAvrTarget.memtype_write_from_string('user_row')
        self.assertEqual(self.nvm.avr.write_memory_section.call_args_list,
                         [call(memtype, 0x1302, bytearray([1, 2]), 4, allow_blank_skip=False),
                          call(memtype, 0x1304, bytearray([3, 4]), 4, allow_blank_skip=False)])

    def test_write_user_row_locked_device(self):
        self.set_up()
        self._real_memtypes()
        self.nvm.options['user-row-locked-device'] = True
        mi = self.memory_info.memory_info_by_name('user_row')
        data = bytearray([1, 2, 3, 4])
        self.nvm.write(mi, 0, data)
        memtype = XTinyXAvrTarget.memtype_write_from_string('user_row')
        self.nvm.avr.write_memory_section.assert_called_once_with(
            memtype, 0x1300, data + bytearray([0xFF]*0x3C), 0x40, allow_blank_skip=False)

    def test_write_fuse_single_byte(self):
        self.set_up()
        self._real_memtypes()
        mi = self.memory_info.memory_info_by_name('fuses')
        self.nvm.write(mi, 5, bytearray([0xAB]))
        self.nvm.avr.write_memory_section.assert_called_once_with(
            Avr8Protocol.AVR8_MEMTYPE_FUSES, 0x1285, bytearray([0xAB]), 1, allow_blank_skip=False)

    def test_write_unsupported_memtype(self):
        self.set_up()
        self.nvm.avr.memtype_write_from_string.return_value = 0
        mi = self.memory_info.memory_info_by_name('flash')
        with self.assertRaises(PymcuprogError):
            self.nvm.write(mi, 0, bytearray([0]))
        self.nvm.avr.write_memory_section.assert_not_called()

    # --- erase_page ---

    def test_erase_page_is_noop(self):
        self.set_up()
        self.assertFalse(self.nvm.erase_page(0x100, self.memory_info.memory_info_by_name('flash'), False))
        self.assertEqual(self.nvm.avr.mock_calls, [])

    # --- erase_chip ---

    def test_erase_chip_from_debug_mode(self):
        self.set_up()
        self.assertTrue(self.nvm.erase_chip(prog_mode=False))
        self.assertEqual(self.nvm.avr.mock_calls,
                         [call.switch_to_progmode(), call.erase(Avr8Protocol.ERASE_CHIP, 0),
                          call.switch_to_debmode()])

    def test_erase_chip_in_prog_mode(self):
        self.set_up()
        self.assertTrue(self.nvm.erase_chip(prog_mode=True))
        self.assertEqual(self.nvm.avr.mock_calls, [call.erase(Avr8Protocol.ERASE_CHIP, 0)])

    def test_erase_chip_eesave_data_unknown(self):
        self.set_up()
        self.nvm.manage = ['eesave']
        self.nvm.device_info = {k: v for k, v in self.nvm.device_info.items()
                                    if k not in ('eesave_base', 'eesave_mask')}
        self.nvm.erase_chip(prog_mode=True)
        self.assertEqual(self.nvm.avr.mock_calls, [call.erase(Avr8Protocol.ERASE_CHIP, 0)])

    # On AVR8X, EESAVE (SYSCFG0 bit 0) is active HIGH (1 = EEPROM is retained during chip erase),
    # and new fuse values only take effect after a reset (leaving/re-entering programming mode).

    def test_erase_chip_eesave_already_set(self):
        self.set_up()
        self.nvm.manage = ['eesave']
        self.nvm.avr.memory_read.return_value = bytearray([0xC9]) # EESAVE=1: EEPROM retained
        self.nvm.erase_chip(prog_mode=True)
        self.nvm.avr.memory_write.assert_not_called()
        self.assertEqual(self.nvm.avr.mock_calls,
                         [call.memory_read(Avr8Protocol.AVR8_MEMTYPE_FUSES, 0x5, 1),
                          call.erase(Avr8Protocol.ERASE_CHIP, 0)])

    def test_erase_chip_eesave_temporarily_set(self):
        self.set_up()
        self.nvm.manage = ['eesave']
        self.nvm.avr.memory_read.return_value = bytearray([0xC8]) # EESAVE=0: EEPROM would be erased
        self.nvm.erase_chip(prog_mode=True)
        self.assertEqual(self.nvm.avr.mock_calls,
                         [call.memory_read(Avr8Protocol.AVR8_MEMTYPE_FUSES, 0x5, 1),
                          call.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, 0x5, bytearray([0xC9])),
                          call.leave_progmode(), call.enter_progmode(),
                          call.erase(Avr8Protocol.ERASE_CHIP, 0),
                          call.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, 0x5, bytearray([0xC8])),
                          call.leave_progmode(), call.enter_progmode()])

    def test_erase_chip_eesave_from_debug_mode(self):
        self.set_up()
        self.nvm.manage = ['eesave']
        self.nvm.avr.memory_read.return_value = bytearray([0xC8])
        self.nvm.erase_chip(prog_mode=False)
        self.assertEqual(self.nvm.avr.mock_calls[0], call.switch_to_progmode())
        self.assertEqual(self.nvm.avr.mock_calls[-1], call.switch_to_debmode())

    # --- read_device_id ---

    def test_read_device_id(self):
        self.set_up()
        self.nvm.avr.memtype_read_from_string.return_value = 0x55
        self.nvm.avr.memory_read.side_effect = [bytearray([0x1E, 0x96, 0x51]), bytearray([0x21])]
        self.assertEqual(self.nvm.read_device_id(), bytearray([0x51, 0x96, 0x1E]))
        self.assertEqual(self.nvm.avr.memory_read.call_args_list,
                         [call(0x55, 0x1100, 3), call(0x55, 0xF01, 1)])
