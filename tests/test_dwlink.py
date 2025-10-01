"""
The test suite for dwlink
"""
import sys
import os
import time

import logging
from unittest.mock import MagicMock, patch, call, create_autospec
from unittest import TestCase

from pyavrocd.dwlink import SerialToNet, DetachException, discover, main

logging.basicConfig(level=logging.CRITICAL)

class TestSerialToNet(TestCase):

    def setUp(self):
        self.sn = SerialToNet(False)
        self.sn.socket = MagicMock()

    def test_convert_gdb_message(self):
        self.sn.last = b'$O48656C6C6F#XX'
        self.assertEqual(self.sn.convert_gdb_message(), 'Hello')

    @patch('pyavrocd.dwlink.sys.stderr.write', MagicMock())
    def test_data_received_nolog(self):
        self.sn.data_received(b'$O48656C6C6F#XX')
        self.sn.socket.sendall.assert_called_once_with(b'$O48656C6C6F#XX')
        self.assertEqual(self.sn.last, b"")
        sys.stderr.write.assert_not_called()

    @patch('pyavrocd.dwlink.sys.stderr.write', MagicMock())
    def test_data_received_log(self):
        self.sn.logging = True
        self.sn.data_received(b'$O48656C6C6F#XX')
        self.sn.socket.sendall.assert_called_once_with(b'$O48656C6C6F#XX')
        self.assertEqual(self.sn.last, b"")
        sys.stderr.write.assert_has_calls([call("[DEBUG] recv: b'$O48656C6C6F#XX'\n"), call("[DEBUG] dw-link: Hello")])
        self.assertEqual(sys.stderr.write.call_count, 2)

    @patch('pyavrocd.dwlink.sys.stderr.write', MagicMock())
    def test_data_received_warning(self):
        self.sn.logging = False
        self.sn.data_received(b'$O2A2A2A204572726F72#XX')
        self.sn.socket.sendall.assert_called_once_with(b'$O2A2A2A204572726F72#XX')
        self.assertEqual(self.sn.last, b"")
        sys.stderr.write.assert_has_calls([call("[WARNING] *** Error")])
        self.assertEqual(sys.stderr.write.call_count, 1)

    @patch('pyavrocd.dwlink.sys.stderr.write', MagicMock())
    @patch('pyavrocd.dwlink.os._exit', MagicMock())
    @patch('pyavrocd.dwlink.time.sleep', MagicMock())
    def test_connection_lost_exception(self):
        self.sn.connection_lost("LOST")
        sys.stderr.write.assert_has_calls([call("[ERROR] 'LOST'\n\r"),
                                               call("[INFO] Serial connection lost, will exit\n\r")])
        self.assertEqual(sys.stderr.write.call_count, 2)
        time.sleep.assert_called_once()

    @patch('pyavrocd.dwlink.sys.stderr.write', MagicMock())
    @patch('pyavrocd.dwlink.os._exit', MagicMock())
    @patch('pyavrocd.dwlink.time.sleep', MagicMock())
    def test_connection_lost_closed(self):
        self.sn.connection_lost(None)
        sys.stderr.write.assert_has_calls([call("[INFO] Serial connection closed\n\r")])
        self.assertEqual(sys.stderr.write.call_count, 1)
        os._exit.assert_called_once()
