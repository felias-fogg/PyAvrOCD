"""
Python AVR MCU debugger
"""
from typing import Any #pylint disable=unused-import
from collections.abc import Callable

# utilities
import time
import logging
import argparse

#edbg library
from pyedbglib.protocols.jtagice3protocol import Jtagice3ResponseError
from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.protocols.avrispprotocol import AvrIspProtocol #pylint: disable=unused-import
from pyedbglib.protocols.edbgprotocol import EdbgProtocol
from pyedbglib.protocols import housekeepingprotocol
from pyedbglib.hidtransport.hidtransportbase import HidTransportBase

# pymcuorig library
from pymcuprog.avrdebugger import AvrDebugger
from pymcuprog.deviceinfo import deviceinfo
from pymcuprog.nvmspi import NvmAccessProviderCmsisDapSpi, NvmAccessProviderCmsisDapAvr
from pymcuprog.pymcuprog_errors import PymcuprogToolConfigurationError,\
     PymcuprogNotSupportedError
from pymcuprog.utils import read_target_voltage, read_tool_info


from pyavrocd.xnvmdebugwire import XNvmAccessProviderCmsisDapDebugwire
from pyavrocd.xnvmmegaavrjtag import XNvmAccessProviderCmsisDapMegaAvrJtag
from pyavrocd.xnvmupdi import XNvmAccessProviderCmsisDapUpdi
from pyavrocd.errors import FatalError, EndOfSession
from pyavrocd.deviceinfo.devices.alldevices import dev_name

#pylint: disable=too-many-public-methods,too-many-instance-attributes
class XAvrDebugger(AvrDebugger):
    """
    AVR debugger wrapper extension
    """
    #pylint: disable=super-init-not-called,too-many-positional-arguments
    def __init__(self, transport : HidTransportBase,
                     devicename : str,
                     iface : str,
                     args : argparse.Namespace) -> None:
        """
        We do not want to make use of the base class' init method,
        because all startup code is collected in the start_debugging method!
        """
        self.logger : logging.Logger = logging.getLogger(__name__)
        self.transport : HidTransportBase = transport
        self._devicename : str = devicename
        self._iface : str = iface
        self.bad_pc_bit_mask : int = 0
        self.manage : list[ str ] = [ ]
        self.clkprg : int = args.clkprg # JTAG programming clock frequency
        self.clkdeb : int = args.clkdeb # JTAG debug clock frequency
        self.kbps : int = args.kbps # UPDI/PDI communication speed limit
        self.timers_run : bool = args.timers[0]=='r'
        self.args : argparse.Namespace = args
        self._hwbpnum : int = 0
        self._architecture : str = ""
        self._sregaddr : int = 0
        self._iooffset : int = 0
        self._nolock : int = 0
        self.device_info : dict[str, Any ] = {}
        self.memory_info : deviceinfo.DeviceMemoryInfo | None = None
        self.flashmemtype : int = 0
        self.spidevice : NvmAccessProviderCmsisDapSpi | None = None
        self.device : NvmAccessProviderCmsisDapAvr
        self.edbg_protocol : EdbgProtocol | None = None
        self.housekeeper : housekeepingprotocol.Jtagice3HousekeepingProtocol | None = None
        self.use_events_for_run_stop_state =  False # in order to avoid the timing glitch with ATmega32/Atmel-ICE
        # Caching general registers, will be updated when execution is resumed
        self._regfile : bytearray | None = None
        self._regsupd : bool = False

        # Gather device info
        # moved here so that we have mem + device info before the debug process starts
        try:
            self.logger.info("Looking for device %s", devicename)
            self.device_info = deviceinfo.getdeviceinfo("pyavrocd.deviceinfo.devices." + devicename)
        except ImportError:
            raise PymcuprogNotSupportedError("No device info for device: {}".format(devicename)) #pylint: disable=raise-missing-from
        self._architecture = str(self.device_info['architecture']).lower()
        if iface not in str(self.device_info['interface']).lower():
            raise PymcuprogToolConfigurationError("Incompatible debugging interface")

        # set ronly and wonly regs
        self.masked_registers : list[int] = self.device_info.get('masked_registers',[])
        self.ronly_registers : list[int] = self.device_info.get('ronly_registers',[])

        # Memory info for the device
        self.memory_info = deviceinfo.DeviceMemoryInfo(self.device_info)

        # Edbg protocol instance, necessary to access target power control
        if transport and transport.hid_device is not None:
            self.edbg_protocol = EdbgProtocol(transport)
            self.logger.debug("EdbgProtocol instance created")

        # Now attach the right NVM device and set other parameters
        if iface == "updi":
            self.manage = [ m for m in args.manage if m in [ 'lockbits', 'eesave' ]]
            self.device = XNvmAccessProviderCmsisDapUpdi(self.transport, self.device_info, manage=self.manage)
            self._hwbpnum = 2
            self._sregaddr = 0x3F
            self._iooffset = 0
            self._nolock = 0xC5
            self.flashmemtype = Avr8Protocol.AVR8_MEMTYPE_BOOT_FLASH_ATOMIC
        elif iface == "debugwire":
            self.manage = [ m for m in args.manage if m in [ 'lockbits', 'bootrst', 'dwen' ]]
            self.device = XNvmAccessProviderCmsisDapDebugwire(self.transport, self.device_info, manage=self.manage)
            self._hwbpnum = 1
            self._sregaddr = 0x5F
            self._iooffset = 0x20
            self._nolock = 0xFF
            self.flashmemtype =  Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE
        elif iface == "jtag" and self._architecture =="avr8":
            self.manage = [ m for m in args.manage if m in [ 'lockbits', 'bootrst', 'ocden', 'eesave' ]]
            self.device = XNvmAccessProviderCmsisDapMegaAvrJtag(self.transport, self.device_info, manage=self.manage)
            self._hwbpnum = 4
            self._sregaddr = 0x5F
            self._iooffset = 0x20
            self._nolock = 0xFF
            self.flashmemtype =  Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE

        self.logger.info("Nvm instance created, iface: %s, HWBPs: %d, arch: %s",
                              self._iface, self._hwbpnum, self._architecture)
        if self.manage == []:
            self.manage = [ 'none' ]
        self.logger.info("Managing fuses: %s", ", ".join(self.manage))

    def get_iface(self) -> str:
        """
        info about debugging interface
        """
        return self._iface

    def get_architecture(self) -> str:
        """
        info about architecture
        """
        return self._architecture

    def get_hwbpnum(self) -> int:
        """
        info about number of hardware breakpoints
        """
        return self._hwbpnum

    def get_sregaddr(self) -> int:
        """
        Address of SREG
        """
        return self._sregaddr

    def get_iooffset(self) -> int:
        """
        Returns offset to I/O registers, i.e., 0x20 for dw and JTAG, 0x00 for UPDI
        """
        return self._iooffset

    def get_devicename(self) -> str:
        """
        Returns devicename
        """
        return self._devicename

    def start_debugging(self, flash_data : bytes | None = None, warmstart : bool = False) -> bool:
        """
        Start the debug session, i.e., initialize everything and start the debug engine.
        A warm start will assume that the OCD has already been activated, and will gracefully
        fail if not. Warmstarts happen only with debugWIRE. Return False if unsuccessful.
        """
        _dummy = flash_data
        self.logger.info("Starting up debug session...")
        try:
            self.housekeeper = housekeepingprotocol.Jtagice3HousekeepingProtocol(self.transport)
            self.housekeeper.start_session()
            dap_info = read_tool_info(self.housekeeper)
            self.logger.info("Signed on to: %s FW: %s.%s.%s, HW: %s", dap_info['product'],
                                 dap_info['firmware_major'],
                                 dap_info['firmware_minor'],
                                 dap_info['build'], dap_info['hardware_rev'])
            self.device.avr.setup_debug_session(kbps=self.kbps,
                                                    clkprg=self.clkprg,
                                                    clkdeb=self.clkdeb,
                                                    timers_run=self.timers_run)
            self.logger.info("Session configuration communicated to tool")
            self.device.avr.setup_config(self.device_info)
            self.logger.info("Device configuration communicated to tool")
            dev_id : int = self._activate_interface(graceful=warmstart)
            if dev_id in [0,  0xFFFFFFFF]:
                raise FatalError("Could  not connect to target.")
            if self._iface == 'jtag' and dev_id & 0xFF != 0x3F:
                raise FatalError("Not a Microchip JTAG target")
        except EndOfSession:
            raise
        except Exception as e:
            if warmstart:
                self.logger.warning("Debug session not started: %s", str(e))
                if self.args.attach:
                    raise FatalError("Could not attach to OCD, because debugWIRE is not active.") #pylint: disable=raise-missing-from
                self.logger.warning("Try later with 'monitor debugwire enable'")
                return False
            raise FatalError("Debug session not started: %s" % str(e)) #pylint: disable=raise-missing-from
        try:
            self.device.avr.attach()
            self.stop() # If successful, OCDEN is already activated
        except Jtagice3ResponseError as e:
            self.logger.debug("Could not attach and stop MCU")
            if e.code == Avr8Protocol.AVR8_FAILURE_ILLEGAL_OCD_STATUS: # we need to set OCDEN
                self.logger.debug("Illegal OCD status, need to activate debugging")
                if self.args.attach:
                    raise FatalError("Could not attach to OCD because debugging is not yet activated") #pylint: disable=raise-missing-from
            elif e.code == Avr8Protocol.AVR8_FAILURE_OCD_LOCKED: # Chip is locked and needs to be unlocked
                self.logger.info("Chip is locked and needs to be erased")
                if self.args.attach:
                    raise FatalError("Could not attach to OCD because chip is locked") #pylint: disable=raise-missing-from
                self._erase_locked_updi_chip()
            else:
                raise e
        self._manage_fuses()
        self._verify_target(dev_id)
        self._check_attiny2313()
        self._check_stuck_at_one_pc()
        if not self.args.attach:
            self.reset()
        self.logger.info("... debug session startup done")
        return True

    def _erase_locked_updi_chip(self) -> None:
        """
        Erase a locked chip (UPDI only)
        """
        self._complain_if_no_lockbits_permission()
        self.device.avr.deactivate_physical()
        self.logger.info("Physical interface deactivated")
        self.device.avr.protocol.set_byte(Avr8Protocol.AVR8_CTXT_OPTIONS,
                                        Avr8Protocol.AVR8_OPT_CHIP_ERASE_TO_ENTER, 1)
        self.logger.info("Chip-erase key entry mechanism activated")
        self._activate_interface()
        self.device.avr.enter_progmode()
        self.switch_to_debmode()
        time.sleep(0.5) # needed for an attiny 1607
        self.logger.info("Switched to debug mode")
        if self.args.load == 'n': # if noinitialload is active, change to readbeforewrite
            self.args.load = 'r'

    def _manage_fuses(self) -> None:
        """
        After having attached to the OCD, set fuses if the
        MCU is not in debugging mode yet: Clear lockbits, unprogram BOOTRST,
        and program OCDEN. This is only useful for Mega JTAG targets.
        """
        if self._iface != 'jtag':
            return
        if self.args.attach: # we do not change fuses when we want only to attach!
            return
        self.switch_to_progmode()
        self.logger.info("Switched to programming mode")
        # clear lockbits if necessary
        self._handle_lockbits(self.read_lock_one_byte, self.device.erase)
        # unprogram BOOTRST fuse if necessary
        self._handle_bootrst(self.read_fuse_one_byte, self.write_fuse)
        if self.device_info.get('ocden_base') is not None:
            # program OCDEN
            ofuse_addr : int = self.device_info['ocden_base']
            ofuse_mask : int = self.device_info['ocden_mask']
            ofuse : bytes = self.read_fuse_one_byte(ofuse_addr)
            self.logger.debug("OCDEN read: 0x%X", ofuse[0] & ofuse_mask)
            if ofuse[0] & ofuse_mask == ofuse_mask: # only if OCDEN is not yet programmed
                if 'ocden' not in self.manage:
                    self.logger.warning("The fuse OCDEN is not managed by PyAvrOCD.")
                    self.logger.warning("In order to allow debugging, you need to program this fuse manually.")
                    self.logger.warning("Or let payavrocd manage this fuse: '-m ocden'.")
                    raise FatalError("Debugging is impossible because OCDEN cannot be programmed")
                newfuse = ofuse[0] & ~ofuse_mask & 0xFF
                self.write_fuse(ofuse_addr, bytearray([newfuse]))
                assert newfuse == self.read_fuse_one_byte(ofuse_addr)[0], "OCDEN could not be programmed"
                self.logger.info("OCDEN fuse has been programmed.")
            else:
                self.logger.info("OCDEN is already programmed")
            # now verify signature using signature bytes (they do not lie!)
            if not self.args.skipsig:
                idbytes : bytes = self.read_sig(0,3)
                sig : int = (idbytes[2]) + (idbytes[1]<<8) + (idbytes[0]<<16)
                self.logger.debug("Device signature expected: %X", self.device_info['device_id'])
                self.logger.debug("Device signature of connected chip: %X", sig)
                if sig != self.device_info['device_id']:
                    raise FatalError("Wrong MCU: '%s', expected: '%s'" %
                            (dev_name.get(sig,"Unknown"),
                            dev_name[self.device_info['device_id']]))
        self.switch_to_debmode()
        self.logger.info("Switched to debugging mode")

    def _verify_target(self, dev_id : int) -> None:
        """
        Check that the MCU we connected to has a device id returned by activate physical that
        is compatible with the type given as an argument when calling the server.
        """
        # list of pairs, where the first entry is a signature computed from the device id
        # and the second one is a possible alternative identity. For example, the first
        # pair signifies that a chip returning a device id corresponding to an atmega48p
        # could well be an atmega48a.
        comp_ids : tuple[ tuple[ int, int], ... ] = \
               ((0x1E920A, 0x1E9205), # pretends to be a 48PA, but is 48A
                (0x1E930F, 0x1E930A), # pretends to be a 88PA, but is 88A
                (0x1E940B, 0x1E9406), # pretends to be a 168PA, but is 168A
                (0x1E950F, 0x1E9514), # pretends to be a 328P, but is 328
                (0x1E9516, 0x1E9514), # pretends to be a 328PB, but is a 328
                (0x1E9516, 0x1E950F), # pretends to be a 328PB, but is a 328P
                (0x1E940A, 0x1E940F), # pretends to be a 164PA, but is a 164A
                (0x1E9511, 0x1E9515), # pretends to be a 324PA but is a 324A
                (0x1E960A, 0x1E9609), # pretends to be a 644PA, but is a 644A
                (0x1E9705, 0x1E9706), # pretends to be a 1284P, but is a 1284
                (0x1E9405, 0x1E9411), # pretends to be a 169PA, but is a 169A
                (0x1E950B, 0x1E9503), # pretends to be a 329PA but is a 329A
                (0x1E960B, 0x1E9603), # pretends to be a 649P, but is a 649A
                (0x1E950C, 0x1E9504), # pretends to be a 3290PA but is a 3290A
                (0x1E960C, 0x1E9604), # pretends to be a 6490P, but is a 6490A
                (0x1E9407, 0x1E9410), # pretends to be a 165PA, but is a 165A
                (0x1E950D, 0x1E9505), # pretends to be a 325PA but is a 325A
                (0x1E960D, 0x1E9605), # pretends to be a 645P, but is a 645A
                (0x1E950E, 0x1E9506), # pretends to be a 3250PA but is a 3250A
                (0x1E960E, 0x1E9606)) # pretends to be a 6450P, but is a 6450A
        sig : int
        if self.args.skipsig:
            return
        if self._iface == 'debugwire':
            sig = (0x1E<<16) + dev_id # derive a signature from the id returned from activate_physical for debugWIRE
        elif self._iface == 'jtag':
            sig = (0x1E<<16) + ((dev_id >> 12)&0xFFFF) # same thing for JTAG
        elif self._iface == 'updi':
            self.logger.debug("Trying to read device code")
            sig = int.from_bytes(self.read_sig(0, 3),'big')
            self.logger.info("UPDI device code: 0x%X", sig)
        else:
            raise FatalError("Unhandled debug interface")
        self.logger.debug("Device signature expected: %X", self.device_info['device_id'])
        self.logger.debug("Device signature of connected chip: %X", sig)
        if sig != self.device_info['device_id']:
            # Some funny special cases of chips pretending to be someone else
            # when in debugWIRE mode / JTAG mode
            if (sig, self.device_info['device_id']) not in comp_ids:
                raise FatalError("Wrong MCU: '%s' (signature: 0x%X), expected: '%s'" %
                        (dev_name.get(sig,"Unknown"), sig,
                        dev_name[self.device_info['device_id']]))
        self.logger.info("Device signature checked")

    def _check_stuck_at_one_pc(self) -> None:
        """
        Check that the connected MCU does not suffer from stuck-at-1-bits in the program counter.
        Currently, I only know of ATmega48, ATmega88, ATmega329, and ATmega3250. The two
        former ones cause other issues as well and are therefore considered undebuggable.
        For the latter two (and perhaps others), we simply remember the stuck bits
        and either apply them (when setting a hardeware breakpoint) or mask them out.

        There are a few others, such as ATmega16 and ATmega64, which push non-zero
        unused PC bits on the stack, but this will now be handled by GDB. So, when
        GDB retrieves return addresses from the stack, it will always mask out unused bits,
        provided the memory map has been communicated to GDB.
        """
        self.logger.info("Check for stuck bits in PC")
        pc : int = (super().program_counter_read()) << 1
        self.logger.debug("PC(byte)=0x%X",pc)
        if self.memory_info is None:
            raise FatalError("No memory info available")
        maxaddr : int = self.memory_info.memory_info_by_name('flash')['size'] - 1
        self.logger.debug("Maximal address: 0x%X", maxaddr)
        bitlen : int = maxaddr.bit_length()
        self.logger.debug("Bit length: %d", bitlen)
        mask = (1 << bitlen) - 1
        self.logger.debug("Mask for testing: 0x%X", mask)
        self.bad_pc_bit_mask = pc - (mask & pc)
        self.logger.debug("Bad pc bit mask: 0x%X", self.bad_pc_bit_mask)
        if self.bad_pc_bit_mask:
            self.logger.warning("MCU has non-zero unused bit in PC: 0x%X", self.bad_pc_bit_mask)

    def _check_attiny2313(self) -> None:
        """
        Distinguishes ATtiny2313 and ATtiny2313A by probing GIMSK. If a
        write of 0xFF reads b ack as 0xE0, it is a 2313, if it reads 0xF8,
        it is a 2313A.
        """
        if not self.device_info['name'].startswith("attiny2313") or self.args.skipsig:
            return
        savebyte : bytearray = self.sram_read(0x5B, 1)
        self.sram_write(0x5B, bytearray([0xFF]))
        readback : bytearray = self.sram_read(0x5B, 1)
        self.sram_write(0x5B, savebyte)
        if readback[0] == 0xE0 and self.device_info['name'] == "attiny2313a":
            pair = ("attiny2313", "attiny2313a")
        elif  readback[0] == 0xF8 and self.device_info['name'] == "attiny2313":
            pair = ("attiny2313a", "attiny2313")
        else:
            self.logger.info("Checked: Connected indeed to %s", self._devicename)
            return
        raise FatalError("Wrong MCU: %s. Expected: %s" % pair)

    def _activate_interface(self, graceful : bool = False) -> int:
        """
        Activate physical interface (perhaps trying twice)

        """

        try:
            use_reset : bool = 'edbg' not in self.transport.device.product_string.lower() and \
              not self.args.attach
            dev_id : bytes = self.device.avr.protocol.activate_physical(use_reset=use_reset)
            dev_code : int = (dev_id[3]<<24) + (dev_id[2]<<16) + (dev_id[1]<<8) + dev_id[0]
            self.logger.info("Physical interface activated: 0x%X", dev_code)
        except Jtagice3ResponseError as error:
            # The debugger could be out of sync with the target, retry
            if error.code == Avr8Protocol.AVR8_FAILURE_INVALID_PHYSICAL_STATE:
                self.logger.warning("Physical state out of sync. Retrying.")
                self.device.avr.deactivate_physical()
                self.logger.info("Physical interface deactivated")
                dev_id = self.device.avr.protocol.activate_physical(use_reset=use_reset)
                dev_code = (dev_id[3]<<24) + (dev_id[2]<<16) + (dev_id[1]<<8) + dev_id[0]
                self.logger.info("Physical interface activated. MCU id=0x%X", dev_code)
            elif error.code == Avr8Protocol.AVR8_FAILURE_DW_PHY_ERROR:
                if graceful:
                    raise FatalError("debugWIRE could not be activated") from error
                raise FatalError("debugWIRE not activated by power-cycling. Parasitic power supply?") \
                  from error
            elif error.code == Avr8Protocol.AVR8_FAILURE_CLOCK_ERROR:
                self.logger.warning("Communication clock failure. Retrying.")
                dev_id = self.device.avr.protocol.activate_physical(use_reset=use_reset)
                dev_code = (dev_id[3]<<24) + (dev_id[2]<<16) + (dev_id[1]<<8) + dev_id[0]
                self.logger.info("Physical interface activated. MCU id=0x%X", dev_code)
            else:
                raise error
        except KeyError as e:
            if str(e) == "4":
                self.logger.critical("Target not connected")
                raise EndOfSession("Terminating...") from e
            self.logger.error("KeyError: %s", str(e))
            raise e
        except Exception as e:
            self.logger.error("%s", str(e))
            raise e
        return dev_code

    def _handle_bootrst(self, read : Callable[[int], bytes],
                              write : Callable[[int, bytearray], bytearray | None]) -> None:
        """
        Unprogram bootrst (if permitted) for different settings (ISP amd JTAG).
        """
        if 'bootrst_base' in self.device_info:
            bfuse_addr : int = self.device_info['bootrst_base']
            bfuse_mask : int = self.device_info['bootrst_mask']
            bfuse : bytes = read(bfuse_addr)
            self.logger.debug("BOOTRST addr: 0x%X, mask: 0x%X", bfuse_addr,   bfuse_mask)
            self.logger.debug("BOOTRST fuse byte: 0x%X", bfuse[0])
            if bfuse[0] & bfuse_mask == 0: # if BOOTRST is programmed
                if 'bootrst' not in self.manage:
                    self.logger.warning("BOOTRST is not managed by PyAvrOCD and will therefore not be cleared.")
                    self.logger.warning("If you do not want to start in the boot loader, clear this fuse manually.")
                    self.logger.warning("Or let payavrocd manage this fuse: '-m bootrst'.")
                else:
                    newfuse : int = bfuse[0] | bfuse_mask
                    self.logger.debug("Writing new fuse byte: 0x%x", newfuse)
                    write(bfuse_addr, bytearray([newfuse]))
                    if self._iface == 'debugwire': #necessary because otherwise the read may fail
                        if self.spidevice is None:
                            raise FatalError("SPI module not initialized")
                        self.spidevice.isp.leave_progmode()
                        self.spidevice =  NvmAccessProviderCmsisDapSpi(self.transport, self.device_info)
                        self.logger.debug("Reconnected to SPI programming module")
                    bfuse = read(bfuse_addr)
                    self.logger.debug("BOOTRST fuse byte read: 0x%X", bfuse[0])
                    assert newfuse == bfuse[0], "BOOTRST could not be unprogrammed"
                    self.logger.info("BOOTRST fuse has been unprogrammed.")
            else:
                self.logger.info("BOOTRST was already unprogrammed")

    def _handle_lockbits(self, read : Callable[[], bytes],
                               erase : Callable[[], None]) -> None:
        """
        Clear lockbits (if permitted) for different settings (JTAG, ISP and UPDI)
        """
        trial : int = 0
        lockbits = read()
        self.logger.debug("Lockbits read: 0x%X", lockbits[0])
        if lockbits[0] == self._nolock:
            self.logger.info("MCU is not locked.")
            return
        self.logger.info("MCU is locked.")
        self._complain_if_no_lockbits_permission()
        while trial < 5: # usually, the 2nd attempt is successful
            time.sleep(0.1)
            erase()
            time.sleep(0.1)
            lockbits = read()
            self.logger.debug("Lockbits after erase: 0x%X", lockbits[0])
            if lockbits[0] == self._nolock:
                break
            trial += 1
        if trial < 5:
            self.logger.info("MCU has been erased and lockbits have been cleared.")
        else:
            raise FatalError("Impossible to clear lockbits")
        if self.args.load and self.args.load[0] == 'n':     # the 'no initial load' option value
            if self._iface == 'debugwire':
                self.args.load = 'r'     # for debugWIRE, the right one is 'read before write'
            elif self._iface == 'jtag':
                self.args.load = 'w'

    def _complain_if_no_lockbits_permission(self) -> None:
        if 'lockbits' not in self.manage:
            self.logger.warning("PyAvrOCD is not allowed to clear lockbits.")
            self.logger.warning("This must be done manually by erasing the chip.")
            self.logger.warning("Alternatively, let PyAvrOCD manage it: '-m lockbits'")
            raise FatalError("Debugging is impossible when lockbits are set.")

    def prepare_debugging(self, callback : Callable[[], bool] | None = None,
                                recognition : Callable[[], None] | None =None) -> None:
        """
        A function that prepares for starting a debug session. The only use case is
        for the debugWIRE interface, where we need to program the DWEN fuse using ISP.

        On the assumption that we are in ISP mode, the lockbits are cleared (if allowed),
        the BOOTRST fuse is unprogrammed (if allowed), and then DWEN is programmed (if allowed).
        After that, a power-cycle is performed and finally, we enter debugWIRE mode.
        If callback is Null or returns False, we wait for a manual power cycle.
        Otherwise, we assume that the callback function does the job.
        """
        if self._iface != 'debugwire':
            return
        self.logger.info("Prepare for debugWIRE debugging...")
        try:
            if read_target_voltage(self.housekeeper) < 1.5:
                raise FatalError("Target is not powered")
            if self.housekeeper is None:
                raise FatalError("Housekeeping module not initialized")
            self.housekeeper.start_session() # need to start a new session after reading target voltage
            self.logger.info("Signed on to tool")
            self.spidevice = NvmAccessProviderCmsisDapSpi(self.transport, self.device_info)
            self.logger.info("Connected to SPI programming module")
            device_id : int = int.from_bytes(self.spidevice.read_device_id(),byteorder='little')
            if self.device_info['device_id'] != device_id and not self.args.skipsig:
                raise FatalError("Wrong MCU: '%s' (Sig: %x), expected: '%s (Sig: %x)'" %
                        (dev_name.get(device_id,"Unknown"),
                        device_id,
                        dev_name[self.device_info['device_id']],
                        self.device_info['device_id']))
            self.spidevice.isp.leave_progmode()
            self.spidevice =  NvmAccessProviderCmsisDapSpi(self.transport, self.device_info)
            self.logger.debug("Reconnected to SPI programming module")
            self._handle_lockbits(self.spidevice.isp.read_lockbits, self.spidevice.erase)
            self._handle_bootrst(self.spidevice.isp.read_fuse_byte, self.spidevice.isp.write_fuse_byte)
            # program the DWEN bit
            dwen_addr : int = self.device_info['dwen_base']
            dwen_mask : int = self.device_info['dwen_mask']
            self.logger.debug("DWEN addr: 0x%X, DWEN mask: 0x%X", dwen_addr, dwen_mask)
            dwen_byte : bytes = self.spidevice.isp.read_fuse_byte(dwen_addr)
            self.logger.debug("DWEN fuse byte: 0x%X", dwen_byte[0])
            if dwen_byte[0] & dwen_mask != 0: # DWEN is not programmed!
                if 'dwen' not in self.manage:
                    self.logger.warning("The DWEN fuse is not managed by PyAvrOCD.")
                    self.logger.warning("Therefore, the fuse will not be programmed.")
                    self.logger.warning("In order to allow debugging, you need to program this fuse manually.")
                    self.logger.warning("Or let payavrocd manage this fuse: '-m dwen'.")
                    raise FatalError("Debugging is impossible when DWEN is not programmed.")
                if device_id in [ 0x1E9205, 0x1E930A ]:
                    self._check_atmega48_and_88(device_id)
                newfuse : int = dwen_byte[0] & (0xFF & ~(dwen_mask))
                self.logger.debug("New DWEN fuse: 0x%X", newfuse)
                self.logger.debug("Writing fuse byte: 0x%X", newfuse)
                self.spidevice.isp.write_fuse_byte(dwen_addr, bytearray([newfuse]))
                self.logger.info("DWEN fuse written")
            self.spidevice.isp.leave_progmode()
            self.logger.info("SPI programming terminated")
            # now you need to power-cycle
            self._power_cycle(callback=callback, recognition=recognition)
            # end current tool session and start a new one
        except Exception as e:
            self.logger.critical("%s", str(e))
            raise e
        finally:
            try:
                if self.spidevice is not None:
                    self.spidevice.isp.leave_progmode()
            except Exception:
                pass
            if self.housekeeper is not None:
                self.housekeeper.end_session()
                self.logger.info("Signed off from tool")
            self.logger.info("... preparation for debugWIRE debugging done")

    def _check_atmega48_and_88(self, device_id : int) -> None:
        """
        The ATmega48 and ATmega88 (without A or P suffix) have a dirty program counter
        and in addition get semi-bricked when trying to program the DWEN fuse. Even
        avrdude cannot resurrect them (but Studio and MPLABX have no problems). The
        only way to recognize them is through looking into the boot_signature, which
        however, is not accessible by SPI programming. So, we flash a short program for
        checking the boot_signature, run the program, and check the lock bits, where
        the result will be stored.
        """
        if self.args.skipsig:
            return
        self.logger.info("Test for dirty PC on ATmega48/88")
        # erase flash (and maybe EEPROM)
        if self.spidevice is None or  self.spidevice.isp is None:
            raise FatalError("SPI module is not initialized")
        self.spidevice.isp.erase()
        # change option value of 'load' option if necessary
        if self.args.load is None or self.args.load[0] == 'n': # the 'no initial load' option value
            self.args.load = 'r'     # for debugWIRE, the right one is 'read before write'
        # program flash with test program, depending on MCU type
        self.logger.debug("Flash test program")
        if self.memory_info is None:
            raise FatalError("No memory info")
        if device_id == 0x1E9205: # ATmega48(A)
            self.spidevice.write(self.memory_info.memory_info_by_name('flash'), 0,
                    bytearray.fromhex("19C02CC02BC02AC029C028C027C026C025C024C023C022C021C020C01FC01EC0" +
                                      "1DC01CC01BC01AC019C018C017C016C015C014C011241FBECFEFD2E0DEBFCDBF" +
                                      "14BE0FB6F894A89580916000886180936000109260000FBE02D014C0D1CF81E2" +
                                      "F0E0E0E08093570084918E3141F089E09EEFE1E0F0E0092E80935700E89590E0" +
                                      "80E00895F894FFCF"))
        else:
            self.spidevice.write(self.memory_info.memory_info_by_name('flash'), 0,
                    bytearray.fromhex("19CE2CCE2BCE2ACE29CE28CE27CE26CE25CE24CE23CE22CE21CE20CE1FCE1ECE" +
                                      "1DCE1CCE1BCE1ACE19CE18CE17CE16CE15CE14CEFFFFFFFFFFFFFFFFFFFFFFFF"))
            self.spidevice.write(self.memory_info.memory_info_by_name('flash'), 0x1C30,
                    bytearray.fromhex("FFFFFFFF11241FBECFEFD4E0DEBFCDBF14BE0FB6F894A8958091600088618093" +
                                      "6000109260000FBE02D018C0D1C181E2F0E0E0E08093570084918E3141F089E0" +
                                      "9BEFE1E0F0E0092E80935700E895E4E3F0E0E491E5B990E080E00895F894FFCF"))
        self.spidevice.isp.leave_progmode()
        # now wait a couple of milliseconds
        time.sleep(0.1)
        # start programming mode again and read result
        self.spidevice.isp.enter_progmode()
        self.logger.debug("Now check result")
        result_lockbits : bytes = self.spidevice.read(self.memory_info.memory_info_by_name('lockbits'), 0, 1)
        # Check result
        self.logger.debug("Result from lockbits: 0x%X",   result_lockbits[0])
        # Now erase chip again to clear lock bits
        self.spidevice.isp.erase()
        self.logger.debug("Chip erased!")
        # Check results
        if result_lockbits[0] != self._nolock:
            raise FatalError("MCU cannot be debugged because of stuck-at-1 bit in the PC")

    def _power_cycle(self, callback : Callable[[], bool] | None = None,
                           recognition : Callable[[], None] | None = None) -> None:
        """
        Ask user for power-cycle and wait for voltage to come up again.
        If callback is callable, we try that first. It might magically
        perform a power cycle.
        """
        wait_start : float = time.monotonic()
        last_message : float = 0
        magic : bool = False
        if callback is not None:
            magic = callback()
        if magic: # callback has done all the work
            return
        self.logger.info("Restarting the debug tool before power-cycling")
        if self.housekeeper is None:
            raise FatalError("Housekeeping module not initialized")
        self.housekeeper.end_session() # might be necessary after an unsuccessful power-cycle
        self.logger.info("Signed off from tool")
        while time.monotonic() - wait_start < 150:
            if time.monotonic() - last_message > 20:
                self.logger.warning("*** Please power-cycle the target system ***")
                last_message = time.monotonic()
            if read_target_voltage(self.housekeeper) < 0.5:
                wait_start = time.monotonic()
                self.logger.info("*** Power-down recognized. Apply power again! ***")
                if recognition is not None:
                    recognition()
                while  read_target_voltage(self.housekeeper) < 1.5 and \
                  time.monotonic() - wait_start < 20:
                    time.sleep(0.1)
                if read_target_voltage(self.housekeeper) < 1.5:
                    raise FatalError("Timed out waiting for repowering target")
                time.sleep(1) # wait for debugWIRE system to be ready to accept connections
                self.housekeeper.start_session()
                self.logger.info("Signed on to tool again")
                return
            time.sleep(0.1)
        raise FatalError("Timed out waiting for power-cycle")

    # Cleanup code for detaching from target
    def stop_debugging(self, skip : bool = False, leave : bool = False, graceful : bool = True) -> None:
        """
        Stop the debug session and clean up in a safe way.
        skip: if true, skip the debugging-leave and fuse-programming parts (when we could not connect)
        leave: if true, leave debugging mode and unprogram the respective fuse
        graceful: do not talk about occurring exceptions
        """
        self.logger.info("Terminating debugging session ...")
        try:
            # Switch to debugging mode
            try:
                self.switch_to_debmode()
                self.logger.info("Switched to debugging mode")
            except Exception:
                self.logger.info("Already in debugging mode")
            # Halt the core
            self.stop()
            self.logger.info("AVR core stopped")
            # Remove all software breakpoints
            self.device.avr.protocol.software_breakpoint_clear_all()
            self.logger.info("All software breakpoints removed")
            # Remove all hardware  breakpoints
            self.device.avr.breakpoint_clear()
            self.logger.info("All hardware breakpoints removed")
            # Continue executing
            self.run()
            self.logger.info("CPU resumes execution")
        except Exception as e:
            if not graceful:
                self.logger.error("Error during stopping core and removing BPs: %s", str(e))
        # if JTAG, disable OCDEN fuse
        if self._iface == 'jtag' and not skip:
            self._ocden_unprogramming(leave)
        # if debugWIRE, disable dw mode
        try:
            if self._iface == "debugwire" and leave and not skip:
                self.device.avr.protocol.debugwire_disable()
                self.logger.info("DebugWIRE mode disabled")
        except Exception as e:
            if not graceful:
                self.logger.error("Error during disabling debugWIRE mode: %s", str(e))
        # Detach from the OCD
        try:
            self.device.avr.protocol.detach()
            self.logger.info("Detached from OCD")
        except Exception as e:
            if not graceful:
                self.logger.error("Error during detaching from OCD: %s", str(e))
        # De-activate physical interface
        try:
            self.device.avr.deactivate_physical()
            self.logger.info("Physical interface deactivated")
        except Exception as e:
            if not graceful:
                self.logger.error("Error during deactivating interface: %s", str(e))
        # Sign off device
        try:
            if self.housekeeper is not None:
                self.housekeeper.end_session()
                self.logger.info("Signed off from tool")
        except Exception as e:
            if not graceful:
                self.logger.error("Error while signing off from tool: %s", str(e))
        # if debugWIRE, disable DWEN
        if self._iface == 'debugwire' and not skip:
            self._dwen_unprogramming(leave)
        self.logger.info("... terminating debugging session done")


    def _ocden_unprogramming(self, leave : bool) -> None:
        """
        Unprogram OCDEN fuse if allowed and possible
        """
        if not leave:
            self.logger.info("OCDEN is not cleared because 'atexit' is set to 'stay'")
            return
        if 'ocden' not in self.manage:
            self.logger.warning("OCDEN cannot be disabled since this fuse is not managed by PyAvrOCD")
            self.logger.warning("In order to let payavrocd manage this fuse use: '-m ocden'.")
            return
        try:
            # Disable OCDEN
            self.switch_to_progmode()
            self.logger.info("Switched to programming mode")
            fuses : bytearray = self.read_fuse(0, 3)
            self.logger.debug("Fuses read: %X %X %X",fuses[0], fuses[1], fuses[2])
            ofuse_addr : int = self.device_info['ocden_base']
            ofuse_mask : int = self.device_info['ocden_mask']
            self.write_fuse(ofuse_addr, bytearray([fuses[ofuse_addr] | ofuse_mask]))
            self.logger.info("OCDEN unprogrammed")
        except Exception as e:
            self.logger.error("Error during unprogramming OCDEN: %s", str(e))
        self.device.avr.protocol.leave_progmode()
        self.logger.info("Programming mode terminated")


    def _dwen_unprogramming(self, leave : bool) -> None:
        """
        Unprogram DWEN fuse if allowed and possible
        """
        if not leave:
            return
        if 'dwen' not in self.manage:
            self.logger.warning("DWEN cannot be disabled since this fuse is not managed by PyAvrOCD")
            self.logger.warning("Disable this fuse before switching the power of the MCU off!")
            self.logger.warning("In order to let payavrocd manage this fuse use: '-m dwen'.")
            return
        try:
            self.housekeeper = housekeepingprotocol.Jtagice3HousekeepingProtocol(self.transport)
            self.housekeeper.start_session()
            self.logger.info("Signed on to tool again")
            # now open an ISP programming session again
            self.logger.info("Reconnecting in SPI programming mode")
            self.spidevice = NvmAccessProviderCmsisDapSpi(self.transport, self.device_info)
            self.spidevice.isp.enter_progmode()
            self.logger.info("Entered SPI programming mode")
            dwen_addr : int = self.device_info['dwen_base']
            dwen_mask : int = self.device_info['dwen_mask']
            dwen_byte : bytearray = self.spidevice.isp.read_fuse_byte(dwen_addr)
            self.logger.debug("DWEN byte: 0x%X", dwen_byte[0])
            dwen_byte[0] |= dwen_mask
            self.logger.debug("New DWEN byte: 0x%X", dwen_byte[0])
            self.spidevice.isp.write_fuse_byte(dwen_addr, dwen_byte)
            self.logger.info("Unprogrammed DWEN fuse")
            self.spidevice.isp.leave_progmode()
            self.logger.info("SPI programming terminated")
            self.housekeeper.end_session()
            self.logger.info("Signed off from tool")
        except Exception as e:
            self.logger.error("Error during unprogramming DWEN: %s", str(e))

    def cold_dw_disable(self) -> None:
        """
        Disable debugWIRE mode without connecting to a debugger. This will only be successful if
        we can access the chip using the debugWIRE protocol.
        """
        if self._iface != 'debugwire':
            raise FatalError("This is not a debugWIRE target!")
        if not self.start_debugging(warmstart=True):
            self.logger.error("Cannot connect to target using the debugWIRE command")
            self.logger.error("MCU is probably already in normal state")
            return
        self.stop_debugging(leave=True, graceful=False)

    def switch_to_debmode(self) -> bool:
        """
        Switch to debugging mode
        """
        return self.device.avr.switch_to_debmode()

    def switch_to_progmode(self) -> bool:
        """
        Switch to programming mode
        """
        return self.device.avr.switch_to_progmode()

    def software_breakpoint_set(self, address : int) -> bool:
        """
        This is a version of setting a software breakpoint that
        catches exceptions.
        """
        try:
            super().software_breakpoint_set(address)
        except Exception as e:
            self.logger.error("Could not set software breakpoint: %s", str(e))
            return False
        return True

    #pylint: disable=arguments-differ
    #we actually need two arguments when more than one HWBP is there
    def hardware_breakpoint_set(self, ix : int, address : int) -> bytes | None:
        """
        Set a hardware breakpoint at address
        """
        return self.device.avr.hardware_breakpoint_set(ix, address | self.bad_pc_bit_mask)

    #pylint: disable=arguments-differ
    #we actually need the extra argument when more than one HWBP is there
    def hardware_breakpoint_clear(self, ix : int) -> bytes | None:
        """
        Clear the ix-th hardware breakpoint
        """
        return self.device.avr.hardware_breakpoint_clear(ix)

    def stack_pointer_write(self, data : bytes) -> None:
        """
        Writes the stack pointer

        :param data: 2 bytes representing stackpointer in little endian
        :type: bytearray
        """
        self.logger.debug("Writing stack pointer")
        self.device.avr.stack_pointer_write(data)

    def status_register_read(self) -> bytearray:
        """
        Reads the status register from the AVR

        :return: 8-bit SREG value
        :rytpe: one byte
        """
        self.logger.debug("Reading status register")
        return self.device.avr.statreg_read()

    def status_register_write(self, data : bytes) -> None:
        """
        Writes new value to status register
        :param data: SREG
        :type: one byte
        """

        self.logger.debug("Write status register: %s", data)
        self.device.avr.statreg_write(data)

    def register_file_read(self) -> bytearray:
        """
        Reads out the AVR register file (R0::R31)

        :return: 32 bytes of register file content as bytearray
        :rtype: bytearray
        """
        self.logger.debug("Reading register file")
        if self._regfile is None:
            self._regfile = self.device.avr.regfile_read()
            self._regsupd = False
        return bytearray(self._regfile[:])

    def register_file_write(self, regs : bytes) -> None:
        """
        Writes the AVR register file (R0::R31)

        :param data: 32 byte register file content as bytearray
        :raises ValueError: if 32 bytes are not given
        """
        self.logger.debug("Writing register file")
        self._regfile = bytearray(regs)
        self._regsupd = True

    def register_read(self, addr : int, size : int) -> bytearray:
        """
        Returns register contents (from cached regfile)
        """
        self.logger.debug("Reading %d bytes starting at r%d", size, addr)
        if addr + size > 32 or addr < 0:
            raise FatalError("Illegal addressing while reading from registers")
        if self._regfile is None:
            self._regfile = self.device.avr.regfile_read()
            self._regsupd = False
        return bytearray(self._regfile[addr:addr+size])

    def register_write(self, addr : int, data : bytes) -> None:
        """
        Writes to registers
        """
        self.logger.debug("Writing %d bytes starting at r%d", len(data), addr)
        if addr + len(data) > 32 or addr < 0:
            raise FatalError("Illegal addressing while writing to registers")
        if self._regfile is None:
            self._regfile = self.device.avr.regfile_read()
        self._regfile[addr:addr+len(data)] = data
        self._regsupd = True

    def reset(self) -> None:
        """
        Reset the AVR core.
        The PC will point to the first instruction to be executed.
        """
        self.logger.info("MCU reset")
        self.device.avr.protocol.reset()
        self._wait_for_break()


    def program_counter_read(self) -> int:
        """
        Apply the bad PC bit mask (which is for addressing bytes, so shift one to the right)
        """
        return super().program_counter_read() & ~(self.bad_pc_bit_mask >> 1)

    def _update_regfile_in_target(self) -> None:
        """
        Write back the register file if changes have happened and invalidate cache
        """
        if self._regfile is not None and self._regsupd:
            self.device.avr.regfile_write(self._regfile)
        self._regfile = None
        self._regsupd = False

    def run(self) -> None:
        """
        Update register file, then execute
        """
        self._update_regfile_in_target()
        self.flush_events() # remove any pending poll events from queue
        super().run()

    def run_to(self, address : int) -> None:
        """
        Update register file, if changes in register.
        Apply bad bit (if present) to cursor address when starting execution.
        """
        self._update_regfile_in_target()
        self.flush_events() # remove any pending poll events from queue
        super().run_to(address | self.bad_pc_bit_mask)

    def step(self) -> None:
        """
        Update register file, then make a single step
        """
        self._update_regfile_in_target()
        self.flush_events() # remove any pending poll events from queue
        self.logger.debug("PC before step: 0x%X", self.program_counter_read() << 1)
        super().step()
        self.logger.debug("PC after step: 0x%X", self.program_counter_read() << 1)


    def reactivate(self) -> None:
        """
        Reactivate debugger (and set timer flag)
        """
        self.device.avr.reactivate()
        self.reset()

######## Memory read/write

    def read_fuse(self, addr : int, size : int) -> bytearray:
        """
        Read fuses (does not work with debugWIRE and in JTAG only when programming mode)
        """
        return self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_FUSES, addr, size)

    def read_fuse_one_byte(self, addr : int) -> bytearray:
        """
        Read fuses (does not work with debugWIRE and in JTAG only when programming mode)
        """
        return self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_FUSES, addr, 1)

    def write_fuse(self, addr : int, data : bytes) -> bytearray | None:
        """
        Write fuses (does not work with debugWIRE and in JTAG only in programming mode)
        """
        return self.device.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, addr, data)

    def read_lock(self, addr : int, size : int) -> bytearray:
        """
        Read lock bits (does not work with debugWIRE and in JTAG only when in programming mode)
        """
        return self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, addr, size)

    def read_lock_one_byte(self) -> bytearray:
        """
        Read lock bits (does not work with debugWIRE and in JTAG only when in programming mode)
        """
        return self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, 0, 1)

    def write_lock(self, addr : int , data : bytes) -> bytearray | None:
        """
        Write lock bits (does not work with debugWIRE and in JTAG only in programming mode)
        """
        return self.device.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, addr, data)

    def read_sig(self, addr : int, size : int) -> bytearray:
        """
        Read signature in a liberal way, i.e., throwing no errors
        """
        resp = self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_SIGNATURE, 0, 3)
        if size+addr > 3:
            resp += [0xFF]*(addr+size)
        return bytearray(resp[addr:addr+size])

    def flash_read(self, address : int, numbytes : int, prog_mode : bool = False) -> bytearray:
        """
        Read flash content from the AVR
        """
        self.logger.debug("Reading %d bytes from flash at %X", numbytes, address)
        # The debugger protocols (via pymcuprog) use memory-types with zero-offsets
        # However the address used here is already zero-offset, so no compensation is done here
        if self.memory_info is None:
            raise FatalError("No memory info available")
        return self.device.read(self.memory_info.memory_info_by_name('flash'),
                                    address, numbytes, prog_mode=prog_mode)

    def usig_read(self, address : int, numbytes : int, prog_mode : bool=False) -> bytes:
        """
        Read contents of user signature (does not work with debugWIRE)
        """
        self.logger.debug("Reading %d bytes from USER_ROW at 0x%X", numbytes, address)
        if self.memory_info is None:
            raise FatalError("No memory info available")
        return self.device.read(self.memory_info.memory_info_by_name('user_row'), address,
                                        numbytes, prog_mode)


    def usig_write(self, address : int, data : bytes, prog_mode : bool=False) -> str | None:
        """
        Write user signature (does not work with debugWIRE)
        """
        self.logger.debug("Writing %d bytes to USER_ROW at 0x%X", len(data), address)
        if self.memory_info is None:
            raise FatalError("No memory info available")
        result : str | None = self.device.write(
                                         self.memory_info.memory_info_by_name('user_row'),
                                         address,
                                         data, prog_mode)
        time.sleep(0.07) # 0.02 is strictly necessary, let's be conservative ...
        return result


    def eeprom_read(self, address : int, numbytes : int, prog_mode : bool=False) -> bytes:
        """
        Read EEPROM content from the AVR
        Needs to be handled here because depending on programm_mode, different memtypes have to be used
        """
        self.logger.debug("Reading %d bytes from EEPROM at 0x%X", numbytes, address)
        if self.memory_info is None:
            raise FatalError("No memory info available")
        return self.device.read(self.memory_info.memory_info_by_name('eeprom'), address,
                                        numbytes, prog_mode)

    def eeprom_write(self, address : int , data : bytes, prog_mode : bool=False) -> None:
        """
        Write EEPROM content to the AVR
        Needs to be handled here because depending on programm_mode, different memtypes have to be used
        """
        self.logger.debug("Writing %d bytes to EEPROM at 0x%X", len(data), address)
        if self.memory_info is None:
            raise FatalError("No memory info available")
        return self.device.write(self.memory_info.memory_info_by_name('eeprom'), address,
                                         data, prog_mode)

    def sram_masked_read(self, addr : int, size : int) -> bytes:
        """
        Read a chunk from SRAM but leaving  out any masked registers. In theory,
        one could use the "Memory Read Masked" method of the AVR8 Generic protocol.
        However, there is no Python method implemented that does that for you.
        For this reason, we do it here step by step.

        In addition to that, the function fetches the values from the general
        registers if the address is below the iooffset, i.e., < 20 for JTAG and
        dw targets.
        """
        addr &= 0xFFFF # mask out GDB bits
        end : int = addr + size
        data : bytearray = bytearray()
        mr : int
        if addr < self.get_iooffset():
            data = self.register_read(addr, min(self.get_iooffset(), end) - addr)
            addr = self.get_iooffset()
        for mr in sorted(self.masked_registers):
            if mr >= end or addr >= end:
                break
            if mr < addr:
                continue
            if addr < mr:
                data.extend(self.sram_read(addr, mr - addr))
            data.append(0x00)
            self.logger.warning("Not reading from SRAM 0x%X because it is read-protected", mr)
            addr = mr + 1
        if addr < end:
            data.extend(self.sram_read(addr, end - addr))
        return data

    def sram_masked_write(self, addr : int, data : bytes) -> None:
        """
        Write a chunk to SRAM but leaving  out any read-only registers. If there is an
        attempt to write to a read-only register, spew out a warning message.

        If we write to SRAM below iooffset, then we will write to the registerfile
        """
        addr &= 0xFFFF # mask out GDB bits
        start : int = addr
        end : int = addr + len(data)
        rr : int
        if addr < self.get_iooffset():
            self.register_write(addr, bytes(data[:min(self.get_iooffset()-addr,len(data))]))
            addr = self.get_iooffset()
            data = data[self.get_iooffset()-addr:]
            if not data:
                return
        for rr in sorted(self.ronly_registers):
            if rr >= end or addr >= end:
                break
            if rr < addr:
                continue
            if addr < rr:
                # write to SRAM from addr up to rr-1
                self.sram_write(addr, data[addr-start:rr-start])
            self.logger.warning("Not writing to SRAM 0x%X because it is write-protected", rr)
            addr = rr + 1
        if addr < end:
            # write remaining data
            self.logger.debug("Write remaining from 0x%X to 0x%X (not incl)", addr, end)
            self.sram_write(addr, data[addr-start:end-start])
