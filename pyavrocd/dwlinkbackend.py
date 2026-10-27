"""
The debugger backend for dw-link from version 7 on: an Arduino turned into a debugWIRE probe that
speaks a subset of the JTAGICE mkII protocol (AVR067) over its serial line. The protocol layer is the
mkII's (pyavrocd.jtag2 with the serial transport), and most of the backend is Jtag2Backend's. What
is different:

- the probe is one of the serial ports; with more than one, -u names it by the end of its name
- software breakpoints are planted by the server (SwbpSupport.SERVER); a step at a BREAK injects the
  original instruction with the vendor command EXECUTE_INSTRUCTION
- the device data go as the device context (0x36), which carries the page buffers per flash block
  (the parts with a 4-page erase); dw-link takes the device descriptor (0x0C) as well
- a failed debugWIRE sync costs nothing, so the sync itself tells whether debugWIRE is active (the
  mkII backend tries ISP instead, and dw-link switches debugWIRE off when ISP fails)
- leaving debugWIRE needs no sign-off, and there is no re-enumeration
- after RSP_FAILED and RSP_DEBUGWIRE_SYNC_FAILED, dw-link's error number says why
- target power: the dw-probe shield can switch it, and power-cycle the target by itself
- opening the port resets most Arduinos, so the port stays open for the whole session; the sign-off
  at the end brings dw-link back to the start speed, where the next session expects it
"""
import argparse
import logging
import time

from serial.tools import list_ports

from pyavrocd import jtag2
from pyavrocd.backend import DebugBackend, SwbpSupport, BackendError, BackendNotSupportedError, ProbeCandidate
from pyavrocd.errors import FatalError
from pyavrocd.jtag2backend import Jtag2Backend

DWLINK_IDENT : str = "dw-link"
MIN_MAJOR_VERSION : int = 7        # the first version that speaks the mkII protocol
BOOT_TIME : float = 4.0            # s: opening the port may reset the Arduino, its bootloader waits
SIGN_ON_TIMEOUT : int = 300        # ms for one sign-on attempt while waiting for it
WRITE_CHUNK : int = 256            # bytes per flash write; dw-link takes frames of up to 300 bytes

# vendor commands and parameters of dw-link (dw-link/src/mkii.cpp)
CMND_EXECUTE_INSTRUCTION : int = 0x70  # one-word opcode, LSB first, executed at the PC of the stopped target
CMND_SELFTEST : int = 0x71             # the self-test of the firmware; overwrites parts of the flash
PAR_TARGET_POWER : int = 0x70          # GET: bit 0 on, bit 1 switchable; SET: 0 off, 1 on, 2 power cycle
PAR_DWLINK_ERROR : int = 0x71          # GET: the number of the last error, 0 = none
PAR_DW_SPEED : int = 0x72              # SET: debugWIRE speed limit in 10 kbps; GET: limit, then speed in bps

# dw-link's error numbers (dw-link/src/config.h and docs/internal_errors.md)
DWLINK_ERRORS : dict[int, str] = {
    1 : "no reply over ISP; check the wiring",
    2 : "no reply over debugWIRE",
    8 : "capacitive load on the RESET line",
    9 : "target not powered, or RESET tied to GND",
    105 : "reset failed", 106 : "flash read at an address that is not a page start",
    107 : "flash read failed", 108 : "SRAM read failed", 109 : "flash write at a wrong page address",
    110 : "flash page erase failed", 112 : "flash page programming failed",
    113 : "flash page verification failed", 116 : "flash word read at an odd address",
    119 : "input buffer overflow", 122 : "timeout on the debugWIRE line",
    123 : "timeout while reading a register", 124 : "timeout while reading an I/O register",
    125 : "timeout while re-enabling the RWW section", 126 : "timeout while reading the EEPROM",
    127 : "bad interrupt" }


def discover() -> list[ProbeCandidate]:
    """
    Every USB serial port is a candidate (ports without a USB vendor ID, e.g., Bluetooth, are not);
    which one is dw-link only the sign-on can tell, and opening the port resets an Arduino. So the
    caller opens only an unambiguous one, or the one -u names.
    """
    return [ProbeCandidate(tool='dwlink', product=DWLINK_IDENT, address=port.device)
            for port in list_ports.comports() if port.vid is not None]


def connect(transport : jtag2.Jtag2SerialTransport, proto : jtag2.Jtag2Protocol, address : str, baud : int,
                logger : logging.Logger) -> jtag2.SignOn:
    """
    Sign on at the start speed. Opening the port may have reset the Arduino, whose bootloader
    then waits for a moment. A dw-link left at a higher speed by a server that ended without
    signing off answers there: most likely at this configuration's speed (baud), but a server
    started with another --dw-link-baud may have left it at any of them.
    """
    speeds = [jtag2.SERIAL_START_BAUD, baud] + \
      [b for b in sorted(jtag2.BAUD_CODES, reverse=True) if b not in (jtag2.SERIAL_START_BAUD, baud)]
    deadline = time.monotonic() + BOOT_TIME
    while True:
        for speed in speeds:
            transport.set_baudrate(speed)
            transport.flush()
            try:
                return proto.sign_on(SIGN_ON_TIMEOUT)
            except jtag2.Jtag2Error as e:
                logger.debug("No sign-on at %d bps: %s", speed, e)
        if time.monotonic() > deadline:
            raise FatalError("No dw-link (version {} or later) answers on {}".format(
                MIN_MAJOR_VERSION, address))

class DwlinkProtocol(jtag2.Jtag2Protocol):
    """The mkII protocol, with dw-link's error number added to the failures it explains"""

    def expect(self, response : bytes, wanted : int, what : str) -> bytes:
        try:
            return super().expect(response, wanted, what)
        except jtag2.Jtag2Error as e:
            if not response or response[0] not in (0xA0, 0xAC):  # RSP_FAILED, RSP_DEBUGWIRE_SYNC_FAILED
                raise
            number = self.error_number()
            if not number:
                raise
            raise jtag2.Jtag2Error("{} (dw-link error {}: {})".format(
                e, number, DWLINK_ERRORS.get(number, "see the dw-link documentation"))) from e

    def error_number(self) -> int:
        """dw-link's last error number; 0 if none or if it cannot be read"""
        response = self.command(bytes([jtag2.CMND_GET_PARAMETER, PAR_DWLINK_ERROR]))
        return response[1] if len(response) > 1 and response[0] == jtag2.RSP_PARAMETER else 0


#pylint: disable=too-many-ancestors
class DwlinkBackend(Jtag2Backend):
    """
    Backend for dw-link, version 7 or later
    """
    SWBP_SUPPORT = SwbpSupport.SERVER

    def __init__(self, candidate : ProbeCandidate, devicename : str, iface : str,
                     args : argparse.Namespace) -> None:
        if iface != 'debugwire':
            raise BackendNotSupportedError("dw-link can only debug debugWIRE targets")
        Jtag2Backend.__init__(self, candidate, devicename, iface, args)
        self.baud : int = args.baud
        self.transport : jtag2.Jtag2SerialTransport | None = None   # type: ignore[assignment]
        self.protocol : DwlinkProtocol | None = None                 # type: ignore[assignment]

    # ----- the port, opened once ------------------------------------------------------

    def _open(self) -> None:
        self.transport = jtag2.Jtag2SerialTransport(self.candidate.address)
        self.protocol = DwlinkProtocol(self.transport)

    def _connect(self) -> jtag2.SignOn:
        """See connect"""
        assert isinstance(self.transport, jtag2.Jtag2SerialTransport)
        return connect(self.transport, self._proto(), self.candidate.address, self.baud, self.logger)

    # ===== primitives for AvrSession =================================================

    def _sign_on(self, announce : bool = False) -> None:
        if self.protocol is None:
            self._open()
        if self.sign_on_info is None:
            info = self._connect()
            if info.ident != DWLINK_IDENT:
                raise FatalError("{} on {} is not dw-link".format(info.ident, self.candidate.address))
            if info.master_firmware[0] < MIN_MAJOR_VERSION:
                raise FatalError("dw-link {}.{} is too old: PyAvrOCD needs version {} or later".format(
                    *info.master_firmware, MIN_MAJOR_VERSION))
            if self.baud != jtag2.SERIAL_START_BAUD:
                self._proto().set_baud(self.baud)
            self.sign_on_info = info
        if announce:
            info = self.sign_on_info
            self.logger.info("Signed on to: %s %d.%d on %s, %s, SN: %s, %d bps", info.ident,
                                 info.master_firmware[0], info.master_firmware[1], self.candidate.address,
                                 "dw-probe shield" if info.master_hardware else "plain Arduino",
                                 info.serial, self.baud)

    def _sign_off(self) -> None:
        """
        Leave ISP and the emulator mode, and sign off: dw-link lets a stopped target run on and goes
        back to the start speed, and so does the host side; the next _sign_on connects anew. Every
        sign-off of the session is a real one, because a session can end without stop_debugging (when
        debugging was refused, e.g., for set lock bits), and with the capacitor on RESET that keeps the
        Arduino from resetting at the next port open, dw-link would stay at the higher speed, where
        avrdude (always 19200 with jtag2isp) does not find it (measured).
        """
        if self.protocol is None:
            return
        if self._isp is not None:
            self._isp.close()
            self._isp = None
        if self._mode_set:
            self.protocol.set_parameter(jtag2.PAR_EMULATOR_MODE, bytes([jtag2.EMULATOR_MODE_UNKNOWN]))
            self._mode_set = False
        if self.sign_on_info is not None and self.transport is not None:
            try:
                self.protocol.sign_off()
            except BackendError as e:
                self.logger.debug("Sign-off: %s", e)
            self.transport.set_baudrate(jtag2.SERIAL_START_BAUD)
            self.sign_on_info = None

    def _debugwire_active(self) -> bool:
        """The sync tells: dw-link answers RSP_DEBUGWIRE_SYNC_FAILED when it does not succeed"""
        try:
            self._proto().set_parameter(jtag2.PAR_EMULATOR_MODE, bytes([jtag2.EMULATOR_MODE_DEBUGWIRE]),
                                            jtag2.MODE_TIMEOUT)
        except jtag2.Jtag2Error as e:
            self.logger.debug("No debugWIRE sync: %s", e)
            return False
        self._mode_set = True
        return True

    def _enter_mode(self) -> None:
        if self._target_voltage() < 1.5:
            raise FatalError("Target is not powered")
        if not self._mode_set and not self._debugwire_active():
            raise FatalError("debugWIRE is not active")
        proto = self._proto()
        proto.set_device_context(jtag2.make_device_context(self.device_info))
        proto.set_parameter(jtag2.PAR_TIMERS_RUNNING, bytes([int(self.timers_run)]))
        self._mode_set = True

    def _debugwire_disable(self) -> None:
        """debugWIRE off until the next power cycle; ISP works right after it"""
        proto = self._proto()
        proto.debugwire_disable()
        proto.set_parameter(jtag2.PAR_EMULATOR_MODE, bytes([jtag2.EMULATOR_MODE_UNKNOWN]))
        self._mode_set = False

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

    # ===== DebugBackend ==================================================================

    def stop_debugging(self, skip : bool = False, leave : bool = False, graceful : bool = True) -> None:
        """
        As in the session, which ends with _sign_off; if it was left by an error before that, sign
        off here. The port stays open: the session may start again ('monitor debugwire enable'), and
        reopening may reset the Arduino.
        """
        try:
            Jtag2Backend.stop_debugging(self, skip, leave, graceful)
        finally:
            self._mode_set = False
            self._sign_off()

    def release(self) -> None:
        """
        At the end of the server, sign off in any case: a session whose start failed (e.g., debugWIRE
        not active and no 'monitor debugwire enable') ends without stop_debugging, and without the
        sign-off dw-link would stay at the higher speed (measured), where avrdude does not find it
        """
        self._sign_off()

    @staticmethod
    def reboot_probe(candidate : ProbeCandidate, args : argparse.Namespace, logger : logging.Logger) -> bool:
        """
        --reboot-debugger: sign off with PAR_SOFT_RESET set to a hard reset, after which dw-link restarts
        (watchdog reset; the target is switched off and on again, as at every start of dw-link), then
        sign on to it once more and off again. The port stays open, so that an Arduino that resets at
        every port open does not restart a second time. Returns False if dw-link does not come back.
        """
        logger.info("Rebooting debugger...")
        transport = jtag2.Jtag2SerialTransport(candidate.address)
        try:
            proto = DwlinkProtocol(transport)
            info = connect(transport, proto, candidate.address, args.baud, logger)
            if info.ident != DWLINK_IDENT or info.master_firmware[0] < MIN_MAJOR_VERSION:
                logger.critical("%s %d.%d on %s cannot be rebooted", info.ident, *info.master_firmware,
                                    candidate.address)
                return False
            proto.set_parameter(jtag2.PAR_SOFT_RESET, bytes([jtag2.SOFT_RESET_HARD]))
            proto.sign_off()
            transport.set_baudrate(jtag2.SERIAL_START_BAUD)
            time.sleep(0.1)   # the watchdog fires after 15 ms; what comes before is not an answer
            connect(transport, proto, candidate.address, jtag2.SERIAL_START_BAUD, logger)
            proto.sign_off()
        except (FatalError, BackendError) as e:
            logger.critical("Could not reboot dw-link: %s", e)
            return False
        finally:
            transport.close()
        logger.info("Reconnected to dw-link on %s", candidate.address)
        return True

    def execute_instruction(self, opcode : int) -> None:
        self._proto().ok(bytes([CMND_EXECUTE_INSTRUCTION]) + opcode.to_bytes(2, 'little'),
                             "Execute instruction 0x{:04X}".format(opcode))

    def program_flash_page(self, address : int, data : bytes) -> None:
        """dw-link erases only if needed, and handles the 4-page blocks itself"""
        self._proto().write_memory(jtag2.MEMTYPE_FLASH_PAGE, address, bytes(data))

    def write_flash_pages(self, address : int, data : bytes, prog_mode : bool) -> None:
        """
        The multi-page in one command (up to WRITE_CHUNK bytes): dw-link reads, merges and writes
        each block of page buffers once. Page by page, the 4-page parts would get their 128-byte block
        erased and written four times (measured on the ATtiny1634: 0.55 s instead of 0.22 s per block).
        The new contents replace planted BREAKs in this range; their original words are gone, and a
        breakpoint that is still wanted is planted again into the new contents before the target runs.
        """
        for planted in [a for a in self._swbp_planted if address <= a < address + len(data)]:
            del self._swbp_planted[planted]
        for offset in range(0, len(data), WRITE_CHUNK):
            self._proto().write_memory(jtag2.MEMTYPE_FLASH_PAGE, address + offset,
                                           bytes(data[offset:offset + WRITE_CHUNK]))

    # the server plants the software breakpoints (DebugBackend), not the probe (Jtag2Backend)
    software_breakpoint_set = DebugBackend.software_breakpoint_set
    software_breakpoint_clear = DebugBackend.software_breakpoint_clear
    software_breakpoint_clear_all = DebugBackend.software_breakpoint_clear_all

    def hardware_breakpoint_set(self, ix : int, address : int) -> None:
        """Only the comparator that RUN_TO_ADDR uses, i.e., hardware breakpoint 0"""
        raise BackendNotSupportedError("dw-link has no further hardware breakpoints")

    def hardware_breakpoint_clear(self, ix : int) -> None:
        """Nothing to clear, see hardware_breakpoint_set"""

    def _power(self) -> int:
        if self.sign_on_info is None:
            self._sign_on()
        return self._proto().get_parameter(PAR_TARGET_POWER)[0]

    def can_switch_target_power(self) -> bool:
        return bool(self._power() & 0x02)

    def set_target_power(self, on : bool) -> None:
        self._proto().set_parameter(PAR_TARGET_POWER, bytes([int(on)]))
        self._mode_set = False

    def can_power_cycle(self) -> bool:
        return self.can_switch_target_power()

    def power_cycle(self) -> bool:
        """dw-link switches off and on with the times the shield needs"""
        if not self.can_power_cycle():
            return False
        self._proto().set_parameter(PAR_TARGET_POWER, bytes([2]), jtag2.MODE_TIMEOUT)
        self._mode_set = False
        return True
