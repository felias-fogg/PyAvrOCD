#!/usr/bin/env python3
"""
This an end-to-end test running avr-gdb, debugging different test programs testing the
outputs of avr-gdb with Pexpect. The GDB server needs to be run separately using the
serv.h bash script.

The specification of the tests is given by the YAML file e2e.yml
"""

#pylint: disable=line-too-long,too-many-locals
import fnmatch
from typing import Any
import pprint
import collections
import argparse
import logging
import textwrap
import sys
import copy
import re
import subprocess
from time import sleep
import os
import pexpect
from pexpect import spawn, run, EOF, TIMEOUT
import yaml
import usb
import usb.core
import serial
from serial import SerialException
import serial.tools.list_ports

logger = logging.getLogger()
schema = { 'includes': [ '<STR>' ],
            'tests':
                 { '<STR>':
                       { 'virtual': '<BOOL>',
                         'requires': { 'ram_atmost': '<NUMBER>',
                                       'ram_atleast': '<NUMBER>',
                                       'flash_atmost': '<NUMBER>',
                                       'flash_atleast': '<NUMBER>',
                                       'boot': '<BOOL>',
                                       'dw': '<BOOL>',
                                       'jtag': '<BOOL>',
                                       'updi': '<BOOL>',
                                       'arduino': '<BOOL>',
                                       'cadc': '<BOOL>',
                                       'autopower': '<BOOL>',
                                       'nolto': '<BOOL>',
                                       'dirty': '<BOOL>' },
                         'import': '<STR>',
                         'sketch': '<STR>',
                         'serverargs': '<STR>',
                         'compilerargs': '<STR>',
                         'upload': '<STR>',
                         'steps': [ {
                             'import': '<STR>',
                             'stimulus': '<STR>',
                             'response': '<STR>',
                             'responses': [ '<STR>' ],
                             'success': '<STR>',
                             'fail': '<STR>',
                             'interrupt': '<NUMBER>',
                             'timeout': '<NUMBER>' } ] } },
           'devices':
                  { '<STR>': {
                        'virtual': '<BOOL>',
                        'import': '<STR>',
                        'mcu': '<STR>',
                        'board': '<STR>',
                        'variant': '<STR>',
                        'pinout': '<STR>',
                        'chip': '<STR>',
                        'architecture': '<STR>',
                        'LTO': '<STR>',
                        'provides':
                             { 'ram': '<NUMBER>',
                               'flash': '<NUMBER>',
                               'boot': '<BOOL>',
                               'dw': '<BOOL>',
                               'jtag': '<BOOL>',
                               'updi': '<BOOL>',
                               'arduino': '<BOOL>',
                               'cadc': '<BOOL>',
                               'autopower': '<BOOL>',
                               'dirty': '<BOOL>',
                               'nolto': '<BOOL>',
                               'usb': '<BOOL>' },
                        'clocks': [ '<NUMBER>' ],
                        'core': '<STR>',
                        'led_builtin': '<NUMBER>',
                        'setup': '<STR>' } },
           'cores':
                  { '<STR>': {
                        'virtual': '<BOOL>',
                        'import': '<STR>',
                        'options': {
                            'cpu': '<BOOL>',
                            'clock': '<BOOL>',
                            'chip': '<BOOL>',
                            'bootloader': '<BOOL>',
                            'LTO': '<BOOL>',
                            'pinout': '<BOOL>',
                            'variant': '<BOOL>' },
                        'default': '<NUMBER>',
                        'clock': {
                            '<NUMBER>': {
                                'code': '<STR>',
                                'value': '<STR>' } } } } }

def setup_options(parser : argparse.ArgumentParser) -> None:
    """
    Define the different options
    """
    parser.add_argument('-b', '--baud',
                            type=int,
                            dest='baud',
                            help='Communication speed of attached dw-link debugger',
                            default=115200)
    parser.add_argument('-c', '--clock',
                            type=float,
                            dest='clock',
                            help='MCU clock frequency in MHz',
                            choices=[1, 2, 4, 5, 8, 10, 16, 20, 1.2, 9.6 ],
                            default=None)
    parser.add_argument('-d', '--device',
                            type=str,
                            dest='dev',
                            help='Device to debug')
    parser.add_argument('-p', '--pretty-print', dest='pp', action='store_true',
                            help="Pretty print specification and exit")
    parser.add_argument('-s', '--spec-file', dest='spec', default='e2e.yml',
                            help='Specfication file (default e2e.yml)')
    parser.add_argument('-t', '--test', dest='script', action='append',
                            help="Test to execute (give multiple times) (default all compatible tests)")
    parser.add_argument('-v', '--verbose',
                        default='info', choices=['debug', 'info',
                                                     'warning', 'error', 'critical'],
                        help="Logging verbosity level")

def fatal_error(filename : str, *messages : str) -> None:
    """
    Reports error and then exits.
    """
    logger.critical("Fatal Error with specification file: %s", filename)
    for m in messages:
        logger.critical(m)
    sys.exit(1)

def parse_specification(specfile : str) -> dict [ str, Any ]:
    """
    Parse the specification, which can contain an 'includes' entry.
    The list of of include files is then visited as well. Cyclic includes
    are forbidden.
    """
    result : dict[str, Any] = { }
    openlist = [ specfile ]
    closedlist = [ ]
    while openlist:
        nextspec = openlist.pop()
        closedlist.append(nextspec)
        try:
            with open(nextspec, "r", encoding='utf-8') as f:
                nextresult = yaml.safe_load(f)
        except FileNotFoundError:
            fatal_error(nextspec, "No such file!")
        except yaml.parser.ParserError as m:
            fatal_error(nextspec, "Parsing error: %s" % str(m))
        except yaml.scanner.ScannerError as m:
            fatal_error(nextspec, "Scanner error: %s" % str(m))
        check_spec(schema, nextresult, [], nextspec)
        if not set(openlist+closedlist).isdisjoint(nextresult.get('includes', [ ])):
            fatal_error("There are includes that have appeared in other files", nextspec)
        openlist += nextresult.get('includes', [ ])
        if 'includes' in nextresult:
            del nextresult['includes']
        result = merge_specs(nextspec, result, nextresult)
    return result

def check_spec(item : dict [ str, Any ] , d : str | float | dict | list,
                     chain : list [ Any ], filename : str) -> None:
    """
    Check the spec 'd' against a schema 'item'
    'chain' is the chain of keys so far and 'filename' is the current
    spec filename. Both are only used to provide reasonable error messages.
    """
    if item == '<NUMBER>':
        if not isinstance(d, (int, float)):
            fatal_error(filename,
                            "There is an error in path %s" % chain,
                            "Expected '%s' to be a number" % d)
    elif item == '<BOOL>':
        if not isinstance(d, bool) and d is not None:
            fatal_error(filename,
                            "There is an error in path %s" % chain,
                            "Expected '%s' to be a bool" % d)
    elif item == '<STR>':
        if not isinstance(d, str):
            fatal_error(filename,
                            "There is an error in path %s" % chain,
                            "Expected '%s' to be a string" % d)
    elif isinstance(item, list):
        if not isinstance(d, list):
            fatal_error(filename,
                            "There is an error in path %s" % chain,
                            "Expected that '%s' is a list" % d)
        for el in d:
            check_spec(item[0], el, chain, filename)
    elif isinstance(item, dict):
        if not isinstance(d, dict):
            fatal_error(filename,
                            "There is an error in path %s" % chain,
                            "Expected that '%s' is a dict" % d)
        else:
            legal = list(item.keys())
            used = list(d.keys())
            if legal == [ '<STR>' ]:
                if not all(isinstance(s, str) for s in used):
                    fatal_error(filename,
                                    "There is an error in path %s" % chain,
                                    "Expected strings as keys but got '%s'" % used)
                else:
                    for k in used:
                        check_spec(item['<STR>'], d[k], chain + [k], filename)
            elif legal == [ '<NUMBER>' ]:
                if not all(isinstance(n, (float, int)) for n in used):
                    fatal_error(filename,
                                    "There is an error in path %s" % chain,
                                    "Expected only numbers as keys but got '%s'" % used)
                else:
                    for k in used:
                        check_spec(item['<NUMBER>'], d[k], chain + [k], filename)
            else:
                if not set(used) <= set(legal):
                    fatal_error(filename,
                                    "There is an error in path %s" % chain,
                                    "Expected only keys %s but got %s" % (legal, used))
                else:
                    for k in used:
                        check_spec(item[k], d[k], chain + [k], filename)


def merge_specs(filename : str, result : dict [ str , Any ], new : dict [ str, Any ]) -> dict [ str, Any ]:
    """
    Merges specs into one big spec.
    'filename' is the file name of the current spec file
    'result' is the result accumulated so far before the merge
    'new' is rthe spec we just read
    Note that all spec files can contain entries under the keys 'tests', 'devices', 'cores'.
    However, the inside these categories the keays have to be unique.
    """
    for top in ('tests', 'devices', 'cores'):
        if top in new:
            if top not in result:
                result[top] = { }
            for k,v in new[top].items():
                if k in result[top]:
                    fatal_error(filename,
                    "Key '%s' in category '%s' has been used before" % (k,top))
                result[top][k] = v
    return result


def deep_update(source : dict [ Any, Any ], overrides : dict [ Any, Any ]) -> dict [ Any, Any ]:
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key, value in overrides.items():
        if isinstance(value, collections.abc.Mapping) and value:
            returned = deep_update(source.get(key, {}), dict(value))
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source

def process_imports(spec : dict[ str, Any ]) -> None:
    """
    Go over the three spec categories and add specified imports (except for the steps list, which will be covered later).
    Multi level imports are possible. We only stop when no more import is requested. So, so do not to request
    a cyclic import!
    """
    while True:
        importing = False
        for d in [ 'tests', 'devices', 'cores' ]:
            for k,v in spec[d].items():
                if 'import' in v.keys():
                    importing = True
                    i = v['import']
                    if i not in spec[d]:
                        logger.critical("Tried to import '%s' in specification of '%s', but failed", i, k)
                        sys.exit(1)
                    new = copy.deepcopy(spec[d][i])
                    new.pop('virtual', None)
                    v.pop('import', None)
                    new = deep_update(new,v)
                    spec[d][k] = new
        if not importing:
            break

def import_steps(spec : dict [ str, Any ]) -> None:
    """
    Splice in a step list at the point where the import is mentioned. The imports are
    resolved recursively, so an imported test may import other tests itself, and the
    order in which the tests appear in the specification does not matter. Cyclic imports
    are reported instead of being expanded until we run out of memory.
    """
    resolved : dict [ str, list [ dict [ str, Any ] ] ] = { }
    pending : list [ str ] = [ ]

    def resolve(name : str, importer : str) -> list [ dict [ str, Any ] ]:
        if name in resolved:
            return resolved[name]
        if name in pending:
            logger.critical("Cyclic step imports: %s", " -> ".join(pending + [ name ]))
            sys.exit(1)
        test = spec['tests'].get(name, None)
        if test is None:
            logger.critical("Could not import '%s' steps into '%s'.", name, importer)
            sys.exit(1)
        pending.append(name)
        newlist : list [ dict [ str, Any ] ] = [ ]
        for s in test.get('steps', [ ]):
            if 'import' in s:
                newlist += resolve(s['import'], name)
            else:
                newlist.append(s)
        pending.pop()
        resolved[name] = newlist
        return newlist

    for t in spec['tests']:
        spec['tests'][t]['steps'] = resolve(t, t)

# Libraries the sketches need, kept here so that every machine compiles the same
# thing. Without this the compilation depends on what happens to sit in the
# sketchbook of whoever runs the tests.
LIBRARIES = "libraries"

AVRDUDE_MIN = (8, 0)

def avrdude_version() -> tuple [ int, int ] | None:
    """
    Version of the avrdude on PATH, which is the one the sketch Makefiles call.
    That is not the avrdude arduino-cli uses for uploads; a core brings its own.
    """
    try:
        done = subprocess.run(["avrdude"], capture_output=True, text=True,
                              timeout=30, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    found = re.search(r"version\s+(\d+)\.(\d+)", done.stdout + done.stderr, re.IGNORECASE)
    return (int(found.group(1)), int(found.group(2))) if found else None

def check_avrdude(spec : dict [ str, Any ], script_list : list [ str ]) -> bool:
    """
    Some sketch Makefiles set fuses with 'avrdude -T "config ..."', which needs
    avrdude 8 or later. Those recipes are prefixed with '-', so make swallows the
    failure and the test then runs against fuses that were never changed. Refuse
    to start instead of measuring the wrong thing.
    """
    needy = [ ]
    for test in script_list:
        sketch = spec['tests'][test].get('sketch')
        if not sketch:
            continue
        makefile = os.path.join('sketches', sketch, 'Makefile')
        if not os.path.exists(makefile):
            continue
        with open(makefile, encoding="utf-8") as src:
            if any('avrdude' in line and ' -T' in line for line in src):
                needy.append(test)
    if not needy:
        return True
    version = avrdude_version()
    if version is None:
        logger.critical("No avrdude on PATH, but %s set fuses with it", sorted(needy))
        return False
    if version < AVRDUDE_MIN:
        logger.critical("avrdude %d.%d is too old for %s, which need 'avrdude -T config' "
                        "from version %d.%d on", version[0], version[1], sorted(needy),
                        AVRDUDE_MIN[0], AVRDUDE_MIN[1])
        return False
    return True

def check_clocks(spec : dict [ str, Any ]) -> None:
    """
    Check that every clock frequency a device offers has an entry in the clock table of
    its core, and that the core's default clock is one the device offers. Both can go
    wrong unnoticed when a device inherits its clock list from a chip but overrides the
    core, or when a core inherits a clock table from a core with a different set.
    """
    cores = spec.get('cores', { })
    problems : list [ str ] = [ ]
    for name, dev in spec.get('devices', { }).items():
        if dev.get('virtual'):
            continue
        core = dev.get('core', None)
        if core is None:
            continue
        if core not in cores:
            problems.append(f"{name}: core '{core}' is not described in the specification")
            continue
        table = cores[core].get('clock', { })
        clocks = dev.get('clocks', [ ])
        unknown = [c for c in clocks if c not in table]
        if unknown:
            problems.append(f"{name}: core '{core}' has no clock entry for "
                                f"{', '.join(str(u) for u in unknown)} MHz")
        default = cores[core].get('default', None)
        if default is not None and clocks and default not in clocks:
            problems.append(f"{name}: default clock {default} MHz of core '{core}' "
                                f"is not among the clocks of this device")
    if problems:
        for p in problems:
            logger.critical("%s", p)
        sys.exit(1)

def select_tests(spec : dict[ str, Any], dev : str, candidates : list[ str ]) -> tuple [ list [str ], list [ str ] ]:
    """
    Select tests according to which requirements are satisfied by the DUT.
    Returns list of all non-virtual tests, and all selected tests
    """
    testlist = [ ]
    alltests = candidates if candidates else [ t for t in spec['tests'] if 'virtual' not in spec['tests'][t]]
    provides = spec['devices'][dev]['provides']
    for t in alltests:
        if t not in spec['tests']:
            logger.critical("%s is not a known test", t)
            sys.exit(1)
        if requirements_met(spec['tests'][t].get('requires',{ }), provides):
            logger.debug("Test selected: %s", t)
            testlist.append(t)
        else:
            if candidates:
                logger.warning("Test '%s' is not feasible for %s", t, dev)
            else:
                logger.debug("Test '%s' is not feasible for %s", t, dev)
    return alltests, testlist

def requirements_met(req : dict[ str, Any ], prov : dict[ str, Any ]) -> bool:
    """
    Check that all requirements 'req' are provided by 'prov'
    """
    ok = True
    for r in req:
        if r == 'ram_atleast':
            if req[r] > prov['ram']:
                ok = False
        elif r == 'ram_atmost':
            if req[r] < prov['ram']:
                ok = False
        elif r == 'flash_atleast':
            if req[r] > prov['flash']:
                ok = False
        elif r == 'flash_atmost':
            if req[r] < prov['flash']:
                ok = False
        else:
            if req[r] != prov.get(r, False):
                ok = False
    return ok

def check_ports(baud : int) -> str | None:
    """
    Go through all connected serial ports and tests whether it is a dw-link server
    """
    for delay in (0.2, 2):
        for s in serial.tools.list_ports.comports(True):
            if s.device in ["/dev/cu.Bluetooth-Incoming-Port", "/dev/cu.debug-console"]:
                continue
            try:
                with serial.Serial(s.device, baud, timeout=0.1,
                                    write_timeout=0.1, exclusive=True) as ser:
                    sleep(delay)
                    ser.write(b'\x05') # send ENQ
                    resp = ser.read(7) # under Linux, the first response might be empty
                    if resp != b'dw-link':
                        sleep(0.2)
                        ser.write(b'\x05') # try again sending ENQ
                        resp = ser.read(7) # now it should be the right response!
                    if resp == b'dw-link':
                        return s.device
            except SerialException:
                pass
            except Exception as e:
                logger.critical("Error: '%s'", str(e))
    return None

def identify_programmer(intf : str, baud : int) -> tuple [ str, str ]:
    """
    Return pair of debugger id and port name for avrdude
    'intf' must be one of 'isp', 'jtag', or 'updi'
    """
    debuggers = { 0x2140: 'jtag3',
                  0x2141: 'atmelice_',
                  0x2144: 'powerdebugger_',
                  0x2111: 'xplainedpro_',
                  0x2169: 'xplainedpro_',
                  0x2145: 'xplainedmini_',
                  0x2175: 'pkobn_',
                  0x2177: 'pickit4_',
                  0x2180: 'snap_' }

    tools = [d for d in usb.core.find(find_all=True) if
                       d.idVendor == 0x3EB and d.idProduct in debuggers]
    if len(tools) > 1:
        logger.critical("More than one debug tool connected!")
        sys.exit(1)
    if len(tools) == 1:
        return debuggers[tools[0].idProduct] + intf, "usb"
    if len(tools) == 0 and intf == 'isp': # check dw-link
        portname = check_ports(baud)
        if portname:
            return 'arduino_as_isp', portname
    logger.critical("No compatible debugger found")
    sys.exit(1)

def build_fqbn(dev : str, clock_value : float , spec : dict [ str, Any ]) -> str:
    """
    Build up the FQBN.
    """
    # Basic FQBN consisting out of core, architecture, and board
    fqbn = ( spec['devices'][dev]['core'] + ':' + spec['devices'][dev]['architecture'] +
        ':' +  spec['devices'][dev]['board'] )
    options_dict = spec['cores'][spec['devices'][dev]['core']].get('options',{})

    # Determine all applicable options
    options = [o for o in options_dict if options_dict[o] and (o in spec['devices'][dev] or o == 'clock')]
    logger.debug("Possible options: %s", options)

    # Now add all applicable options, first needs to be attached using ':'
    sep = ':'
    while options:
        if 'chip' in options: # add chip first (if applicable)
            opt = 'chip'
            options.remove('chip')
        else:
            opt = options.pop()
        if opt == 'clock':
            val = spec['cores'][spec['devices'][dev]['core']]['clock'][clock_value]['code']
        else:
            val = spec['devices'][dev][opt]
        fqbn += sep + opt + '=' + val
        sep = ','
    return fqbn

def run_compile_command(cmd : str) -> bool:
    """
    Compile sketch by running 'cmd' and return success value.
    """
    logger.debug("Command: %s", cmd)
    cmd_out, exit_status =  run(cmd, withexitstatus=1)
    logger.debug("Result: %s", cmd_out.decode("utf-8"))
    return exit_status == 0


def compile_arduino(sketch : str, spec : dict [ str, Any ],
                        dev : str, clock : float) -> bool:
    """
    Compile an Arduino sketch
    """
    logger.info("Compile '%s.ino' with arduino-cli for %s / clock: %s MHz", sketch, dev, clock)
    fqbn = build_fqbn(dev, clock, spec)
    logger.info("FQBN: %s", fqbn)
    cmd = f"arduino-cli compile --clean -b {fqbn} --export-binaries"
    cmd += f" --libraries {LIBRARIES}"     # so that a host's sketchbook does not matter
    cmd += f" --optimize-for-debug --output-dir sketches/{sketch} sketches/{sketch}"
    return run_compile_command(cmd)

def compile_make(sketch : str, spec : dict [ str, Any ],
                     dev : str, clock : float, prog : str, port : str) -> bool:
    """
    Call make.
    """
    logger.info("Compile '%s' with make for %s / clock: %s MHz", sketch, dev, clock)
    mcu = spec['devices'][dev]['mcu']
    cclock = spec['cores'][spec['devices'][dev]['core']]['clock'][clock]['value']
    # A Makefile that sets fuses needs to know which the part has. DWEN in
    # particular exists only on debugWIRE parts, and some tests run on JTAG parts
    # as well.
    provides = spec['devices'][dev]['provides']
    caps = " ".join(f"{name.upper()}={'yes' if provides.get(name) else 'no'}"
                    for name in ('dw', 'jtag', 'updi'))
    # Writing lock bits is a property of the debugger, not of the board: the mEDBG
    # of an Xplained Mini cannot do it, while a dw-link or an Atmel-ICE attached to
    # the same board can. So a Makefile that wants to lock a part is told what is
    # currently connected.
    caps += " LOCK=" + ("no" if prog.startswith('xplainedmini') else "yes")
    cmd = f"make -C sketches/{sketch} PORT={port} MCU={mcu} F_CPU={cclock} PROG={prog}"
    cmd += f" {caps} fresh"
    return run_compile_command(cmd)

#pylint: disable=unused-argument
def do_upload(sketch : str, upload_options : str,
                  spec : dict  [ str, Any ], dev : str,
                  programmer : str, port : str) -> bool:
    """
    Upload a sketch
    """
    return False

def progress() -> None:
    """
    Just print a dot to signal progress
    """
    print(".",end='')
    sys.stdout.flush()

def report_failure(child : pexpect.spawn , mes : str) -> tuple [ bool, int ]:
    """
    Report failure and exit.
    """
    print()
    child.close()
    logger.error(mes)
    return False, 0

def match(line : str, expect_list : list [ str ]) -> bool:
    """
    Check whether the 'expect_list' contains a wildcard string that matches into the 'line'
    returned by the debugger. Return a boolean value.
    """
    for p in expect_list:
        if fnmatch.filter(line.split('\n'), '*' + p + '*'):
            return True
    return False

def remove_echo(cmd : str, response : str) -> str:
    """
    Remove echo from response.
    """
    response = response.replace("\n", " ").replace("\r", "")
    echo = f"{cmd} +{cmd} "
    index = response.find(cmd)+len(echo)
    if response.find(cmd) >= 0:
        return response[index+8:]
    return response

def exec_step(child : pexpect.spawn, step : dict [ str, Any ]) -> tuple [ bool, int ]:
    """
    Execute one step and return whether the step was successful. In addition return 1, 0, -1 if the step
    was finished with early success, regularly, or with early failure, respectively.
    """
    progress()
    logger.debug("Sending command '%s'", step['stimulus'])
    try:
        child.sendline(step['stimulus'])
    except OSError:
        child.close()
        return False, 0
    interrupt = step.get('interrupt', None)
    if interrupt:
        child.expect(["\\+", TIMEOUT], timeout=5) # wait for the + of the GDB tracer
        sleep(interrupt)
        child.sendcontrol('C')
        logger.debug("Sending ^C")
        sleep(1)
        resp = child.expect([ r"\(gdb\)", TIMEOUT, EOF],
                                timeout=5)
        if resp >= 1:
            return report_failure(child,
                        "Received TIMEOUT/EOF in response to ^C after '%s'" %
                            step['stimulus'])
        if not match(child.before, [ "SIGINT" ]):
            return report_failure(child,
                                      "After sending %s and ^C expected SIGINT but got %s" %
                                      (step['stimulus'], child.before))
        return True, 0
    resp = child.expect([r"\(gdb\)", TIMEOUT, EOF,
                             r'Please power-cycle the target system'],
                            timeout=step.get('timeout', 5))
    if resp == 3:
        print()
        logger.warning("*** Power-cycle target system! ***")
        resp = child.expect([ r"\(gdb\)", TIMEOUT, EOF], timeout=60)
        if resp != 0:
            return report_failure(child, "Failed during power-cycling")
    logger.debug("Response: %s", remove_echo(step['stimulus'], child.before))
    if resp >= 1:
        if step['stimulus'] == 'quit':
            return True, 0
        return report_failure(child,
                            "Received TIMEOUT or EOF after '%s'" %
                                  step['stimulus'])
    expect_list = step.get('responses', [])
    if not expect_list and step.get('response', None):
        expect_list = [ step['response'] ]
    if expect_list:
        if match(child.before, expect_list):
            return True, 0
        return report_failure(child, "After sending %s expected %s but got %s" %
                                  (step['stimulus'], expect_list, child.before))
    if step.get('success', False):
        if match(child.before, [ step['success'] ]):
            return True, 1
        return True, 0
    if step.get('fail', False):
        if match(child.before, [ step['fail'] ]):
            return True, -1
        return True, 0
    return True, 0


def exec_all_steps(script : str, steps : list [ dict [ str, Any ] ], dev : str, spec : dict [ str , Any]) -> bool:
    """
    Run the script in AVR-GDB
    """
    print("Running", script, end='')
    sys.stdout.flush()
    sketch = spec['tests'][script].get('sketch', '')
    binary = ""
    if sketch:
        binary = "sketches/" + sketch + "/" + sketch + ".ino.elf"
        logger.debug("Check for %s", binary)
        if not os.path.exists(binary):
            binary = "sketches/" + sketch + "/" + sketch + ".elf"
            if not os.path.exists(binary):
                logger.critical("Binary not found")
                sys.exit(1)
    with open("pyavrocd.options", "w", encoding="utf-8") as f:
        f.write("\n".join(['-d', spec['devices'][dev]['mcu'], '-m', 'all' ]))
        f.write("\n")
        if spec['tests'][script].get('serverargs', None):
            f.write("\n".join(spec['tests'][script]['serverargs'].split(" ")))
    sleep(1)
    child = spawn("avr-gdb " + binary + " -n", encoding="utf-8")
    resp = child.expect([r"\(gdb\)", TIMEOUT, EOF],timeout=5)
    logger.debug("Initial response: %s", child.before)
    if resp >= 1:
        report_failure(child, "Failed %s calling avr-gdb" % script)
        return False
    for s in steps:
        ok, succfail = exec_step(child, s)
        if not ok:
            child.close()
            return False
        if succfail != 0:
            child.close()
            return succfail == 1
    child.close()
    return True

def run_scripts(scripts : list [ str ], spec : dict [ str, Any ],
                    dev : str, clock : float, progger : str, port : str) -> tuple [ list [ str ], list [ str ] ]:
    """
    Run all selected test 'scripts' (given as list of identifiers)
    """
    # If no clock value has been given, then apply default (from core) if applicable
    if clock is None and spec['cores'][spec['devices'][dev]['core']].get('default', None):
        clock = spec['cores'][spec['devices'][dev]['core']]['default']
    compiled = []
    failed_comp = []
    failed_run = []
    for s in scripts:
        logger.info("Run test '%s'", s)
        sketch = spec['tests'][s].get('sketch', None)
        comp_ok = True
        run_ok = True
        # compile sketch (if necessary)
        if sketch:
            if sketch in compiled:
                logger.info("Program %s has been compiled already", sketch)
            elif os.path.exists(f"sketches/{sketch}/{sketch}.ino"):
                comp_ok = compile_arduino(sketch, spec, dev, clock)
            elif os.path.exists(f"sketches/{sketch}/Makefile"):
                comp_ok = compile_make(sketch, spec, dev, clock, progger, port)
            else:
                logger.critical("Program '%s' was not found", sketch)
                comp_ok = False
            if comp_ok:
                compiled.append(sketch)
            else:
                failed_comp.append(s)
                continue
        # upload (if desired)
        upload = spec['tests'][s].get('upload', None)
        if upload:
            run_ok = do_upload(sketch, spec['tests'][s]['upload'], spec, dev, progger, port)
        # execute all steps after starting GDB
        steps = spec['tests'][s].get('steps', None)
        if steps and run_ok:
            run_ok = exec_all_steps(s, steps, dev, spec)
        if not run_ok:
            print("FAILED")
            failed_run.append(s)
        else:
            print("OK")
    return failed_comp, failed_run


def main() -> int:
    """
    Main routine. Sets up everything and runs the tests.
    """

    # process options
    parser = argparse.ArgumentParser(usage="%(prog)s [options]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\n\
    End-to-end test for GDBserver
            '''))
    setup_options(parser)
    args = parser.parse_args()

    # set up logging
    args.verbose = args.verbose.strip()
    if args.verbose.upper() in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
        form = "[%(levelname)s] %(message)s"
    else:
        form = "[%(levelname)s] %(message)s"
    logging.basicConfig(stream=sys.stderr,level=args.verbose.upper(), format = form)

    # delete spurious pyavrocd.options file
    if os.path.exists('pyavrocd.options'):
        logger.info("Deleting spurious 'pyavrocd.options' file")
        os.remove('pyavrocd.options')

    # read specifications and process
    spec = parse_specification(args.spec)
    process_imports(spec)
    import_steps(spec)
    check_clocks(spec)

    # check if only pretty printing is required
    if args.pp:
        pprint.pprint(spec)
        sys.exit(0)

    # check that a device argument has been given
    if args.dev is None:
        logger.critical("No device has been specified")
        sys.exit(1)

    # check that specified device is supported
    if not spec['devices'].get(args.dev,None) or spec['devices'][args.dev].get('virtual',False):
        logger.critical("Device '%s' is unknown'", args.dev)
        return 1

    # check clock speed
    if args.clock and args.clock not in spec['devices'][args.dev].get('clocks', []):
        logger.critical("Clock frequency %s MHz is not supported on %s for end-to-end tests", args.clock, args.dev)
        return 1

    # determine programming interface
    if 'dw' in spec['devices'][args.dev]['provides']:
        interface = 'isp'
    elif 'jtag' in spec['devices'][args.dev]['provides']:
        interface = 'jtag'
    elif 'updi' in spec['devices'][args.dev]['provides']:
        interface = 'updi'
    else:
        logger.critical("No programming interface for '%s' known", args.dev)
        return 1

    #determine programmer and port
    programmer, port = identify_programmer(interface, args.baud)

    # create list of feasible tests
    all_scripts, script_list = select_tests(spec, args.dev, args.script)

    if not check_avrdude(spec, script_list):
        return 1

    # run scripts
    try:
        failed_comp, failed_scripts = run_scripts(script_list, spec, args.dev, args.clock, programmer, port)
    except KeyError as e:
        logger.critical("Missing value for key %s", str(e))
        return 1
    except Exception as e:
        logger.critical("Terminated because of error: %s", str(e))
        raise e

    # tell result
    logger.info("All tests:               %s", len(all_scripts))
    logger.info("Tried:                   %s", len(script_list))
    logger.info("Successful runs:         %s", len(script_list)-len(failed_comp)-len(failed_scripts))
    logger.info("Compilations failed:     %s", len(failed_comp))
    logger.info("Scripts failed:          %s", len(failed_scripts))
    if [ e for e in all_scripts if e not in script_list]:
        logger.info("Skipped tests:           %s", [ e for e in all_scripts if e not in script_list])
    if failed_scripts + failed_comp:
        logger.error("Some tests failed.")
    if failed_comp:
        logger.error("Failed compilations: %s", failed_comp)
    if failed_scripts:
        logger.error("Failed scripts:      %s", failed_scripts)
    if failed_scripts + failed_comp:
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())


