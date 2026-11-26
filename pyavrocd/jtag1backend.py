"""
The debugger backend for the JTAGICE mkI and its clones (protocol AVR060, pyavrocd.jtag1), on a
serial port. JTAG targets only, and only the parts the mkI knows (MKI_PARTS). The probe-independent
session logic is in session.py; this module supplies the primitives it needs.

What is different from the mkII backend:
- the probe is a serial port; with more than one, -u names it by the end of its name
- hardware breakpoints only (SwbpSupport.NONE): the mkI has no command for software breakpoints.
  The server could plant them (page erase and IReg injection work), but only with a number of
  special cases, see docs/jtagice1-software-breakpoints.md. Four comparators: PSB0 and PSB1
  through memory type 0x60, X and Y through parameters and the break control register. The probe
  clears them at every break, so all of them are sent before each go; there are no clear commands.
- no run-to-address command: run_to sets one more comparator
- a load needs 'erase before load' (the default on JTAG), since the backend does not erase single
  pages
- the CH340 clone does not measure the target voltage (always 0xFF), and the baud rate it
  reports is meaningless (0x17); the Olimex clone reports both properly (5.05 V as 0xCE). The
  server switches to 115200 and back to 19200 at the end
- FORCED_STOP on a target that is stopped already lets it run a few instructions (measured: the PC
  moves on by 4 words each time), so the backend sends it only while the target runs; after a
  reset, step or stop, the probe sends no break message (measured), so none is waited for
"""
import argparse
import logging

from serial.tools import list_ports

from pyavrocd import jtag1
from pyavrocd.backend import SwbpSupport, BackendError, BackendNotSupportedError, ProbeCandidate
from pyavrocd.session import AvrSession
from pyavrocd.errors import FatalError

TOOL : str = 'jtagice1'
PRODUCT : str = 'JTAGICE mkI'
# the parts the mkI is documented for (and avrdude 8.3 lists for it): m16(A), m32(A), m64(A), m128(A),
# m162, m169(A), AT90CAN128; there is no device file for the original ATmega169. The ATmega169P worked
# on an AVR Butterfly as well (same signature, JTAG part number and OCD revision as the 169), but is
# left out, as it is not documented for the mkI.
MKI_PARTS : tuple[str, ...] = ('atmega16', 'atmega16a', 'atmega32', 'atmega32a', 'atmega64', 'atmega64a',
                               'atmega128', 'atmega128a', 'atmega162', 'atmega169a', 'at90can128')
BP_X_ON : int = 0x20              # break control: comparator X on, as program breakpoint
BP_X_PROGRAM : int = 0x0C
BP_Y_ON : int = 0x10              # comparator Y on (only together with X)
BP_Y_PROGRAM : int = 0x03
# Data breakpoints on X and Y: the mode (0 read, 1 write, 2 access) goes into bits 3:2 for X and
# bits 1:0 for Y. The break status (Resp_BREAK, parameter 0x87) has bit 2 for X, bit 3 for Y, bit 5
# for PSB0 and bit 7 for a step, several at once (measured on the Olimex clone, ATmega32)
BREAK_STATUS_X : int = 0x04
BREAK_STATUS_Y : int = 0x08


def discover() -> list[ProbeCandidate]:
    """Every USB serial port is a candidate; which one is the mkI only the sign-on can tell"""
    return [ProbeCandidate(tool=TOOL, product=PRODUCT, address=port.device, serial=port.serial_number or "")
            for port in list_ports.comports() if port.vid is not None]


def supported_part(devicename : str) -> bool:
    """Can the mkI debug this MCU?"""
    return devicename.lower() in MKI_PARTS


def jtag_clock_code(khz : int) -> tuple[int, int]:
    """The JTAG clock code for at most khz kHz, and its frequency; at least 125 kHz"""
    for clock in sorted(jtag1.JTAG_CLOCK_CODES, reverse=True):
        if clock <= khz:
            return jtag1.JTAG_CLOCK_CODES[clock], clock
    return jtag1.JTAG_CLOCK_CODES[125], 125


#pylint: disable=too-many-public-methods,too-many-instance-attributes
class Jtag1Backend(AvrSession):
    """
    Backend for the JTAGICE mkI
    """
    SWBP_SUPPORT = SwbpSupport.NONE

    def __init__(self, candidate : ProbeCandidate, devicename : str, iface : str,
                     args : argparse.Namespace) -> None:
        AvrSession.__init__(self, devicename, iface, args)
        if iface != 'jtag':
            raise BackendNotSupportedError("The {} can only debug JTAG targets".format(PRODUCT))
        if not supported_part(devicename):
            raise BackendNotSupportedError("The {} cannot debug the {}".format(PRODUCT, devicename))
        self.candidate : ProbeCandidate = candidate
        self.timers_run : bool = args.timers[0] == 'r'
        self.clkdeb : int | None = args.clkdeb
        self.clkprg : int | None = args.clkprg
        self.transport : jtag1.Jtag1SerialTransport | None = None
        self.protocol : jtag1.Jtag1Protocol | None = None
        self._hwbps : dict[int, int] = {}       # comparator index (1-3) -> byte address
        self._data_bps : dict[int, tuple[int, int]] = {}  # index (2, 3) -> (data address, mode)
        self._data_on : dict[int, int] = {}     # break status bit of X/Y -> index of its data breakpoint
        self._break_status : int = 0            # break status of the last stop
        self._running : bool = True             # may the target run? Unknown counts as running
        self._ext_reset_held : bool = False
        self.logger.info("mkI backend on %s, iface: %s, HWBPs: %d", candidate.address, iface, self._hwbpnum)
        if self.manage == []:
            self.manage = [ 'none' ]
        self.logger.info("Managing fuses: %s", ", ".join(self.manage))

    # ----- the protocol, opened on demand ----------------------------------------

    def _proto(self) -> jtag1.Jtag1Protocol:
        if self.protocol is None:
            raise FatalError("Not signed on to the {}".format(PRODUCT))
        return self.protocol

    def _open(self) -> None:
        """Open the port, find the speed the probe listens at, and switch to the fast one"""
        self.transport = jtag1.Jtag1SerialTransport(self.candidate.address)
        self.protocol = jtag1.Jtag1Protocol(self.transport)
        try:
            baud = self.protocol.sync()
            self.logger.debug("%s answers at %d bps", PRODUCT, baud)
            if baud != jtag1.FAST_BAUD:
                self.protocol.set_baud(jtag1.FAST_BAUD)
        except BackendError:
            self._close()
            raise

    def _close(self) -> None:
        if self.transport is not None:
            self.transport.close()
        self.transport = None
        self.protocol = None

    def _set_jtag_clock(self, khz : int | None) -> None:
        """The JTAG clock for -D or -P"""
        if khz is None:
            return
        code, clock = jtag_clock_code(khz)
        if clock > khz:
            self.logger.warning("JTAG clock %d kHz is below the minimum of the %s; using %d kHz", khz, PRODUCT, clock)
        self.logger.debug("JTAG clock: %d kHz (asked for %d kHz)", clock, khz)
        self._proto().set_parameter(jtag1.PAR_OCD_JTAG_CLOCK, code)

    # ===== primitives for AvrSession ==================================================

    def _sign_on(self, announce : bool = False) -> None:
        if self.protocol is None:
            self._open()
        proto = self._proto()
        ident = proto.sign_on()
        if announce:
            self.logger.info("Signed on to: %s (%s), HW: 0x%02X, SW: 0x%02X, on %s", PRODUCT, ident,
                                 proto.get_parameter(jtag1.PAR_HW_VERSION),
                                 proto.get_parameter(jtag1.PAR_SW_VERSION), self.candidate.address)

    def _sign_off(self) -> None:
        """The port stays open for the whole session; see release"""

    def _target_voltage(self) -> float:
        """6.25 V at 0xFF (avrdude's scale); the CH340 clone always reports 0xFF"""
        if self.protocol is None:
            self._sign_on()
        return 6.25 * self._proto().get_parameter(jtag1.PAR_OCD_VTARGET) / 255

    def _configure_session(self) -> None:
        proto = self._proto()
        proto.forced_stop()
        proto.set_device_descriptor(jtag1.make_device_descriptor(self.device_info, self.masked_registers))
        self._set_jtag_clock(self.clkdeb)
        proto.set_parameter(jtag1.PAR_TIMERS_RUNNING, int(self.timers_run))
        self.logger.info("Device data and timer mode communicated to tool")

    def _activate_interface(self, graceful : bool = False) -> int:
        """The JTAG ID. Reading it lets a stopped target run again (avarice), so a stop follows."""
        _dummy = graceful
        if self._target_voltage() < 1.5:
            raise FatalError("Target is not powered")
        self._running = True
        jtag_id = self._proto().jtag_id()
        if jtag_id in (0, 0xFFFFFFFF):
            # as with the mkII: a sleeping target may answer only with its reset line held
            self._proto().set_parameter(jtag1.PAR_EXTERNAL_RESET, 1)
            self._ext_reset_held = True
            jtag_id = self._proto().jtag_id()
            if jtag_id not in (0, 0xFFFFFFFF):
                self.logger.info("Target reachable over JTAG only with its reset line held")
        self.logger.info("JTAG ID: 0x%08X", jtag_id)
        return jtag_id

    def _attach_and_stop(self) -> None:
        self.stop()

    def _clear_all_breakpoints(self) -> None:
        self._hwbps.clear()

    def _debugwire_disable(self) -> None:
        raise BackendNotSupportedError("The {} has no debugWIRE".format(PRODUCT))

    def _detach(self) -> None:
        """Nothing to do: the target runs on"""

    def _deactivate_interface(self) -> None:
        """Nothing to do"""

    def _leave_progmode(self) -> None:
        """After OCDEN has been unprogrammed, leaving may be refused, as with the mkII"""
        try:
            self._proto().leave_progmode()
        except jtag1.Jtag1Error as e:
            self.logger.debug("Leaving programming mode without OCD: %s", e)

    def _ocd_erase(self) -> None:
        self._proto().chip_erase()

    def _send_breakpoints(self, cursor : int | None = None) -> None:
        """
        All hardware breakpoints, before a go: the cursor of run_to first, then the others, on PSB0,
        PSB1, X and Y (as avarice assigns them); word addresses
        """
        addresses = ([cursor] if cursor is not None else []) + [self._hwbps[ix] for ix in sorted(self._hwbps)]
        words = [(address | self.bad_pc_bit_mask) >> 1 for address in addresses]
        # X and Y: the data breakpoints first (Y works only together with X), then program ones
        combined : list[tuple[int, int, int | None]] = \
            [(address, data_mode, ix) for ix, (address, data_mode) in sorted(self._data_bps.items())]
        if len(words) > 4 - len(combined):
            raise BackendError("More than four hardware breakpoints")
        combined += [(word, -1, None) for word in words[2:]]
        proto = self._proto()
        for number, word in enumerate(words[:2]):
            proto.set_program_breakpoint(number, word)
        mode = 0
        self._data_on = {}
        if combined:
            address, data_mode, ix = combined[0]
            proto.set_parameter(jtag1.PAR_BREAK_ADDR1_HIGH, address >> 8)
            proto.set_parameter(jtag1.PAR_BREAK_ADDR1_LOW, address & 0xFF)
            mode |= BP_X_ON | (BP_X_PROGRAM if data_mode < 0 else data_mode << 2)
            if ix is not None:
                self._data_on[BREAK_STATUS_X] = ix
        if len(combined) > 1:
            address, data_mode, ix = combined[1]
            proto.set_parameter(jtag1.PAR_BREAK_ADDR2_HIGH, address >> 8)
            proto.set_parameter(jtag1.PAR_BREAK_ADDR2_LOW, address & 0xFF)
            mode |= BP_Y_ON | (BP_Y_PROGRAM if data_mode < 0 else data_mode)
            if ix is not None:
                self._data_on[BREAK_STATUS_Y] = ix
        if mode:
            proto.set_parameter(jtag1.PAR_COMB_BREAK_CTRL, mode)

    def _go(self) -> None:
        self._break_status = 0
        self._send_breakpoints()
        self._proto().go()
        self._running = True

    def _go_to(self, address : int) -> None:
        self._break_status = 0
        self._send_breakpoints(cursor=address)
        self._proto().go()
        self._running = True

    def _single_step(self) -> None:
        """
        The probe clears all breakpoints at a break; a step reports a data breakpoint that fires in
        it, if it was set right before (measured: status 0x84 = step + X). So the data breakpoints
        are set before the step, and the break cause read afterwards.
        """
        self._break_status = 0
        if self._data_bps:
            self._send_breakpoints()
        self._proto().single_step()
        if self._data_bps:
            self._break_status = self._proto().get_parameter(jtag1.PAR_OCD_BREAK_CAUSE)

    def _regfile_read_raw(self) -> bytearray:
        return bytearray(self._proto().read_memory(jtag1.MEMTYPE_SRAM, 0, 32))

    def _regfile_write_raw(self, regs : bytes) -> None:
        self._proto().write_memory(jtag1.MEMTYPE_SRAM, 0, bytes(regs))

    def _pc_read_raw(self) -> int:
        return self._proto().read_pc()

    def _no_isp(self) -> None:
        raise BackendNotSupportedError("The {} has no ISP".format(PRODUCT))

    def _isp_open(self) -> None:
        self._no_isp()

    def _isp_enter(self) -> None:
        self._no_isp()

    def _isp_leave(self) -> None:
        self._no_isp()

    def _isp_device_id(self) -> int:
        self._no_isp()
        return 0

    def _isp_read_fuse(self, addr : int) -> bytes:
        self._no_isp()
        return b''

    def _isp_write_fuse(self, addr : int, data : bytearray) -> None:
        self._no_isp()

    def _isp_read_lock(self) -> bytes:
        self._no_isp()
        return b''

    def _isp_erase(self) -> None:
        self._no_isp()

    def _isp_write_flash(self, address : int, data : bytes) -> None:
        self._no_isp()

    # ===== DebugBackend ==================================================================

    def guard_transactions(self) -> None:
        """Jtag1Protocol runs every command with its answer inside termination.transaction()"""

    def is_set_up(self) -> bool:
        return self.protocol is not None

    def release(self) -> None:
        """Back to the start speed, where the next session (or another program) expects the probe"""
        if self.protocol is None:
            return
        try:
            self.protocol.set_baud(jtag1.START_BAUD)
        except BackendError as e:
            self.logger.debug("Switching back to %d bps: %s", jtag1.START_BAUD, e)
        finally:
            self._close()

    @staticmethod
    def reboot_probe(candidate : ProbeCandidate, args : argparse.Namespace, logger : logging.Logger) -> bool:
        """The mkI cannot be rebooted; check that it answers and leave it at the start speed"""
        _dummy = args
        try:
            transport = jtag1.Jtag1SerialTransport(candidate.address)
            try:
                proto = jtag1.Jtag1Protocol(transport)
                if proto.sync() != jtag1.START_BAUD:
                    proto.set_baud(jtag1.START_BAUD)
            finally:
                transport.close()
        except BackendError as e:
            logger.critical("No %s answers on %s: %s", PRODUCT, candidate.address, e)
            return False
        logger.info("The %s cannot be rebooted; it answers on %s", PRODUCT, candidate.address)
        return True

    def get_toolname(self) -> str:
        return PRODUCT

    def reactivate(self) -> None:
        """Callers expect a reset (after a load)"""
        self.reset()

    def switch_to_progmode(self) -> bool:
        self._set_jtag_clock(self.clkprg)
        self._proto().enter_progmode()
        if self._ext_reset_held:  # programming mode holds the MCU in reset over JTAG
            self._proto().set_parameter(jtag1.PAR_EXTERNAL_RESET, 0)
            self._ext_reset_held = False
        return True

    def switch_to_debmode(self) -> bool:
        self._proto().leave_progmode()
        self._set_jtag_clock(self.clkdeb)
        self._running = True     # unknown after programming mode
        return True

    def stop(self) -> None:
        """Only a running target, see the module docstring"""
        if self._running:
            self._proto().forced_stop()
            self._running = False

    def reset(self) -> None:
        self.logger.info("MCU reset")
        self._proto().reset()
        self._running = False

    def poll_event(self) -> int | None:
        if not self._running:
            return None
        status = self._proto().poll_break(0)
        if status is None:
            return None
        self._running = False
        self._break_status = status
        return self._proto().read_pc() << 1

    def program_counter_write(self, program_counter : int) -> None:
        self._proto().write_pc(program_counter)

    def stack_pointer_read(self) -> bytearray:
        sp = bytearray(self._proto().read_memory(jtag1.MEMTYPE_SRAM, 0x5D, 2))
        if 0x5E in self.masked_registers:
            sp[1] = 0
        return sp

    def stack_pointer_write(self, data : bytes) -> None:
        self._proto().write_memory(jtag1.MEMTYPE_SRAM, 0x5D, bytes(data))

    def status_register_read(self) -> bytearray:
        return bytearray(self._proto().read_memory(jtag1.MEMTYPE_SRAM, self._sregaddr, 1))

    def status_register_write(self, data : bytes) -> None:
        self._proto().write_memory(jtag1.MEMTYPE_SRAM, self._sregaddr, bytes(data))

    def sram_read(self, address : int, numbytes : int) -> bytearray:
        return bytearray(self._proto().read_memory(jtag1.MEMTYPE_SRAM, address, numbytes))

    def sram_write(self, address : int, data : bytes) -> None:
        self._proto().write_memory(jtag1.MEMTYPE_SRAM, address, bytes(data))

    def _flash_read(self, address : int, numbytes : int, prog_mode : bool = False) -> bytearray:
        """In words, from an even address; PML in debug mode, FLASH_PAGE in programming mode"""
        memtype = jtag1.MEMTYPE_FLASH_PAGE if prog_mode else jtag1.MEMTYPE_PML
        start = address & ~1
        end = address + numbytes
        count = end - start + ((end - start) & 1)
        data = self._proto().read_memory(memtype, start >> 1, count)
        return bytearray(data[address - start:end - start])

    def eeprom_read(self, address : int, numbytes : int, prog_mode : bool = False) -> bytes:
        memtype = jtag1.MEMTYPE_EEPROM_PAGE if prog_mode else jtag1.MEMTYPE_EEPROM
        return self._proto().read_memory(memtype, address, numbytes)

    def eeprom_write(self, address : int, data : bytes, prog_mode : bool = False) -> None:
        """
        In programming mode by whole aligned pages, read-modify-write, as for the mkII on the
        ATmega128 (AVR060 allows byte writes, too; not measured)
        """
        if not prog_mode:
            self._proto().write_memory(jtag1.MEMTYPE_EEPROM, address, bytes(data))
            return
        page = self.device_info['eeprom_page_size_bytes']
        end = address + len(data)
        for base in range(address - address % page, end, page):
            content = bytearray(self._proto().read_memory(jtag1.MEMTYPE_EEPROM_PAGE, base, page))
            for a in range(max(base, address), min(base + page, end)):
                content[a - base] = data[a - address]
            self._proto().write_memory(jtag1.MEMTYPE_EEPROM_PAGE, base, bytes(content))

    def read_fuse(self, addr : int, size : int) -> bytearray:
        return bytearray(self._proto().read_memory(jtag1.MEMTYPE_FUSE, addr, size))

    def write_fuse(self, addr : int, data : bytes) -> None:
        self._proto().write_memory(jtag1.MEMTYPE_FUSE, addr, bytes(data))

    def read_lock(self, addr : int, size : int) -> bytearray:
        return bytearray(self._proto().read_memory(jtag1.MEMTYPE_LOCK, addr, size))

    def write_lock(self, addr : int, data : bytes) -> None:
        self._proto().write_memory(jtag1.MEMTYPE_LOCK, addr, bytes(data))

    def read_sig(self, addr : int, size : int) -> bytearray:
        data = bytearray(self._proto().read_memory(jtag1.MEMTYPE_SIGNATURE, 0, 3))
        data += bytes([0xFF] * max(0, addr + size - 3))
        return data[addr:addr + size]

    def erase_chip(self, prog_mode : bool) -> None:
        """With '-m eesave', EESAVE is programmed for the erase, as in the mkII backend"""
        if not prog_mode:
            self.switch_to_progmode()
        eesave_base : int | None = self.device_info.get('eesave_base')
        eesave_mask : int | None = self.device_info.get('eesave_mask')
        saved_fuse : bytes | None = None
        if 'eesave' in self.manage:
            if eesave_base is not None and eesave_mask:
                fuse = self._proto().read_memory(jtag1.MEMTYPE_FUSE, eesave_base, 1)
                if fuse[0] & eesave_mask:
                    self._proto().write_memory(jtag1.MEMTYPE_FUSE, eesave_base, bytes([fuse[0] & ~eesave_mask & 0xFF]))
                    saved_fuse = fuse
                    self.logger.debug("EESAVE programmed temporarily")
            else:
                self.logger.error("EESAVE fuse data unknown. EEPROM will be deleted")
        self._proto().chip_erase()
        if saved_fuse is not None and eesave_base is not None:
            self._proto().write_memory(jtag1.MEMTYPE_FUSE, eesave_base, saved_fuse)
            self.logger.debug("EESAVE fuse restored")
        if not prog_mode:
            self.switch_to_debmode()

    def erase_flash_page(self, address : int, prog_mode : bool) -> bool:
        raise FatalError("The {} cannot erase a single flash page; "
                         "use 'monitor erasebeforeload enable' (the default)".format(PRODUCT))

    def write_flash_pages(self, address : int, data : bytes, prog_mode : bool) -> None:
        if not prog_mode:
            raise FatalError("The {} writes flash in programming mode only".format(PRODUCT))
        page = self.device_info['flash_page_size_bytes']
        for offset in range(0, len(data), page):
            self._proto().write_memory(jtag1.MEMTYPE_FLASH_PAGE, (address + offset) >> 1,
                                       bytes(data[offset:offset + page]), timeout=2 * jtag1.TIMEOUT)

    def hardware_breakpoint_set(self, ix : int, address : int) -> None:
        """Remembered; sent before the next go"""
        self._hwbps[ix] = address

    def hardware_breakpoint_clear(self, ix : int) -> None:
        self._hwbps.pop(ix, None)
        self._data_bps.pop(ix, None)

    def data_breakpoint_slots(self) -> list[int]:
        """The combined comparators X and Y can compare data addresses"""
        return [2, 3] if self._architecture == 'avr8' else []

    def data_breakpoint_set(self, ix : int, address : int, mode : int) -> None:
        """Remembered; sent before the next go or step, on X or Y"""
        self._hwbps.pop(ix, None)
        self._data_bps[ix] = (address, mode)

    def data_breakpoints_hit(self) -> list[int]:
        """The data breakpoints that caused the last stop, by the X and Y bits of the break status"""
        return [ix for bit, ix in self._data_on.items() if self._break_status & bit]

    def can_set_run_timers(self) -> bool:
        return True

    def set_run_timers(self, run : bool) -> None:
        self.timers_run = run
        if self.protocol is not None:
            self._proto().set_parameter(jtag1.PAR_TIMERS_RUNNING, int(run))
