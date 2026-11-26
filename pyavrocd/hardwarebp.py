"""
This module deals with the management of hardware breakpoints
"""
# args, logging
import logging

from pyavrocd.backend import DebugBackend
from pyavrocd.errors import FatalError

# A hardware breakpoint that compares a data address for a watchpoint; it is not free for code
RESERVED : int = -1

# GDB's watchpoint types (Z2, Z3, Z4), the name in the stop reply, and the data breakpoint mode
WATCH_KINDS : dict[int, tuple[str, int]] = {2 : ('watch', DebugBackend.DATA_WRITE),
                                            3 : ('rwatch', DebugBackend.DATA_READ),
                                            4 : ('awatch', DebugBackend.DATA_ACCESS)}


class HardwareBP():
    """
    This class manages the hardware breakpoints with some basic methods (including starting
    execution with the temporary breakpoint). All addresses are byte addresses into flash space.
    """

    def __init__(self, dbg : DebugBackend) -> None:
        self.dbg : DebugBackend = dbg
        self._numhwbp : int = dbg.get_hwbpnum()
        self._hwbplist : list[int | None] = [None]*self._numhwbp
        self._tempalloc : list[int] | None = None
        self.logger : logging.Logger = logging.getLogger('pyavrocd.hardwarebp')
        # watchpoints: (type, data address, length) -> the hardware breakpoints comparing for it
        self._data_slots : list[int] = [ix for ix in dbg.data_breakpoint_slots() if ix < self._numhwbp]
        self._watches : dict[tuple[int, int, int], list[int]] = {}


    def execute(self, cursor : int|None = None) -> None:
        """
        Start execution with HWBP 0 (if not None)
        """
        # The PC is read for the log only, and that is a round trip to the probe: the arguments
        # of a logging call are evaluated even when its level is disabled, so read it only then
        pc : int | None = None
        if self.logger.isEnabledFor(logging.DEBUG):
            pc = self.dbg.program_counter_read() << 1
        if cursor is not None: # if HWBP has been reserved for temporary work
            self.logger.debug("Run from 0x%X to cursor 0x%X", pc, cursor)
            self.dbg.run_to(cursor)
        elif self._hwbplist[0] is not None:
            self.logger.debug("Run from 0x%X to HWBP0 0x%X", pc, self._hwbplist[0])
            self.dbg.run_to(self._hwbplist[0])
        else:
            self.logger.debug("Run from 0x%X", pc)
            self.dbg.run()

    def clear_all(self) -> None:
        """
        Clear all hardware breakpoints
        """
        self._hwbplist = [None]*self._numhwbp
        self._watches = {}
        for ix in range(self._numhwbp-1):
            self.dbg.hardware_breakpoint_clear(ix+1)
        self.logger.debug("All hardware breakpoints cleared")

    def clear(self, addr : int) -> bool:
        """
        Clear breakpoint at a given address. If successful return True, otherwise False.
        """
        if addr in self._hwbplist:
            self._free(self._hwbplist.index(addr))
            return True
        self.logger.error("Tried to clear hardware breakpoint at 0x%X, but there is none", addr)
        return False

    def _free(self, ix : int) -> bool:
        """
        Free a BP at index ix. If unsuccessful, return False, otherwise True.
        """
        if 0 <= ix < self._numhwbp and self._hwbplist[ix] is not None:
            self.logger.debug("HWBP %d at addr 0x%X freed", ix, self._hwbplist[ix])
            self._hwbplist[ix] = None
            if ix > 0:
                self.dbg.hardware_breakpoint_clear(ix)
            return True
        self.logger.error("Tried to release unallocated hardware breakpoint %d", ix)
        return False

    def available(self) -> int:
        """
        Returns the number of hardware breakpoints that are available
        """
        return self._numhwbp - len([addr for addr in self._hwbplist if addr is not None])

    def usable(self) -> int:
        """
        The number of hardware breakpoints that can be used for code, i.e., not reserved for watchpoints
        """
        return self._numhwbp - self._hwbplist.count(RESERVED)

    def set(self, addr : int) -> int | None:
        """
        Allocates the next free hardware breakpoint (counting up) and returns the index
        -- provided there is a free hardware breakpoint. Otherwise, None is returned.
        """
        self.logger.debug("Trying to allocate HWBP for addr 0x%X", addr)
        if addr % 2 != 0:
            self.logger.error("Breakpoint at odd address: 0x%X", addr)
            return None

        for ix in range(self._numhwbp):
            if self._hwbplist[ix] is None:
                self._hwbplist[ix] = addr
                if ix > 0:
                    self.dbg.hardware_breakpoint_clear(ix)
                    self.dbg.hardware_breakpoint_set(ix, addr)
                self.logger.debug("Successfully allocated HWBP %d", ix)
                return ix
        self.logger.debug("Could not allocate a HWBP")
        return None

    def set_temp(self,templist : list[int]) -> list[int]:
        """
        Try to set all HWBPs for all addresses in templist. Raise error if impossible or
        returns a list of addresses that needs to become software breakpoints. This function
        is used to support range-stepping. In self._tempalloc we remember, which HWBPs (index!)
        have been allocated temporarily.
        """
        self.logger.debug("Trying to allocate %d temp HWBPs", len(templist))
        reassignlist : list[int] = []
        if len(templist) > self.usable():
            raise FatalError("Not enough HWBPs for range-stepping. Internal confusion.")
        self._tempalloc = []
        allocated : list[int] = [addr for addr in self._hwbplist if addr is not None and addr != RESERVED]
        nextix : int | None
        for el in templist:
            nextix = self.set(el)
            if nextix is not None:
                self._tempalloc.append(nextix)
            else:
                trytoremove = allocated.pop()
                reassignlist.append(trytoremove)
                self.clear(trytoremove)
                nextix = self.set(el)
                if nextix is not None:
                    self._tempalloc.append(nextix)
                else:
                    raise FatalError("Internal confusion in hardware breakpoint management")
        self.logger.debug("Allocated %d temp HWBPs", len(self._tempalloc))
        return reassignlist

    def clear_temp(self) -> None:
        """
        Clears the temporary allocated hardware breakpoints.
        """
        self.logger.debug("Trying to free temp allocation")
        if self._tempalloc is None:
            return
        toclear = len(self._tempalloc)
        for el in self._tempalloc:
            if el >= 0:
                self._free(el)
        self._tempalloc = None
        self.logger.debug("HWBP temp allocation cleared: %d HWBPs cleared", toclear)

    def temp_allocated(self) -> int | None:
        """
        Returns number of HWBPs temporarily allocated to range-stepping
        """
        if self._tempalloc is None:
            return None
        return len(self._tempalloc)

    def temp_allocated_num(self) -> int:
        """
        Always returns a number
        """
        temp = self.temp_allocated()
        if temp is None:
            return 0
        return temp

    def borrow_hwbp0(self) -> int | None:
        """
        Borrow the temporary breakpoint for just one single step (over a sleep instruction).
        If it is used as a temporary HWBP in range-stepping, simply return None. Same, if we can
        reallocate HWBP0 to another HW breakpoint or if it is free from the beginning. Otherwise,
        return address and let the caller decide what to do with it.
        """
        self.logger.debug("Freeing HWBP0 so that in can be borrowed")
        if self._hwbplist[0] is None or (self._tempalloc is not None and 0 in self._tempalloc):
            self.logger.debug("Already free")
            return None
        if self.available() > 0:
            self.set(self._hwbplist[0])
            self._free(0)
            self.logger.debug("HWBP0 moved to other HWBP")
            return None
        reassign = self._hwbplist[0]
        self._free(0)
        self.logger.debug("BP 0x%X needs to be reassigned to SWBP", reassign)
        return reassign

    def hwbp0_available(self) -> bool:
        """
        Tells us whether HWBP0 is available
        """
        return self._hwbplist[0] is None

    # ===== watchpoints ==========================================================

    def set_watch(self, kind : int, address : int, length : int) -> tuple[bool, list[int]]:
        """
        Set a watchpoint of GDB type 'kind' (2 write, 3 read, 4 access) on 'length' bytes at data
        address 'address'. One data breakpoint per byte, so 1 or 2 bytes, at any alignment. Returns
        whether it worked, and the code breakpoints that had to give up their hardware breakpoint
        (they have to be allocated anew). A range-stepping scaffold is given up as well.
        """
        if kind not in WATCH_KINDS or length < 1 or (kind, address, length) in self._watches:
            return False, []
        free = [ix for ix in self._data_slots if self._hwbplist[ix] != RESERVED]
        if length > len(free):
            self.logger.debug("Watchpoint at 0x%X (%d bytes) needs %d data breakpoints, %d free",
                              address, length, length, len(free))
            return False, []
        slots = free[:length]
        if self._tempalloc is not None and set(slots) & set(self._tempalloc):
            self.clear_temp()
        displaced : list[int] = []
        for ix in slots:
            if self._hwbplist[ix] is not None:
                displaced.append(self._hwbplist[ix]) # type: ignore[arg-type]
                self._free(ix)
            self._hwbplist[ix] = RESERVED
        for offset, ix in enumerate(slots):
            self.dbg.hardware_breakpoint_clear(ix)
            self.dbg.data_breakpoint_set(ix, address + offset, WATCH_KINDS[kind][1])
        self._watches[(kind, address, length)] = slots
        self.logger.debug("Watchpoint %s at 0x%X (%d bytes) on HWBP %s",
                          WATCH_KINDS[kind][0], address, length, slots)
        return True, displaced

    def clear_watch(self, kind : int, address : int, length : int) -> bool:
        """Remove a watchpoint; False if there is none like this"""
        slots = self._watches.pop((kind, address, length), None)
        if slots is None:
            return False
        for ix in slots:
            self.dbg.hardware_breakpoint_clear(ix)
            self._hwbplist[ix] = None
        self.logger.debug("Watchpoint at 0x%X removed", address)
        return True

    def watch_hit(self, fired : list[int]) -> tuple[str, int] | None:
        """
        The watchpoint behind the data breakpoints that fired, as the name for the stop reply
        ('watch', 'rwatch', 'awatch') and its data address; None if none of them is a watchpoint
        """
        for (kind, address, _), slots in self._watches.items():
            if set(slots) & set(fired):
                return WATCH_KINDS[kind][0], address
        return None

    def watch_for_access(self, address : int, write : bool) -> tuple[str, int] | None:
        """
        The watchpoint that an access to data address 'address' triggers (a write: watch and
        awatch, a read: rwatch and awatch), as for watch_hit; for accesses the server simulates
        """
        for (kind, start, length) in self._watches:
            if start <= address < start + length and (kind == 4 or (kind == 2) == write):
                return WATCH_KINDS[kind][0], start
        return None

    def has_watches(self) -> bool:
        """Whether any watchpoint is set"""
        return bool(self._watches)
