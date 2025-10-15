"""
The test suit for main module
"""
#pylint: disable=protected-access,missing-function-docstring,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
import logging
import os.path
from unittest.mock import MagicMock, Mock, call, patch, ANY
from unittest import TestCase
from types import SimpleNamespace
import sys
from usb.core import NoBackendError
import pymcuprog.pymcuprog_errors
from pyavrocd.main import _setup_tool_connection, options, install_udev_rules, setup_logging, \
     process_arguments, startup_helper_prog, run_server, startup
logging.basicConfig(level=logging.CRITICAL)

class TestMain(TestCase):

    def setUp(self):
        pass

    @patch('pyavrocd.main.logging.getLogger', MagicMock())
    def test_setup_tool_connection_full_spec(self):
        args = SimpleNamespace()
        args.serialnumber = "123456"
        args.tool = "PRODUCT"
        logger =  logging.getLogger()
        conn = _setup_tool_connection(args, logger)
        self.assertEqual(conn.serialnumber, args.serialnumber)
        self.assertEqual(conn.tool_name, args.tool)
        logger.info.assert_called_with("Connecting to " + args.tool + " (" + args.serialnumber + ")")

    @patch('pyavrocd.main.logging.getLogger', MagicMock())
    def test_setup_tool_connection_no_spec(self):
        args = SimpleNamespace()
        args.serialnumber = None
        args.tool = None
        logger =  logging.getLogger()
        conn = _setup_tool_connection(args, logger)
        self.assertEqual(conn.serialnumber, args.serialnumber)
        self.assertEqual(conn.tool_name, args.tool)
        logger.info.assert_called_with("Connecting to anything possible")

    @patch('pyavrocd.main.os.path.exists', MagicMock(return_value=False))
    @patch('pyavrocd.main.sys.exit', MagicMock())
    def test_options_none(self):
        args = options([])
        self.assertEqual(args.cmd, None)
        self.assertEqual(args.dev, None)
        self.assertEqual(args.clkdeb, 200)
        self.assertEqual(args.interface, None)
        self.assertEqual(args.manage, [])
        self.assertEqual(args.port, 2000)
        self.assertEqual(args.clkprg, 1000)
        self.assertEqual(args.tool, None)
        self.assertEqual(args.serialnumber, None)
        self.assertEqual(args.verbose, 'info')
        self.assertEqual(args.version, False)
        self.assertEqual(args.f, None)
        self.assertEqual(args.atexit, 'stayindebugwire')
        self.assertEqual(args.breakpoints, 'all')
        self.assertEqual(args.caching, 'enable')
        self.assertEqual(args.erasebeforeload, 'enable')
        self.assertEqual(args.onlywhenloaded, 'enable')
        self.assertEqual(args.rangestepping, 'enable')
        self.assertEqual(args.singlestep, 'safe')
        self.assertEqual(args.timers, 'run')
        self.assertEqual(args.verify, 'enable')
        self.assertEqual(args.load, None)

    @patch('pyavrocd.main.os.path.exists', MagicMock(return_value=False))
    @patch('pyavrocd.main.sys.exit', MagicMock())
    def test_options_questionmark(self):
        args = options(["-d", "mcu", "-t", "?"])
        self.assertEqual(args.dev, "mcu")
        self.assertEqual(args.tool, "?")
        sys.exit.assert_called_once()

    @patch('builtins.print')
    @patch('pyavrocd.main.sys.exit', MagicMock())
    def test_options_device_questionmark(self, mocked_print):
        options(["-d", "?", "-i", "pdi"])
        sys.exit.assert_called_once()
        mocked_print.assert_has_calls([call("Supported device with debugging interface 'pdi':"), call('None')])

    @patch('pyavrocd.main.os.path.exists', MagicMock(return_value=False))
    @patch('pyavrocd.main.sys.exit', MagicMock())
    def test_options_list(self):
        args = options(["-m", "all", "-m", "nobootrst", "-m=nodwen"])
        self.assertEqual(args.manage, [ "all", "nobootrst", "nodwen"])
        sys.exit.assert_not_called()

    @patch('pyavrocd.main.open', MagicMock())
    def test_udev(self):
        logger = MagicMock()
        self.assertEqual(install_udev_rules(logger), 0)


    @patch('pyavrocd.main.logging.basicConfig', MagicMock())
    @patch('pyavrocd.main.sys.stdout', MagicMock)
    def test_setup_logging_debug(self):
        args = SimpleNamespace()
        args.verbose = "debug"
        setup_logging(args, False)
        logging.basicConfig.assert_called_with(stream=sys.stdout, level='DEBUG', format='[%(levelname)s] %(name)s: %(message)s') #pylint: disable=no-member

    @patch('pyavrocd.main.logging.basicConfig', MagicMock())
    @patch('pyavrocd.main.sys.stdout', MagicMock)
    def test_setup_logging_info(self):
        args = SimpleNamespace()
        args.verbose = "info"
        setup_logging(args,  True)
        logging.basicConfig.assert_called_with(stream=sys.stdout, level='INFO', format='[%(levelname)s] %(message)s')  #pylint: disable=no-member

    def test_process_arguments_manage_override(self):
        args = SimpleNamespace()
        args.dev = 'atmega328p'
        args.interface = 'debugwire'
        args.version = None
        args.cmd = None
        args.tool = None
        args.manage = ['all', 'nobootrst', 'nodwen']
        args.clkprg = 1000
        args.clkdeb = 200
        self.assertEqual(process_arguments(args, MagicMock()), (None, 'atmega328p', 'debugwire'))
        self.assertEqual(args.manage, ['ocden', 'lockbits', 'eesave'])

    @patch('builtins.print')
    def test_process_arguments_wrong_iface(self, mocked_print):
        args = SimpleNamespace()
        args.dev = 'atmega328p'
        args.interface = 'jtag'
        args.version = None
        args.cmd = None
        args.tool = None
        args.manage = ['all', 'nobootrst', 'nodwen']
        args.clkprg = 1000
        args.clkdeb = 200
        self.assertEqual(process_arguments(args, MagicMock()), (1, None, None))
        mocked_print.assert_has_calls([call("Device 'atmega328p' does not have the interface 'jtag'")])

    @patch('pyavrocd.main.subprocess.Popen')
    def test_startup_helper_prog_noop(self, mocked_popen):
        args = SimpleNamespace()
        args.prg = 'noop'
        startup_helper_prog(args, MagicMock())
        mocked_popen.assert_not_called()

    @patch('pyavrocd.main.sys.exit')
    @patch('pyavrocd.main.shutil.which')
    @patch('pyavrocd.main.subprocess.Popen')
    def test_startup_helper_prog_call(self, mocked_popen, mocked_which, mocked_exit):
        args = SimpleNamespace()
        args.prg = 'prog -c'
        mocked_which.return_value = '/bin/prog'
        startup_helper_prog(args, MagicMock())
        mocked_popen.assert_called_with(['/bin/prog', '-c'])
        mocked_exit.assert_not_called()

    @patch('pyavrocd.main.sys.exit')
    @patch('pyavrocd.main.shutil.which')
    @patch('pyavrocd.main.subprocess.Popen')
    def test_startup_helper_prog_none(self, mocked_popen, mocked_which, mocked_exit):
        args = SimpleNamespace()
        args.prg = 'prog -c'
        mocked_which.return_value = None
        startup_helper_prog(args, MagicMock())
        mocked_popen.assert_not_called()
        mocked_exit.assert_called_once()

    def test_run_server_success(self):
        mock_server = MagicMock()
        mock_server.serve.return_value = 0
        mock_logger = MagicMock()
        self.assertEqual(run_server(mock_server, mock_logger), 0)

    @patch('pyavrocd.main.sys.stdout.write')
    def test_startup_no_args(self, mock_print):
        self.assertRaises(SystemExit,startup, [], Mock)
        self.assertEqual(mock_print.call_count,1)

    @patch('pyavrocd.main.sys.stderr.write')
    def test_startup_wrong_args(self, mock_print):
        self.assertRaises(SystemExit,startup, ['-x'], Mock)
        caller = os.path.basename(sys.argv[0])
        mock_print.assert_has_calls([call('usage: ' + caller + ' [options]\n'),
                                     call(caller + ': error: unrecognized arguments: -x\n')])

    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.dwlink.main')
    def test_startup_no_dwlink(self, mock_dwlink, mock_version):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        self.assertEqual(startup(['-d', 'atmega328p', '-t', 'dwlink'], mock_logger), 1)
        mock_logger.critical.assert_has_calls([call('No compatible tool discovered')])
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
        self.assertEqual(mock_dwlink.call_count,1)

    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.pymcuprog.backend.Backend')
    def test_startup_no_backend(self, mock_backend, mock_version):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        mock_backend.return_value = Mock(connect_to_tool=Mock(side_effect = NoBackendError("")))
        self.assertEqual(startup(['-d', 'atmega328p'], mock_logger), 1)
        self.assertEqual(mock_backend.call_count,1)
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
        mock_logger.critical.assert_has_calls([
                 call('Could not connect to hardware debugger: %s', ANY),
                 call("Install libusb: 'brew install libusb'"),
                 call('Maybe consult: https://github.com/greatscottgadgets/cynthion/issues/136')])

    @patch('pyavrocd.main.dwlink.main')
    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.pymcuprog.backend.Backend')
    def test_startup_no_tools(self, mock_backend, mock_version, mock_dwlink):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        mock_backend.return_value = MagicMock(connect_to_tool=Mock(side_effect=pymcuprog.pymcuprog_errors.PymcuprogToolConnectionError("")),get_available_hid_tools=Mock(return_value=[]))
        self.assertEqual(startup(['-d', 'atmega328p'], mock_logger), 1)
        self.assertEqual(mock_backend.call_count,1)
        self.assertEqual(mock_dwlink.call_count,1)
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
        mock_logger.critical.assert_has_calls([call('No compatible tool discovered')])

    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.pymcuprog.backend.Backend')
    def test_startup_two_tools(self, mock_backend, mock_version):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        mock_backend.return_value = MagicMock(connect_to_tool=Mock(side_effect=pymcuprog.pymcuprog_errors.PymcuprogToolConnectionError("")),get_available_hid_tools=Mock(return_value=[1,2]))
        self.assertEqual(startup(['-d', 'atmega328p'], mock_logger), 1)
        self.assertEqual(mock_backend.call_count,1)
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
        mock_logger.critical.assert_has_calls([call('Too many connected tools. Use -t or -s to distinguish!')])





