"""
The test suit for the MonitorCommand class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
import importlib
from unittest import TestCase
from unittest.mock import MagicMock, call
from pyavrocd.monitor import MonitorCommand, monopts
from pyavrocd.main import options
from pyavrocd.errors import FatalError

class TestMonitorCommand(TestCase):

    def setUp(self):
        self.mo = None
        self.moj = None
        self.mockdbg = None

    def set_up(self):
        self.mockdbg = MagicMock()
        self.mockdbg.return_value.get_architecture.return_value = 'avr8'
        self.mo = MonitorCommand('debugwire', options(['-f', 'foo', '-d', 'atmega328p']), "Tool",
                                     self.mockdbg)
        self.mo._arch = 'avr8'
        self.moj = MonitorCommand('jtag', options(['-f', 'foo', '-d', 'atmega128', '--timer', 'freeze']), "Tool",
                                      self.mockdbg)
        self.moj._arch = 'avr8'

    def test_consistency_failure(self):
        self.set_up()
        monopts['bla'] = [1,2,3]
        self.assertRaises(FatalError, MonitorCommand, 'jtag', options([ '-d', 'atmega328p']), "Tool",
                              self.mockdbg)
        monopts.pop('bla')
        temp = monopts['LiveTests']
        del monopts['LiveTests']
        self.assertRaises(FatalError, MonitorCommand, 'jtag', options([ '-d', 'atmega328p']), "Tool",
                              self.mockdbg)
        monopts['LiveTests'] = temp

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

    def test_is_noinitialload(self):
        self.set_up()
        self.mo._only_cache = False
        self.assertEqual(self.mo.is_noinitialload(), self.mo._only_cache)
        self.mo._only_cache = True
        self.assertEqual(self.mo.is_noinitialload(), self.mo._only_cache)

    def test_disable_noinitialload(self):
        self.set_up()
        self.mo._only_cache = True
        self.mo.disable_noinitialload()
        self.assertFalse(self.mo._only_cache)

    def test_is_leaveonexit(self):
        self.set_up()
        self.mo._leaveonexit = False
        self.assertEqual(self.mo.is_leaveonexit(), self.mo._leaveonexit)
        self.mo._leaveonexit = True
        self.assertEqual(self.mo.is_leaveonexit(), self.mo._leaveonexit)

    def test_is_onlyhwbps(self):
        self.set_up()
        self.mo._onlyhwbps = False
        self.assertEqual(self.mo.is_onlyhwbps(), self.mo._onlyhwbps)
        self.mo._onlyhwbps = True
        self.assertEqual(self.mo.is_onlyhwbps(), self.mo._onlyhwbps)

    def test_is_onlyswbps(self):
        self.set_up()
        self.mo._onlyswbps = False
        self.assertEqual(self.mo.is_onlyswbps(), self.mo._onlyswbps)
        self.mo._onlyswbps = True
        self.assertEqual(self.mo.is_onlyswbps(), self.mo._onlyswbps)

    def test_is_cache(self):
        self.set_up()
        self.mo._cache = False
        self.assertEqual(self.mo.is_cache(), self.mo._cache)
        self.mo._cache = True
        self.assertEqual(self.mo.is_cache(), self.mo._cache)

    def test_is_debugger_active(self):
        self.set_up()
        self.mo._debugger_active = False
        self.assertEqual(self.mo.is_debugger_active(), self.mo._debugger_active)
        self.mo._debugger_active = True
        self.assertEqual(self.mo.is_debugger_active(), self.mo._debugger_active)

    def test_set_debug_mode_active(self):
        self.set_up()
        self.assertFalse(self.mo._debugger_active)
        self.assertFalse(self.mo._debugger_activated_once)
        self.mo.set_debug_mode_active(enable=True)
        self.assertTrue(self.mo._debugger_active)
        self.assertTrue(self.mo._debugger_activated_once)
        self.mo.set_debug_mode_active(enable=False)
        self.assertFalse(self.mo._debugger_active)
        self.assertTrue(self.mo._debugger_activated_once)


    def test_is_read_before_write(self):
        self.set_up()
        self.mo._read_before_write = False
        self.assertEqual(self.mo.is_read_before_write(), self.mo._read_before_write)
        self.mo._read_before_write = True
        self.assertEqual(self.mo.is_read_before_write(), self.mo._read_before_write)

    def test_is_noload(self):
        self.set_up()
        self.mo._noload = False
        self.assertEqual(self.mo.is_noload(), self.mo._noload)
        self.mo._noload = True
        self.assertEqual(self.mo.is_noload(), self.mo._noload)

    def test_is_range(self):
        self.set_up()
        self.mo._range = False
        self.assertEqual(self.mo.is_range(), self.mo._range)
        self.mo._range = True
        self.assertEqual(self.mo.is_range(), self.mo._range)

    def test_is_safe(self):
        self.set_up()
        self.mo._safe = False
        self.assertEqual(self.mo.is_safe(), self.mo._safe)
        self.mo._safe = True
        self.assertEqual(self.mo.is_safe(), self.mo._safe)

    def test_is_timersfreeze(self):
        self.set_up()
        self.mo._timersfreeze = False
        self.assertEqual(self.mo.is_timersfreeze(), self.mo._timersfreeze)
        self.mo._timersfreeze = True
        self.assertEqual(self.mo.is_timersfreeze(), self.mo._timersfreeze)

    def test_is_verify(self):
        self.set_up()
        self.mo._verify = False
        self.assertEqual(self.mo.is_verify(), self.mo._verify)
        self.mo._verify = True
        self.assertEqual(self.mo.is_verify(), self.mo._verify)

    def test_is_old_exec(self):
        self.set_up()
        self.mo._old_exec = False
        self.assertEqual(self.mo.is_old_exec(), self.mo._old_exec)
        self.mo._old_exec = True
        self.assertEqual(self.mo.is_old_exec(), self.mo._old_exec)

    def test_is_power(self):
        self.set_up()
        self.mo._power = False
        self.assertEqual(self.mo.is_power(), self.mo._power)
        self.mo._power = True
        self.assertEqual(self.mo.is_power(), self.mo._power)

    def test_is_erase_before_load(self):
        self.set_up()
        self.mo._erase_before_load = False
        self.assertEqual(self.mo.is_erase_before_load(), self.mo._erase_before_load)
        self.mo._erase_before_load = True
        self.assertEqual(self.mo.is_erase_before_load(), self.mo._erase_before_load)


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


    def test_dispatch_breakpoints_m128(self):
        self.set_up()
        self.assertEqual(self.moj.dispatch(['break', 'soft']),
                                 ("", "Breakpoint mode cannot be changed on this MCU"))

    def test_dispatch_cache(self):
        self.set_up()
        self.mo._cache = False
        self.assertEqual(self.mo.dispatch(["caching", "enable"]), ("", "Flash memory will be cached"))
        self.assertEqual(self.mo._cache, True)
        self.mo._cache = True
        self.assertEqual(self.mo.dispatch(["caching"]), ("", "Flash memory will be cached"))
        self.assertEqual(self.mo.dispatch(["caching", "dis"]), ("", "Flash memory will not be cached"))
        self.assertEqual(self.mo._cache, False)
        self.assertEqual(self.mo.dispatch(["ca"]), ("", "Flash memory will not be cached"))
        self.assertEqual(self.mo.dispatch(["ca", "X"]), ("", "Unknown argument in 'monitor' command"))


    def test_dispatch_debugWIRE(self):
        self.set_up()
        self.mo._debugger_active = False
        self.assertEqual(self.mo.dispatch(["de"]), ("", "debugWIRE is disabled"))
        self.mo._debugger_active = True
        self.assertEqual(self.mo.dispatch(["debugwire"]), ("", "debugWIRE is enabled"))
        self.mo._debugger_active = False
        self.assertEqual(self.mo.dispatch(["debug", "e"]), ("dwon", "debugWIRE is enabled"))
        self.assertFalse(self.mo._debugger_active) # The enable command does NOT change the value of the state var!
        self.mo._debugger_active = True
        self.assertEqual(self.mo.dispatch(["debug", "e"]), ("reset", "debugWIRE is enabled"))
        self.assertTrue(self.mo._debugger_active)
        self.mo._debugger_activated_once = True
        self.assertEqual(self.mo.dispatch(["debug", "dis"]), ("dwoff", "debugWIRE is disabled"))
        self.assertFalse(self.mo._debugger_active)
        self.assertEqual(self.mo.dispatch(["debug", "dis"]), ("", "debugWIRE is disabled"))

        self.assertEqual(self.mo.dispatch(["debug", "enable"]),
                             ("", "Cannot reactivate debugWIRE\nYou have to exit and restart the debugger"))
        self.assertFalse(self.mo._debugger_active)
        self.assertTrue(self.mo._debugger_activated_once)
        self.assertEqual(self.mo.dispatch(['debugwire', 'bla']), ("", "Unknown argument in 'monitor' command"))


    def test_dispatch_debugWIRE_other(self):
        self.set_up()
        self.mo._iface = "other"
        self.assertEqual(self.mo.dispatch(['debugwire', 'e']), ("reset", "This is not a debugWIRE target"))
        self.assertEqual(self.mo.dispatch(['debugwire']), ("", "This is not a debugWIRE target"))
        self.assertEqual(self.mo.dispatch(['debugwire', 'bla']), ("", "Unknown argument in 'monitor' command"))


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
        self.assertEqual(self.mo.dispatch(['atexit']), ("", "MCU will stay in debug mode on exit"))
        self.assertEqual(self.mo.dispatch(['at', 'leave']), ("",  "MCU will leave debug mode on exit"))
        self.assertTrue(self.mo._leaveonexit)
        self.assertEqual(self.mo.dispatch(['a', 'stay']), ("",   "MCU will stay in debug mode on exit"))
        self.assertFalse(self.mo._leaveonexit)
        self.assertEqual(self.mo.dispatch(['atexit', 'bla']), ("", "Unknown argument in 'monitor' command"))

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
        self.assertEqual(self.mo.dispatch(['era', 'bla']), ("", "Unknown argument in 'monitor' command"))


    def test_dispatch_load(self):
        self.set_up()
        self.assertTrue(self.mo._read_before_write)
        self.assertFalse(self.mo._only_cache)
        self.assertEqual(self.mo.dispatch(['load']), ("", "Reading before writing when loading"))
        self.assertEqual(self.mo.dispatch(['load', 'writeonly']),  ("", "No reading before writing when loading"))
        self.assertFalse(self.mo._read_before_write)
        self.assertEqual(self.mo.dispatch(['load', 'read']),  ("", "Reading before writing when loading"))
        self.assertTrue(self.mo._read_before_write)
        self.assertEqual(self.mo.dispatch(['load', 'noinitialload']),  ("", "Only caching when loading"))
        self.assertTrue(self.mo._only_cache)
        self.assertEqual(self.mo.dispatch(['load', 'bla']), ("", "Unknown argument in 'monitor' command"))

    def test_dispatch_noload(self):
        self.set_up()
        self.assertFalse(self.mo._noload)
        self.assertEqual(self.mo.dispatch(['onlywhenloaded', 'dis']), ("", "Execution is always possible"))
        self.assertTrue(self.mo._noload)
        self.assertEqual(self.mo.dispatch(['only', 'enable']), ("",  "Execution is only possible after a previous load command"))
        self.assertFalse(self.mo._noload)
        self.assertEqual(self.mo.dispatch(['only', 'bla']), ("", "Unknown argument in 'monitor' command"))

    def test_dispatch_range(self):
        self.set_up()
        self.assertTrue(self.mo._range)
        self.assertEqual(self.mo.dispatch(['rangestepping', 'disable']), ("", "Range stepping is disabled"))
        self.assertFalse(self.mo._range)
        self.assertEqual(self.mo.dispatch(['range']), ("", "Range stepping is disabled"))
        self.assertEqual(self.mo.dispatch(['rangestepping', 'enable']), ("", "Range stepping is enabled"))
        self.assertTrue(self.mo._range)
        self.assertEqual(self.mo.dispatch(['range', 'bla']), ("", "Unknown argument in 'monitor' command"))


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
        self.assertEqual(self.mo.dispatch(['single', 'bla']), ("", "Unknown argument in 'monitor' command"))


    def test_dispatch_timers(self):
        self.set_up()
        self.assertFalse(self.mo._timersfreeze)
        self.assertEqual(self.mo.dispatch(['timers', 'run']), ("1", "MCU reset\nTimers will run when execution is stopped"))
        self.assertFalse(self.mo._timersfreeze)
        self.assertEqual(self.mo.dispatch(['timers', 'freeze']), ("0", "MCU reset\nTimers are frozen when execution is stopped"))
        self.assertTrue(self.mo._timersfreeze)
        self.assertEqual(self.mo.dispatch(['timers']), ("", "Timers are frozen when execution is stopped"))
        self.assertEqual(self.mo.dispatch(['timers', 'bla']), ("", "Unknown argument in 'monitor' command"))


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
        self.assertTrue(self.mo._old_exec)

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
        self.assertEqual(self.mo.dispatch(['Target', 'bla']), ("", "Unknown argument in 'monitor' command"))

    def test_dispatch_live_tests(self):
        self.set_up()
        self.assertEqual(self.mo.dispatch(['LiveTests']),
                             ("", "Cannot run tests because debugging is not enabled"))
        self.mo._debugger_active = True
        self.assertEqual(self.mo.dispatch(['LiveTests']),
                             ("live_tests", "Tests done"))

    def test_dispatch_breakpoints_internal_confusion(self):
        self.set_up()
        self.mo._onlyhwbps = True
        self.mo._onlyswbps = True
        self.assertEqual(self.mo.dispatch(['breakpoints']),
                             ("", "Internal confusion: No breakpoints are allowed"))

    def test_dispatch_breakpoints_fixed_hardware_only(self):
        self.set_up()
        self.assertTrue(self.moj._onlyhwbps)
        self.assertTrue(self.moj._bpfixed)
        self.assertEqual(self.moj.dispatch(['breakpoints']),
                             ("", "On this MCU, only hardware breakpoints are allowed"))

    def test_dispatch_disconnect(self):
        self.set_up()
        self.assertEqual(self.mo.dispatch(['disconnect']), ("", "No connection to debug tool"))
        self.mo._debugger_active = True
        self.assertEqual(self.mo.dispatch(['disconnect']), ("disconnect", "Disconnected from debug tool"))

    def test_dispatch_exit(self):
        self.set_up()
        self.assertEqual(self.mo.dispatch(['exit']), ("exit", "Exiting from GDB server"))

    def test_dispatch_test(self):
        self.set_up()
        self.assertEqual(self.mo.dispatch(['Test']),
                             ("", "Cannot execute test because debugging is not enabled"))
        self.mo._debugger_active = True
        self.assertEqual(self.mo.dispatch(['Test']), ("test", "Tests done"))

    def test_dispatch_timers_on_avr8x(self):
        self.set_up()
        self.mo._arch = 'avr8x'
        self.assertEqual(self.mo.dispatch(['timers']),
                             ("", "On (U)PDI targets, timers are frozen when execution is stopped"))
        self.assertEqual(self.mo.dispatch(['timers', 'run']),
                             ("", "On (U)PDI targets, timers are frozen when execution is stopped"))


SVD = { 'device' : { 'peripherals' : { 'peripheral' : [
    { 'name' : 'TCA0', 'baseAddress' : 0x0A00, 'registers' : { 'register' : [
        { 'name' : 'CTRLA', 'addressOffset' : 0x00, 'size' : 8, 'description' : 'Control A',
          'fields' : { 'field' : [
              { 'name' : 'ENABLE', 'bitRange' : '[0:0]', 'description' : 'Module Enable',
                'enumeratedValues' : { 'enumeratedValue' : [
                    { 'value' : '0x0', 'name' : 'DISABLED', 'description' : 'off' },
                    { 'value' : '0x1', 'name' : 'ENABLED', 'description' : 'on' } ] } },
              { 'name' : 'CLKSEL', 'bitRange' : '[3:1]', 'description' : 'Clock Selection' } ] } },
        { 'name' : 'CNT', 'addressOffset' : 0x20, 'size' : 16, 'description' : 'Count' } ] } },
    { 'name' : 'TCB0', 'baseAddress' : 0x0B00, 'registers' : { 'register' : [
        { 'name' : 'CTRLA', 'addressOffset' : 0x00, 'size' : 8, 'description' : 'Control A',
          'fields' : { 'field' : [
              { 'name' : 'ENABLE', 'bitRange' : '[0:0]', 'description' : 'Module Enable' } ] } } ] } } ] } } }


class TestMonitorIORegister(TestCase):
    """
    Tests for the 'monitor ioregister' command, i.e., for reading and writing
    I/O registers and bitfields described by the SVD file of the target.
    """

    def setUp(self):
        self.mockdbg = MagicMock()
        self.mockdbg.device_info = { 'svd' : SVD }
        self.mockdbg.get_devicename.return_value = 'atmega328p'
        self.mockdbg.get_architecture.return_value = 'avr8'
        self.mockdbg.masked_registers = []
        self.mo = MonitorCommand('debugwire', options(['-f', 'foo', '-d', 'atmega328p']), "Tool",
                                     self.mockdbg)
        self.mo._arch = 'avr8'

    # --- reading ---------------------------------------------------------

    def test_ioreg_without_svd(self):
        self.mockdbg.device_info = {}
        self.assertEqual(self.mo.dispatch(['ioreg', 'TCA0.CNT']),
                             ("", "No SVD information for 'atmega328p'"))

    def test_ioreg_wrong_number_of_arguments(self):
        self.assertEqual(self.mo.dispatch(['ioreg']),
                             ("", "The 'ioregister' command requires 1 or 2 arguments"))
        self.assertEqual(self.mo.dispatch(['ioreg', 'TCA0.CNT', '1', '2']),
                             ("", "The 'ioregister' command requires 1 or 2 arguments"))

    def test_ioreg_read_unique_register_without_fields(self):
        self.mockdbg.sram_masked_read.return_value = bytes([0x34, 0x12])
        self.assertEqual(self.mo.dispatch(['ioreg', 'tca0.cnt']),
                             ("", "TCA0.CNT (@0xA20, 16-bits) = 0x1234, 0b1001000110100, 4660 (Count)"))
        self.mockdbg.sram_masked_read.assert_called_with(0x0A20, 2)

    def test_ioreg_read_ambigious_register(self):
        self.mockdbg.sram_masked_read.return_value = bytes([0x03])
        self.assertEqual(self.mo.dispatch(['ioreg', 'CTRLA']),
                             ("", "TCA0.CTRLA (@0xA00, 8-bits) = 0x3, 0b11, 3 (Control A)\n" +
                                  "TCB0.CTRLA (@0xB00, 8-bits) = 0x3, 0b11, 3 (Control A)"))

    def test_ioreg_read_unique_register_with_fields(self):
        self.mockdbg.sram_masked_read.return_value = bytes([0x03])
        self.assertEqual(self.mo.dispatch(['ioreg', 'TCA0.CTRLA']),
                             ("", "TCA0.CTRLA (@0xA00, 8-bits) = 0x3, 0b11, 3 (Control A)\n" +
                                  "TCA0.CTRLA.ENABLE (@0xA00[0:0]) = 0x1, 0b1, 1 (Module Enable)\n" +
                                  "TCA0.CTRLA.CLKSEL (@0xA00[3:1]) = 0x1, 0b1, 1 (Clock Selection)"))

    def test_ioreg_read_unique_field_with_enumerated_values(self):
        self.mockdbg.sram_masked_read.return_value = bytes([0x03])
        self.assertEqual(self.mo.dispatch(['ioreg', 'TCA0.CTRLA.ENABLE']),
                             ("", "TCA0.CTRLA.ENABLE (@0xA00[0:0]) = 0x1, 0b1, 1 (Module Enable)\n" +
                                  "   0x0: DISABLED (off)\n" +
                                  "   0x1: ENABLED (on)"))

    def test_ioreg_read_ambigious_field(self):
        self.mockdbg.sram_masked_read.return_value = bytes([0x03])
        self.assertEqual(self.mo.dispatch(['ioreg', 'ENABLE']),
                             ("", "TCA0.CTRLA.ENABLE (@0xA00[0:0]) = 0x1, 0b1, 1 (Module Enable)\n" +
                                  "TCB0.CTRLA.ENABLE (@0xB00[0:0]) = 0x1, 0b1, 1 (Module Enable)"))

    def test_ioreg_read_empty_expression(self):
        self.assertEqual(self.mo.dispatch(['ioreg', '']),
                             ("", "No matching I/O registers or fields identified"))

    def test_ioreg_read_no_match(self):
        self.assertEqual(self.mo.dispatch(['ioreg', 'FOO']),
                             ("", "No matching I/O registers or fields identified"))

    # --- writing ---------------------------------------------------------

    def test_ioreg_write_malformed_value(self):
        self.assertEqual(self.mo.dispatch(['ioreg', 'TCA0.CNT', 'xyz']),
                             ("", "Second argument must be a well-formed integer literal"))

    def test_ioreg_write_ambigious_register(self):
        self.assertEqual(self.mo.dispatch(['ioreg', 'CTRLA', '1']),
                             ("", "No unique I/O register addressed"))

    def test_ioreg_write_register(self):
        self.mockdbg.sram_masked_read.side_effect = [ bytes([0x00, 0x00]), bytes([0x34, 0x12]) ]
        self.assertEqual(self.mo.dispatch(['ioreg', 'TCA0.CNT', '0x1234']),
                             ("", "TCA0.CNT = 4660 (old value was: 0)"))
        self.assertEqual(self.mockdbg.sram_masked_write.mock_calls,
                             [ call(0x0A21, b'\x12'), call(0x0A20, b'\x34') ])

    def test_ioreg_write_register_value_too_large(self):
        self.mockdbg.sram_masked_read.return_value = bytes([0x00, 0x00])
        self.assertEqual(self.mo.dispatch(['ioreg', 'TCA0.CNT', '0x12345']),
                             ("", "Value out of range, cannot be stored"))
        self.mockdbg.sram_masked_write.assert_not_called()

    def test_ioreg_write_register_read_protected(self):
        self.mockdbg.masked_registers = [ 0x0A20 ]
        self.mockdbg.sram_masked_read.return_value = bytes([0x00, 0x00])
        self.assertEqual(self.mo.dispatch(['ioreg', 'TCA0.CNT', '0x1234']),
                             ("", "TCA0.CNT = 4660 (old value was: 0) register is read-protected"))

    def test_ioreg_write_register_unsuccessful(self):
        self.mockdbg.sram_masked_read.return_value = bytes([0x00, 0x00])
        self.assertEqual(self.mo.dispatch(['ioreg', 'TCA0.CNT', '0x1234']),
                             ("", "TCA0.CNT = 4660 (old value was: 0) was unsuccessful"))

    def test_ioreg_write_ambigious_field(self):
        self.assertEqual(self.mo.dispatch(['ioreg', 'ENABLE', '1']),
                             ("", "No unique I/O register field addressed"))

    def test_ioreg_write_field(self):
        self.mockdbg.sram_masked_read.side_effect = [ bytes([0x01]), bytes([0x07]) ]
        self.assertEqual(self.mo.dispatch(['ioreg', 'TCA0.CTRLA.CLKSEL', '3']),
                             ("", "TCA0.CTRLA.CLKSEL = 3 (old value was: 0)"))
        self.assertEqual(self.mockdbg.sram_masked_write.mock_calls, [ call(0x0A00, b'\x07') ])

    def test_ioreg_write_field_value_too_large(self):
        self.mockdbg.sram_masked_read.return_value = bytes([0x01])
        self.assertEqual(self.mo.dispatch(['ioreg', 'TCA0.CTRLA.CLKSEL', '8']),
                             ("", "Value out of range, cannot be stored"))
        self.mockdbg.sram_masked_write.assert_not_called()

    def test_ioreg_write_field_read_protected(self):
        self.mockdbg.masked_registers = [ 0x0A00 ]
        self.mockdbg.sram_masked_read.return_value = bytes([0x01])
        self.assertEqual(self.mo.dispatch(['ioreg', 'TCA0.CTRLA.CLKSEL', '3']),
                             ("", "TCA0.CTRLA.CLKSEL = 3 (old value was: 0) register is read-protected"))

    def test_ioreg_write_field_unsuccessful(self):
        self.mockdbg.sram_masked_read.return_value = bytes([0x01])
        self.assertEqual(self.mo.dispatch(['ioreg', 'TCA0.CTRLA.CLKSEL', '3']),
                             ("", "TCA0.CTRLA.CLKSEL = 3 (old value was: 0) was unsuccessful"))

    def test_ioreg_write_no_match(self):
        self.assertEqual(self.mo.dispatch(['ioreg', 'FOO', '1']),
                             ("", "No matching I/O register or field"))

    def test_sram_write16bitreg_on_modern_mcus(self):
        self.mockdbg.get_architecture.return_value = 'avr8x'
        self.mo._sram_write16bitreg(0x0A20, b'\x34\x12')   # low, high, low
        self.assertEqual(self.mockdbg.sram_masked_write.mock_calls,
                             [ call(0x0A20, b'\x34'), call(0x0A21, b'\x12'),
                                   call(0x0A20, b'\x34') ])

    def test_sram_write16bitreg_single_byte(self):
        self.mo._sram_write16bitreg(0x0A00, b'\x07')
        self.assertEqual(self.mockdbg.sram_masked_write.mock_calls, [ call(0x0A00, b'\x07') ])
