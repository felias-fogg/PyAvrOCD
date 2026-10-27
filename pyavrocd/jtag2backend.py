"""
The debugger backend for the probes that speak the JTAGICE mkII protocol (AVR067): the JTAGICE
mkII and the AVR Dragon, through pyavrocd.jtag2. The probe-independent session logic is in
session.py; this module supplies the primitives it needs.

For JTAG and debugWIRE targets. Before the emulator mode is set to debugWIRE, the backend makes
sure debugWIRE is active: a failed debugWIRE sync leaves the mkII clone hanging until it is
switched off. ISP (SPI mode, then ISP programming mode) succeeds only when it is not.

Behaviour of the probes that the code relies on (measured with a JTAGICE mkII clone, firmware
7.27, and an AVR Dragon, firmware 6.0B and 7.27, on an ATmega324P and an ATmega328P):
- after a stop, step or reset, the probe sends EVT_BREAK; LEAVE_PROGMODE leaves two stale ones,
  so pending events are drained before the target runs or steps
- the probe plants software breakpoints with SPM from ulBootAddress and steps over them itself
  (no flash reprogramming, also for two-word instructions on JTAG)
- PAR_TIMERS_RUNNING can be set, not read; on JTAG it falls back to 'frozen' whenever the emulator
  mode is entered, so it is set after every entry
- after CMND_SIGN_OFF, the probe re-enumerates on USB (about 3 s); so it is sent only after
  debugWIRE has been switched off, where ISP is impossible without it
- the probe sets and clears software breakpoints in flash only at the next go or step (a reset
  does not count); until then a cleared one still reads as BREAK, and a page written over it gets
  the old word back at the next go -- on debugWIRE and on JTAG, even after a chip erase.
  CMND_RESTORE_TARGET removes them at once, so it is sent before the first flash write of a load
- after a power cycle of the target, the AVR Dragon and the JTAGICE mkII do not answer the first
  command on a connection left idle during the cycle, however long one waits (polled across the
  cycle, nothing is lost); after reopening they do, so the sign-on reopens once
- USB errors reach the session as Jtag2UsbError (a BackendError), timeouts as Jtag2UsbTimeout
"""
import argparse
import logging
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
        if iface not in ('jtag', 'debugwire'):
            raise BackendNotSupportedError("Debugging over {} with the {} is not supported"
                                               .format(iface, candidate.product))
        self.candidate : ProbeCandidate = candidate
        self.timers_run : bool = args.timers[0] == 'r'
        self.clkdeb : int | None = args.clkdeb   # JTAG clock in kHz while debugging (-D)
        self.clkprg : int | None = args.clkprg   # and in programming mode (-P); None: keep the probe's
        self._jtag_khz : float | None = None      # the JTAG clock set last; None: the probe's own
        self._clock_hint_given : bool = False
        for khz in {self.clkdeb, self.clkprg} - {None} if iface == 'jtag' else set():
            if jtag2.jtag_clock_khz(jtag2.jtag_clock_code(khz)) > khz:
                self.logger.warning("JTAG clock %d kHz is below the minimum of the %s; using %.1f kHz", khz,
                                        candidate.product, jtag2.jtag_clock_khz(jtag2.jtag_clock_code(khz)))
        self.transport : jtag2.Jtag2UsbTransport | None = None
        self.protocol : jtag2.Jtag2Protocol | None = None
        self.sign_on_info : jtag2.SignOn | None = None
        self._swbps : set[int] = set()       # software breakpoints (byte addresses)
        self._planted : set[int] = set()     # those the probe has planted at the last go or step
        self._pending_removals : dict[int, int] = {}  # cleared, but still in flash -> original word
        self._isp : jtag2.Jtag2Isp | None = None
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

    def _close(self) -> None:
        """Close the USB connection; errors do not matter, the probe may be gone already"""
        if self.transport is not None:
            try:
                self.transport.close()
            except usb.core.USBError:
                pass
        self.transport = None
        self.protocol = None
        self._isp = None

    def _debugwire_active(self) -> bool:
        """
        Is the target in debugWIRE mode? Measured with the AVR Dragon on an ATmega328P: while it is,
        the SPI emulator mode is refused (RSP_FAILED); when it is not, ISP works. Only a successful
        ISP entry counts as 'not active', so that the debugWIRE mode is never set blindly.
        """
        isp = jtag2.Jtag2Isp(self._proto())
        try:
            isp.enter()
        except jtag2.Jtag2Error as e:
            self.logger.debug("No ISP access, debugWIRE is active: %s", e)
            return True
        isp.close()
        return False

    def _enter_mode(self) -> None:
        """Set the emulator mode and everything that has to follow each entry into it"""
        proto = self._proto()
        mode = jtag2.EMULATOR_MODE_JTAG
        if self._iface == 'debugwire':
            if self._target_voltage() < 1.5:
                raise FatalError("Target is not powered")
            if not self._debugwire_active():
                raise FatalError("debugWIRE is not active")
            mode = jtag2.EMULATOR_MODE_DEBUGWIRE
        four_page = self._iface == 'debugwire' and self.device_info.get('buffers_per_flash_page', 1) > 1
        if four_page and self.sign_on_info is not None and self.sign_on_info.master_firmware[0] < 7:
            major, minor = self.sign_on_info.master_firmware
            raise FatalError("Firmware {:X}.{:02X} of the {} cannot write the flash of the {} over debugWIRE "
                             "(4-page erase); update it with Microchip Studio 7".format(
                                 major, minor, self.candidate.product, self._devicename))
        proto.set_parameter(jtag2.PAR_EMULATOR_MODE, bytes([mode]), jtag2.MODE_TIMEOUT)
        self._set_jtag_clock(self.clkdeb)
        if four_page and self.sign_on_info is not None:
            # The 4-page parts (ATtiny441/841/1634): only the device context (0x36, as Microchip Studio 7
            # sends it) carries the page buffers per flash block, without which the mkII writes them
            # wrongly. Measured on the ATtiny1634: that value survives a later device descriptor, which
            # restores the I/O handling of the descriptor. With the context alone, the mkII refreshes
            # its copy of every I/O register in the context's read masks at the first access after
            # each stop (312 ms instead of 29), which made single-stepping several times slower
            # (range_dw failed), and extended I/O registers outside the masks read as 0.
            proto.set_device_context(jtag2.make_device_context(self.device_info))
        proto.set_device_descriptor(jtag2.make_device_descriptor(self.device_info))
        proto.set_parameter(jtag2.PAR_TIMERS_RUNNING, bytes([int(self.timers_run)]))
        self._mode_set = True

    # ===== primitives for AvrSession ==================================================

    def _sign_on(self, announce : bool = False) -> None:
        if self.protocol is None:
            self._open()
        try:
            info = self._proto().sign_on()
        except jtag2.Jtag2UsbTimeout:
            # After a power cycle of the target, the AVR Dragon and the JTAGICE mkII never answer the
            # first command on a connection left idle during the cycle, however long one waits; after
            # reopening they do (measured)
            self.logger.debug("No answer to sign-on, reopening the probe")
            self._close()
            self._open()
            info = self._proto().sign_on()
        self.sign_on_info = info
        # PAR_SOFT_RESET stays at its default (hard reset after CMND_SIGN_OFF), on purpose. With 3, as
        # Microchip Studio 7 sets it, the probe stays on the bus after a sign-off, but an AVR Dragon
        # that has not been reset since its last sign-on hangs at the next power cycle of the target,
        # until it is replugged (see release; the JTAGICE mkII clone forgets the 3 at the next
        # sign-off and does not hang)
        if announce:
            self.logger.info("Signed on to: %s FW: %X.%02X, HW: %d, SN: %s", info.ident,
                                 info.master_firmware[0], info.master_firmware[1],
                                 info.master_hardware, info.serial)
            if info.master_firmware[0] < 7:
                self.logger.warning("Firmware %X.%02X is old; single steps can be slow "
                                        "(update it with Microchip Studio)", *info.master_firmware)

    def _sign_off(self) -> None:
        """
        Only leave the emulator mode. CMND_SIGN_OFF is never sent: after it, the probe leaves the
        bus for about 3 s and enumerates again, and the session signs off and on again several times
        while it prepares debugWIRE -- long enough for GDB to give up waiting for the answer to
        'monitor debugwire enable' (its remotetimeout is 2 s). A later process opens the probe,
        discards what is left in it, and signs on, which works without a sign-off before.
        """
        if self.protocol is None:
            return
        if self._isp is not None:
            if self._isp.protocol is self.protocol:
                self._isp.close()
            self._isp = None
        if self._mode_set:
            self.protocol.set_parameter(jtag2.PAR_EMULATOR_MODE, bytes([jtag2.EMULATOR_MODE_UNKNOWN]))
            self._mode_set = False

    def _target_voltage(self) -> float:
        if self.protocol is None:  # the session reads it while waiting for a power cycle, signed off
            self._sign_on()
        return int.from_bytes(self._proto().get_parameter(jtag2.PAR_OCD_VTARGET), 'little') / 1000

    def _configure_session(self) -> None:
        self._enter_mode()
        self.logger.info("Emulator mode, device data and timer mode communicated to tool")

    def _activate_interface(self, graceful : bool = False) -> int:
        """
        The id the session expects for the signature check: the JTAG ID, or on debugWIRE the
        signature without the 0x1E (PAR_TARGET_SIGNATURE: 0x950F for the ATmega328P)
        """
        _dummy = graceful
        if self._target_voltage() < 1.5:
            raise FatalError("Target is not powered")
        if self._iface == 'debugwire':
            signature = int.from_bytes(self._proto().get_parameter(jtag2.PAR_TARGET_SIGNATURE), 'little')
            self.logger.info("debugWIRE signature: 0x%04X", signature)
            return signature
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
        """
        Measured with the AVR Dragon on an ATmega328P (2026-10-24): after CMND_RESET with the debugWIRE
        disable flag, the probe refuses the SPI mode -- and so ISP, which the session needs next for
        DWEN -- until it has been signed off, however long one waits (15 s tried). So sign off here,
        and open the probe again. Not reproducible on 2026-10-26: the same Dragon (FW 7.27) accepted the
        SPI mode at once on an ATmega328P and an ATtiny1634, with and without the sign-off, with
        PAR_SOFT_RESET 0 and 3; the sign-off stays as a precaution. With PAR_SOFT_RESET at its default
        (see _sign_on), the probe then leaves the bus, so wait until it is back.
        """
        proto = self._proto()
        proto.debugwire_disable()
        proto.set_parameter(jtag2.PAR_EMULATOR_MODE, bytes([jtag2.EMULATOR_MODE_UNKNOWN]))
        self._mode_set = False
        proto.sign_off()
        self._close()
        self._wait_for_reenumeration(gone=0.6)   # measured: a probe that resets is gone after 0.2 s

    def _wait_for_reenumeration(self, gone : float = 2.0, back : float = 6.0) -> None:
        """See wait_for_reenumeration; _sign_on opens the probe again"""
        wait_for_reenumeration(self.candidate, gone, back)

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
        self._breakpoints_updated()

    def _go_to(self, address : int) -> None:
        self._proto().drain_breaks()
        self._proto().run_to(address >> 1)
        self._breakpoints_updated()

    def _single_step(self) -> None:
        self._proto().drain_breaks()
        try:
            self._proto().single_step()
            self._proto().wait_for_break()
        except jtag2.Jtag2Error:
            self._clock_hint()
            raise
        self._breakpoints_updated()

    def _breakpoints_updated(self) -> None:
        """After a go or step, the probe has planted the set software breakpoints and removed the cleared ones"""
        self._planted = set(self._swbps)
        self._pending_removals.clear()

    def _flush_pending_removals(self) -> None:
        """
        Before flash is written (a load): remove the cleared software breakpoints from flash now,
        or the probe writes the old words into the new program at the next go. CMND_RESTORE_TARGET
        does it at once, but it resets the target, lets it run, and makes the probe forget the
        breakpoints that are still set; so stop again and set those once more.
        """
        if not self._pending_removals:
            return
        self.logger.debug("Removing %d cleared software breakpoint(s) from flash before writing",
                              len(self._pending_removals))
        self._proto().restore_target()
        time.sleep(0.1)
        self.stop()
        self._pending_removals.clear()
        self._planted.clear()
        for address in sorted(self._swbps):
            self._proto().set_break(jtag2.SOFTWARE_BREAKPOINT, address >> 1)

    def _regfile_read_raw(self) -> bytearray:
        return bytearray(self._proto().read_memory(jtag2.MEMTYPE_SRAM, 0, 32))

    def _regfile_write_raw(self, regs : bytes) -> None:
        self._proto().write_memory(jtag2.MEMTYPE_SRAM, 0, bytes(regs))

    def _pc_read_raw(self) -> int:
        return self._proto().read_pc()

    # ISP, for debugWIRE targets while DWEN is not programmed
    def _isp_session(self) -> jtag2.Jtag2Isp:
        if self._isp is None:
            raise FatalError("ISP programming mode not entered")
        return self._isp

    def _isp_open(self) -> None:
        if self._isp is None or self._isp.protocol is not self._proto():  # a new session after a sign-off
            self._isp = jtag2.Jtag2Isp(self._proto())
        self._isp.enter()

    def _isp_enter(self) -> None:
        self._isp_session().enter()

    def _isp_leave(self) -> None:
        """
        Leave the SPI mode as well: the session power-cycles the target next, and afterwards the
        Dragon took more than 2 s to leave the SPI mode (e2e run on the Uno). _isp_enter sets it again.
        """
        self._isp_session().close()

    def _isp_device_id(self) -> int:
        return self._isp_session().signature()

    def _isp_read_fuse(self, addr : int) -> bytes:
        return bytes([self._isp_session().read_fuse(addr)])

    def _isp_write_fuse(self, addr : int, data : bytearray) -> None:
        self._isp_session().write_fuse(addr, data[0])

    def _isp_read_lock(self) -> bytes:
        return bytes([self._isp_session().read_lock()])

    def _isp_erase(self) -> None:
        self._isp_session().chip_erase()

    def _isp_write_flash(self, address : int, data : bytes) -> None:
        page = self.device_info['flash_page_size_bytes']
        for offset in range(0, len(data), page):
            self._isp_session().write_flash_page(address + offset, bytes(data[offset:offset + page]))

    # ===== DebugBackend ==================================================================

    def guard_transactions(self) -> None:
        """Jtag2Protocol.command runs every command with its response inside termination.transaction()"""

    def is_set_up(self) -> bool:
        return self.protocol is not None

    def release(self) -> None:
        """
        At the end of the server, a real CMND_SIGN_OFF, which the session's own sign-offs avoid (see
        _sign_off). With PAR_SOFT_RESET at its default, the probe then resets. An AVR Dragon that has
        not been reset since its last sign-on hangs at the next power cycle of the target, for every
        program, ISP included, until it is replugged; a sign-on alone is enough for that (measured
        2026-10-27, FW 7.27). A killed server cannot prevent it.
        """
        if self.protocol is None:
            return
        try:
            self._sign_off()
            self.protocol.sign_off()
        except (BackendError, usb.core.USBError) as e:
            self.logger.debug("Final sign-off: %s", e)
        finally:
            self._close()

    @staticmethod
    def reboot_probe(candidate : ProbeCandidate, args : argparse.Namespace, logger : logging.Logger) -> bool:
        """
        --reboot-debugger: sign off with PAR_SOFT_RESET set to a hard reset, after which the probe leaves
        the bus and enumerates again, then sign on to it once more. Needs no target and no device data.
        Returns False if the probe does not come back or does not answer.
        """
        _dummy = args
        logger.info("Rebooting debugger...")
        try:
            transport = jtag2.Jtag2UsbTransport.open(tool=candidate.tool, serial_suffix=candidate.address)
            try:
                proto = jtag2.Jtag2Protocol(transport)
                proto.sign_on()
                proto.set_parameter(jtag2.PAR_SOFT_RESET, bytes([jtag2.SOFT_RESET_HARD]))
                proto.sign_off()
            finally:
                transport.close()
            if not wait_for_reenumeration(candidate, gone=2.0, back=6.0):
                logger.critical("... could not reconnect")
                return False
            # it may be there before it answers: try for a while
            deadline = time.monotonic() + 5
            while True:
                try:
                    transport = jtag2.Jtag2UsbTransport.open(tool=candidate.tool, serial_suffix=candidate.address)
                    try:
                        jtag2.Jtag2Protocol(transport).sign_on()
                    finally:
                        transport.close()
                    break
                except (jtag2.Jtag2Error, usb.core.USBError):
                    if time.monotonic() > deadline:
                        raise
                    time.sleep(0.3)
        except (jtag2.Jtag2Error, usb.core.USBError) as e:
            logger.critical("Could not reboot the %s: %s", candidate.product, e)
            return False
        logger.info("Reconnected to %s", candidate.product)
        return True

    def get_toolname(self) -> str:
        return self.candidate.product

    def reactivate(self) -> None:
        """The timer mode needs no reactivation on the mkII, but callers expect a reset (after a load)"""
        self.reset()

    def switch_to_progmode(self) -> bool:
        """On debugWIRE, programming and debugging mode are the same, as with the EDBG probes"""
        if self._iface == 'jtag':
            self._flush_pending_removals()
            self._set_jtag_clock(self.clkprg)
            self._proto().enter_progmode()
        return True

    def switch_to_debmode(self) -> bool:
        if self._iface == 'jtag':
            self._proto().leave_progmode()
            self._proto().drain_breaks()
            self._set_jtag_clock(self.clkdeb)
        return True

    def _set_jtag_clock(self, khz : int | None) -> None:
        """The JTAG clock for -D or -P, on JTAG targets only, never above khz unless that is below the minimum"""
        if self._iface != 'jtag' or khz is None:
            return
        code = jtag2.jtag_clock_code(khz)
        self.logger.debug("JTAG clock: %.1f kHz (asked for %d kHz)", jtag2.jtag_clock_khz(code), khz)
        self._proto().set_parameter(jtag2.PAR_OCD_JTAG_CLK, bytes([code]))
        self._proto().byte_ms = jtag2.jtag_byte_ms(code)
        self._jtag_khz = jtag2.jtag_clock_khz(code)

    def _clock_hint(self) -> None:
        """
        On JTAG, with TCK above a quarter of the MCU clock, stops of the running target time out at
        random and single steps fail (RSP_ILLEGAL_MCU_STATE) or end at wrong addresses (measured with
        the mkII on an ATmega324P at 128 kHz: up to 32.6 kHz all fine, from 47.8 kHz on not). The
        default -D keeps below it if -F is right; so after such an error, point to both, once.
        """
        if self._iface != 'jtag' or self._clock_hint_given:
            return
        self._clock_hint_given = True
        khz = self._jtag_khz if self._jtag_khz is not None else jtag2.jtag_clock_khz(6)   # the probe's default
        self.logger.warning("The JTAG clock (%.1f kHz) may be too fast for the MCU clock, which must be more "
                                "than four times faster; check -F (now %s Hz) or lower -D", khz, self.args.F_CPU)

    def stop(self) -> None:
        """Stop and consume the break events, so that poll_event does not report a stop later"""
        try:
            self._proto().forced_stop()
            self._proto().wait_for_break()
        except jtag2.Jtag2Error:
            self._clock_hint()
            raise
        self._proto().drain_breaks()

    def reset(self) -> None:
        self.logger.info("MCU reset")
        self._proto().drain_breaks()
        self._proto().reset()
        self._proto().wait_for_break()
        # after a power cycle more than one EVT_BREAK may come; a stale one would make the handler
        # report a stop to GDB in the middle of a monitor command (seen as 'Invalid hex digit 83')
        self._proto().drain_breaks()

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
        # on debugWIRE always FLASH_PAGE: the Dragon with firmware 6.0B refuses SPM there
        memtype = jtag2.MEMTYPE_FLASH_PAGE if prog_mode or self._iface == 'debugwire' else jtag2.MEMTYPE_SPM
        start = address - address % page
        end = address + numbytes
        data = bytearray()
        for base in range(start, end, page):
            data += self._proto().read_memory(memtype, base, page)
        for bp, orig in self._pending_removals.items():    # BREAKs the probe has not removed yet
            for i in (0, 1):
                if start <= bp + i < end:
                    data[bp + i - start] = (orig >> (8*i)) & 0xFF
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
        if self._iface == 'debugwire':
            self.logger.debug("No chip erase on debugWIRE; pages are erased when they are written")
            return
        if not prog_mode:
            self.switch_to_progmode()
        self._proto().chip_erase()
        if not prog_mode:
            self.switch_to_debmode()

    def erase_flash_page(self, address : int, prog_mode : bool) -> bool:
        """
        In debug mode only, as with the EDBG probes. On debugWIRE nothing to do: writing a page with
        FLASH_PAGE erases it first (measured: a page written over an older program reads back right)
        """
        if self._iface == 'debugwire':
            return False
        if prog_mode:
            self.switch_to_debmode()
        self._flush_pending_removals()
        self._proto().erase_page_spm(address)
        if prog_mode:
            self.switch_to_progmode()
        return True

    def write_flash_pages(self, address : int, data : bytes, prog_mode : bool) -> None:
        if self._iface == 'debugwire' or not prog_mode:  # on JTAG, switch_to_progmode has done it
            self._flush_pending_removals()
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
        self._pending_removals.pop(address, None)
        return True

    def software_breakpoint_clear(self, address : int) -> None:
        if address in self._planted:
            original = self._flash_read(address, 2)    # the probe still shows the original word
            self._pending_removals[address] = original[0] | (original[1] << 8)
            self._planted.discard(address)
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


def wait_for_reenumeration(candidate : ProbeCandidate, gone : float = 2.0, back : float = 6.0) -> bool:
    """
    After a sign-off without PAR_SOFT_RESET, the probe leaves the bus for 1.5 to 3 s. Opening it
    before it has gone can still succeed, and then commands reach a restarting probe. So wait
    until it has gone, at most 'gone' seconds, then until it is back, at most 'back' seconds.
    A probe that does not leave the bus within 'gone' has not reset. Returns whether it is there.
    """
    def present() -> bool:
        return any(c.address == candidate.address for c in jtag2.discover(candidate.tool))
    deadline = time.monotonic() + gone
    while present() and time.monotonic() < deadline:
        time.sleep(0.1)
    deadline = time.monotonic() + back
    while not present() and time.monotonic() < deadline:
        time.sleep(0.2)
    return present()
