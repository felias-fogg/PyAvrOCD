"""
AVR GDB server main program
"""
# args, logging
from typing import Any
from collections.abc import Callable
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
import usb.util

# elftools
from elftools.elf.elffile import ELFFile

# debugger modules
import pymcuprog
import pymcuprog.backend
from pymcuprog.toolconnection import ToolUsbHidConnection
from pymcuprog.pymcuprog_errors import PymcuprogToolConnectionError

import pyedbglib

from pyavrocd import dwlinkbackend
from pyavrocd import jtag2
from pyavrocd.xavrdebugger import EdbgBackend, EdbgProbe
from pyavrocd.jtag2backend import Jtag2Backend
from pyavrocd.dwlinkbackend import DwlinkBackend
from pyavrocd.backend import DebugBackend, ProbeCandidate
from pyavrocd.deviceinfo.devices.alldevices import dev_id, dev_iface
from pyavrocd.monitor import monopts
from pyavrocd.server import RspServer


def options(cmd: list[str]) -> argparse.Namespace:
    """
    Option processing. Returns processed options.
    """
    parser : argparse.ArgumentParser
    parser = argparse.ArgumentParser(prog="pyavrocd",
            usage="%(prog)s [options]\nGDB server for AVR MCUs",
            fromfile_prefix_chars='@',
            formatter_class=argparse.RawTextHelpFormatter,
            #description='GDB server for 8-bit AVR MCUs'
                                         )
    parser.add_argument("-H", "--webhelp",
                            action='store_true',
                            help="Open web page with help text")

    parser.add_argument("-a", "--attach",
                            action='store_true',
                            help="Start without resetting the MCU")

    parser.add_argument("-c",
                            action='append',
                            dest='cmd',
                            #help="Command to set gdb port (OpenOCD style)",
                            help=argparse.SUPPRESS,
                            type=str)

    parser.add_argument("-C", "--comm-speed",
                            metavar="CS",
                            dest='kbps',
                            default=750,
                            help="Communication speed for (U)PDI (kbps) (def.: 750)",
                            #help=argparse.SUPPRESS,
                            type=int)


    parser.add_argument("-d", "--device",
                            dest='dev',
                            type=str,
                            help="Device to debug, list supported MCUs with '?'")

    parser.add_argument("-e", "--elf-file",
                            metavar="EF",
                            dest='elffile',
                            help="ELF file, will be checked for '-mrelax' optimization")

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

    interface_choices : list[str] = ['debugwire', 'jtag', 'pdi', 'updi']
    parser.add_argument("-i", "--interface",
                            metavar="IF",
                            type=str,
                            choices= ['?'] + interface_choices,
                            help="Debugging interface to use, use '?' for list")

    manage_choices : list [str] = ['all', 'none', 'bootrst', 'nobootrst', 'dwen', 'nodwen',
                          'ocden', 'noocden', 'lockbits', 'nolockbits', 'eesave', 'noeesave']
    parser.add_argument("-m", "--manage",
                            metavar="FUSE",
                            action='append',
                            dest='manage',
                            default = [ 'none' ],
                            type=str,
                            choices= ['?'] + manage_choices,
                            help="Fuse to manage (give multiple times), use '?' for list")

    parser.add_argument('-p', '--port',  type=int, default=2000, dest='port',
                            help='Local port on machine (default: 2000)')

    parser.add_argument("-P", "--prog-clock",
                            metavar="PC",
                            dest='clkprg',
                            type=int,
                            default=1000,
                            help="JTAG clock frequency for programming (kHz) (d.: 1000)")

    parser.add_argument('-s', '--start',  dest='prg',
                            help='Start specified program (e.g., simavr or gede)')

    tool_choices : list [str] = sorted(EDBG_TOOLS | JTAG2_TOOLS | {'dwlink'})
    parser.add_argument("-t", "--tool",
                            metavar="TOOL",
                            type=str,
                            choices= ['?'] + tool_choices,
                            help="Tool to connect to, use '?' to list options")

    parser.add_argument("-u", "--usbsn",
                            metavar="SN",
                            type=str,
                            dest='serialnumber',
                            help="Suffix of USB serial number or serial port name")


    level_choices : list[str] = ['all', 'debug', 'info', 'warning', 'error', 'critical']
    parser.add_argument("-v", "--verbose",
                            metavar="LEVEL",
                            default="info", choices= ['?'] + level_choices,
                            help="Verbosity level for logger, use '?' to list levels")

    parser.add_argument("-V", "--version",
                            help="Print PyAvrOCD version number and exit",
                            action="store_true")

    parser.add_argument("-x", "--xarg",
                            metavar="XARG",
                            type=str,
                            action='append',
                            help="Extra argument for simavr (give multiple times)")

    parser.add_argument("--once",
                            dest='once',
                            action='store_true',
                            help="Terminate when GDB disconnects or detaches")

    parser.add_argument("--dw-link-baud",
                            dest='baud',
                            type=int,
                            default=115200,
                            help=argparse.SUPPRESS)

    parser.add_argument("--reboot-debugger",
                            dest='reboot',
                            action='store_true',
                            help=argparse.SUPPRESS)

    parser.add_argument("--memory-map-disable",
                            dest='nomm',
                            action='store_true',
                            help=argparse.SUPPRESS)

    parser.add_argument("--skip-signature-verification",
                            dest='skipsig',
                            action='store_true',
                            help=argparse.SUPPRESS)

    parser.add_argument("--power-cycle-command",
                            dest='powercycle',
                            type=str,
                            default=None,
                            help=argparse.SUPPRESS)

    option_name : str
    option_type : tuple[ str | None, str | None, list [ str ] ]
    for option_name, option_type in monopts.items():
        if option_type[0] == 'cli':
            default : str | None = option_type[1]
            choices : list[str] = option_type[2][:] # copy all options after the None entry
            choices += [ opt[0] for opt in choices ]
            parser.add_argument("--" + option_name, help=argparse.SUPPRESS,
                                    type=str, choices=choices, default=default)

    # Parse args and return
    if os.path.exists('pyavrocd.options'):
        cmd.append('@pyavrocd.options')
    if len(cmd) == 0:
        cmd.append('-h')
    cmd = [x for x in cmd if not x.startswith('@') or os.path.exists(x[1:]) ]

    args : argparse.Namespace = parser.parse_args(cmd)

    if args.webhelp:
        webbrowser.open('https://pyavrocd.io/latest/command-line-options/')
        sys.exit(0)

    if args.version:
        print("PyAvrOCD version {}".format(importlib.metadata.version("pyavrocd")))
        sys.exit(0)

    questionmark : bool = False
    alldev : list[str]
    if args.dev == "?":
        questionmark = True
        if args.interface and args.interface != '?':
            print("Supported devices with debugging interface '%s':" % args.interface)
            alldev = [x for x in sorted(dev_id)
                                      if args.interface in dev_iface[dev_id[x]].lower().split("+")]
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


def setup_logging(args : argparse.Namespace, log_rsp : bool) -> None:
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
        # we do not want to see the "read flash" messages
        getLogger('pymcuprog.avr8target').setLevel(logging.ERROR)
        # we do not want to see the message 'Looking for ...' from getdeviceinfo
        getLogger('pymcuprog.deviceinfo.deviceinfo').setLevel(logging.ERROR)
        # suppress errors of not connecting: It is intended!
        getLogger('pymcuprog.nvm').setLevel(logging.CRITICAL)

#pylint: disable=too-many-branches
def process_arguments(args : argparse.Namespace, logger : logging.Logger) -> tuple [None|int, str, str]:
    """
    Process the parsed options. Return triple of
    - return value (if program should be terminated, else None);
    - device name
    - interface string
    """
    args.F_CPU = int(args.F_CPU.rstrip('UL'))

    if args.cmd:
        portcmd : list[str] = [c for c in args.cmd if 'gdb_port' in c]
        if portcmd:
            cmd : str = portcmd[0]
            args.port = int(cmd[cmd.index('gdb_port')+len('gdb_port'):])

    if args.tool:
        args.tool = args.tool.strip()

    if args.dev:
        args.dev = args.dev.strip()

    manage :list[str] = []
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

    if args.clkprg < 0 or args.clkdeb < 0 or (args.kbps and args.kbps < 0):
        print("Negative frequency or communication speed values are discouraged")
        return 1, "", ""

    device : str = args.dev

    if not device and not args.reboot:
        print("Please specify target MCU with -d option")
        return 1, "", ""
    if device:
        device = device.lower()
        if device not in dev_id:
            print("Device '%s' is not supported by PyAvrOCD" % device)
            return 1, "", ""
    else:
        return None, "", "" # We only want to reboot

    intf : list[str]
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
        return 1, "", ""
    if len(intf) == 1 and intf[0] not in dev_iface[dev_id[device]].lower():
        print ("Device '%s' does not have the interface '%s'" % (device, intf[0]))
        return 1, "", ""
    if len(intf) > 1:
        print("Debugging interface for device '%s' ambiguous: '%s'" % (device, intf))
        return 1, "", ""
    args.dev = device
    return None, device, intf[0]

def handle_simavr(args : argparse.Namespace, device : str) -> bool:
    """
    Checks whether simavr shall be started, and if so, will prepare the start, and will return
    with True when simavr exits. If simavr shall not be started, return False.
    """
    if not args.prg:
        return False
    args.prg = args.prg.strip()
    if os.path.basename(args.prg) != 'simavr':
        return False
    prg : str = shutil.which(args.prg)
    if not prg:
        print("Could not find program '%s'" % args.prg)
        return True
    prg = os.path.abspath(prg)
    simavr_args = [ "-g", str(args.port), "-f", str(args.F_CPU), "-m", device ]
    if args.xarg:
        simavr_args += args.xarg
    print("Simavr starts: %s" %  " ".join([ prg ] + simavr_args), flush=True)
    print("Listening on port %d for gdb connection" % args.port, flush=True)
    sim : subprocess.Popen = subprocess.Popen( [ prg ] + simavr_args, bufsize=0, shell=False)
    sim.wait()
    return True

def check_elf_file_for_relax_optimization(elf_file : str, logger : logging.Logger) -> bool:
    """
    Checks whether the program had been compiled with the -mrelax optimization option.
    If so, it spits out a critical log message and returns True.
    Otherwise, it will return False.
    """
    logger.debug("Checking ELF %s file for -mrelax", elf_file)
    if elf_file is None:
        return False
    try:
        with open (elf_file, 'rb') as f:
            ef = ELFFile(f)
            dwarfinfo = ef.get_dwarf_info()
            for cu in dwarfinfo.iter_CUs():
                for die in cu.iter_DIEs():
                    for attr in die.attributes.values():
                        if 'DW_AT_producer' in attr.name:
                            logger.debug("Command line of producer: %s", attr.value.decode('ascii'))
                            if '-mrelax' in  attr.value.decode('ascii'):
                                logger.critical("Cannot debug programs compiled with '-mrelax'")
                                return True
    except FileNotFoundError:
        logger.error("ELF file '%s' not found", elf_file)
        return False
    except Exception as e:
        logger.error("Could not read ELF file '%s' because '%s'", elf_file, str(e))
        return False
    return False

def startup_helper_prog(args : argparse.Namespace, logger : logging.Logger) -> None:
    """
    Starts program requested by user, e.g., a debugger GUI
    """
    if args.prg and args.prg != "nop":
        args.prg = args.prg.strip()
        prg : str = shutil.which(args.prg)
        if prg:
            prg = os.path.abspath(prg)
            logger.info("Starting %s", prg)
            subprocess.Popen(prg)
        else:
            logger.critical("Could not find program '%s'", args.prg)
            sys.exit(1)

def run_server(server: RspServer, logger : logging.Logger) -> int:
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

EDBG_PRODUCTS : dict[int, str] = { 0x2140 : 'jtagice3', 0x2141 : 'atmelice', 0x2144 : 'powerdebugger',
                                   0x2111 : 'edbg', 0x2169 : 'edbg', 0x2145 : 'medbg', 0x2175 : 'nedbg',
                                   0x2FC0 : 'nedbg', 0x2177 : 'pickit4', 0x2180 : 'snap' }
EDBG_TOOLS : frozenset[str] = frozenset(EDBG_PRODUCTS.values())
JTAG2_TOOLS : frozenset[str] = frozenset(jtag2.PRODUCTS.values())
REENUMERATION_WAIT : float = 5.0   # s, see find_probe

def find_probe(args : argparse.Namespace, intf : str,
                   logger : logging.Logger) -> tuple[bool, ProbeCandidate | None]:
    """
    The probe to debug with. Returns (abort, probe); abort is True if there is none or the choice is
    ambiguous, after the reason has been logged. First the probes on USB, EDBG tools (HID) and
    JTAGICE mkII / AVR Dragon (bulk) alike: one of them is taken if it is the only one, -t and -u
    narrowing the choice. Only if there is none on USB, or -t or -u mean a serial port, dw-link is
    looked for there.
    A JTAGICE mkII or AVR Dragon leaves the bus for 1.5 to 3 s after every sign-off, avrdude's at the
    end of an upload too, and a server started right after it would not find the probe. So, with
    nothing on USB, wait for it up to REENUMERATION_WAIT seconds, unless the selection rules it out
    (an EDBG tool, which does not do this, or a serial port; the wait would cost every dw-link start).
    """
    serial_meant : bool = args.tool == 'dwlink' or \
      (bool(args.serialnumber) and serial_port_with_suffix(args.serialnumber))
    found : list[ProbeCandidate] = []
    libusb : bool = True
    if args.tool != 'dwlink':
        wait : bool = not serial_meant and args.tool not in EDBG_TOOLS
        deadline : float = time.monotonic() + (REENUMERATION_WAIT if wait else 0)
        while True:
            found, libusb = usb_probes(args, logger)
            if found or time.monotonic() >= deadline:
                break
            time.sleep(0.3)
    if len(found) == 1:
        return False, found[0]
    if len(found) > 1:
        logger.critical("More than one compatible tool! Use -t or -u to select.")
        for c in found:
            logger.critical(" Tool: %s, SN: %s", c.product, c.address)
        return True, None
    lacking_rules : bool = not serial_meant and lacking_udev_rules(logger)   # always ask: it explains
    if lacking_rules or (args.tool is not None and args.tool != 'dwlink'):
        logger.critical("No compatible tool discovered")
        explain_missing_probe(args, libusb, logger)
        return True, None
    return find_dwlink(args, intf, logger, lambda: explain_missing_probe(args, libusb, logger))

def usb_probes(args : argparse.Namespace, logger : logging.Logger) -> tuple[list[ProbeCandidate], bool]:
    """
    The probes on USB that -t and -u allow, and whether libusb is there. The EDBG tools are found
    through hidapi and do not need it; JTAGICE mkII and AVR Dragon do.
    """
    found : list[ProbeCandidate] = []
    if args.tool is None or args.tool in EDBG_TOOLS:
        found += [ProbeCandidate(tool=args.tool or EDBG_PRODUCTS.get(t.product_id, 'edbg'),
                                     product=t.product_string, address=t.serial_number)
                  for t in pymcuprog.backend.Backend().get_available_hid_tools(
                      serialnumber_substring=args.serialnumber or '', tool_name=args.tool)]
    libusb : bool = True
    if args.tool is None or args.tool in JTAG2_TOOLS:
        try:
            # without a serial number, the probe cannot be opened either (Linux without udev rules)
            found += [c for c in jtag2.discover(args.tool) if c.address and
                      (not args.serialnumber or c.address.lower().endswith(args.serialnumber.lower()))]
        except usb.core.NoBackendError:
            logger.debug("No libusb, cannot look for JTAGICE mkII / AVR Dragon")
            libusb = False
    return found, libusb

def lacking_udev_rules(logger : logging.Logger) -> bool:
    """
    Linux: is there a probe on USB that this user may not open? libusb lists it all the same, but
    hidapi leaves an EDBG tool out, and the serial number of a JTAGICE mkII / AVR Dragon cannot be
    read. If so, say how to install the udev rules.
    """
    if platform.system() != 'Linux':
        return False
    try:
        edbg_on_bus = [d for d in usb.core.find(find_all=True, idVendor=0x3EB) if d.idProduct in EDBG_PRODUCTS]
        lacking = any(not c.address for c in jtag2.discover()) or \
          len(pymcuprog.backend.Backend().get_available_hid_tools()) < len(edbg_on_bus)
    except (usb.core.NoBackendError, usb.core.USBError):
        return False
    if lacking:
        logger.critical("Perhaps you need to install the udev rules first:")
        logger.critical("Download https://pyavrocd.io/99-edbg-debuggers.rules,")
        logger.critical("review, edit, and install under /etc/udev/rules.d/.")
    return lacking

def explain_missing_probe(args : argparse.Namespace, libusb : bool, logger : logging.Logger) -> None:
    """After 'No compatible tool discovered': why a JTAGICE mkII or AVR Dragon may not have been seen"""
    if args.tool is not None and args.tool not in JTAG2_TOOLS:
        return
    if platform.system() == 'Windows':
        logger.warning("A JTAGICE mkII or AVR Dragon needs a libusb driver, e.g., WinUSB, installed with Zadig;")
        logger.warning("on Windows on Arm, they cannot be used")
    elif not libusb:
        logger.warning("A JTAGICE mkII or AVR Dragon needs libusb: %s",
                           "'brew install libusb'" if platform.system() == 'Darwin'
                           else "'sudo apt install libusb-1.0-0'")

def find_dwlink(args : argparse.Namespace, intf : str, logger : logging.Logger,
                    explain : Callable[[], None] = lambda: None) -> tuple[bool, ProbeCandidate | None]:
    """
    dw-link on a serial port. Returns (abort, probe) like find_probe. Which serial port is dw-link
    only the sign-on tells, and opening a port resets an Arduino; so the probe is taken only if
    exactly one USB serial port is there, or -u names one by the end of its name. 'explain' adds
    to 'No compatible tool discovered' why a probe on USB may have been missed.
    """
    if intf and intf != 'debugwire':   # no interface: no device, only --reboot-debugger
        if args.tool == "dwlink":
            logger.critical("dw-link can only debug debugWIRE targets")
        else:
            logger.critical("No compatible tool discovered")
            explain()
        return True, None
    if args.baud not in jtag2.BAUD_CODES:
        logger.critical("--dw-link-baud: %d bps is not possible, choose one of %s", args.baud,
                            ", ".join(str(b) for b in sorted(jtag2.BAUD_CODES)))
        return True, None
    found = [c for c in dwlinkbackend.discover()
             if not args.serialnumber or c.address.lower().endswith(args.serialnumber.lower())]
    if not found:
        logger.critical("No compatible tool discovered")
        explain()
        return True, None
    if len(found) > 1:
        logger.critical("More than one serial port; name the one of dw-link with -u, e.g., -u %s",
                            found[0].address.split('/')[-1])
        for c in found:
            logger.critical(" Port: %s", c.address)
        return True, None
    return False, found[0]

def serial_port_with_suffix(suffix : str) -> bool:
    """Is there a USB serial port whose name ends in suffix (where dw-link may be)?"""
    return any(c.address.lower().endswith(suffix.lower()) for c in dwlinkbackend.discover())

#pylint: disable=too-many-branches
def startup(command_line : list[str], logger : logging.Logger) -> int:
    """
    Configures the CLI, connects to a tool, and starts debugger
    """
    log_rsp : bool = False # will becomce true when verbosity is 'all'

    args : argparse.Namespace = options(command_line)

    # verbose option 'all' is a special one
    if args.verbose == "all":
        log_rsp = True
        args.verbose = "debug"

    # set up logging
    setup_logging(args, log_rsp)

    # process arguments
    result : int | None
    device : str
    intf : str
    result, device, intf = process_arguments(args, logger)
    if result is not None:
        return result

    # check whether simavr should be started, and if so, do that exclusively
    if device and handle_simavr(args, device):
        return 0 # returning after simavr has finished

    # now report startup
    logger.info("This is PyAvrOCD version %s", importlib.metadata.version("pyavrocd"))

    # check that ELF file has not been produced using the -mrelax option
    if check_elf_file_for_relax_optimization(args.elffile, logger):
        return 1

    abort, probe = find_probe(args, intf, logger)
    if abort or probe is None:
        return 1
    if probe.tool in JTAG2_TOOLS:
        logger.info("Connected to %s, SN: %s", probe.product, probe.address)
        return reboot_or_serve(Jtag2Backend, probe, lambda: Jtag2Backend(probe, device, intf, args),
                                   device, intf, args, probe.product, logger)
    if probe.tool == 'dwlink':
        logger.info("Using dw-link on %s", probe.address)
        return reboot_or_serve(DwlinkBackend, probe, lambda: DwlinkBackend(probe, device, intf, args),
                                   device, intf, args, probe.product, logger)

    backend : pymcuprog.backend.Backend = pymcuprog.backend.Backend()
    tool : ToolUsbHidConnection = ToolUsbHidConnection(serialnumber=probe.address, tool_name=args.tool)
    # Now try to connect
    try:
        toolname : str = "Unknown tool"
        backend.connect_to_tool(tool)
        toolname = backend.transport.hid_device.get_product_string()
        tool.serialnumber = backend.transport.hid_device.get_serial_number_string()
        logger.info("Connected to %s, SN: %s", toolname, tool.serialnumber)
    except (PymcuprogToolConnectionError, OSError, pyedbglib.protocols.avrcmsisdap.AvrCommandError) as e:
        if "open failed" in str(e):
            logger.critical("Debug probe busy, cannot connect")
        else:
            logger.critical("Could not connect to debug probe: %s", str(e))
        return 1

    # tool is connected, now we can start
    return reboot_or_serve(EdbgBackend, EdbgProbe(backend, tool),
                               lambda: EdbgBackend(backend.transport, device, intf, args),
                               device, intf, args, toolname, logger)

#pylint: disable=too-many-positional-arguments,too-many-arguments
def reboot_or_serve(backend_class : type[DebugBackend], candidate : Any,
                        make_backend : Callable[[], DebugBackend], device : str, intf : str,
                        args : argparse.Namespace, toolname : str, logger : logging.Logger) -> int:
    """
    --reboot-debugger first, if asked for; then serve, unless there is no device, which means that
    only a reboot was wanted. 'candidate' is what backend_class.reboot_probe needs to find the probe.
    """
    if args.reboot:
        if not backend_class.reboot_probe(candidate, args, logger):
            return 1
        if not device:
            logger.info("Terminating ...")
            return 0
    return serve(make_backend, device, intf, args, toolname, logger)

#pylint: disable=too-many-positional-arguments,too-many-arguments
def serve(make_backend : Callable[[], DebugBackend], device : str, intf : str,
              args : argparse.Namespace, toolname : str, logger : logging.Logger) -> int:
    """
    Create the backend for the connected tool and run the GDB server with it
    """
    logger.info("Starting GDB server")
    try:
        avrdebugger = make_backend()
        if args.debugwire:
            if intf != 'debugwire':
                if args.debugwire[0] == 'd':
                    logger.critical("Cannot disable debugWIRE on %s target", intf)
                    return 1
                logger.warning("Ignoring --debugwire option on %s target", intf)
            else:
                if args.debugwire[0] == 'd' and intf == 'debugwire':
                    try:
                        avrdebugger.cold_dw_disable()
                    finally:
                        avrdebugger.release() # as the server does at its end, also after an error
                    return 0
        server = RspServer(avrdebugger, device, args, toolname)
    except Exception as e:
        if logger.getEffectiveLevel() != logging.DEBUG:
            logger.critical("Fatal Error: %s",e)
            return 1
        raise
    startup_helper_prog(args, logger)
    return run_server(server, logger)

def main() -> int:
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
