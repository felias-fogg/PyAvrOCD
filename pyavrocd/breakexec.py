"""
This module deals with breakpoints and execution.
"""

# args, logging
from logging import getLogger

# Errors
from pyavrocd.errors import FatalError

# Hardware breakpoints
from pyavrocd.hardwarebp import HardwareBP

# special opcodes
BREAKCODE = 0x9598
SLEEPCODE = 0x9588

# signal codes
NOSIG   = 0     # no signal
SIGHUP  = 1     # no connection
SIGINT  = 2     # Interrupt  - user interrupted the program (UART ISR)
SIGILL  = 4     # Illegal instruction (BREAK or undefined)
SIGTRAP = 5     # Trace trap  - stopped on a breakpoint
SIGABRT = 6     # Abort because of a fatal error or no breakpoint available
SIGBUS = 10     # Access to undefined portion of memory means in our case stack overflow
SIGSEGV = 11    # Invalid memory reference means executable not loaded
SIGSYS = 12     # Bad system call means in our case "Too many breakpoints"

SWBP = 1
HWBP = -1

SREGADDR = 0x5F

class BreakAndExec():
    """
    This class manages breakpoints, supports flashwear minimizing execution, and
    makes interrupt-safe single stepping possible.
    """

    def __init__(self, mon, dbg, read_flash_word):
        self.mon = mon
        self.dbg = dbg
        self.logger = getLogger('pyavrocd.breakexec')
        self._hwbp = HardwareBP(dbg)
        self._read_flash_word = read_flash_word
        self._bp = {}
        self._bpactive = 0
        self._bstamp = 0
        # more than 128 kB:
        self._big_flash_mem = self.dbg.memory_info.memory_info_by_name('flash')['size'] > 128*1024
        self._big_sram = self.dbg.memory_info.memory_info_by_name('internal_sram')['size'] \
                                   > 64*1024
        self._sram_start = self.dbg.memory_info.memory_info_by_name('internal_sram')['address']
        self._range_start = 0
        self._range_end = 0
        self._range_word = []
        self._range_branch = []
        self._range_exit = set()

    def maxbpnum(self):
        """
        Returns maximum number of explicit breakpoints
        """
        if self.mon.is_onlyhwbps():
            return self.dbg.get_hwbpnum()
        return 1024

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
        self._bp[address] =  {'active': True, 'allocated': None,
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

    def _read_filtered_flash_word(self, address):
        """
        Instead of reading directly from flash memory, we filter out break points.
        """
        if address in self._bp:
            return self._bp[address]['opcode']
        return self._read_flash_word(address)

    def _update_breakpoints(self, protected_bp, release_temp=True):
        """
        This is called directly before execution is started. It will remove
        inactive breakpoints different from protected_bp, it will assign a
        hardware breakpoint to the most recently added unallocated breakpoint
        (kicking out the oldest hardware breakpoint),  and it will request to set
        active breakpoints into flash, if they not there already. The argument protected_bp
        is set by single and range-stepping when we start at a place where there is a
        software breakpoint set. In this case, we do a single-step and then wait for
        GDB to re-activate the BP after the single step (saving two flash page reprogramming
        operations).

        The method will return False when at least one BP cannot be activated due
        to resource restrictions (e.g., not enough HWBPs).
        """
        if self.mon.is_old_exec():
            return True
        self.logger.debug("Updating breakpoints before execution")
        # release temporarily allocated hardware breakpoints (if requested)
        if self._hwbp.temp_allocated() and release_temp:
            self._hwbp.clear_temp()
        # remove inactive BPs and de-allocate BPs that are now forbidden
        self._remove_inactive_and_deallocate_forbidden_bps(protected_bp)
        # check if there are enough software and hardware breakpoints to allocate
        if len(self._bp) > self.maxbpnum(): # too many BPs requested
            self.logger.debug("Not enough (HW)BPs")
            return False
        # if list of BPs is empty, just return
        if not self._bp:
            return True
        # determine most recent HWBP, probably a temporary one -- if not already allocated!
        most_recent = max(self._bp, key=lambda key: self._bp[key]['timestamp'])
        # all remaining BPs are active or protected
        # assign a HWBP to the most recently introduced BP (if we are not range-stepping)
        # and take into account the possibility that hardware breakpoints are not allowed
        if self._bp[most_recent]['allocated'] is None and not self._hwbp.temp_allocated() \
            and not self.mon.is_onlyswbps():
            # try to set a HWBP
            if self._hwbp.set(most_recent) is not None:
                self._bp[most_recent]['allocated'] = HWBP
            else:
                # find oldest HWBP
                kickout = min([b for b in self._bp if self._bp[b]['allocated'] == HWBP],
                                  key=lambda key: self._bp[key]['timestamp'])
                # kick it out
                self._hwbp.clear(kickout)
                self._bp[kickout]['allocated'] = None
                # now there should be a free slot
                if self._hwbp.set(most_recent) is not None:
                    self._bp[most_recent]['allocated'] = HWBP
                else:
                    self.logger.error("Could not allocate a HWBP for new breakpoint 0x%X", most_recent)
        # now assign the remaining BPs
        for a in self._bp:
            if self._bp[a]['allocated'] is None:
                # try first to set as HWBP if allowed
                if not self.mon.is_onlyswbps() and self._hwbp.set(a) is not None:
                    self._bp[a]['allocated'] = HWBP
                else:
                    # we catered for the HWBPs already above
                    if not self.dbg.software_breakpoint_set(a):
                        self.logger.debug("Could not allocate SWBP for 0x%X", a)
                        return False
                    self.logger.debug("BP at 0x%X will now be set as a SWBP", a)
                    self._bp[a]['allocated'] = SWBP
        return True

    def _remove_inactive_and_deallocate_forbidden_bps(self, protected_bp):
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
                self._bp[a]['allocated'] = None
                self._hwbp.clear(a)
            if self.mon.is_onlyhwbps() and self._bp[a]['allocated'] == SWBP: # only HWBPs allowed
                self.logger.debug("Removing SWBP at 0x%X  because only HWBPs allowed", a)
                self._bp[a]['allocated'] = None
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
                self._bp[a] = None
        self._bp = { k : v for k, v in self._bp.items() if v is not None }

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
        SWBPs at this point are not protected! The reason is that if we start at a location
        with a BP, GDB would never simply resume when the BP is still there. So, we can safely
        remove a SWBP before starting to execute at this point.
        """
        self._range_start = None
        if addr:
            self.dbg.program_counter_write(addr>>1)
        else:
            addr = self.dbg.program_counter_read() << 1
        if not self._update_breakpoints(None): # if we resume, a BP is not protected at that point!
            return SIGSYS
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
        interrupt vector table. For all instruction (except those branching on the I-bit
        or addressing SREG), we clear the I-bit before and set it afterwards (if necessary).
        For the remaining one, we simulate.
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
        if not self._update_breakpoints(addr):
            self.logger.error("Not enough free HW BPs: SIGSYS")
            return SIGSYS
        if not self._stack_pointer_legal(opcode):
            return SIGBUS
        # If there is a SWBP at the place where we want to step,
        # if a two-word instruction, simulate the step
        if addr in self._bp and self._bp[addr]['allocated']:
            if self._two_word_instr(self._bp[addr]['opcode']):
            # if there is a two word instruction, simulate
                self.logger.debug("Two-word instruction at SWBP: simulate")
                addr = self._sim_two_word_instr(self._bp[addr]['opcode'],
                                                self._bp[addr]['secondword'], addr)
                self.logger.debug("New PC(byte addr)=0x%X, return SIGTRAP", addr)
                self.dbg.program_counter_write(addr>>1)
                return SIGTRAP
        # if stepping is unsafe, just use the AVR stepper
        if not self.mon.is_safe():
            self.logger.debug("Unsafe Single-stepping: use AVR stepper, return SIGTRAP")
            self.dbg.step()
            return SIGTRAP
        # now we have to check for unsafe instructions, which we simulate;
        # the other instructions will be single-stepped with the I-Bit cleared.
        self.logger.debug("Interrupt-safe stepping begins here")
        if self._filter_unsafe_instruction(addr, opcode):
            return SIGTRAP
        # for the remaining instructions,
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

    def _stack_pointer_legal(self, opcode):
        """
        Checks whether the next instruction operates on the stack and will mess up I/O
        registers or load data/return addresses from I/O space. If so, False is returned.
        """
        if self._pop_instr(opcode) or self._retx_instr(opcode):
            return int.from_bytes(self.dbg.stack_pointer_read(),byteorder='little') >= \
              self._sram_start-1
        if self._push_instr(opcode):
            return int.from_bytes(self.dbg.stack_pointer_read(),byteorder='little') >= \
              self._sram_start
        if self._callx_instr(opcode):
            return int.from_bytes(self.dbg.stack_pointer_read(),byteorder='little') >= \
              self._sram_start+1
        return True

    #pylint: disable=too-many-return-statements,too-many-branches
    #It simply is a large case analysis, would not make sense to break it up
    def _filter_unsafe_instruction(self, addr, opcode):
        """
        Check all instructions for potential I-bit manipulation. If
        the instruction addresses SREG, it will be simulated and True is returned.
        """
        # if the opcode is a register only instruction, simply return
        if self._low_alu_instr(opcode):
            return False
        # Data space too large
        if self._big_sram:
            # One needs to account for RAMPZ / RAMPX / RAMPY / RAMPD registers
            # when computing target or source address in SRAM
            raise FatalError("SRAM too large. Disable safe stepping or extend stepping method")
        # LDS and STS
        if self._long_load_or_store_instr(opcode):
            secondword = self._read_filtered_flash_word(addr + 2)
            if secondword != SREGADDR:
                return False
            self._load_or_store_reg(opcode, self._is_store_instr)
            return self._sim_done(addr+2)
        # LD r,X, ST X,r and LD r,Y, STS Y, r without displacement
        if self._indirect_load_or_store_without_displacement_instr(opcode):
            if self._is_x_reg(opcode):
                base_reg = 26
            elif self._is_y_reg(opcode):
                base_reg = 28
            else:
                base_reg = 30
            iaddr = int.from_bytes(self.dbg.sram_read(base_reg, 2), byteorder='little')
            if self._is_pre_decr(opcode):
                iaddr -= 1
            if iaddr != SREGADDR:
                return False
            self._load_or_store_reg(opcode, self._is_store_instr)
            if self._is_post_incr(opcode):
                iaddr += 1
            if self._is_change_ix(opcode):
                self.dbg.sram_write(base_reg, iaddr.to_bytes(2, byteorder='little'))
            return self._sim_done(addr)
        # LD r, Y/Z and ST Y/Z, r with displacement
        if self._indirect_load_or_store_with_displacement_instr(opcode):
            disp = self._extract_displacement(opcode)
            if self._is_y_reg(opcode):
                base_reg = 28
            else:
                base_reg = 30
            iaddr = int.from_bytes(self.dbg.sram_read(base_reg, 2), byteorder='little') + disp
            if iaddr != SREGADDR:
                return False
            self._load_or_store_reg(opcode, self._is_store_instr)
            return self._sim_done(addr)
        # IN and OUT
        if self._in_or_out_instr(opcode):
            if self._extract_io_addr(opcode) == SREGADDR - 0x20:
                self._load_or_store_reg(opcode, self._is_out_instr)
                return self._sim_done(addr)
            return False
        # BCLR/BSET
        if self._bit_clear_or_set_in_sreg_instr(opcode):
            if opcode == 0x94F8: # CLI
                sreg = self.dbg.status_register_read()[0]
                sreg &= ~0x80
                self.dbg.status_register_write(bytearray([sreg]))
                return self._sim_done(addr)
            if opcode == 0x9478: # SEI
                sreg = self.dbg.status_register_read()[0]
                sreg |= 0x80
                self.dbg.status_register_write(bytearray([sreg]))
                return self._sim_done(addr)
            return False
        # BRIE, BRID
        if self._branch_on_ibit_instr(opcode):
            ibit = bool(self.dbg.status_register_read()[0] & 0x80)
            destination = self._compute_destination_of_ibranch(opcode, ibit, addr)
            self.logger.debug("Branching on I-Bit. Destination=0x%X", destination)
            self.dbg.program_counter_write(destination>>1)
            return True
        # XCH and LAx
        if self._exchange_instr(opcode) or self._lax_instr(opcode):
            # the avr8 architecture does not support these instructions
            if self.dbg.get_architecture() != "avr8e":
                return False
            if int.from_bytes(self.dbg.sram_read(30, 2), byteorder='little') != SREGADDR:
                return False
            tempval = self.dbg.status_register_read()
            regnum = self._extract_register(opcode)
            regval = self.dbg.sram_read(regnum, 1)
            if self._exchange_instr(opcode):
                self.dbg.status_register_write(regval)
            elif self._lac_instr(opcode):
                self.dbg.status_register_write(bytearray([(0xFF-regval[0])&tempval[0]]))
            elif self._las_instr(opcode):
                self.dbg.status_register_write(bytearray([regval[0]|tempval[0]]))
            elif self._lat_instr(opcode):
                self.dbg.status_register_write(bytearray([regval[0]^tempval[0]]))
            else:
                raise FatalError("Instruction decoding error in filter_unsafe_instructions")
            self.dbg.sram_write(regnum, tempval)
            return self._sim_done(addr)
        return False

    def _load_or_store_reg(self, opcode, do_store_check):
        """
        Load or stores SREG from/to a register. The do_store_check parameter
        is a function parameter that checks the right bit in the opcode.
        """
        reg = self._extract_register(opcode)
        if do_store_check(opcode):
            self.dbg.status_register_write(bytearray(self.dbg.sram_read(reg,1)))
        else:
            self.dbg.sram_write(reg, self.dbg.status_register_read())


    def _sim_done(self, addr):
        """
        Increments PC by 2 and then returns True
        """
        self.dbg.program_counter_write((addr + 2) >> 1)
        return True

    def range_step(self, start, end):
        """
        range stepping: Break only if we leave the interval start-end. If we can cover all
        exit points, we watch them. If it is an inside point (e.g., RET), we single-step on it.
        In order to do so, we allocate temporarily some hardware breakpoints. These get released
        when we do an ordinary 'continue' or 'step'.
        Otherwise, we break at each branching point and single-step this branching instruction.
        Note that we need to return after the first step to allow GDB to set a breakpoint at the
        location where we started.
        There is one corner case: If only hardware breakpoints are allowed, and all of them
        are in use, we simply single-step.
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
        addr = self.dbg.program_counter_read() << 1
        new_range = self._build_range(start, end)
        if not self._update_breakpoints(addr, release_temp=new_range):
            return SIGSYS
        if self.maxbpnum() == self._bpactive:
            return self.single_step(None)
        if addr < start or addr >= end: # starting outside of range, should not happen!
            self.logger.error("PC 0x%X outside of range boundary", addr)
            return self.single_step(None)
        if (addr in self._range_exit or # starting at possible exit point inside range
            self._read_filtered_flash_word(addr) in { BREAKCODE, SLEEPCODE } or # special opcode
            addr in self._bp or # a SWBP at this point
            new_range): # or it is a new range
            return self.single_step(None, fresh=False) # reduce to one step!
        if not self._hwbp.temp_allocated(): # we need to set up the range scaffold
            available = self.dbg.get_hwbpnum()
            if self.mon.is_onlyhwbps():
                available = self._hwbp.available()
                if available == 0:
                    self.logger.warning("Additional HWBP needed for range stepping")
                    return self.single_step(None)
            if len(self._range_exit) <= available: # allocate enough HWBPs
                reserve = self._range_exit
            else:
                reserve = [ -1 ]
            for reassign in self._hwbp.set_temp(reserve):
                if not self.dbg.software_breakpoint_set(reassign):
                    self.logger.error("Could not reassgin HWBPs to SWBPs in range-step")
                    return SIGSYS
                self._bp[reassign]['allocated'] = SWBP
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

    def _build_range(self, start, end):
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
            if self._branch_instr(opcode):
                self._range_branch += [ start + (i * 2) ]
            if self._two_word_instr(opcode):
                if self._branch_instr(opcode): # JMP and CALL
                    dest = [ secondword << 1 ]
                else: # STS and LDS
                    dest = [ start + (i + 2) * 2 ]
            else:
                if not self._branch_instr(opcode): # straight-line ops
                    dest = [start + (i + 1) * 2]
                elif self._skip_instr(opcode): # CPSE, SBIC, SBIS, SBRC, SBRS
                    dest = [start + (i + 1) * 2,
                               start + (i + 2 + self._two_word_instr(secondword)) * 2]
                elif self._cond_branch_instr(opcode): # BRBS, BRBC
                    dest = [start + (i + 1) * 2,
                                self._compute_possible_destination_of_branch(opcode,
                                                                                start + (i * 2)) ]
                elif self._relative_branch_instr(opcode): # RJMP, RCALL
                    dest = [ self._compute_destination_of_relative_branch(opcode, start + (i * 2)) ]
                else: # IJMP, EIJMP, RET, ICALL, RETI, EICALL
                    dest = [ -1 ]
            self.logger.debug("Dest at 0x%X: %s", start + i*2, [hex(x) for x in dest])
            if -1 in dest:
                self._range_exit.add(start + (i * 2))
            else:
                self._range_exit = self._range_exit.union([ a for a in dest
                                                                if a < start or a >= end ])
            i += 1 + self._two_word_instr(opcode)
        self._range_branch += [ end ]
        self.logger.debug("Exit points: %s", {hex(x) for x in self._range_exit})
        self.logger.debug("Branch points: %s", [hex(x) for x in self._range_branch])
        return True

    def _sim_two_word_instr(self, opcode, secondword, addr):
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
            sp -= (2 + int(self._big_flash_mem))
            self.logger.debug("New stack pointer: 0x%X", sp)
            self.dbg.stack_pointer_write(sp.to_bytes(2,byteorder='little'))
            if self._big_flash_mem:
                self.dbg.sram_write(sp+1, returnaddr.to_bytes(3,byteorder='big'))
            else:
                self.dbg.sram_write(sp+1, returnaddr.to_bytes(2,byteorder='big'))
            addr = newaddr
        return addr


    @staticmethod
    def _extract_io_addr(opcode):
        """
        Extracts the IO address of an IN/OUT opcode
        """
        return ((opcode & 0x0600) >> 5) + (opcode & 0x000F)

    @staticmethod
    def _extract_displacement(opcode):
        """
        Extracts the displacement from a load/store instruction with displacements
        """
        return ((opcode & 0x2000) >> 8) + ((opcode & 0x0C00) >> 7) + (opcode & 0x0007)

    @staticmethod
    def _is_out_instr(opcode):
        """
        Returns True iff the given IN or OUT opcode is an OUT instruction.
        """
        return opcode & 0x0800 != 0

    @staticmethod
    def _is_post_incr(opcode):
        """
        Returns True iff the opcode is a post-increment instruction
        """
        return opcode & 3 == 1

    @staticmethod
    def _is_pre_decr(opcode):
        """
        Returns True iff the opcode is a pre-decrement instruction
        """
        return opcode & 3 == 2

    @staticmethod
    def _is_change_ix(opcode):
        """
        Returns True iff the index operation is a pre-decr or post-incr instruction.
        """
        return opcode & 3 != 0

    @staticmethod
    def _is_x_reg(opcode):
        """
        Checks whether this is an indirect store/load instruction with
        X as the index register
        """
        return opcode & 0xF00C == 0x900C

    @staticmethod
    def _is_y_reg(opcode):
        """
        Checks whether it is the Y or Z register, given that it is a displacement
        or Y/Z indirect store/load instruction.
        So, this has to be checked before this method can be applied.
        """
        return opcode & 0x0008 == 0x0008

    @staticmethod
    def _extract_register(opcode):
        """
        Extracts the register number. The placement of the register bits appears to
        be universal.
        """
        return (opcode & 0x01F0) >> 4

    @staticmethod
    def _is_store_instr(opcode):
        """
        Checks whether the given opcode LD(S)(D)/ST(S)(D) is a store or load instruction.
        Returns True iff it is a store instruction.
        """
        return opcode & 0x0200 != 0

    @staticmethod
    def _low_alu_instr(opcode):
        """
        Returns True iff it is a ALU instruction in the lower half
        Everything below 0x8000, except CPSE:
           0001 00xx xxxx xxxx CPSE
        """
        return opcode < 0x8000 and (opcode & 0xFC00) != 0x1000

    @staticmethod
    def _lax_instr(opcode):
        """
        Returns True iff it is a laX instruction
        1001 001x xxxx 0110 LAC
        1001 001x xxxx 0101 LAS
        1001 001x xxxx 0111 LAT
        """
        return opcode & 0xFE0C == 0x9204 and opcode & 3 != 0

    @staticmethod
    def _lac_instr(opcode):
        """
        Returns True iff it is a lac instruction
        1001 001x xxxx 0110 LAC
        """
        return opcode & 0xFE0F == 0x9206

    @staticmethod
    def _las_instr(opcode):
        """
        Returns True if las instruction
        1001 001x xxxx 0101 LAS
        """
        return opcode & 0xFE0F == 0x9205

    @staticmethod
    def _lat_instr(opcode):
        """
        Returns True if las instruction
        1001 001x xxxx 0111 LAT
        """
        return opcode & 0xFE0F == 0x9207

    @staticmethod
    def _branch_instr(opcode):
        """
        Returns True iff it is a branch instruction
        """
        return (BreakAndExec._skip_instr(opcode) or
                BreakAndExec._cond_branch_instr(opcode) or
                BreakAndExec._callx_instr(opcode) or
                BreakAndExec._jmpx_instr(opcode) or
                BreakAndExec._retx_instr(opcode))

    @staticmethod
    def _pop_instr(opcode):
        """
        Returns True when opcode is a POP instruction
        1001 000x xxxx 1111
        """
        return (opcode & 0xFE0F) == 0x900F

    @staticmethod
    def _push_instr(opcode):
        """
        Returns True when opcode is PUSH instruction
        1001 001x xxxx 1111
        """
        return (opcode & 0xFE0F) == 0x920F

    @staticmethod
    def _retx_instr(opcode):
        """
        Returns True when opcode is a RET or RETI instruction
        1001 0101 000x 1000
        """
        return (opcode & 0xFFEF) == 0x9508

    @staticmethod
    def _callx_instr(opcode):
        """
        Returns True when the opcode is a (R)(E)(I)CALL instruction:
        1001 0101 000x 1001 (E)ICALL
        1001 010x xxxx 111x CALL
        1101 xxxx xxxx xxxx RCALL
        """
        return (((opcode & 0xFFEF) == 0x9509) or # (E)ICALL
                ((opcode & 0xFE0E) == 0x940E) or # CALL
                ((opcode & 0xF000) == 0xD000)) # RCALL

    @staticmethod
    def _jmpx_instr(opcode):
        """
        Returns True when the opcode is a (R)(E)(I)JMP instruction:
        1001 0100 000x 1001 (E)IJMP
        1001 010x xxxx 110x JMP
        1100 xxxx xxxx xxxx RJMP
        """
        return (((opcode & 0xFFEF) == 0x9409) or # (E)JMP
                ((opcode & 0xFE0E) == 0x940C) or # JMP
                ((opcode & 0xF000) == 0xC000)) # RJMP

    @staticmethod
    def _relative_branch_instr(opcode):
        """
        Returns True iff it is a branch instruction with relative addressing mode
        1101 xxxx xxxx xxxx RCALL
        1100 xxxx xxxx xxxx RJMP
        """
        if (opcode & 0xE000) == 0xC000: # RJMP, RCALL
            return True
        return False

    @staticmethod
    def _compute_destination_of_relative_branch(opcode, addr):
        """
        Computes branch destination for instructions with relative addressing mode
        """
        rdist = opcode & 0x0FFF
        tsc = rdist - int((rdist << 1) & 2**12)
        return addr + 2 + (tsc*2)

    @staticmethod
    def _skip_instr(opcode):
        """
        Returns True iff instruction is a skip instruction
        0001 00xx xxxx xxxx CPSE
        1001 1001 xxxx xxxx SBIC
        1001 1011 xxxx xxxx SBIS
        1111 110x xxxx 0xxx SBRC
        1111 111x xxxx 0xxx SBRS
        """
        if (opcode & 0xFC00) == 0x1000: # CPSE
            return True
        if (opcode & 0xFD00) == 0x9900: # SBIC, SBIS
            return True
        if (opcode & 0xFC08) == 0xFC00: # SBRC, SBRS
            return True
        return False

    @staticmethod
    def _cond_branch_instr(opcode):
        """
        Returns True iff instruction is a conditional branch instruction
        1111 01xx xxxx xxxx BRBC
        1111 00xx xxxx xxxx BRBS
        """
        if (opcode & 0xF800) == 0xF000: # BRBS, BRBC
            return True
        return False

    @staticmethod
    def _branch_on_ibit_instr(opcode):
        """
        Returns True iff instruction is a conditional branch instruction on the I-bit
        1111 01xx xxxx x111 BRID
        1111 00xx xxxx x111 BRIE

        """
        return (opcode & 0xF807) == 0xF007 # BRID, BRIE

    @staticmethod
    def _compute_possible_destination_of_branch(opcode, addr):
        """
        Computes branch destination address for conditional branch instructions
        """
        rdist = (opcode >> 3) & 0x007F
        tsc = rdist - int((rdist << 1) & 2**7) # compute twos complement
        return addr + 2 + (tsc*2)


    @staticmethod
    def _compute_destination_of_ibranch(opcode, ibit, addr):
        """
        Interprets BRIE/BRID instructions and computes the target instruction.
        This is used to simulate the execution of these two instructions.
        """
        branch = ibit ^ bool(opcode & 0x0400 != 0)
        if not branch:
            return addr + 2
        return BreakAndExec._compute_possible_destination_of_branch(opcode, addr)

    @staticmethod
    def _long_load_or_store_instr(opcode):
        """
        Returns True iff opcode is a two-word load or store instruction (LDS or STS)
        1001 000x xxxx 0000 LDS
        1001 001x xxxx 0000 STS
        """
        return opcode & 0xFC0F == 0x9000

    @staticmethod
    def _indirect_load_or_store_without_displacement_instr(opcode):
        """
        Returns True iff opcode is an indirect load or store instruction without displacement
        1001 00sx xxxx 1100 LD r, X    / ST X, r
        1001 00sx xxxx 1101 LD r, X+   / ST X+, r
        1001 00sx xxxx 1110 LD r, -X   / ST -X, r
        1001 00sx xxxx y001 LD r, Y/Z+ / ST Y/Z+, r
        1001 00sx xxxx y010 LD r, -Y/Z / ST -Y/Z, r
        """
        return opcode & 0xFC00 == 0x9000 and opcode & 0x0003 != 3 and \
            (opcode & 0x000C == 0x000C or (opcode & 0x0004 == 0 and opcode & 0x0003 != 0))

    @staticmethod
    def _indirect_load_or_store_with_displacement_instr(opcode):
        """
        Returns True iff opcode is an indirect load or store instruction with displacement (perhaps 0)
        10x0 xxsx xxxx yxxx  LDS r, Y/Z+q / STD Y/Z+q, r
        """
        return opcode & 0xD000 == 0x8000

    @staticmethod
    def _exchange_instr(opcode):
        """
        Returns True iff opcode is a XCH instruction
        1001 001r rrrr 0100
        """
        return (opcode & 0xFE0F) == 0x9204

    @staticmethod
    def _in_or_out_instr(opcode):
        """
        Returns True iff opcode is a IN or OUT instruction
        1011 sxxx xxxx xxxx IN / OUT
        """
        return opcode & 0xF000 == 0xB000

    @staticmethod
    def _bit_clear_or_set_in_sreg_instr(opcode):
        """
        Returns True if opcode is a bit clear or set in SREG instruction
        1001 0100 1xxx 1000 BCLR
        1001 0100 0xxx 1000 BSET
         """
        return opcode & 0xFF0F == 0x9408

    @staticmethod
    def _two_word_instr(opcode):
        """
        Returns True iff instruction is a two-word instruction
        1001 000x xxxx 0000 LDS
        1001 001x xxxx 0000 STS
        1001 010x xxxx 111x CALL
        1001 010x xxxx 110x JMP
        """
        return(((opcode & ~0x03F0) == 0x9000) or # lds / sts
               ((opcode & 0x0FE0C) == 0x940C))   # jmp / call

