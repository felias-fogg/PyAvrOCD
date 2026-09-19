#!/usr/bin/env python3
"""
This an end-to-end test running avr-gdb, debugging different test programs testing the 
outputs of avr-gdb with Pexpect. The GDB server needs to be run seperately using the 
serv.h bash script.

The specification of the tests is given by the YAML file e2e.yml
"""

#pylint: disable=line-too-long,too-many-locals
import pprint
import collections
import argparse
import logging
import textwrap
import sys
import copy
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
import fnmatch
from typing import Any

logger = None
schema = { 'includes': [ '<STR>' ],
            'tests':
                 { '<STR>':
                       { 'virtual': '<BOOL>',
                         'requires': { 'ram_atmost': '<NUMBER>',
                                       'ram_atleast': '<NUMBER>',
                                       'flash_atmost': '<NUMBER>',
                                       'flash_atleast': '<NUMBER>',
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
                        'chip': '<STR>',
                        'architecture': '<STR>',
                        'LTO': '<STR>',
                        'provides': 
                             { 'ram': '<NUMBER>',
                               'flash': '<NUMBER>',
                               'dw': '<BOOL>',
                               'jtag': '<BOOL>',
                               'updi': '<BOOL>',
                               'arduino': '<BOOL>',
                               'cadc': '<BOOL>',
                               'autopower': '<BOOL>',
                               'dirty': '<BOOL>',
                               'nolto': '<BOOL>',
                               'autopc': '<BOOL>',
                               'usb': '<BOOL>' },
                        'clocks': [ '<NUMBER>' ],
                        'core': '<STR>',
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

def fatal_error(filename : str, *messages : list[str]):
    logger.critical("Fatal Error with specification file: %s", filename)
    for m in messages:
        logger.critical(m)
    sys.exit(1)
    
def parse_specification(specfile : str) -> dict [ str, Any ]:
    """
    Parse all spec files and store the result in a dict
    """
    result = { }
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
        check_scheme(schema, nextresult, [], nextspec)
        if not set(openlist+closedlist).isdisjoint(nextresult.get('includes', [ ])):
            fatal_error("There are includes that have appeared in other files", nextspec)
        openlist += nextresult.get('includes', [ ])
        if 'includes' in nextresult:
            del nextresult['includes']
        result = merge_specs(nextspec, result, nextresult)
    return result

def check_scheme(schema : dict [ str, Any ] , d : str | float ,
                     chain : list [ Any ], filename : str):
    """
    Check the spec against the scheme
    """
    if schema == '<NUMBER>':
        if not isinstance(d, (int, float)):
            fatal_error(filename,
                            "There is an error in path %s" % chain,
                            "Expected '%s' to be a number" % d)
    elif schema == '<BOOL>':
        if not isinstance(d, bool) and d is not None:
            fatal_error(filename,
                            "There is an error in path %s" % chain,
                            "Expected '%s' to be a bool" % d)
    elif schema == '<STR>':
        if not isinstance(d, str):
            fatal_error(filename,
                            "There is an error in path %s" % chain,
                            "Expected '%s' to be a string" % d)
    elif isinstance(schema, list):
        if not isinstance(d, list):
            fatal_error(filename,
                            "There is an error in path %s" % chain,
                            "Expected that '%s' is a list" % d)
        for el in d:
            check_scheme(schema[0], el, chain, f)
    elif isinstance(schema, dict):
        if not isinstance(d, dict):
            fatal_error(filename,
                            "There is an error in path %s" % chain,
                            "Expected that '%s' is a dict" % d)
        legal = list(schema.keys())
        used = list(d.keys())
        if legal == [ '<STR>' ]:
            if not all(isinstance(s, str) for s in used):
                fatal_error(filename,
                                "There is an error in path %s" % chain,
                                "Expected strings as keys but got '%s'" % used)
            for k in used:
                check_scheme(schema['<STR>'], d[k], chain + [k], f)
        elif legal == [ '<NUMBER>' ]:
            if not all(isinstance(n, (float, int)) for n in used):
                fatal_error(filename,
                                "There is an error in path %s" % chain,
                                "Expected only numbers as keys but got '%s'" % used)
            for k in used:
                check_scheme(schema['<NUMBER>'], d[k], chain + [k], f)
        else:
            if not set(used) <= set(legal):
                fatal_error(filename,
                                "There is an error in path %s" % chain,
                                "Expected only keys %s but got %s" % (legal, used))
            for k in used:
                check_scheme(schema[k], d[k], chain + [k], f)


def merge_specs(filename : str, result : dict [ str , Any ], new : dict [ str, Any ]):
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
                

def deep_update(source : dict [Any,Any], overrides : dict [Any,Any]):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key, value in overrides.items():
        if isinstance(value, collections.abc.Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source

def process_imports(spec : dict[ str, Any ]):
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

def import_steps(spec : dict [ str, Any ]):
    """
    Splice in a step list at the point where the import is mentioned. This does not work multi-level, but could
    be extended to work that way.
    """
    for t, v in spec['tests'].items():
        steplist = v.get('steps',[])
        newlist = []
        for s in steplist:
            if 'import' in s:
                exporter = spec['tests'].get(s['import'], None)
                if exporter is None:
                    logger.critical("Could not import '%s' steps into '%s'.", s['import'], t)
                    sys.exit(1)
                newlist += exporter.get('steps', [])
            else:
                newlist.append(s)
        v['steps'] = newlist

def select_tests(spec : dict[ str, Any], dev : str, candidates : list[ str ]):
    """
    Select tests according to which requirements are satisfied by the DUT.
    Returns list of all non-virtual tests, and all selected tests
    """
    testlist = [ ]
    alltests = candidates if candidates else [ t for t in spec['tests'] if 'virtual' not in spec['tests'][t]]
    provides = spec['devices'][dev]['provides']
    for t in alltests:
        if requirements_met(spec['tests'][t].get('requires',{ }), provides):
            logger.debug("Test selected: %s", t)
            testlist.append(t)
        else:
            if candidates:
                logger.info("Test '%s' is not feasible for %s", t, dev)
            else:
                logger.debug("Test '%s' is not feasible for %s", t, dev)
    return alltests, testlist

def requirements_met(req : dict[ str, Any ], prov : dict[ str, Any ]):
    """
    Check that all requirements 'req' are provided by 'prov'
    """
    OK = True
    for r in req:
        if r == 'ram_atleast':
            if req[r] > prov['ram']:
                OK = False
        elif r == 'ram_atmost':
            if req[r] < prov['ram']:
                OK = False
        elif r == 'flash_atleast':
            if req[r] > prov['flash']:
                OK = False
        elif r == 'flash_atmost':
            if req[r] < prov['flash']:
                OK = False
        else:
            if req[r] != prov.get(r, False):
                OK = False
    return OK

def check_ports(baud : int):
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
        
def identify_programmer(intf : str, baud : int):
    """
    return pair of debugger id and port name for avrdude
    intf must be one of 'isp', 'jtag', or 'updi'
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

def build_fqbn(dev : str, clock_value : str , spec : dict [ str, ANY ]) -> str:
    """
    Build up the FQBN.
    """
    # Basic FQBN consisting out of core, architecture, and board
    fqbn = ( spec['devices'][dev]['core'] + ':' + spec['devices'][dev]['architecture'] + 
        ':' +  spec['devices'][dev]['board'] )
    options_dict = spec['cores'][spec['devices'][dev]['core']].get('options',{})

    # Determine all applicable options
    options = [o for o in options_dict if options_dict[o] and (o in spec['devices'][dev] or o == 'clock')]

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
    logger.debug("Command: %s", cmd)
    cmd_out, exit_status =  run(cmd, withexitstatus=1)
    logger.debug("Result: %s", cmd_out.decode("utf-8"))
    return exit_status == 0


def compile_arduino(script : str, sketch : str, spec : dict [ str, Any ],
                        dev : str, clock : float) -> bool:
    """
    Compile an Arduino sketch
    """
    logger.info(f"Compile '%s.ino' with arduino-cli for %s / clock: %s MHz", sketch, dev, clock)
    fqbn = build_fqbn(dev, clock, spec)
    logger.info("FQBN: %s", fqbn)
    cmd = f"arduino-cli compile --clean -b {fqbn} --export-binaries"
    cmd += f" --optimize-for-debug --output-dir sketches/{sketch} sketches/{sketch}"
    return run_compile_command(cmd)

def compile_make(script : str, sketch : str, spec : dict [ str, Any ],
                     dev : str, clock : float, prog : str, port : str) -> bool:
    """
    Call make.
    """
    logger.info("Compile '%s' with make for %s / clock: %s MHz", sketch, dev, clock)
    mcu = spec['devices'][dev]['mcu']
    cclock = spec['cores'][spec['devices'][dev]['core']]['clock'][clock]['value']
    cmd = f"make -C sketches/{sketch} PORT={port} MCU={mcu} F_CPU={cclock} PROG={prog} fresh"
    return run_compile_command(cmd)

def do_upload(sketch : str, upload_options : str,
                  spec : dict  [ str, Any ], dev : str,
                  programmer : str, port : str) -> bool:
    """
    Upload a sketch
    """
    return False

def progress():
    print(".",end='')
    sys.stdout.flush()

def report_failure(child, mes):
    print()
    child.close()
    logger.error(mes)
    return False, 0

def match(line, expect_list):
    for p in expect_list:
        if fnmatch.filter(line.split('\n'), '*' + p + '*'):
            return True
    return False

def remove_echo(cmd, response):
    """
    Remove echo from response
    """
    response = response.replace("\n", " ").replace("\r", "")
    echo = f"{cmd} +{cmd} "
    index = response.find(cmd)+len(echo)
    if response.find(cmd) >= 0:
        return response[index+8:]
    return response
    
def exec_step(child, step, spec):
    progress()
    logger.debug("Sending command '%s'", step['stimulus'])
    child.sendline(step['stimulus'])
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
        if not match(child.before, "SIGINT"):
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
        else:
            return report_failure(child, "After sending %s expected %s but got %s" %
                                      (step['stimulus'], expect_list, child.before))
    if step.get('success', False):
        if match(child.before, [ step['success'] ]):
            return True, 1
        else:
            return True, 0
    if step.get('fail', False):
        if match(child.before, [ step['fail'] ]):
            return True, -1
        else:
            return True, 0
    return True, 0
    

def exec_all_steps(script, steps, dev, spec):
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
        return report_failure(child, "Failed %s calling avr-gdb" % script)
    for s in steps:
        ok, succfail = exec_step(child, s, spec)
        if not ok:
            return False
        if succfail != 0:
            child.close()
            print()
            return succfail == 1
    child.close()
    print()
    return True

def run_scripts(scripts, spec, dev, clock, progger, port):
    """
    Run all selected test scripts 
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
                logger.info("Program % has been compiled already", sketch)
            elif os.path.exists(f"sketches/{sketch}/{sketch}.ino"):
                comp_ok = compile_arduino(s, sketch, spec, dev, clock)
            elif os.path.exists(f"sketches/{sketch}/Makefile"):
                comp_ok = compile_make(s, sketch, spec, dev, clock, progger, port)
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
                failed_run.append(s)
    return failed_comp, failed_run
        
        
def main():
    """
    Main routine. Sets up everything and runs the tests.
    """
    global logger

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
    logger = logging.getLogger()

    # delete spurious pyavrocd.options file
    if os.path.exists('pyavrocd.options'):
        logger.info("Deleting spurious 'pyavrocd.options' file")
        os.remove('pyavrocd.options')

    # read specifications and process
    spec = parse_specification(args.spec)
    process_imports(spec)
    import_steps(spec)

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

                             
