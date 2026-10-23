"""
The session logic for classic and AVR8X targets that does not depend on the probe:
fuse management (lockbits, BOOTRST, OCDEN, DWEN, EESAVE), signature checks, the checks for
chips with known defects, waiting for a power cycle, the register cache, and the order of
the steps when a session starts and ends. Moved here unchanged from EdbgBackend, so that
every backend (EDBG, JTAGICE mkII / AVR Dragon, ...) gets it.

A backend derives from AvrSession and implements the primitives below (the methods whose
names start with an underscore and that are abstract here), in addition to the
DebugBackend methods that AvrSession does not implement.
"""
from abc import abstractmethod
from typing import Any
from collections.abc import Callable
import argparse
import logging
import time

from pymcuprog.deviceinfo import deviceinfo  # pure device description, no tool dependency

from pyavrocd.backend import DebugBackend, BackendError, BackendNotSupportedError
from pyavrocd.errors import FatalError, EndOfSession
from pyavrocd.deviceinfo.devices.alldevices import dev_name


class OcdNotEnabledError(BackendError):
    """Attaching failed because the OCD is not enabled yet (OCDEN, was AVR8_FAILURE_ILLEGAL_OCD_STATUS)"""

class OcdLockedError(BackendError):
    """Attaching failed because the chip is locked (UPDI, was AVR8_FAILURE_OCD_LOCKED)"""


# Properties of the debugging interfaces: the fuses that may be managed, number of hardware
# breakpoints, SREG address, start of the I/O space, and the value of unset lockbits
IFACE_PROPERTIES : dict[str, dict[str, Any]] = {
    'updi' :      { 'manage' : ['lockbits', 'eesave'],
                    'hwbpnum' : 2, 'sregaddr' : 0x3F, 'iooffset' : 0, 'nolock' : 0xC5 },
    'debugwire' : { 'manage' : ['lockbits', 'bootrst', 'dwen', 'eesave'],
                    'hwbpnum' : 1, 'sregaddr' : 0x5F, 'iooffset' : 0x20, 'nolock' : 0xFF },
    'jtag' :      { 'manage' : ['lockbits', 'bootrst', 'ocden', 'eesave'],
                    'hwbpnum' : 4, 'sregaddr' : 0x5F, 'iooffset' : 0x20, 'nolock' : 0xFF },
    }

# Pairs of a signature computed from the device id and a possible alternative identity.
# For example, the first pair signifies that a chip returning a device id corresponding
# to an atmega48p could well be an atmega48a.
COMPATIBLE_IDS : tuple[ tuple[ int, int], ... ] = \
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


#pylint: disable=too-many-public-methods,too-many-instance-attributes
class AvrSession(DebugBackend):
    """
    Probe-independent session logic on top of a small set of primitives
    """

    def __init__(self, devicename : str, iface : str, args : argparse.Namespace) -> None:
        DebugBackend.__init__(self, devicename, iface)
        # log under the concrete backend's module, as before the logic moved here
        self.logger : logging.Logger = logging.getLogger(type(self).__module__)
        self.args : argparse.Namespace = args
        self.bad_pc_bit_mask : int = 0
        # Caching general registers, will be updated when execution is resumed
        self._regfile : bytearray | None = None
        self._regsupd : bool = False

        # Gather device info
        try:
            self.logger.info("Looking for device %s", devicename)
            self.device_info = deviceinfo.getdeviceinfo("pyavrocd.deviceinfo.devices." + devicename)
        except ImportError:
            raise BackendNotSupportedError("No device info for device: {}".format(devicename)) #pylint: disable=raise-missing-from
        self._architecture : str = str(self.device_info['architecture']).lower()
        if iface not in str(self.device_info['interface']).lower():
            raise BackendError("Incompatible debugging interface")
        self.masked_registers = self.device_info.get('masked_registers',[])
        self.ronly_registers = self.device_info.get('ronly_registers',[])
        self.memory_info = deviceinfo.DeviceMemoryInfo(self.device_info)

        properties = IFACE_PROPERTIES.get(iface, {})
        if iface == 'jtag' and self._architecture != 'avr8': # JTAG on XMEGA: not supported
            properties = {}
        self.manage : list[str] = [ m for m in args.manage if m in properties.get('manage', []) ]
        self._hwbpnum : int = properties.get('hwbpnum', 0)
        self._sregaddr : int = properties.get('sregaddr', 0)
        self._iooffset : int = properties.get('iooffset', 0)
        self._nolock : int = properties.get('nolock', 0)

    # ===== primitives, implemented by each backend ============================

    # --- the tool
    @abstractmethod
    def _sign_on(self, announce : bool = False) -> None:
        """Start a session with the tool; with 'announce', log what the tool is"""

    @abstractmethod
    def _sign_off(self) -> None:
        """End the session with the tool"""

    @abstractmethod
    def _target_voltage(self) -> float:
        """Target supply in volt"""

    # --- the OCD
    @abstractmethod
    def _configure_session(self) -> None:
        """Communicate session parameters (clocks, timers) and the device description to the tool"""

    @abstractmethod
    def _activate_interface(self, graceful : bool = False) -> int:
        """Activate the physical interface; returns the device id the OCD reports"""

    @abstractmethod
    def _attach_and_stop(self) -> None:
        """Attach to the OCD and stop the core; raises OcdNotEnabledError or OcdLockedError"""

    def _erase_locked_chip(self) -> None:
        """Erase a locked chip so that the OCD can be attached (UPDI only)"""
        raise BackendNotSupportedError("Erasing a locked chip is not supported")

    @abstractmethod
    def _clear_all_breakpoints(self) -> None:
        """Remove all software and hardware breakpoints"""

    @abstractmethod
    def _debugwire_disable(self) -> None:
        """Leave debugWIRE mode, so that ISP works again until the next power cycle"""

    @abstractmethod
    def _detach(self) -> None:
        """Detach from the OCD"""

    @abstractmethod
    def _deactivate_interface(self) -> None:
        """Deactivate the physical interface"""

    @abstractmethod
    def _leave_progmode(self) -> None:
        """Leave programming mode without going back to debug mode"""

    @abstractmethod
    def _ocd_erase(self) -> None:
        """Chip erase through the OCD's programming mode (to clear lockbits)"""

    @abstractmethod
    def _go(self) -> None:
        """Resume execution (registers are written back already)"""

    @abstractmethod
    def _go_to(self, address : int) -> None:
        """Resume execution until byte address 'address'"""

    @abstractmethod
    def _single_step(self) -> None:
        """Execute one instruction"""

    @abstractmethod
    def _regfile_read_raw(self) -> bytearray:
        """Read r0..r31 from the target"""

    @abstractmethod
    def _regfile_write_raw(self, regs : bytes) -> None:
        """Write r0..r31 to the target"""

    @abstractmethod
    def _pc_read_raw(self) -> int:
        """PC as word address, as the OCD reports it"""

    # --- ISP (debugWIRE targets, while DWEN is not programmed)
    @abstractmethod
    def _isp_open(self) -> None:
        """Connect to the ISP programming module and enter programming mode"""

    @abstractmethod
    def _isp_enter(self) -> None:
        """Enter ISP programming mode again"""

    @abstractmethod
    def _isp_leave(self) -> None:
        """Leave ISP programming mode"""

    @abstractmethod
    def _isp_device_id(self) -> int:
        """Signature read through ISP"""

    @abstractmethod
    def _isp_read_fuse(self, addr : int) -> bytes:
        """One fuse byte through ISP"""

    @abstractmethod
    def _isp_write_fuse(self, addr : int, data : bytearray) -> None:
        """Write one fuse byte through ISP"""

    @abstractmethod
    def _isp_read_lock(self) -> bytes:
        """Lock byte through ISP"""

    @abstractmethod
    def _isp_erase(self) -> None:
        """Chip erase through ISP"""

    @abstractmethod
    def _isp_write_flash(self, address : int, data : bytes) -> None:
        """Program flash through ISP"""

    def _isp_restart(self) -> None:
        """Leave ISP programming mode and connect again (a read after a write may fail otherwise)"""
        self._isp_leave()
        self._isp_open()
        self.logger.debug("Reconnected to SPI programming module")

    # ===== static properties ===================================================

    def get_architecture(self) -> str:
        """info about architecture"""
        return self._architecture

    def get_hwbpnum(self) -> int:
        """info about number of hardware breakpoints"""
        return self._hwbpnum

    def get_sregaddr(self) -> int:
        """Address of SREG"""
        return self._sregaddr

    def get_iooffset(self) -> int:
        """Returns offset to I/O registers, i.e., 0x20 for dw and JTAG, 0x00 for UPDI"""
        return self._iooffset

    # ===== session start ========================================================

    def start_debugging(self, flash_data : bytes | None = None, warmstart : bool = False) -> bool:
        """
        Start the debug session, i.e., initialize everything and start the debug engine.
        A warm start will assume that the OCD has already been activated, and will gracefully
        fail if not. Warmstarts happen only with debugWIRE. Return False if unsuccessful.
        """
        _dummy = flash_data
        self.logger.info("Starting up debug session...")
        try:
            self._sign_on(announce=True)
            self._configure_session()
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
            self._attach_and_stop() # If successful, OCDEN is already activated
        except OcdNotEnabledError:
            self.logger.debug("Illegal OCD status, need to activate debugging")
            if self.args.attach:
                raise FatalError("Could not attach to OCD because debugging is not yet activated") #pylint: disable=raise-missing-from
        except OcdLockedError:
            self.logger.info("Chip is locked and needs to be erased")
            if self.args.attach:
                raise FatalError("Could not attach to OCD because chip is locked") #pylint: disable=raise-missing-from
            self._erase_locked_chip()
        self._manage_fuses()
        self._verify_target(dev_id)
        self._check_attiny2313()
        self._check_stuck_at_one_pc()
        if not self.args.attach:
            self.reset()
        self.logger.info("... debug session startup done")
        return True

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
        self._handle_lockbits(lambda: self.read_lock(0, 1), self._ocd_erase)
        # unprogram BOOTRST fuse if necessary
        self._handle_bootrst(lambda addr: self.read_fuse(addr, 1), self.write_fuse)
        if self.device_info.get('ocden_base') is not None:
            # program OCDEN
            ofuse_addr : int = self.device_info['ocden_base']
            ofuse_mask : int = self.device_info['ocden_mask']
            ofuse : bytes = self.read_fuse(ofuse_addr, 1)
            self.logger.debug("OCDEN read: 0x%X", ofuse[0] & ofuse_mask)
            if ofuse[0] & ofuse_mask == ofuse_mask: # only if OCDEN is not yet programmed
                if 'ocden' not in self.manage:
                    self.logger.warning("The fuse OCDEN is not managed by PyAvrOCD.")
                    self.logger.warning("In order to allow debugging, you need to program this fuse manually.")
                    self.logger.warning("Or let payavrocd manage this fuse: '-m ocden'.")
                    raise FatalError("Debugging is impossible because OCDEN cannot be programmed")
                newfuse = ofuse[0] & ~ofuse_mask & 0xFF
                self.write_fuse(ofuse_addr, bytearray([newfuse]))
                assert newfuse == self.read_fuse(ofuse_addr, 1)[0], "OCDEN could not be programmed"
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
            if (sig, self.device_info['device_id']) not in COMPATIBLE_IDS:
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
        pc : int = self._pc_read_raw() << 1
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

    def _handle_bootrst(self, read : Callable[[int], bytes],
                              write : Callable[[int, bytearray], Any]) -> None:
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
                        self._isp_restart()
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

    # ===== preparing a debugWIRE target =========================================

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
        isp_open : bool = False
        try:
            if self._target_voltage() < 1.5:
                raise FatalError("Target is not powered")
            self._sign_on() # need to start a new session after reading target voltage
            self.logger.info("Signed on to tool")
            self._isp_open()
            isp_open = True
            self.logger.info("Connected to SPI programming module")
            device_id : int = self._isp_device_id()
            if self.device_info['device_id'] != device_id and not self.args.skipsig:
                raise FatalError("Wrong MCU: '%s' (Sig: %x), expected: '%s (Sig: %x)'" %
                        (dev_name.get(device_id,"Unknown"),
                        device_id,
                        dev_name[self.device_info['device_id']],
                        self.device_info['device_id']))
            self._isp_restart()
            self._handle_lockbits(self._isp_read_lock, self._isp_erase)
            self._handle_bootrst(self._isp_read_fuse, self._isp_write_fuse)
            # program the DWEN bit
            dwen_addr : int = self.device_info['dwen_base']
            dwen_mask : int = self.device_info['dwen_mask']
            self.logger.debug("DWEN addr: 0x%X, DWEN mask: 0x%X", dwen_addr, dwen_mask)
            dwen_byte : bytes = self._isp_read_fuse(dwen_addr)
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
                self._isp_write_fuse(dwen_addr, bytearray([newfuse]))
                self.logger.info("DWEN fuse written")
            self._isp_leave()
            self.logger.info("SPI programming terminated")
            # now you need to power-cycle
            self._power_cycle(callback=callback, recognition=recognition)
            # end current tool session and start a new one
        except Exception as e:
            self.logger.critical("%s", str(e))
            raise e
        finally:
            try:
                if isp_open:
                    self._isp_leave()
            except Exception:
                pass
            self._sign_off()
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
        # The test erases the chip twice. If EESAVE is managed, program it temporarily in order
        # to preserve the EEPROM (on classic AVRs, EESAVE takes effect immediately).
        original_fuse_byte : bytes | None = self._program_eesave_temporarily()
        try:
            self._dirty_pc_test(device_id)
        finally:
            if original_fuse_byte is not None:
                self._isp_write_fuse(self.device_info['eesave_base'], bytearray(original_fuse_byte))
                self.logger.info("EESAVE fuse restored")

    def _program_eesave_temporarily(self) -> bytes | None:
        """
        Program EESAVE via ISP if it is managed and not programmed yet.
        Returns the original fuse byte if it was changed, otherwise None.
        """
        if 'eesave' not in self.manage:
            self.logger.warning("The EEPROM will be erased while testing for a dirty PC.")
            self.logger.warning("Let PyAvrOCD manage the EESAVE fuse in order to preserve it: '-m eesave'.")
            return None
        eesave_base : int | None = self.device_info.get('eesave_base')
        eesave_mask : int | None = self.device_info.get('eesave_mask')
        if eesave_base is None or not eesave_mask:
            self.logger.warning("EESAVE fuse data unknown. EEPROM will be deleted")
            return None
        fuse_byte : bytes = self._isp_read_fuse(eesave_base)
        if fuse_byte[0] & eesave_mask == 0: # already programmed (active low)
            return None
        self._isp_write_fuse(eesave_base, bytearray([fuse_byte[0] & ~eesave_mask & 0xFF]))
        self.logger.info("EESAVE temporarily programmed to preserve EEPROM")
        return fuse_byte

    def _dirty_pc_test(self, device_id : int) -> None:
        """
        Flash a test program that checks the boot_signature, run it, and check the result
        in the lock bits. Erases the chip before and after.
        """
        # erase flash (EEPROM is preserved by EESAVE)
        self._isp_erase()
        # change option value of 'load' option if necessary
        if self.args.load is None or self.args.load[0] == 'n': # the 'no initial load' option value
            self.args.load = 'r'     # for debugWIRE, the right one is 'read before write'
        # program flash with test program, depending on MCU type
        self.logger.debug("Flash test program")
        if device_id == 0x1E9205: # ATmega48(A)
            self._isp_write_flash(0,
                    bytearray.fromhex("19C02CC02BC02AC029C028C027C026C025C024C023C022C021C020C01FC01EC0" +
                                      "1DC01CC01BC01AC019C018C017C016C015C014C011241FBECFEFD2E0DEBFCDBF" +
                                      "14BE0FB6F894A89580916000886180936000109260000FBE02D014C0D1CF81E2" +
                                      "F0E0E0E08093570084918E3141F089E09EEFE1E0F0E0092E80935700E89590E0" +
                                      "80E00895F894FFCF"))
        else:
            self._isp_write_flash(0,
                    bytearray.fromhex("19CE2CCE2BCE2ACE29CE28CE27CE26CE25CE24CE23CE22CE21CE20CE1FCE1ECE" +
                                      "1DCE1CCE1BCE1ACE19CE18CE17CE16CE15CE14CEFFFFFFFFFFFFFFFFFFFFFFFF"))
            self._isp_write_flash(0x1C30,
                    bytearray.fromhex("FFFFFFFF11241FBECFEFD4E0DEBFCDBF14BE0FB6F894A8958091600088618093" +
                                      "6000109260000FBE02D018C0D1C181E2F0E0E0E08093570084918E3141F089E0" +
                                      "9BEFE1E0F0E0092E80935700E895E4E3F0E0E491E5B990E080E00895F894FFCF"))
        self._isp_leave()
        # now wait a couple of milliseconds
        time.sleep(0.1)
        # start programming mode again and read result
        self._isp_enter()
        self.logger.debug("Now check result")
        result_lockbits : bytes = self._isp_read_lock()
        # Check result
        self.logger.debug("Result from lockbits: 0x%X",   result_lockbits[0])
        # Now erase chip again to clear lock bits
        self._isp_erase()
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
        self._sign_off() # might be necessary after an unsuccessful power-cycle
        self.logger.info("Signed off from tool")
        while time.monotonic() - wait_start < 150:
            if time.monotonic() - last_message > 20:
                self.logger.warning("*** Please power-cycle the target system ***")
                last_message = time.monotonic()
            if self._target_voltage() < 0.5:
                wait_start = time.monotonic()
                self.logger.info("*** Power-down recognized. Apply power again! ***")
                if recognition is not None:
                    recognition()
                while  self._target_voltage() < 1.5 and \
                  time.monotonic() - wait_start < 20:
                    time.sleep(0.1)
                if self._target_voltage() < 1.5:
                    raise FatalError("Timed out waiting for repowering target")
                time.sleep(1) # wait for debugWIRE system to be ready to accept connections
                self._sign_on()
                self.logger.info("Signed on to tool again")
                return
            time.sleep(0.1)
        raise FatalError("Timed out waiting for power-cycle")

    # ===== session end ==========================================================

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
            # Remove all software and hardware breakpoints
            self._clear_all_breakpoints()
            self.logger.info("All breakpoints removed")
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
                self._debugwire_disable()
                self.logger.info("DebugWIRE mode disabled")
        except Exception as e:
            if not graceful:
                self.logger.error("Error during disabling debugWIRE mode: %s", str(e))
        # Detach from the OCD
        try:
            self._detach()
            self.logger.info("Detached from OCD")
        except Exception as e:
            if not graceful:
                self.logger.error("Error during detaching from OCD: %s", str(e))
        # De-activate physical interface
        try:
            self._deactivate_interface()
            self.logger.info("Physical interface deactivated")
        except Exception as e:
            if not graceful:
                self.logger.error("Error during deactivating interface: %s", str(e))
        # Sign off device
        try:
            self._sign_off()
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
        self._leave_progmode()
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
            self._sign_on()
            self.logger.info("Signed on to tool again")
            # now open an ISP programming session again
            self.logger.info("Reconnecting in SPI programming mode")
            self._isp_open()
            self._isp_enter()
            self.logger.info("Entered SPI programming mode")
            dwen_addr : int = self.device_info['dwen_base']
            dwen_mask : int = self.device_info['dwen_mask']
            dwen_byte : bytearray = bytearray(self._isp_read_fuse(dwen_addr))
            self.logger.debug("DWEN byte: 0x%X", dwen_byte[0])
            dwen_byte[0] |= dwen_mask
            self.logger.debug("New DWEN byte: 0x%X", dwen_byte[0])
            self._isp_write_fuse(dwen_addr, dwen_byte)
            self.logger.info("Unprogrammed DWEN fuse")
            self._isp_leave()
            self.logger.info("SPI programming terminated")
            self._sign_off()
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

    # ===== execution, with the register cache and the stuck PC bits ===============

    def _update_regfile_in_target(self) -> None:
        """
        Write back the register file if changes have happened and invalidate cache
        """
        if self._regfile is not None and self._regsupd:
            self._regfile_write_raw(self._regfile)
        self._regfile = None
        self._regsupd = False

    def _run(self) -> None:
        """
        Update register file, then execute
        """
        self._update_regfile_in_target()
        self._go()

    def _run_to(self, address : int) -> None:
        """
        Update register file, if changes in register.
        Apply bad bit (if present) to cursor address when starting execution.
        """
        self._update_regfile_in_target()
        self._go_to(address | self.bad_pc_bit_mask)

    def _step(self) -> None:
        """
        Update register file, then make a single step
        """
        self._update_regfile_in_target()
        self.logger.debug("PC before step: 0x%X", self.program_counter_read() << 1)
        self._single_step()
        self.logger.debug("PC after step: 0x%X", self.program_counter_read() << 1)

    def program_counter_read(self) -> int:
        """
        Apply the bad PC bit mask (which is for addressing bytes, so shift one to the right)
        """
        return self._pc_read_raw() & ~(self.bad_pc_bit_mask >> 1)

    # ===== registers ==============================================================

    def register_file_read(self) -> bytearray:
        """
        Reads out the AVR register file (R0::R31)
        """
        self.logger.debug("Reading register file")
        if self._regfile is None:
            self._regfile = self._regfile_read_raw()
            self._regsupd = False
        return bytearray(self._regfile[:])

    def register_file_write(self, regs : bytes) -> None:
        """
        Writes the AVR register file (R0::R31)
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
            self._regfile = self._regfile_read_raw()
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
            self._regfile = self._regfile_read_raw()
        self._regfile[addr:addr+len(data)] = data
        self._regsupd = True
