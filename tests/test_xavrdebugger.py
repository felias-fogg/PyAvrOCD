"""
The test suit for the EdbgBackend class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
from unittest.mock import MagicMock, patch,  Mock, call, ANY
from unittest import TestCase
from types import SimpleNamespace

from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.protocols.jtagice3protocol import Jtagice3ResponseError
from pyedbglib.protocols.edbgprotocol import EdbgProtocol
from pyedbglib.protocols.avrispprotocol import AvrIspProtocolError
from pymcuprog.pymcuprog_errors import PymcuprogError, PymcuprogNotSupportedError
from pyavrocd.xavrdebugger import EdbgBackend
from pyavrocd.xavr8target import XTinyAvrTarget
from pyavrocd.errors import FatalError
from pyavrocd.backend import SwbpSupport, BackendError, BackendNotSupportedError, InvalidAddressError, IspConnectionError

class TestXAvrDebugger(TestCase):

    def setUp(self):
        self.xa = None
        self.xaj = None
        self.xau = None
        self.xa23 = None

    def set_up(self):
        mock_transport = MagicMock()
        args = SimpleNamespace()
        args.manage = ['bootrst', 'lockbits', 'dwen', 'ocden']
        args.clkprg = 500
        args.clkdeb = 4000
        args.kbps = 100
        args.timers = 'r'
        args.load = 'n'
        args.attach = False
        args.skipsig = False
        # a debugWIRE target
        self.xa = EdbgBackend(mock_transport, "attiny85", "debugwire", args)
        self.xa.logger = MagicMock()
        self.xa.transport = mock_transport
        self.xa.memory_info = MagicMock()
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock()
        self.xa.device.avr.protocol = MagicMock(spec=Avr8Protocol)
        self.xa.logger = Mock()
        self.xa.housekeeper = Mock()
        self.xa._wait_for_break = Mock()
        self.xa._wait_for_break.return_value = False # after reset: we are stopped
        self.xa.flush_events = Mock()
        # special case: ATtiny2313
        self.xa23 = EdbgBackend(mock_transport, "attiny2313", "debugwire", args)
        self.xa23.logger = MagicMock()
        self.xa23.transport = mock_transport
        self.xa23.memory_info = MagicMock()
        self.xa23.device = MagicMock()
        self.xa23.device.avr = MagicMock()
        self.xa23.device.avr.protocol = MagicMock(spec=Avr8Protocol)
        self.xa23.logger = Mock()
        self.xa23.housekeeper = Mock()
        self.xa23._wait_for_break = Mock()
        self.xa23._wait_for_break.return_value = False # after reset: we are stopped
        self.xa23.flush_events = Mock()
        # a JTAG target
        self.xaj = EdbgBackend(mock_transport, "atmega644", "jtag", args)
        self.xaj.logger = MagicMock()
        self.xaj.transport = mock_transport
        self.xaj.memory_info = MagicMock()
        self.xaj.device = MagicMock()
        self.xaj.device.avr = MagicMock()
        self.xaj.device.avr.protocol = MagicMock(spec=Avr8Protocol)
        self.xaj.housekeeper = Mock()
        self.xaj._wait_for_break = Mock()
        self.xaj._wait_for_break.return_value = False
        self.xaj.flush_events = Mock()
        # a UPDI target
        args.manage = []
        self.xau = EdbgBackend(mock_transport, "atmega4809", "updi", args)
        self.xau.logger = MagicMock()
        self.xau.transport = mock_transport
        self.xau.memory_info = MagicMock()
        self.xau.device = MagicMock()
        self.xau.device.avr = MagicMock()
        self.xau.device.avr.protocol = MagicMock(spec=Avr8Protocol)
        self.xau.housekeeper = Mock()
        self.xau._wait_for_break = Mock()
        self.xau._wait_for_break.return_value = False
        self.xau.flush_events = Mock()


    def test_get_iface(self):
        self.set_up()
        self.assertEqual(self.xa.get_iface(), 'debugwire')
        self.assertEqual(self.xaj.get_iface(), 'jtag')
        self.assertEqual(self.xau.get_iface(), 'updi')

    def test_get_architecture(self):
        self.set_up()
        self.assertEqual(self.xa.get_architecture(), 'avr8')
        self.assertEqual(self.xaj.get_architecture(), 'avr8')
        self.assertEqual(self.xau.get_architecture(), 'avr8x')

    def test_get_hwbpnum(self):
        self.set_up()
        self.assertEqual(self.xa.get_hwbpnum(), 1)
        self.assertEqual(self.xaj.get_hwbpnum(), 4)
        self.assertEqual(self.xau.get_hwbpnum(), 2)


    @patch('pyavrocd.xavrdebugger.housekeepingprotocol.Jtagice3HousekeepingProtocol', MagicMock())
    def test_start_debugging_dw(self):
        self.set_up()
        self.xa.device.avr.protocol.activate_physical.return_value = bytearray([0x0B, 0x93, 0, 0])
        self.xa.device.avr.protocol.program_counter_read.return_value = 0x0
        self.xa.memory_info.memory_info_by_name.return_value={'address': 0x200, 'size': 0x1000}
        self.xa.device.read.return_value = [0]
        self.assertTrue(self.xa.start_debugging())
        self.xa.device.avr.memory_read.assert_not_called()
        self.xa.housekeeper.start_session.assert_called_once()
        self.xa.device.avr.setup_debug_session.assert_called_once()
        self.xa.device.avr.setup_config.assert_called_once()
        self.xa.device.avr.protocol.activate_physical.assert_called_once()
        self.xa.device.avr.switch_to_progmode.assert_not_called()
        self.xa.device.avr.switch_to_debmode.assert_not_called()
        self.assertEqual(self.xa.device.avr.protocol.reset.call_count,1)
        self.xa.device.avr.protocol.program_counter_read.assert_called_once()

    @patch('pyavrocd.xavrdebugger.housekeepingprotocol.Jtagice3HousekeepingProtocol', MagicMock())
    def test_start_debugging_dw_warmstart_fail(self):
        self.set_up()
        self.xa.device.avr.protocol.activate_physical.return_value = Exception()
        self.xa.device.avr.protocol.program_counter_read.return_value = 0x0
        self.xa.memory_info.memory_info_by_name.return_value={'size': 0x1000, 'address': 0x200}
        self.assertFalse(self.xa.start_debugging(warmstart=True))

    @patch('pyavrocd.xavrdebugger.housekeepingprotocol.Jtagice3HousekeepingProtocol', MagicMock())
    def test_start_debugging_dw_coldstart_fail(self):
        self.set_up()
        self.xa.device.avr.activate_physical.return_value = Exception()
        self.xa.device.avr.protocol.program_counter_read.return_value = 0x0
        self.xa.memory_info.memory_info_by_name.return_value={'size': 0x1000}
        self.assertRaises(FatalError,self.xa.start_debugging,warmstart=False)

    @patch('pyavrocd.xavrdebugger.housekeepingprotocol.Jtagice3HousekeepingProtocol', MagicMock())
    def test_start_debugging_jtag(self):
        self.set_up()
        self.xaj.device_info['bootrst_base'] = 0x01
        self.xaj.device_info['bootrst_mask'] = 0x08
        self.xaj.device_info['ocden_base'] = 0x02
        self.xaj.device_info['ocden_mask'] = 0x04
        self.xaj.device.avr.protocol.activate_physical.return_value = \
                                                   bytearray([0x3F, 0x90, 0x60, 0x09])
        self.xaj.device.avr.memory_read.side_effect = [ bytearray([0xFF]),  # lockbits
                                                        bytearray([0xFF]),  # bootrst
                                                        bytearray([0x04]),  # ocden
                                                        bytearray([0x00]),  # ocden after programming
                                                        bytearray([0x1E, 0x96, 0x09]) # signature
                                                       ]
        self.xaj.device.avr.protocol.program_counter_read.return_value = 0x0
        self.xaj.memory_info.memory_info_by_name.return_value={'size': 0x1000, 'address': 0x200}
        self.xaj.device.read.return_value = [0]
        self.xaj.device.avr.protocol.stop.side_effect = \
          Jtagice3ResponseError(code=Avr8Protocol.AVR8_FAILURE_ILLEGAL_OCD_STATUS, msg="bla")
        self.assertTrue(self.xaj.start_debugging())
        self.assertEqual(self.xaj.device.avr.memory_read.call_count, 5)
        self.xaj.housekeeper.start_session.assert_called_once()
        self.xaj.device.avr.setup_debug_session.assert_called_once()
        self.xaj.device.avr.setup_config.assert_called_once()
        self.xaj.device.avr.protocol.activate_physical.assert_called_once()
        self.xaj.device.avr.switch_to_progmode.assert_called_once()
        self.xaj.device.avr.switch_to_debmode.assert_called_once()
        self.assertEqual(self.xaj.device.avr.protocol.reset.call_count, 1)
        self.xaj.device.avr.protocol.program_counter_read.assert_called_once()

    @patch('pyavrocd.xavrdebugger.housekeepingprotocol.Jtagice3HousekeepingProtocol', MagicMock())
    def test_start_jtag_fail(self):
        self.set_up()
        self.xaj.device.avr.activate_physical.return_value = bytearray([0x3E, 0x93, 0, 0])
        self.assertRaises(FatalError, self.xaj.start_debugging)



    def test__manage_fuses_jtag(self):
        self.set_up()
        self.xaj._iface = 'jtag'
        self.xaj.manage = ['bootrst', 'lockbits', 'ocden']
        self.xaj.device_info['bootrst_base'] = 0x01
        self.xaj.device_info['bootrst_mask'] = 0x08
        self.xaj.device_info['ocden_base'] = 0x02
        self.xaj.device_info['ocden_mask'] = 0x04
        # read lockbits and fuses: lockbits before and after, bootrst (not set), ocden before and after
        self.xaj.device.avr.memory_read.side_effect = [bytearray([0x0F]), bytearray([0xFF]),
                                                       bytearray([0x00]), bytearray([0x08]),
                                                       bytearray([0x04]), bytearray([0x00]),
                                                       bytearray([0x1E, 0x96, 0x09])]
        self.xaj._manage_fuses()
        self.xaj.device.erase.assert_called_once()
        self.xaj.device.avr.memory_read.assert_has_calls(
            [call(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, 0, 1),
             call(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, 0, 1),
             call(Avr8Protocol.AVR8_MEMTYPE_FUSES, 1, 1),
             call(Avr8Protocol.AVR8_MEMTYPE_FUSES, 1, 1),
             call(Avr8Protocol.AVR8_MEMTYPE_FUSES, 2, 1),
             call(Avr8Protocol.AVR8_MEMTYPE_FUSES, 2, 1),
             call(Avr8Protocol.AVR8_MEMTYPE_SIGNATURE, 0, 3)])
        self.xaj.device.avr.memory_write.assert_has_calls([call(Avr8Protocol.AVR8_MEMTYPE_FUSES, 2,
                                                              bytearray([0]))])

    @patch('pyavrocd.session.logging.getLogger', MagicMock())
    def test__manage_fuses_lockbits_not_managed(self):
        self.set_up()
        self.xaj.device.avr.memory_read.return_value = bytes([0x0F])
        self.xaj._iface = 'jtag'
        self.xaj.manage = ['bootrst']
        self.xaj.device_info['bootrst_base'] = 0x01
        self.xaj.device_info['bootrst_mask'] = 0x08
        self.xaj.device_info['ocden_base'] = 0x02
        self.xaj.device_info['ocden_mask'] = 0x04
        self.assertRaises(FatalError, self.xaj._manage_fuses)
        self.xaj.logger.warning.assert_has_calls([
            call("Alternatively, let PyAvrOCD manage it: '-m lockbits'")])

    @patch('pyavrocd.session.logging.getLogger', MagicMock())
    def test__manage_fuses_ocden_not_managed(self):
        self.set_up()
        self.xaj.device.avr.memory_read.side_effect = [ bytearray([0xFF]),
                                                        bytearray([0xFF]),
                                                        bytearray([0xFF]) ]
        self.xaj._iface = 'jtag'
        self.xaj.manage = ['bootrst']
        self.xaj.device_info['bootrst_base'] = 0x01
        self.xaj.device_info['bootrst_mask'] = 0x08
        self.xaj.device_info['ocden_base'] = 0x02
        self.xaj.device_info['ocden_mask'] = 0x04
        self.assertRaises(FatalError, self.xaj._manage_fuses)
        self.xaj.logger.warning.assert_has_calls([
            call("Or let payavrocd manage this fuse: '-m ocden'.")])

    @patch('pyavrocd.session.logging.getLogger', MagicMock())
    def test__manage_fuses_sig_ok(self):
        self.set_up()
        self.xaj.device.avr.memory_read.side_effect = [ bytearray([0xFF]),
                                                        bytearray([0x00]),
                                                        bytearray([0x00]),
                                                        bytearray([0x1E, 0x96, 0x09])]
        self.xaj._iface = 'jtag'
        self.xaj.manage = []
        self.xaj.device_info['bootrst_base'] = 0x01
        self.xaj.device_info['bootrst_mask'] = 0x08
        self.xaj.device_info['ocden_base'] = 0x02
        self.xaj.device_info['ocden_mask'] = 0x04
        self.xaj._manage_fuses()
        self.xaj.logger.info.assert_has_calls([
            call("Switched to debugging mode")])

    def test__manage_fuses_sig_fail(self):
        self.set_up()
        self.xaj.device.avr.memory_read.side_effect = [ bytearray([0xFF]),
                                                        bytearray([0x00]),
                                                        bytearray([0x00]),
                                                        bytearray([0x1E, 0x96, 0x0A])]
        self.xaj._iface = 'jtag'
        self.xaj.manage = []
        self.xaj.device_info['bootrst_base'] = 0x01
        self.xaj.device_info['bootrst_mask'] = 0x08
        self.xaj.device_info['ocden_base'] = 0x02
        self.xaj.device_info['ocden_mask'] = 0x04
        self.assertRaises(FatalError, self.xaj._manage_fuses)


    @patch('pyavrocd.session.logging.getLogger', MagicMock())
    def test__manage_fuses_nothing_to_do(self):
        self.set_up()
        self.xaj.device.avr.memory_read.side_effect = [
            bytes([0xFF]), bytes([0x08]), bytes([0x00]), bytearray([0x1E, 0x96, 0x09]) ]
        self.xaj._iface = 'jtag'
        self.xaj.manage = ['bootrst', 'lockbits', 'ocden']
        self.xaj.device_info['bootrst_base'] = 0x01
        self.xaj.device_info['bootrst_mask'] = 0x08
        self.xaj.device_info['ocden_base'] = 0x02
        self.xaj.device_info['ocden_mask'] = 0x04
        self.xaj._manage_fuses()
        self.xaj.logger.info.assert_has_calls([
            call("OCDEN is already programmed")])

    def test__verify_target_fail(self):
        self.set_up()
        self.assertRaises(FatalError, self.xa._verify_target, 0x920B)

    def test__verify_target_ok(self):
        self.set_up()
        self.xa.device_info['device_id'] = 0x1E9205 # ATmega48(A)
        self.xa._verify_target(0x920A)              # ATmega48PA
        self.xa.device_info['device_id'] = 0x1E930B # ATtiny85 restored

    def test__check_stuck_at_one_pc_fail(self):
        self.set_up()
        self.xa.device.avr.protocol.program_counter_read.return_value = 0x4000
        self.xa.memory_info.memory_info_by_name.return_value = {'size': 0x1000}
        self.xa._check_stuck_at_one_pc()
        self.assertEqual(self.xa.bad_pc_bit_mask,0x8000)

    def test__check_stuck_at_one_pc_ok(self):
        self.set_up()
        self.xa.device.avr.protocol.program_counter_read.return_value = 0x0000
        self.xa.device.read.return_value = [0]
        self.xa.memory_info.memory_info_by_name.return_value = {'size': 0x1000, 'address': 0x200}
        self.xa._check_stuck_at_one_pc()
        self.assertEqual(self.xa.bad_pc_bit_mask,0)

    def test__activate_interface_ok(self):
        self.set_up()
        self.xa.device.avr.protocol.activate_physical.return_value = bytearray([0x01, 0x02, 0x03, 0x04])
        self.assertEqual(self.xa._activate_interface(), 0x04030201)

    def test__check_attiny2313_ok(self):
        self.set_up()
        self.xa23.device.read.retun_value = bytearray([0xE0])
        self.assertEqual(self.xa23._check_attiny2313(), None)
        self.assertEqual(self.xa23.device.read.call_count, 2)
        self.assertEqual(self.xa23.device.write.call_count, 2)

    def test__check_attiny2313_fail(self):
        self.set_up()
        self.xa23.device.read.return_value = bytearray([0xF8])
        self.assertRaises(FatalError,self.xa23._check_attiny2313)
        self.assertEqual(self.xa23.device.read.call_count, 2)
        self.assertEqual(self.xa23.device.write.call_count, 2)


    def test__check_attiny2313_no2313(self):
        self.set_up()
        self.assertEqual(self.xa._check_attiny2313(), None)
        self.xa.device.read.assert_not_called()


    def test__activate_interface_fail_invalid_state(self):
        self.set_up()
        self.xa.device.avr.protocol.activate_physical.side_effect = Jtagice3ResponseError("Error",
                                    Avr8Protocol.AVR8_FAILURE_INVALID_PHYSICAL_STATE)
        self.assertRaises(Jtagice3ResponseError, self.xa._activate_interface)

    def test__activate_interface_fail_phy_dw_error(self):
        self.set_up()
        self.xa.device.avr.protocol.activate_physical.side_effect = Jtagice3ResponseError("Error",
                                    Avr8Protocol.AVR8_FAILURE_DW_PHY_ERROR)
        self.assertRaises(FatalError, self.xa._activate_interface)

    def test__activate_interface_fail_clock(self):
        self.set_up()
        self.xa.device.avr.protocol.activate_physical.side_effect = Jtagice3ResponseError("Error",
                                    Avr8Protocol.AVR8_FAILURE_CLOCK_ERROR)
        self.assertRaises(Jtagice3ResponseError, self.xa._activate_interface)


    def test__handle_bootrst_fail(self):
        self.set_up()
        self.xaj.manage = []
        self.xaj.device_info['bootrst_base'] = 0x01
        self.xaj.device_info['bootrst_mask'] = 0x08
        read = Mock(side_effect=[bytearray([0x00])])
        write = Mock()
        self.xaj._handle_bootrst(read, write)
        self.xaj.logger.warning.assert_has_calls([
            call("BOOTRST is not managed by PyAvrOCD and will therefore not be cleared.")])
        self.xaj.manage = ['bootrst', 'lockbits', 'ocden'] # restore!

    def test__handle_bootrst_ok(self):
        self.set_up()
        self.xaj.device_info['bootrst_base'] = 0x01
        self.xaj.device_info['bootrst_mask'] = 0x08
        read = Mock(side_effect=[bytearray([0x00]), bytearray([0x08])])
        write = Mock()
        self.xaj._handle_bootrst(read, write)
        self.xaj.logger.info.assert_has_calls([
            call("BOOTRST fuse has been unprogrammed.")])
        self.xaj.manage = ['bootrst', 'lockbits', 'ocden'] # restore!

    def test__handle_lockbits_fail(self):
        self.set_up()
        self.xaj.manage = []
        read = Mock(side_effect=[bytes([0x00])])
        self.assertRaises(FatalError,self.xaj._handle_lockbits, read, Mock())
        self.xaj.manage = ['bootrst', 'lockbits', 'ocden'] # restore!

    def test__handle_lockbits_ok(self):
        self.set_up()
        read = Mock(side_effect=[bytes([0x00]), bytes([0xFF])])
        erase = Mock()
        self.xaj._handle_lockbits(read, erase)
        erase.assert_called_once()
        self.xaj.logger.info.assert_has_calls([
            call("MCU has been erased and lockbits have been cleared.")])

    def test_handle_lockbits_nochange(self):
        self.set_up()
        read = Mock(side_effect=[bytes([0xFF])])
        erase = Mock()
        self.xaj._handle_lockbits(read, erase)
        erase.assert_not_called()
        self.xaj.logger.info.assert_has_calls([
            call("MCU is not locked.")])


    @patch('pyavrocd.xavrdebugger.read_target_voltage', MagicMock(return_value=5.0))
    @patch('pyavrocd.xavrdebugger.NvmAccessProviderCmsisDapSpi.read_device_id',
               MagicMock(return_value = bytearray([0x0B, 0x93, 0x1E])))
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.erase', MagicMock())
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.enter_progmode', MagicMock())
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.leave_progmode', MagicMock())
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.read_lockbits',
               MagicMock(side_effect = [bytearray([0x0F]), bytearray([0x0FF])]))
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.read_fuse_byte',
               MagicMock(side_effect = [bytearray([0x00]), bytearray([0x08]),
                                        bytearray([0x04]) ]))
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.write_fuse_byte', MagicMock())
    #pylint: disable=no-member
    def test_prepare_debugging_debugWIRE(self):
        self.set_up()
        self.xa.manage = ['bootrst', 'lockbits', 'dwen']
        self.xa.device_info['bootrst_base'] = 0x01
        self.xa.device_info['bootrst_mask'] = 0x08
        self.xa.device_info['dwen_base'] = 0x02
        self.xa.device_info['dwen_mask'] = 0x04
        self.xa.housekeeper = Mock()
        self.xa.prepare_debugging(callback=lambda: True, recognition=lambda: None)
        self.xa.spidevice.isp.read_lockbits.assert_has_calls([call(), call()])
        self.xa.spidevice.isp.read_fuse_byte.assert_has_calls([call(1), call(1), call(2)])
        self.xa.spidevice.isp.write_fuse_byte.assert_has_calls([call(1,bytearray([0x08])),
                                                                    call(2,bytearray([0x00]))])
        self.xa.housekeeper.start_session.assert_called()
        self.xa.spidevice.isp.enter_progmode.assert_called()
        self.xa.spidevice.isp.leave_progmode.assert_called()

    @patch('pyavrocd.session.logging.getLogger', MagicMock())
    def test_prepare_debugging_jtag(self):
        self.set_up()
        self.xaj.prepare_debugging()
        self.xaj.logger.info.assert_not_called()

    @patch('pyavrocd.xavrdebugger.read_target_voltage', MagicMock(return_value=0.8))
    def test_prepare_debugging_no_power(self):
        self.set_up()
        self.assertRaises(FatalError, self.xa.prepare_debugging)

    @patch('pyavrocd.xavrdebugger.read_target_voltage', MagicMock(return_value=5.0))
    @patch('pyavrocd.xavrdebugger.NvmAccessProviderCmsisDapSpi.read_device_id',
               Mock(return_value= bytes([0,0,0])))
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.enter_progmode', MagicMock())
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.leave_progmode', MagicMock())
    def test_prepare_debugging_wrong_mcu(self):
        self.set_up()
        self.assertRaises(FatalError, self.xa.prepare_debugging)

    @patch('pyavrocd.xavrdebugger.read_target_voltage', MagicMock(return_value=5.0))
    @patch('pyavrocd.xavrdebugger.NvmAccessProviderCmsisDapSpi.read_device_id',
               MagicMock(return_value = bytearray([0x0B, 0x93, 0x1E])))
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.enter_progmode', MagicMock())
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.leave_progmode', MagicMock())
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.read_lockbits',
               MagicMock(side_effect = [bytearray([0xFF]), bytearray([0x0FF])]))
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.write_fuse_byte', Mock())
    @patch('pyavrocd.xavrdebugger.AvrIspProtocol.read_fuse_byte',
               MagicMock(side_effect = [bytearray([0x00]), bytearray([0x08]),
                                        bytearray([0x14])]))
    @patch('pyavrocd.session.logging.getLogger', MagicMock())
    def test_prepare_debugging_dwen_not_managed(self):
        self.set_up()
        self.xa.manage = ['bootrst', 'lockbits' ]
        self.xa.device_info['bootrst_base'] = 0x01
        self.xa.device_info['bootrst_mask'] = 0x08
        self.xa.device_info['dwen_base'] = 0x02
        self.xa.device_info['dwen_mask'] = 0x04
        self.xa.housekeeper = Mock()
        self.assertRaises(FatalError, self.xa.prepare_debugging)
        self.xa.logger.warning.assert_has_calls([
            call("The DWEN fuse is not managed by PyAvrOCD.")])

    @patch('pyavrocd.xavrdebugger.time.sleep',Mock())
    def test__check_atmega48_and_88_atmega48_fail(self):
        self.set_up()
        self.xa.spidevice = Mock()
        self.xa.spidevice.isp.read_fuse_byte.return_value = bytes([0xD7]) # EESAVE programmed
        self.xa.spidevice.isp.read_lockbits.side_effect=[bytes([0x00])]
        self.assertRaises(FatalError, self.xa._check_atmega48_and_88, 0x1E9205)

    @patch('pyavrocd.xavrdebugger.time.sleep',Mock())
    def test__check_atmega48_and_88_atmega48_ok(self):
        self.set_up()
        self.xa.spidevice = Mock()
        self.xa.spidevice.isp.read_fuse_byte.return_value = bytes([0xD7]) # EESAVE programmed
        self.xa.spidevice.isp.read_lockbits.side_effect=[bytes([0xFF])]
        self.xa._check_atmega48_and_88(0x1E9205)

    @patch('pyavrocd.xavrdebugger.time.sleep',Mock())
    def test__check_atmega48_and_88_atmega88_fail(self):
        self.set_up()
        self.xa.spidevice = Mock()
        self.xa.spidevice.isp.read_fuse_byte.return_value = bytes([0xD7]) # EESAVE programmed
        self.xa.spidevice.isp.read_lockbits.side_effect=[bytes([0x00])]
        self.assertRaises(FatalError, self.xa._check_atmega48_and_88, 0x1E930A)

    @patch('pyavrocd.xavrdebugger.time.sleep',Mock())
    def test__check_atmega48_and_88_atmega88_ok(self):
        self.set_up()
        self.xa.spidevice = Mock()
        self.xa.spidevice.isp.read_fuse_byte.return_value = bytes([0xD7]) # EESAVE programmed
        self.xa.spidevice.isp.read_lockbits.side_effect=[bytes([0xFF])]
        self.xa._check_atmega48_and_88(0x1E930A)

    @patch('pyavrocd.xavrdebugger.time.sleep',Mock())
    @patch('pyavrocd.xavrdebugger.read_target_voltage', MagicMock(side_effect=[
        5.0, 5.0, 0.0, 0.0, 0.0, 5.0, 5.0, 5.0]))
    @patch('pyavrocd.session.logging.getLogger', MagicMock())
    def test__power_cycle(self):
        self.set_up()
        self.xa._power_cycle()
        self.xa.logger.info.assert_has_calls([call("Signed on to tool again")])

    def test_stop_debugging_dw_no_leave(self):
        self.set_up()
        self.xa.stop_debugging(leave=False,graceful=False)
        self.xa.device.avr.switch_to_debmode.assert_called_once()
        self.xa.device.avr.protocol.stop.assert_called_once()
        self.xa.device.avr.protocol.software_breakpoint_clear_all.assert_called_once()
        self.xa.device.avr.breakpoint_clear.assert_called_once()
        self.xa.device.avr.switch_to_progmode.assert_not_called()
        self.xa.device.avr.protocol.debugwire_disable.assert_not_called()
        self.xa.device.avr.protocol.detach.assert_called_once()
        self.xa.device.avr.deactivate_physical.assert_called_once()
        self.xa.housekeeper.end_session.assert_called_once()

    def test_stop_debugging_dw_error_stopping_leave(self):
        self.set_up()
        self.xa.device.avr.protocol.stop.side_effect = FatalError("bla")
        self.xa.stop_debugging(leave=True,graceful=False)
        self.xa.logger.error.assert_has_calls([
            call("Error during stopping core and removing BPs: %s", "bla")])
        self.xa.device.avr.protocol.stop.assert_called_once()
        self.xa.device.avr.protocol.software_breakpoint_clear_all.assert_not_called()
        self.xa.device.avr.breakpoint_clear.assert_not_called()
        self.xa.device.avr.protocol.debugwire_disable.assert_called_once()
        self.xa.device.avr.switch_to_progmode.assert_not_called()
        self.xa.device.avr.protocol.detach.assert_called_once()
        self.xa.device.avr.deactivate_physical.assert_called_once()

    def test_stop_debugging_dw_error_dw_disable_leave(self):
        self.set_up()
        self.xa.device.avr.protocol.debugwire_disable.side_effect = FatalError("bla")
        self.xa.stop_debugging(leave=True,graceful=False)
        self.xa.logger.error.assert_has_calls([
            call("Error during disabling debugWIRE mode: %s", "bla")])
        self.xa.device.avr.protocol.stop.assert_called_once()
        self.xa.device.avr.protocol.software_breakpoint_clear_all.assert_called_once()
        self.xa.device.avr.breakpoint_clear.assert_called_once()
        self.xa.device.avr.protocol.debugwire_disable.assert_called_once()
        self.xa.device.avr.switch_to_progmode.assert_not_called()
        self.xa.device.avr.protocol.detach.assert_called_once()
        self.xa.device.avr.deactivate_physical.assert_called_once()

    def test_stop_debugging_jtag(self):
        self.set_up()
        self.xaj.stop_debugging(leave=True, graceful=False)
        self.xaj.device.avr.switch_to_debmode.assert_called_once()
        self.xaj.device.avr.protocol.stop.assert_called_once()
        self.xaj.device.avr.protocol.software_breakpoint_clear_all.assert_called_once()
        self.xaj.device.avr.breakpoint_clear.assert_called_once()
        self.xaj.device.avr.switch_to_progmode.assert_called_once() # diff to dw!
        self.xaj.device.avr.protocol.detach.assert_called_once()
        self.xaj.device.avr.deactivate_physical.assert_called_once()
        self.xaj.housekeeper.end_session.assert_called_once()

    def test_stop_debugging_jtag_error_ocden(self):
        self.set_up()
        self.xaj.device.avr.switch_to_progmode.side_effect = FatalError("bla")
        self.xaj.stop_debugging(leave=True, graceful=False)
        self.xaj.logger.error.assert_has_calls([call("Error during unprogramming OCDEN: %s", "bla")])
        self.xaj.device.avr.switch_to_debmode.assert_called_once()
        self.xaj.device.avr.protocol.stop.assert_called_once()
        self.xaj.device.avr.protocol.software_breakpoint_clear_all.assert_called_once()
        self.xaj.device.avr.breakpoint_clear.assert_called_once()
        self.xaj.device.avr.switch_to_progmode.assert_called_once() # diff to dwen
        self.xaj.device.avr.protocol.detach.assert_called_once()
        self.xaj.device.avr.deactivate_physical.assert_called_once()
        self.xaj.housekeeper.end_session.assert_called_once()

    def test_stop_debugging_jtag_no_leave(self):
        self.set_up()
        self.xaj.stop_debugging(leave=False, graceful=False)
        self.xaj.device.avr.switch_to_debmode.assert_called_once()
        self.xaj.device.avr.protocol.stop.assert_called_once()
        self.xaj.device.avr.protocol.software_breakpoint_clear_all.assert_called_once()
        self.xaj.device.avr.breakpoint_clear.assert_called_once()
        self.xaj.device.avr.switch_to_progmode.assert_not_called()
        self.xaj.device.avr.protocol.detach.assert_called_once()
        self.xaj.device.avr.deactivate_physical.assert_called_once()
        self.xaj.housekeeper.end_session.assert_called_once()

    def test_stop_debugging_jtag_leave(self):
        self.set_up()
        self.xaj.stop_debugging(leave=False, graceful=False)
        self.xaj.logger.info.assert_has_calls([
            call("OCDEN is not cleared because 'atexit' is set to 'stay'")])
        self.xaj.device.avr.switch_to_debmode.assert_called_once()
        self.xaj.device.avr.protocol.stop.assert_called_once()
        self.xaj.device.avr.protocol.software_breakpoint_clear_all.assert_called_once()
        self.xaj.device.avr.breakpoint_clear.assert_called_once()
        self.xaj.device.avr.switch_to_progmode.assert_not_called()
        self.xaj.device.avr.protocol.detach.assert_called_once()
        self.xaj.device.avr.deactivate_physical.assert_called_once()
        self.xaj.housekeeper.end_session.assert_called_once()


    def test_stop_debugging_jtag_error_deactivate_interface(self):
        self.set_up()
        self.xaj.device.avr.deactivate_physical.side_effect = FatalError("blabla")
        self.xaj.stop_debugging(leave=True, graceful=False)
        self.xaj.device.avr.switch_to_debmode.assert_called_once()
        self.xaj.device.avr.protocol.stop.assert_called_once()
        self.xaj.device.avr.protocol.software_breakpoint_clear_all.assert_called_once()
        self.xaj.device.avr.breakpoint_clear.assert_called_once()
        self.xaj.device.avr.switch_to_progmode.assert_called_once() # diff to dw!
        self.xaj.device.avr.protocol.detach.assert_called_once()
        self.xaj.device.avr.deactivate_physical.assert_called_once()
        self.xaj.housekeeper.end_session.assert_called_once()
        self.xaj.logger.error.assert_has_calls([
            call("Error during deactivating interface: %s", "blabla")])

    def test_stop_debugging_jtag_error_housekeeper(self):
        self.set_up()
        self.xaj.housekeeper.end_session.side_effect = FatalError("blablabla")
        self.xaj.stop_debugging(leave=True, graceful=False)
        self.xaj.device.avr.switch_to_debmode.assert_called_once()
        self.xaj.device.avr.protocol.stop.assert_called_once()
        self.xaj.device.avr.protocol.software_breakpoint_clear_all.assert_called_once()
        self.xaj.device.avr.breakpoint_clear.assert_called_once()
        self.xaj.device.avr.switch_to_progmode.assert_called_once() # diff to dw!
        self.xaj.device.avr.protocol.detach.assert_called_once()
        self.xaj.device.avr.deactivate_physical.assert_called_once()
        self.xaj.housekeeper.end_session.assert_called_once()
        self.xaj.logger.error.assert_has_calls([
            call("Error while signing off from tool: %s", "blablabla")])

    def test_dw_disable_nodwen(self):
        self.set_up()
        self.xa.manage = []
        self.xa._dwen_unprogramming(True)
        self.xa.housekeeper.start_session.assert_not_called()
        self.xa.housekeeper.end_session.assert_not_called()
        self.xa.logger.warning.assert_called_with(ANY)

    def test_ocden_unprogramming_not_managed(self):
        self.set_up()
        self.xaj.manage = []
        self.xaj._ocden_unprogramming(True)
        self.xaj.logger.warning.assert_has_calls([
            call("OCDEN cannot be disabled since this fuse is not managed by PyAvrOCD")])

    @patch('pyavrocd.xavrdebugger.housekeepingprotocol.Jtagice3HousekeepingProtocol', MagicMock())
    @patch('pyavrocd.xavrdebugger.NvmAccessProviderCmsisDapSpi', MagicMock())
    def test_dwen_unprogramming(self):
        self.set_up()
        self.xa.manage = ['dwen']
        self.xa._dwen_unprogramming(True)
        self.xa.logger.info.assert_called_with("Signed off from tool")
        self.xa.housekeeper.start_session.assert_called_once()
        self.xa.housekeeper.end_session.assert_called_once()
        self.xa.spidevice.isp.enter_progmode.assert_called_once()
        self.xa.spidevice.isp.write_fuse_byte.assert_called_once()
        self.xa.spidevice.isp.leave_progmode.assert_called_once()


    def test_cold_dw_disable_nodwen_start(self):
        self.set_up()
        self.xa.manage = []
        self.xa.start_debugging = Mock(return_value=True)
        self.xa.cold_dw_disable()
        self.xa.device.avr.protocol.debugwire_disable.assert_called_once()

    def test_cold_dw_disable_nodwen_nostart(self):
        self.set_up()
        self.xa.manage = []
        self.xa.start_debugging = Mock(return_value=False)
        self.xa.cold_dw_disable()
        self.xa.device.avr.protocol.debugwire_disable.assert_not_called()

    def test_cold_dw_disable_nojtag(self):
        self.set_up()
        self.assertRaises(FatalError, self.xaj.cold_dw_disable)

    def _avr_debugger_mocks(self, pc_word):
        """AvrDebugger's methods that the step-off logic uses, all recorded in one Mock"""
        m = Mock()
        m.program_counter_read.return_value = pc_word
        patches = [patch('pyavrocd.xavrdebugger.AvrDebugger.' + name, getattr(m, name))
                   for name in ('step', 'program_counter_read', 'program_counter_write', 'run',
                                'software_breakpoint_set', 'software_breakpoint_clear')]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        return m

    def test_step_updi_pc_written_onto_swbp(self):
        # measured with nEDBG, mEDBG and SNAP: the OCD would execute the BREAK instead
        self.set_up()
        m = self._avr_debugger_mocks(0x66)
        self.xau.software_breakpoint_set(0xCC)
        self.xau.program_counter_write(0x66)
        m.reset_mock()
        self.xau.step()
        self.assertEqual([c[0] for c in m.mock_calls if c[0] != 'program_counter_read'],
                         ['software_breakpoint_clear', 'step', 'software_breakpoint_set'])
        # the address is the last argument (AvrDebugger.x(self, ...) passes self as well)
        self.assertEqual(m.software_breakpoint_clear.call_args.args[-1], 0xCC)
        self.assertEqual(m.software_breakpoint_set.call_args.args[-1], 0xCC)
        self.assertIn(0xCC, self.xau._swbps)       # still a breakpoint for the next run
        self.assertFalse(self.xau._pc_written)
        m.reset_mock()
        self.xau.step()                            # a second step is an ordinary one again
        self.assertEqual(m.step.call_count, 1)
        m.software_breakpoint_clear.assert_not_called()

    def test_step_updi_at_swbp_after_hit(self):
        # after a real hit the probe steps over its BREAK itself
        self.set_up()
        m = self._avr_debugger_mocks(0x66)
        self.xau.software_breakpoint_set(0xCC)
        m.reset_mock()
        self.xau.step()
        m.software_breakpoint_clear.assert_not_called()
        self.assertEqual(m.step.call_count, 1)

    def test_step_updi_pc_written_elsewhere(self):
        self.set_up()
        m = self._avr_debugger_mocks(0x70)
        self.xau.software_breakpoint_set(0xCC)
        self.xau.program_counter_write(0x70)
        m.reset_mock()
        self.xau.step()
        m.software_breakpoint_clear.assert_not_called()
        self.assertEqual(m.step.call_count, 1)

    def test_step_debugwire_pc_written_onto_swbp(self):
        # debugWIRE and JTAG step correctly after a PC write onto a BREAK
        self.set_up()
        m = self._avr_debugger_mocks(0x66)
        self.xa.software_breakpoint_set(0xCC)
        self.xa.program_counter_write(0x66)
        m.reset_mock()
        self.xa.step()
        m.software_breakpoint_clear.assert_not_called()
        self.assertEqual(m.step.call_count, 1)

    def test_run_forgets_pc_write(self):
        self.set_up()
        self._avr_debugger_mocks(0x66)
        self.xau.software_breakpoint_set(0xCC)
        self.xau.program_counter_write(0x66)
        self.xau.run()
        self.assertFalse(self.xau._pc_written)
        self.xau.software_breakpoint_clear(0xCC)
        self.assertNotIn(0xCC, self.xau._swbps)
        self.xau.software_breakpoint_set(0xCE)
        self.xau.software_breakpoint_clear_all()
        self.assertEqual(self.xau._swbps, set())

    def test_software_breakpoint_set_ok(self):
        self.set_up()
        self.assertTrue(self.xa.software_breakpoint_set(10))
        self.xa.device.avr.protocol.software_breakpoint_set.assert_called_once()

    def test_software_breakpoint_set_fail(self):
        self.set_up()
        self.xa.device.avr.protocol.software_breakpoint_set.side_effect = FatalError()
        self.assertFalse(self.xa.software_breakpoint_set(10))

    def test_hardware_breakpoint_set(self):
        self.set_up()
        self.xa.bad_pc_bit_mask = 0x8000
        self.xa.hardware_breakpoint_set(1, 0x100)
        self.xa.device.avr.hardware_breakpoint_set.assert_called_with(1, 0x8100)

    def test_hardware_breakpoint_clear(self):
        self.set_up()
        self.xa.hardware_breakpoint_clear(1)
        self.xa.device.avr.hardware_breakpoint_clear.assert_called_with(1)


    def test_stack_pointer_write(self):
        self.set_up()
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        self.xa.stack_pointer_write(b'\x34\x12')
        self.xa.device.avr.stack_pointer_write.assert_called_with(b'\x34\x12')

    def test_stack_pointer_read(self):
        self.set_up()
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        self.xa.device.avr.stack_pointer_read.return_value = b'\x34\x12'
        self.assertEqual(self.xa.stack_pointer_read(), b'\x34\x12')

    def test_status_register_write(self):
        self.set_up()
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        self.xa.status_register_write(b'\x12')
        self.xa.device.avr.statreg_write.assert_called_with(b'\x12')

    def test_status_register_read(self):
        self.set_up()
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        self.xa.device.avr.statreg_read.return_value = b'\x34'
        self.assertEqual(self.xa.status_register_read(),b'\x34')
        self.xa.device.avr.statreg_read.assert_called_once()

    def test_register_file_write(self):
        self.set_up()
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        rfile = bytearray(list(range(32)))
        self.xa.register_file_write(rfile)
        self.xa.device.regfile_write(rfile)

    def test_register_file_read(self):
        self.set_up()
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        rfile = bytearray(list(range(32)))
        self.xa.device.avr.regfile_read.return_value=rfile
        self.assertEqual(self.xa.register_file_read(),rfile)
        self.xa.device.avr.regfile_read.assert_called_once()

    def test_reset(self):
        self.set_up()
        self.xa.reset()
        self.xa.device.avr.protocol.reset.assert_called_once()

    def test_readmem_sram_masked_register_one_byte(self):
        self.set_up()
        self.xa._iooffset = 0
        self.xa.masked_registers = [0x35, 0x21, 0x26]
        self.assertEqual(self.xa.sram_masked_read(0x21, 1), bytearray([0x00]))

    def test_readmem_sram_masked_register_bytearray(self):
        self.set_up()
        self.xa._iooffset = 0
        self.xa.masked_registers = [0x35, 0x21, 0x26]
        sram = list(reversed(range(0x35)))
        def access_sram(ix, length):
            return bytearray(sram[ix:ix+length])
        self.xa.sram_read = MagicMock(side_effect=access_sram)
        self.assertEqual(self.xa.sram_masked_read(0x25, 3), bytearray([0x0F, 0x00, 0x0D]))
        self.assertEqual(self.xa.sram_masked_read(0x24, 3), bytearray([0x10, 0x0F, 0x00]))

    def test_readmem_sram_iooffset_nonnull_below(self):
        self.set_up()
        self.xa._iooffset = 0x20
        self.xa.sram_masked_read(0x10,3)
        self.xa.device.read.assert_not_called()

    def test_readmem_sram_iooffset_nonnull_above(self):
        self.set_up()
        self.xa._iooffset = 0x20
        self.xa.sram_masked_read(0x30,3)
        self.xa.device.read.assert_called_once()

    def test_readmem_sram_iooffset_nonnull_crossing(self):
        self.set_up()
        self.xa._iooffset = 0x20
        self.xa.sram_masked_read(0x1F,3)
        self.xa.device.read.assert_called_once()

    def test_readmem_sram_iooffset_null_crossing(self):
        self.set_up()
        self.xa._iooffset = 0
        self.xa.sram_masked_read(0x1F,3)
        self.xa.device.read.assert_called_once()

    def test_writemem_sram_iooffset_nonnull_below(self):
        self.set_up()
        self.xa._iooffset = 0x20
        data = bytearray([1,2,3])
        self.xa.sram_masked_write(0x10, data)
        self.xa.device.write.assert_not_called()

    def test_writemem_sram_iooffset_nonnull_above(self):
        self.set_up()
        self.xa._iooffset = 0x20
        data = bytearray([1,2,3])
        self.xa.sram_masked_write(0x30, data)
        self.xa.device.write.assert_called_once()

    def test_writemem_sram_iooffset_nonnull_crossing(self):
        self.set_up()
        self.xa._iooffset = 0x20
        data = bytearray([1,2,3])
        self.xa.sram_masked_write(0x1F, data)
        self.xa.device.write.assert_called_once()

    def test_writemem_sram_iooffset_null_crossing(self):
        self.set_up()
        self.xa._iooffset = 0
        data = bytearray([1,2,3])
        self.xa.sram_masked_write(0x1F, data)
        self.xa.device.write.assert_called_once()

    def test_writemem_sram_ronly_register_one_byte(self):
        self.set_up()
        self.xa._iooffset = 0
        self.xa.ronly_registers = [15, 1, 6]
        self.xa.sram_masked_write(1,  bytearray([0x55]))
        self.xa.device.write.assert_not_called()

    def test_writemem_sram_ronly_register_bytearray(self):
        self.set_up()
        self.xa._iooffset = 0
        self.xa.ronly_registers = [15, 1, 6, 0]
        self.xa.sram_masked_write(1, bytearray([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]))
        self.assertEqual(self.xa.device.write.call_count, 2)

    # --- EESAVE handling during the dirty-PC test (attiny85 device info: EESAVE = hfuse bit 3) ---

    @patch('pyavrocd.xavrdebugger.time.sleep',Mock())
    def test__check_atmega48_and_88_eesave_already_programmed(self):
        self.set_up()
        self.xa.manage.append('eesave')
        self.xa.spidevice = Mock()
        self.xa.spidevice.isp.read_fuse_byte.return_value = bytes([0xD7])
        self.xa.spidevice.isp.read_lockbits.side_effect=[bytes([0xFF])]
        self.xa._check_atmega48_and_88(0x1E9205)
        self.xa.spidevice.isp.write_fuse_byte.assert_not_called()

    @patch('pyavrocd.xavrdebugger.time.sleep',Mock())
    def test__check_atmega48_and_88_eesave_temporarily_programmed(self):
        self.set_up()
        self.xa.manage.append('eesave')
        self.xa.spidevice = Mock()
        self.xa.spidevice.isp.read_fuse_byte.return_value = bytes([0xDF])
        self.xa.spidevice.isp.read_lockbits.side_effect=[bytes([0xFF])]
        self.xa._check_atmega48_and_88(0x1E9205)
        isp_calls = [c for c in self.xa.spidevice.isp.mock_calls
                         if c[0] in ('write_fuse_byte', 'erase')]
        self.assertEqual(isp_calls, [call.write_fuse_byte(1, bytearray([0xD7])),
                                     call.erase(),
                                     call.erase(),
                                     call.write_fuse_byte(1, bytearray([0xDF]))])

    @patch('pyavrocd.xavrdebugger.time.sleep',Mock())
    def test__check_atmega48_and_88_eesave_restored_on_failure(self):
        self.set_up()
        self.xa.manage.append('eesave')
        self.xa.spidevice = Mock()
        self.xa.spidevice.isp.read_fuse_byte.return_value = bytes([0xDF])
        self.xa.spidevice.isp.read_lockbits.side_effect=[bytes([0x00])]
        self.assertRaises(FatalError, self.xa._check_atmega48_and_88, 0x1E9205)
        self.assertEqual(self.xa.spidevice.isp.write_fuse_byte.call_args_list[-1],
                         call(1, bytearray([0xDF])))

    @patch('pyavrocd.xavrdebugger.time.sleep',Mock())
    def test__check_atmega48_and_88_eesave_unknown(self):
        self.set_up()
        self.xa.manage.append('eesave')
        self.xa.spidevice = Mock()
        self.xa.device_info = {k: v for k, v in self.xa.device_info.items()
                                   if k not in ('eesave_base', 'eesave_mask')}
        self.xa.spidevice.isp.read_lockbits.side_effect=[bytes([0xFF])]
        self.xa._check_atmega48_and_88(0x1E9205)
        self.xa.spidevice.isp.read_fuse_byte.assert_not_called()
        self.xa.spidevice.isp.write_fuse_byte.assert_not_called()

    @patch('pyavrocd.xavrdebugger.time.sleep',Mock())
    def test__check_atmega48_and_88_eesave_not_managed(self):
        self.set_up()
        self.xa.spidevice = Mock()
        self.xa.spidevice.isp.read_lockbits.side_effect=[bytes([0xFF])]
        self.xa._check_atmega48_and_88(0x1E9205)
        self.xa.spidevice.isp.read_fuse_byte.assert_not_called()
        self.xa.spidevice.isp.write_fuse_byte.assert_not_called()


class TestEdbgBackendInterface(TestCase):
    """The parts of EdbgBackend that implement or route the DebugBackend interface"""

    def make(self, product="Atmel-ICE CMSIS-DAP"):
        args = SimpleNamespace(manage=['bootrst', 'lockbits', 'dwen', 'ocden'], clkprg=500, clkdeb=4000,
                               kbps=100, timers='r', load='n', attach=False, skipsig=False)
        transport = MagicMock()
        transport.device.product_string = product
        xa = EdbgBackend(transport, "attiny85", "debugwire", args)
        xa.logger = Mock()
        xa.device = MagicMock()
        xa.device.avr.protocol = MagicMock(spec=Avr8Protocol)
        xa.edbg_protocol = MagicMock()
        xa.flush_events = Mock()
        return xa

    def test_probe_breakpoints_and_set_up(self):
        xa = self.make()
        self.assertEqual(xa.SWBP_SUPPORT, SwbpSupport.PROBE)
        self.assertTrue(xa.is_set_up())
        self.assertFalse(xa.step_is_interrupt_safe())
        xa.software_breakpoint_clear_all()
        xa.device.avr.protocol.software_breakpoint_clear_all.assert_called_once() # the probe's, not the base class'
        xa.software_breakpoint_clear(0x100)
        xa.device.avr.protocol.software_breakpoint_clear.assert_called_once()

    def test_run_step_reach_pymcuprog_once(self):
        xa = self.make()
        with patch('pyavrocd.xavrdebugger.AvrDebugger.run') as run, \
             patch('pyavrocd.xavrdebugger.AvrDebugger.run_to') as run_to, \
             patch('pyavrocd.xavrdebugger.AvrDebugger.step') as step, \
             patch('pyavrocd.xavrdebugger.AvrDebugger.program_counter_read', return_value=0x10):
            xa.run()
            xa.run_to(0x200)
            xa.step(0x0000)
            xa.step()
        run.assert_called_once()
        run_to.assert_called_once_with(xa, 0x200)
        self.assertEqual(step.call_count, 2)

    def test_flash_read_unchanged(self):
        xa = self.make()
        xa.device.read.return_value = bytearray([1, 2, 3, 4])
        self.assertEqual(xa.flash_read(0, 4), bytearray([1, 2, 3, 4]))

    def test_run_timers(self):
        xa = self.make()
        self.assertTrue(xa.can_set_run_timers())
        xa.set_run_timers(False)
        xa.device.avr.protocol.set_byte.assert_called_with(Avr8Protocol.AVR8_CTXT_OPTIONS,
                                                           Avr8Protocol.AVR8_OPT_RUN_TIMERS, 0)

    def test_target_power(self):
        xa = self.make()
        self.assertTrue(xa.can_switch_target_power())
        xa.set_target_power(True)
        xa.edbg_protocol.set_byte.assert_called_with(EdbgProtocol.EDBG_CTXT_CONTROL,
                                                     EdbgProtocol.EDBG_CONTROL_TARGET_POWER, 1)
        xa.edbg_protocol = None
        self.assertFalse(xa.can_switch_target_power())
        with self.assertRaises(FatalError):
            xa.set_target_power(True)

    @patch('pyavrocd.backend.time.sleep')
    def test_power_cycle_only_medbg(self, mock_sleep):
        xa = self.make("Atmel-ICE CMSIS-DAP")
        self.assertFalse(xa.can_power_cycle())
        self.assertFalse(xa.power_cycle())
        xa.edbg_protocol.set_byte.assert_not_called()
        xa = self.make("mEDBG CMSIS-DAP")
        self.assertTrue(xa.can_power_cycle())
        self.assertTrue(xa.power_cycle())
        xa.edbg_protocol.set_byte.assert_has_calls([
            call(EdbgProtocol.EDBG_CTXT_CONTROL, EdbgProtocol.EDBG_CONTROL_TARGET_POWER, 0),
            call(EdbgProtocol.EDBG_CTXT_CONTROL, EdbgProtocol.EDBG_CONTROL_TARGET_POWER, 1)])
        mock_sleep.assert_has_calls([call(0.5), call(0.2)])

    def test_flash_programming(self):
        xa = self.make()
        xa.memory_info = MagicMock()
        xa.memory_info.memory_info_by_name.return_value = {'page_size': 64}
        xa.erase_chip(True)
        xa.device.erase_chip.assert_called_once_with(True)
        xa.device.erase_page.return_value = True
        self.assertTrue(xa.erase_flash_page(0x40, False))
        xa.device.erase_page.assert_called_once_with(0x40, {'page_size': 64}, False)
        xa.write_flash_pages(0x40, bytes(64), False)
        xa.device.avr.write_memory_section.assert_called_once_with(xa.flashmemtype, 0x40, bytes(64), 64,
                                                                   allow_blank_skip=False)

    def test_error_translation(self):
        xa = self.make()
        cases = [(AvrIspProtocolError("isp"), IspConnectionError),
                 (Jtagice3ResponseError("bad", Avr8Protocol.AVR8_FAILURE_INVALID_ADDRESS), InvalidAddressError),
                 (PymcuprogNotSupportedError("ns"), BackendNotSupportedError),
                 (PymcuprogError("pe"), BackendError)]
        for raised, expected in cases:
            xa.device.avr.statreg_read.side_effect = raised
            with self.assertRaises(expected):
                xa.status_register_read()
        for untouched in (Jtagice3ResponseError("other", 0x77), FatalError("f"), ValueError("v")):
            xa.device.avr.statreg_read.side_effect = untouched
            with self.assertRaises(type(untouched)):
                xa.status_register_read()
