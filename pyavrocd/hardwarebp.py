"""
This module deals with the management of hardware breakpoints
"""
# args, logging
import logging

from pyavrocd.backend import DebugBackend
from pyavrocd.errors import FatalError


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


    def execute(self, cursor : int|None = None) -> None:
        """
        Start execution with HWBP 0 (if not None)
        """
        if cursor is not None: # if HWBP has been reserved for temporary work
            self.logger.debug("Run from 0x%X to cursor 0x%X", self.dbg.program_counter_read()<<1,
                                  cursor)
            self.dbg.run_to(cursor)
        elif self._hwbplist[0] is not None:
            self.logger.debug("Run from 0x%X to HWBP0 0x%X", self.dbg.program_counter_read()<<1,
                                  self._hwbplist[0])
            self.dbg.run_to(self._hwbplist[0])
        else:
            self.logger.debug("Run from 0x%X",  self.dbg.program_counter_read()<<1)
            self.dbg.run()

    def clear_all(self) -> None:
        """
        Clear all hardware breakpoints
        """
        self._hwbplist = [None]*self._numhwbp
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
        if len(templist) > self._numhwbp:
            raise FatalError("Not enough HWBPs for range-stepping. Internal confusion.")
        self._tempalloc = []
        allocated : list[int] = [addr for addr in self._hwbplist if addr is not None]
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
