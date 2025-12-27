"""
The test suit for the XAvrDebugger class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
from unittest.mock import MagicMock, patch,  Mock, call
from unittest import TestCase

from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.protocols.jtagice3protocol import Jtagice3ResponseError
from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.xavr8target import XTinyAvrTarget
from pyavrocd.errors import FatalError

class TestXAvrDebugger(TestCase):

    def setUp(self):
        self.xa = None
        self.xaj = None
        self.xau = None

    def set_up(self):
        mock_transport = MagicMock()
        # a debugWIRE target
        self.xa = XAvrDebugger(mock_transport, "attiny85", "debugwire", ['bootrst', 'lockbits', 'dwen'], 4000, 500, True)
        self.xa.logger = MagicMock()
        self.xa.transport = mock_transport
        self.xa.memory_info = MagicMock()
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock()
        self.xa.device.avr.protocol = MagicMock(spec=Avr8Protocol)
        self.xa.logger = Mock()
        self.xa.housekeeper = Mock()
        # a JTAG target
        self.xaj = XAvrDebugger(mock_transport, "atmega644", "jtag", ['bootrst', 'lockbits', 'ocden'], 4000, 500, True)
        self.xaj.logger = MagicMock()
        self.xaj.transport = mock_transport
        self.xaj.memory_info = MagicMock()
        self.xaj.device = MagicMock()
        self.xaj.device.avr = MagicMock()
        self.xaj.device.avr.protocol = MagicMock(spec=Avr8Protocol)
        self.xaj.housekeeper = Mock()
        # a UPDI target
        self.xau = XAvrDebugger(mock_transport, "atmega4809", "updi", ['bootrst', 'lockbits', 'ocden'], 4000, 500, True)
        self.xau.logger = MagicMock()
        self.xau.transport = mock_transport
        self.xau.memory_info = MagicMock()
        self.xau.device = MagicMock()
        self.xau.device.avr = MagicMock()
        self.xau.device.avr.protocol = MagicMock(spec=Avr8Protocol)
        self.xau.housekeeper = Mock()


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
        self.xa.device.avr.activate_physical.return_value = bytearray([0x0B, 0x93, 0, 0])
        self.xa.device.avr.protocol.program_counter_read.return_value = 0x0
        self.xa.memory_info.memory_info_by_name.return_value={'size': 0x1000}
        self.assertTrue(self.xa.start_debugging())
        self.xa.device.avr.memory_read.assert_not_called()
        self.xa.housekeeper.start_session.assert_called_once()
        self.xa.device.avr.setup_debug_session.assert_called_once()
        self.xa.device.avr.setup_config.assert_called_once()
        self.xa.device.avr.activate_physical.assert_called_once()
        self.xa.device.avr.switch_to_progmode.assert_called_once()
        self.xa.device.avr.switch_to_debmode.assert_called_once()
        self.xa.device.avr.protocol.reset.assert_called_once()
        self.xa.device.avr.protocol.program_counter_read.assert_called_once()

    @patch('pyavrocd.xavrdebugger.housekeepingprotocol.Jtagice3HousekeepingProtocol', MagicMock())
    def test_start_debugging_dw_warmstart_fail(self):
        self.set_up()
        self.xa.device.avr.activate_physical.return_value = Exception()
        self.xa.device.avr.protocol.program_counter_read.return_value = 0x0
        self.xa.memory_info.memory_info_by_name.return_value={'size': 0x1000}
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
        self.xaj.device.avr.activate_physical.return_value = bytearray([0x3F, 0x93, 0, 0])
        self.xaj.device.avr.memory_read.side_effect = [ bytearray([0x1E, 0x96, 0x09]), # signature
                                                            bytearray([0xFF]),  # lockbits
                                                            bytearray([0xFF]),  # bootrst
                                                            bytearray([0x04]),  # ocden
                                                            bytearray([0x00])  # ocden after programming
                                                            ]
        self.xaj.device.avr.protocol.program_counter_read.return_value = 0x0
        self.xaj.memory_info.memory_info_by_name.return_value={'size': 0x1000}
        self.assertTrue(self.xaj.start_debugging())
        self.assertEqual(self.xaj.device.avr.memory_read.call_count, 5)
        self.xaj.housekeeper.start_session.assert_called_once()
        self.xaj.device.avr.setup_debug_session.assert_called_once()
        self.xaj.device.avr.setup_config.assert_called_once()
        self.xaj.device.avr.activate_physical.assert_called_once()
        self.xaj.device.avr.switch_to_progmode.assert_called_once()
        self.xaj.device.avr.switch_to_debmode.assert_called_once()
        self.xaj.device.avr.protocol.reset.assert_called_once()
        self.xaj.device.avr.protocol.program_counter_read.assert_called_once()

    @patch('pyavrocd.xavrdebugger.housekeepingprotocol.Jtagice3HousekeepingProtocol', MagicMock())
    def test_start_jtag_fail(self):
        self.set_up()
        self.xaj.device.avr.activate_physical.return_value = bytearray([0x3E, 0x93, 0, 0])
        self.assertRaises(FatalError, self.xaj.start_debugging)

    def test_stop_debugging_dw(self):
        self.set_up()
        self.xa.stop_debugging(graceful=False)
        self.xa.device.avr.switch_to_debmode.assert_called_once()
        self.xa.device.avr.protocol.stop.assert_called_once()
        self.xa.device.avr.protocol.software_breakpoint_clear_all.assert_called_once()
        self.xa.device.avr.breakpoint_clear.assert_called_once()
        self.xa.device.avr.switch_to_progmode.assert_not_called()
        self.xa.device.avr.protocol.detach.assert_called_once()
        self.xa.device.avr.deactivate_physical.assert_called_once()

    def test_stop_debugging_jtag(self):
        self.set_up()
        self.xaj.stop_debugging(graceful=False)
        self.xaj.device.avr.switch_to_debmode.assert_called_once()
        self.xaj.device.avr.protocol.stop.assert_called_once()
        self.xaj.device.avr.protocol.software_breakpoint_clear_all.assert_called_once()
        self.xaj.device.avr.breakpoint_clear.assert_called_once()
        self.xaj.device.avr.switch_to_progmode.assert_called_once() # diff to dw!
        self.xaj.device.avr.protocol.detach.assert_called_once()
        self.xaj.device.avr.deactivate_physical.assert_called_once()

    def test__post_process_after_start_jtag(self):
        self.set_up()
        self.xaj._iface = 'jtag'
        self.xaj.manage = ['bootrst', 'lockbits', 'ocden']
        self.xaj.device_info['bootrst_base'] = 0x01
        self.xaj.device_info['bootrst_mask'] = 0x08
        self.xaj.device_info['ocden_base'] = 0x02
        self.xaj.device_info['ocden_mask'] = 0x04
        # read lockbits and fuses: lockbits before and after, bootrst (not set), ocden before and after
        self.xaj.device.avr.memory_read.side_effect = [bytearray([0x0F]), bytearray([0xFF]),
                                                          bytearray([0xFF]), bytearray([0x04]),
                                                          bytearray([0x00]), bytearray([0x00])]
        self.xaj._post_process_after_start()
        self.xaj.device.erase.assert_called_once()
        self.xaj.device.avr.memory_read.assert_has_calls([call(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, 0, 1),
                                                         call(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, 0, 1),
                                                         call(Avr8Protocol.AVR8_MEMTYPE_FUSES, 1, 1),
                                                         call(Avr8Protocol.AVR8_MEMTYPE_FUSES, 2, 1),
                                                         call(Avr8Protocol.AVR8_MEMTYPE_FUSES, 2, 1)])
        self.xaj.device.avr.memory_write.assert_has_calls([call(Avr8Protocol.AVR8_MEMTYPE_FUSES, 2,
                                                              bytearray([0]))])

    @patch('pyavrocd.xavrdebugger.logging.getLogger', MagicMock())
    def test__post_process_after_start_not_managed(self):
        self.set_up()
        self.xaj.device.avr.memory_read.return_value = bytes([0xFF])
        self.xaj._iface = 'jtag'
        self.xaj.manage = ['bootrst', 'lockbits']
        self.xaj.device_info['bootrst_base'] = 0x01
        self.xaj.device_info['bootrst_mask'] = 0x08
        self.xaj.device_info['ocden_base'] = 0x02
        self.xaj.device_info['ocden_mask'] = 0x04
        self.assertRaises(FatalError, self.xaj._post_process_after_start)
        self.xaj.logger.warning.assert_has_calls([
            call("Or let payavrocd manage this fuse: '-m ocden'.")])
        self.xaj.manage = ['bootrst', 'lockbits', 'ocden']


    @patch('pyavrocd.xavrdebugger.logging.getLogger', MagicMock())
    def test__post_process_after_start_nothing_to_do(self):
        self.set_up()
        self.xaj.device.avr.memory_read.side_effect = [
            bytes([0xFF]), bytes([0xFF]), bytes([0x00]) ]
        self.xaj._iface = 'jtag'
        self.xaj.manage = ['bootrst', 'lockbits', 'ocden']
        self.xaj.device_info['bootrst_base'] = 0x01
        self.xaj.device_info['bootrst_mask'] = 0x08
        self.xaj.device_info['ocden_base'] = 0x02
        self.xaj.device_info['ocden_mask'] = 0x04
        self.xaj._post_process_after_start()
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
        self.assertRaises(FatalError, self.xa._check_stuck_at_one_pc)

    def test__check_stuck_at_one_pc_ok(self):
        self.set_up()
        self.xa.device.avr.protocol.program_counter_read.return_value = 0x0000
        self.xa.memory_info.memory_info_by_name.return_value = {'size': 0x1000}
        self.xa._check_stuck_at_one_pc()

    def test__check_atmega16_fail(self):
        self.set_up()
        self.xa.memory_info.memory_info_by_name.return_value = {'size': 0x1000, 'address': 0x200}
        self.xa.device.avr.stack_pointer_read.return_value = bytearray([0xFD, 0x11]) # 0x1200-3
        self.xa.device.read.return_value =  bytearray([0x40, 0x00])
        self.assertRaises(FatalError, self.xa._check_atmega16)

    def test__check_atmega16_ok(self):
        self.set_up()
        self.xa.memory_info.memory_info_by_name.return_value = {'size': 0x1000, 'address': 0x200}
        self.xa.device.avr.stack_pointer_read.return_value = bytearray([0xFD, 0x11]) # 0x1200-3
        self.xa.device.read.return_value =  bytearray([0x01, 0x00])
        self.xa._check_atmega16()

    @patch('pyavrocd.xavrdebugger.logging.getLogger', MagicMock())
    def test__check_atmega16_no_irq(self):
        self.set_up()
        self.xa.memory_info.memory_info_by_name.return_value = {'size': 0x1000, 'address': 0x200}
        self.xa.device.avr.stack_pointer_read.return_value = bytearray([0xFF, 0x11]) # 0x1200-3
        self.xa.device.read.return_value =  bytearray([0x01, 0x00])
        self.xa._check_atmega16()
        self.xa.logger.error.assert_has_calls([
            call("IRQ has not been raised!")])


    def test__activate_interface_ok(self):
        self.set_up()
        self.xa.device.avr.activate_physical.return_value = bytearray([0x01, 0x02, 0x03, 0x04])
        self.assertEqual(self.xa._activate_interface(), 0x04030201)

    def test__activate_interface_fail(self):
        self.set_up()
        self.xa.device.avr.activate_physical.side_effect = Jtagice3ResponseError("Error",
                                    Avr8Protocol.AVR8_FAILURE_INVALID_PHYSICAL_STATE)
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
        self.set_up()
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

    @patch('pyavrocd.xavrdebugger.logging.getLogger', MagicMock())
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
    @patch('pyavrocd.xavrdebugger.logging.getLogger', MagicMock())
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
    def test__check_atmega48_and_88_fail(self):
        self.set_up()
        self.xa.spidevice = Mock()
        self.xa.spidevice.read.side_effect=[bytes([0x00])]
        self.assertRaises(FatalError, self.xa._check_atmega48_and_88, 0x1E9025)

    @patch('pyavrocd.xavrdebugger.time.sleep',Mock())
    def test__check_atmega48_and_88_ok(self):
        self.set_up()
        self.xa.spidevice = Mock()
        self.xa.spidevice.read.side_effect=[bytes([0xFF])]
        self.xa._check_atmega48_and_88(0x1E9025)

    @patch('pyavrocd.xavrdebugger.time.sleep',Mock())
    def test__check_atmega48_and_88_atmega88_ok(self):
        self.set_up()
        self.xa.spidevice = Mock()
        self.xa.spidevice.read.side_effect=[bytes([0xFF])]
        self.xa._check_atmega48_and_88(0x1E930A)

    @patch('pyavrocd.xavrdebugger.time.sleep',Mock())
    @patch('pyavrocd.xavrdebugger.read_target_voltage', MagicMock(side_effect=[
        5.0, 5.0, 0.0, 0.0, 0.0, 5.0, 5.0, 5.0]))
    @patch('pyavrocd.xavrdebugger.logging.getLogger', MagicMock())
    def test__power_cycle(self):
        self.set_up()
        self.xa._power_cycle()
        self.xa.logger.info.assert_has_calls([call("Signed on to tool again")])

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
