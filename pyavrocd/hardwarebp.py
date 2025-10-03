"""
This module deals with the management of hardware breakpoints
"""
# args, logging
import logging

class HardwareBP():
    """
    This class manages the hardware breakpoints with some basic methods (including starting
    execution with the temporary breakpoint).
    """

    def __init__(self, dbg):
        self.dbg = dbg
        self._numhwbp = dbg.get_hwbpnum()
        self._hwbplist = [None]*self._numhwbp
        self._tempalloc = None
        self.logger = logging.getLogger('pyavrocd.hardwarebp')


    def execute(self):
        """
        Start execution with HWBP 0 (if not None)
        """
        if self._hwbplist[0] is not None:
            self.logger.debug("Run to cursor 0x%X", self._hwbplist[0])
            self.dbg.run_to(self._hwbplist[0])
        else:
            self.logger.debug("Run")
            self.dbg.run()

    def clear_all(self):
        """
        Clear all hardware breakpoints
        """
        self._hwbplist = [None]*self._numhwbp
        for ix in range(self._numhwbp-1):
            self.dbg.hardware_breakpoint_clear(ix+1)
        self.logger.debug("All hardware breakpoints cleared")

    def clear(self, addr):
        """
        Clear breakpoint at a given address. If successful return True, otherwise False.
        """
        if addr in self._hwbplist:
            self._free(self._hwbplist.index(addr))
            return True
        self.logger.error("Tried to clear hardware breakpoint at 0x%X, but there is none", addr)
        return False

    def _free(self, ix):
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

    def available(self):
        """
        Returns the number of hardware breakpoints that are available
        """
        return self._numhwbp - len([addr for addr in self._hwbplist if addr is not None])

    def set(self, addr):
        """
        Allocates the next free hardware breakpoint (counting up) and returns the index
        -- provided there is a free hardware breakpoint. Otherwise, None is returned.
        """
        self.logger.debug("Trying to allocate HWBP for addr 0x%X", addr)
        for ix in range(self._numhwbp):
            if self._hwbplist[ix] is None:
                self._hwbplist[ix] = addr
                if ix > 0:
                    self.dbg.hardware_breakpoint_set(ix, addr)
                self.logger.debug("Successfully allocated HWBP %d", ix)
                return ix
        self.logger.debug("Could not allocate a HWBP")
        return None

    def set_temp(self,templist):
        """
        Try to set all HWBPs for all addresses in templist. Returns None if impossible or
        returns a list of addresses that needs to become software breakpoints. This function
        is used to support range-stepping. In self._tempalloc we remember, which HWBPs
        have been allocated temporarily.
        """
        self.logger.debug("Trying to allocate %d temp HWBPs", len(templist))
        reassignlist = []
        if len(templist) > self._numhwbp:
            return None
        self._tempalloc = []
        allocated = [addr for addr in self._hwbplist if addr is not None]
        for el in templist:
            nextix = self.set(el)
            if nextix is not None:
                self._tempalloc.append(nextix)
            else:
                trytoremove = allocated.pop()
                reassignlist.append(trytoremove)
                self.clear(trytoremove)
                self._tempalloc.append(self.set(el))
        self.logger.debug("Allocated %d temp HWBPs", len(self._tempalloc))
        return reassignlist

    def clear_temp(self):
        """
        Clears the temporary allocated hardware breakpoints.
        """
        if self._tempalloc is None:
            return
        toclear = len(self._tempalloc)
        for el in self._tempalloc:
            if el >= 0:
                self._free(el)
        self._tempalloc = None
        self.logger.debug("HWBP temp allocation cleared: %d HWBPs cleared", toclear)

    def temp_allocated(self):
        """
        Returns number of HWBPs temporarily allocated to range-stepping
        """
        if self._tempalloc is None:
            return 0
        return len(self._tempalloc)

