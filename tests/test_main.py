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
     process_arguments, startup_helper_prog, run_server, startup, handle_simavr, \
     find_probe, EDBG_PRODUCTS
from pyavrocd.backend import ProbeCandidate
from pyavrocd.xavrdebugger import EdbgBackend, EdbgProbe


def hid_tool(pid=0x2141, product='Atmel-ICE CMSIS-DAP', sn='J42700018184'):
    """an EDBG tool as libusb (idVendor, idProduct) and hidapi (the rest) see it"""
    return SimpleNamespace(idVendor=0x3EB, idProduct=pid, vendor_id=0x3EB, product_id=pid,
                           product_string=product, serial_number=sn)

def no_hid_tools():
    return MagicMock(get_available_hid_tools=MagicMock(return_value=[]))

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

    @patch('pyavrocd.xavrdebugger.time.sleep',Mock())
    def test_reboot(self):
        mockbackend = MagicMock(reboot_tool=Mock(), connect_to_tool=Mock())
        self.assertEqual(EdbgBackend.reboot_probe(EdbgProbe(mockbackend, Mock()), Mock(), Mock()), True)
        mockbackend.reboot_tool.assert_called_once()
        mockbackend.connect_to_tool.assert_called_once()

    @patch('pyavrocd.xavrdebugger.time.sleep',Mock())
    def test_reboot_timeout(self):
        mockbackend = MagicMock(reboot_tool=Mock(), connect_to_tool=Mock(side_effect=ValueError()))
        mock_logger = Mock()
        self.assertEqual(EdbgBackend.reboot_probe(EdbgProbe(mockbackend, Mock()), Mock(), mock_logger), False)
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

    @patch('pyavrocd.main.serve')
    @patch('pyavrocd.main.Jtag2Backend.reboot_probe', return_value=True)
    @patch('pyavrocd.main.find_probe')
    @patch('pyavrocd.main.importlib.metadata.version', return_value='VERSION')
    def test_startup_reboot_jtag2_only(self, _version, mock_find, mock_reboot, mock_serve):
        dragon = ProbeCandidate(tool='dragon', product='AVRDRAGON', address='00A200050860')
        mock_find.return_value = (False, dragon)
        mock_logger = MagicMock()
        self.assertEqual(startup(['--reboot-debugger'], mock_logger), 0)
        mock_reboot.assert_called_once_with(dragon, ANY, mock_logger)
        mock_serve.assert_not_called()
        mock_logger.info.assert_called_with('Terminating ...')

    @patch('pyavrocd.main.serve', return_value=0)
    @patch('pyavrocd.main.DwlinkBackend.reboot_probe', return_value=True)
    @patch('pyavrocd.main.dwlinkbackend.discover')
    @patch('pyavrocd.main.importlib.metadata.version', return_value='VERSION')
    def test_startup_reboot_dwlink(self, _version, mock_discover, mock_reboot, mock_serve):
        dwlink = ProbeCandidate(tool='dwlink', product='dw-link', address='/dev/cu.usbmodem242101')
        mock_discover.return_value = [dwlink]
        mock_logger = MagicMock()
        self.assertEqual(startup(['--reboot-debugger', '-t', 'dwlink'], mock_logger), 0)  # no device
        mock_reboot.assert_called_once_with(dwlink, ANY, mock_logger)
        self.assertEqual(mock_reboot.call_args.args[1].baud, 115200)
        mock_serve.assert_not_called()
        mock_reboot.reset_mock()
        self.assertEqual(startup(['--reboot-debugger', '-t', 'dwlink', '-d', 'attiny85'], mock_logger), 0)
        mock_reboot.assert_called_once()
        mock_serve.assert_called_once()
        mock_reboot.return_value = False
        self.assertEqual(startup(['--reboot-debugger', '-t', 'dwlink', '-d', 'attiny85'], mock_logger), 1)
        mock_serve.assert_called_once()                               # not again

    @patch('pyavrocd.main.time.sleep', Mock())
    @patch('pyavrocd.main.time.monotonic', Mock(side_effect=itertools.count()))
    @patch('pyavrocd.main.dwlinkbackend.discover', Mock(return_value=[]))
    @patch('pyavrocd.main.pymcuprog.backend.Backend', Mock(return_value=no_hid_tools()))
    @patch('pyavrocd.main.importlib.metadata.version', Mock(return_value='VERSION'))
    @patch('pyavrocd.main.usb.core.find', Mock(side_effect=NoBackendError("")))
    @patch('pyavrocd.main.platform.system')
    def test_startup_no_libusb(self, mock_system):
        # the EDBG tools do not need libusb; without it, only JTAGICE mkII / AVR Dragon are missed
        for system, hint in (('Darwin', "'brew install libusb'"), ('Linux', "'sudo apt install libusb-1.0-0'")):
            mock_system.return_value = system
            mock_logger = MagicMock()
            self.assertEqual(startup(['-d', 'atmega328p'], mock_logger), 1)
            mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
            mock_logger.critical.assert_called_with('No compatible tool discovered')
            mock_logger.warning.assert_called_with('A JTAGICE mkII or AVR Dragon needs libusb: %s', hint)

    @patch('pyavrocd.main.time.sleep', Mock())
    @patch('pyavrocd.main.time.monotonic', Mock(side_effect=itertools.count()))
    @patch('pyavrocd.main.pymcuprog.backend.Backend', Mock(return_value=no_hid_tools()))
    @patch('pyavrocd.main.platform.system', Mock(return_value='Darwin'))
    @patch('pyavrocd.main.dwlinkbackend.discover', return_value=[])
    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.usb.core.find')
    def test_startup_no_tools(self, mock_find,  mock_version, mock_dwlink):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        mock_find.return_value=[ SimpleNamespace(idVendor=0x3EB, idProduct=0x2139) ]
        self.assertEqual(startup(['-d', 'atmega328p'], mock_logger), 1)
        self.assertEqual(mock_dwlink.call_count,1)
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
        mock_logger.critical.assert_has_calls([call('No compatible tool discovered')])
        mock_logger.warning.assert_not_called()

    @patch('pyavrocd.main.time.sleep', Mock())
    @patch('pyavrocd.main.time.monotonic', Mock(side_effect=itertools.count()))
    @patch('pyavrocd.main.dwlinkbackend.discover')
    @patch('pyavrocd.main.usb.core.find')
    @patch('pyavrocd.main.pymcuprog.backend.Backend', Mock(return_value=no_hid_tools()))
    @patch('pyavrocd.main.platform.system', Mock(return_value='Linux'))
    def test_startup_linux_no_udev(self, mock_find, mock_dwlink):
        mock_find.return_value=[ hid_tool() ]  # libusb lists the Atmel-ICE, hidapi does not
        mock_logger = MagicMock()
        self.assertEqual(startup(['-d', 'atmega328p'], mock_logger), 1)
        mock_logger.critical.assert_has_calls([call("Perhaps you need to install the udev rules first:"),
                                               call("Download https://pyavrocd.io/99-edbg-debuggers.rules,"),
                                               call("review, edit, and install under /etc/udev/rules.d/."),
                                               call("No compatible tool discovered")])
        mock_dwlink.assert_not_called()     # an Arduino on a serial port would be reset for nothing

    @patch('pyavrocd.main.time.sleep', Mock())
    @patch('pyavrocd.main.time.monotonic', Mock(side_effect=itertools.count()))
    @patch('pyavrocd.main.dwlinkbackend.discover', Mock(return_value=[]))
    @patch('pyavrocd.main.usb.core.find', Mock(side_effect=NoBackendError("")))
    @patch('pyavrocd.main.pymcuprog.backend.Backend', Mock(return_value=no_hid_tools()))
    @patch('pyavrocd.main.platform.system', Mock(return_value='Windows'))
    def test_startup_windows_nothing(self):
        mock_logger = MagicMock()
        self.assertEqual(startup(['-d', 'atmega328p'], mock_logger), 1)
        mock_logger.critical.assert_called_with("No compatible tool discovered")
        self.assertIn("WinUSB", mock_logger.warning.call_args_list[0].args[0])
        self.assertIn("Windows on Arm", mock_logger.warning.call_args_list[1].args[0])

    @patch('pyavrocd.main.EdbgBackend', MagicMock())
    @patch('pyavrocd.main.RspServer', MagicMock())
    @patch('pyavrocd.main.dwlinkbackend.discover', return_value=[])
    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.usb.core.find')
    @patch('pyavrocd.main.pymcuprog.backend.Backend')
    def test_startup_with_tool(self, mock_backend, mock_find,  mock_version, mock_dwlink):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        t3 = hid_tool()
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
        t3 = hid_tool()
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
        t3 = hid_tool()
        mock_find.return_value=[ t3 ]
        mock_backend.return_value = MagicMock(connect_to_tool=Mock(side_effect=OSError("other")),
                                                  get_available_hid_tools=MagicMock(return_value=[t3]),
                                                  transport=Mock())
        self.assertEqual(startup(['-d', 'atmega328p', '-v=all'], mock_logger), 1)
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
        mock_logger.critical.assert_has_calls([call('Could not connect to debug probe: %s', 'other')])

    @patch('pyavrocd.main.RspServer', MagicMock())
    @patch('pyavrocd.main.EdbgBackend', MagicMock(reboot_probe=EdbgBackend.reboot_probe))
    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.usb.core.find')
    @patch('pyavrocd.main.pymcuprog.backend.Backend')
    def test_startup_reboot(self, mock_backend, mock_find,  mock_version):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        t3 = hid_tool()
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

    @patch('pyavrocd.main.platform.system', MagicMock(return_value='Linux'))
    @patch('pyavrocd.main.importlib.metadata.version')
    @patch('pyavrocd.main.pymcuprog.backend.Backend')
    @patch('pyavrocd.main.usb.core.find')
    def test_startup_two_tools(self, mock_find, mock_backend, mock_version):
        mock_logger = MagicMock()
        mock_version.return_value='VERSION'
        t1 = hid_tool(0x2140, "PROD1", "S/N01")
        t2 = hid_tool(0x2141, "PROD2", "S/N02")
        t3 = SimpleNamespace(idVendor=0x3EB, idProduct=0x2139)
        t4 = SimpleNamespace(idVendor=0x3EC, idProduct=0x2140)
        mock_find.return_value=(t1, t2, t3, t4)
        mock_backend.return_value = MagicMock(connect_to_tool=Mock(side_effect=pymcuprog.pymcuprog_errors.PymcuprogToolConnectionError("")),get_available_hid_tools=MagicMock(return_value=[t1,t2]))
        self.assertEqual(startup(['-d', 'atmega328p'], mock_logger), 1)
        self.assertEqual(mock_backend.call_count,1)
        mock_logger.info.assert_has_calls([call('This is PyAvrOCD version %s', 'VERSION')])
        mock_logger.critical.assert_has_calls([call('More than one compatible tool! Use -t or -u to select.'),
                                                   call(' Tool: %s, SN: %s', 'PROD1', 'S/N01'),
                                                   call(' Tool: %s, SN: %s', 'PROD2', 'S/N02')])


class TestFindProbe(TestCase):
    """main picks the probe: one on USB (EDBG or JTAGICE mkII / AVR Dragon), else dw-link on a serial port"""

    CLONE = ProbeCandidate('jtagice2', 'JTAGICE mkII', '090000004262')
    DRAGON = ProbeCandidate('dragon', 'AVRDRAGON', '00A200050860')
    ICE = hid_tool()
    ICE_CANDIDATE = ProbeCandidate('atmelice', 'Atmel-ICE CMSIS-DAP', 'J42700018184')
    PORT = ProbeCandidate('dwlink', 'dw-link', '/dev/cu.usbmodem242101')

    def find(self, jtag2_found=(), hid=(), ports=(), cmd=(), intf='debugwire', system='Darwin', usb_bus=()):
        """find_probe with the given probes attached; returns ((abort, probe), logger, sleep)"""
        logger = MagicMock()
        args = options(['-d', 'attiny85'] + list(cmd))
        def hid_tools(serialnumber_substring='', tool_name=None):
            return [t for t in hid if t.serial_number.lower().endswith(serialnumber_substring.lower())
                    and tool_name in (None, EDBG_PRODUCTS[t.product_id])]
        jtag2_discover = jtag2_found if callable(jtag2_found) else \
          lambda t=None: [c for c in jtag2_found if t in (None, c.tool)]
        # one second per call to the clock: the wait for a re-enumerating probe takes no real time
        with patch('pyavrocd.main.jtag2.discover', side_effect=jtag2_discover), \
             patch('pyavrocd.main.pymcuprog.backend.Backend',
                       return_value=MagicMock(get_available_hid_tools=MagicMock(side_effect=hid_tools))), \
             patch('pyavrocd.main.dwlinkbackend.discover', return_value=list(ports)), \
             patch('pyavrocd.main.usb.core.find', return_value=list(usb_bus)), \
             patch('pyavrocd.main.platform.system', return_value=system), \
             patch('pyavrocd.main.time.monotonic', side_effect=itertools.count()), \
             patch('pyavrocd.main.time.sleep') as sleep:
            return find_probe(args, intf, logger), logger, sleep

    def test_one_alone(self):
        for found, hid, probe in (([self.DRAGON], [], self.DRAGON), ([], [self.ICE], self.ICE_CANDIDATE)):
            result, logger, sleep = self.find(found, hid, ports=[self.PORT])
            self.assertEqual(result, (False, probe))      # USB first, the serial port is not looked at
            logger.critical.assert_not_called()
            sleep.assert_not_called()

    def test_ambiguous_across_families(self):
        result, logger, _ = self.find([self.DRAGON], [self.ICE])
        self.assertEqual(result, (True, None))
        logger.critical.assert_has_calls([call("More than one compatible tool! Use -t or -u to select."),
                                          call(" Tool: %s, SN: %s", 'Atmel-ICE CMSIS-DAP', 'J42700018184'),
                                          call(" Tool: %s, SN: %s", 'AVRDRAGON', '00A200050860')])
        self.assertEqual(self.find([self.CLONE, self.DRAGON])[0], (True, None))

    def test_selected_by_tool_and_by_serial(self):
        both = ([self.CLONE, self.DRAGON], [self.ICE])
        self.assertEqual(self.find(*both, cmd=['-t', 'jtagice2'])[0], (False, self.CLONE))
        self.assertEqual(self.find(*both, cmd=['-t', 'atmelice'])[0], (False, self.ICE_CANDIDATE))
        self.assertEqual(self.find(*both, cmd=['-u', '0860'])[0], (False, self.DRAGON))
        self.assertEqual(self.find(*both, cmd=['-u', 'a200050860'])[0], (False, self.DRAGON)) # case does not matter
        self.assertEqual(self.find(*both, cmd=['-u', '18184'])[0], (False, self.ICE_CANDIDATE))
        self.assertEqual(self.find([], [hid_tool(0x2111, 'EDBG CMSIS-DAP', 'ATML1')])[0][1].tool, 'edbg')

    def test_waits_for_reenumeration(self):
        # after avrdude has signed off, the probe is back on the bus only after a few seconds
        attempts = iter([[], [], [self.CLONE]])
        result, _, sleep = self.find(lambda t=None: next(attempts), cmd=['-u', '4262'])
        self.assertEqual(result, (False, self.CLONE))
        self.assertEqual(sleep.call_count, 2)

    def test_nothing_after_the_wait(self):
        result, logger, sleep = self.find(ports=[])
        self.assertEqual(result, (True, None))
        self.assertGreater(sleep.call_count, 0)
        logger.critical.assert_called_with("No compatible tool discovered")
        logger.warning.assert_not_called()

    def test_dwlink_when_nothing_on_usb(self):
        result, _, sleep = self.find(ports=[self.PORT])
        self.assertEqual(result, (False, self.PORT))
        self.assertGreater(sleep.call_count, 0)              # the price of a reliable start after an upload

    def test_no_wait_when_a_serial_port_is_meant(self):
        # -t dwlink, or -u naming the port of dw-link: no mkII or Dragon to wait for
        for cmd in (['-t', 'dwlink'], ['-u', '242101']):
            result, _, sleep = self.find(ports=[self.PORT], cmd=cmd)
            self.assertEqual(result, (False, self.PORT))
            sleep.assert_not_called()

    def test_no_wait_when_an_edbg_tool_is_meant(self):
        result, logger, sleep = self.find([self.DRAGON], ports=[self.PORT], cmd=['-t', 'atmelice'])
        self.assertEqual(result, (True, None))
        sleep.assert_not_called()
        logger.critical.assert_called_with("No compatible tool discovered")

    def test_no_libusb(self):
        def no_libusb(t=None):
            raise NoBackendError("none")
        self.assertEqual(self.find(no_libusb, [self.ICE])[0], (False, self.ICE_CANDIDATE))
        result, logger, _ = self.find(no_libusb, cmd=['-t', 'dragon'])
        self.assertEqual(result, (True, None))
        logger.warning.assert_called_with('A JTAGICE mkII or AVR Dragon needs libusb: %s', "'brew install libusb'")

    def test_linux_without_udev_rules(self):
        # libusb lists the probes, but hidapi leaves the Atmel-ICE out / the Dragon's serial number is unreadable
        for found, bus, cmd in (([], [hid_tool()], []), ([ProbeCandidate('dragon', 'AVRDRAGON', '')], [], []),
                                ([ProbeCandidate('jtagice2', 'JTAGICE mkII', '')], [], ['-t', 'jtagice2'])):
            result, logger, _ = self.find(found, ports=[self.PORT], system='Linux', usb_bus=bus, cmd=cmd)
            self.assertEqual(result, (True, None))
            logger.critical.assert_any_call("Perhaps you need to install the udev rules first:")
            logger.critical.assert_called_with("No compatible tool discovered")
        # with rights: on to dw-link
        self.assertEqual(self.find(ports=[self.PORT], system='Linux')[0], (False, self.PORT))

    def test_not_debugwire(self):
        result, logger, _ = self.find(ports=[self.PORT], intf='updi', system='Windows')
        self.assertEqual(result, (True, None))
        logger.critical.assert_called_with("No compatible tool discovered")
        self.assertIn("WinUSB", logger.warning.call_args_list[0].args[0])
