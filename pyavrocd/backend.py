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
  5. Software breakpoints look the same to the upper layers on every backend:
     either the probe plants them and steps over them (SwbpSupport.PROBE), or this
     base class does it from primitives (SwbpSupport.SERVER): BREAKs are collected
     and written page by page right before the target runs, flash_read returns the
     original words, and step() injects the original instruction instead of
     restoring it, which would cost two erase/write cycles per hit. breakexec.py
     therefore does not need to know which kind of backend it talks to.
  6. Every transaction with the probe (a command with its complete response) runs
     inside termination.transaction(), so that SIGTERM/SIGINT cannot cut it short.
     guard_transactions() installs that for the backend's transport.

Addresses: flash addresses are byte addresses, SRAM addresses are data-space
addresses without the GDB offset bits (callers mask them out).
"""
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any
import argparse
import logging
import time

from pymcuprog.deviceinfo import deviceinfo  # pure device description, no tool dependency

BREAKCODE : int = 0x9598


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


class SwbpSupport(Enum):
    """Who takes care of software breakpoints"""
    PROBE = "probe"    # the probe plants BREAKs and steps over them (EDBG, probably mkII/Dragon)
    SERVER = "server"  # this base class does, from page programming and instruction injection
                       # (dw-link, mkI, serialUPDI, PICkit5)
    NONE = "none"      # hardware breakpoints only


# ---------------------------------------------------------------------------
# The interface
# ---------------------------------------------------------------------------

#pylint: disable=too-many-public-methods
class DebugBackend(ABC):
    """
    Abstract debugger backend. One instance per debugging session and target.
    """

    SWBP_SUPPORT: SwbpSupport = SwbpSupport.PROBE   # set by each backend

    def __init__(self, devicename: str, iface: str) -> None:
        self.logger: logging.Logger = logging.getLogger(__name__)
        self._devicename: str = devicename
        self._iface: str = iface
        # to be filled by the concrete backend's constructor:
        self.device_info: dict[str, Any] = {}
        self.memory_info: deviceinfo.DeviceMemoryInfo | None = None
        self.masked_registers: list[int] = []   # read-protected I/O registers
        self.ronly_registers: list[int] = []    # write-protected I/O registers
        # SwbpSupport.SERVER: BREAKs in flash (address -> original word), and the wanted ones
        self._swbp_planted: dict[int, int] = {}
        self._swbp_wanted: set[int] = set()

    @abstractmethod
    def guard_transactions(self) -> None:
        """
        Make sure every transaction with the probe runs inside termination.transaction()
        (design rule 6). Called once by the server before it installs its signal handlers.
        Abstract, so that no backend can forget it.
        """

    def is_set_up(self) -> bool:
        """
        Is the backend set up for its target, so that stop_debugging makes sense?
        Asked by the server when it shuts down.
        """
        return True

    def release(self) -> None:
        """
        Let go of the probe. Called once by the server when it ends, after stop_debugging if that
        was called at all, whatever the session did; e.g., a session whose start was refused or
        failed ends without stop_debugging. Nothing to do for most backends.
        """

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
    # run, run_to and step bring the software breakpoints into flash first; the
    # backends implement the bare operations _run, _run_to and _step.

    def run(self) -> None:
        """Resume execution"""
        self._sync_software_breakpoints()
        self._run()

    def run_to(self, address: int) -> None:
        """Resume execution and stop at 'address' (byte address)"""
        self._sync_software_breakpoints()
        self._run_to(address)

    def step(self, opcode: int | None = None) -> None: # pylint: disable=unused-argument # for subclasses
        """
        Execute exactly one instruction. 'opcode' is the instruction at the PC as the
        caller knows it (BREAKs filtered out), so that a backend that steps by injection
        does not have to read flash for every step.

        With SwbpSupport.SERVER, a BREAK at the PC is stepped over by injecting the
        original instruction, so the BREAK stays in flash. Two-word instructions at a
        BREAK never get here: breakexec simulates them.
        """
        self._sync_software_breakpoints()
        if self.SWBP_SUPPORT == SwbpSupport.SERVER:
            pc = self.program_counter_read() << 1
            if pc in self._swbp_planted:
                self.execute_instruction(self._swbp_planted[pc])
                return
        self._step()

    def step_is_interrupt_safe(self) -> bool:
        """
        Does step() never let an interrupt in? True for backends that step by injecting
        the instruction; breakexec then skips its own interrupt-safe stepping (clearing
        and restoring the I-bit around every step), which costs extra round trips.
        """
        return False

    @abstractmethod
    def _run(self) -> None:
        """Resume execution (bare)"""

    @abstractmethod
    def _run_to(self, address: int) -> None:
        """Resume execution and stop at 'address' (bare)"""

    @abstractmethod
    def _step(self) -> None:
        """Execute exactly one instruction from flash (bare)"""

    def execute_instruction(self, opcode: int) -> None:
        """
        SwbpSupport.SERVER only: execute the one-word instruction 'opcode' instead of the
        one at the PC (instruction injection). PC-changing instructions change the PC;
        otherwise the PC advances by one word.
        """
        raise BackendNotSupportedError("instruction injection not supported")

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

    def flash_read(self, address: int, numbytes: int, prog_mode: bool = False) -> bytearray:
        """Read flash (byte address); planted BREAKs read as the original words"""
        data = self._flash_read(address, numbytes, prog_mode)
        for bp, orig in self._swbp_planted.items():
            for i in (0, 1):
                if address <= bp + i < address + numbytes:
                    data[bp + i - address] = (orig >> (8*i)) & 0xFF
        return data

    @abstractmethod
    def _flash_read(self, address: int, numbytes: int, prog_mode: bool = False) -> bytearray:
        """Read flash as it is (bare)"""

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

    def program_flash_page(self, address: int, data: bytes) -> None:
        """
        SwbpSupport.SERVER only: erase and program the single flash page at 'address'
        (page aligned) while in debug mode
        """
        raise BackendNotSupportedError("page programming in debug mode not supported")

    # ----- breakpoints -------------------------------------------------------

    @abstractmethod
    def hardware_breakpoint_set(self, ix: int, address: int) -> bytes | None:
        """Set hardware breakpoint number 'ix' (1-based) to byte address 'address' (reply ignored)"""

    @abstractmethod
    def hardware_breakpoint_clear(self, ix: int) -> bytes | None:
        """Clear hardware breakpoint number 'ix' (reply ignored)"""

    # The three public methods below are the SwbpSupport.SERVER implementation.
    # SwbpSupport.PROBE backends override them with the probe's commands.

    def software_breakpoint_set(self, address: int) -> bool:
        """Insert BREAK at 'address' (takes effect before the target runs). True on success."""
        if self.SWBP_SUPPORT == SwbpSupport.NONE:
            return False
        self._swbp_wanted.add(address)
        return True

    def software_breakpoint_clear(self, address: int) -> None:
        """Remove BREAK at 'address' (takes effect before the target runs)"""
        self._swbp_wanted.discard(address)

    def software_breakpoint_clear_all(self) -> None:
        """
        Remove all BREAKs, at once. Called when the session ends and, through
        breakexec.cleanup_breakpoints, before every load (vFlashErase, X): flashing a
        program therefore never meets planted BREAKs, and the table cannot go stale.
        """
        self._swbp_wanted.clear()
        self._sync_software_breakpoints()

    def _sync_software_breakpoints(self) -> None:
        """
        SwbpSupport.SERVER: bring flash in line with the wanted BREAKs, programming each
        affected page once. Called right before the target runs or steps.
        """
        if self.SWBP_SUPPORT != SwbpSupport.SERVER:
            return
        planted = set(self._swbp_planted)
        changed = (self._swbp_wanted - planted) | (planted - self._swbp_wanted)
        if not changed:
            return
        assert self.memory_info is not None
        pagesize: int = self.memory_info.memory_info_by_name('flash')['page_size']
        for page in sorted({a - a % pagesize for a in changed}):
            data = self._flash_read(page, pagesize)
            for a in range(page, page + pagesize, 2):
                if a in self._swbp_wanted and a not in self._swbp_planted:
                    self._swbp_planted[a] = data[a - page] | (data[a - page + 1] << 8)
                    data[a - page:a - page + 2] = BREAKCODE.to_bytes(2, 'little')
                elif a in self._swbp_planted and a not in self._swbp_wanted:
                    data[a - page:a - page + 2] = self._swbp_planted.pop(a).to_bytes(2, 'little')
            self.logger.debug("Reprogramming flash page 0x%X for software breakpoints", page)
            self.program_flash_page(page, bytes(data))

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

    def can_power_cycle(self) -> bool:
        """
        Can the tool power-cycle the target by itself to activate debugWIRE? Not the same
        as can_switch_target_power: on EDBG tools only the mEDBG gets through it, the
        others end up in a state where the housekeeper does not respond.
        """
        return False

    def power_cycle(self) -> bool:
        """
        Try to power-cycle the target automatically.
        Returns False if the tool cannot do it (then the user is asked).
        """
        if not self.can_power_cycle():
            return False
        self.set_target_power(False)
        time.sleep(0.5)
        self.set_target_power(True)
        time.sleep(0.2)
        return True

    # ----- generic helpers built on the primitives ---------------------------

    def sram_masked_read(self, addr: int, size: int) -> bytearray:
        """
        Read a chunk from SRAM but leaving  out any masked registers. In theory,
        one could use the "Memory Read Masked" method of the AVR8 Generic protocol.
        However, there is no Python method implemented that does that for you.
        For this reason, we do it here step by step.

        In addition to that, the function fetches the values from the general
        registers if the address is below the iooffset, i.e., < 20 for JTAG and
        dw targets.
        (moved from XAvrDebugger unchanged)
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

    def sram_masked_write(self, addr: int, data: bytes) -> None:
        """
        Write a chunk to SRAM but leaving  out any read-only registers. If there is an
        attempt to write to a read-only register, spew out a warning message.

        If we write to SRAM below iooffset, then we will write to the registerfile
        (moved from XAvrDebugger unchanged)
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


# ---------------------------------------------------------------------------
# Tool registry: what -t accepts, how a tool is found, which backend serves it.
# Replaces the fixed tool list in main.py and the special route for dw-link.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ProbeCandidate:
    """A probe found on this machine"""
    tool: str       # registry name, e.g. 'atmelice'
    product: str    # what the probe calls itself
    address: str    # USB serial number or serial port


@dataclass(frozen=True)
class ToolSpec:
    """A kind of debug probe"""
    name: str                   # value of -t
    transport: str              # 'hid', 'usb' (bulk, through libusb) or 'serial'
    ifaces: tuple[str, ...]     # debugging interfaces the tool can drive
    discover: Callable[[], list[ProbeCandidate]]
    # (candidate, devicename, iface, args) -> connected backend
    connect: Callable[[ProbeCandidate, str, str, argparse.Namespace], DebugBackend]


TOOLS: dict[str, ToolSpec] = {}


def register_tool(spec: ToolSpec) -> None:
    """Called by each backend module for every tool it serves"""
    TOOLS[spec.name] = spec


def discover_probes(tool: str | None = None, address_suffix: str | None = None) -> list[ProbeCandidate]:
    """
    All attached probes of the given kind (all kinds if None), optionally only those whose
    serial number or port ends in 'address_suffix' (like -u today)
    """
    found: list[ProbeCandidate] = []
    for name in [tool] if tool else list(TOOLS):
        found += [c for c in TOOLS[name].discover()
                  if address_suffix is None or c.address.endswith(address_suffix)]
    return found
