"""
This module implements the 'monitor' command
"""
# args, logging
import importlib.metadata
from logging import getLogger

# error exceptions
from pyavrocd.errors import FatalError


# This is a list of monitor commands, of which many also be used as command line options
# Key: option/monitor command name
# 1st entry is type: 'cli' means command line option, 'full' needs full name as monitor command
# 2nd entry: default value
# 3rd entry: possible option values, '*' means don't care
monopts = { 'atexit'          : ['cli', 'stayindebugwire', [None, 'stayindebugwire', 'leavedebugwire']],
            'breakpoints'     : ['cli', 'all', [None, 'all', 'software', 'hardware']],
            'caching'         : ['cli', 'enable', [None, 'enable', 'disable']],
            'debugwire'       : [None, None, [None, 'enable', 'disable']],
            'erasebeforeload' : ['cli', 'enable', [None, 'enable', 'disable']],
            'help'            : [None, None, [None]],
            'info'            : [None, None, [None]],
            'load'            : ['cli', None, [None, 'readbeforewrite', 'writeonly']],
            'onlywhenloaded'  : ['cli', 'enable', [None, 'enable', 'disable']],
            'rangestepping'   : ['cli', 'enable', [None, 'enable', 'disable']],
            'reset'           : [None, None, [None, '*']],
            'singlestep'      : ['cli', 'safe', [None, 'safe', 'interruptible']],
            'timers'          : ['cli', 'run', [None, 'run', 'freeze']],
            'verify'          : ['cli', 'enable', [None, 'enable', 'disable']],
            'version'         : [None, None, [None]],
            'NoXML'           : ['full', None, [None]],
            'OldExecution'    : ['full', None, [None]],
            'Target'          : ['full', None, [None, 'on', 'off', 'query']],
            'LiveTests'       : ['full', None, [None]] }

class MonitorCommand():
    """
    This class implements all the monitor commands
    It manages state variables, gives responses and selects
    the right action. The return value of the dispatch method is
    a pair consisting of an action identifier and the string to be displayed.
    """
    def __init__(self, iface, args):
        self._iface = iface
        self._debugger_active = False
        self._debugger_activated_once = False
        self.logger = getLogger('pyavrocd.monitor')
        # state variables (will be set by set_default_values)
        self._noload = None # when true, one may start execution even without a previous load
        self._onlyhwbps = None # only hardware breakpoints permitted
        self._onlyswbps = None # only software breakpoints permitted
        self._read_before_write = None # read before write
        self._leaveonexit = None # leave debugWIRE on exit
        self._cache = None # cache executable and use the cache instead of the MCU's flash
        self._safe = None # safe single-stepping
        self._verify = None # verify flash after load
        self._timersfreeze = None # freeze timers when execution is stopped
        self._noxml = None # disallow XML (only for tests needed)
        self._power = None # power state
        self._old_exec = None # use old-style execution (only for tests needed)
        self._range = None # range-stepping is allowed
        self._erase_before_load = None # erase flash memory before load
        self._args = args # these are all the arguments -- needed to set initial monitor option values


        # commands: merge monoopts and jump table (should have the same sets of keys!)
        self.moncmds = {}
        for key, value in {
            'atexit'          : self._mon_atexit,
            'breakpoints'     : self._mon_breakpoints,
            'caching'         : self._mon_cache,
            'debugwire'       : self._mon_debugwire,
            'erasebeforeload' : self._mon_erase_before_load,
            'help'            : self._mon_help,
            'info'            : self._mon_info,
            'load'            : self._mon_load,
            'onlywhenloaded'  : self._mon_noload,
            'rangestepping'   : self._mon_range_stepping,
            'reset'           : self._mon_reset,
            'singlestep'      : self._mon_singlestep,
            'timers'          : self._mon_timers,
            'verify'          : self._mon_flash_verify,
            'version'         : self._mon_version,
            'NoXML'           : self._mon_noxml,
            'OldExecution'    : self._mon_old_execution,
            'Target'          : self._mon_target,
            'LiveTests'       : self._mon_live_tests,
            }.items():
            self.moncmds[key] = [value] + monopts[key]
            if len(self.moncmds[key]) != 4:
                raise FatalError("Inconsistencies in the monitor command tables")
        if len(self.moncmds) != len(monopts):
            raise FatalError("Inconsistencies in the monitor command tables: different sets of keys")

        # default state values
        self.set_default_state()


    def set_default_state(self):
        """
        Set state variables to default values.
        """
        self._leaveonexit = self._args.atexit[0] == 'l'      # default: stayindebugwire
        self._noload = self._args.onlywhenloaded[0] == 'd'   # default: enable
        self._onlyhwbps = self._args.breakpoints[0] == 'h'   # default: all
        self._onlyswbps = self._args.breakpoints[0] == 's'   # default all
        self._read_before_write = (self._iface == 'debugwire' and \
                                       (not self._args.load or self._args.load[0] != 'w')) or \
                                       (self._args.load and self._args.load[0] == 'r')
                                       # default: readbeforewrite when debugWIRE, otherwise: writeonly
        self._cache = self._args.caching[0] != 'd'           # default: enable
        self._safe = self._args.singlestep[0] != 'i'         # default: safe
        self._verify = self._args.verify[0] != 'd'           # default: enable
        self._timersfreeze = self._args.timers[0] == 'f'     # default: run
        self._range = self._args.rangestepping[0] != 'd'     # default: enable
        self._erase_before_load = self._iface != 'debugwire' and \
          self._args.erasebeforeload[0] != 'd'               # default: enable on non-dw targets, on dw targets
                                                             # it is always false!
        self._noxml = False
        self._power = True
        self._old_exec = False

    def is_leaveonexit(self):
        """
        Returns True iff the debugger will leave debugWIRE mode on exit
        """
        return self._leaveonexit

    def is_onlyhwbps(self):
        """
        Returns True iff only hardware breakpoints are used
        """
        return self._onlyhwbps

    def is_onlyswbps(self):
        """
        Returns True iff only software brrakpoints are used
        """
        return self._onlyswbps

    def is_cache(self):
        """
        Returns True iff the loaded binary is cached and used as a cache
        """
        return self._cache

    def is_debugger_active(self):
        """
        Returns True if debugger is active
        """
        return self._debugger_active

    def set_debug_mode_active(self, enable=True):
        """
        Sets the debug mode to True and remembers that debug mode has been
        activated once
        """
        self._debugger_active = enable
        self._debugger_activated_once = True

    def is_read_before_write(self):
        """
        Returns True iff read-before-write is enabled for the load function
        """
        return self._read_before_write

    def is_noload(self):
        """
        Returns True iff execution without a previous load command is allowed
        """
        return self._noload

    def is_range(self):
        """
        Returns True iff range-stepping is permitted.
        """
        return self._range

    def is_safe(self):
        """
        Returns True iff interrupt-safe single-stepping is enabled
        """
        return self._safe

    def is_timersfreeze(self):
        """
        Returns True iff timers will freeze when execution is stopped.
        """
        return self._timersfreeze

    def is_verify(self):
        """
        Returns True iff we verify flashing after load.
        """
        return self._verify

    def is_old_exec(self):
        """
        Returns True iff the traditional Exec style is used.
        """
        return self._old_exec

    def is_noxml(self):
        """
        Returns True iff GDB is supposed to not accept XML queries
        """
        return self._noxml

    def is_power(self):
        """
        Return True iff target is powered.
        """
        return self._power

    def is_erase_before_load(self):
        """
        return True iff erase before load is required.
        """
        return self._erase_before_load

    def dispatch(self, tokens):
        """
        Dispatch according to tokens. First element is
        the monitor command.
        """
        if not tokens:
            return self._mon_help(0)
        handler = self._mon_unknown_cmd
        full = False
        opts = None
        name = None
        for cmd in self.moncmds.items():
            if cmd[0].startswith(tokens[0]):
                if handler == self._mon_unknown_cmd:
                    handler = cmd[1][0]
                    opts = cmd[1][3]
                    full = cmd[1][1] == 'full'
                    name = cmd[0]
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

        # Now we parse the arguments
        optix = 0
        if opts and len(tokens) > 1:
            self.logger.debug("opts=%s", opts)
            for i, poss in enumerate(opts):
                if poss and poss.startswith(tokens[1]) or poss == '*':
                    optix = i
            if optix == 0: # no match found
                handler = self._mon_unknown_arg
        # call the determined handler with option index
        self.logger.debug("optix=%s", optix)
        return handler(optix)

    def _mon_unknown_cmd(self, _):
        return("", "Unknown 'monitor' command")

    def _mon_unknown_arg(self, _):
        return("", "Unknown argument in 'monitor' command")

    def _mon_ambigious(self, _):
        return("", "Ambiguous 'monitor' command string")

    def _mon_atexit(self, optix):
        if optix == 1 or (optix == 0 and self._leaveonexit is False):
            self._leaveonexit = False
            return("", "MCU will stay in debugWIRE mode on exit")
        if optix == 2 or (optix == 0 and self._leaveonexit is True):
            self._leaveonexit = True
            return("", "MCU will leave debugWIRE mode on exit")
        return self._mon_unknown_arg(None)

    def _mon_breakpoints(self, optix):
        if optix == 0:
            if self._onlyhwbps and self._onlyswbps:
                return("", "Internal confusion: No breakpoints are allowed")
            if self._onlyswbps:
                return("", "Only software breakpoints")
            if self._onlyhwbps:
                return("", "Only hardware breakpoints")
            return("", "All breakpoints are allowed")
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
        return self._mon_unknown_arg(None)

    def _mon_cache(self, optix):
        if optix == 1 or (optix == 0 and self._cache is True):
            self._cache = True
            return("", "Flash memory will be cached")
        if optix == 2 or (optix == 0 and self._cache is False):
            self._cache = False
            return("", "Flash memory will not be cached")
        return self._mon_unknown_arg(None)

    def _mon_debugwire(self, optix):
        if not self._iface == "debugwire":
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
        return self._mon_unknown_arg(None)

    def _mon_erase_before_load(self, optix):
        if self._iface == 'debugwire':
            return("", "On debugWIRE targets, flash memory cannot be erased before loading executable")
        if optix == 1 or (optix == 0 and self._cache is True):
            self._erase_before_load = True
            return("", "Flash memory will be erased before loading executable")
        if optix == 2 or (optix == 0 and self._cache is False):
            self._erase_before_load = False
            return("", "Flash memory will not be erased before loading executable")
        return self._mon_unknown_arg(None)

    def _mon_flash_verify(self, optix):
        if optix == 1 or (optix == 0 and self._verify is True):
            self._verify = True
            return("", "Verifying flash after load")
        if optix == 2 or (optix == 0 and self._verify is False):
            self._verify = False
            return("", "Load operations are not verified")
        return self._mon_unknown_arg(None)

    def _mon_help(self, _):
        return("", """monitor help                       - this help text
monitor version                    - print version
monitor info                       - print info about target and debugger
monitor reset                      - reset MCU
monitor atexit [stayindebugwire|leavedebugwire]
                                   - stay in debugWIRE on exit (def.) or leave
monitor breakpoints [all|software|hardware]
                                   - allow breakpoints of a certain kind
monitor caching [enable|disable]   - use loaded executable as cache (default)
monitor debugwire [enable|disable] - activate/deactivate debugWIRE mode,
monitor erasebeforeload [enable|disable]
                                   - erase flash memory before load (default)
                                     except for debugWIRE
monitor load [readbeforewrite|writeonly]
                                   - optimize loading by first reading flash or
                                     write without reading before (default only
                                     for debugWIRE)
monitor onlywhenloaded [enable|disable]
                                   - execute only with loaded executable
monitor singlestep [safe|interruptible]
                                   - single stepping mode; safe is default
monitor rangestepping [enable|disable]
                                   - allow range stepping
monitor timers [run|freeze]        - run (default) or freeze timers when stopped
monitor verify [enable|disable]    - verify that loading was successful (def.)
If no parameter is specified, the current setting is returned""")

    def _mon_info(self, _):
        return ('info',"""PyAvrOCD version:         """ + importlib.metadata.version("pyavrocd") + """
Target:                   {}
Debugging interface:      """ + self._iface + ((" (leave on exit)" if self._leaveonexit else " (stay on exit)") \
                                                   if self._iface == "debugwire" else "") + """
Debugging enabled:        """ + ("yes" if self._debugger_active else "no") + """
Breakpoints:              """ + ("all types"
                                     if (not self._onlyhwbps and not self._onlyswbps) else
                                     ("only hardware bps"
                                          if self._onlyhwbps else "only software bps")) + """
Execute only when loaded: """ + ("enabled" if not self._noload else "disabled") + """
Load mode:                """ + ("read-before-write" if self._read_before_write else "write-only") + """
Erase before load:        """ + ("enabled" if self._erase_before_load else "disabled") + """
Verify after load:        """ + ("enabled" if self._verify else "disabled") + """
Caching loaded binary:    """ + ("enabled" if self._cache else "disabled") + """
Range-stepping:           """ + ("enabled" if self._range else "disabled") + """
Single-stepping:          """ + ("safe" if self._safe else "interruptible")  + """
Timers:                   """ + ("frozen when stopped"
                                     if self._timersfreeze else "run when stopped") + "{}")


    def _mon_load(self, optix):
        if optix == 1 or (optix == 0 and self._read_before_write is True):
            self._read_before_write = True
            return("", "Reading before writing when loading")
        if optix == 2 or (optix == 0 and self._read_before_write is False):
            self._read_before_write = False
            return("", "No reading before writing when loading")
        return self._mon_unknown_arg(None)

    def _mon_noload(self, optix):
        if optix == 1 or(optix == 0 and self._noload is False):
            self._noload = False
            return("",  "Execution is only possible after a previous load command")
        if optix == 2  or (optix == 0 and self._noload is True):
            self._noload = True
            return("", "Execution is always possible")
        return self._mon_unknown_arg(None)

    def _mon_range_stepping(self, optix):
        if optix == 1 or (optix == 0 and self._range is True):
            self._range = True
            return("",  "Range stepping is enabled")
        if optix == 2 or (optix == 0 and self._range is False):
            self._range = False
            return("", "Range stepping is disabled")
        return self._mon_unknown_arg(None)

    def _mon_reset(self, _):
        if self._debugger_active:
            return("reset", "MCU has been reset")
        return("","Debugger is not enabled")

    def _mon_singlestep(self, optix):
        if optix == 1 or (optix == 0 and self._safe is True):
            self._safe = True
            return("", "Single-stepping is interrupt-safe")
        if optix == 2  or (optix == 0 and self._safe is False):
            self._safe = False
            return("", "Single-stepping is interruptible")
        return self._mon_unknown_arg(None)

    def _mon_timers(self, optix):
        if optix == 2 or (optix == 0 and self._timersfreeze is True):
            self._timersfreeze = True
            return(0, "Timers are frozen when execution is stopped")
        if optix == 1 or (optix == 0 and self._timersfreeze is False):
            self._timersfreeze = False
            return(1, "Timers will run when execution is stopped")
        return self._mon_unknown_arg(None)

    def _mon_version(self, _):
        return("", "PyAvrOCD version {}".format(importlib.metadata.version("pyavrocd")))

    # The following commands are for internal purposes
    def _mon_noxml(self, _):
        self._noxml = True
        return("", "XML disabled")

    def _mon_old_execution(self, _):
        self._old_exec = True
        return("", "Old execution mode")

    def _mon_target(self, optix):
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
            return self._mon_unknown_arg(None)
        return res

    def _mon_live_tests(self, _):
        if self._debugger_active:
            return("live_tests", "Tests done")
        return("", "Cannot run tests because debugging is not enabled")


