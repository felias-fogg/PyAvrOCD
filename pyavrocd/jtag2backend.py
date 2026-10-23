"""
The debugger backend for the probes that speak the JTAGICE mkII protocol (AVR067): the JTAGICE
mkII and the AVR Dragon, through pyavrocd.jtag2. The probe-independent session logic is in
session.py; this module supplies the primitives it needs.

So far for JTAG targets. debugWIRE needs a check of DWEN through ISP before the emulator mode is
set: a failed debugWIRE sync leaves the mkII hanging until it is switched off.

Behaviour of the probes that the code relies on (measured with a JTAGICE mkII clone, firmware
7.27, and an AVR Dragon, firmware 6.0B and 7.27, on an ATmega324P and an ATmega328P):
- after a stop, step or reset, the probe sends EVT_BREAK; LEAVE_PROGMODE leaves two stale ones,
  so pending events are drained before the target runs or steps
- the probe plants software breakpoints with SPM from ulBootAddress and steps over them itself
  (no flash reprogramming, also for two-word instructions on JTAG)
- PAR_TIMERS_RUNNING can be set, not read; on JTAG it falls back to 'frozen' whenever the emulator
  mode is entered, so it is set after every entry
- after CMND_SIGN_OFF, the probe re-enumerates on USB
"""
import argparse
import time

import usb.core

from pyavrocd import jtag2
from pyavrocd.backend import SwbpSupport, BackendError, BackendNotSupportedError, ProbeCandidate
from pyavrocd.session import AvrSession
from pyavrocd.errors import FatalError

#pylint: disable=too-many-public-methods,too-many-instance-attributes
class Jtag2Backend(AvrSession):
    """
    Backend for JTAGICE mkII and AVR Dragon
    """
    SWBP_SUPPORT = SwbpSupport.PROBE

    def __init__(self, candidate : ProbeCandidate, devicename : str, iface : str,
                     args : argparse.Namespace) -> None:
        AvrSession.__init__(self, devicename, iface, args)
        if iface != 'jtag':
            raise BackendNotSupportedError("Debugging over {} with the {} is not supported yet"
                                               .format(iface, candidate.product))
        self.candidate : ProbeCandidate = candidate
        self.timers_run : bool = args.timers[0] == 'r'
        self.transport : jtag2.Jtag2UsbTransport | None = None
        self.protocol : jtag2.Jtag2Protocol | None = None
        self.sign_on_info : jtag2.SignOn | None = None
        self._swbps : set[int] = set()       # software breakpoints (byte addresses)
        self._mode_set : bool = False
        self.logger.info("mkII backend for %s (%s), iface: %s, HWBPs: %d", candidate.product,
                             candidate.address, iface, self._hwbpnum)
        if self.manage == []:
            self.manage = [ 'none' ]
        self.logger.info("Managing fuses: %s", ", ".join(self.manage))

    # ----- the protocol, opened on demand ----------------------------------------

    def _proto(self) -> jtag2.Jtag2Protocol:
        if self.protocol is None:
            raise FatalError("Not signed on to the {}".format(self.candidate.product))
        return self.protocol

    def _open(self) -> None:
        """Open the probe; after a sign-off it re-enumerates on USB, which takes a moment"""
        deadline = time.monotonic() + 5
        while True:
            try:
                self.transport = jtag2.Jtag2UsbTransport.open(tool=self.candidate.tool,
                                                              serial_suffix=self.candidate.address)
                break
            except (jtag2.Jtag2Error, usb.core.USBError):
                if time.monotonic() > deadline:
                    raise
                time.sleep(0.3)
        self.protocol = jtag2.Jtag2Protocol(self.transport)

    def _enter_mode(self) -> None:
        """Set the emulator mode and everything that has to follow each entry into it"""
        proto = self._proto()
        proto.set_parameter(jtag2.PAR_EMULATOR_MODE, bytes([jtag2.EMULATOR_MODE_JTAG]))
        proto.set_device_descriptor(jtag2.make_device_descriptor(self.device_info))
        proto.set_parameter(jtag2.PAR_TIMERS_RUNNING, bytes([int(self.timers_run)]))
        self._mode_set = True

    # ===== primitives for AvrSession ==================================================

    def _sign_on(self, announce : bool = False) -> None:
        if self.protocol is None:
            self._open()
        info = self._proto().sign_on()
        self.sign_on_info = info
        if announce:
            self.logger.info("Signed on to: %s FW: %X.%02X, HW: %d, SN: %s", info.ident,
                                 info.master_firmware[0], info.master_firmware[1],
                                 info.master_hardware, info.serial)
            if info.master_firmware[0] < 7:
                self.logger.warning("Firmware %X.%02X is old; single steps can be slow "
                                        "(update it with Microchip Studio)", *info.master_firmware)

    def _sign_off(self) -> None:
        if self.protocol is None:
            return
        try:
            if self._mode_set:
                self.protocol.set_parameter(jtag2.PAR_EMULATOR_MODE, bytes([jtag2.EMULATOR_MODE_UNKNOWN]))
                self._mode_set = False
            self.protocol.sign_off()
        finally:
            if self.transport is not None:
                try:
                    self.transport.close()
                except usb.core.USBError:
                    pass     # the probe is already re-enumerating
            self.transport = None
            self.protocol = None

    def _target_voltage(self) -> float:
        return int.from_bytes(self._proto().get_parameter(jtag2.PAR_OCD_VTARGET), 'little') / 1000

    def _configure_session(self) -> None:
        self._enter_mode()
        self.logger.info("Emulator mode, device descriptor and timer mode communicated to tool")

    def _activate_interface(self, graceful : bool = False) -> int:
        """The JTAG ID of the target, as the session expects it for the signature check"""
        _dummy = graceful
        if self._target_voltage() < 1.5:
            raise FatalError("Target is not powered")
        jtag_id = int.from_bytes(self._proto().get_parameter(jtag2.PAR_JTAGID), 'little')
        self.logger.info("JTAG ID: 0x%08X", jtag_id)
        return jtag_id

    def _attach_and_stop(self) -> None:
        self.stop()

    def _clear_all_breakpoints(self) -> None:
        self.software_breakpoint_clear_all()
        for ix in range(1, self._hwbpnum):
            self.hardware_breakpoint_clear(ix)

    def _debugwire_disable(self) -> None:
        self._proto().debugwire_disable()

    def _detach(self) -> None:
        """Nothing to do: the target runs on, and leaving the emulator mode happens at the sign-off"""

    def _deactivate_interface(self) -> None:
        """Nothing to do, see _detach"""

    def _leave_progmode(self) -> None:
        """
        Called by the session after it has unprogrammed OCDEN: the mkII then answers LEAVE_PROGMODE
        with RSP_FAILED, presumably because it tries to go back to the OCD (measured on the 324P;
        with OCDEN programmed the same command succeeds)
        """
        try:
            self._proto().leave_progmode()
        except jtag2.Jtag2Error as e:
            self.logger.debug("Leaving programming mode without OCD: %s", e)
        self._proto().drain_breaks()

    def _ocd_erase(self) -> None:
        self._proto().chip_erase()

    def _go(self) -> None:
        self._proto().drain_breaks()
        self._proto().go()

    def _go_to(self, address : int) -> None:
        self._proto().drain_breaks()
        self._proto().run_to(address >> 1)

    def _single_step(self) -> None:
        self._proto().drain_breaks()
        self._proto().single_step()
        self._proto().wait_for_break()

    def _regfile_read_raw(self) -> bytearray:
        return bytearray(self._proto().read_memory(jtag2.MEMTYPE_SRAM, 0, 32))

    def _regfile_write_raw(self, regs : bytes) -> None:
        self._proto().write_memory(jtag2.MEMTYPE_SRAM, 0, bytes(regs))

    def _pc_read_raw(self) -> int:
        return self._proto().read_pc()

    # ISP, needed for debugWIRE only: not supported yet
    def _isp_unsupported(self) -> None:
        raise BackendNotSupportedError("ISP through the JTAGICE mkII protocol is not supported yet")

    def _isp_open(self) -> None:
        self._isp_unsupported()

    def _isp_enter(self) -> None:
        self._isp_unsupported()

    def _isp_leave(self) -> None:
        self._isp_unsupported()

    def _isp_device_id(self) -> int:
        self._isp_unsupported()
        return 0

    def _isp_read_fuse(self, addr : int) -> bytes:
        self._isp_unsupported()
        return b""

    def _isp_write_fuse(self, addr : int, data : bytearray) -> None:
        self._isp_unsupported()

    def _isp_read_lock(self) -> bytes:
        self._isp_unsupported()
        return b""

    def _isp_erase(self) -> None:
        self._isp_unsupported()

    def _isp_write_flash(self, address : int, data : bytes) -> None:
        self._isp_unsupported()

    # ===== DebugBackend ==================================================================

    def guard_transactions(self) -> None:
        """Jtag2Protocol.command runs every command with its response inside termination.transaction()"""

    def is_set_up(self) -> bool:
        return self.protocol is not None

    def get_toolname(self) -> str:
        return self.candidate.product

    def reactivate(self) -> None:
        """The timer mode needs no reactivation on the mkII, but callers expect a reset (after a load)"""
        self.reset()

    def switch_to_progmode(self) -> bool:
        self._proto().enter_progmode()
        return True

    def switch_to_debmode(self) -> bool:
        self._proto().leave_progmode()
        self._proto().drain_breaks()
        return True

    def stop(self) -> None:
        self._proto().forced_stop()
        self._proto().wait_for_break()

    def reset(self) -> None:
        self.logger.info("MCU reset")
        self._proto().drain_breaks()
        self._proto().reset()
        self._proto().wait_for_break()

    def poll_event(self) -> int | None:
        result = self._proto().poll_break(0)
        if result is None:
            return None
        return result[0] << 1

    def program_counter_write(self, program_counter : int) -> None:
        self._proto().write_pc(program_counter)

    def stack_pointer_read(self) -> bytearray:
        return bytearray(self._proto().read_memory(jtag2.MEMTYPE_SRAM, 0x5D, 2))

    def stack_pointer_write(self, data : bytes) -> None:
        self._proto().write_memory(jtag2.MEMTYPE_SRAM, 0x5D, bytes(data))

    def status_register_read(self) -> bytearray:
        return bytearray(self._proto().read_memory(jtag2.MEMTYPE_SRAM, self._sregaddr, 1))

    def status_register_write(self, data : bytes) -> None:
        self._proto().write_memory(jtag2.MEMTYPE_SRAM, self._sregaddr, bytes(data))

    def sram_read(self, address : int, numbytes : int) -> bytearray:
        return bytearray(self._proto().read_memory(jtag2.MEMTYPE_SRAM, address, numbytes))

    def sram_write(self, address : int, data : bytes) -> None:
        self._proto().write_memory(jtag2.MEMTYPE_SRAM, address, bytes(data))

    def _flash_read(self, address : int, numbytes : int, prog_mode : bool = False) -> bytearray:
        """
        Whole aligned pages, which every probe and mode can read (the Dragon returns 0xFF for an
        unaligned start); SPM in debug mode, FLASH_PAGE in programming mode
        """
        page = self.device_info['flash_page_size_bytes']
        memtype = jtag2.MEMTYPE_FLASH_PAGE if prog_mode else jtag2.MEMTYPE_SPM
        start = address - address % page
        end = address + numbytes
        data = bytearray()
        for base in range(start, end, page):
            data += self._proto().read_memory(memtype, base, page)
        return data[address - start:end - start]

    def eeprom_read(self, address : int, numbytes : int, prog_mode : bool = False) -> bytes:
        return self._proto().read_memory(jtag2.MEMTYPE_EEPROM, address, numbytes)

    def eeprom_write(self, address : int, data : bytes, prog_mode : bool = False) -> None:
        self._proto().write_memory(jtag2.MEMTYPE_EEPROM, address, bytes(data))

    def read_fuse(self, addr : int, size : int) -> bytearray:
        return bytearray(self._proto().read_memory(jtag2.MEMTYPE_FUSE, addr, size))

    def write_fuse(self, addr : int, data : bytes) -> None:
        self._proto().write_memory(jtag2.MEMTYPE_FUSE, addr, bytes(data))

    def read_lock(self, addr : int, size : int) -> bytearray:
        return bytearray(self._proto().read_memory(jtag2.MEMTYPE_LOCK, addr, size))

    def write_lock(self, addr : int, data : bytes) -> None:
        self._proto().write_memory(jtag2.MEMTYPE_LOCK, addr, bytes(data))

    def read_sig(self, addr : int, size : int) -> bytearray:
        data = bytearray(self._proto().read_memory(jtag2.MEMTYPE_SIGNATURE, 0, 3))
        data += bytes([0xFF] * max(0, addr + size - 3))
        return data[addr:addr + size]

    def erase_chip(self, prog_mode : bool) -> None:
        if not prog_mode:
            self.switch_to_progmode()
        self._proto().chip_erase()
        if not prog_mode:
            self.switch_to_debmode()

    def erase_flash_page(self, address : int, prog_mode : bool) -> bool:
        """In debug mode only, as with the EDBG probes"""
        if prog_mode:
            self.switch_to_debmode()
        self._proto().erase_page_spm(address)
        if prog_mode:
            self.switch_to_progmode()
        return True

    def write_flash_pages(self, address : int, data : bytes, prog_mode : bool) -> None:
        page = self.device_info['flash_page_size_bytes']
        for offset in range(0, len(data), page):
            self._proto().write_memory(jtag2.MEMTYPE_FLASH_PAGE, address + offset,
                                           bytes(data[offset:offset + page]))

    def hardware_breakpoint_set(self, ix : int, address : int) -> None:
        if address == 0:
            self.logger.warning("A hardware breakpoint at address 0 does not fire on this probe")
        self._proto().set_break(ix, (address | self.bad_pc_bit_mask) >> 1)

    def hardware_breakpoint_clear(self, ix : int) -> None:
        try:
            self._proto().clr_break(ix)
        except jtag2.Jtag2Error as e:     # clearing an unset comparator is refused by some firmware
            self.logger.debug("Clearing hardware breakpoint %d: %s", ix, e)

    def software_breakpoint_set(self, address : int) -> bool:
        try:
            self._proto().set_break(jtag2.SOFTWARE_BREAKPOINT, address >> 1)
        except BackendError as e:
            self.logger.error("Could not set software breakpoint: %s", str(e))
            return False
        self._swbps.add(address)
        return True

    def software_breakpoint_clear(self, address : int) -> None:
        self._proto().clr_break(jtag2.SOFTWARE_BREAKPOINT, address >> 1)
        self._swbps.discard(address)

    def software_breakpoint_clear_all(self) -> None:
        for address in sorted(self._swbps):
            self.software_breakpoint_clear(address)

    def can_set_run_timers(self) -> bool:
        return True

    def set_run_timers(self, run : bool) -> None:
        """Takes effect at once (measured); also remembered for the next entry into the emulator mode"""
        self.timers_run = run
        if self._mode_set:
            self._proto().set_parameter(jtag2.PAR_TIMERS_RUNNING, bytes([int(run)]))
