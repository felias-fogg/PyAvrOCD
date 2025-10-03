"""
The test suit for server module
"""
#pylint: disable=protected-access,missing-function-docstring,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
import logging
from logging import getLogger
from unittest.mock import MagicMock, Mock, call, patch, create_autospec
from unittest import TestCase
import sys
from types import SimpleNamespace

from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.server import RspServer
from pyavrocd.handler import GdbHandler, RECEIVE_BUFFER
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

