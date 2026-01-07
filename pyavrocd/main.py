"""
AVR GDB server main program
"""

# args, logging
import webbrowser
import platform
import importlib.metadata
import sys
import os
import argparse
import logging
import shutil
import subprocess
import contextlib
import time
from logging import getLogger


# communication
import usb
import usb.core

# debugger modules
import pymcuprog
import pymcuprog.backend
from pymcuprog.toolconnection import ToolUsbHidConnection
from pymcuprog.pymcuprog_errors import PymcuprogToolConnectionError

from pyavrocd import dwlink
from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.deviceinfo.devices.alldevices import dev_id, dev_iface
from pyavrocd.monitor import monopts
from pyavrocd.server import RspServer

def options(cmd):
    """
    Option processing. Returns processed options.
    """
    parser = argparse.ArgumentParser(usage="%(prog)s [options]",
            fromfile_prefix_chars='@',
            #formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            #epilog="Monitor options can also be specified, e.g. '--verify enable'",
            description='GDB server for debugWIRE and JTAG AVR MCUs'
                                         )
    parser.add_argument("-H", "--webhelp",
                            action='store_true',
                            help="Open web page with help text")

    parser.add_argument("-c", "--command",
                            action='append',
                            dest='cmd',
                            type=str,
                            help=argparse.SUPPRESS) # "Command to set gdb port (OpenOCD style)")

    parser.add_argument("-d", "--device",
                            dest='dev',
                            type=str,
                            help="Device to debug, list supported MCUs with '?'")

    parser.add_argument("-D", "--debug-clock",
                            metavar="DC",
                            dest='clkdeb',
                            type=int,
                            help="JTAG clock frequency for debugging (kHz) (def.: 200)")

    parser.add_argument("-f", type=str, help=argparse.SUPPRESS)

    parser.add_argument("-F", "--F_CPU",
                            type=str,
                            default="1000000",
                            help="CPU clock frequency in Hz (default 1000000)")

    interface_choices = ['debugwire', 'jtag', 'pdi', 'updi']
    parser.add_argument("-i", "--interface",
                            metavar="IF",
                            type=str,
                            choices= ['?'] + interface_choices,
                            help="Debugging interface to use, use '?' for list")

    manage_choices = ['all', 'none', 'bootrst', 'nobootrst', 'dwen', 'nodwen',
                          'ocden', 'noocden', 'lockbits', 'nolockbits', 'eesave', 'noeesave']
    parser.add_argument("-m", "--manage",
                            metavar="FUSE",
                            action='append',
                            dest='manage',
                            default = [ 'none' ],
                            type=str,
                            choices= ['?'] + manage_choices,
                            help="Fuses to be managed, use '?' for list")

    parser.add_argument('-p', '--port',  type=int, default=2000, dest='port',
                            help='Local port on machine (default: 2000)')

    parser.add_argument("-P", "--prog-clock",
                            metavar="PC",
                            dest='clkprg',
                            type=int,
                            default=1000,
                            help="JTAG clock frequency for programming (kHz) (d.: 1000)")

    parser.add_argument('-s', '--start',  dest='prg',
                            help='Start specified program (e.g., simavr)')

    tool_choices = ['atmelice', 'dwlink', 'edbg', 'jtagice3', 'medbg', 'nedbg',
                        'pickit4', 'powerdebugger', 'snap']
    parser.add_argument("-t", "--tool",
                            metavar="TOOL",
                            type=str,
                            choices= ['?'] + tool_choices,
                            help="Tool to connect to, use '?' to list options")

    parser.add_argument("-u", "--usbsn",
                            metavar="SN",
                            type=str,
                            dest='serialnumber',
                            help="USB serial number of the unit to use")

    level_choices = ['all', 'debug', 'info', 'warning', 'error', 'critical']
    parser.add_argument("-v", "--verbose",
                            metavar="LEVEL",
                            default="info", choices= ['?'] + level_choices,
                            help="Verbosity level for logger, use '?' to list levels")

    parser.add_argument("-V", "--version",
                            help="Print PyAvrOCD version number and exit",
                            action="store_true")

    parser.add_argument("-x", "--xargs",
                            metavar="XARGS",
                            type=str,
                            help="Extra arguments for simavr")

    parser.add_argument("--dw-link-baud",
                            dest='baud',
                            type=int,
                            default=115200,
                            help=argparse.SUPPRESS)

    parser.add_argument("--reboot-debugger",
                            dest='reboot',
                            action='store_true',
                            help=argparse.SUPPRESS)


    for option_name, option_type in monopts.items():
        if option_type[0] == 'cli':
            default = option_type[1]
            choices = option_type[2][1:] # copy all options after the None entry
            choices += [ opt[0] for opt in choices ]
            parser.add_argument("--" + option_name, help=argparse.SUPPRESS,
                                    type=str, choices=choices, default=default)

    # Parse args and return
    if os.path.exists('pyavrocd.options'):
        cmd.append('@pyavrocd.options')
    if len(cmd) == 0:
        cmd.append('-h')
    cmd = [x for x in cmd if not x.startswith('@') or os.path.exists(x[1:]) ]

    args = parser.parse_args(cmd)

    if args.webhelp:
        webbrowser.open('pyavrocd.io/command-line-options/')
        sys.exit(0)

    if args.version:
        print("PyAvrOCD version {}".format(importlib.metadata.version("pyavrocd")))
        sys.exit(0)

    questionmark = False
    if args.dev == "?":
        questionmark = True
        if args.interface and args.interface != '?':
            print("Supported devices with debugging interface '%s':" % args.interface)
            alldev = [x for x in sorted(dev_id) if args.interface in dev_iface[dev_id[x]].lower().split("+")]
        else:
            print("Supported devices:")
            alldev = sorted(dev_id)
        for d in alldev[:-1]:
            print(d,sep="",end=", ")
        if alldev:
            print(alldev[-1])
        else:
            print("None")

    if args.interface == '?':
        questionmark = True
        args.interface = None
        print("Possible interfaces (-i) are: ", end="")
        print(', '.join(map(str, interface_choices)))

    if '?' in args.manage:
        questionmark = True
        print("Possible (repeatable) fuse management options (-m) are: ")
        print(', '.join(map(str, manage_choices)),  "(default = %s)" % 'none')

    if args.tool == '?':
        questionmark = True
        print("Possible tools (-t) are: ")
        print(', '.join(map(str, tool_choices)))

    if args.verbose == '?':
        questionmark = True
        args.verbose = 'info'
        print("Possible verbosity levels (-v) are: ")
        print(', '.join(map(str, level_choices)), "(default = %s)" % vars(parser.parse_args([]))['verbose'])

    if questionmark:
        sys.exit(0)

    return args


def setup_logging(args, log_rsp):
    """
    Setup logging
    """
    if args.verbose:
        args.verbose = args.verbose.strip()
    if args.verbose.upper() in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
        form = "[%(levelname)s] %(message)s"
    else:
        form = "[%(levelname)s] %(name)s: %(message)s"
    logging.basicConfig(stream=sys.stdout,level=args.verbose.upper(), format = form)

    if args.verbose.lower() == "debug":
        getLogger('pyedbglib.hidtransport.hidtransportbase').setLevel(logging.CRITICAL)
        getLogger('pyedbglib.protocols.housekeepingprotocol').setLevel(logging.INFO)
        getLogger('pyedbglib.protocols.jtagice3protocol').setLevel(logging.INFO)
        if not log_rsp:
            getLogger('pyavrocd.rsp').setLevel(logging.CRITICAL)
    if args.verbose.lower() != "debug":
        # suppress messages from hidtransport
        getLogger('pyedbglib.hidtransport.hidtransportbase').setLevel(logging.CRITICAL)
        # suppress spurious error messages from pyedbglib
        getLogger('pyedbglib.protocols').setLevel(logging.CRITICAL)
        # suppress errors of not connecting: It is intended!
        getLogger('pymcuprog.nvm').setLevel(logging.CRITICAL)
        # we do not want to see the "read flash" messages
        getLogger('pymcuprog.avr8target').setLevel(logging.ERROR)
        # we do not want to see the message 'Looking for ...' from getdeviceinfo
        getLogger('pymcuprog.deviceinfo.deviceinfo').setLevel(logging.ERROR)

def process_arguments(args, logger): #pylint: disable=too-many-branches
    """
    Process the parsed options. Return triple of
    - return value (if program should be terminated, else None);
    - device name
    - interface string
    """
    args.F_CPU = int(args.F_CPU.rstrip('UL'))

    if args.cmd:
        portcmd = [c for c in args.cmd if 'gdb_port' in c]
        if portcmd:
            cmd = portcmd[0]
            args.port = int(cmd[cmd.index('gdb_port')+len('gdb_port'):])

    if args.tool:
        args.tool = args.tool.strip()

    if args.dev:
        args.dev = args.dev.strip()

    manage = []
    for f in args.manage:
        if f == 'all':
            manage = ['bootrst', 'dwen', 'ocden', 'lockbits', 'eesave']
        elif f == 'none':
            manage = []
        elif f.startswith('no'):
            with contextlib.suppress(ValueError):
                manage.remove(f[2:])
        else:
            manage.append(f)
    args.manage = manage

    if args.clkdeb is None:
        args.clkdeb = min(2000, args.F_CPU//5000)

    if args.clkprg < 0 or args.clkdeb < 0:
        print("Negative frequency values are discouraged")
        return 1, None, None

    device = args.dev

    if not device:
        print("Please specify target MCU with -d option")
        return 1, None, None
    device = device.lower()

    if device not in dev_id:
        print("Device '%s' is not supported by PyAvrOCD" % device)
        return 1, None, None

    if args.interface:
        intf = [args.interface]
    else:
        intf = [x for x in ['debugwire', 'jtag', 'pdi', 'updi']
                    if x in dev_iface[dev_id[device]].lower().split('+')]
    logger.debug("Device: %s", device)
    logger.debug("Possible interfaces: %s", intf)
    logger.debug("Interfaces of chip: %s",  dev_iface[dev_id[device]].lower())
    if not intf:
        print("Device '%s' does not have a compatible debugging interface" % device)
        return 1, None, None
    if len(intf) == 1 and intf[0] not in dev_iface[dev_id[device]].lower():
        print ("Device '%s' does not have the interface '%s'" % (device, intf[0]))
        return 1, None, None
    if len(intf) > 1:
        print("Debugging interface for device '%s' ambiguous: '%s'" % (device, intf))
        return 1, None, None
    intf = intf[0]
    args.dev = device
    return None, device, intf

def handle_simavr(args, device):
    """
    Checks whether simavr shall be started, and if so, will prepare the the start and exit
    when simavr returns.
    """
    if not args.prg:
        return False
    args.prg = args.prg.strip()
    if os.path.basename(args.prg) != 'simavr':
        return False
    prg = shutil.which(args.prg)
    if not prg:
        print("Could not find program '%s'" % args.prg)
        return True
    prg = os.path.abspath(prg)
    prg += " -g " + str(args.port) + " -f " + str(args.F_CPU) + " -m " + device
    if args.xargs:
        prg += " " + args.xargs
    print("Simavr will be started: %s" % prg, flush=True)
    print("Listening on port %d for gdb connection" % args.port, flush=True)
    sim = subprocess.Popen(prg, bufsize=0, shell=True)
    sim.wait()
    return True

def startup_helper_prog(args, logger):
    """
    Starts program requested by user, e.g., a debugger GUI
    """
    if args.prg and args.prg != "nop":
        args.prg = args.prg.strip()
        prg = shutil.which(args.prg)
        if prg:
            prg = os.path.abspath(prg)
            logger.info("Starting %s", prg)
            subprocess.Popen(prg)
        else:
            logger.critical("Could not find program '%s'", args.prg)
            sys.exit(1)

def run_server(server, logger):
    """
    Startup server and serve until done.
    """
    try:
        return server.serve()
    except (ValueError, Exception) as e:
        if logger.getEffectiveLevel() != logging.DEBUG:
            logger.critical("Fatal Error: %s",e)
            return 1
        raise
    return 0

def number_of_connected_edbg_tools(logger):
    """
    Find out how many debugging tools are connected
    """
    prodids = (0x2140, 0x2141, 0x2144, 0x2111, 0x2169, 0x2145, 0x2175, 0x2FC0, 0x2177, 0x2180)
    try:
        if platform.system() == 'Windows':
            return len([d for d in pymcuprog.backend.Backend().get_available_hid_tools() if
                        d.vendor_id == 0x3EB and d.product_id in prodids ])
        return len([d for d in usb.core.find(find_all=True) if
                        d.idVendor == 0x3EB and d.idProduct in prodids])
    except usb.core.NoBackendError as e:
        logger.critical("Could not discover debug probes: %s", e)
        if platform.system() == 'Darwin':
            logger.critical("Install libusb: 'brew install libusb'")
        elif platform.system() == 'Linux':
            logger.critical("Install libusb: 'sudo apt install libusb-1.0-0'")
        else:
            logger.critical("On Windows, USB core is not used, i.e., this error should not happen!")
        return -1 # error return

def reboot(backend, tool, logger):
    """
    Reboots tool and waits for it to reappear.
    In case it takes too long (> 5sec), False is returned, otherwise True.
    """
    logger.info("Rebooting debugger...")
    backend.reboot_tool()
    timeout = 200
    while timeout > 0:
        try:
            backend.connect_to_tool(tool)
            break
        except (PymcuprogToolConnectionError, ValueError):
            pass
        time.sleep(0.1)
        timeout -= 1
    if timeout == 0:
        logger.critical("... could not reconnect")
        return False
    logger.info("Reconnected to %s", backend.transport.hid_device.get_product_string())
    return True

#pylint: disable=too-many-branches
def startup(command_line, logger):
    """
    Configures the CLI, connects to a tool, and starts debugger
    """
    log_rsp = False # will becomce true when verbosity is 'all'

    args = options(command_line)

    # verbose option 'all' is a special one
    if args.verbose == "all":
        log_rsp = True
        args.verbose = "debug"

    # set up logging
    setup_logging(args, log_rsp)

    # process arguments
    result, device, intf = process_arguments(args, logger)
    if result is not None:
        return result

    # check whether simavr should be started, and if so, do that exclusively
    if handle_simavr(args, device):
        return 0

    # now report startup
    logger.info("This is PyAvrOCD version %s", importlib.metadata.version("pyavrocd"))
    # determine number of connected tools
    num_tools = 0
    if args.tool != "dwlink":
        num_tools = number_of_connected_edbg_tools(logger)

    if num_tools < 0: # meaning that USB is not there
        return 1

    if args.tool == "dwlink" or num_tools == 0:
        dwlink.main(args, intf) # if we return, then there is no HW debugger
        logger.critical("No compatible tool discovered")
        return 1 # exit with error code

    # Check whether all connected tools are available as HID devices
    backend = pymcuprog.backend.Backend()
    if len(backend.get_available_hid_tools()) != num_tools:
        if platform.system() == 'Linux':
            logger.critical("Perhaps you need to install the udev rules first:")
            logger.critical("Download https://pyavrocd.io/99-edbg-debuggers.rules,")
            logger.critical("review, edit, and install under /etc/udev/rules.d/.")
        else:
            print(num_tools, backend.get_available_hid_tools())
            logger.error("Not all discovered tools are available")

    available = backend.get_available_hid_tools(serialnumber_substring=args.serialnumber, tool_name=args.tool)
    if len(available) == 0:
        logger.critical("No compatible tool discovered")
        return 1 # exit with error code
    if len(available) > 1:
        logger.critical("More than one compatible tool! Use -u or -t to distinguish.")
        for d in available:
            logger.critical("> Tool: %s, S/N: %s", d.product_string, d.serial_number)
        return 1 # exit with error code

    tool = ToolUsbHidConnection(serialnumber=args.serialnumber, tool_name=args.tool)
    # Now try to connect
    try:
        toolname = "Unknown tool"
        backend.connect_to_tool(tool)
        toolname = backend.transport.hid_device.get_product_string()
        tool.serialnumber = backend.transport.hid_device.get_serial_number_string()
        logger.info("Connected to %s", toolname)
    except OSError as e:
        if str(e) == "open failed":
            logger.critical("Debug probe busy, cannot connect")
        else:
            logger.critical("Could not connect to debug probe: %s", str(e))
            return 1

    if args.reboot:
        if not reboot(backend, tool, logger):
            return 1

    # tool is connected, now we can start
    logger.info("Starting GDB server")
    try:
        avrdebugger = XAvrDebugger(backend.transport, device, intf, args.manage, args.clkprg, args.clkdeb,
                                       args.timers[0]=='r')
        if args.debugwire and args.debugwire[0] == 'd' and intf == 'debugwire':
            avrdebugger.cold_dw_disable()
            return 0
        server = RspServer(avrdebugger, device, args, toolname)
    except Exception as e:
        if logger.getEffectiveLevel() != logging.DEBUG:
            logger.critical("Fatal Error: %s",e)
            return 1
        raise
    startup_helper_prog(args, logger)
    return run_server(server, logger)

def main():
    """
    This generates the root logger and forwards it as well as the arguments to the startup function
    """
    try:
        logger = getLogger()
        return startup(sys.argv[1:], logger)
    except KeyboardInterrupt:
        logger.info("Terminated by Ctrl-C")
        return 1

if __name__ == "__main__":
    sys.exit(main())
