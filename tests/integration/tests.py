#!/usr/bin/env python3
"""
This an integration test running both the gdbserver and avr-gdb
debugging different test programs testing the outputs of avr-gdb with Pexpect.
"""
#pylint: disable=line-too-long,too-many-locals
import argparse
import logging
import textwrap
import sys
from time import sleep
import os
import pexpect

from scripts import all_scripts
from devices import test_devices

#pylint: disable=too-many-statements
def main():
    """
    Main routine. Sets up everything and runs the tests.
    """
    parser = argparse.ArgumentParser(usage="%(prog)s [options]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\n\
    Integration test for GDBserver
            '''))
    parser.add_argument('-c', '--clock',
                            type=str,
                            dest='clock',
                            help='MCU clock frequency in MHz',
                            choices=['1', '8', '16', '1.2', '9.6', 'none' ],
                            required=True)
    parser.add_argument('-d', '--device',
                            type=str,
                            dest='dev',
                            help='Device to debug',
                            required=True)
    parser.add_argument("-v", "--verbose",
                        default="info", choices=['debug', 'info',
                                                     'warning', 'error', 'critical'],
                        help="Logging verbosity level")

    parser.add_argument("-s", "--script", dest='script',
                            help="Script to execute (default all compatible scripts)")
    args = parser.parse_args()

    # set up logging
    args.verbose = args.verbose.strip()
    if args.verbose.upper() in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
        form = "[%(levelname)s] %(message)s"
    else:
        form = "[%(levelname)s] %(name)s: %(message)s"
    logging.basicConfig(stream=sys.stderr,level=args.verbose.upper(), format = form)
    logger = logging.getLogger()

    script_list = None
    if args.script:
        if args.script.strip() not in all_scripts:
            logger.critical("'%s' is not a test script", args.script.strip())
            return 1
        script_list = [ args.script.strip() ]
    if args.dev.lower() not in test_devices:
        logger.critical("%s is not supported for integration tests", args.dev)
        return 1
    mcu_name = args.dev.lower()
    mcu_clocks, tag_list, fqbn, test_board = test_devices[mcu_name]
    if args.clock in mcu_clocks:
        clock = mcu_clocks[args.clock]
    else:
        logger.critical("Clock frequency %s MHz is not supported for integration tests on %s",
                            args.clock, mcu_name)
        return 1
    if script_list is None:
        script_list = [ script_name for script_name in all_scripts.keys() if all([(tag in all_scripts[script_name][0]) for tag in tag_list]) ]
        script_list = ([ sn for sn in script_list if 'first' in all_scripts[sn][0] ] +
          [ sn for sn in script_list if 'first' not in all_scripts[sn][0] and 'last' not in all_scripts[sn][0] ] +
          [ sn for sn in script_list if 'last' in all_scripts[sn][0] ])

    logger.info("Starting integration testing on %s.", mcu_name)
    logger.warning("Prepare debugging with %s.", test_board)
    logger.warning("Make sure that 'serv.sh' is running")
    logger.warning("Press <RETURN> when everything has been set up.")
    input()

    logger.info("Running %d integration test%s on %s", len(script_list), "s" if len(script_list) > 1 else "", mcu_name)
    failed_comp = 0
    failed_scripts = 0
    tests_done = 0
    for sn in script_list:
        logger.info("Try: %s", sn)
        script = all_scripts[sn]
        exit_status = 0
        cmd_out = ""
        if script[1]:
            if os.path.exists("sketches/" + script[1] + "/" + script[1] + ".ino"): # Arduino sketch
                logger.info("Compile '%s.ino' for '%s' clock on %s", script[1], clock, mcu_name)
                cmd = "arduino-cli compile -b " + fqbn + clock + \
                  ' -e --build-property="build.extra_flags=-Og -ggdb3 ' + script[2] + '" --output-dir ' + \
                  "sketches/" + script[1] + " sketches/" + script[1]
            else: # C/C++-program
                logger.info("Compile C/C++ program '%s' for clock '%s' on %s", script[1], clock, mcu_name)
                cmd = "make -C sketches/" + script[1] + " MCU=" + mcu_name + " F_CPU=" + args.clock + "000000UL fresh"
            logger.debug("Compile command: '%s'", cmd)
            cmd_out, exit_status =  pexpect.run(cmd, withexitstatus=1)
        tests_done += 1
        if exit_status != 0:
            logger.error("Failed compilation: %s", cmd_out)
            failed_comp += 1
            continue
        if not run_script(logger, sn, script):
            logger.error("Failed to run script '%s'", sn)
            failed_scripts += 1
        else:
            logger.info("Succeeded: %s", sn)
    logger.info("Test runs:           %s", tests_done)
    logger.info("Compilations failed: %s", failed_comp)
    logger.info("Scripts failed:      %s", failed_scripts)
    return 0

#pylint: disable=too-many-return-statements,too-many-branches,too-many-statements
def run_script(logger, test_name, script):
    """
    Execute one script and compare with expected replies.
    """
    last_response = ""
    print("Running", test_name, end='')
    test_binary = "sketches/" + script[1] + "/" + script[1] +  ".elf"
    if not os.path.exists(test_binary):
        test_binary = "sketches/" + script[1] + "/" + script[1] + ".ino.elf"
    if script[1] == "":
        test_binary = ""
    child = pexpect.spawn("avr-gdb " + test_binary + " -n")
    sleep(2)
    ix = 0
    script = script[3] # The list of interaction pairs
    resp = child.expect([r"\(gdb\)",pexpect.TIMEOUT,pexpect.EOF],timeout=1)
    logger.debug("Initial response: %s", child.before.decode())
    if resp >= 1:
        logger.error("Failed %s calling avr-gdb", test_name)
        child.close()
        print()
        return False
    while ix < len(script):
        print(".",end='')
        sys.stdout.flush()
        interact = script[ix]
        if interact[0] == "$SLEEP":
            logger.debug("COMMAND: Sleep(%s)",interact[1])
            sleep(interact[1])
            ix += 1
            continue
        if interact[0] == "$SUCCESS_IF":
            if last_response.find(interact[1]) >= 0: # preliminary success / skip
                child.close()
                print("SKIP")
                return True
            ix += 1
            continue
        logger.debug("COMMAND: %s", interact[0])
        child.sendline(interact[0])
        resp = child.expect([ r"\(gdb\)", pexpect.TIMEOUT, pexpect.EOF,
                                r'Please power-cycle the target system' ],
                                timeout=(120 if interact[0] == 'load' else 20))
        if resp == 1:
            if interact[1] == pexpect.TIMEOUT:
                logger.debug("RESPONSE: TIMEOUT")
                continue
            logger.error("Failed %s in line %s with TIMEOUT", test_name, ix-1)
            logger.error("Expected: '%s' in response to: '%s'", interact[1], interact[0])
            logger.debug("FAILED: %s", test_name)
            child.close()
            print()
            return False
        if resp == 2:
            if ix == len(script) - 1:
                logger.debug("SUCCEEDED: " + test_name)
                print("OK")
                return True
            logger.debug("FAILED: %s in line %s with EOF from child",  test_name, ix-1)
            child.close()
            print()
            return False
        if resp == 3:
            logger.warning("*** Power-cycle target system! ***")
            resp = child.expect([ r"\(gdb\)", pexpect.TIMEOUT, pexpect.EOF], timeout=30)
            if resp != 0:
                logger.debug("Failed during power-cycling")
                child.close()
                print()
                return False
        logger.debug("RESPONSE: '%s'", child.before.decode())
        last_response = child.before.decode()
        if child.before.decode().find(interact[1]) >= 0 or \
            len(interact) > 2 and child.before.decode().find(interact[2])  >= 0 or \
            len(interact) > 3 and child.before.decode().find(interact[3])  >= 0:
            ix += 1
        else:
            logger.error("Failed %s in line %s with unexpected response:", test_name, ix-1)
            logger.error("      '%s'",  child.before.decode())
            logger.error("Expected: '%s' in response to: '%s'", interact[1], interact[0])
            logger.debug("FAILED: %s", test_name)
            print()
            child.close()
            return False
    logger.debug("SUCCEEDED: %s", test_name)
    child.close()
    print("OK")
    return True

if __name__ == '__main__':
    sys.exit(main())
