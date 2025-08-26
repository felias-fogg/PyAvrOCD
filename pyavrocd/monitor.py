"""
This module implements the 'monitor' command
"""

# args, logging
import importlib.metadata

class MonitorCommand():
    """
    This class implements all the monitor commands
    It manages state variables, gives responses and selects
    the right action. The return value of the dispatch method is
    a pair consisting of an action identifier and the string to be displayed.
    """
    def __init__(self, iface, defaults):
        self._iface = iface
        self._debugger_active = False
        self._debugger_activated_once = False

        # state variables (will be set by set_default_values)
        self._noload = None # when true, one may start execution even without a previous load
        self._onlyhwbps = None
        self._onlyswbps = None
        self._read_before_write = None
        self._cache = None
        self._safe = None
        self._verify = None
        self._timersfreeze = None
        self._noxml = None
        self._power = None
        self._old_exec = None
        self._range = None
        self._defaults = defaults

        # commands
        self.moncmds = {
            'breakpoints'  : self._mon_breakpoints,
            'caching'      : self._mon_cache,
            'debugwire'    : self._mon_debugwire,
            'help'         : self._mon_help,
            'info'         : self._mon_info,
            'load'         : self._mon_load,
            'onlyloaded'   : self._mon_noload,
            'reset'        : self._mon_reset,
            'rangestepping': self._mon_range_stepping,
            'singlestep'   : self._mon_singlestep,
            'timers'       : self._mon_timers,
            'verify'       : self._mon_flash_verify,
            'version'      : self._mon_version,
            'NoXML'        : self._mon_noxml,
            'OldExecution' : self._mon_old_execution,
            'Target'       : self._mon_target,
            'LiveTests'    : self._mon_live_tests,
            }

        # default state values
        self.set_default_state()


    def set_default_state(self):
        """
        Set state variables to default values.
        """
        self._noload = 'o:d' in self._defaults
        self._onlyhwbps = 'b:h' in self._defaults
        self._onlyswbps = 'b:s' in self._defaults
        self._read_before_write = (self._iface == 'debugwire' and 'l:w' not in self._defaults) \
                                    or 'l:r' in self._defaults
        self._cache = 'c:d' not in self._defaults
        self._safe = 's:i' not in self._defaults
        self._verify = 'v:e' in self._defaults
        self._timersfreeze = 't:f' in self._defaults
        self._range = 'r:d' not in self._defaults
        self._noxml = False
        self._power = True
        self._old_exec = False


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

    def dispatch(self, tokens):
        """
        Dispatch according to tokens. First element is
        the monitor command.
        """
        if not tokens:
            return self._mon_help([])
        if len(tokens) == 1:
            tokens += [""]
        handler = self._mon_unknown
        for cmd in self.moncmds.items():
            if cmd[0].startswith(tokens[0]):
                if handler == self._mon_unknown:
                    handler = cmd[1]
                else:
                    handler = self._mon_ambigious
        # For these internal monitor commands, we require that
        # they are fully spelled out so that they are not
        # invoked by a mistyped abbreviation
        if handler == self._mon_noxml and tokens[0] != "NoXML": # pylint: disable=comparison-with-callable
            handler = self._mon_unknown
        if handler == self._mon_target and tokens[0] != "Target": # pylint: disable=comparison-with-callable
            handler = self._mon_unknown
        if handler == self._mon_old_execution and tokens[0] != "OldExecution": # pylint: disable=comparison-with-callable
            handler = self._mon_unknown
        return handler(tokens[1:])

    def _mon_unknown(self, _):
        return("", "Unknown 'monitor' command")

    def _mon_ambigious(self, _):
        return("", "Ambiguous 'monitor' command string")

    def _mon_breakpoints(self, tokens):
        if not tokens[0]:
            if self._onlyhwbps and self._onlyswbps:
                return("", "Internal confusion: No breakpoints are allowed")
            if self._onlyswbps:
                return("", "Only software breakpoints")
            if self._onlyhwbps:
                return("", "Only hardware breakpoints")
            return("", "All breakpoints are allowed")
        if 'all'.startswith(tokens[0]):
            self._onlyhwbps = False
            self._onlyswbps = False
            return("", "All breakpoints are allowed")
        if 'hardware'.startswith(tokens[0]):
            self._onlyhwbps = True
            self._onlyswbps = False
            return("", "Only hardware breakpoints")
        if 'software'.startswith(tokens[0]):
            self._onlyhwbps = False
            self._onlyswbps = True
            return("", "Only software breakpoints")
        return self._mon_unknown(tokens[0])

    def _mon_cache(self, tokens):
        if (("enable".startswith(tokens[0]) and tokens[0] != "") or
                (tokens[0] == "" and self._cache is True)):
            self._cache = True
            return("", "Flash memory will be cached")
        if (("disable".startswith(tokens[0]) and tokens[0] != "") or
                (tokens[0] == "" and self._cache is False)):
            self._cache = False
            return("", "Flash memory will not be cached")
        return self._mon_unknown(tokens[0])

    def _mon_debugwire(self, tokens):
        if not self._iface == "debugwire":
            if tokens[0] =="":
                return("", "This is not a debugWIRE target")
            return("reset", "This is not a debugWIRE target")
        if tokens[0] =="":
            if self._debugger_active:
                return("", "debugWIRE is enabled")
            return("", "debugWIRE is disabled")
        if "enable".startswith(tokens[0]):
            if not self._debugger_active:
                if self._debugger_activated_once:
                    return("", "Cannot reactivate debugWIRE\n" +
                               "You have to exit and restart the debugger")
                # we set the state variable to active in the calling module
                return("dwon", "debugWIRE is enabled")
            return("reset", "debugWIRE is enabled")
        if "disable".startswith(tokens[0]):
            if self._debugger_active:
                self._debugger_active = False
                return("dwoff", "debugWIRE is disabled")
            return("reset", "debugWIRE is disabled")
        return self._mon_unknown(tokens[0])

    def _mon_flash_verify(self, tokens):
        if (("enable".startswith(tokens[0]) and tokens[0] != "") or
                (tokens[0] == "" and self._verify is True)):
            self._verify = True
            return("", "Verifying flash after load")
        if (("disable".startswith(tokens[0]) and tokens[0] != "") or
                (tokens[0] == "" and self._verify is False)):
            self._verify = False
            return("", "Load operations are not verified")
        return self._mon_unknown(tokens[0])

    def _mon_help(self, _):
        return("", """monitor help                       - this help text
monitor version                    - print version
monitor info                       - print info about target and debugger
monitor debugwire [enable|disable] - activate/deactivate debugWIRE mode
monitor reset                      - reset MCU
monitor onlyloaded [enable|disable]
                                   - execute only with loaded executable
monitor load [readbeforewrite|writeonly]
                                   - optimize loading by first reading flash
monitor verify [enable|disable]    - verify that loading was successful
monitor caching [on|off]           - use loaded executable as cache
monitor timers [freeze|run]        - freeze/run timers when stopped
monitor breakpoints [all|software|hardware]
                                   - allow breakpoints of a certain kind
monitor singlestep [safe|interruptible]
                                   - single stepping mode
monitor rangestepping [enable|disable]
                                   - allow range stepping
The first option is always the default one
If no parameter is specified, the current setting is returned""")

    def _mon_info(self, _):
        return ('info',"""
Pyavrocd version:         """ + importlib.metadata.version("pyavrocd") + """
Target:                   {}
Debugging interface:      """ + self._iface + """
Debugging enabled:        """ + ("yes" if self._debugger_active else "no") + """
Breakpoints:              """ + ("all types"
                                     if (not self._onlyhwbps and not self._onlyswbps) else
                                     ("only hardware bps"
                                          if self._onlyhwbps else "only software bps")) + """
Execute only when loaded: """ + ("enabled" if not self._noload else "disabled") + """
Load mode:                """ + ("read-before-write" if self._read_before_write else "write-only") + """
Verify after load:        """ + ("enabled" if self._verify else "disabled") + """
Caching loaded binary:    """ + ("enabled" if self._cache else "disabled") + """
Timers:                   """ + ("frozen when stopped"
                                     if self._timersfreeze else "run when stopped") + """
Range-stepping:           """ + ("enabled" if self._range else "disabled") + """
Single-stepping:          """ + ("safe" if self._safe else "interruptible"))


    def _mon_load(self,tokens):
        if (("readbeforewrite".startswith(tokens[0])  and tokens[0] != "") or
            (tokens[0] == "" and self._read_before_write is True)):
            self._read_before_write = True
            return("", "Reading before writing when loading")
        if (("writeonly".startswith(tokens[0])  and tokens[0] != "") or
                (tokens[0] == "" and self._read_before_write is False)):
            self._read_before_write = False
            return("", "No reading before writing when loading")
        return self._mon_unknown(tokens[0])

    def _mon_noload(self, tokens):
        if (("enable".startswith(tokens[0])  and tokens[0] != "") or
                (tokens[0] == "" and self._noload is False)):
            self._noload = False
            return("",  "Execution is only possible after a previous load command")
        if (("disable".startswith(tokens[0])  and tokens[0] != "")  or
                (tokens[0] == "" and self._noload is True)):
            self._noload = True
            return("", "Execution is always possible")
        return self._mon_unknown(tokens[0])

    def _mon_range_stepping(self, tokens):
        if (("enable".startswith(tokens[0])  and tokens[0] != "") or
                (tokens[0] == "" and self._range is True)):
            self._range = True
            return("",  "Range stepping is enabled")
        if (("disable".startswith(tokens[0])  and tokens[0] != "")  or
                  (tokens[0] == "" and self._range is False)):
            self._range = False
            return("", "Range stepping is disabled")
        return self._mon_unknown(tokens[0])

    def _mon_reset(self, _):
        if self._debugger_active:
            return("reset", "MCU has been reset")
        return("","Enable debugWIRE first")

    def _mon_singlestep(self, tokens):
        if (("safe".startswith(tokens[0]) and tokens[0] != "") or
                (tokens[0] == "" and self._safe is True)):
            self._safe = True
            return("", "Single-stepping is interrupt-safe")
        if (("interruptible".startswith(tokens[0]) and tokens[0] != "")  or
                (tokens[0] == "" and self._safe is False)):
            self._safe = False
            return("", "Single-stepping is interruptible")
        return self._mon_unknown(tokens[0])

    def _mon_timers(self, tokens):
        if (("freeze".startswith(tokens[0]) and tokens[0] != "") or
                (tokens[0] == "" and self._timersfreeze is True)):
            self._timersfreeze = True
            return(0, "Timers are frozen when execution is stopped")
        if (("run".startswith(tokens[0])  and tokens[0] != "") or
                (tokens[0] == "" and self._timersfreeze is False)):
            self._timersfreeze = False
            return(1, "Timers will run when execution is stopped")
        return self._mon_unknown(tokens[0])

    def _mon_version(self, _):
        return("", "pyavrocd version {}".format(importlib.metadata.version("pyavrocd")))

    # The following commands are for internal purposes
    def _mon_noxml(self, _):
        self._noxml = True
        return("", "XML disabled")

    def _mon_old_execution(self, _):
        self._old_exec = True
        return("", "Old execution mode")

    def _mon_target(self, tokens):
        if ("on".startswith(tokens[0]) and len(tokens[0]) > 1):
            self._power = True
            res = ("power on", "Target power on")
        elif ("off".startswith(tokens[0]) and len(tokens[0]) > 1):
            self._power = False
            res = ("power off", "Target power off")
        elif ("query".startswith(tokens[0]) and len(tokens[0]) > 1):
            res = ("power query", "Target query")
        elif tokens[0] == "":
            if self._power is True:
                res = ("", "Target power is on")
            else:
                res = ("", "Target power is off")
        else:
            return self._mon_unknown(tokens[0])
        return res

    def _mon_live_tests(self, _):
        if self._debugger_active:
            return("live_tests", "Tests done")
        return("", "Enable debugWIRE first")

