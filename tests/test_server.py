"""
The test suit for server module
"""
#pylint: disable=protected-access,missing-function-docstring,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
import logging
from unittest.mock import  Mock, call, patch, create_autospec
from unittest import TestCase
from types import SimpleNamespace

from pyavrocd.xavrdebugger import EdbgBackend
from pyavrocd.server import RspServer
from pyavrocd.handler import GdbHandler
from pyavrocd.errors import  EndOfSession, TerminationRequest

class TestRspServer(TestCase):

    def setUp(self):
        self.rs = None

    def set_up(self):
        mock_dbg = create_autospec(EdbgBackend)
        mock_dbg.device = 'atmega328p'
        args = SimpleNamespace()
        args.port = 2000
        args.once = False
        self.rs = RspServer(mock_dbg, "atemga328p", args, "Tool")
        self.rs.logger = Mock()
        self.rs.logger.info = Mock()
        self.rs.logger.getEffectiveLevel.return_value = logging.INFO

    def test_signal_server(self):
        self.set_up()
        with self.assertRaises(TerminationRequest):
            self.rs._signal_server(None, None)
        self.assertTrue(self.rs._terminate)
        self.rs.logger.info.assert_called_with("System requested termination using SIGTERM signal")

    def test_interrupt_server(self):
        self.set_up()
        with self.assertRaises(KeyboardInterrupt):
            self.rs._interrupt_server(None, None)

    def test_signal_server_during_cleanup(self):
        self.set_up()
        self.rs._terminate = True
        self.rs._signal_server(None, None) # must not raise
        self.rs.logger.info.assert_called_with("System requested termination using SIGTERM signal")

    def test_signal_server_during_cleanup_after_detach(self):
        # the session ended by detach, not by SIGTERM: _terminate is not set
        self.set_up()
        self.rs._cleaning_up = True
        self.rs._signal_server(None, None) # must not raise
        self.assertFalse(self.rs._terminate)

    def test_interrupt_server_during_cleanup(self):
        self.set_up()
        self.rs._cleaning_up = True
        self.rs._interrupt_server(None, None) # must not raise
        self.rs.logger.info.assert_called_with("Ctrl-C ignored: cleaning up")

    @patch('pyavrocd.server.time.sleep',Mock())
    @patch('pyavrocd.server.signal.signal',Mock())
    @patch('pyavrocd.server.socket.socket')
    @patch('pyavrocd.server.select.select')
    @patch('pyavrocd.server.GdbHandler')
    def test_serve_SIGTERM_during_cleanup_after_detach(self, mock_handler, mock_select, mock_socket):
        # what an IDE does: detach, then SIGTERM while the server is still cleaning up
        self.set_up()
        mock_socket.return_value.accept.return_value = (Mock(close=Mock()), '111.222.333.444')
        mock_socket.return_value.accept.return_value[0].recv.side_effect = EndOfSession("")
        mock_handler.return_value = Mock(mon=None, spec=GdbHandler)
        mock_select.side_effect = [(1,0,0)]
        cleanup_done = []
        def stop_debugging(**_kwargs):
            self.rs._signal_server(None, None) # SIGTERM arrives in the middle of the cleanup
            self.rs._interrupt_server(None, None) # and a Ctrl-C, for good measure
            cleanup_done.append(True)
        self.rs.avrdebugger.stop_debugging.side_effect = stop_debugging
        self.assertEqual(self.rs.serve(), 0)
        self.assertEqual(cleanup_done, [True])
        self.rs.gdb_socket.close.assert_called_once() #pylint: disable=no-member
        self.rs.connection.close.assert_called_once() #pylint: disable=no-member

    @patch('pyavrocd.server.signal.signal',Mock())
    @patch('pyavrocd.server.time.sleep',Mock())
    @patch('pyavrocd.server.socket.socket')
    @patch('pyavrocd.server.select.select')
    @patch('pyavrocd.server.GdbHandler')
    def test_serve_SIGTERM(self, mock_handler, mock_select, mock_socket):
        self.set_up()
        mock_socket.return_value.accept.return_value = (Mock(close=Mock()), '111.222.333.444')
        mock_socket.return_value.accept.return_value[0].recv.side_effect = TerminationRequest()
        mock_handler.return_value = Mock(mon=None, spec=GdbHandler)
        mock_select.side_effect = [(1,0,0)]
        self.assertEqual(self.rs.serve(), 0)
        self.rs.avrdebugger.stop_debugging.assert_called_once()
        self.rs.gdb_socket.close.assert_called_once() #pylint: disable=no-member
        self.rs.connection.close.assert_called_once() #pylint: disable=no-member

    @patch('pyavrocd.server.time.sleep',Mock())
    @patch('pyavrocd.server.signal.signal',Mock())
    @patch('pyavrocd.server.socket.socket')
    @patch('pyavrocd.server.select.select')
    @patch('pyavrocd.server.GdbHandler')
    def test_serve(self, mock_handler, mock_select, mock_socket):
        self.set_up()
        mock_socket.return_value.accept.return_value = (Mock(), '111.222.333.444')
        mock_socket.return_value.accept.return_value[0].recv.side_effect = [b'123', b'123', b'']
        mock_handler.return_value = Mock(spec=GdbHandler, mon=None, extended_remote_mode=False)
        mock_select.side_effect = [(1,0,0), (1,0,0), (1,0,0)]
        self.assertEqual(self.rs.serve(), 0)
        self.rs.logger.info.assert_has_calls([call('Listening on port %s for gdb connection', 2000),
                                              call('Connection from %s', '111.222.333.444'),
                                              call('Connection closed by GDB'),
                                              call('Leaving GDB server')])
        self.assertEqual(self.rs.logger.info.call_count, 6)

    @patch('pyavrocd.server.time.sleep',Mock())
    @patch('pyavrocd.server.signal.signal',Mock())
    @patch('pyavrocd.server.socket.socket')
    @patch('pyavrocd.server.select.select')
    @patch('pyavrocd.server.GdbHandler')
    def test_serve_extended_remote_mode(self, mock_handler, mock_select, mock_socket):
        self.set_up()
        mock_socket.return_value.accept.return_value = (Mock(), '111.222.333.444')
        mock_socket.return_value.accept.return_value[0].recv.side_effect = [b'123', b'123', b'',KeyboardInterrupt]
        mock_handler.return_value = Mock(spec=GdbHandler, mon=None, extended_remote_mode=True, _once=False)
        mock_select.side_effect = [(1,0,0), (1,0,0), (1,0,0), (1,0,0)]
        self.assertEqual(self.rs.serve(), 1)
        self.rs.logger.info.assert_has_calls([call('Listening on port %s for gdb connection', 2000),
                                              call('Connection from %s', '111.222.333.444'),
                                              call('Connection closed by GDB'),
                                              call('Listening on port %s for gdb connection', 2000),
                                              call('Connection from %s', '111.222.333.444'),
                                              call('Terminated by Ctrl-C'),
                                              call('Leaving GDB server')])
        self.assertEqual(self.rs.logger.info.call_count, 10)


    @patch('pyavrocd.server.time.sleep',Mock())
    @patch('pyavrocd.server.signal.signal',Mock())
    @patch('pyavrocd.server.socket.socket')
    @patch('pyavrocd.server.select.select')
    @patch('pyavrocd.server.GdbHandler')
    def test_serve_EOS(self, mock_handler, mock_select, mock_socket):
        self.set_up()
        mock_socket.return_value.accept.return_value = (Mock(), '111.222.333.444')
        mock_socket.return_value.accept.return_value[0].recv.side_effect = EndOfSession("")
        mock_handler.return_value = Mock(mon=None, spec=GdbHandler)
        mock_select.side_effect = [(1,0,0), (1,0,0), (1,0,0)]
        self.assertEqual(self.rs.serve(), 0)
        self.rs.logger.info.assert_has_calls([call('Listening on port %s for gdb connection', 2000),
                                              call('Connection from %s', '111.222.333.444'),
                                              call('End of session'),
                                              call('Leaving GDB server')])
        self.assertEqual(self.rs.logger.info.call_count,7)

    @patch('pyavrocd.server.time.sleep',Mock())
    @patch('pyavrocd.server.signal.signal',Mock())
    @patch('pyavrocd.server.socket.socket')
    @patch('pyavrocd.server.select.select')
    @patch('pyavrocd.server.GdbHandler')
    def test_serve_probe_gone(self, mock_handler, mock_select, mock_socket):
        # an error outside the packet handlers, e.g. the probe unplugged while events are polled
        self.set_up()
        mock_socket.return_value.accept.return_value = (Mock(), '111.222.333.444')
        mock_handler.return_value = Mock(mon=None, spec=GdbHandler)
        mock_handler.return_value.poll_events.side_effect = OSError(19, "No such device")
        mock_select.side_effect = [(0,0,0), (0,0,0)]
        self.assertEqual(self.rs.serve(), 1)
        self.rs.logger.critical.assert_called_once()
        self.assertEqual(self.rs.logger.critical.call_args[0][0], "Forced exit: %s")
        self.assertIn("No such device", str(self.rs.logger.critical.call_args[0][1]))


    @patch('pyavrocd.server.signal.signal',Mock())
    @patch('pyavrocd.server.time.sleep',Mock())
    @patch('builtins.print')
    @patch('pyavrocd.server.socket.socket')
    @patch('pyavrocd.server.select.select')
    @patch('pyavrocd.server.GdbHandler')
    def test_serve_KI(self, mock_handler, mock_select, mock_socket, mock_print):
        self.set_up()
        mock_socket.return_value.accept.return_value = (Mock(close=Mock()), '111.222.333.444')
        mock_socket.return_value.accept.return_value[0].recv.side_effect = KeyboardInterrupt("")
        mock_handler.return_value = Mock(mon=None, spec=GdbHandler)
        mock_select.side_effect = [(1,0,0), (1,0,0), (1,0,0)]
        self.rs.logger.getEffectiveLevel.return_value = logging.CRITICAL
        self.assertEqual(self.rs.serve(), 1)
        mock_print.assert_has_calls([call('Listening on port 2000 for gdb connection')])
        self.rs.avrdebugger.stop_debugging.assert_called_once()
        self.rs.gdb_socket.close.assert_called_once() #pylint: disable=no-member
        self.rs.connection.close.assert_called_once() #pylint: disable=no-member
