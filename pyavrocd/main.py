"""
AVR GDB Server
"""

# args, logging
import platform
import importlib.metadata
import sys
import os
import argparse
import logging
import textwrap
import shutil
import shlex
import subprocess
from logging import getLogger


# utilities
import time

# communication
import socket
import select
import usb

# debugger modules
import pymcuprog
from pyedbglib.hidtransport.hidtransportfactory import hid_transport
from pymcuprog.backend import Backend
from pymcuprog.pymcuprog_main import  _clk_as_int # _setup_tool_connection
from pymcuprog.toolconnection import ToolUsbHidConnection, ToolSerialConnection

from pyavrocd import dwlink
from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.handler import GdbHandler
from pyavrocd.errors import  EndOfSession
from pyavrocd.deviceinfo.devices.alldevices import dev_id, dev_iface


class AvrGdbRspServer():
    """
    This is the GDB RSP server, setting up the connection to the GDB, reading
    and responding, and terminating. The important part is calling the handle_data
    method of the handler.
    """
    def __init__(self, avrdebugger, devicename, port):
        self.avrdebugger = avrdebugger
        self.devicename = devicename
        self.port = port
        self.logger = getLogger("AvrGdbRspServer")
        self.connection = None
        self.gdb_socket = None
        self.handler = None
        self.address = None

    def serve(self):
        """
        Serve away ...
        """
        self.gdb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.info("Listening on port %s for gdb connection", self.port)
        # make sure that this message can be seen
        if self.logger.getEffectiveLevel() not in {logging.DEBUG, logging.INFO}:
            print("Listening on port {} for gdb connection".format(self.port))
        self.gdb_socket.bind(("127.0.0.1", self.port))
        self.gdb_socket.listen()
        self.connection, self.address = self.gdb_socket.accept()
        self.connection.setblocking(0)
        self.logger.info('Connection from %s', self.address)
        self.handler = GdbHandler(self.connection, self.avrdebugger, self.devicename)
        while True:
            ready = select.select([self.connection], [], [], 0.5)
            if ready[0]:
                data = self.connection.recv(8192)
                if len(data) > 0:
                    # self.logger.debug("Received over TCP/IP: %s",data)
                    self.handler.handle_data(data)
            self.handler.poll_events()


    def __del__(self):
        try:
            if self.avrdebugger and self.avrdebugger.device:
                self.avrdebugger.stop_debugging()
        except Exception as e:
            if self.logger.getEffectiveLevel() == logging.DEBUG:
                self.logger.debug("Graceful exception during stopping: %s",e)
                # raise
            else:
                pass
        finally:
            # sleep 0.5 seconds before closing in order to allow the client to close first
            time.sleep(0.5)
            self.logger.info("Closing socket")
            if self.gdb_socket:
                self.gdb_socket.close()
            self.logger.info("Closing connection")
            if self.connection:
                self.connection.close()



def _setup_tool_connection(args, logger):
    """
    Copied from pymcuprog_main and modified so that no messages printed on the console
    """
    toolconnection = None

    # Parse the requested tool from the CLI
    if args.tool == "uart":
        baudrate = _clk_as_int(args)
        # Embedded GPIO/UART tool (eg: raspberry pi) => no USB connection
        toolconnection = ToolSerialConnection(serialport=args.uart,
                                                  baudrate=baudrate, timeout=args.uart_timeout)
    else:
        usb_serial = args.serialnumber
        product = args.tool
        if usb_serial and product:
            logger.info("Connecting to {0:s} ({1:s})'".format(product, usb_serial))
        else:
            if usb_serial:
                logger.info("Connecting to any tool with USB serial number '{0:s}'".\
                                format(usb_serial))
            elif product:
                logger.info("Connecting to any {0:s}".format(product))
            else:
                logger.info("Connecting to anything possible")
        toolconnection = ToolUsbHidConnection(serialnumber=usb_serial, tool_name=product)

    return toolconnection


def options():
    """
    Option processing. Returns a pair of processed options and unknown options.
    """
    parser = argparse.ArgumentParser(usage="%(prog)s [options]",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent('''\n\
        GDB server for AVR MCUs
            '''))

    parser.add_argument("-c", "--command",
                            action='append',
                            dest='cmd',
                            type=str,
                            help="Command to set gdb port (OpenOCD style)")

    parser.add_argument("-d", "--device",
                            dest='dev',
                            type=str,
                            help="Device to debug")

    parser.add_argument('-g', '--gede',  action="store_true",
                            help='Start Gede debugger GUI')

    parser.add_argument("-i", "--interface",
                            type=str,
                            choices=['debugwire', 'jtag', 'pdi', 'updi'],
                            help="Debugging interface to use")

    parser.add_argument('-p', '--port',  type=int, default=2000, dest='port',
                            help='Local port on machine (default 2000)')

    parser.add_argument('-s', '--start',  dest='prg',
                            help='Start specified program or "noop"')

    parser.add_argument("-t", "--tool",
                            type=str,
                            choices=['atmelice', 'dwlink', 'edbg', 'jtagice3', 'medbg', 'nedbg',
                                          'pickit4', 'powerdebugger', 'snap'],
                            help="Tool to connect to")

    parser.add_argument("-u", "--usbsn",
                            type=str,
                            dest='serialnumber',
                            help="USB serial number of the unit to use")

    parser.add_argument("-v", "--verbose",
                            default="info", choices=['debug', 'info',
                                                         'warning', 'error', 'critical'],
                            help="Logging verbosity level")

    parser.add_argument("-V", "--version",
                            help="Print pyavrocd version number and exit",
                            action="store_true")

    if platform.system() == 'Linux':
        parser.add_argument("--install-udev-rules",
                                help="Install udev rules for Microchip hardware " +
                                "debuggers under /etc/udev/rules.d/",
                                action="store_true")
    # Parse args and return
    return parser.parse_known_args()

def install_udev_rules(logger):
    """
    Install the udev rules for all the debuggers. Necessary only under Linux
    """
    # These rules are added (under Linux only) when requested by the user"
    udev_rules= '''# JTAGICE3
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2140", MODE="0666"
# Atmel-ICE
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2141", MODE="0666"
# Power Debugger
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2144", MODE="0666"
# EDBG - debugger on Xplained Pro
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2111", MODE="0666"
# EDBG - debugger on Xplained Pro (MSD mode)
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2169", MODE="0666"
# mEDBG - debugger on Xplained Mini
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2145", MODE="0666"
# PKOB nano (nEDBG) - debugger on Curiosity Nano
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2175", MODE="0666"
# PKOB nano (nEDBG) in DFU mode - bootloader of debugger on Curiosity Nano
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2fc0", MODE="0666"
# MPLAB PICkit 4 In-Circuit Debugger
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2177", MODE="0666"
# MPLAB Snap In-Circuit Debugger
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2180", MODE="0666"'''

    logger.info("Will try to install udev rules")
    try:
        with open("/etc/udev/rules.d/99-edbg-debuggers.rules", "w", encoding='utf-8') as f:
            f.write(udev_rules)
    except Exception as e:
        logger.critical("Could not install the udev rules: %s", e)
        return 1
    logger.info("Udev rules have been successfully installed")
    return 0

def setup_logging(args):
    """
    Setup logging
    """
    if args.verbose:
        args.verbose = args.verbose.strip()
    if args.verbose.upper() in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
        form = "[%(levelname)s] %(message)s"
    else:
        form = "[%(levelname)s] %(name)s: %(message)s"
    logging.basicConfig(stream=sys.stderr,level=args.verbose.upper(), format = form)
    logger = getLogger()

    if args.verbose.lower() == "debug":
        getLogger('pyedbglib').setLevel(logging.INFO)
    if args.verbose.lower() != "debug":
        # suppress messages from hidtransport
        getLogger('pyedbglib.hidtransport.hidtransportbase').setLevel(logging.ERROR)
        # suppress spurious error messages from pyedbglib
        getLogger('pyedbglib.protocols').setLevel(logging.CRITICAL)
        # suppress errors of not connecting: It is intended!
        getLogger('pymcuprog.nvm').setLevel(logging.CRITICAL)
        # we do not want to see the "read flash" messages
        getLogger('pymcuprog.avr8target').setLevel(logging.ERROR)
    return logger

def process_arguments(args, logger):
    """
    Process the parsed options. Return triple of
    - return value (if program should be terminated, else None;
    - device name
    - interface string
    """
    if args.version:
        print("pyavrocd version {}".format(importlib.metadata.version("pyavrocd")))
        return 0,None,None

    if args.cmd:
        args.cmd = args.cmd
        portcmd = [c for c in args.cmd if 'gdb_port' in c]
        if portcmd:
            cmd = portcmd[0]
            args.port = int(cmd[cmd.index('gdb_port')+len('gdb_port'):])

    if args.dev:
        args.dev = args.dev.strip()

    if args.dev and args.dev == "?":
        if args.interface:
            print("Supported device with debugging interface '%s':" % args.interface)
            alldev = [x for x in sorted(dev_id) if args.interface in dev_iface[dev_id[x]].lower()]
        else:
            print("Supported devices:")
            alldev = sorted(dev_id)
        for d in alldev[:-1]:
            print(d,sep="",end=", ")
        if alldev:
            print(alldev[-1])
        else:
            print("None")
        return 0, None, None

    if hasattr(args, 'install_udev_rules') and args.install_udev_rules:
        return install_udev_rules(logger), None, None

    device = args.dev

    if not device:
        print("Please specify target MCU with -d option")
        return 1, None, None
    device = device.lower()

    if device not in dev_id:
        logger.critical("Device '%s' is not supported by pyavrocd", device)
        return 1, None, None

    if args.interface:
        intf = [args.interface]
    else:
        intf = [x for x in ['debugwire', 'jtag', 'pdi', 'updi']
                    if x in dev_iface[dev_id[device]].lower()]
    logger.debug("Device: %s", device)
    logger.debug("Possible interfaces: %s", intf)
    logger.debug("Interfaces of chip: %s",  dev_iface[dev_id[device]].lower())
    if not intf:
        logger.critical("Device '%s' does not have a compatible debugging interface", device)
        return 1
    if len(intf) == 1 and intf[0] not in dev_iface[dev_id[device]].lower():
        logger.critical("Device '%s' does not have the interface '%s'", device, intf[0])
        return 1
    if len(intf) > 1:
        logger.critical("Debugging interface for device '%s' ambiguous: '%s'", device, intf)
        return 1
    intf = intf[0]
    return None, device, intf

def startup_helper(args, logger):
    """
    Starts program requested by user, e.g., a debugger GUI
    """
    if args.gede:
        args.prg = "gede"
    if args.prg and args.prg != "noop":
        args.prg = args.prg.strip()
        logger.info("Starting %s", args.prg)
        cmd = shlex.split(args.prg)
        cmd[0] = shutil.which(cmd[0])
        subprocess.Popen(cmd)

def run_server(server, logger):
    """
    Startup server and serve until done.
    """
    try:
        server.serve()
    except (EndOfSession, SystemExit):
        logger.info("End of session")
        return 0
    except KeyboardInterrupt:
        logger.info("Terminated by Ctrl-C")
        return 1
    except (ValueError, Exception) as e:
        if logger.getEffectiveLevel() != logging.DEBUG:
            logger.critical("Fatal Error: %s",e)
            return 1
        raise
    return 0


def main():
    """
    Configures the CLI and parses the arguments, connects to a tool and starts debugger
    """
    no_backend_error = False # will become true when libusb is not found
    no_hw_dbg_error = False # will become true, when no HW debugger is found

    # Parse options
    args, unknown = options()

    # set up logging
    logger = setup_logging(args)

    if unknown:
        logger.warning("Unknown options: %s", ' '.join(unknown))

    result, device, intf = process_arguments(args, logger)
    if result is not None:
        return result


    if args.tool:
        args.tool = args.tool.strip()
    if args.tool == "dwlink":
        dwlink.main(args, intf) # if we return, then there is no HW debugger
        no_hw_dbg_error = True
        logger.critical("No hardware debugger discovered")
    else:
        # Use pymcuprog backend for initial connection here
        backend = Backend()
        toolconnection = _setup_tool_connection(args, logger)

        try:
            backend.connect_to_tool(toolconnection)
        except usb.core.NoBackendError as e:
            no_backend_error = True
            logger.critical("Could not connect to hardware debugger: %s", e)
            if platform.system() == 'Darwin':
                logger.critical("Install libusb: 'brew install libusb'")
                logger.critical("Maybe consult: " +
                                "https://github.com/greatscottgadgets/cynthion/issues/136")
            elif platform.system() == 'Linux':
                logger.critical("Install libusb: 'sudo apt install libusb-1.0-0'")
            else:
                logger.critical("This error should not happen!")
        except pymcuprog.pymcuprog_errors.PymcuprogToolConnectionError:
            dwlink.main(args, intf)
            no_hw_dbg_error = True
        finally:
            backend.disconnect_from_tool()

        transport = hid_transport()
        if len(transport.devices) > 1:
            logger.critical("Too many hardware debuggers connected")
        if len(transport.devices) == 0 and no_hw_dbg_error:
            logger.critical("No hardware debugger discovered")
        if not no_backend_error and not no_hw_dbg_error:
            transport.connect(serial_number=toolconnection.serialnumber,
                                product=toolconnection.tool_name)
            logger.info("Connected to %s", transport.hid_device.get_product_string())
        elif platform.system() == 'Linux' and no_hw_dbg_error and len(transport.devices) == 0:
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                path_to_prog, _ = os.path.split((sys._MEIPASS)[:-1]) #pylint: disable=protected-access
                path_to_prog +=  '/pyavrocd'
            else:
                path_to_prog = 'pyavrocd'
            logger.critical(("Perhaps you need to install the udev rules first:\n"
                             "'sudo %s --install-udev-rules'\n" +
                             "and then unplug and replug the debugger."), path_to_prog)

    if no_hw_dbg_error or no_backend_error:
        return 1

    logger.info("Starting GDB server")
    try:
        avrdebugger = XAvrDebugger(transport, device, intf)
        server = AvrGdbRspServer(avrdebugger, device, args.port)
    except Exception as e:
        if logger.getEffectiveLevel() != logging.DEBUG:
            logger.critical("Fatal Error: %s",e)
            return 1
        raise

    startup_helper(args, logger)

    return run_server(server, logger)

if __name__ == "__main__":
    sys.exit(main())
