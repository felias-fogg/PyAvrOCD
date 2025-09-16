"""
This module deals with breakpoints and execution.
"""

# args, logging
from logging import getLogger

# special opcodes
BREAKCODE = 0x9598
SLEEPCODE = 0x9588

# signal codes
NOSIG   = 0     # no signal
SIGHUP  = 1     # no connection
SIGINT  = 2     # Interrupt  - user interrupted the program (UART ISR)
SIGILL  = 4     # Illegal instruction
SIGTRAP = 5     # Trace trap  - stopped on a breakpoint
SIGABRT = 6     # Abort because of a fatal error or no breakpoint available
SIGBUS = 10     # Segmentation violation means in our case stack overflow

class BreakAndExec():
    """
    This class manages breakpoints, supports flashwear minimizing execution, and
    makes interrupt-safe single stepping possible.
    """

    SWBP = 1
    HWBP = -1
    UNALLOCATED = 0

    def __init__(self, hwbpnum, mon, dbg, read_flash_word):
        self.mon = mon
        self.dbg = dbg
        self.logger = getLogger('pyavrocd.breakexec')
        self._hwbpnum = hwbpnum # This number includes the implicit HWBP used by run_to
        self._hwbp = HardwareBP(hwbpnum, self.logger, dbg)
        self._read_flash_word = read_flash_word
        self._bp = {}
        self._bpactive = 0
        self._bstamp = 0
        # more than 128 kB:
        self._bigmem = self.dbg.memory_info.memory_info_by_name('flash')['size'] > 128*1024
        self._range_start = 0
        self._range_end = 0
        self._range_word = []
        self._range_branch = []
        self._range_exit = set()
        self._last_single_step_start = 0

    def clear_last_single_step_start():
        self._last_single_step_start = 0

    def maxbpnum(self):
        """
        Returns maximum number of explicit breakpoints
        """
        if mon.is_onlyhwbps():
            return self._hwbpnum - int(self.mon.is_safe())
        return 1024

    def _read_filtered_flash_word(self, address):
        """
        Instead of reading directly from flash memory, we filter out break points.
        """
        if address in self._bp:
            return self._bp[address]['opcode']
        return self._read_flash_word(address)

    def insert_breakpoint(self, address):
        """
        Generate a new breakpoint at given address, do not allocate flash or hwbp yet
        This method will be called before GDB starts executing or single-stepping.
        """
        if address % 2 != 0:
            self.logger.error("Breakpoint at odd address: 0x%X", address)
            return
        if self.mon.is_old_exec():
            self.dbg.software_breakpoint_set(address)
            return
        if address in self._bp: # bp already set, needs to be activated
            self.logger.debug("Already existing BP at 0x%X will be re-activated",address)
            if not self._bp[address]['active']:
                self._bp[address]['active'] = True
                self._bpactive += 1
                self.logger.debug("Set BP at 0x%X to active", address)
            else:
                # if already active, ignore
                self.logger.debug("There is already an active BP at 0x%X", address)
            return
        self.logger.debug("New BP at 0x%X", address)
        opcode = self._read_flash_word(address)
        secondword = self._read_flash_word(address+2)
        self._bstamp += 1
        self._bp[address] =  {'active': True, 'allocated': UNALLOCATED,
                                  'opcode': opcode,
                                  'secondword' : secondword, 'timestamp' : self._bstamp }
        self.logger.debug("New BP at 0x%X: %s", address,  self._bp[address])
        self._bpactive += 1
        self.logger.debug("Now %d active BPs", self._bpactive)

    def remove_breakpoint(self, address):
        """
        Will mark a breakpoint as non-active, but it will stay in flash memory or marked as a hwbp.
        This method is called immediately after execution is stopped.
        """
        if address % 2 != 0:
            self.logger.error("Breakpoint at odd address: 0x%X", address)
            return
        if self.mon.is_old_exec():
            self.dbg.software_breakpoint_clear(address)
            return
        if not (address in self._bp) or not self._bp[address]['active']:
            self.logger.debug("BP at 0x%X was removed before", address)
            return # was already removed before
        self._bp[address]['active'] = False
        self._bpactive -= 1
        self.logger.debug("BP at 0x%X is now inactive", address)
        self.logger.debug("Only %d BPs are now active", self._bpactive)

    def update_breakpoints(self, protected_bp, release_temp=True):
        """
        This is called directly before execution is started. It will remove
        inactive breakpoints different from protected_bp, it will assign the hardware
        breakpoints to the most recently added breakpoints, and request to set active
        breakpoints into flash, if they not there already. The argument protected_bp
        is set by single and range-stepping, when we start at a place where there is a
        software breakpoint set. In this case, we do a single-step and then wait for
        GDB to re-activate the BP.
        The method will return False when at least one BP cannot be activated due
        to resource restrictions (e.g., not enough HWBPs).
        """
        self.logger.debug("Updating breakpoints before execution")
        # release temporarily allocated hardware breakpoints
        if release_temp:
            self._hwbp.clear_temp()
        # remove inactive BPs and de-allocate BPs that are now forbidden
        self.remove_inactive_and_deallocate_forbidden_bps(protected_bp):
        # check if there are enough software and hardware breakpoints to allocate
        if len(self._bp) > self.maxbpnum(): # too many BPs requested
            if self.mon.is_onlyhwbps() and len(self._bp) - 1 == self.maxbpnum() and \
              self._last_single_step_start in self._bp and \
              not self._bp[self._last_single_step_start]['allocated']:
              # This is critical since we might just be asked to re-assert a HWBP after a single-step,
              # but we do not have enough HWBPs. Issue warning and deallocate BP. This implies that
              # we can complete the step-over cleanly (but might miss a breakpoint in a recursice call)
              self.logger.error("Cannot allocate hardware breakpoint for start location.")
              self.logger.error("Will continue to execute without it (missing recursive calls)")
              self.remove_breakpoint(self._last_single_step_start)
            else:
              return False
        # determine most recent HWBP, probably a temporary one!
        most_recent = max(self._bp, key=lambda key: self._bp[key]['timestamp'])
        # all remaining BPs are active or protected
        # assign HWBP0 to the most recently introduced BP (if we are not range-stepping)
        # and take into account the possibility that hardware breakpoints are not allowed
        if not self._bp[most_recent]['allocated'] and not self._hwbp.allocated_temp() \
            and not self.mon.is_onlyswbp():
            reassign = self._hwbp.unallocate_hwbp0()
            self._hwbp.set(most_recent)
            self._bp[most_recent]['allocated'] = HWBP
            if reassign:
                self._bp[reassign]['allocated'] = UNALLOCATED
        # now assign the remaining BPs
        for a in self._bp:
            if not self._bp[a]['allocated']:
                if not self.mon.is_onlyswbps() and self._hwbp.set(a):
                    self._bp[a]['allocated'] = HWBP
                else:
                    self.logger.debug("BP at 0x%X will now be set as a SW BP", a)
                    self.dbg.software_breakpoint_set(a)
                    self._bp[a]['allocated'] = SWBP
        return True

    def remove_inactive_and_deallocate_forbidden_bps(self, protected_bp):
        """
        Remove all inactive BPs and deallocate BPs that are forbidden
        (after changing BP preference). A protected SW BP is not deleted!
        These are BPs at the current PC that have been set before and
        will now be overstepped in a single-step action.
        """
        self.logger.debug("Deallocate forbidden BPs and remove inactive ones")
        for a in self._bp:
            if self.mon.is_onlyswbps() and self._bp[a]['allocated'] == HWBP: # only SWBPs allowed
                self.logger.debug("Removing HWBP at 0x%X  because only SWBPs allowed.", a)
                self._bp[a]['allocated'] = UNALLOCATED
                self._hwbp.clear(a)
            if self.mon.is_onlyhwbps() and self._bp[a]['allocated'] == SWBP: # only HWBPs allowed
                self.logger.debug("Removing SWBP at 0x%X  because only HWBPs allowed", a)
                self._bp[a]['allocated'] = UNALLOCATED
                self.dbg.software_breakpoint_clear(a)
            # check for protected BP
            if a == protected_bp and self._bp[a]['allocated'] == SWBP:
                self.logger.debug("BP at 0x%X is protected", a)
                continue
            # delete BP
            if not self._bp[a]['active']: # delete inactive BP
                self.logger.debug("BP at 0x%X is not active anymore", a)
                if self._bp[a]['allocated']  == SWBP:
                    self.logger.debug("Removed as a SWBP")
                    self.dbg.software_breakpoint_clear(a)
                if self._bp[a]['allocated'] == HWBP:
                    self.logger.debug("Removed as a HWBP")
                    self._hwbp.clear(a)
                self.logger.debug("BP at 0x%X will now be deleted", a)
                del self._bp[a]

    def cleanup_breakpoints(self):
        """
        Remove all breakpoints from flash and clear hardware breakpoints
        """
        self.logger.debug("Deleting all breakpoints")
        self._hwbp.clear_all()
        self.dbg.software_breakpoint_clear_all()
        self._bp = {}
        self._bpactive = 0

    def resume_execution(self, addr):
        """
        Start execution at given addr (byte addr). If none given, use the actual PC.
        Update breakpoints. Return SIGABRT if not enough break points.
        """
        self._range_start = None
        if not self.update_breakpoints(None):
            return SIGABRT
        self.clear_last_single_step_start()
        if addr:
            self.dbg.program_counter_write(addr>>1)
        else:
            addr = self.dbg.program_counter_read() << 1
        opcode = self._read_filtered_flash_word(addr)
        if opcode == BREAKCODE: # this should not happen at all
            self.logger.debug("Stopping execution in 'continue' because of BREAK instruction")
            return SIGILL
        if opcode == SLEEPCODE: # ignore sleep
            self.logger.debug("Ignoring sleep in 'single-step'")
            addr += 2
            self.dbg.program_counter_write(addr>>1)
        if self.mon.is_old_exec():
            self.dbg.run()
            return None
        self._hwbp.execute()
        return None

    def single_step(self, addr, fresh=True):
        """
        Perform a single step. If at the current location, there is a software breakpoint,
        we simulate a two-word instruction or ask the hardware debugger to do a single step
        if it is a one-word instruction. The simulation saves two flash reprogramming operations.
        Otherwise, if mon._safe is true, we will make every effort to not end up in the
        interrupt vector table. For all straight-line instructions, we will use the hardware
        breakpoint to break after one step. If an interrupt occurs, we may break in the ISR,
        if there is a breakpoint, or we will not notice it at all. For all remaining instruction
        (except those branching on the I-bit), we clear the I-bit before and set it
        afterwards (if necessary). For those branching on the I-Bit, we will evaluate and
        then set the hardware BP.
        """
        if fresh:
            self._range_start = None
        if addr:
            self.dbg.program_counter_write(addr>>1)
        else:
            addr = self.dbg.program_counter_read() << 1
        self.logger.debug("One single step at 0x%X", addr)
        opcode = self._read_filtered_flash_word(addr)
        if opcode == SLEEPCODE: # ignore sleep
            self.logger.debug("Ignoring sleep in 'single-step'")
            addr += 2
            self.dbg.program_counter_write(addr>>1)
            return SIGTRAP
        if self.mon.is_old_exec():
            self.logger.debug("Single step in old execution mode")
            self.dbg.step()
            return SIGTRAP
        if opcode == BREAKCODE: # this should not happen!
            self.logger.error("Stopping execution in 'single-step' because of BREAK instruction")
            return SIGILL
        if not self.update_breakpoints(addr):
            self.logger.debug("Not enough free HW BPs: SIGABRT")
            return SIGABRT
        self._last_single_step_start = addr
        # If there is a SWBP at the place where we want to step,
        # if a two-word instruction, simulate the step;
        # otherwise use a conventional single-step
        if addr in self._bp and self._bp[addr]['allocated']:
            if self.two_word_instr(self._bp[addr]['opcode']):
            # if there is a two word instruction, simulate
                self.logger.debug("Two-word instruction at SWBP: simulate")
                addr = self.sim_two_word_instr(self._bp[addr]['opcode'],
                                                self._bp[addr]['secondword'], addr)
                self.logger.debug("New PC(byte addr)=0x%X, return SIGTRAP", addr)
                self.dbg.program_counter_write(addr>>1)
                return SIGTRAP
        # if stepping is unsafe, just use the AVR stepper
        if not self.mon.is_safe():
            self.logger.debug("Unsafe Single-stepping: use AVR stepper, return SIGTRAP")
            self.dbg.step()
            return SIGTRAP
        # now we have to do the dance using the HWBP or masking the I-bit
        opcode = self._read_filtered_flash_word(addr)
        self.logger.debug("Interrupt-safe stepping begins here")
        destination = None
        # compute destination for straight-line instructions and branches on I-Bit
        if self.store_instr(opcode):
            destination = addr + 2 + 2*int(self.two_word_instr(opcode))
            self.logger.debug("This is a store instructions. Destination=0x%X", destination)
        if self.branch_on_ibit(opcode):
            ibit = bool(self.dbg.status_register_read()[0] & 0x80)
            destination = self.compute_destination_of_ibranch(opcode, ibit, addr)
            self.logger.debug("Branching on I-Bit. Destination=0x%X", destination)
        if destination is not None: # we need to single-step using HWBP 0
            if not self._hwbp.is_temp_allocated(): # if we are range-stepping, we can use HWBP 0
                reassign = self._hwbp.unallocate_hwbp0()
                if reassign:
                    if self.mon.is_onlyhwbps():
                        # This should not happen
                        self.logger.error("Additional HWBP needed in safe single-stepping")
                        return SIGABRT
                    self.logger.debug("Stealing HWBP 0 from BP at 0x%X", reassign)
                    self._bp[reassign]['allocated'] = SWBP
                    self.dbg.software_breakpoint_set(reassign)
            self.logger.debug("Run to cursor... at 0x%X", destination)
            self.dbg.run_to(destination)
            return None
        # for the remaining branch and load instructions,
        # clear I-bit before and set it afterwards (if it was on before)
        self.logger.debug("Remaining branch instructions")
        sreg = self.dbg.status_register_read()[0]
        self.logger.debug("sreg=0x%X", sreg)
        ibit = sreg & 0x80
        if ibit:
            sreg &= 0x7F # clear I-Bit
            self.logger.debug("New sreg=0x%X",sreg)
            self.dbg.status_register_write(bytearray([sreg]))
        self.logger.debug("Now make a step...")
        self.dbg.step()
        if ibit:
            sreg = self.dbg.status_register_read()[0]
            self.logger.debug("New sreg=0x%X", sreg)
            sreg |= ibit
            self.logger.debug("Restored sreg=0x%X", sreg)
            self.dbg.status_register_write(bytearray([sreg]))
        self.logger.debug("Returning with SIGTRAP")
        return SIGTRAP


    def range_step(self, start, end):
        """
        range stepping: Break only if we leave the interval start-end. If we can cover all
        exit points, we watch them. If it is an inside point (e.g., RET), we single-step on it.
        In order to do so, we allocate temporarily some hardware breakpoints. These get released
        when we do an ordinary 'continue' or 'step'.
        Otherwise, we break at each branching point and single-step this branching instruction.
        Note that we need to return after the first step to allow GDB to set a breakpoint at the
        location where we started.
        """
        self.logger.debug("Range stepping from 0x%X to 0x%X", start, end)
        if not self.mon.is_range() or self.mon.is_old_exec():
            self.logger.warning("Range stepping forbidden")
            return self.single_step(None)
        if start%2 != 0 or end%2 != 0:
            self.logger.error("Range addresses in range stepping are ill-formed")
            return self.single_step(None)
        if start == end:
            self.logger.debug("Empty range: Simply single step")
            return self.single_step(None)
        new_range = self.build_range(start, end)
        if not self.update_breakpoints(addr, release_temp=new_range):
            return SIGABRT
        addr = self.dbg.program_counter_read() << 1
        if addr < start or addr >= end: # starting outside of range, should not happen!
            self.logger.error("PC 0x%X outside of range boundary", addr)
            return self.single_step(None)
        if (addr in self._range_exit or # starting at possible exit point inside range
            self._read_filtered_flash_word(addr) in { BREAKCODE, SLEEPCODE } or # special opcode
            addr in self._bp or # a SWBP at this point
            new_range): # or it is a new range
            return self.single_step(None, fresh=False) # reduce to one step!
        if not self._hwbp.temp_allocated(): # we need to set up the range scaffold
            available = self._hwbpnum
            if self.mon.is_onlyhwbps():
                available = self._hwbp.available()
                if available == 0:
                    self.logger.error("Addtional HWBP needed for range stepping")
                    return SIGABRT
            if len(self._range_exit) <= available: # allocate enough HWBPs
                reserve = self._range_exit
            else:
                reserve = [ -1 ]
            for r in self._hwbp.set_temp(reserve):
                self._bp[r]['allocated'] = SWBP
                self.dbg.software_breakpoint_set(r)
        if self._hwbp.temp_allocated() == len(self._range_exit): # all exits covered
            self._hwbp.execute()
            return None
        if addr in self._range_branch: # if branch point, single-step
            return self.single_step(None, fresh=False)
        for b in self._range_branch:   # otherwise search for next branch point and stop there
            if addr < b:
                self.dbg.run_to(b)
                return None
        return self.single_step(None, fresh=False)

    def build_range(self, start, end):
        """
        Collect all instructions in the range and analyze them. Find all points, where
        an instruction possibly leaves the range. This includes the first instruction
        after the range, provided it is reachable. These points are remembered in
        self._range_exit. If the number of exits is less than or equal to the number of
        hardware BPs, then one can check for all them. In case of dW this number is one.
        However, this is enough for handling _delay_ms(_). In all other cases, we stop at all
        branching instructions, memorized in self._range_branch, and single-step them.
        Return False, if the range is already established.
        """
        if start == self._range_start and end == self._range_end:
            return False # previously analyzed
        self._range_word = []
        self._range_exit = set()
        self._range_branch = []
        self._range_start = start
        self._range_end = end
        for a in range(start, end+2, 2):
            self._range_word += [ self._read_filtered_flash_word(a) ]
        i = 0
        while i < len(self._range_word) - 1:
            dest = []
            opcode = self._range_word[i]
            secondword = self._range_word[i+1]
            if self.branch_instr(opcode):
                self._range_branch += [ start + (i * 2) ]
            if self.two_word_instr(opcode):
                if self.branch_instr(opcode): # JMP and CALL
                    dest = [ secondword << 1 ]
                else: # STS and LDS
                    dest = [ start + (i + 2) * 2 ]
            else:
                if not self.branch_instr(opcode): # straight-line ops
                    dest = [start + (i + 1) * 2]
                elif self.skip_operation(opcode): # CPSE, SBIC, SBIS, SBRC, SBRS
                    dest = [start + (i + 1) * 2,
                               start + (i + 2 + self.two_word_instr(secondword)) * 2]
                elif self.cond_branch_operation(opcode): # BRBS, BRBC
                    dest = [start + (i + 1) * 2,
                                self.compute_possible_destination_of_branch(opcode,
                                                                                start + (i * 2)) ]
                elif self.relative_branch_operation(opcode): # RJMP, RCALL
                    dest = [ self.compute_destination_of_relative_branch(opcode, start + (i * 2)) ]
                else: # IJMP, EIJMP, RET, ICALL, RETI, EICALL
                    dest = [ -1 ]
            self.logger.debug("Dest at 0x%X: %s", start + i*2, [hex(x) for x in dest])
            if -1 in dest:
                self._range_exit.add(start + (i * 2))
            else:
                self._range_exit = self._range_exit.union([ a for a in dest
                                                                if a < start or a >= end ])
            i += 1 + self.two_word_instr(opcode)
        self._range_branch += [ end ]
        self.logger.debug("Exit points: %s", {hex(x) for x in self._range_exit})
        self.logger.debug("Branch points: %s", [hex(x) for x in self._range_branch])
        return True

    @staticmethod
    def branch_instr(opcode):
        """
        Returns True iff it is a branch instruction
        """
        if (((opcode & 0xFC00) == 0x1000) or # CPSE
            ((opcode & 0xFFEF) == 0x9409) or # IJMP / EIJMP
            ((opcode & 0xFFEE) == 0x9508) or # RET, ICALL, RETI, EICALL
            ((opcode & 0xFE0C) == 0x940C) or # CALL, JMP
            ((opcode & 0xFD00) == 0x9900) or # SBIC, SBIS
            ((opcode & 0xE000) == 0xC000) or # RJMP, RCALL
            ((opcode & 0xF800) == 0xF000) or # BRBS, BRBC
            ((opcode & 0xFC08) == 0xFC00)): # SBRC, SBRS
            return True
        return False

    @static_method
    def store_instr(opcode):
        """
        Returns True iff it is STS, ST, OUT or SEI/CLI instruction.
        """
        if (((opcode & 0xF800) == 0xB800) or # OUT
            (opcode == 0x9478) or # SEI
            (opcode == 0x94F8) or # CLI
            ((opcode & 0xD200) == 0x8200) or # STx
            (((opcode & 0xFE00) == 0x9200) and (opcode & 0x000F != 0x000F))): # STS and ST -+
            return True
        return False


    @staticmethod
    def relative_branch_operation(opcode):
        """
        Returns True iff it is a branch instruction with relative addressing mode
        """
        if (opcode & 0xE000) == 0xC000: # RJMP, RCALL
            return True
        return False

    @staticmethod
    def compute_destination_of_relative_branch(opcode, addr):
        """
        Computes branch destination for instructions with relative addressing mode
        """
        rdist = opcode & 0x0FFF
        tsc = rdist - int((rdist << 1) & 2**12)
        return addr + 2 + (tsc*2)

    @staticmethod
    def skip_operation(opcode):
        """
        Returns True iff instruction is a skip instruction
        """
        if (opcode & 0xFC00) == 0x1000: # CPSE
            return True
        if (opcode & 0xFD00) == 0x9900: # SBIC, SBIS
            return True
        if (opcode & 0xFC08) == 0xFC00: # SBRC, SBRS
            return True
        return False

    @staticmethod
    def cond_branch_operation(opcode):
        """
        Returns True iff instruction is a conditional branch instruction
        """
        if (opcode & 0xF800) == 0xF000: # BRBS, BRBC
            return True
        return False

    @staticmethod
    def branch_on_ibit(opcode):
        """
        Returns True iff instruction is a conditional branch instruction on the I-bit
        """
        return (opcode & 0xF807) == 0xF007 # BRID, BRIE

    @staticmethod
    def compute_possible_destination_of_branch(opcode, addr):
        """
        Computes branch destination address for conditional branch instructions
        """
        rdist = (opcode >> 3) & 0x007F
        tsc = rdist - int((rdist << 1) & 2**7) # compute twos complement
        return addr + 2 + (tsc*2)


    @staticmethod
    def compute_destination_of_ibranch(opcode, ibit, addr):
        """
        Interprets BRIE/BRID instructions and computes the target instruction.
        This is used to simulate the execution of these two instructions.
        """
        branch = ibit ^ bool(opcode & 0x0400 != 0)
        if not branch:
            return addr + 2
        return BreakAndExec.compute_possible_destination_of_branch(opcode, addr)

    @staticmethod
    def two_word_instr(opcode):
        """
        Returns True iff instruction is a two-word instruction
        """
        return(((opcode & ~0x01F0) == 0x9000) or # lds
               ((opcode & ~0x01F0) == 0x9200) or # sts
               ((opcode & 0x0FE0E) == 0x940C) or # jmp
               ((opcode & 0x0FE0E) == 0x940E))   # call

    def sim_two_word_instr(self, opcode, secondword, addr):
        """
        Simulate a two-word instruction with opcode and 2nd word secondword at addr (byte address).
        Update all registers (except PC) and return the (byte-) address
        where execution will continue.
        """
        newaddr = (secondword << 1) + ((opcode & 1) << 17) # new byte addr, only for branching instructions
        if (opcode & ~0x1F0) == 0x9000: # lds
            register = (opcode & 0x1F0) >> 4
            val = self.dbg.sram_read(secondword, 1)
            self.dbg.sram_write(register, val)
            self.logger.debug("Simulating lds")
            addr += 4
        elif (opcode & ~0x1F0) == 0x9200: # sts
            register = (opcode & 0x1F0) >> 4
            val = self.dbg.sram_read(register, 1)
            self.dbg.sram_write(secondword, val)
            self.logger.debug("Simulating sts")
            addr += 4
        elif (opcode & 0x0FE0E) == 0x940C: # jmp
            addr = newaddr
            self.logger.debug("Simulating jmp 0x%X", addr)
        elif (opcode & 0x0FE0E) == 0x940E: # call
            returnaddr = (addr + 4) >> 1 # now word address
            self.logger.debug("Simulating call to 0x%X", newaddr)
            self.logger.debug("Pushing return addr on stack: 0x%X", returnaddr << 1)
            sp = int.from_bytes(self.dbg.stack_pointer_read(),byteorder='little')
            self.logger.debug("Current stack pointer: 0x%X", sp)
            sp -= (2 + int(self._bigmem))
            self.logger.debug("New stack pointer: 0x%X", sp)
            self.dbg.stack_pointer_write(sp.to_bytes(2,byteorder='little'))
            if self._bigmem:
                self.dbg.sram_write(sp+1, returnaddr.to_bytes(3,byteorder='big'))
            else:
                self.dbg.sram_write(sp+1, returnaddr.to_bytes(2,byteorder='big'))
            addr = newaddr
        return addr

class HardwareBP():
    """
    This class manages the hardware breakpoints with some basic methods (including starting
    execution with the temporary breakpoint).
    """

    def __init__(self, numhwbp, logger, dbg):
        self._numhwbp = numhwbp
        self._hwbplist = [None]*numhwbp
        self._temp = None
        self.logger = getLogger('pyavrocd.hardwarebp')


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
        self.dbg.device.avr.breakpoint_clear()
        self.logger.debug("All hardware breakpoints cleared")

    def clear(self, addr):
        """
        Clear breakpoint at a given address. If successful return True, otherwise False.
        """
        if addr in self._hwbplist:
            self._free(self._hwbplist.find(addr))
            return True
        self.logger.error("Tried to clear hardware breakpoint at 0x%X, but there is none", addr)
        return False

    def _free(self, ix):
        """
        Free a BP at index ix. If unsuccessful, return False, otherwise True.
        """
        if ix < self.numhwbp and ix >= 0 and self._hwbplist[ix] is not None:
            self.logger.debug("HWBP %d at addr 0x%X freed", ix, self._hwbplist[ix])
            self._hwbplist[ix] = None
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
        Allocates the next free hardware breakpoint (counting up) and returns True
        -- provided there is a free hardware breakpoint. Otherwise, False is returned.
        """
        self.logger.debug("Trying to allocate HWBP for addr 0x%X", addr)
        for ix in range(self._numhwbp):
            if self._hwbplist[ix] is None:
                self._hwbplist[ix] = addr
                self.logger.debug("Successfully allocated HWBP %d", ix)
                return True
        self.logger.debug("Could not allocate a HWBP")
        return False

    def unallocate_hwbp0(self):
        """
        Unallocates hardware breakpoint 0. It first tries to find a free slot among the
        hardware breakpoints. If there is no free slot, it will kick out an occupied
        one and returns the address, so that this BP can become a software breakpoint.
        If we only have one hardware breakpont, we simply return the address.
        The result is either None, meaning that we were able to find some empty space,
        or it will be an address of a BP that needs to become a software breakpoint.
        The rationale behind this method is: Sometimes we need this hardware breakpoint
        (for safe single-stepping). And the best way to handle that is to find another
        hardware breakpoint slot because HWBP 0 is often assigned to a temporary breakpoint.
        """
        if self._hwbplist[0] is None:
            return None
        if self.available():
            self.set(self._hwbplist[0])
            self._free(0)
            return None
        if self._numhwbp < 2:
            reassign = self._hwbplist[0]
        else:
            reassgin = self._hwbplist[1]
            self._hwbplist[1] = self._hwbplist[0]
        self._free(0)
        return reassign

    def set_temp(self,templist):
        """
        Try to set all HWBPs for all addresses in templist. Returns None if impossible or
        returns a list of addresses that needs to become software breakpoints. This function
        is used to support range-stepping.
        """
        reassignlist = []
        if len(templist) > self._numhwbp:
            return None
        # make sure that HWBP 0 is one of our BPs!
        reassign = self.unallocate_hwp0()
        if reassign:
            reassignlist.append(reassign)
        self._temp = templist
        allocated = [addr for addr in self._hwbplist if addr is not None]
        for el in templist:
            if not self.set(el):
                trytoremove = pop(allocated)
                reassignlist.append(trytoremove)
                self.clear(trytoremove)
                self.set(el)
        return reassignlist

    def clear_temp(self):
        """
        Clears the temporary allocated hardware breakpoints.
        """
        if self._temp is None:
            return
        for el in self._temp:
            if el >= 0:
                self.clear(el)
        self._temp = None

    def temp_allocated(self):
        if self.temp is None:
            return 0
        else:
            return len(self._temp)

