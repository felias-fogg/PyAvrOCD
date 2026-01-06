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
from pyavrocd.main import options,  setup_logging, \
     process_arguments, startup_helper_prog, run_server, startup, handle_simavr

class TestMain(TestCase):

    @patch('pyavrocd.main.os.path.exists', MagicMock(return_value=False))
    @patch('pyavrocd.main.sys.exit', MagicMock())
    def test_options_none(self):
        args = options([])
        self.assertEqual(args.webhelp, False)
        self.assertEqual(args.cmd, None)
        self.assertEqual(args.dev, None)
        self.assertEqual(args.clkdeb, None)
        self.assertEqual(args.interface, None)
        self.assertEqual(args.manage, ['none'])
        self.assertEqual(args.port, 2000)
        self.assertEqual(args.clkprg, 1000)
        self.assertEqual(args.tool, None)
        self.assertEqual(args.serialnumber, None)
        self.assertEqual(args.verbose, 'info')
        self.assertEqual(args.version, False)
        self.assertEqual(args.f, None)
        self.assertEqual(args.F_CPU, '1000000')
        self.assertEqual(args.atexit, 'stayindebugwire')
        self.assertEqual(args.breakpoints, 'all')
        self.assertEqual(args.caching, 'enable')
        self.assertEqual(args.erasebeforeload, 'enable')
        self.assertEqual(args.load, None)
        self.assertEqual(args.onlywhenloaded, 'enable')
        self.assertEqual(args.rangestepping, 'enable')
        self.assertEqual(args.singlestep, 'safe')
        self.assertEqual(args.timers, 'run')
        self.assertEqual(args.verify, 'enable')

    @patch('pyavrocd.main.os.path.exists', MagicMock(return_value=False))
    @patch('pyavrocd.main.sys.exit', MagicMock())
    def test_options_tools_questionmark(self):
        args = options(["-d", "mcu", "-t", "?"])
        self.assertEqual(args.dev, "mcu")
        self.assertEqual(args.tool, "?")
        sys.exit.assert_called_once()

    @patch('pyavrocd.main.sys.exit', MagicMock())
    @patch('pyavrocd.main.webbrowser.open')
    def test_options_webhelp(self, mock_web):
        options(["-H"])
        mock_web.assert_called_once()
        sys.exit.assert_called_once()


    @patch('builtins.print')
    @patch('pyavrocd.main.sys.exit', MagicMock())
    def test_options_device_with_interface_questionmark(self, mocked_print):
        options(["-d", "?", "-i", "pdi"])
        sys.exit.assert_called_once()
        mocked_print.assert_has_calls([call("Supported devices with debugging interface 'pdi':"), call('None')])

    @patch('builtins.print')
    @patch('pyavrocd.main.sys.exit', MagicMock())
    def test_options_device_questionmark(self, mocked_print):
        options(["-d", "?"])
        sys.exit.assert_called_once()
        mocked_print.assert_has_calls([call("Supported devices:")])


    @patch('builtins.print')
    @patch('pyavrocd.main.sys.exit', MagicMock())
    def test_options_questionmarks(self, mocked_print):
        options(['-i?', '-m', '?', '--verbose=?'])
        sys.exit.assert_called_once()
        mocked_print.assert_has_calls([
            call('Possible interfaces (-i) are: ', end=''),
            call('debugwire, jtag, pdi, updi'),
            call('Possible (repeatable) fuse management options (-m) are: '),
            call('all, none, bootrst, nobootrst, dwen, nodwen, ocden, noocden, lockbits, nolockbits, eesave, noeesave', '(default = none)'),
            call('Possible verbosity levels (-v) are: '),
            call('all, debug, info, warning, error, critical', '(default = info)')])


    @patch('pyavrocd.main.os.path.exists', MagicMock(return_value=False))
    @patch('pyavrocd.main.sys.exit', MagicMock())
    def test_options_list(self):
        args = options(["-m", "all", "-m", "nobootrst", "-m=nodwen"])
        self.assertEqual(args.manage, [ "none", "all", "nobootrst", "nodwen"])
        sys.exit.assert_not_called()

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
        args.F_CPU = '1000000L'
        args.clkprg = 1000
        args.clkdeb = 200
        self.assertEqual(process_arguments(args, MagicMock()), (None, 'atmega328p', 'debugwire'))
        self.assertEqual(args.manage, ['ocden', 'lockbits', 'eesave'])

    def test_process_arguments_gdb_manage_none_port(self):
        args = SimpleNamespace()
        args.dev = 'atmega328p'
        args.interface = 'debugwire'
        args.version = None
        args.cmd = [ 'tcl_port 56', 'gdb_port 9999' ]
        args.tool = None
        args.F_CPU = '1000000L'
        args.manage = ['all', 'nobootrst', 'nodwen', 'none', 'eesave' ]
        args.clkprg = 1000
        args.clkdeb = 200
        self.assertEqual(process_arguments(args, MagicMock()), (None, 'atmega328p', 'debugwire'))
        self.assertEqual(args.manage, ['eesave'])
        self.assertEqual(args.port, 9999)

    def test_process_arguments_default_clkdeb(self):
        args = SimpleNamespace()
        args.cmd = None
        args.manage = []
        args.dev = 'atmega328p'
        args.interface = 'debugwire'
        args.version = None
        args.tool = None
        args.F_CPU = '2000000L'
        args.clkprg = 1000
        args.clkdeb = None
        self.assertEqual(process_arguments(args, MagicMock()), (None, 'atmega328p', 'debugwire'))
        self.assertEqual(args.clkdeb, 400)

    @patch('builtins.print')
    def test_process_arguments_neg_freq(self, mocked_print):
        args = SimpleNamespace()
        args.dev = 'atmega328p'
        args.interface = 'debugwire'
        args.version = None
        args.cmd = None
        args.tool = None
        args.manage = []
        args.clkprg = -10
        args.clkdeb = None
        args.F_CPU = '1000000L'
        self.assertEqual(process_arguments(args, MagicMock()), (1, None, None))
        mocked_print.assert_has_calls([call("Negative frequency values are discouraged")])

    @patch('builtins.print')
    def test_process_arguments_no_device(self, mocked_print):
        args = SimpleNamespace()
        args.dev = None
        args.interface = 'debugwire'
        args.version = None
        args.cmd = None
        args.tool = None
        args.manage = []
        args.clkprg = 1000
        args.clkdeb = None
        args.F_CPU = '1000000L'
        self.assertEqual(process_arguments(args, MagicMock()), (1, None, None))
        mocked_print.assert_has_calls([call("Please specify target MCU with -d option")])

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
        args.clkdeb = None
        args.F_CPU = '1000000L'
        self.assertEqual(process_arguments(args, MagicMock()), (1, None, None))
        mocked_print.assert_has_calls([call("Device 'atmega328p' does not have the interface 'jtag'")])

    @patch('builtins.print')
    def test_process_arguments_no_support(self, mocked_print):
        args = SimpleNamespace()
        args.dev = 'atmega31'
        args.interface = 'jtag'
        args.version = None
        args.cmd = None
        args.tool = None
        args.manage = ['all', 'nobootrst', 'nodwen']
        args.clkprg = 1000
        args.clkdeb = None
        args.F_CPU = '1000000L'
        self.assertEqual(process_arguments(args, MagicMock()), (1, None, None))
        mocked_print.assert_has_calls([call("Device 'atmega31' is not supported by PyAvrOCD")])

    @patch('pyavrocd.main.subprocess.Popen')
    def test_startup_helper_prog_nop(self, mocked_popen):
        args = SimpleNamespace()
        args.prg = 'nop'
        startup_helper_prog(args, MagicMock())
        mocked_popen.assert_not_called()

    @patch('pyavrocd.main.sys.exit')
    @patch('pyavrocd.main.shutil.which')
    @patch('pyavrocd.main.subprocess.Popen')
    def test_startup_helper_prog_call(self, mocked_popen, mocked_which, mocked_exit):
        args = SimpleNamespace()
        args.prg = 'prog'
        mocked_which.return_value = '/bin/prog'
        startup_helper_prog(args, MagicMock())
        mocked_popen.assert_called_with('/bin/prog')
        mocked_exit.assert_not_called()

    @patch('pyavrocd.main.sys.exit')
    @patch('pyavrocd.main.shutil.which')
    @patch('pyavrocd.main.subprocess.Popen')
    def test_startup_helper_prog_none(self, mocked_popen, mocked_which, mocked_exit):
        args = SimpleNamespace()
        args.prg = 'prog'
        mocked_which.return_value = None
        startup_helper_prog(args, MagicMock())
        mocked_popen.assert_not_called()
        mocked_exit.assert_called_once()

    @patch('pyavrocd.main.subprocess.Popen')
    def test_handle_simavr_empty(self, mocked_popen):
        args = SimpleNamespace()
        args.prg = None
        self.assertFalse(handle_simavr(args, 'atmega328p'))
        mocked_popen.assert_not_called()

    @patch('pyavrocd.main.subprocess.Popen')
    def test_handle_simavr_nop(self, mocked_popen):
        args = SimpleNamespace()
        args.prg = 'nop'
        self.assertFalse(handle_simavr(args, 'atmega328p'))
        mocked_popen.assert_not_called()

    @patch('pyavrocd.main.shutil.which')
    @patch('pyavrocd.main.subprocess.Popen')
    def test_handle_simavr_not_called(self, mocked_popen, mocked_which):
        args = SimpleNamespace()
        args.prg = '/usr/bin/simavr'
        mocked_which.return_value = None
        self.assertTrue(handle_simavr(args, 'atmega328p'))
        mocked_popen.assert_not_called()

    @patch('pyavrocd.main.sys.exit')
    @patch('pyavrocd.main.shutil.which')
    @patch('pyavrocd.main.subprocess.Popen')
    def test_handle_simavr_called(self, mocked_popen, mocked_which, mocked_exit):
        args = SimpleNamespace()
        args.prg = 'simavr'
        args.port = 2000
        args.F_CPU = '16000000UL'
        args.xargs = '-o out.log --add-trace LED=trace@0x0038/0xff'
        mocked_which.return_value =  '/usr/bin/simavr'
        self.assertTrue(handle_simavr(args, 'atmega328p'))
        mocked_popen.assert_called_once()
        mocked_exit.assert_not_called()

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
        self.assertRaises(SystemExit,startup, ['-z'], Mock)
        caller = os.path.basename(sys.argv[0])
        mock_print.assert_has_calls([
                                     call(caller + ': error: unrecognized arguments: -z\n')])

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
    @patch('pyavrocd.main.usb.core.find')
    def test_startup_no_backend(self, mock_find, mock_version):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        mock_find.side_effect = NoBackendError("")
        self.assertEqual(startup(['-d', 'atmega328p'], mock_logger), 1)
        mock_find.assert_called_once()
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
        mock_logger.critical.assert_has_calls([call('Could not discover debug probes: %s', ANY)])

    @patch('pyavrocd.main.dwlink.main')
    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.usb.core.find')
    def test_startup_no_tools(self, mock_find,  mock_version, mock_dwlink):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        t3 = SimpleNamespace()
        t3.idVendor = 0x3EB
        t3.idProduct = 0x2139
        mock_find.return_value=[ t3 ]
        self.assertEqual(startup(['-d', 'atmega328p'], mock_logger), 1)
        self.assertEqual(mock_dwlink.call_count,1)
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
        mock_logger.critical.assert_has_calls([call('No compatible tool discovered')])

    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.pymcuprog.backend.Backend')
    @patch('pyavrocd.main.usb.core.find')
    def test_startup_two_tools(self, mock_find, mock_backend, mock_version):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        t1 = SimpleNamespace()
        t1.idVendor = 0x3EB
        t1.idProduct = 0x2140
        t1.product_string = "PROD1"
        t1.serial_number ="S/N01"
        t2 = SimpleNamespace()
        t2.idVendor = 0x3EB
        t2.idProduct = 0x2141
        t2.product_string = "PROD2"
        t2.serial_number ="S/N02"
        t3 = SimpleNamespace()
        t3.idVendor = 0x3EB
        t3.idProduct = 0x2139
        t4 = SimpleNamespace()
        t4.idVendor = 0x3EC
        t4.idProduct = 0x2140
        mock_find.return_value=(t1, t2, t3, t4)
        mock_backend.return_value = MagicMock(connect_to_tool=Mock(side_effect=pymcuprog.pymcuprog_errors.PymcuprogToolConnectionError("")),get_available_hid_tools=MagicMock(return_value=[t1,t2]))
        self.assertEqual(startup(['-d', 'atmega328p'], mock_logger), 1)
        self.assertEqual(mock_backend.call_count,1)
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
        mock_logger.critical.assert_has_calls([call('More than one compatible tool! Use -u or -t to distinguish.'),
                                                   call('> Tool: %s, S/N: %s', 'PROD1', 'S/N01'),
                                                   call('> Tool: %s, S/N: %s', 'PROD2', 'S/N02')])





