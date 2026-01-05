"""
The test suit for the GdbHandler class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
from unittest.mock import Mock, MagicMock, patch, call, create_autospec
from unittest import TestCase
import socket
from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.protocols.edbgprotocol import EdbgProtocol
from pyedbglib.protocols.avrispprotocol import AvrIspProtocolError
from pymcuprog.pymcuprog_errors import PymcuprogError
from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.handler import GdbHandler
from pyavrocd.errors import EndOfSession, FatalError
from pyavrocd.memory import Memory
from pyavrocd.monitor import MonitorCommand
from pyavrocd.livetests import LiveTests
from pyavrocd.main import options
from pyavrocd.breakexec import BreakAndExec, SIGHUP, SIGINT, SIGILL, SIGBUS, SIGSYS

# generate an RSP packet from a string
def rsp(packet):
    checksum = sum(packet.encode("ascii")) % 256
    return ("$%s#%02x" % (packet, checksum)).encode("ascii")

class TestGdbHandler(TestCase):

    def setUp(self):
        self.gh = None

    @patch('pyavrocd.handler.logging.getLogger', MagicMock())
    def set_up(self):
        mock_socket = create_autospec(socket.socket, spec_set=True, instance=True)
        mock_dbg = create_autospec(XAvrDebugger, spec_set=False, instance=True)
        mock_dbg.memory_info = MagicMock()
        mock_dbg.device_info = MagicMock()
        mock_dbg.transport = MagicMock()
        mock_dbg.edbg_protocol = MagicMock()
        mock_dbg.device = Mock()
        mock_dbg.device.avr = Mock()
        mock_dbg.get_iface.return_value = 'debugwire'
        mock_dbg.memory_info.memory_info_by_name('flash')['size'].__gt__ = lambda self, compare: False
        # setting up the GbdHandler instance we want to test
        self.gh = GdbHandler(mock_socket, mock_dbg, "atmega328p",
                                 options(['-f', 'foo', '-d', 'atmega328p']), "Tool")
        self.gh.mon = create_autospec(MonitorCommand, specSet=True, instance=True)
        self.gh.mon.is_onlycache.return_value = False
        self.gh.mem = create_autospec(Memory, specSet=True, instance=True)
        self.gh.mem.lazy_loading = False
        self.gh.mem.programming_mode = False
        self.gh.bp = create_autospec(BreakAndExec, specSet=True, instance=True)
        self.gh._live_tests = create_autospec(LiveTests, specSet=True, instance=True)

    def test_rsp_packet_construction(self):
        self.set_up()
        self.assertEqual(b'$#00', rsp(''))
        self.assertEqual(b'$abc#26', rsp('abc'))

    def test_unknownPacket(self):
        self.set_up()
        self.gh.dispatch('_', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp(""))

    @patch('pyavrocd.handler.GdbHandler._set_binary_memory_handler_finalize',Mock())
    def test_empty_packet(self):
        self.set_up()
        self.gh.mem.lazy_loading = True
        self.gh.dispatch(None,'')
        self.assertEqual(self.gh._set_binary_memory_handler_finalize.call_count, 2) #pylint: disable=no-member


    def test_exception_in_packet_handler(self):
        self.set_up()
        self.gh.critical = None
        self.gh.dispatch('!', None)
        self.gh._comsocket.sendall.assert_called_with(rsp("S06"))
        self.assertFalse(self.gh.critical is None)
        self.gh.critical = None

    def test_extended_remote_handler(self):
        self.set_up()
        self.assertFalse(self.gh._extended_remote_mode)
        self.gh.dispatch('!', b'')
        self.assertTrue(self.gh._extended_remote_mode)
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    @patch('pyavrocd.handler.GdbHandler._set_binary_memory_handler_finalize',Mock())
    def test_extended_remote_when_lazy_loading(self):
        self.set_up()
        self.gh.mem.lazy_loading = True
        self.assertFalse(self.gh._extended_remote_mode)
        self.gh.dispatch('!', b'')
        self.assertTrue(self.gh._extended_remote_mode)
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))
        self.assertEqual(self.gh._set_binary_memory_handler_finalize.call_count, 1) #pylint: disable=no-member

    def test_stop_reason_handler_none(self):
        self.set_up()
        self.gh.last_sigval = None
        self.gh.dispatch('?', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("S00"))

    def test_stop_reason_handler_SIGINT(self):
        self.set_up()
        self.gh.last_sigval = SIGINT
        self.gh.dispatch('?', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("S02"))

    def test__send_execution_results_SIGSYS(self):
        self.set_up()
        self.gh._send_execution_result_signal(SIGSYS)
        self.gh._comsocket.sendall.assert_called_with(rsp("S0C"))
        self.gh.logger.warning.assert_called_with("Too many breakpoints.")

    def test__send_execution_results_SIGILL(self):
        self.set_up()
        self.gh._send_execution_result_signal(SIGILL)
        self.gh._comsocket.sendall.assert_called_with(rsp("S04"))
        self.gh.logger.warning.assert_called_with("Cannot execute because of BREAK instruction.")

    def test__send_execution_results_SIGBUS(self):
        self.set_up()
        self.gh._send_execution_result_signal(SIGBUS)
        self.gh._comsocket.sendall.assert_called_with(rsp("S0A"))
        self.gh.logger.warning.assert_called_with("Cannot execute because stack pointer is too low.")

    def test_continue_handler_impossible_debugwire(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.mem.is_flash_empty.return_value = True
        self.gh.mon.is_noload.return_value = False
        self.gh.dbg.status_register_read.return_value = [0x55]
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.program_counter_read.return_value = 0x00003421
        self.gh.dispatch('vCont',b';c')
        self.gh._comsocket.sendall.assert_has_calls([
            call(rsp("O456E61626C65206465627567574952452066697273743A202" + \
                         "76D6F6E69746F722064656275677769726520656E61626C65270A")),
            call(rsp("S01"))])

    def test_continue_handler_impossible_jtag(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.mem.is_flash_empty.return_value = True
        self.gh.mon.is_noload.return_value = False
        self.gh.dbg.status_register_read.return_value = [0x55]
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.program_counter_read.return_value = 0x00003421
        self.gh.dbg.get_iface.return_value = 'jtag'
        self.gh.dispatch('vCont',b';c')
        self.gh._comsocket.sendall.assert_has_calls([
            call(rsp("O4A5441472070696E7320617265206E6F7420656E61626C65640A")),
            call(rsp("S01"))])

    def test_continue_handler_impossible_other_iface(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.mem.is_flash_empty.return_value = True
        self.gh.mon.is_noload.return_value = False
        self.gh.dbg.status_register_read.return_value = [0x55]
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.program_counter_read.return_value = 0x00003421
        self.gh.dbg.get_iface.return_value = 'updi'
        self.gh.dispatch('vCont',b';c')
        self.gh._comsocket.sendall.assert_has_calls([
            call(rsp("O4E6F20636F6E6E656374696F6E20746F204F43442E20456E61626C6520646562756767696E672066697273740A")),
            call(rsp("S01"))])

    def test_continue_handler_impossible_not_loaded(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.mem.is_flash_empty.return_value = True
        self.gh.mon.is_noload.return_value = False
        self.gh.dbg.status_register_read.return_value = [0x55]
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.program_counter_read.return_value = 0x00003421
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('vCont',b';c')
        self.gh._comsocket.sendall.assert_has_calls([
            call(rsp("O4E6F2070726F6772616D206C6F616465643B2063616E6E6F7420" + \
                         "737461727420657865637574696F6E0A")),
            call(rsp("S0B"))])

    def test_continue_handler_without_start(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.is_flash_empty.return_value = False
        self.gh.bp.resume_execution.return_value = None
        self.gh.dbg.program_counter_read.return_value = 1
        self.gh.dispatch('vCont',b';c')
        self.gh.bp.resume_execution.assert_called_with(None)
        self.gh._comsocket.sendall.assert_not_called()

    def test_continue_with_signal_handler_without_start(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.is_flash_empty.return_value = False
        self.gh.bp.resume_execution.return_value = None
        self.gh.dispatch('vCont',b';C09')
        self.gh.bp.resume_execution.assert_called_with(None)
        self.gh._comsocket.sendall.assert_not_called()

    def test_continue_after_critical_error(self):
        self.set_up()
        self.gh.critical = True
        self.gh.dispatch('vCont',b';C06')
        self.gh._comsocket.sendall.assert_called_with(rsp("S06"))

    def test_detach_handler(self):
        self.set_up()
        with self.assertRaises(EndOfSession):
            self.gh.dispatch('D',b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_get_register_handler_impossible(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('g',b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2000341200000000"))

    def test_get_register_handler(self):
        self.set_up()
        self.gh.dbg.program_counter_read.return_value = 0x00003421
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.status_register_read.return_value = [0x55]
        self.gh.dbg.register_file_read.return_value = bytearray(list(range(32)))
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('g',b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f55341242680000"))

    def test_setRegisterHandle_impossible(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('G',b'000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f66341242680000')
        self.gh.dbg.program_counter_write.assert_not_called()
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_setRegisterHandle(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('G',b'000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f66341242680000')
        self.gh.dbg.register_file_write.assert_called_with(bytearray(list(range(32))))
        self.gh.dbg.status_register_write.assert_called_with(bytearray([0x66]))
        self.gh.dbg.stack_pointer_write.assert_called_with(bytearray(bytearray([0x34, 0x12])))
        self.gh.dbg.program_counter_write.assert_called_with(0x00003421)
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_set_thread_handler(self):
        self.set_up()
        self.gh.dispatch('H',b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_get_memory_handler_impossible(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('m',b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("E01"))

    def test_get_memory_handler_chunk(self):
        # read chunk from memory
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.readmem.return_value = b'\x01\x02\x03\x04'
        self.gh.dispatch('m',b'800101,4')
        self.gh._comsocket.sendall.assert_called_with(rsp("01020304"))
        self.gh.mem.readmem.assert_called_with("800101", "4")

    def test_get_memory_handler_empty_request(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.readmem.return_value = None
        self.gh.dispatch('m',b'800101,0')
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))
        self.gh.mem.readmem.assert_not_called()

    def test_get_memory_handler_empty_return(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.readmem.return_value = b''
        self.gh.dispatch('m',b'800101,4')
        self.gh._comsocket.sendall.assert_called_with(rsp("E14"))
        self.gh.mem.readmem.assert_called_with("800101", "4")

    def test_set_memory_handler_impossible(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('M', b'800100,0:')
        self.gh._comsocket.sendall.assert_called_with(rsp('E01'))

    def test_set_memory_handler_byte(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.writemem.return_value = "OK"
        self.gh.dispatch('M', b'800100,1:63')
        self.gh.mem.writemem.assert_called_with("800100", bytes([0x63]))
        self.gh._comsocket.sendall.assert_called_with(rsp('OK'))

    def test_set_memory_handler_failure(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.writemem.return_value = "OK"
        self.gh.dispatch('M', b'800100,2:63')
        self.gh.mem.writemem.assert_not_called()
        self.gh._comsocket.sendall.assert_called_with(rsp('E15'))

    def test_get_one_register_handler_impossible(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('p', b'22')
        self.gh._comsocket.sendall.assert_called_with(rsp("E01"))

    def test_get_one_register_handler_pc(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dbg.program_counter_read.return_value = 0x123
        self.gh.dispatch('p', b'22')
        self.gh._comsocket.sendall.assert_called_with(rsp("46020000"))

    def test_get_one_register_handler_sp(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x23,0x01])
        self.gh.dispatch('p', b'21')
        self.gh._comsocket.sendall.assert_called_with(rsp("2301"))

    def test_get_one_register_handler_sreg(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dbg.status_register_read.return_value = bytearray([0x01])
        self.gh.dispatch('p', b'20')
        self.gh._comsocket.sendall.assert_called_with(rsp("01"))

    def test_get_one_register_handler_reg(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dbg.sram_read.return_value = bytearray([0x23])
        self.gh.dispatch('p', b'07')
        self.gh._comsocket.sendall.assert_called_with(rsp("23"))

    def test_set_one_register_handler_impossible(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('P', b'22=04200000')
        self.gh._comsocket.sendall.assert_called_with(rsp("E01"))

    def test_set_one_register_handler_pc(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('P', b'22=04200000')
        self.gh.dbg.program_counter_write.assert_called_with(0x2004>>1)
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_set_one_register_handler_sp(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('P', b'21=0420')
        self.gh.dbg.stack_pointer_write.assert_called_with(bytearray([0x04, 0x20]))
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_set_one_register_handler_sreg(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('P', b'20=04')
        self.gh.dbg.status_register_write.assert_called_with(bytearray([0x04]))
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_set_one_register_handler_reg(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('P', b'10=ee')
        self.gh.dbg.sram_write.assert_called_with(0x10, bytearray([0xee]))
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_attached_handler(self):
        self.set_up()
        self.gh.dispatch('qAttached', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("1"))

    def test_offsets_handler(self):
        self.set_up()
        self.gh.dispatch('qOffsets', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("Text=000;Data=000;Bss=000"))

    def test_monitorCommand_dwon_ok(self):
        self.set_up()
        self.gh.mon.dispatch.return_value = ('dwon', 'BlaBla')
        self.assertEqual(self.gh.dispatch('qRcmd', b',642065'), None)
        self.gh.dbg.prepare_debugging.assert_called_once()
        self.gh.dbg.start_debugging.assert_called_once()
        self.gh.mon.set_debug_mode_active.assert_called_once()
        self.gh._comsocket.sendall.assert_called_with(rsp("426C61426C610A"))

    def test_monitorCommand_dwon_critical(self):
        self.set_up()
        self.gh.critical = "Critical"
        self.gh.mon.dispatch.return_value = ('dwon', 'Bla')
        self.assertEqual(self.gh.dispatch('qRcmd', b',642065'), None)
        self.gh.dbg.prepare_debugging.assert_not_called()
        self.gh._comsocket.sendall.assert_called_with(
            rsp("466174616C206572726F723A20437269746963616C0A")) # error message

    def test_monitorCommand_dwoff(self):
        self.set_up()
        self.gh.mon.dispatch.return_value = ('dwoff', 'BlaBlaBla')
        self.assertEqual(self.gh.dispatch('qRcmd', b',642064'), None)
        self.gh.dbg.dw_disable.assert_called_once()
        self.gh._comsocket.sendall.assert_called_with(rsp("426C61426C61426C610A"))

    def test_monitorCommand_Target_0(self):
        self.set_up()
        self.gh.mon.dispatch.return_value = (0, 'B')
        self.assertEqual(self.gh.dispatch('qRcmd', b',5461726765742030'), None)
        self.gh.dbg.device.avr.protocol.set_byte.assert_called_with(
            Avr8Protocol.AVR8_CTXT_OPTIONS,
            Avr8Protocol.AVR8_OPT_RUN_TIMERS, 0)
        self.gh._comsocket.sendall.assert_called_with(rsp("420A"))

    def test_monitorCommand_reset(self):
        self.set_up()
        self.gh.mon.dispatch.return_value = ('reset', 'Bla')
        self.gh.dispatch('qRcmd', b',7265736574')
        self.assertTrue(self.gh.dbg.reset.called)
        self.gh._comsocket.sendall.assert_called_with(rsp("426C610A"))

    def test_monitorCommand_Target_on(self):
        self.set_up()
        self.gh.mon.dispatch.return_value = ('power on', 'Blub')
        self.gh.dispatch('qRcmd', b',546172676574206F6E') # Target on
        self.gh.dbg.edbg_protocol.set_byte.assert_called_with(
            EdbgProtocol.EDBG_CTXT_CONTROL,
            EdbgProtocol.EDBG_CONTROL_TARGET_POWER,
            True)
        self.gh._comsocket.sendall.assert_called_with(rsp("426C75620A"))

    def test_monitorCommand_Target_query(self):
        self.set_up()
        self.gh.mon.dispatch.return_value = ('power query', 'Bla')
        self.gh.dispatch('qRcmd', b',546172676574207175657279') # Target query
        self.gh.dbg.edbg_protocol.query.assert_called_with(
            EdbgProtocol.EDBG_QUERY_COMMANDS)
        self.gh._comsocket.sendall.assert_called_with(rsp("426C610A"))

    def test_monitorCommand_info_ok(self):
        self.set_up()
        self.gh.critical = None
        self.gh.mon.dispatch.return_value = ("info", "INFO {} {}")
        self.gh.dbg.device_info.__getitem__.return_value = 0x1E950F
        self.gh.dispatch('qRcmd', b',696E666F') # info
        self.gh._comsocket.sendall.assert_called_with(
            rsp("494E464F2061746D65676133323870200A")) # INFO atmega328p

    def test_monitorCommand_info_critical(self):
        self.set_up()
        self.gh.critical = "Critical"
        self.gh.mon.dispatch.return_value = ("info", "INFO {} {}")
        self.gh.dbg.device_info.__getitem__.return_value = 0x1E950F
        self.gh.dispatch('qRcmd', b',696E666F') # info
        self.gh._comsocket.sendall.assert_called_with(
            rsp("494E464F2061746D65676133323870200A4C6173742063726" + \
                    "9746963616C206572726F723A202020202020437269746963616C0A"))

    def test_monitorCommand_ISP_error(self):
        self.set_up()
        self.gh.critical = None
        self.gh.mon.dispatch.return_value = ('dwon', 'Bla')
        self.gh.dbg.prepare_debugging = Mock(side_effect=AvrIspProtocolError("XXX"))
        self.assertEqual(self.gh.dispatch('qRcmd', b',642065'), None)
        self.gh.dbg.prepare_debugging.assert_called_once()
        self.gh._comsocket.sendall.assert_called_with(
            rsp("4953502070726F6772616D6D696E67206661696C65642E2057726F6E6720636F6E6E656374696F6E206F722077726F6E67204D43553F0A")) # ISP error message

    def test_monitorCommand_pymcuprog_error(self):
        self.set_up()
        self.gh.critical = None
        self.gh.mon.dispatch.return_value = ('dwon', 'Bla')
        self.gh.dbg.prepare_debugging = Mock(side_effect=PymcuprogError("XXX"))
        self.assertEqual(self.gh.dispatch('qRcmd', b',642065'), None)
        self.gh.dbg.prepare_debugging.assert_called_once()
        self.gh._comsocket.sendall.assert_called_with(
            rsp("466174616C206572726F723A205858580A")) # Fatal error: XXX


    def test_monitorCommand_LiveTests(self):
        self.set_up()
        self.gh.mon.dispatch.return_value = ('live_tests', 'Tests done')
        self.gh.dispatch('qRcmd', b',4C6976655465737473')
        self.assertTrue(self.gh._live_tests.run_tests.called)
        self.gh._comsocket.sendall.assert_called_with(rsp("546573747320646F6E650A"))

    @patch('pyavrocd.handler.time.sleep')
    def test__send_power_cycle_automatic(self, mock_sleep):
        self.set_up()
        self.gh.dbg.transport.device.product_string.lower.return_value = "medbg blabla"
        self.assertTrue(self.gh._send_power_cycle())
        self.gh.dbg.edbg_protocol.set_byte.assert_has_calls([
            call(EdbgProtocol.EDBG_CTXT_CONTROL,
                 EdbgProtocol.EDBG_CONTROL_TARGET_POWER,
                 0),
            call(EdbgProtocol.EDBG_CTXT_CONTROL,
                 EdbgProtocol.EDBG_CONTROL_TARGET_POWER,
                 1)])
        self.assertEqual(mock_sleep.call_count, 2)

    @patch('pyavrocd.handler.time.sleep')
    def test__send_power_cycle_manual(self, mock_sleep):
        self.set_up()
        self.gh.dbg.transport.device.product_string.lower.return_value = "uno"
        self.assertFalse(self.gh._send_power_cycle())
        self.assertEqual(mock_sleep.call_count, 0)
        self.gh._comsocket.sendall.assert_called_with(
            rsp("O2A2A2A20506C6561736520706F7765722D6379636C6" + \
                    "520746865207461726765742073797374656D202A2A2A0A"))
                    # *** Please power-cycle the system ***

    def test__send_ready_message(self):
        self.set_up()
        self.gh._send_ready_message()
        self.gh._comsocket.sendall.assert_called_with(
            rsp("O2A2A2A20506F7765722D646F776E207265636F676E6" + \
                    "97A65642E204170706C7920706F77657220616761696E21202A2A2A0A"))
                    # *** Power-down recognized. Apply power again! ***

    def test_supported_handler(self):
        self.set_up()
        self.gh.dbg.start_debugging.return_value = True
        self.gh.dispatch('qSupported', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("PacketSize={0:X};qXfer:memory-map:read+".format(self.gh.packet_size)))
        self.gh.mon.set_debug_mode_active.assert_called_once()

    def test_supported_handler_error(self):
        self.set_up()
        self.gh.dbg.start_debugging.side_effect = FatalError("XXX")
        self.gh.dispatch('qSupported', b'')
        self.gh.mon.set_debug_mode_active.assert_not_called()
        self.gh.dbg.stop_debugging.assert_called_once()
        self.gh._comsocket.sendall.assert_called_with(rsp("PacketSize={0:X};qXfer:memory-map:read+".format(self.gh.packet_size)))

    def test_first_thread_info_handler(self):
        self.set_up()
        self.gh.dispatch('qfThreadInfo', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("m01"))

    def test_subsequent_thread_info_handler(self):
        self.set_up()
        self.gh.dispatch('qsThreadInfo', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("l"))

    def test_memory_map_handler(self):
        self.set_up()
        self.gh.mon.is_noxml.return_value = False
        self.gh.mem.memory_map.return_value="map"
        self.gh.dispatch('qXfer', b':memory-map:read::0,1000')
        self.gh.mem.memory_map.assert_called_once()

    def test_no_memory_map_handler(self):
        self.set_up()
        self.gh.mon.is_noxml.return_value = False
        self.gh.dispatch('qXfer', b':huhu')
        self.gh.mem.memory_map.assert_not_called()
        self.gh._comsocket.sendall.assert_called_with(rsp(""))

    def test_step_handler_impossible(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value=False
        self.gh.mem.is_flash_empty.return_value = True
        self.gh.mon.is_noload.return_value = False
        self.gh.dispatch('vCont', b';s')
        self.gh._comsocket.sendall.assert_called_with(rsp("S01"))
        self.gh.mon.is_debugger_active.return_value=True
        self.gh.dispatch('vCont', b';s')
        self.gh._comsocket.sendall.assert_called_with(rsp("S0B"))

    def test_step_handler_without_start(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value=True
        self.gh.mem.is_flash_empty.return_value = False
        self.gh.mon.is_noload.return_value = False
        self.gh.dbg.program_counter_read.return_value = 0x00000101
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.status_register_read.return_value = [0x55]
        self.gh.bp.single_step.return_value = 5
        self.gh.dispatch('vCont', b';s')
        self.gh.bp.single_step.assert_called_with(None)
        self.gh._comsocket.sendall.assert_called_with(rsp("T0520:55;21:3412;22:02020000;thread:1;"))

    def test_step_with_signal_handler(self):
        self.set_up()
        self.gh._step_handler = Mock()
        self.gh.dispatch('vCont', b';S09')
        self.gh._step_handler.assert_has_calls([call('')])

    def test_thread_alive_handler(self):
        self.set_up()
        self.gh.dispatch('T', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_vcont_handler_query(self):
        self.set_up()
        self.gh.dispatch('vCont', b'?')
        self.gh._comsocket.sendall.assert_called_with(rsp("vCont;c;C;s;S;r"))

    @patch('pyavrocd.handler.GdbHandler._continue_handler')
    def test_vcont_handler_continue(self, mock_handler):
        self.set_up()
        self.gh.dispatch('vCont', b';c')
        mock_handler.assert_called_once()

    @patch('pyavrocd.handler.GdbHandler._step_handler')
    def test_vcont_handler_step(self, mock_handler):
        self.set_up()
        self.gh.dispatch('vCont', b';S')
        mock_handler.assert_called_once()

    def test_vcont_handler_rangestep(self):
        self.set_up()
        self.gh.bp.range_step.return_value = SIGILL
        self.gh.dispatch('vCont', b';r0020,0040:1')
        self.gh.bp.range_step.assert_called_with(32,64)
        self.gh._comsocket.sendall.assert_called_with(rsp("S04"))

    def test_vcont_handler_illformed1(self):
        self.set_up()
        self.gh.dispatch('vCont', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp(""))

    def test_vcont_handler_illformed2(self):
        self.set_up()
        self.gh.dispatch('vCont', b';')
        self.gh._comsocket.sendall.assert_called_with(rsp(""))

    def test_vcont_handler_illformed3(self):
        self.set_up()
        self.gh.dispatch('vCont', b';x')
        self.gh._comsocket.sendall.assert_called_with(rsp(""))

    def test_vcont_handler_illformed4(self):
        self.set_up()
        self.gh.dispatch('vCont', b'!')
        self.gh._comsocket.sendall.assert_called_with(rsp(""))


    def test_flashDoneHandler(self):
        self.set_up()
        self.gh.dispatch('vFlashDone', b'')
        self.gh.mem.flash_pages.assert_called_once()
        self.gh.mon.disable_onlycache.assert_not_called()
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_flashDoneHandler_onlycache(self):
        self.set_up()
        self.gh.mon.is_onlycache.return_value = True
        self.gh.dispatch('vFlashDone', b'')
        self.gh.mem.flash_pages.assert_called_once()
        self.gh.mon.disable_onlycache.assert_called_once()
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_flashDoneHandler_error(self):
        self.set_up()
        self.gh.dbg.switch_to_progmode.side_effect=FatalError("XXX")
        self.gh.dispatch('vFlashDone', b'')
        self.gh.dbg.switch_to_progmode.assert_called_once()
        self.gh.mem.flash_pages.assert_not_called()
        self.assertEqual(self.gh._comsocket.sendall.call_count, 2)
        self.gh._comsocket.sendall.assert_has_calls([call(rsp("E11")), call(rsp("S06"))])

    def test_flashEraseHandler_impossible(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('vFlashErase', b':100,10')
        self.gh._comsocket.sendall.assert_called_with(rsp("E01"))

    def test_flashEraseHandler_fresh(self):
        self.set_up()
        self.gh._vflashdone = True
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('vFlashErase', b':100,10')
        self.assertFalse(self.gh._vflashdone)
        self.gh.dispatch('vFlashErase', b':200,10')
        self.gh.mem.init_flash.assert_called_once()
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_flash_writeHandler_success(self):
        self.set_up()
        self.gh.dispatch('vFlashWrite', b':0100:ABC')
        self.gh.mem.store_to_cache.assert_called_with(0x100,[ord('A'), ord('B'), ord('C')])
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_escape(self):
        self.set_up()
        seq = [ 0x7d, 0xFF, 0x2A, 0x00, 0x23, 0x24 ]
        self.assertEqual(self.gh.escape(seq),bytes([0x7d, 0x5d, 0xFF, 0x7D, 0x0A, 0x00, 0x7D, 0x03, 0x7D, 0x04]))

    def test_unescape(self):
        self.set_up()
        seq = [0x7d, 0x5d, 0xFF, 0x7D, 0x0A, 0x00, 0x7D, 0x03, 0x7D, 0x04]
        self.assertEqual(self.gh.unescape(seq),[ 0x7d, 0xFF, 0x2A, 0x00, 0x23, 0x24 ])

    def test_kill_handler_not_exteded_remote(self):
        self.set_up()
        self.gh._extended_remote_mode = False
        with self.assertRaises(EndOfSession):
            self.gh.dispatch('vKill', b'')
        self.gh.dbg.reset.assert_called_once()

    def test_kill_handler_exteded_remote(self):
        self.set_up()
        self.gh._extended_remote_mode = True
        self.gh.dispatch('vKill', b'')
        self.gh.dbg.reset.assert_called_once()
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_run_handler_impossible(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('vRun', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("S01"))

    def test_run_handler(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dbg.program_counter_read.return_value = 0x00000101
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.status_register_read.return_value = [0x77]
        self.gh.dispatch('vRun', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("T0520:77;21:3412;22:02020000;thread:1;"))
        self.gh.dbg.reset.assert_called_once()

    def test_set_binary_memory_handler_impossible(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('X',b'800100,1:}]')
        self.gh._comsocket.sendall.assert_called_with(rsp("E01"))

    def test_set_binary_memory_handler_wrong_size(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('X',b'800100,2:}]')
        self.gh._comsocket.sendall.assert_called_with(rsp("E15"))

    def test_set_binary_memory_handler_byte(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.writemem.return_value = "OK"
        self.gh.dispatch('X', b'800100,1:}]')
        self.gh.mem.writemem.assert_called_with("800100", bytearray([0x7D]))
        self.gh._comsocket.sendall.assert_called_with(rsp('OK'))

    def test_set_binary_memory_handler_flash(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.writemem.return_value = "OK"
        self.gh.mem.lazy_loading = False
        self.gh.mon.is_erase_before_load.return_value = True
        self.gh.dispatch('X', b'100,1:}]')
        self.gh.bp.cleanup_breakpoints.assert_called_once()
        self.gh.dbg.switch_to_progmode.assert_called_once()
        self.gh.dbg.device.erase_chip.assert_called_once()
        self.assertTrue(self.gh.mem.lazy_loading)
        self.gh._comsocket.sendall.assert_called_with(rsp('OK'))

    def test_set_binary_memory_handler_exception(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.writemem.side_effect = FatalError("XXX")
        self.gh.dispatch('X', b'100,1:}]')
        self.assertEqual(self.gh._comsocket.sendall.call_count, 2)
        self.gh._comsocket.sendall.assert_has_calls([call(rsp('E11')), call(rsp('S06'))])


    def test_set_binary_memory_handler_finalize_no_action(self):
        self.set_up()
        self.gh.mem.lazy_loading = False
        self.assertEqual(self.gh.dispatch(None,None), None)
        self.gh.mem.flash_pages.assert_not_called()
        self.gh.mon.disable_onlycache.assert_not_called()

    def test_set_binary_memory_handler_finalize_finish_action(self):
        self.set_up()
        self.gh.mon.is_onlycache.return_value = True
        self.gh.mem.lazy_loading = True
        self.assertEqual(self.gh.dispatch(None,None), None)
        self.gh.mem.flash_pages.assert_called_once()
        self.assertFalse(self.gh.mem.lazy_loading)
        self.gh.mon.disable_onlycache.assert_called_once()

    def test_remove_breakpoint_handler_impossible(self):
        self.set_up()
        # even when debugger is not active, success is returned
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('z',b'0,111,2')
        self.gh._comsocket.sendall.assert_called_with(rsp('OK'))

    def test_remove_breakpoint_handler_wrong_type(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('z',b'2,111,2')
        self.gh._comsocket.sendall.assert_called_with(rsp(''))

    def test_remove_breakpoint_handler(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('z',b'0,222,2')
        # note: for  breakpoints, it is always the byte address!
        self.gh.bp.remove_breakpoint.assert_called_with(0x222)
        self.gh._comsocket.sendall.assert_called_with(rsp('OK'))

    def test_add_breakpoint_handler_impossible(self):
        self.set_up()
        # even when debugger is not active, success is returned
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('Z',b'0,111,2')
        self.gh._comsocket.sendall.assert_called_with(rsp('OK'))

    def test_add_breakpoint_handler_wrong_type(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('Z',b'2,111,2')
        self.gh._comsocket.sendall.assert_called_with(rsp(''))

    def test_add_breakpoint_handler_new(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('Z',b'0,222,2')
        # note: for  breakpoints, it is always the byte address!
        self.gh.bp.insert_breakpoint.assert_called_with(0x222)
        self.gh._comsocket.sendall.assert_called_with(rsp('OK'))

    def test_poll_events_impossible(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.poll_events()
        self.gh.dbg.poll_event.assert_not_called()

    def test_poll_events_positive(self):
        self.set_up()
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dbg.poll_event.return_value = 0x101
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dbg.program_counter_read.return_value = 0x00000101
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.status_register_read.return_value = [0x88]
        self.gh.poll_events()
        self.gh.dbg.poll_event.assert_called_once()
        self.gh._comsocket.sendall.assert_called_with(rsp("T0520:88;21:3412;22:02020000;thread:1;"))

    @patch('pyavrocd.server.select.select', Mock(return_value=[None, None, None]))
    def test_poll_gdb_input_false(self):
        self.set_up()
        self.assertFalse(self.gh.poll_gdb_input())

    @patch('pyavrocd.server.select.select', Mock(return_value=[[1], None, None]))
    def test_poll_gdb_input_true(self):
        self.set_up()
        self.assertTrue(self.gh.poll_gdb_input())

    def test_send_packet(self):
        self.set_up()
        self.gh.send_packet("abc")
        self.gh._comsocket.sendall.assert_called_with(rsp("abc"))

    def test_send_reply_packet(self):
        self.set_up()
        self.gh.send_reply_packet("Hello World")
        self.gh._comsocket.sendall.assert_called_with(rsp("48656C6C6F20576F726C640A"))

    def test_send_debug_message(self):
        self.set_up()
        self.gh.send_debug_message("Hello World")
        self.gh._comsocket.sendall.assert_called_with(rsp("O48656C6C6F20576F726C640A"))

    def test_send_signal_none(self):
        self.set_up()
        self.gh.send_signal(None)
        self.gh._comsocket.sendall.assert_not_called()
        self.assertEqual(self.gh.last_sigval, None)

    def test_send_signal_SIGINT(self):
        self.set_up()
        self.gh.dbg.program_counter_read.return_value = 0x00000404
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.status_register_read.return_value = [0x99]
        self.gh.send_signal(SIGINT)
        self.gh._comsocket.sendall.assert_called_with(rsp("T0220:99;21:3412;22:08080000;thread:1;"))

    def test_send_signal_SIGHUP(self):
        self.set_up()
        self.gh.send_signal(SIGHUP)
        self.gh._comsocket.sendall.assert_called_with(rsp("S01"))

    def test_handle_data_ACK_NACK(self):
        self.set_up()
        self.gh._lastmessage = 'bla'
        self.gh.handle_data(b'++---+---')
        self.gh._comsocket.sendall.assert_called_with(rsp("bla"))

    def test_handle_data_NACK_ACK_ignore_NAK(self):
        self.set_up()
        self.gh._lastmessage = 'bla'
        self.gh.handle_data(b'--------+ ---')
        self.gh._comsocket.sendall.assert_called_with(rsp(""))

    def test_handle_data_CTRLC(self):
        self.set_up()
        self.gh.handle_data(b'\x03')
        self.assertTrue(self.gh._interrupt)

    def test_handle_data_Packets(self):
        self.set_up()
        self.gh.handle_data(b'+++$qfThreadInfo#bb$qsThreadInfo#c8-')
        self.gh._comsocket.sendall.assert_has_calls([call(b'+'), call(rsp('m01')),  call(b'+'), call(rsp('l')),  call(rsp('l'))])

    def test_handle_data_wrong_checksum(self):
        self.set_up()
        self.gh.handle_data(b'$qfThreadInfo#cc')
        self.gh._comsocket.sendall.assert_called_with(b"-")

    @patch('pyavrocd.handler.GdbHandler._set_binary_memory_handler_finalize',Mock())
    def test_handle_data_None1(self):
        self.set_up()
        self.gh.mem.lazy_loading = False
        self.gh.handle_data(None)
        self.assertEqual(self.gh._set_binary_memory_handler_finalize.call_count, 1) #pylint: disable=no-member

    @patch('pyavrocd.handler.GdbHandler._set_binary_memory_handler_finalize',Mock())
    def test_handle_data_None2(self):
        self.set_up()
        self.gh.mem.lazy_loading = True
        self.gh.handle_data(None)
        self.assertEqual(self.gh._set_binary_memory_handler_finalize.call_count, 2) #pylint: disable=no-member

    @patch('pyavrocd.handler.GdbHandler.dispatch',Mock())
    def test_handle_data_single_cmd(self):
        self.set_up()
        self.gh.handle_data(rsp('Z0,2,111,2'))
        self.gh.dispatch.assert_called_with('Z',b'0,2,111,2') #pylint: disable=no-member
