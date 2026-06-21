"""
This module implements the 'monitor' command
"""
from collections.abc import Callable
from typing import Any

# wildcard matching
import fnmatch

# args, logging
import importlib.metadata
import logging
import argparse

# error exceptions
from pyavrocd.errors import FatalError
from pyavrocd.xavrdebugger import XAvrDebugger


# This is a list of monitor commands, of which many also be used as command line options
# Key: option/monitor command name
# 1st entry is type: 'cli' means command line option, 'full' needs full name as monitor command
# 2nd entry: default value
# 3rd entry: possible option values, '*' means don't care
monopts: dict[str, tuple[ str | None, str | None, list [ str ] ] ] \
        = { 'atexit'          : ('cli', None, ['stay', 'leave']),
            'breakpoints'     : ('cli', 'all', ['all', 'software', 'hardware']),
            'caching'         : ('cli', 'enable', ['enable', 'disable']),
            'debugwire'       : ('cli', None, ['enable', 'disable']),
            'erasebeforeload' : ('cli', None, ['enable', 'disable']),
            'help'            : (None, None, []),
            'info'            : (None, None, []),
            'ioregister'      : (None, None, ['*']),
            'load'            : ('cli', None, ['readbeforewrite', 'writeonly', 'noinitialload']),
            'onlywhenloaded'  : ('cli', None, ['enable', 'disable']),
            'rangestepping'   : ('cli', 'enable', ['enable', 'disable']),
            'reset'           : (None, None, ['*']),
            'singlestep'      : ('cli', 'safe', ['safe', 'interruptible']),
            'timers'          : ('cli', 'run', ['run', 'freeze']),
            'verify'          : ('cli', 'enable', ['enable', 'disable']),
            'version'         : (None, None, []),
            'OldExecution'    : ('full', None, []),
            'Target'          : ('full', None, ['on', 'off', 'query']),
            'LiveTests'       : ('full', None, []),
            'Test'            : ('full', None, []) }

class MonitorCommand():
    """
    This class implements all the monitor commands
    It manages state variables, gives responses and selects
    the right action. The return value of the dispatch method is
    a pair consisting of an action identifier and the string to be displayed.
    """
    def __init__(self, iface : str, args : argparse.Namespace, toolname : str,
                     dbg : XAvrDebugger) -> None:
        self._iface : str = iface
        self._debugger_active : bool = False
        self._toolname : str = toolname
        self._arch : str = dbg.get_architecture()
        self._dbg = dbg
        self._debugger_activated_once : bool = False
        self.logger : logging.Logger = logging.getLogger('pyavrocd.monitor')
        # state variables (will be set by set_default_values)
        self._leaveonexit : bool = False # leave debugging mode on exit
        self._onlyhwbps : bool = False # only hardware breakpoints permitted
        self._onlyswbps : bool = False # only software breakpoints permitted
        self._bpfixed : bool = False # It is possible to change
        self._cache : bool  = False # cache executable and use the cache instead of the MCU's flash
        self._erase_before_load : bool = False  # erase flash memory before load
        self._read_before_write : bool = False # read before write
        self._only_cache : bool = False # do not flash while loading
        self._noload : bool = False # when true, one may start execution even without a previous load
        self._range : bool = False # range-stepping is allowed
        self._safe : bool = False # safe single-stepping
        self._timersfreeze : bool = False # freeze timers when execution is stopped
        self._verify : bool = False # verify flash after load
        self._power : bool = False # power state
        self._old_exec : bool = False # use old-style execution (only for tests needed)
        self._args : argparse.Namespace = args # needed to set initial monitor option values

        # The jump table (should have the same set of keys as monopts)
        self.jumptable : dict[ str, Callable[ [ int | list[ str ] ], tuple[ str, str ] ] ] = {
            'atexit'          : self._mon_atexit,
            'breakpoints'     : self._mon_breakpoints,
            'caching'         : self._mon_cache,
            'debugwire'       : self._mon_debugwire,
            'erasebeforeload' : self._mon_erase_before_load,
            'help'            : self._mon_help,
            'info'            : self._mon_info,
            'ioregister'      : self._mon_ioregister,
            'load'            : self._mon_load,
            'onlywhenloaded'  : self._mon_noload,
            'rangestepping'   : self._mon_range_stepping,
            'reset'           : self._mon_reset,
            'singlestep'      : self._mon_singlestep,
            'timers'          : self._mon_timers,
            'verify'          : self._mon_flash_verify,
            'version'         : self._mon_version,
            'OldExecution'    : self._mon_old_execution,
            'Target'          : self._mon_target,
            'LiveTests'       : self._mon_live_tests,
            'Test'            : self._mon_test
            }
        # Check that _jumptable and monopts have indeed the same set of keys
        if self.jumptable.keys() != monopts.keys():
            raise FatalError("Inconsistencies in the monitor command tables: different sets of keys")

        # default state values
        self.set_default_state()


    def set_default_state(self) -> None:
        """
        Set state variables to default values.
        """
        self._leaveonexit = (self._iface == 'debugwire' and bool(self._args.atexit) and \
                                 self._args.atexit[0] == 'l') or \
                            (self._iface != 'debugwire' and (self._args.atexit is None or \
                                 self._args.atexit[0] != 's'))
        # default: atexit stayindebugwire
        self._onlyhwbps = self._args.breakpoints[0] == 'h'   # default: breakpoints all
        self._onlyswbps = self._args.breakpoints[0] == 's'   # default: breakpoints all
        self._bpfixed = False                                # only true with ATmega128
        self._cache = self._args.caching[0] != 'd'           # default: caching enabled
        self._erase_before_load = (self._iface == 'jtag' and self._args.erasebeforeload is None) or \
                                  (self._iface == 'jtag' and self._args.erasebeforeload[0] != 'd') or \
                                  (bool(self._args.erasebeforeload) and self._args.erasebeforeload[0] == 'e')
                                                             # default: enable on jtag targets
        self._read_before_write = (self._iface in ['debugwire', 'updi'] and \
                                       (not self._args.load or self._args.load[0] != 'w')) or \
                                       (bool(self._args.load) and self._args.load[0] in ['r', 'n'])
                                                             # default: readbeforewrite when
                                                             # debugWIRE or updi, otherwise: writeonly
        self._only_cache = bool(self._args.load) and self._args.load[0] == 'n'
                                                             # 'noinitialload' only if requested
        self._noload = (bool(self._args.onlywhenloaded) and self._args.onlywhenloaded[0] == 'd') or \
                         (bool(self._args.attach) and \
                              (self._args.onlywhenloaded is None or \
                                   self._args.onlywhenloaded[0] != 'e'))
                                                             # default: onlywhenloaded enable (when not --attach)
        self._range = self._args.rangestepping[0] != 'd'     # default: rangestepping enable
        self._safe = self._args.singlestep[0] != 'i'         # default: singlestep safe
        self._timersfreeze = (self._args.timers[0] == 'f') or \
                             (self._arch == 'avr8x')         # default: timers run, except for (U)PDI targets

        self._verify = self._args.verify[0] != 'd'           # default: verify enable
        self._power = True
        self._old_exec = False
        # The ATmega128 special case:
        if self._args.dev.lower() in [ 'atmega128', 'atmega128a' ]:
            self._onlyhwbps = True
            self._onlyswbps = False
            self._bpfixed = True

    def is_noinitialload(self) -> bool:
        """
        Returns value of self._only_cache
        """
        return self._only_cache

    def disable_noinitialload(self) -> None:
        """
        Disables only caching after first load
        """
        self._only_cache = False

    def is_leaveonexit(self) -> bool:
        """
        Returns True iff the debugger will leave debug mode on exit (i.e.,
        """
        return self._leaveonexit

    def is_onlyhwbps(self) -> bool:
        """
        Returns True iff only hardware breakpoints are used
        """
        return self._onlyhwbps

    def is_onlyswbps(self) -> bool:
        """
        Returns True iff only software brrakpoints are used
        """
        return self._onlyswbps

    def is_cache(self) -> bool:
        """
        Returns True iff the loaded binary is cached and used as a cache
        """
        return self._cache

    def is_debugger_active(self) -> bool:
        """
        Returns True if debugger is active
        """
        return self._debugger_active

    def set_debug_mode_active(self, enable : bool = True) -> None:
        """
        Sets the debug mode to True (or False) and remembers that debug mode has been
        activated once
        """
        self._debugger_active = enable
        if enable:
            self._debugger_activated_once = True

    def is_read_before_write(self) -> bool:
        """
        Returns True iff read-before-write is enabled for the load function
        """
        return self._read_before_write

    def is_noload(self) -> bool:
        """
        Returns True iff execution without a previous load command is allowed
        """
        return self._noload

    def is_range(self) -> bool:
        """
        Returns True iff range-stepping is permitted.
        """
        return self._range

    def is_safe(self) -> bool:
        """
        Returns True iff interrupt-safe single-stepping is enabled
        """
        return self._safe

    def is_timersfreeze(self) -> bool:
        """
        Returns True iff timers will freeze when execution is stopped.
        """
        return self._timersfreeze

    def is_verify(self) -> bool:
        """
        Returns True iff we verify flashing after load.
        """
        return self._verify

    def is_old_exec(self) -> bool:
        """
        Returns True iff the traditional Exec style is used.
        """
        return self._old_exec

    def is_power(self) -> bool:
        """
        Return True iff target is powered.
        """
        return self._power

    def is_erase_before_load(self) -> bool:
        """
        return True iff erase before load is required.
        """
        return self._erase_before_load

    def dispatch(self, tokens : list[str]) -> tuple[str, str]:
        """
        Dispatch according to tokens. First element is
        the monitor command.
        """
        if not tokens:
            return self._mon_help(0)
        handler : Callable[[int | list [ str ] ], tuple[str,  str]] = self._mon_unknown_cmd
        full : bool = False
        opts : list[str | None] | None = None
        name : str | None = None
        cmd : tuple[ str, tuple [ str | None, str | None, list [ str ] ] ]
        optix : int
        for cmd in monopts.items():
            if cmd[0].startswith(tokens[0]):
                if handler == self._mon_unknown_cmd:
                    name = cmd[0]
                    opts = [None] + cmd[1][2] # add None as first entry in options list
                    full = cmd[1][0] == 'full'
                    handler = self.jumptable[name]
                else:
                    handler = self._mon_ambigious
                    opts = None
                    full = False
                    name = None

        # For the 'internal' monitor commands, we require that
        # they are fully spelled out so that they are not
        # invoked by a mistyped abbreviation
        if full:
            if tokens[0] != name:
                handler = self._mon_unknown_cmd
                opts = None

        # If opts == ['*'], just pass the remaining tokens
        if opts == [None, '*']:
            self.logger.debug("Pass on tokens to monitor handlers: %s", tokens)
            return handler(tokens[1:])
        # Now we parse the arguments
        optix = 0
        if opts and len(tokens) > 1:
            optix = -1 # unknown argument
            self.logger.debug("opts=%s", opts)
            for i, poss in enumerate(opts):
                if poss is not None and poss.startswith(tokens[1]) or poss == '*':
                    optix = i
        # call the determined handler with option index
        self.logger.debug("optix=%s", optix)
        return handler(optix)

    def _mon_unknown_cmd(self, _ : int | list[str]) -> tuple[ str, str ]:
        return("", "Unknown 'monitor' command")

    def _mon_unknown_arg(self, _ : int | list[str]) -> tuple[ str, str ]:
        return("", "Unknown argument in 'monitor' command")

    def _mon_ambigious(self, _ : int | list[str]) -> tuple[ str, str ]:
        return("", "Ambiguous 'monitor' command string")

    def _mon_atexit(self, optix : int | list[str]) -> tuple[ str, str ]:
        assert self._leaveonexit is True or self._leaveonexit is False, "self._leaveonexit violates LEM"
        if optix == 1 or (optix == 0 and self._leaveonexit is False):
            self._leaveonexit = False
            return("", "MCU will stay in debug mode on exit")
        if optix == 2 or (optix == 0 and self._leaveonexit is True):
            self._leaveonexit = True
            return("", "MCU will leave debug mode on exit")
        return self._mon_unknown_arg(0)

    def _mon_breakpoints(self, optix : int | list[str]) -> tuple[ str, str ]:
        if optix == 0:
            if self._onlyhwbps and self._onlyswbps:
                return("", "Internal confusion: No breakpoints are allowed")
            if self._onlyswbps:
                return("", "Only software breakpoints")
            if self._onlyhwbps:
                if self._bpfixed:
                    return("", "On this MCU, only hardware breakpoints are allowed")
                return("", "Only hardware breakpoints")
            return("", "All breakpoints are allowed")
        if optix in [1, 2, 3] and self._bpfixed:
            return("", "Breakpoint mode cannot be changed on this MCU")
        if optix == 1:
            self._onlyhwbps = False
            self._onlyswbps = False
            return("", "All breakpoints are allowed")
        if optix == 2:
            self._onlyhwbps = False
            self._onlyswbps = True
            return("", "Only software breakpoints")
        if optix == 3:
            self._onlyhwbps = True
            self._onlyswbps = False
            return("", "Only hardware breakpoints")
        return self._mon_unknown_arg(0)

    def _mon_cache(self, optix : int | list[str]) -> tuple[ str, str ]:
        if optix == 1 or (optix == 0 and self._cache is True):
            self._cache = True
            return("", "Flash memory will be cached")
        if optix == 2 or (optix == 0 and self._cache is False):
            self._cache = False
            return("", "Flash memory will not be cached")
        return self._mon_unknown_arg(0)

    def _mon_debugwire(self, optix : int | list[str]) -> tuple[ str, str ]:
        if self._iface != "debugwire" and optix in [0, 1, 2]:
            return("reset" if optix != 0 else "", "This is not a debugWIRE target")
        if optix == 0:
            if self._debugger_active:
                return("", "debugWIRE is enabled")
            return("", "debugWIRE is disabled")
        if optix == 1:
            if not self._debugger_active:
                if self._debugger_activated_once:
                    return("", "Cannot reactivate debugWIRE\n" +
                               "You have to exit and restart the debugger")
                # we set the state variable to active in the calling module
                return("dwon", "debugWIRE is enabled")
            return("reset", "debugWIRE is enabled")
        if optix == 2:
            if self._debugger_active:
                self._debugger_active = False
                return("dwoff", "debugWIRE is disabled")
            return("", "debugWIRE is disabled")
        return self._mon_unknown_arg(0)

    def _mon_erase_before_load(self, optix : int | list[str]) -> tuple[ str, str ]:
        if self._iface == 'debugwire':
            return("", "On debugWIRE targets, flash memory cannot be erased before loading executable")
        if optix == 1 or (optix == 0 and self._erase_before_load is True):
            self._erase_before_load = True
            return("", "Flash memory will be erased before loading executable")
        if optix == 2 or (optix == 0 and self._erase_before_load is False):
            self._erase_before_load = False
            return("", "Flash memory will not be erased before loading executable")
        return self._mon_unknown_arg(0)

    def _mon_flash_verify(self, optix : int | list[str]) -> tuple[ str, str ]:
        if optix == 1 or (optix == 0 and self._verify is True):
            self._verify = True
            return("", "Verifying flash after load")
        if optix == 2 or (optix == 0 and self._verify is False):
            self._verify = False
            return("", "Load operations are not verified")
        return self._mon_unknown_arg(0)

    def _mon_help(self, _ : int | list[str]) -> tuple[ str, str ]:
        return("", """help                                - this help text
version                             - print version
info                                - print info about target and debugger
reset                               - reset MCU
atexit [stay|leave]                 - stay in/leave debug mode on exit
breakpoints [all|software|hardware] - allow breakpoints of a certain kind
caching [enable|disable]            - use loaded executable as cache (default)
debugwire [enable|disable]          - activate/deactivate debugWIRE mode,
erasebeforeload [enable|disable]    - erase flash memory before load (default
                                      only for JTAG targets)
ioregister <ioreg-expr> [<int>]     - display I/O register or bitfield and
                                      set it to new value if <int> is given
load [readbeforewrite|writeonly|noinitialload]
                                    - read flash before writing (default for
                                      debugWIRE), write blindly, or read
                                      w/o flashing initially
onlywhenloaded [enable|disable]     - execute only with loaded executable (def.)
rangestepping [enable|disable]      - allow range stepping
singlestep [safe|interruptible]     - single stepping mode; safe is default
timers [run|freeze]                 - run (def.) or freeze timers when stopped
                                      ('run' is impossible on UPDI targets)
verify [enable|disable]             - verify that loading was successful (def.)""")

    def _mon_info(self, _ : int | list[str]) -> tuple[ str, str ]:
        return ('info',"""PyAvrOCD version:         """ + importlib.metadata.version("pyavrocd") + """
Debugging enabled:        """ + ("yes" if self._debugger_active else "no") + """
Target:                   {}
Debugger:                 """ + self._toolname + """
Debugging interface:      """ + self._iface + (" (leave on exit)" if self._leaveonexit else " (stay on exit)") + """
Breakpoints:              """ + ("all types"
                                     if (not self._onlyhwbps and not self._onlyswbps) else
                                     ("only hardware bps"
                                          if self._onlyhwbps else "only software bps")) + """
Execute only when loaded: """ + ("enabled" if not self._noload else "disabled") + """
Load mode:                """ + ("only-cache" if self._only_cache else
                                     ("read-before-write" if self._read_before_write else "write-only")) + """
Erase before load:        """ + ("enabled" if self._erase_before_load else "disabled") + """
Verify after load:        """ + ("enabled" if self._verify else "disabled") + """
Caching loaded binary:    """ + ("enabled" if self._cache else "disabled") + """
Range-stepping:           """ + ("enabled" if self._range else "disabled") + """
Single-stepping:          """ + ("safe" if self._safe else "interruptible")  + """
Timers:                   """ + ("frozen when stopped"
                                     if self._timersfreeze else "run when stopped") + "{}")

    def _mon_ioregister(self, args : int | list [str]) -> tuple[ str, str ]:
        if not 'svd' in self._dbg.device_info:
            return("", f"No SVD information for '{self._dbg.get_devicename()}'")
        if isinstance(args, list) and len(args) == 1:
            return self._get_ioregister_value(args)
        if isinstance(args, list) and len(args) == 2:
            return self._set_ioregister_value(args)
        return("", "The 'ioregister' command requires 1 or 2 arguments")

    def _mon_load(self, optix: int | list[str]) -> tuple[ str, str ]:
        if optix == 3 or (optix == 0 and self._only_cache is True):
            self._only_cache = True
            return("", "Only caching when loading")
        if optix == 1 or (optix == 0 and self._read_before_write is True):
            self._only_cache = False
            self._read_before_write = True
            return("", "Reading before writing when loading")
        if optix == 2 or (optix == 0 and self._read_before_write is False):
            self._only_cache = False
            self._read_before_write = False
            return("", "No reading before writing when loading")
        return self._mon_unknown_arg(0)

    def _mon_noload(self, optix : int | list[str]) -> tuple[ str, str ]:
        if optix == 1 or(optix == 0 and self._noload is False):
            self._noload = False
            return("",  "Execution is only possible after a previous load command")
        if optix == 2  or (optix == 0 and self._noload is True):
            self._noload = True
            return("", "Execution is always possible")
        return self._mon_unknown_arg(0)

    def _mon_range_stepping(self, optix : int | list[str]) -> tuple[ str, str ]:
        if optix == 1 or (optix == 0 and self._range is True):
            self._range = True
            return("",  "Range stepping is enabled")
        if optix == 2 or (optix == 0 and self._range is False):
            self._range = False
            return("", "Range stepping is disabled")
        return self._mon_unknown_arg(0)

    def _mon_reset(self, _ : int | list[str]) -> tuple[ str, str ]:
        if self._debugger_active:
            return("reset", "MCU has been reset")
        return("","Debugger is not enabled")

    def _mon_singlestep(self, optix : int | list[str]) -> tuple[ str, str ]:
        if optix == 1 or (optix == 0 and self._safe is True):
            self._safe = True
            return("", "Single-stepping is interrupt-safe")
        if optix == 2  or (optix == 0 and self._safe is False):
            self._safe = False
            return("", "Single-stepping is interruptible")
        return self._mon_unknown_arg(0)

    def _mon_timers(self, optix : int | list[str]) -> tuple[ str, str ]:
        if self._arch == 'avr8x':
            return("", "On (U)PDI targets, timers are frozen when execution is stopped")
        if optix == 2 or (optix == 0 and self._timersfreeze is True):
            self._timersfreeze = True
            resp = "Timers are frozen when execution is stopped"
        elif optix == 1 or (optix == 0 and self._timersfreeze is False):
            self._timersfreeze = False
            resp = "Timers will run when execution is stopped"
        else:
            return self._mon_unknown_arg(0)
        if optix == 0:
            return("", resp)
        return (str(int(not self._timersfreeze)), "MCU reset\n" + resp)

    def _mon_version(self, _ : int | list[str] ) -> tuple[ str, str ]:
        return("", "PyAvrOCD version {}".format(importlib.metadata.version("pyavrocd")))

    # The following commands are for internal purposes
    def _mon_old_execution(self, _ : int | list[str]) -> tuple[ str, str ]:
        self._old_exec = True
        return("", "Old execution mode")

    def _mon_target(self, optix : int | list[str] )  -> tuple[ str, str ]:
        res : tuple[ str, str ]
        if optix == 1:
            self._power = True
            res = ("power on", "Target power on")
        elif optix == 2:
            self._power = False
            res = ("power off", "Target power off")
        elif optix == 3:
            res = ("power query", "Target query")
        elif optix == 0:
            if self._power is True:
                res = ("", "Target power is on")
            else:
                res = ("", "Target power is off")
        else:
            return self._mon_unknown_arg(0)
        return res

    def _mon_live_tests(self, _ : int | list[str]) -> tuple[ str, str ]:
        if self._debugger_active:
            return("live_tests", "Tests done")
        return("", "Cannot run tests because debugging is not enabled")


    def _mon_test(self,_ : int | list[str]) -> tuple[ str, str ]:
        if self._debugger_active:
            return("test", "Tests done")
        return("", "Cannot execute test because debugging is not enabled")

    def _matching_registers(self, expr : str) -> list[ dict[ str, Any ]]:
        result = []
        if not expr:
            return []
        for p in self._dbg.device_info['svd']['device']['peripherals']['peripheral']: # all peripherals
            for r in p['registers']['register']: # all registers
                if fnmatch.fnmatch(p['name'] + '.' + r['name'], expr.upper()): # matching register
                    result.append({ 'name': p['name'] + '.' + r['name'],
                                        'address' : p['baseAddress'] + r['addressOffset'],
                                        'description': r['description'], 'size': r['size'] })
        self.logger.debug("Matching regs: %s", result)
        return result

    def _matching_fields(self, expr : str) -> list[ dict[ str, Any ]]:
        result = []
        if not expr:
            return []
        for p in self._dbg.device_info['svd']['device']['peripherals']['peripheral']: # all peripherals
            for r in p['registers']['register']: # all registers
                if 'fields' not in r:
                    continue
                for f in r['fields']['field']: # all fields
                    if fnmatch.fnmatch(p['name'] + '.' + r['name'] + '.' + f['name'], expr.upper()):
                        result.append({ 'name': p['name'] + '.' + r['name'] + '.' + f['name'],
                                        'address' : p['baseAddress'] + r['addressOffset'],
                                        'bits' : f['bitRange'],
                                        'size' : r['size'],
                                        'description': f['description'],
                                        'enumeratedValues': f.get('enumeratedValues',{'enumeratedValue' : [] }) })
        self.logger.debug("Matching fields: %s", result)
        return result

    def _display_registers(self, regs : list [ dict [ str, Any ]]) -> str:
        results = []
        for r in regs:
            val = int.from_bytes(self._dbg.sram_masked_read(r['address'], r['size']//8), 'little')
            results.append(
              f"{r['name']} (@0x{r['address']:X}, {r['size']}-bits) = 0x{val:X}, 0b{val:b}, {val} ({r['description']})")
        return '\n'.join(results)

    def _display_fields(self,  fields : list [ dict [ str, Any ]]) -> str:
        results = []
        for f in fields:
            val = int.from_bytes(self._dbg.sram_masked_read(f['address'], f['size']//8), 'little')
            val = self._extract_bitfield(val, f['bits'])
            results.append(
                f"{f['name']} (@0x{f['address']:X}{f['bits']}) = 0x{val:X}, 0b{val:b}, {val} ({f['description']})")
        if len(fields) == 1:
            for v in fields[0]['enumeratedValues']['enumeratedValue']:
                results.append(
                    f"   {v['value']}: {v['name']} ({v['description']})")
        return '\n'.join(results)



    def _extract_bitfield(self, val : int, bits : str) -> int:
        bitsrange = bits.replace("[","").replace("]","").split(":")
        start = int(bitsrange[0])
        end = int(bitsrange[1])
        val = val >> end
        mask = (1 << (start-end+1)) - 1
        return val & mask

    def _set_bitfield(self, oldregval : int, newval : int, bits : str) -> int:
        bitsrange = bits.replace("[","").replace("]","").split(":")
        start = int(bitsrange[0])
        end = int(bitsrange[1])
        self.logger.debug("start=%d, end=%d", start, end)
        mask = (1 << (start - end + 1)) - 1
        self.logger.debug("mask=0x%X", mask)
        if mask < newval:
            raise OverflowError
        newregval = (newval & mask) << end
        self.logger.debug("newregval=0x%X", newregval)
        mask = mask << end
        self.logger.debug("shifted mask=0x%X", mask)
        return oldregval - (oldregval & mask) + newregval

    def _get_ioregister_value(self, args : list [str]) -> tuple[ str, str ]:
        regs = self._matching_registers(args[0])
        if len(regs) == 0:
            regs = self._matching_registers("*." + args[0])
        if len(regs) > 1:
            return ("", self._display_registers(regs))
        if len(regs) == 1:
            result = self._display_fields(self._matching_fields(regs[0]['name'] + ".*"))
            if result:
                result = self._display_registers(regs) + '\n' + result
            else:
                result = self._display_registers(regs)
            return ("", result)
        fields = self._matching_fields(args[0])
        if len(fields) == 0:
            fields = self._matching_fields("*." + args[0])
        if fields:
            return("", self._display_fields(fields))
        return("", "No matching I/O registers or fields identified")

    def _set_ioregister_value(self, args : list [str]) -> tuple[ str, str ]:
        try:
            newvalue = int(args[1], 0)
        except ValueError:
            return("", "Second argument must be a well-formed integer literal")
        regs = self._matching_registers(args[0])
        if len(regs) == 0:
            regs = self._matching_registers("*." + args[0])
        if len(regs) > 1:
            return("", "No unique I/O register addressed")
        if len(regs) == 1:
            oldvalue = int.from_bytes(self._dbg.sram_masked_read(regs[0]['address'], regs[0]['size']//8), 'little')
            try:
                self._sram_write16bitreg(regs[0]['address'], newvalue.to_bytes(regs[0]['size']//8, 'little'))
            except OverflowError:
                return("", "Value out of range, cannot be stored")
            mess = ""
            if regs[0]['address'] & 0xFFFF in self._dbg.masked_registers:
                mess = " register is read-protected"
            elif newvalue != int.from_bytes(self._dbg.sram_masked_read(regs[0]['address'],
                                                                           regs[0]['size']//8), 'little'):
                mess = " was unsuccessful"
            return("", f"{regs[0]['name']} = {newvalue} (old value was: {oldvalue}){mess}")
        fields = self._matching_fields(args[0])
        if len(fields) == 0:
            fields = self._matching_fields("*." + args[0])
        if len(fields) > 1:
            return("", "No unique I/O register field addressed")
        if len(fields) == 1:
            self.logger.debug("Field to change: %s", fields[0])
            oldregval = int.from_bytes(self._dbg.sram_masked_read(fields[0]['address'], fields[0]['size']//8), 'little')
            self.logger.debug("oldreg = %s", oldregval)
            oldfieldval = self._extract_bitfield(oldregval, fields[0]['bits'])
            self.logger.debug("oldreg = %s, oldfield = %s", oldregval, oldfieldval)
            try:
                newregval = self._set_bitfield(oldregval, newvalue, fields[0]['bits'])
                self._sram_write16bitreg(fields[0]['address'], newregval.to_bytes(fields[0]['size']//8, 'little'))
            except OverflowError:
                return("", "Value out of range, cannot be store")
            mess = ""
            if fields[0]['address'] & 0xFFFF in self._dbg.masked_registers: #pylint: disable='protected-access'
                mess = " register is read-protected"
            elif newregval != int.from_bytes(self._dbg.sram_masked_read(fields[0]['address'],
                                                                            fields[0]['size']//8), 'little'):
                mess = " was unsuccessful"
            return("", f"{fields[0]['name']} = {newvalue} (old value was: {oldfieldval}){mess}")
        return("", "No matching I/O register or field")

    def _sram_write16bitreg(self, addr : int, data : bytes) -> None:
        """
        If writing to a 16 bit register on the classic MCUs, you first have to write the high, then the low byte.
        On modern MCUs, it is the other way around.
        """
        if len(data) != 2 or self._dbg.get_architecture() == 'avr8x':
            self._dbg.sram_masked_write(addr, data)
        else:
            self._dbg.sram_masked_write(addr+1, data[1:])
            self._dbg.sram_masked_write(addr, data[:1])
