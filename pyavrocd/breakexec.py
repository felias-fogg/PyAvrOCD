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

    def __init__(self, hwbps, mon, dbg, read_flash_word):
        self.mon = mon
        self.dbg = dbg
        self.logger = getLogger('pyavrocd.breakexec')
        self._hwbps = hwbps # This number includes the implicit HWBP used by run_to
        self._read_flash_word = read_flash_word
        self._hw = [-1] + [None]*self._hwbps # note that the entries start at index 1
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
        self._bp[address] =  {'active': True, 'inflash': False,
                                  'hwbp' : None, 'opcode': opcode,
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

    def update_breakpoints(self, reserved, protected_bp):
        """
        This is called directly before execution is started. It will remove
        inactive breakpoints different from protected_bp, it will assign the hardware
        breakpoints to the most recently added breakpoints, and request to set active
        breakpoints into flash, if they not there already. The reserved argument states
        how many HWBPs should be reserved for single- or range-stepping. The argument protected_bp
        is set by single and range-stepping, when we start at a place where there is a
        software breakpoint set. In this case, we do a single-step and then wait for
        GDB to re-activate the BP.
        The method will return False when at least one BP cannot be activated due
        to resource restrictions (e.g., not enough HWBPs).
        """
        # remove inactive BPs and de-allocate BPs that are now forbidden
        if not self.remove_inactive_and_deallocate_forbidden_bps(reserved, protected_bp):
            return False
        self.logger.debug("Updating breakpoints before execution")
        # all remaining BPs are active or protected
        # assign HWBPs to the most recently introduced BPs
        # take into account the possibility that hardware breakpoints are not allowed or reserved
        sortedbps = sorted(self._bp.items(), key=lambda entry: entry[1]['timestamp'], reverse=True)
        self.logger.debug("Sorted BP list: %s", sortedbps)
        for hix in range(min((self._hwbps-reserved)*(1-self.mon.is_onlyswbps()),len(sortedbps))):
            h = sortedbps[hix][0]
            hbp = sortedbps[hix][1]
            self.logger.debug("Consider BP at 0x%X", h)
            if hbp['hwbp'] or hbp['inflash']:
                self.logger.debug("BP at 0x%X is already assigned, either HWBP or SWBP", h)
                break # then all older BPs are already allocated!
            if None in self._hw: # there is still an available hwbp
                self.logger.debug("There is still a free HWBP at index: %s", self._hw.index(None))
                hbp['hwbp'] = self._hw.index(None)
                self._hw[self._hw.index(None)] = h
                if hbp['hwbp'] and hbp['hwbp'] > 1:
                    self.logger.error("Trying to set non-existent HWBP %s", hbp['hwbp'])
            else: # steal hwbp from oldest HWBP
                self.logger.debug("Trying to steal HWBP")
                stealbps = sorted(self._bp.items(), key=lambda entry: entry[1]['timestamp'])
                for s, sbp in stealbps:
                    if sbp['hwbp']:
                        self.logger.debug("BP at 0x%X is a HWBP", s)
                        if sbp['hwbp'] > 1:
                            self.logger.error("Trying to clear non-existent HWBP %s", sbp['hwbp'])
                            # self.dbg.hardware_breakpoint_clear(steal[s][1]['hwbp']-1)
                            # not yet implemented
                            return False
                        hbp['hwbp'] = sbp['hwbp']
                        self.logger.debug("Now BP at 0x%X is the HWP", h)
                        self._hw[hbp['hwbp']] = h
                        sbp['hwbp'] = None
                        break
        # now set SWBPs, if they are not already in flash
        for a, bp in self._bp.items():
            if not bp['inflash'] and not bp['hwbp']:
                if self.mon.is_onlyhwbps():
                    return False # we are not allowed to set a software breakpoint
                self.logger.debug("BP at 0x%X will now be set as a SW BP", a)
                self.dbg.software_breakpoint_set(a)
                bp['inflash'] = True
        return True

    def remove_inactive_and_deallocate_forbidden_bps(self, reserved, protected_bp):
        """
        Remove all inactive BPs and deallocate BPs that are forbidden
        (after changing BP preference). A protected SW BP is not deleted!
        These are BPs at the current PC that have been set before and
        will now be overstepped in a single-step action.
        Return False if a non-existent HWBP shall be cleared.
        """
        self.logger.debug("Deallocate forbidden BPs and remove inactive ones")
        for a, bp in list(self._bp.items()):
            if self.mon.is_onlyswbps() and bp['hwbp']: # only SWBPs allowed
                self.logger.debug("Removing HWBP at 0x%X  because only SWBPs allowed.", a)
                if bp['hwbp'] > 1: # this is a real HWBP
                    # self.dbg.hardware_breakpoint_clear(self._bp[a]['hwbp']-1)
                    # not yet implemented
                    self.logger.error("Trying to clear non-existent HWBP %s", bp['hwbp'])
                    return False
                bp['hwbp'] = None
                self._hw = [-1] + [None]*self._hwbps # entries start at 1
            if self.mon.is_onlyhwbps() and bp['inflash']: # only HWBPs allowed
                self.logger.debug("Removing SWBP at 0x%X  because only HWBPs allowed", a)
                bp['inflash'] = False
                self.dbg.software_breakpoint_clear(a)
            # deallocate HWBP
            if reserved > 0 and self._bp[a]['hwbp'] and self._bp[a]['hwbp'] <= reserved:
                if bp['hwbp'] > 1: # this is a real HWBP
                    # self.dbg.hardware_breakpoint_clear(self._bp[a]['hwbp']-1)
                    # not yet implemented
                    self.logger.error("Trying to clear non-existent HWBP %s",
                                          bp['hwbp'])
                    return False
                self._hw[bp['hwbp']] = None
                bp['hwbp'] = None
            # check for protected BP
            if a == protected_bp and bp['inflash']:
                self.logger.debug("BP at 0x%X is protected", a)
                continue
            # delete BP
            if not bp['active']: # delete inactive BP
                self.logger.debug("BP at 0x%X is not active anymore", a)
                if bp['inflash']:
                    self.logger.debug("Removed as a SWBP")
                    self.dbg.software_breakpoint_clear(a)
                if bp['hwbp']:
                    self.logger.debug("Removed as a HWBP")
                    if bp['hwbp'] > 1: # this is a real HWBP
                        # self.dbg.hardware_breakpoint_clear(self._bp[a]['hwbp']-1)
                        # not yet implemented
                        self.logger.error("Trying to clear non-existent HWBP %s",
                                              bp['hwbp'])
                        return False
                    self._hw[bp['hwbp']] = None
                self.logger.debug("BP at 0x%X will now be deleted", a)
                del self._bp[a]
        return True

    def cleanup_breakpoints(self):
        """
        Remove all breakpoints from flash and clear hardware breakpoints
        """
        self.logger.debug("Deleting all breakpoints")
        self._hw = [-1] + [None for x in range(self._hwbps)]
        # self.dbg.hardware_breakpoint_clear_all() # not yet implemented
        self.dbg.software_breakpoint_clear_all()
        self._bp = {}
        self._bpactive = 0

    def resume_execution(self, addr):
        """
        Start execution at given addr (byte addr). If none given, use the actual PC.
        Update breakpoints in memory and the HWBP. Return SIGABRT if not enough break points.
        """
        self._range_start = None
        if not self.update_breakpoints(0, -1):
            return SIGABRT
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
        if self._hw[1] is not None:
            self.logger.debug("Run to cursor at 0x%X starting at 0x%X", self._hw[1], addr)
            # according to docu, it is the word address, but in reality it is the byte address!
            self.dbg.run_to(self._hw[1])
        else:
            self.logger.debug("Now start executing at 0x%X without HWBP", addr)
            self.dbg.run()
        return None

    def single_step(self, addr, fresh=True):
        """
        Perform a single step. If at the current location, there is a software breakpoint,
        we simulate a two-word instruction or ask the hardware debugger to do a single step
        if it is a one-word instruction. The simulation saves two flash reprogramming operations.
        Otherwise, if mon._safe is true, it means that we will try to not end up in the
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
        if not self.update_breakpoints(1, addr):
            self.logger.debug("Not enough free HW BPs: SIGABRT")
            return SIGABRT
        # If there is a SWBP at the place where we want to step,
        # use the internal single-step (which will execute the instruction offline)
        # or, if a two-word instruction, simulate the step. That is, if memory
        # is not 256k!
        if addr in self._bp and self._bp[addr]['inflash']:
            if self.two_word_instr(self._bp[addr]['opcode']):
            # if there is a two word instruction, simulate
                self.logger.debug("Two-word instruction at SWBP: simulate")
                addr = self.sim_two_word_instr(self._bp[addr]['opcode'],
                                                self._bp[addr]['secondword'], addr)
                self.logger.debug("New PC(byte addr)=0x%X, return SIGTRAP", addr)
                self.dbg.program_counter_write(addr>>1)
                return SIGTRAP
            # one-word instructions are handled by offline execution in the OCD
            self.logger.debug("One-word instruction at SWBP: offline execution in OCD")
            self.dbg.step()
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
        if not self.branch_instr(opcode):
            destination = addr + 2 + 2*int(self.two_word_instr(opcode))
            self.logger.debug("This is not a branch instruction. Destination=0x%X", destination)
        if self.branch_on_ibit(opcode):
            ibit = bool(self.dbg.status_register_read()[0] & 0x80)
            destination = self.compute_destination_of_ibranch(opcode, ibit, addr)
            self.logger.debug("Branching on I-Bit. Destination=0x%X", destination)
        if destination is not None:
            self.logger.debug("Run to cursor... at 0x%X, return None", destination)
            self.dbg.run_to(destination)
            return None
        # for the remaining branch instructions,
        # clear I-bit before and set it afterwards (if it was on before)
        self.logger.debug("Remaining branch instructions")
        sreg = self.dbg.status_register_read()[0]
        self.logger.debug("sreg=0x%X", sreg)
        ibit = sreg & 0x80
        sreg &= 0x7F # clear I-Bit
        self.logger.debug("New sreg=0x%X",sreg)
        self.dbg.status_register_write(bytearray([sreg]))
        self.logger.debug("Now make a step...")
        self.dbg.step()
        sreg = self.dbg.status_register_read()[0]
        self.logger.debug("New sreg=0x%X", sreg)
        sreg |= ibit
        self.logger.debug("Restored sreg=0x%X", sreg)
        self.dbg.status_register_write(bytearray([sreg]))
        self.logger.debug("Returning with SIGTRAP")
        return SIGTRAP


    def range_step(self, start, end):
        """
        range stepping: Break only if we leave the interval start-end. If there is only
        one exit point, we watch that. If it is an inside point (e.g., RET), we single-step on it.
        Otherwise, we break at each branching point and single-step this branching instruction.
        In principle this can be generalized to n exit points (n being the number of hardware BPs).
        Note that we need to return after the first step to allow GDB to set a breakpoint at the
        location where we started.
        """
        self.logger.debug("Range stepping from 0x%X to 0x%X", start, end)
        if not self.mon.is_range() or self.mon.is_old_exec():
            self.logger.debug("Range stepping forbidden")
            return self.single_step(None)
        if start%2 != 0 or end%2 != 0:
            self.logger.error("Range addresses in range stepping are ill-formed")
            return self.single_step(None)
        if start == end:
            self.logger.debug("Empty range: Simply single step")
            return self.single_step(None)
        new_range = self.build_range(start, end)
        reservehwbps = len(self._range_exit)
        if reservehwbps > self._hwbps or self.mon.is_onlyhwbps():
            reservehwbps = 1
        addr = self.dbg.program_counter_read() << 1
        if not self.update_breakpoints(reservehwbps, addr):
            return SIGABRT
        if addr < start or addr >= end: # starting outside of range, should not happen!
            self.logger.error("PC 0x%X outside of range boundary", addr)
            return self.single_step(None)
        if (addr in self._range_exit or # starting at possible exit point inside range
            self._read_filtered_flash_word(addr) in { BREAKCODE, SLEEPCODE } or # special opcode
            addr in self._bp or # a SWBP at this point
            new_range): # or it is a new range
            return self.single_step(None, fresh=False) # reduce to one step!
        if len(self._range_exit) == reservehwbps: # we can cover all exit points!
            # if more HWBPs, one could use them here!
            # #MOREHWBPS
            self.dbg.run_to(list(self._range_exit)[0]) # this covers only 1 exit point!
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

