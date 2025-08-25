"""
The test suit for the GdbHandler class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
import logging
from unittest.mock import Mock, MagicMock, patch, call, create_autospec
from unittest import TestCase
import socket
from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.handler import GdbHandler, SIGINT, SIGHUP
from pyavrocd.errors import EndOfSession
from pyavrocd.memory import Memory
from pyavrocd.monitor import MonitorCommand
from pyavrocd.breakexec import BreakAndExec

logging.basicConfig(level=logging.CRITICAL)

# generate an RSP packet from a string
def rsp(packet):
    checksum = sum(packet.encode("ascii")) % 256
    return ("$%s#%02x" % (packet, checksum)).encode("ascii")

class TestGdbHandler(TestCase):

    def setUp(self):
        mock_socket = create_autospec(socket.socket, spec_set=True, instance=True)
        mock_dbg = create_autospec(XAvrDebugger, spec_set=False, instance=True)
        mock_dbg.memory_info = MagicMock()
        mock_dbg.device_info = MagicMock()
        mock_dbg.transport = MagicMock()
        mock_dbg.edbg_protocol = MagicMock()
        mock_dbg.device = Mock()
        mock_dbg.device.avr = Mock()
        mock_dbg.iface = 'debugwire'
        mock_dbg.memory_info.memory_info_by_name('flash')['size'].__gt__ = lambda self, compare: False
        # setting up the GbdHandler instance we want to test
        self.gh = GdbHandler(mock_socket, mock_dbg, "atmega328p")
        self.gh.mon = create_autospec(MonitorCommand, specSet=True, instance=True)
        self.gh.mem = create_autospec(Memory, specSet=True, instance=True)
        self.gh.mem.programming_mode = False
        self.gh.bp = create_autospec(BreakAndExec, specSet=True, instance=True)

    def test_rsp_packet_construction(self):
        self.assertEqual(b'$#00', rsp(''))
        self.assertEqual(b'$abc#26', rsp('abc'))

    def test_unknownPacket(self):
        self.gh.dispatch('_', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp(""))

    def test_extended_remote_handler(self):
        self.assertFalse(self.gh._extended_remote_mode)
        self.gh.dispatch('!', b'')
        self.assertTrue(self.gh._extended_remote_mode)
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_stop_reason_handler_none(self):
        self.gh.last_sigval = None
        self.gh.dispatch('?', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("S00"))

    def test_stop_reason_handler_SIGINT(self):
        self.gh.last_sigval = SIGINT
        self.gh.dispatch('?', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("S02"))

    def test_continue_handler_impossible(self):
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.mem.is_flash_empty.return_value = True
        self.gh.mon.is_noload.return_value = False
        self.gh.dbg.status_register_read.return_value = [0x55]
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.program_counter_read.return_value = 0x00003421
        self.gh.dispatch('c',b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("S01"))
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('c',b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("S04"))

    def test_continue_handler_with_start(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.is_flash_empty.return_value = False
        self.gh.bp.resume_execution.return_value = None
        self.gh.dispatch('c',b'2244')
        self.gh.bp.resume_execution.assert_called_with(0x2244)
        self.gh._comsocket.sendall.assert_not_called()

    def test_continue_handler_without_start(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.is_flash_empty.return_value = False
        self.gh.bp.resume_execution.return_value = None
        self.gh.dbg.program_counter_read.return_value = 1
        self.gh.dispatch('c',b'')
        self.gh.bp.resume_execution.assert_called_with(None)
        self.gh._comsocket.sendall.assert_not_called()

    def test_continue_with_signal_handler(self):
        self.gh._continue_handler = Mock()
        self.gh.dispatch('C',b'09;2244')
        self.gh.dispatch('C',b'09')
        self.gh._continue_handler.assert_has_calls([call('2244'), call('')])

    def test_continue_with_signal_handler_without_start(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.is_flash_empty.return_value = False
        self.gh.bp.resume_execution.return_value = None
        self.gh.dispatch('C',b'09')
        self.gh.bp.resume_execution.assert_called_with(None)
        self.gh._comsocket.sendall.assert_not_called()

    def test_detach_handler(self):
        with self.assertRaises(EndOfSession):
            self.gh.dispatch('D',b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_get_register_handler_impossible(self):
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('g',b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2000341200000000"))

    def test_get_register_handler(self):
        self.gh.dbg.program_counter_read.return_value = 0x00003421
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.status_register_read.return_value = [0x55]
        self.gh.dbg.register_file_read.return_value = bytearray(list(range(32)))
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('g',b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f55341242680000"))

    def test_setRegisterHandle_impossible(self):
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('G',b'000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f66341242680000')
        self.gh.dbg.program_counter_write.assert_not_called()
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_setRegisterHandle(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('G',b'000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f66341242680000')
        self.gh.dbg.register_file_write.assert_called_with(bytearray(list(range(32))))
        self.gh.dbg.status_register_write.assert_called_with(bytearray([0x66]))
        self.gh.dbg.stack_pointer_write.assert_called_with(bytearray(bytearray([0x34, 0x12])))
        self.gh.dbg.program_counter_write.assert_called_with(0x00003421)
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_set_thread_handler(self):
        self.gh.dispatch('H',b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_get_memory_handler_impossible(self):
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('m',b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("E01"))

    def test_get_memory_handler_chunk(self):
        # read chunk from memory
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.readmem.return_value = b'\x01\x02\x03\x04'
        self.gh.dispatch('m',b'800101,4')
        self.gh.mem.readmem.assert_called_with("800101", "4")
        self.gh._comsocket.sendall.assert_called_with(rsp("01020304"))

    def test_get_memory_handler_empty_request(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.readmem.return_value = None
        self.gh.dispatch('m',b'800101,0')
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))
        self.gh.mem.readmem.assert_not_called()

    def test_get_memory_handler_empty_return(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.readmem.return_value = b''
        self.gh.dispatch('m',b'800101,4')
        self.gh.mem.readmem.assert_called_with("800101", "4")
        self.gh._comsocket.sendall.assert_called_with(rsp("E14"))

    def test_set_memory_handler_impossible(self):
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('M', b'800100,0:')
        self.gh._comsocket.sendall.assert_called_with(rsp('E01'))

    def test_set_memory_handler_byte(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.writemem.return_value = "OK"
        self.gh.dispatch('M', b'800100,1:63')
        self.gh.mem.writemem.assert_called_with("800100", bytes([0x63]))
        self.gh._comsocket.sendall.assert_called_with(rsp('OK'))

    def test_get_one_register_handler_impossible(self):
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('p', b'22')
        self.gh._comsocket.sendall.assert_called_with(rsp("E01"))

    def test_get_one_register_handler_pc(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dbg.program_counter_read.return_value = 0x123
        self.gh.dispatch('p', b'22')
        self.gh._comsocket.sendall.assert_called_with(rsp("46020000"))

    def test_get_one_register_handler_sp(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x23,0x01])
        self.gh.dispatch('p', b'21')
        self.gh._comsocket.sendall.assert_called_with(rsp("2301"))

    def test_get_one_register_handler_sreg(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dbg.status_register_read.return_value = bytearray([0x01])
        self.gh.dispatch('p', b'20')
        self.gh._comsocket.sendall.assert_called_with(rsp("01"))

    def test_get_one_register_handler_reg(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dbg.sram_read.return_value = bytearray([0x23])
        self.gh.dispatch('p', b'07')
        self.gh._comsocket.sendall.assert_called_with(rsp("23"))

    def test_set_one_register_handler_impossible(self):
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('P', b'22=04200000')
        self.gh._comsocket.sendall.assert_called_with(rsp("E01"))

    def test_set_one_register_handler_pc(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('P', b'22=04200000')
        self.gh.dbg.program_counter_write.assert_called_with(0x2004>>1)
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_set_one_register_handler_sp(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('P', b'21=0420')
        self.gh.dbg.stack_pointer_write.assert_called_with(bytearray([0x04, 0x20]))
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_set_one_register_handler_sreg(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('P', b'20=04')
        self.gh.dbg.status_register_write.assert_called_with(bytearray([0x04]))
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_set_one_register_handler_reg(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('P', b'10=ee')
        self.gh.dbg.sram_write.assert_called_with(0x10, bytearray([0xee]))
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_attached_handler(self):
        self.gh.dispatch('qAttached', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("1"))

    def test_offsets_handler(self):
        self.gh.dispatch('qOffsets', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("Text=000;Data=000;Bss=000"))

    def test_monitorCommand(self):
        self.gh.mon.dispatch.return_value = ('reset', 'Bla')
        self.gh.dispatch('qRcmd', b',7265736574')
        self.assertTrue(self.gh.dbg.reset.called)
        self.gh._comsocket.sendall.assert_called_with(rsp("426C610A"))

    def test_supported_handler(self):
        self.gh.dbg.start_debugging.return_value = True
        self.gh.dispatch('qSupported', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("PacketSize={0:X};qXfer:memory-map:read+".format(self.gh.packet_size)))
        self.gh.mon.set_debug_mode_active.assert_called_once()

    def test_first_thread_info_handler(self):
        self.gh.dispatch('qfThreadInfo', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("m01"))

    def test_subsequent_thread_info_handler(self):
        self.gh.dispatch('qsThreadInfo', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("l"))

    def test_memory_map_handler(self):
        self.gh.mon.is_noxml.return_value = False
        self.gh.mem.memory_map.return_value="map"
        self.gh.dispatch('qXfer', b':memory-map:read::0,1000')
        self.gh.mem.memory_map.assert_called_once()

    def test_step_handler_impossible(self):
        self.gh.mon.is_debugger_active.return_value=False
        self.gh.mem.is_flash_empty.return_value = True
        self.gh.mon.is_noload.return_value = False
        self.gh.dispatch('s', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("S01"))
        self.gh.mon.is_debugger_active.return_value=True
        self.gh.dispatch('s', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("S04"))

    def test_step_handler_with_start(self):
        self.gh.mon.is_debugger_active.return_value=True
        self.gh.mem.is_flash_empty.return_value = False
        self.gh.mon.is_noload.return_value = False
        self.gh.dbg.program_counter_read.return_value = 0x00000102
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.status_register_read.return_value = [0x55]
        self.gh.bp.single_step.return_value = 5
        self.gh.dispatch('s', b'00000202')
        self.gh.bp.single_step.assert_called_with(0x202)
        self.gh._comsocket.sendall.assert_called_with(rsp("T0520:55;21:3412;22:04020000;thread:1;"))

    def test_step_handler_without_start(self):
        self.gh.mon.is_debugger_active.return_value=True
        self.gh.mem.is_flash_empty.return_value = False
        self.gh.mon.is_noload.return_value = False
        self.gh.dbg.program_counter_read.return_value = 0x00000101
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.status_register_read.return_value = [0x55]
        self.gh.bp.single_step.return_value = 5
        self.gh.dispatch('s', b'')
        self.gh.bp.single_step.assert_called_with(None)
        self.gh._comsocket.sendall.assert_called_with(rsp("T0520:55;21:3412;22:02020000;thread:1;"))

    def test_step_with_signal_handler(self):
        self.gh._step_handler = Mock()
        self.gh.dispatch('S', b'09;4545')
        self.gh.dispatch('S', b'09')
        self.gh._step_handler.assert_has_calls([call('4545'), call('')])

    def test_thread_alive_handler(self):
        self.gh.dispatch('T', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_flashDoneHandler(self):
        self.gh.dispatch('vFlashDone', b'')
        self.gh.mem.flash_pages.assert_called_once()
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_flashEraseHandler_impossible(self):
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('vFlashErase', b':100,10')
        self.gh._comsocket.sendall.assert_called_with(rsp("E01"))

    def test_flashEraseHandler_fresh(self):
        self.gh._vflashdone = True
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('vFlashErase', b':100,10')
        self.assertFalse(self.gh._vflashdone)
        self.gh.dispatch('vFlashErase', b':200,10')
        self.gh.mem.init_flash.assert_called_once()
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_flash_writeHandler_success(self):
        self.gh.dispatch('vFlashWrite', b':0100:ABC')
        self.gh.mem.store_to_cache.assert_called_with(0x100,[ord('A'), ord('B'), ord('C')])
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_escape(self):
        seq = [ 0x7d, 0xFF, 0x2A, 0x00, 0x23, 0x24 ]
        self.assertEqual(self.gh.escape(seq),bytes([0x7d, 0x5d, 0xFF, 0x7D, 0x0A, 0x00, 0x7D, 0x03, 0x7D, 0x04]))

    def test_unescape(self):
        seq = [0x7d, 0x5d, 0xFF, 0x7D, 0x0A, 0x00, 0x7D, 0x03, 0x7D, 0x04]
        self.assertEqual(self.gh.unescape(seq),[ 0x7d, 0xFF, 0x2A, 0x00, 0x23, 0x24 ])

    def test_kill_handler_not_exteded_remote(self):
        self.gh._extended_remote_mode = False
        with self.assertRaises(EndOfSession):
            self.gh.dispatch('vKill', b'')
        self.gh.dbg.reset.assert_called_once()

    def test_kill_handler_exteded_remote(self):
        self.gh._extended_remote_mode = True
        self.gh.dispatch('vKill', b'')
        self.gh.dbg.reset.assert_called_once()
        self.gh._comsocket.sendall.assert_called_with(rsp("OK"))

    def test_run_handler_impossible(self):
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('vRun', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("S01"))

    def test_run_handler(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dbg.program_counter_read.return_value = 0x00000101
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.status_register_read.return_value = [0x77]
        self.gh.dispatch('vRun', b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("T0520:77;21:3412;22:02020000;thread:1;"))
        self.gh.dbg.reset.assert_called_once()

    def test_set_binary_memory_handler_impossible(self):
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('m',b'')
        self.gh._comsocket.sendall.assert_called_with(rsp("E01"))

    def test_set_binary_memory_handler_byte(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.mem.writemem.return_value = "OK"
        self.gh.dispatch('X', b'800100,1:}]')
        self.gh.mem.writemem.assert_called_with("800100", bytearray([0x7D]))
        self.gh._comsocket.sendall.assert_called_with(rsp('OK'))

    def test_remove_breakpoint_handler_impossible(self):
        # even when debugger is not active, success is returned
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('z',b'0,111,2')
        self.gh._comsocket.sendall.assert_called_with(rsp('OK'))

    def test_remove_breakpoint_handler_wrong_type(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('z',b'2,111,2')
        self.gh._comsocket.sendall.assert_called_with(rsp(''))

    def test_remove_breakpoint_handler(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('z',b'0,222,2')
        # note: for  breakpoints, it is always the byte address!
        self.gh.bp.remove_breakpoint.assert_called_with(0x222)
        self.gh._comsocket.sendall.assert_called_with(rsp('OK'))

    def test_add_breakpoint_handler_impossible(self):
        # even when debugger is not active, success is returned
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.dispatch('Z',b'0,111,2')
        self.gh._comsocket.sendall.assert_called_with(rsp('OK'))

    def test_add_breakpoint_handler_wrong_type(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('Z',b'2,111,2')
        self.gh._comsocket.sendall.assert_called_with(rsp(''))

    def test_add_breakpoint_handler_new(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dispatch('Z',b'0,222,2')
        # note: for  breakpoints, it is always the byte address!
        self.gh.bp.insert_breakpoint.assert_called_with(0x222)
        self.gh._comsocket.sendall.assert_called_with(rsp('OK'))

    def test_poll_events_impossible(self):
        self.gh.mon.is_debugger_active.return_value = False
        self.gh.poll_events()
        self.gh.dbg.poll_event.assert_not_called()

    def test_poll_events_positive(self):
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dbg.poll_event.return_value = 0x101
        self.gh.mon.is_debugger_active.return_value = True
        self.gh.dbg.program_counter_read.return_value = 0x00000101
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.status_register_read.return_value = [0x88]
        self.gh.poll_events()
        self.gh.dbg.poll_event.assert_called_once()
        self.gh._comsocket.sendall.assert_called_with(rsp("T0520:88;21:3412;22:02020000;thread:1;"))

    @patch('pyavrocd.main.select.select', Mock(return_value=[None, None, None]))
    def test_poll_gdb_input_false(self):
        self.assertFalse(self.gh.poll_gdb_input())

    @patch('pyavrocd.main.select.select', Mock(return_value=[[1], None, None]))
    def test_poll_gdb_input_true(self):
        self.assertTrue(self.gh.poll_gdb_input())

    def test_send_packet(self):
        self.gh.send_packet("abc")
        self.gh._comsocket.sendall.assert_called_with(rsp("abc"))

    def test_send_reply_packet(self):
        self.gh.send_reply_packet("Hello World")
        self.gh._comsocket.sendall.assert_called_with(rsp("48656C6C6F20576F726C640A"))

    def test_send_debug_message(self):
        self.gh.send_debug_message("Hello World")
        self.gh._comsocket.sendall.assert_called_with(rsp("O48656C6C6F20576F726C640A"))

    def test_send_signal_none(self):
        self.gh.send_signal(None)
        self.gh._comsocket.sendall.assert_not_called()
        self.assertEqual(self.gh.last_sigval, None)

    def test_send_signal_SIGINT(self):
        self.gh.dbg.program_counter_read.return_value = 0x00000404
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x12])
        self.gh.dbg.status_register_read.return_value = [0x99]
        self.gh.send_signal(SIGINT)
        self.gh._comsocket.sendall.assert_called_with(rsp("T0220:99;21:3412;22:08080000;thread:1;"))

    def test_send_signal_SIGHUP(self):
        self.gh.send_signal(SIGHUP)
        self.gh._comsocket.sendall.assert_called_with(rsp("S01"))

    def test_handle_data_ACK_NACK(self):
        self.gh._lastmessage = 'bla'
        self.gh.handle_data(b'++---+---')
        self.gh._comsocket.sendall.assert_called_with(rsp("bla"))

    def test_handle_data_NACK_ACK_ignore_NAK(self):
        self.gh._lastmessage = 'bla'
        self.gh.handle_data(b'--------+ ---')
        self.gh._comsocket.sendall.assert_called_with(rsp(""))

    def test_handle_data_CTRLC(self):
        self.gh.dbg.program_counter_read.return_value = 0x00000404
        self.gh.dbg.stack_pointer_read.return_value = bytearray([0x34, 0x11])
        self.gh.dbg.status_register_read.return_value = [0x11]
        self.gh.handle_data(b'\x03')
        self.gh._comsocket.sendall.assert_called_with(rsp("T0220:11;21:3411;22:08080000;thread:1;"))

    def test_handle_data_Packets(self):
        self.gh.handle_data(b'+++$qfThreadInfo#bb$qsThreadInfo#c8-')
        self.gh._comsocket.sendall.assert_has_calls([call(b'+'), call(rsp('m01')),  call(b'+'), call(rsp('l')),  call(rsp('l'))])

    def test_handle_data_wrong_checksum(self):
        self.gh.handle_data(b'$qfThreadInfo#cc')
        self.gh._comsocket.sendall.assert_called_with(b"-")
