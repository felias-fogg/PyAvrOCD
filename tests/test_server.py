"""
The test suit for server module
"""
#pylint: disable=protected-access,missing-function-docstring,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
import logging
from unittest.mock import  Mock, call, patch, create_autospec
from unittest import TestCase
from types import SimpleNamespace

from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.server import RspServer
from pyavrocd.handler import GdbHandler
from pyavrocd.errors import  EndOfSession

class TestRspServer(TestCase):

    def setUp(self):
        mock_dbg = create_autospec(XAvrDebugger)
        mock_dbg.device = 'atmega328p'
        args = SimpleNamespace()
        args.port = 2000
        self.rs = RspServer(mock_dbg, "atemga328p", args)
        self.rs.logger = Mock()
        self.rs.logger.info = Mock()
        self.rs.logger.getEffectiveLevel.return_value = logging.INFO

    def test_signal_server(self):
        self.rs._signal_server(None, None)
        self.assertTrue(self.rs._terminate)
        self.rs.logger.info.assert_called_with("System requested termination using SIGTERM signal")

    @patch('pyavrocd.server.signal.signal',Mock())
    @patch('pyavrocd.server.socket.socket')
    @patch('pyavrocd.server.select.select')
    @patch('pyavrocd.server.GdbHandler')
    def test_serve(self, mock_handler, mock_select, mock_socket):
        mock_socket.return_value.accept.return_value = (Mock(), '111.222.333.444')
        mock_socket.return_value.accept.return_value[0].recv.side_effect = [b'123', b'123', b'']
        mock_handler.return_value = create_autospec(GdbHandler)
        mock_select.side_effect = [(1,0,0), (1,0,0), (1,0,0)]
        self.assertEqual(self.rs.serve(), 0)
        self.rs.logger.info.assert_has_calls([call('Listening on port %s for gdb connection', 2000),
                                              call('Connection from %s', '111.222.333.444'),
                                              call('Connection closed by GDB'),
                                              call('Leaving GDB server')])
        self.assertEqual(self.rs.logger.info.call_count,4)


    @patch('pyavrocd.server.signal.signal',Mock())
    @patch('pyavrocd.server.socket.socket')
    @patch('pyavrocd.server.select.select')
    @patch('pyavrocd.server.GdbHandler')
    def test_serve_EOS(self, mock_handler, mock_select, mock_socket):
        mock_socket.return_value.accept.return_value = (Mock(), '111.222.333.444')
        mock_socket.return_value.accept.return_value[0].recv.side_effect = EndOfSession("")
        mock_handler.return_value = create_autospec(GdbHandler)
        mock_select.side_effect = [(1,0,0), (1,0,0), (1,0,0)]
        self.assertEqual(self.rs.serve(), 0)
        self.rs.logger.info.assert_has_calls([call('Listening on port %s for gdb connection', 2000),
                                              call('Connection from %s', '111.222.333.444'),
                                              call('End of session'),
                                              call('Leaving GDB server')])
        self.assertEqual(self.rs.logger.info.call_count,4)


    @patch('pyavrocd.server.signal.signal',Mock())
    @patch('pyavrocd.server.time.sleep',Mock())
    @patch('builtins.print')
    @patch('pyavrocd.server.socket.socket')
    @patch('pyavrocd.server.select.select')
    @patch('pyavrocd.server.GdbHandler')
    def test_serve_KI(self, mock_handler, mock_select, mock_socket, mock_print):
        mock_socket.return_value.accept.return_value = (Mock(), '111.222.333.444')
        mock_socket.return_value.accept.return_value[0].recv.side_effect = KeyboardInterrupt("")
        mock_handler.return_value = create_autospec(GdbHandler)
        mock_select.side_effect = [(1,0,0), (1,0,0), (1,0,0)]
        self.rs.logger.getEffectiveLevel.return_value = logging.CRITICAL
        mock_stop = self.rs.avrdebugger.stop_debugging
        self.assertEqual(self.rs.serve(), 1)
        mock_print.assert_has_calls([call('Listening on port 2000 for gdb connection')])
        self.assertEqual(self.rs.avrdebugger, None)
        mock_stop.assert_called_once()
