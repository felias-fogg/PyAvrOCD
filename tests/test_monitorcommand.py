"""
The test suit for the MonitorCommand class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring
import importlib
from unittest import TestCase
from pyavrocd.monitor import MonitorCommand
from pyavrocd.main import options


class TestMonitorCommand(TestCase):

    def setUp(self):
        self.mo = None
        self.moj = None

    def set_up(self):
        self.mo = MonitorCommand('debugwire', options(['-f', 'foo', '-d', 'atmega328p']))
        self.moj = MonitorCommand('jtag', options(['-f', 'foo', '-d', 'atmega128', '--timer', 'freeze']))

    def test_defaults_atmega128(self):
        self.set_up()
        self.assertTrue(self.moj._onlyhwbps)
        self.assertFalse(self.moj._onlyswbps)
        self.assertTrue(self.moj._bpfixed)
        self.assertTrue(self.moj._timersfreeze)
        self.assertTrue(self.moj._erase_before_load)
        self.assertFalse(self.moj._read_before_write)

    def test_defaults_atmega328p(self):
        self.set_up()
        self.assertFalse(self.mo._onlyhwbps)
        self.assertFalse(self.mo._onlyswbps)
        self.assertFalse(self.mo._bpfixed)
        self.assertFalse(self.mo._timersfreeze)
        self.assertFalse(self.mo._erase_before_load)
        self.assertTrue(self.mo._read_before_write)

    def test_dispatch_ambigious(self):
        self.set_up()
        self.assertEqual(self.mo.dispatch(["ver"]), ("", "Ambiguous 'monitor' command string"))

    def test_dispatch_unknown(self):
        self.set_up()
        self.assertEqual(self.mo.dispatch(["XXX"]), ("", "Unknown 'monitor' command"))

    def test_dispatch_breakpoints(self):
        self.set_up()
        self.mo._onlyhwbps = False
        self.mo._onlyswbps = False
        self.assertEqual(self.mo.dispatch(["break"]), ("", "All breakpoints are allowed"))
        self.mo._onlyhwbps = True
        self.mo._onlyswbps = False
        self.assertEqual(self.mo.dispatch(["break"]), ("", "Only hardware breakpoints"))
        self.mo._onlyhwbps = False
        self.mo._onlyswbps = True
        self.assertEqual(self.mo.dispatch(["break"]), ("", "Only software breakpoints"))
        self.mo._onlyhwbps = True
        self.mo._onlyswbps = True
        self.assertEqual(self.mo.dispatch(["break"]), ("", "Internal confusion: No breakpoints are allowed"))
        self.assertEqual(self.mo.dispatch(["break", "all"]), ("", "All breakpoints are allowed"))
        self.assertEqual(self.mo._onlyhwbps, False)
        self.assertEqual(self.mo._onlyswbps, False)
        self.assertEqual(self.mo.dispatch(["break", "hardware"]), ("", "Only hardware breakpoints"))
        self.assertEqual(self.mo._onlyhwbps, True)
        self.assertEqual(self.mo._onlyswbps, False)
        self.assertEqual(self.mo.dispatch(["break", "software"]), ("", "Only software breakpoints"))
        self.assertEqual(self.mo._onlyhwbps, False)
        self.assertEqual(self.mo._onlyswbps, True)
        self.assertEqual(self.mo.dispatch(["break", "X"]), ("", "Unknown argument in 'monitor' command"))
        self.mo._onlyhwbps = False
        self.mo._onlyswbps = False


    def test_dispatch_Cache(self):
        self.set_up()
        self.mo._cache = False
        self.assertEqual(self.mo.dispatch(["caching", "enable"]), ("", "Flash memory will be cached"))
        self.assertEqual(self.mo._cache, True)
        self.mo._cache = True
        self.assertEqual(self.mo.dispatch(["caching"]), ("", "Flash memory will be cached"))
        self.assertEqual(self.mo.dispatch(["caching", "dis"]), ("", "Flash memory will not be cached"))
        self.assertEqual(self.mo._cache, False)
        self.assertEqual(self.mo.dispatch(["ca"]), ("", "Flash memory will not be cached"))

    def test_dispatch_debugWIRE(self):
        self.set_up()
        self.mo._debugger_active = False
        self.assertEqual(self.mo.dispatch(["d"]), ("", "debugWIRE is disabled"))
        self.mo._debugger_active = True
        self.assertEqual(self.mo.dispatch(["debugwire"]), ("", "debugWIRE is enabled"))
        self.mo._debugger_active = False
        self.assertEqual(self.mo.dispatch(["debug", "e"]), ("dwon", "debugWIRE is enabled"))
        self.assertFalse(self.mo._debugger_active) # The enable command does NOT change the value of the state var!
        self.mo._debugger_active = True
        self.assertEqual(self.mo.dispatch(["debug", "dis"]), ("dwoff", "debugWIRE is disabled"))
        self.assertFalse(self.mo._debugger_active)
        self.mo._debugger_activated_once = True
        self.assertEqual(self.mo.dispatch(["debug", "enable"]),
                             ("", "Cannot reactivate debugWIRE\nYou have to exit and restart the debugger"))
        self.assertFalse(self.mo._debugger_active)
        self.assertTrue(self.mo._debugger_activated_once)

    def test_dispatch_flashVerify(self):
        self.set_up()
        self.assertTrue(self.mo._verify)
        self.assertEqual(self.mo.dispatch(['veri']), ("", "Verifying flash after load"))
        self.assertEqual(self.mo.dispatch(['verify', 'disable']), ("", "Load operations are not verified"))
        self.assertFalse(self.mo._verify)
        self.assertEqual(self.mo.dispatch(['veri', 'e']), ("", "Verifying flash after load"))
        self.assertTrue(self.mo._verify)
        self.assertEqual(self.mo.dispatch(['veri', 'ex']), ("", "Unknown argument in 'monitor' command"))
        self.assertEqual(self.mo.dispatch(['ver']), ("", "Ambiguous 'monitor' command string"))


    def test_dispatch_help(self):
        self.set_up()
        self.assertTrue(len(self.mo.dispatch(['help'])[1]) > 1000)
        self.assertTrue(len(self.mo.dispatch([])[1]) > 1000)

    def test_dispatch_info(self):
        self.set_up()
        try:
            importlib.metadata.version("pyavrocd")
        except importlib.metadata.PackageNotFoundError:
            return
        self.assertTrue(len(self.mo.dispatch(['info'])[1]) > 50)
        self.assertEqual(self.mo.dispatch(['info'])[0], 'info')

    def test_dispatch_atexit(self):
        self.set_up()
        self.assertFalse(self.mo._leaveonexit)
        self.assertEqual(self.mo.dispatch(['atexit']), ("", "MCU will stay in debugWIRE mode on exit"))
        self.assertEqual(self.mo.dispatch(['at', 'leave']), ("",  "MCU will leave debugWIRE mode on exit"))
        self.assertTrue(self.mo._leaveonexit)
        self.assertEqual(self.mo.dispatch(['a', 'stay']), ("",   "MCU will stay in debugWIRE mode on exit"))
        self.assertFalse(self.mo._leaveonexit)

    def test_dispatch_erase_before_load_dw(self):
        self.set_up()
        self.assertFalse(self.mo._erase_before_load)
        self.assertEqual(self.mo.dispatch(['erase']),
                         ("", "On debugWIRE targets, flash memory cannot be erased before loading executable"))

    def test_dispatch_erase_before_load_jtag(self):
        self.set_up()
        self.mo._iface = 'jtag'
        self.mo.set_default_state()
        self.assertTrue(self.mo._erase_before_load)
        self.assertEqual(self.mo.dispatch(['erase']),
                         ("", "Flash memory will be erased before loading executable"))
        self.assertEqual(self.mo.dispatch(['erase', 'disable']),
                         ("", "Flash memory will not be erased before loading executable"))
        self.assertFalse(self.mo._erase_before_load)
        self.assertEqual(self.mo.dispatch(['era', 'e']),
                         ("", "Flash memory will be erased before loading executable"))
        self.assertTrue(self.mo._erase_before_load)

    def test_dispatch_load(self):
        self.set_up()
        self.assertTrue(self.mo._read_before_write)
        self.assertEqual(self.mo.dispatch(['load']), ("", "Reading before writing when loading"))
        self.assertEqual(self.mo.dispatch(['load', 'writeonly']),  ("", "No reading before writing when loading"))
        self.assertFalse(self.mo._read_before_write)
        self.assertEqual(self.mo.dispatch(['load', 'read']),  ("", "Reading before writing when loading"))
        self.assertTrue(self.mo._read_before_write)

    def test_dispatch_noload(self):
        self.set_up()
        self.assertFalse(self.mo._noload)
        self.assertEqual(self.mo.dispatch(['onlywhenloaded', 'dis']), ("", "Execution is always possible"))
        self.assertTrue(self.mo._noload)
        self.assertEqual(self.mo.dispatch(['only', 'enable']), ("",  "Execution is only possible after a previous load command"))
        self.assertFalse(self.mo._noload)

    def test_dispatch_range(self):
        self.set_up()
        self.assertTrue(self.mo._range)
        self.assertEqual(self.mo.dispatch(['rangestepping', 'disable']), ("", "Range stepping is disabled"))
        self.assertFalse(self.mo._range)
        self.assertEqual(self.mo.dispatch(['range']), ("", "Range stepping is disabled"))
        self.assertEqual(self.mo.dispatch(['rangestepping', 'enable']), ("", "Range stepping is enabled"))
        self.assertTrue(self.mo._range)


    def test_dispatch_reset(self):
        self.set_up()
        self.mo._debugger_active = False
        self.assertEqual(self.mo.dispatch(['reset', 'halt']), ("","Debugger is not enabled"))
        self.mo._debugger_active = True
        self.assertEqual(self.mo.dispatch(['res']), ("reset", "MCU has been reset"))

    def test_dispatch_singlestep(self):
        self.set_up()
        self.assertTrue(self.mo._safe)
        self.assertEqual(self.mo.dispatch(['singlestep', 'interruptible']), ("", "Single-stepping is interruptible"))
        self.assertFalse(self.mo._safe)
        self.assertEqual(self.mo.dispatch(['singlestep']), ("", "Single-stepping is interruptible"))
        self.assertEqual(self.mo.dispatch(['s', 's']), ("", "Single-stepping is interrupt-safe"))
        self.assertTrue(self.mo._safe)

    def test_dispatch_timers(self):
        self.set_up()
        self.assertFalse(self.mo._timersfreeze)
        self.assertEqual(self.mo.dispatch(['timers', 'run']), (1, "Timers will run when execution is stopped"))
        self.assertFalse(self.mo._timersfreeze)
        self.assertEqual(self.mo.dispatch(['timers', 'freeze']), (0, "Timers are frozen when execution is stopped"))
        self.assertTrue(self.mo._timersfreeze)
        self.assertEqual(self.mo.dispatch(['timers']), (0, "Timers are frozen when execution is stopped"))

    def test_dispatch_version(self):
        self.set_up()
        try:
            importlib.metadata.version("pyavrocd")
        except importlib.metadata.PackageNotFoundError:
            return
        self.assertEqual(self.mo.dispatch(['version']), ("", "PyAvrOCD version {}".format(importlib.metadata.version("pyavrocd"))))

    def test_dispatch_oldExec_ok(self):
        self.set_up()
        self.assertEqual(self.mo.dispatch(['OldExecution']), ("", "Old execution mode"))

    def test_dispatch_oldExec_no_abbrev(self):
        self.set_up()
        self.assertEqual(self.mo.dispatch(['OldExec']), ("", "Unknown 'monitor' command"))

    def test_dispatch_target(self):
        self.set_up()
        self.assertEqual(self.mo.dispatch(['Target']), ("", "Target power is on"))
        self.assertEqual(self.mo.dispatch(['Target', 'on']), ("power on", "Target power on"))
        self.assertEqual(self.mo.dispatch(['Target', 'off']), ("power off", "Target power off"))
        self.assertEqual(self.mo.dispatch(['Target']), ("", "Target power is off"))
        self.assertEqual(self.mo.dispatch(['Target', 'query']), ("power query", "Target query"))


