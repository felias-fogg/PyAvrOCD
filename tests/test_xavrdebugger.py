"""
The test suit for the XAvrDebugger class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
import logging
from unittest.mock import MagicMock, patch,  Mock, call
from unittest import TestCase

from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.xavr8target import XTinyAvrTarget

logging.basicConfig(level=logging.CRITICAL)

class TestXAvrDebugger(TestCase):

    def setUp(self):
        mock_transport = MagicMock()
        self.xa = XAvrDebugger(mock_transport, "attiny85", "debugwire", ['bootrst', 'lockbits', 'dwen'], 4000, 500)
        self.xa.logger = MagicMock()
        self.xa.transport = mock_transport
        self.xa.memory_info = MagicMock()
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock()
        self.xa.device.avr.protocol = MagicMock(spec=Avr8Protocol)

    @patch('pyavrocd.xavrdebugger.housekeepingprotocol.Jtagice3HousekeepingProtocol', MagicMock())
    def test_start_debugging(self):
        self.xa.device.avr.activate_physical.return_value = bytearray([0x0B, 0x93, 0, 0])
        self.xa.device.avr.memory_read.return_value = bytearray([0x1E, 0, 0])
        self.xa.device.avr.protocol.program_counter_read.return_value = 0x0
        self.xa.memory_info.memory_info_by_name.return_value={'size': 0x1000}
        self.xa.start_debugging()
        self.xa.device.avr.memory_read.assert_called_once()
        self.xa.housekeeper.start_session.assert_called_once()
        self.xa.device.avr.setup_debug_session.assert_called_once()
        self.xa.device.avr.setup_config.assert_called_once()
        self.xa.device.avr.activate_physical.assert_called_once()
        self.xa.device.avr.switch_to_progmode.assert_called_once()
        self.xa.device.avr.switch_to_debmode.assert_called_once()
        self.xa.device.avr.protocol.reset.assert_called_once()
        self.xa.device.avr.protocol.program_counter_read.assert_called_once()

    def test_stop_debugging(self):
        self.xa.stop_debugging(graceful=False)
        self.xa.device.avr.switch_to_debmode.assert_called_once()
        self.xa.device.avr.protocol.stop.assert_called_once()
        self.xa.device.avr.protocol.software_breakpoint_clear_all.assert_called_once()
        self.xa.device.avr.breakpoint_clear.assert_called_once()
        self.xa.device.avr.switch_to_progmode.assert_not_called()
        self.xa.device.avr.protocol.detach.assert_called_once()
        self.xa.device.avr.deactivate_physical.assert_called_once()

    def test__post_process_after_start_jtag(self):
        self.xa.iface = 'jtag'
        self.xa.manage = ['bootrst', 'lockbits', 'ocden']
        self.xa.device_info['bootrst_base'] = 0x01
        self.xa.device_info['bootrst_mask'] = 0x08
        self.xa.device_info['ocden_base'] = 0x02
        self.xa.device_info['ocden_mask'] = 0x04
        # read lockbits and fuses: lockbits before and after, bootrst (not set), ocden before and after
        self.xa.device.avr.memory_read.side_effect = [bytearray([0x0F]), bytearray([0xFF]),
                                                          bytearray([0xFF]), bytearray([0x04]),
                                                          bytearray([0x00])]
        self.xa._post_process_after_start()
        self.xa.device.erase.assert_called_once()
        self.xa.device.avr.memory_read.assert_has_calls([call(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, 0, 1),
                                                         call(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, 0, 1),
                                                         call(Avr8Protocol.AVR8_MEMTYPE_FUSES, 1, 1),
                                                         call(Avr8Protocol.AVR8_MEMTYPE_FUSES, 2, 1),
                                                         call(Avr8Protocol.AVR8_MEMTYPE_FUSES, 2, 1)])
        self.xa.device.avr.memory_write.assert_has_calls([call(Avr8Protocol.AVR8_MEMTYPE_FUSES, 2,
                                                              bytearray([0]))])

    @patch('pyavrocd.xavrdebugger.read_target_voltage', MagicMock(return_value=5.0))
    @patch('pyavrocd.xavrdebugger.NvmAccessProviderCmsisDapSpi.read_device_id',
               MagicMock(return_value = bytearray([0x0B, 0x93, 0x1E])))
    @patch('pyavrocd.xavrdebugger.NvmAccessProviderCmsisDapSpi.erase', MagicMock())
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.enter_progmode', MagicMock())
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.leave_progmode', MagicMock())
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.read_lockbits',
               MagicMock(side_effect = [bytearray([0x0F]), bytearray([0x0FF])]))
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.read_fuse_byte',
               MagicMock(side_effect = [bytearray([0x00]), bytearray([0x08]),
                                        bytearray([0x14])]))
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.write_fuse_byte', MagicMock())
    #pylint: disable=no-member
    def test_prepare_debugging_debugWIRE(self):
        self.xa.manage = ['bootrst', 'lockbits', 'dwen']
        self.xa.device_info['bootrst_base'] = 0x01
        self.xa.device_info['bootrst_mask'] = 0x08
        self.xa.device_info['dwen_base'] = 0x02
        self.xa.device_info['dwen_mask'] = 0x04
        self.xa.housekeeper = Mock()
        self.xa.prepare_debugging(callback=lambda: True)
        self.xa.spidevice.isp.read_lockbits.assert_has_calls([call(), call()])
        self.xa.spidevice.isp.read_fuse_byte.assert_has_calls([call(1), call(1), call(2)])
        self.xa.spidevice.isp.write_fuse_byte.assert_has_calls([call(1,bytearray([0x08])),
                                                                    call(2,bytearray([0x10]))])
        self.xa.housekeeper.start_session.assert_called()
        self.xa.spidevice.isp.enter_progmode.assert_called()
        self.xa.spidevice.isp.leave_progmode.assert_called()

    def test_stack_pointer_write(self):
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        self.xa.stack_pointer_write(b'\x34\x12')
        self.xa.device.avr.stack_pointer_write.assert_called_with(b'\x34\x12')

    def test_stack_pointer_read(self):
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        self.xa.device.avr.stack_pointer_read.return_value = b'\x34\x12'
        self.assertEqual(self.xa.stack_pointer_read(), b'\x34\x12')

    def test_status_register_write(self):
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        self.xa.status_register_write(b'\x12')
        self.xa.device.avr.statreg_write.assert_called_with(b'\x12')

    def test_status_register_read(self):
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        self.xa.device.avr.statreg_read.return_value = b'\x34'
        self.assertEqual(self.xa.status_register_read(),b'\x34')
        self.xa.device.avr.statreg_read.assert_called_once()

    def test_register_file_write(self):
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        rfile = bytearray(list(range(32)))
        self.xa.register_file_write(rfile)
        self.xa.device.regfile_write(rfile)

    def test_register_file_read(self):
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        rfile = bytearray(list(range(32)))
        self.xa.device.avr.regfile_read.return_value=rfile
        self.assertEqual(self.xa.register_file_read(),rfile)
        self.xa.device.avr.regfile_read.assert_called_once()
