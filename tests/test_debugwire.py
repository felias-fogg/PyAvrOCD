"""
The test suit for the DebugWire class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
import logging
from unittest.mock import Mock, MagicMock, patch, create_autospec
from unittest import TestCase
#from pymcuprog.utils import read_target_voltage
from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.pyavrocd import DebugWIRE,  FatalError
from pyavrocd.deviceinfo.devices.alldevices import dev_name

logging.basicConfig(level=logging.CRITICAL)


class TestDebugWire(TestCase):

    def setUp(self):
        mock_dbg = create_autospec(XAvrDebugger, spec_set=False, instance=True)
        self.dw = DebugWIRE(mock_dbg, "atmega328")
        self.dw.dbg.device_info = MagicMock()
        self.dw.dbg.device = MagicMock()
        self.dw.dbg.memory_info = MagicMock()
        self.dw.dbg.transport = MagicMock()
        self.dw.dbg.device.read_device_id.return_value = bytearray([0x0F, 0x95]) # atmega328p

    def test_warm_start_not_ready(self):
        self.dw.dbg.device_info.__getitem__.return_value = 0x1E9514
        self.dw.dbg.setup_session.side_effect=Mock(side_effect=Exception("Test"))
        self.assertFalse(self.dw.warm_start())

    def test_warm_start_wrong_mcu(self):
        self.dw.dbg.device_info.__getitem__.return_value = 0x1E940B
        with self.assertRaises(FatalError):
            self.dw.warm_start()

    def test_warm_start_stuck(self):
        self.dw.dbg.device_info.__getitem__.return_value = 0x1E9514
        self.dw.dbg.memory_info.memory_info_by_name.return_value = { 'size' : 0x1000 }
        self.dw.dbg.program_counter_read.return_value = 0x3000
        with self.assertRaises(FatalError):
            self.dw.warm_start()
            self.dw.dbg.memory_info.memory_info_by_name.assert_called_with('flash')
            self.dw.dbg.start_debugging.assert_called_once()
            self.dw.dbg.reset.assert_called_once()
            self.dw.dbg.program_counter_read.assert_called_once()

    def test_warm_start_ok(self):
        self.dw.dbg.device_info.__getitem__.return_value = 0x1E9514
        self.dw.dbg.memory_info.memory_info_by_name.return_value = { 'size' : 0x1000 }
        self.dw.dbg.program_counter_read.return_value = 0x700
        self.assertTrue(self.dw.warm_start())
        self.dw.dbg.memory_info.memory_info_by_name.assert_called_with('flash')
        self.dw.dbg.start_debugging.assert_called_once()
        self.dw.dbg.reset.assert_called_once()
        self.dw.dbg.program_counter_read.assert_called_once()

    def test_cold_start(self):
        self.dw.dbg.device_info.__getitem__.return_value = 0x1E9514
        self.dw.dbg.memory_info.memory_info_by_name.return_value = { 'size' : 0x1000 }
        self.dw.dbg.program_counter_read.return_value = 0x700
        self.dw.enable = MagicMock()
        self.dw.dbg.housekeeper = MagicMock()
        self.assertTrue(self.dw.cold_start(False, Mock(return_value=True), True))
        self.dw.enable.assert_called_once()
        self.dw.dbg.housekeeper.end_session.assert_called_once()
        self.dw.dbg.housekeeper.start_session.assert_called_once()

    def test_power_cycle_magic(self):
        self.dw.dbg.housekeeper = MagicMock()
        read_target_voltage = MagicMock()
        self.assertEqual(self.dw.power_cycle(Mock(return_value=True)), None)
        self.dw.dbg.housekeeper.end_session.assert_not_called()
        read_target_voltage.assert_not_called()

    @patch('pyavrocd.pyavrocd.pymcuprog.utils.read_voltage_parameter',
               Mock(side_effect=[5,5,5,0,0,0,0,0,5,5,5,5]))
    @patch('pyavrocd.pyavrocd.time.sleep', Mock())
    def test_power_cycle_normal(self):
        self.dw.dbg.housekeeper = Mock()
        self.assertEqual(self.dw.power_cycle(None), None)

    @patch('pyavrocd.pyavrocd.NvmAccessProviderCmsisDapSpi',MagicMock(spec_set=True))
    def test_disable(self):
        self.dw.dbg.housekeeper = Mock()
        self.dw.disable()
        self.dw.dbg.software_breakpoint_clear_all.assert_called_once()
        self.dw.spidevice.read.assert_called()
        self.dw.spidevice.write.assert_called_once()
        self.dw.spidevice.isp.enter_progmode.assert_called_once()
        self.dw.spidevice.isp.leave_progmode.assert_called_once()

    @patch('pyavrocd.pyavrocd.pymcuprog.utils.read_voltage_parameter',
               Mock(return_value=5.0))
    @patch('pyavrocd.pyavrocd.NvmAccessProviderCmsisDapSpi', MagicMock())
    def test_enable_wrong_mcu(self):
        dev_name[0] = "Wrong MCU"
        self.dw.dbg.housekeeper = MagicMock()
        self.dw.dbg.device_info.__getitem__.return_value = 0x1E9514
        with self.assertRaises(FatalError):
            self.dw.enable()

    @patch('pyavrocd.pyavrocd.pymcuprog.utils.read_voltage_parameter',
               Mock(return_value=5.0))
    @patch('pyavrocd.pyavrocd.NvmAccessProviderCmsisDapSpi', MagicMock())
    def test_enable_ok(self):
        self.dw.dbg.housekeeper = MagicMock()
        self.dw.spidevice = Mock()
        self.dw.spidevice.isp = Mock()
        self.dw.dbg.device_info.__getitem__.return_value = 0
        self.dw.enable()
        self.dw.spidevice.erase.assert_called_once()
        self.dw.spidevice.read.assert_called()
        self.dw.spidevice.write.assert_called()
        self.dw.spidevice.isp.leave_progmode.assert_called()
        self.dw.spidevice.isp.enter_progmode.assert_called()

    @patch('pyavrocd.pyavrocd.pymcuprog.utils.read_voltage_parameter',
               Mock(return_value=0.0))
    def test_enable_no_target_power(self):
        self.dw.dbg.housekeeper = MagicMock()
        self.dw.spidevice = Mock()
        self.dw.spidevice.isp = Mock()
        self.dw.dbg.device_info.__getitem__.return_value = 0
        with self.assertRaises(FatalError):
            self.dw.enable()
