"""
DRAFT (v2): Abstract debugger backend for PyAvrOCD.

Everything above this layer (handler, breakexec, hardwarebp, memory, monitor,
server, livetests) talks to the hardware debugger only through this interface.
Concrete backends:
  - EdbgBackend       (today's XAvrDebugger: Atmel-ICE, PICkit4, SNAP, (m/n)EDBG, ...)
  - SerialUpdiBackend (planned, based on the avr-absurd approach)
  - DwLinkBackend     (planned, dw-link firmware reduced to debugWIRE primitives)
  - Pk5Backend        (planned, script-based MPLAB tools)

Design rules:
  1. No pyedbglib/pymcuprog protocol objects cross this interface
     (no Avr8Protocol constants, no .device.avr.protocol, no EdbgProtocol).
  2. Backends translate their tool-specific errors into the exceptions below.
  3. Tool features that not every debugger has are optional capabilities:
     the default implementation returns False / raises BackendNotSupportedError,
     and callers ask before they use them.
  4. Logic that only needs the primitives (e.g., masked SRAM access) lives in
     this base class, so that each backend gets it for free.

Addresses: flash addresses are byte addresses, SRAM addresses are data-space
addresses without the GDB offset bits (callers mask them out).
"""
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any
import logging

from pymcuprog.deviceinfo import deviceinfo  # pure device description, no tool dependency


# ---------------------------------------------------------------------------
# Exceptions (replace Jtagice3ResponseError, AvrIspProtocolError, PymcuprogError
# in the upper layers)
# ---------------------------------------------------------------------------

class BackendError(Exception):
    """Generic error reported by a debugger backend"""

class BackendNotSupportedError(BackendError):
    """Operation or capability not supported by this backend/tool"""

class InvalidAddressError(BackendError):
    """Access to an address the OCD refuses (was AVR8_FAILURE_INVALID_ADDRESS)"""

class IspConnectionError(BackendError):
    """ISP access (e.g., for setting DWEN/OCDEN) failed (was AvrIspProtocolError)"""


# ---------------------------------------------------------------------------
# The interface
# ---------------------------------------------------------------------------

#pylint: disable=too-many-public-methods
class DebugBackend(ABC):
    """
    Abstract debugger backend. One instance per debugging session and target.
    """

    def __init__(self, devicename: str, iface: str) -> None:
        self.logger: logging.Logger = logging.getLogger(__name__)
        self._devicename: str = devicename
        self._iface: str = iface
        # to be filled by the concrete backend's constructor:
        self.device_info: dict[str, Any] = {}
        self.memory_info: deviceinfo.DeviceMemoryInfo | None = None
        self.masked_registers: list[int] = []   # read-protected I/O registers
        self.ronly_registers: list[int] = []    # write-protected I/O registers

    # ----- static target/tool properties ------------------------------------

    def get_devicename(self) -> str:
        """MCU name, e.g., 'attiny85'"""
        return self._devicename

    def get_iface(self) -> str:
        """Debugging interface: 'debugwire', 'updi', or 'jtag'"""
        return self._iface

    @abstractmethod
    def get_architecture(self) -> str:
        """'avr8' or 'avr8x'"""

    @abstractmethod
    def get_hwbpnum(self) -> int:
        """Number of hardware breakpoints available to GDB"""

    @abstractmethod
    def get_sregaddr(self) -> int:
        """Data-space address of SREG"""

    @abstractmethod
    def get_iooffset(self) -> int:
        """Start of the I/O space in the data space (0x20 for classic AVRs, 0 for AVR8X)"""

    @abstractmethod
    def get_toolname(self) -> str:
        """Human readable name of the debug probe (for messages)"""

    # ----- session lifecycle -------------------------------------------------

    @abstractmethod
    def prepare_debugging(self, callback: Callable[[], bool] | None = None,
                          recognition: Callable[[], None] | None = None) -> None:
        """
        Bring the target into a state where an OCD session can be started
        (e.g., program DWEN via ISP and power-cycle for debugWIRE).
        'callback' asks the user (or the tool) to power-cycle,
        'recognition' reports that the target has been recognized.
        """

    @abstractmethod
    def start_debugging(self, flash_data: bytes | None = None, warmstart: bool = False) -> bool:
        """Start the OCD session. Returns True on success."""

    @abstractmethod
    def stop_debugging(self, skip: bool = False, leave: bool = False, graceful: bool = True) -> None:
        """
        End the OCD session. 'leave' means: leave the OCD enabled
        (e.g., do not clear DWEN), 'graceful' means: try to restore a sane state.
        """

    @abstractmethod
    def reactivate(self) -> None:
        """Re-establish OCD after settings have changed (e.g., running timers)"""

    @abstractmethod
    def switch_to_progmode(self) -> bool:
        """Switch from debug to programming mode (flash/fuse access). True on success."""

    @abstractmethod
    def switch_to_debmode(self) -> bool:
        """Switch back from programming to debug mode. True on success."""

    def cold_dw_disable(self) -> None:
        """
        Disable debugWIRE without an active session (used by 'main' on request).
        Only meaningful for debugWIRE backends.
        """
        raise BackendNotSupportedError("cold debugWIRE disable not supported")

    # ----- execution control -------------------------------------------------

    @abstractmethod
    def run(self) -> None:
        """Resume execution"""

    @abstractmethod
    def run_to(self, address: int) -> None:
        """Resume execution and stop at 'address' (byte address)"""

    @abstractmethod
    def step(self) -> None:
        """Execute exactly one instruction"""

    @abstractmethod
    def stop(self) -> None:
        """Halt execution"""

    @abstractmethod
    def reset(self) -> None:
        """Reset the target and halt it at the reset vector"""

    @abstractmethod
    def poll_event(self) -> int | None:
        """
        Non-blocking check whether the target has stopped since the last call.
        Returns the PC (byte address) if a stop has been detected, else None.
        Backends without an event mechanism poll the halt status here.
        """

    # ----- registers ---------------------------------------------------------

    @abstractmethod
    def register_file_read(self) -> bytearray:
        """Read r0..r31"""

    @abstractmethod
    def register_file_write(self, regs: bytes) -> None:
        """Write r0..r31"""

    @abstractmethod
    def register_read(self, addr: int, size: int) -> bytearray:
        """Read 'size' general purpose registers starting at register 'addr'"""

    @abstractmethod
    def register_write(self, addr: int, data: bytes) -> None:
        """Write general purpose registers starting at register 'addr'"""

    @abstractmethod
    def program_counter_read(self) -> int:
        """PC as word address"""

    @abstractmethod
    def program_counter_write(self, program_counter: int) -> None:
        """Set PC (word address)"""

    @abstractmethod
    def stack_pointer_read(self) -> bytearray:
        """SP, little endian, 2 bytes"""

    @abstractmethod
    def stack_pointer_write(self, data: bytes) -> None:
        """Set SP (little endian)"""

    @abstractmethod
    def status_register_read(self) -> bytearray:
        """SREG, 1 byte"""

    @abstractmethod
    def status_register_write(self, data: bytes) -> None:
        """Set SREG"""

    # ----- memories ----------------------------------------------------------

    @abstractmethod
    def sram_read(self, address: int, numbytes: int) -> bytearray:
        """
        Read data space (I/O + SRAM). Raises InvalidAddressError if the OCD
        refuses the access.
        """

    @abstractmethod
    def sram_write(self, address: int, data: bytes) -> None:
        """Write data space (I/O + SRAM)"""

    @abstractmethod
    def flash_read(self, address: int, numbytes: int, prog_mode: bool = False) -> bytearray:
        """Read flash (byte address)"""

    @abstractmethod
    def eeprom_read(self, address: int, numbytes: int, prog_mode: bool = False) -> bytes:
        """Read EEPROM"""

    @abstractmethod
    def eeprom_write(self, address: int, data: bytes, prog_mode: bool = False) -> None:
        """Write EEPROM"""

    def usig_read(self, address: int, numbytes: int, prog_mode: bool = False) -> bytes:
        """Read user signature (AVR8X only)"""
        raise BackendNotSupportedError("user signature not supported")

    def usig_write(self, address: int, data: bytes, prog_mode: bool = False) -> str | None:
        """Write user signature (AVR8X only)"""
        raise BackendNotSupportedError("user signature not supported")

    @abstractmethod
    def read_fuse(self, addr: int, size: int) -> bytearray:
        """Read fuse bytes"""

    @abstractmethod
    def write_fuse(self, addr: int, data: bytes) -> bytearray | None:
        """Write fuse bytes"""

    @abstractmethod
    def read_lock(self, addr: int, size: int) -> bytearray:
        """Read lock bits"""

    @abstractmethod
    def write_lock(self, addr: int, data: bytes) -> bytearray | None:
        """Write lock bits"""

    @abstractmethod
    def read_sig(self, addr: int, size: int) -> bytearray:
        """Read signature bytes"""

    # ----- flash programming (replaces dbg.device / dbg.device.avr access) ---

    @abstractmethod
    def erase_chip(self, prog_mode: bool) -> None:
        """Erase the whole chip (flash, and EEPROM unless EESAVE)"""

    @abstractmethod
    def erase_flash_page(self, address: int, prog_mode: bool) -> bool:
        """Erase one flash page if necessary. Returns True if erased."""

    @abstractmethod
    def write_flash_pages(self, address: int, data: bytes, prog_mode: bool) -> None:
        """
        Program one 'multi page' (as determined by memory.py) starting at 'address'.
        The backend decides how to split it (replaces write_memory_section + flashmemtype).
        """

    # ----- breakpoints -------------------------------------------------------

    @abstractmethod
    def hardware_breakpoint_set(self, ix: int, address: int) -> None:
        """Set hardware breakpoint number 'ix' (1-based) to byte address 'address'"""

    @abstractmethod
    def hardware_breakpoint_clear(self, ix: int) -> None:
        """Clear hardware breakpoint number 'ix'"""

    @abstractmethod
    def software_breakpoint_set(self, address: int) -> bool:
        """Insert BREAK at 'address'. True on success."""

    @abstractmethod
    def software_breakpoint_clear(self, address: int) -> None:
        """Remove BREAK at 'address'"""

    @abstractmethod
    def software_breakpoint_clear_all(self) -> None:
        """Remove all BREAKs"""

    # ----- optional tool capabilities ----------------------------------------

    def can_set_run_timers(self) -> bool:
        """Can timers be configured to run/freeze while the target is stopped?"""
        return False

    def set_run_timers(self, run: bool) -> None:
        """Let timers run (True) or freeze (False) while stopped"""
        raise BackendNotSupportedError("timer control not supported")

    def can_switch_target_power(self) -> bool:
        """Can the tool switch the target's supply?"""
        return False

    def set_target_power(self, on: bool) -> None:
        """Switch target supply on/off"""
        raise BackendNotSupportedError("target power control not supported")

    def power_cycle(self) -> bool:
        """
        Try to power-cycle the target automatically.
        Returns False if the tool cannot do it (then the user is asked).
        """
        if not self.can_switch_target_power():
            return False
        import time  # pylint: disable=import-outside-toplevel
        self.set_target_power(False)
        time.sleep(0.5)
        self.set_target_power(True)
        time.sleep(0.2)
        return True

    # ----- generic helpers built on the primitives ---------------------------

    def sram_masked_read(self, addr: int, size: int) -> bytearray:
        """
        Read data space, but return 0 for read-protected registers.
        (moved from XAvrDebugger unchanged)
        """
        raise NotImplementedError("to be moved from XAvrDebugger")

    def sram_masked_write(self, addr: int, data: bytes) -> None:
        """
        Write data space, but skip write-protected registers.
        (moved from XAvrDebugger unchanged)
        """
        raise NotImplementedError("to be moved from XAvrDebugger")
