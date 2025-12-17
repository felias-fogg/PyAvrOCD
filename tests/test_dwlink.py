"""
The test suite for dwlink
"""
#pylint: disable=protected-access,missing-function-docstring,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch, call
from unittest import TestCase

from pyavrocd.dwlink import SerialToNet, discover, main

class TestSerialToNet(TestCase):

    def setUp(self):
        self.sn = None

    def set_up(self):
        self.sn = SerialToNet(False)
        self.sn.socket = MagicMock()
        self.sn.socket.sendall = MagicMock()

    def test_convert_gdb_message(self):
        self.set_up()
        self.sn.last = b'$O48656C6C6F#XX'
        self.assertEqual(self.sn.convert_gdb_message(), 'Hello')

    @patch('pyavrocd.dwlink.sys.stdout.write')
    def test_data_received_nolog(self, mock_write):
        self.set_up()
        self.sn.data_received(b'$O48656C6C6F#XX')
        self.sn.socket.sendall.assert_called_once_with(b'$O48656C6C6F#XX')
        self.assertEqual(self.sn.last, b"")
        mock_write.write.assert_not_called()

    @patch('pyavrocd.dwlink.sys.stdout.write')
    def test_data_received_log(self, mock_write):
        self.set_up()
        self.sn.logging = True
        self.sn.data_received(b'$O48656C6C6F#XX')
        self.sn.socket.sendall.assert_called_once_with(b'$O48656C6C6F#XX')
        self.assertEqual(self.sn.last, b"")
        mock_write.assert_has_calls([call("[DEBUG] recv: b'$O48656C6C6F#XX'\n"), call("[DEBUG] dw-link: Hello")])
        self.assertEqual(mock_write.call_count, 2)

    @patch('pyavrocd.dwlink.sys.stdout.write')
    def test_data_received_warning(self, mock_write):
        self.set_up()
        self.sn.logging = False
        self.sn.data_received(b'$O2A2A2A204572726F72#XX')
        self.sn.socket.sendall.assert_called_once_with(b'$O2A2A2A204572726F72#XX')
        self.assertEqual(self.sn.last, b"")
        mock_write.assert_has_calls([call("[WARNING] *** Error")])
        self.assertEqual(mock_write.call_count, 1)

    @patch('pyavrocd.dwlink.sys.stdout.write')
    @patch('pyavrocd.dwlink.os._exit')
    @patch('pyavrocd.dwlink.time.sleep')
    def test_connection_lost_exception(self, mock_sleep, mock_exit, mock_write):
        self.set_up()
        self.sn.connection_lost("LOST")
        mock_write.assert_has_calls([call("[ERROR] 'LOST'\n\r"),
                                               call("[INFO] Serial connection lost, will exit\n\r")])
        self.assertEqual(mock_write.call_count, 2)
        mock_sleep.assert_called_once()
        mock_exit.asssert_not_called()

    @patch('pyavrocd.dwlink.sys.stdout.write')
    @patch('pyavrocd.dwlink.os._exit')
    @patch('pyavrocd.dwlink.time.sleep')
    def test_connection_lost_closed(self, mock_sleep, mock_exit, mock_write):
        self.set_up()
        self.sn.connection_lost(None)
        mock_write.assert_has_calls([call("[INFO] Serial connection closed\n\r")])
        self.assertEqual(mock_write.call_count, 1)
        mock_exit.assert_called_once()
        mock_sleep.assert_not_called()

    @patch('pyavrocd.dwlink.serial.tools.list_ports.comports')
    @patch('pyavrocd.dwlink.sys.stdout.write')
    @patch('pyavrocd.dwlink.sys.stdout.flush', Mock())
    @patch('pyavrocd.dwlink.time.sleep', Mock())
    def test_discover_postive(self, mock_write, mock_comports):
        self.set_up()
        mock_ser0 = SimpleNamespace()
        mock_ser0.device = '/dev/cu.debug-console'
        mock_ser1 = SimpleNamespace()
        mock_ser1.device = '/dev/tty'
        mock_comports.return_value = [ mock_ser0, mock_ser1]
        args = SimpleNamespace()
        args.verbose = 'debug'
        args.dev = 'atmega328p'
        args.timers = 'freeze'
        args.manage = ['bootrst', 'lockbits' ]
        args.baud = 115200
        with patch("serial.Serial") as mock_Serial:
            mock_iface = MagicMock()
            mock_iface.read.side_effect = [ b'', b'dw-link' ]
            mock_iface.read_until.side_effect = [ b'6.', b'+', b'+', b'+' ]
            mock_Serial.return_value.__enter__.return_value = mock_iface
            result = discover(args)
            mock_iface.write.assert_has_calls([call(b'\x05'), call(b'\x05')])
            self.assertEqual(result, (115200, '/dev/tty', 6))
            mock_write.assert_has_calls([call("[DEBUG] Device: /dev/cu.debug-console\n"),
                                         call("[DEBUG] Device: /dev/tty\n"),
                                         call("[DEBUG] Check: /dev/tty\n")])

    @patch('pyavrocd.dwlink.serial.tools.list_ports.comports')
    @patch('pyavrocd.dwlink.sys.stdout.write')
    @patch('pyavrocd.dwlink.sys.stdout.flush', Mock())
    @patch('pyavrocd.dwlink.time.sleep', Mock())
    def test_discover_negative(self, mock_write, mock_comports):
        self.set_up()
        mock_ser0 = SimpleNamespace()
        mock_ser0.device = '/dev/cu.debug-console'
        mock_ser1 = SimpleNamespace()
        mock_ser1.device = '/dev/tty'
        mock_comports.return_value = [ mock_ser0, mock_ser1]
        args = SimpleNamespace()
        args.verbose = 'info'
        args.dev = 'atmega328p'
        args.baud = 115200
        with patch("serial.Serial") as mock_Serial:
            mock_iface = MagicMock()
            mock_iface.read.return_value = b''
            mock_Serial.return_value.__enter__.return_value = mock_iface
            result = discover(args)
            mock_write.assert_not_called()
            mock_iface.write.assert_has_calls([call(b'\x05'), call(b'\x05'), call(b'\x05'), call(b'\x05')])
            self.assertEqual(result, (None, None, None))

    @patch('pyavrocd.dwlink.discover')
    @patch('pyavrocd.dwlink.sys.stdout.write')
    def test_main_no_dwlink(self, mock_write, mock_discover):
        self.set_up()
        args = SimpleNamespace()
        args.verbose = 'info'
        args.dev = 'atmega328p'
        mock_discover.return_value = (None, None, None)
        self.assertEqual(main(args, 'debugwire'), None)
        mock_write.assert_not_called()

    @patch('pyavrocd.dwlink.discover')
    @patch('pyavrocd.dwlink.sys.stdout.write')
    def test_main_no_interface(self, mock_write,  mock_discover):
        self.set_up()
        args = SimpleNamespace()
        args.verbose = 'all'
        args.dev = 'atmega328p'
        mock_discover.return_value = (10, '/dev/null', 6)
        self.assertRaises(SystemExit, main, args, 'jtag')
        mock_write.assert_called_once()


