"""
The test suit for main module
"""
#pylint: disable=protected-access,missing-function-docstring,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
import itertools
import logging
from unittest.mock import MagicMock, Mock, call, patch, ANY
from unittest import TestCase
from types import SimpleNamespace
import os
import sys
from usb.core import NoBackendError
import pymcuprog.pymcuprog_errors
from pyavrocd.main import options,  setup_logging, \
     process_arguments, startup_helper_prog, run_server, startup, handle_simavr, tool_reboot, \
     find_jtag2_tool
from pyavrocd.backend import ProbeCandidate

class TestMain(TestCase):

    @patch('pyavrocd.main.os.path.exists', MagicMock(return_value=False))
    @patch('pyavrocd.main.sys.exit', MagicMock())
    def test_options_none(self):
        args = options([])
        self.assertEqual(args.webhelp, False)
        self.assertEqual(args.attach, False)
        self.assertEqual(args.cmd, None)
        self.assertEqual(args.dev, None)
        self.assertEqual(args.interface, None)
        self.assertEqual(args.manage, ['none'])
        self.assertEqual(args.port, 2000)
        self.assertEqual(args.clkprg, 1000)
        self.assertEqual(args.clkdeb, None)
        self.assertEqual(args.kbps, 750)
        self.assertEqual(args.tool, None)
        self.assertEqual(args.serialnumber, None)
        self.assertEqual(args.verbose, 'info')
        self.assertEqual(args.version, False)
        self.assertEqual(args.xarg, None)
        self.assertEqual(args.baud, 115200)
        self.assertEqual(args.reboot, False)
        self.assertEqual(args.nomm, False)
        self.assertEqual(args.skipsig, False)
        self.assertEqual(args.f, None)
        self.assertEqual(args.F_CPU, '1000000')
        self.assertEqual(args.atexit, None)
        self.assertEqual(args.breakpoints, 'all')
        self.assertEqual(args.caching, 'enable')
        self.assertEqual(args.debugwire, None)
        self.assertEqual(args.erasebeforeload, None)
        self.assertEqual(args.load, None)
        self.assertEqual(args.onlywhenloaded, None)
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

    @patch('pyavrocd.main.os.path.exists', MagicMock(return_value=True))
    @patch('pyavrocd.main.argparse.ArgumentParser.parse_args')
    def test_add_pyavrocd_options(self,mockparse):
        mockparse.return_value = SimpleNamespace(dev="atmega328p",
                                                     webhelp=False,
                                                     version=False,
                                                     interface="debugwire",
                                                     manage=[],
                                                     tool='dwlink',
                                                     verbose='all',
                                                     kbps=None)
        options(["-d", "atmega328p"])
        mockparse.assert_called_with(["-d", "atmega328p", "@pyavrocd.options"])

    @patch('pyavrocd.main.sys.exit', MagicMock())
    @patch('pyavrocd.main.importlib.metadata.version')
    def test_options_version(self, mockversion):
        mockversion.return_value = "VERSION"
        options(["--version"])
        sys.exit.assert_called_once()

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
        args.kbps = None
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
        args.kbps = None
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
        args.kbps = None
        args.clkdeb = None
        self.assertEqual(process_arguments(args, MagicMock()), (None, 'atmega328p', 'debugwire'))
        self.assertEqual(args.clkdeb, 400)

    def test_process_arguments_default_kbps(self):
        args = SimpleNamespace()
        args.cmd = None
        args.manage = []
        args.dev = 'atmega328p'
        args.interface = 'debugwire'
        args.version = None
        args.tool = None
        args.F_CPU = '4000000L'
        args.clkprg = 1000
        args.kbps = None
        args.clkdeb = None
        self.assertEqual(process_arguments(args, MagicMock()), (None, 'atmega328p', 'debugwire'))
        self.assertEqual(args.kbps, None)

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
        args.kbps = None
        self.assertEqual(process_arguments(args, MagicMock()), (1, "", ""))
        mocked_print.assert_has_calls([call("Negative frequency or communication speed values are discouraged")])

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
        args.kbps = None
        args.reboot = False
        self.assertEqual(process_arguments(args, MagicMock()), (1, "", ""))
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
        args.kbps = None
        self.assertEqual(process_arguments(args, MagicMock()), (1, "", ""))
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
        args.kbps = None
        self.assertEqual(process_arguments(args, MagicMock()), (1, "", ""))
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
        mocked_popen.assert_called_with(os.path.abspath('/bin/prog'))
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
        args.xarg = ['-oout.log', '--add-trace=LED=trace@0x0038/0xff']
        mocked_which.return_value =  '/usr/bin/simavr'
        self.assertTrue(handle_simavr(args, 'atmega328p'))
        mocked_popen.assert_called_once()
        mocked_exit.assert_not_called()

    def test_run_server_success(self):
        mock_server = MagicMock()
        mock_server.serve.return_value = 0
        mock_logger = MagicMock()
        self.assertEqual(run_server(mock_server, mock_logger), 0)

    def test_run_server_error(self):
        mock_server = Mock(serve=Mock(side_effect = ValueError()))
        self.assertEqual(run_server(mock_server, Mock()), 1)

    @patch('pyavrocd.main.time.sleep',Mock())
    def test_reboot(self):
        mockbackend = MagicMock(reboot_tool=Mock(), connect_to_tool=Mock())
        self.assertEqual(tool_reboot(mockbackend, Mock(), Mock()), True)
        mockbackend.reboot_tool.assert_called_once()
        mockbackend.connect_to_tool.assert_called_once()

    @patch('pyavrocd.main.time.sleep',Mock())
    def test_reboot_timeout(self):
        mockbackend = MagicMock(reboot_tool=Mock(), connect_to_tool=Mock(side_effect=ValueError()))
        mock_logger = Mock()
        self.assertEqual(tool_reboot(mockbackend, Mock(), mock_logger), False)
        mock_logger.critical.assert_called_with("... could not reconnect")

    def test_startup_fail(self):
        mock_logger = Mock()
        self.assertEqual(startup(['-t', 'dwlink'], mock_logger), 1)

    @patch('pyavrocd.main.sys.stdout.write')
    def test_startup_no_args(self, mock_print):
        self.assertRaises(SystemExit,startup, [], Mock)
        self.assertEqual(mock_print.call_count,1)

    @patch('pyavrocd.main.sys.stderr.write')
    def test_startup_wrong_args(self, mock_print):
        self.assertRaises(SystemExit,startup, ['-z'], Mock)
        mock_print.assert_has_calls([call('pyavrocd: error: unrecognized arguments: -z\n')])

    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.dwlinkbackend.discover', return_value=[])
    def test_startup_no_dwlink(self, mock_dwlink, mock_version):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        self.assertEqual(startup(['-d', 'atmega328p', '-t', 'dwlink'], mock_logger), 1)
        mock_logger.critical.assert_has_calls([call('No compatible tool discovered')])
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
        self.assertEqual(mock_dwlink.call_count,1)

    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.usb.core.find')
    @patch('pyavrocd.main.platform.system')
    def test_startup_mac_no_backend(self, mock_system, mock_find, mock_version):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        mock_find.side_effect = NoBackendError("")
        mock_system.return_value = 'Darwin'
        self.assertEqual(startup(['-d', 'atmega328p'], mock_logger), 1)
        mock_find.assert_called_once()
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
        mock_logger.critical.assert_has_calls([call('Could not discover debug probes: %s', ANY),
                                                   call("Install libusb: 'brew install libusb'")])

    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.usb.core.find')
    @patch('pyavrocd.main.platform.system')
    def test_startup_linux_no_backend(self, mock_system, mock_find, mock_version):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        mock_find.side_effect = NoBackendError("")
        mock_system.return_value = 'Linux'
        self.assertEqual(startup(['-d', 'atmega328p'], mock_logger), 1)
        mock_find.assert_called_once()
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
        mock_logger.critical.assert_has_calls([call('Could not discover debug probes: %s', ANY),
                                                   call("Install libusb: 'sudo apt install libusb-1.0-0'")])

    @patch('pyavrocd.main.dwlinkbackend.discover', return_value=[])
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

    @patch('pyavrocd.main.usb.core.find')
    @patch('pyavrocd.main.pymcuprog.backend.Backend')
    @patch('pyavrocd.main.platform.system')
    def test_startup_linux_no_udev(self, mock_system, mock_backend, mock_find):
        t3 = SimpleNamespace()
        t3.idVendor = 0x3EB
        t3.idProduct = 0x2141
        mock_find.return_value=[ t3 ]
        mock_backend.return_value = MagicMock(get_available_hid_tools=MagicMock(return_value=[]))
        mock_system.return_value = 'Linux'
        mock_logger = MagicMock()
        self.assertEqual(startup(['-d', 'atmega328p'], mock_logger), 1)
        mock_logger.critical.assert_called_with("review, edit, and install under /etc/udev/rules.d/.")

    @patch('pyavrocd.main.usb.core.find')
    @patch('pyavrocd.main.pymcuprog.backend.Backend')
    @patch('pyavrocd.main.platform.system')
    def test_startup_mac_not_available(self, mock_system, mock_backend, mock_find):
        t3 = SimpleNamespace()
        t3.idVendor = 0x3EB
        t3.idProduct = 0x2141
        mock_find.return_value=[ t3 ]
        mock_backend.return_value = MagicMock(get_available_hid_tools=MagicMock(return_value=[]))
        mock_system.return_value = 'Darwin'
        mock_logger = MagicMock()
        self.assertEqual(startup(['-d', 'atmega328p'], mock_logger), 1)
        mock_logger.error.assert_called_with("Not all discovered tools are available")
        mock_logger.critical.assert_called_with("No compatible tool discovered")

    @patch('pyavrocd.main.EdbgBackend', MagicMock())
    @patch('pyavrocd.main.RspServer', MagicMock())
    @patch('pyavrocd.main.dwlinkbackend.discover', return_value=[])
    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.usb.core.find')
    @patch('pyavrocd.main.pymcuprog.backend.Backend')
    def test_startup_with_tool(self, mock_backend, mock_find,  mock_version, mock_dwlink):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        t3 = SimpleNamespace()
        t3.idVendor = 0x3EB
        t3.idProduct = 0x2141
        t3.vendor_id = 0x3EB
        t3.product_id = 0x2141
        mock_find.return_value=[ t3 ]
        mock_backend.return_value = MagicMock(connect_to_tool=Mock(),get_available_hid_tools=MagicMock(return_value=[t3]),transport=Mock())
        self.assertNotEqual(startup(['-d', 'atmega328p', '-v=all'], mock_logger), 1)
        self.assertEqual(mock_dwlink.call_count,0)
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION'),
                                               call('Connected to %s, SN: %s', ANY, ANY),
                                               call('Starting GDB server')])

    @patch('pyavrocd.main.dwlinkbackend.discover', return_value=[])
    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.usb.core.find')
    @patch('pyavrocd.main.pymcuprog.backend.Backend')
    def test_startup_oserror_busy(self, mock_backend, mock_find,  mock_version, mock_dwlink):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        t3 = SimpleNamespace()
        t3.idVendor = 0x3EB
        t3.idProduct = 0x2141
        t3.vendor_id = 0x3EB
        t3.product_id = 0x2141
        mock_find.return_value=[ t3 ]
        mock_backend.return_value = MagicMock(connect_to_tool=Mock(side_effect=OSError("open failed")),
                                                  get_available_hid_tools=MagicMock(return_value=[t3]),
                                                  transport=Mock())
        self.assertEqual(startup(['-d', 'atmega328p', '-v=all'], mock_logger), 1)
        self.assertEqual(mock_dwlink.call_count,0)
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
        mock_logger.critical.assert_has_calls([call('Debug probe busy, cannot connect')])

    @patch('pyavrocd.main.EdbgBackend', MagicMock())
    @patch('pyavrocd.main.RspServer', MagicMock())
    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.usb.core.find')
    @patch('pyavrocd.main.pymcuprog.backend.Backend')
    def test_startup_oserror_other(self, mock_backend, mock_find,  mock_version):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        t3 = SimpleNamespace()
        t3.idVendor = 0x3EB
        t3.idProduct = 0x2141
        t3.vendor_id = 0x3EB
        t3.product_id = 0x2141
        mock_find.return_value=[ t3 ]
        mock_backend.return_value = MagicMock(connect_to_tool=Mock(side_effect=OSError("other")),
                                                  get_available_hid_tools=MagicMock(return_value=[t3]),
                                                  transport=Mock())
        self.assertEqual(startup(['-d', 'atmega328p', '-v=all'], mock_logger), 1)
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
        mock_logger.critical.assert_has_calls([call('Could not connect to debug probe: %s', 'other')])

    @patch('pyavrocd.main.RspServer', MagicMock())
    @patch('pyavrocd.main.EdbgBackend', MagicMock())
    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.usb.core.find')
    @patch('pyavrocd.main.pymcuprog.backend.Backend')
    def test_startup_reboot(self, mock_backend, mock_find,  mock_version):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        t3 = SimpleNamespace()
        t3.idVendor = 0x3EB
        t3.idProduct = 0x2141
        t3.vendor_id = 0x3EB
        t3.product_id = 0x2141
        mock_find.return_value=[ t3 ]
        mock_backend.return_value = MagicMock(connect_to_tool=Mock(),get_available_hid_tools=MagicMock(return_value=[t3]),transport=Mock())
        self.assertNotEqual(startup(['-d', 'atmega328p', '-v=all', '--reboot'], mock_logger), 1)
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION'),
                                           call('Connected to %s, SN: %s', ANY, ANY),
                                           call('Rebooting debugger...'),
                                           call('Reconnected to %s', ANY),
                                           call('Starting GDB server')])
        mock_logger.critical.assert_not_called()

    @patch('pyavrocd.main.sys.exit')
    @patch('pyavrocd.main.shutil.which')
    @patch('pyavrocd.main.subprocess.Popen')
    def test_startup_simavr(self, mocked_popen, mocked_which, mocked_exit):
        mocked_which.return_value =  '/usr/bin/simavr'
        self.assertEqual(startup(['-d', 'atmega328p', '-s=simavr'], Mock()), 0)
        mocked_popen.assert_called_once()
        mocked_exit.assert_not_called()

    # Pinned to Linux: on Windows number_of_connected_edbg_tools creates a
    # Backend of its own, and the call count below would be 2.
    @patch('pyavrocd.main.platform.system', MagicMock(return_value='Linux'))
    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.pymcuprog.backend.Backend')
    @patch('pyavrocd.main.usb.core.find')
    def test_startup_two_tools(self, mock_find, mock_backend, mock_version):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        t1 = SimpleNamespace()
        t1.idVendor = 0x3EB
        t1.idProduct = 0x2140
        t1.vendor_id = 0x3EB
        t1.product_id = 0x2140
        t1.product_string = "PROD1"
        t1.serial_number ="S/N01"
        t2 = SimpleNamespace()
        t2.idVendor = 0x3EB
        t2.idProduct = 0x2141
        t2.vendor_id = 0x3EB
        t2.product_id = 0x2141
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
        mock_logger.critical.assert_has_calls([call('More than one compatible tool! Use -t or -u to select.'),
                                                   call(' Tool: %s, SN: %s', 'PROD1', 'S/N01'),
                                                   call(' Tool: %s, SN: %s', 'PROD2', 'S/N02')])


class TestFindJtag2Tool(TestCase):
    """main picks a JTAGICE mkII / AVR Dragon to debug with, or leaves the choice to the EDBG tools"""

    CLONE = ProbeCandidate('jtagice2', 'JTAGICE mkII', '090000004262')
    DRAGON = ProbeCandidate('dragon', 'AVRDRAGON', '00A200050860')

    def find(self, found, tool=None, sn=None, num_edbg=0, edbg_serial=False):
        logger = MagicMock()
        args = SimpleNamespace(tool=tool, serialnumber=sn)
        # one second per call to the clock: the wait for a re-enumerating probe takes no real time
        with patch('pyavrocd.main.jtag2.discover', side_effect=lambda t=None: [c for c in found if t in (None, c.tool)]), \
             patch('pyavrocd.main.time.monotonic', side_effect=itertools.count()), \
             patch('pyavrocd.main.time.sleep'), \
             patch('pyavrocd.main.edbg_tool_with_serial', return_value=edbg_serial):
            return find_jtag2_tool(args, num_edbg, logger), logger

    def test_none_attached(self):
        (abort, probe), _ = self.find([])
        self.assertEqual((abort, probe), (False, None)) # on to the EDBG tools or dw-link, as before

    def test_none_attached_but_asked_for(self):
        (abort, probe), logger = self.find([], tool='dragon')
        self.assertEqual((abort, probe), (True, None))
        logger.critical.assert_called_with("No compatible tool discovered")

    def test_one_alone(self):
        (abort, probe), logger = self.find([self.DRAGON])
        self.assertEqual((abort, probe), (False, self.DRAGON))
        logger.critical.assert_not_called()

    def test_two_without_selection(self):
        (abort, probe), logger = self.find([self.CLONE, self.DRAGON])
        self.assertEqual((abort, probe), (True, None))
        logger.critical.assert_any_call("More than one compatible tool! Use -t or -u to select.")

    def test_selected_by_tool_and_by_serial(self):
        self.assertEqual(self.find([self.CLONE, self.DRAGON], tool='jtagice2')[0], (False, self.CLONE))
        self.assertEqual(self.find([self.CLONE, self.DRAGON], sn='0860')[0], (False, self.DRAGON))
        self.assertEqual(self.find([self.CLONE, self.DRAGON], sn='a200050860')[0], # case does not matter
                         (False, self.DRAGON))

    def test_with_an_edbg_tool(self):
        (abort, probe), logger = self.find([self.DRAGON], num_edbg=1)
        self.assertEqual((abort, probe), (True, None)) # ambiguous without -t / -u
        logger.critical.assert_any_call("More than one compatible tool! Use -t or -u to select.")
        self.assertEqual(self.find([self.DRAGON], num_edbg=1, sn='18184')[0], (False, None)) # -u names the EDBG tool
        self.assertEqual(self.find([self.DRAGON], num_edbg=1, tool='atmelice')[0], (False, None)) # an EDBG tool

    def test_waits_for_reenumeration(self):
        # after avrdude has signed off, the probe is back on the bus only after a few seconds
        logger = MagicMock()
        attempts = iter([[], [], [self.CLONE]])
        with patch('pyavrocd.main.jtag2.discover', side_effect=lambda t=None: next(attempts)), \
             patch('pyavrocd.main.time.monotonic', side_effect=itertools.count()), \
             patch('pyavrocd.main.time.sleep') as sleep:
            self.assertEqual(find_jtag2_tool(SimpleNamespace(tool=None, serialnumber='4262'), 0, logger),
                             (False, self.CLONE))
        self.assertEqual(sleep.call_count, 2)

    def test_no_wait_when_an_edbg_tool_is_meant(self):
        with patch('pyavrocd.main.jtag2.discover', return_value=[]) as discover, \
             patch('pyavrocd.main.edbg_tool_with_serial', return_value=True):
            self.assertEqual(find_jtag2_tool(SimpleNamespace(tool=None, serialnumber='18184'), 1, MagicMock()),
                             (False, None))
        self.assertEqual(discover.call_count, 1)

    def test_no_libusb(self):
        logger = MagicMock()
        with patch('pyavrocd.main.jtag2.discover', side_effect=NoBackendError("none")):
            self.assertEqual(find_jtag2_tool(SimpleNamespace(tool=None, serialnumber=None), 1, logger),
                             (False, None))

