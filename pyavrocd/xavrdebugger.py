"""
The debugger backend for the EDBG-based probes (Atmel-ICE, PICkit4, SNAP, (m/n)EDBG, ...),
built on pymcuprog's AvrDebugger. The probe-independent session logic is in session.py;
this module supplies the primitives it needs.
"""
from typing import Any #pylint disable=unused-import
from collections.abc import Callable
import functools

# utilities
import time
import argparse

#edbg library
from pyedbglib.protocols.jtagice3protocol import Jtagice3ResponseError
from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.protocols.avrispprotocol import AvrIspProtocol, AvrIspProtocolError #pylint: disable=unused-import
from pyedbglib.protocols.edbgprotocol import EdbgProtocol
from pyedbglib.protocols import housekeepingprotocol
from pyedbglib.hidtransport.hidtransportbase import HidTransportBase

# pymcuorig library
from pymcuprog.avrdebugger import AvrDebugger
from pymcuprog.nvmspi import NvmAccessProviderCmsisDapSpi, NvmAccessProviderCmsisDapAvr
from pymcuprog.pymcuprog_errors import PymcuprogNotSupportedError, PymcuprogError
from pymcuprog.utils import read_target_voltage, read_tool_info


from pyavrocd.backend import DebugBackend, SwbpSupport, BackendError, BackendNotSupportedError,\
     InvalidAddressError, IspConnectionError
from pyavrocd.session import AvrSession, OcdNotEnabledError, OcdLockedError
from pyavrocd.termination import guard_probe_transactions
from pyavrocd.xnvmdebugwire import XNvmAccessProviderCmsisDapDebugwire
from pyavrocd.xnvmmegaavrjtag import XNvmAccessProviderCmsisDapMegaAvrJtag
from pyavrocd.xnvmupdi import XNvmAccessProviderCmsisDapUpdi
from pyavrocd.errors import FatalError, EndOfSession

#pylint: disable=too-many-public-methods,too-many-instance-attributes
class EdbgBackend(AvrSession, AvrDebugger):
    """
    Backend for the EDBG-based probes.

    AvrSession (and through it DebugBackend) comes first in the method resolution order,
    so its methods (run, run_to, step, flash_read, program_counter_read, the register
    methods) and the SERVER implementation of the software breakpoints would hide
    AvrDebugger's methods of the same name. That is why this class calls AvrDebugger's
    methods explicitly (AvrDebugger.x(self, ...)), never through super(), and overrides
    the software breakpoint methods with the probe's.
    """
    SWBP_SUPPORT = SwbpSupport.PROBE

    #pylint: disable=super-init-not-called,too-many-positional-arguments
    def __init__(self, transport : HidTransportBase,
                     devicename : str,
                     iface : str,
                     args : argparse.Namespace) -> None:
        """
        We do not want to make use of AvrDebugger's init method,
        because all startup code is collected in the start_debugging method!
        """
        AvrSession.__init__(self, devicename, iface, args)
        self.transport : HidTransportBase = transport
        self.clkprg : int = args.clkprg # JTAG programming clock frequency
        self.clkdeb : int = args.clkdeb # JTAG debug clock frequency
        self.kbps : int = args.kbps # UPDI/PDI communication speed limit
        self.timers_run : bool = args.timers[0]=='r'
        self.flashmemtype : int = 0
        self.spidevice : NvmAccessProviderCmsisDapSpi | None = None
        self.device : NvmAccessProviderCmsisDapAvr
        self.edbg_protocol : EdbgProtocol | None = None
        self.housekeeper : housekeepingprotocol.Jtagice3HousekeepingProtocol | None = None
        self.use_events_for_run_stop_state =  False # in order to avoid the timing glitch with ATmega32/Atmel-ICE
        # software breakpoints requested from the probe (byte addresses), and whether the PC
        # has been written since the target last stopped (see _step_off_written_pc_bp)
        self._swbps : set[int] = set()
        self._pc_written : bool = False

        # Edbg protocol instance, necessary to access target power control
        if transport and transport.hid_device is not None:
            self.edbg_protocol = EdbgProtocol(transport)
            self.logger.debug("EdbgProtocol instance created")

        # Now attach the right NVM device
        if iface == "updi":
            self.device = XNvmAccessProviderCmsisDapUpdi(self.transport, self.device_info, manage=self.manage)
            self.flashmemtype = Avr8Protocol.AVR8_MEMTYPE_BOOT_FLASH_ATOMIC
        elif iface == "debugwire":
            self.device = XNvmAccessProviderCmsisDapDebugwire(self.transport, self.device_info, manage=self.manage)
            self.flashmemtype =  Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE
        elif iface == "jtag" and self._architecture =="avr8":
            self.device = XNvmAccessProviderCmsisDapMegaAvrJtag(self.transport, self.device_info, manage=self.manage)
            self.flashmemtype =  Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE

        self.logger.info("Nvm instance created, iface: %s, HWBPs: %d, arch: %s",
                              self._iface, self._hwbpnum, self._architecture)
        if self.manage == []:
            self.manage = [ 'none' ]
        self.logger.info("Managing fuses: %s", ", ".join(self.manage))

    ######## Primitives for AvrSession

    def _sign_on(self, announce : bool = False) -> None:
        """
        Start a housekeeping session; with 'announce', create the housekeeper and log the tool
        """
        if announce or self.housekeeper is None:
            self.housekeeper = housekeepingprotocol.Jtagice3HousekeepingProtocol(self.transport)
        self.housekeeper.start_session()
        if announce:
            dap_info = read_tool_info(self.housekeeper)
            self.logger.info("Signed on to: %s FW: %s.%s.%s, HW: %s", dap_info['product'],
                                 dap_info['firmware_major'],
                                 dap_info['firmware_minor'],
                                 dap_info['build'], dap_info['hardware_rev'])

    def _sign_off(self) -> None:
        """
        End the housekeeping session
        """
        if self.housekeeper is not None:
            self.housekeeper.end_session()

    def _target_voltage(self) -> float:
        """
        Target supply in volt
        """
        if self.housekeeper is None:
            raise FatalError("Housekeeping module not initialized")
        return float(read_target_voltage(self.housekeeper))

    def _configure_session(self) -> None:
        """
        Session parameters and device description
        """
        self.device.avr.setup_debug_session(kbps=self.kbps,
                                                clkprg=self.clkprg,
                                                clkdeb=self.clkdeb,
                                                timers_run=self.timers_run)
        self.logger.info("Session configuration communicated to tool")
        self.device.avr.setup_config(self.device_info)
        self.logger.info("Device configuration communicated to tool")

    def _attach_and_stop(self) -> None:
        """
        Attach to the OCD and stop the core
        """
        try:
            self.device.avr.attach()
            self.stop()
        except Jtagice3ResponseError as e:
            self.logger.debug("Could not attach and stop MCU")
            if e.code == Avr8Protocol.AVR8_FAILURE_ILLEGAL_OCD_STATUS: # we need to set OCDEN
                raise OcdNotEnabledError(str(e)) from e
            if e.code == Avr8Protocol.AVR8_FAILURE_OCD_LOCKED: # Chip is locked and needs to be unlocked
                raise OcdLockedError(str(e)) from e
            raise e

    def _erase_locked_chip(self) -> None:
        """
        Erase a locked chip (UPDI only)
        """
        self._complain_if_no_lockbits_permission()
        self.device.avr.deactivate_physical()
        self.logger.info("Physical interface deactivated")
        self.device.avr.protocol.set_byte(Avr8Protocol.AVR8_CTXT_OPTIONS,
                                        Avr8Protocol.AVR8_OPT_CHIP_ERASE_TO_ENTER, 1)
        self.logger.info("Chip-erase key entry mechanism activated")
        self._activate_interface()
        self.device.avr.enter_progmode()
        self.switch_to_debmode()
        time.sleep(0.5) # needed for an attiny 1607
        self.logger.info("Switched to debug mode")
        if self.args.load == 'n': # if noinitialload is active, change to readbeforewrite
            self.args.load = 'r'

    def _clear_all_breakpoints(self) -> None:
        """
        Software breakpoints in the probe, then the hardware breakpoints
        """
        self.device.avr.protocol.software_breakpoint_clear_all()
        self.device.avr.breakpoint_clear()

    def _debugwire_disable(self) -> None:
        """
        Leave debugWIRE mode
        """
        self.device.avr.protocol.debugwire_disable()

    def _detach(self) -> None:
        """
        Detach from the OCD
        """
        self.device.avr.protocol.detach()

    def _deactivate_interface(self) -> None:
        """
        Deactivate the physical interface
        """
        self.device.avr.deactivate_physical()

    def _leave_progmode(self) -> None:
        """
        Leave programming mode
        """
        self.device.avr.protocol.leave_progmode()

    def _ocd_erase(self) -> None:
        """
        Chip erase in programming mode
        """
        self.device.erase()

    def _go(self) -> None:
        """
        Execute, after removing pending events
        """
        self.flush_events() # remove any pending poll events from queue
        self._pc_written = False
        AvrDebugger.run(self)

    def _go_to(self, address : int) -> None:
        """
        Execute up to address, after removing pending events
        """
        self.flush_events() # remove any pending poll events from queue
        self._pc_written = False
        AvrDebugger.run_to(self, address)

    def _single_step(self) -> None:
        """
        One step, after removing pending events
        """
        self.flush_events() # remove any pending poll events from queue
        if not self._step_off_written_pc_bp():
            AvrDebugger.step(self)
        self._pc_written = False

    def _step_off_written_pc_bp(self) -> bool:
        """
        On UPDI, a step does not get off a software breakpoint if the PC was written onto it:
        the OCD executes the BREAK instead of the original instruction, and the step after that
        lands in the middle of an instruction (measured with nEDBG, mEDBG and SNAP on ATtiny3227,
        ATmega4809 and ATmega4808). After a real hit, the probe steps over its BREAK correctly. So,
        in exactly this case, remove the breakpoint, step, and set it again; the probe plants it
        at the next run. Returns True if the step has been made here.
        """
        if self._iface != 'updi' or not self._pc_written:
            return False
        address : int = AvrDebugger.program_counter_read(self) << 1
        if address not in self._swbps:
            return False
        self.logger.debug("PC was written onto the software breakpoint at 0x%X: step without it", address)
        AvrDebugger.software_breakpoint_clear(self, address)
        AvrDebugger.step(self)
        AvrDebugger.software_breakpoint_set(self, address)
        return True

    def _regfile_read_raw(self) -> bytearray:
        """
        r0..r31 from the target
        """
        return self.device.avr.regfile_read()

    def _regfile_write_raw(self, regs : bytes) -> None:
        """
        r0..r31 to the target
        """
        self.device.avr.regfile_write(regs)

    def _pc_read_raw(self) -> int:
        """
        PC (word address) as the OCD reports it
        """
        return AvrDebugger.program_counter_read(self)

    def _spi(self) -> NvmAccessProviderCmsisDapSpi:
        """
        The SPI programming module, which must have been opened
        """
        if self.spidevice is None:
            raise FatalError("SPI module not initialized")
        return self.spidevice

    def _isp_open(self) -> None:
        """
        Connect to the SPI programming module, which enters programming mode
        """
        self.spidevice = NvmAccessProviderCmsisDapSpi(self.transport, self.device_info)

    def _isp_enter(self) -> None:
        """
        Enter ISP programming mode
        """
        self._spi().isp.enter_progmode()

    def _isp_leave(self) -> None:
        """
        Leave ISP programming mode
        """
        self._spi().isp.leave_progmode()

    def _isp_device_id(self) -> int:
        """
        Signature through ISP
        """
        return int.from_bytes(self._spi().read_device_id(),byteorder='little')

    def _isp_read_fuse(self, addr : int) -> bytes:
        """
        One fuse byte through ISP
        """
        return self._spi().isp.read_fuse_byte(addr)

    def _isp_write_fuse(self, addr : int, data : bytearray) -> None:
        """
        One fuse byte through ISP
        """
        self._spi().isp.write_fuse_byte(addr, data)

    def _isp_read_lock(self) -> bytes:
        """
        Lock byte through ISP
        """
        return self._spi().isp.read_lockbits()

    def _isp_erase(self) -> None:
        """
        Chip erase through ISP (what NvmAccessProviderCmsisDapSpi.erase does as well)
        """
        self._spi().isp.erase()

    def _isp_write_flash(self, address : int, data : bytes) -> None:
        """
        Program flash through ISP
        """
        if self.memory_info is None:
            raise FatalError("No memory info")
        self._spi().write(self.memory_info.memory_info_by_name('flash'), address, data)

    ######## The OCD

    def _activate_interface(self, graceful : bool = False) -> int:
        """
        Activate physical interface (perhaps trying twice)

        """

        try:
            use_reset : bool = 'edbg' not in self.transport.device.product_string.lower() and \
              not self.args.attach
            dev_id : bytes = self.device.avr.protocol.activate_physical(use_reset=use_reset)
            dev_code : int = (dev_id[3]<<24) + (dev_id[2]<<16) + (dev_id[1]<<8) + dev_id[0]
            self.logger.info("Physical interface activated: 0x%X", dev_code)
        except Jtagice3ResponseError as error:
            # The debugger could be out of sync with the target, retry
            if error.code == Avr8Protocol.AVR8_FAILURE_INVALID_PHYSICAL_STATE:
                self.logger.warning("Physical state out of sync. Retrying.")
                self.device.avr.deactivate_physical()
                self.logger.info("Physical interface deactivated")
                dev_id = self.device.avr.protocol.activate_physical(use_reset=use_reset)
                dev_code = (dev_id[3]<<24) + (dev_id[2]<<16) + (dev_id[1]<<8) + dev_id[0]
                self.logger.info("Physical interface activated. MCU id=0x%X", dev_code)
            elif error.code == Avr8Protocol.AVR8_FAILURE_DW_PHY_ERROR:
                if graceful:
                    raise FatalError("debugWIRE could not be activated") from error
                raise FatalError("debugWIRE not activated by power-cycling. Parasitic power supply?") \
                  from error
            elif error.code == Avr8Protocol.AVR8_FAILURE_CLOCK_ERROR:
                self.logger.warning("Communication clock failure. Retrying.")
                dev_id = self.device.avr.protocol.activate_physical(use_reset=use_reset)
                dev_code = (dev_id[3]<<24) + (dev_id[2]<<16) + (dev_id[1]<<8) + dev_id[0]
                self.logger.info("Physical interface activated. MCU id=0x%X", dev_code)
            else:
                raise error
        except KeyError as e:
            if str(e) == "4":
                self.logger.critical("Target not connected")
                raise EndOfSession("Terminating...") from e
            self.logger.error("KeyError: %s", str(e))
            raise e
        except Exception as e:
            self.logger.error("%s", str(e))
            raise e
        return dev_code

    def switch_to_debmode(self) -> bool:
        """
        Switch to debugging mode
        """
        return self.device.avr.switch_to_debmode()

    def switch_to_progmode(self) -> bool:
        """
        Switch to programming mode
        """
        return self.device.avr.switch_to_progmode()

    def software_breakpoint_set(self, address : int) -> bool:
        """
        This is a version of setting a software breakpoint that
        catches exceptions.
        """
        try:
            AvrDebugger.software_breakpoint_set(self, address)
        except Exception as e:
            self.logger.error("Could not set software breakpoint: %s", str(e))
            return False
        self._swbps.add(address)
        return True

    #pylint: disable=arguments-differ
    #we actually need two arguments when more than one HWBP is there
    def hardware_breakpoint_set(self, ix : int, address : int) -> bytes | None:
        """
        Set a hardware breakpoint at address
        """
        return self.device.avr.hardware_breakpoint_set(ix, address | self.bad_pc_bit_mask)

    #pylint: disable=arguments-differ
    #we actually need the extra argument when more than one HWBP is there
    def hardware_breakpoint_clear(self, ix : int) -> bytes | None:
        """
        Clear the ix-th hardware breakpoint
        """
        return self.device.avr.hardware_breakpoint_clear(ix)

    def stack_pointer_write(self, data : bytes) -> None:
        """
        Writes the stack pointer

        :param data: 2 bytes representing stackpointer in little endian
        :type: bytearray
        """
        self.logger.debug("Writing stack pointer")
        self.device.avr.stack_pointer_write(data)

    def status_register_read(self) -> bytearray:
        """
        Reads the status register from the AVR

        :return: 8-bit SREG value
        :rytpe: one byte
        """
        self.logger.debug("Reading status register")
        return self.device.avr.statreg_read()

    def status_register_write(self, data : bytes) -> None:
        """
        Writes new value to status register
        :param data: SREG
        :type: one byte
        """

        self.logger.debug("Write status register: %s", data)
        self.device.avr.statreg_write(data)

    def reset(self) -> None:
        """
        Reset the AVR core.
        The PC will point to the first instruction to be executed.
        """
        self.logger.info("MCU reset")
        self.device.avr.protocol.reset()
        self._wait_for_break()
        self._pc_written = False


    def reactivate(self) -> None:
        """
        Reactivate debugger (and set timer flag)
        """
        self.device.avr.reactivate()
        self.reset()

######## Memory read/write

    def read_fuse(self, addr : int, size : int) -> bytearray:
        """
        Read fuses (does not work with debugWIRE and in JTAG only when programming mode)
        """
        return self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_FUSES, addr, size)

    def write_fuse(self, addr : int, data : bytes) -> bytearray | None:
        """
        Write fuses (does not work with debugWIRE and in JTAG only in programming mode)
        """
        return self.device.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, addr, data)

    def read_lock(self, addr : int, size : int) -> bytearray:
        """
        Read lock bits (does not work with debugWIRE and in JTAG only when in programming mode)
        """
        return self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, addr, size)

    def write_lock(self, addr : int , data : bytes) -> bytearray | None:
        """
        Write lock bits (does not work with debugWIRE and in JTAG only in programming mode)
        """
        return self.device.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, addr, data)

    def read_sig(self, addr : int, size : int) -> bytearray:
        """
        Read signature in a liberal way, i.e., throwing no errors
        """
        resp = self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_SIGNATURE, 0, 3)
        if size+addr > 3:
            resp += [0xFF]*(addr+size)
        return bytearray(resp[addr:addr+size])

    def _flash_read(self, address : int, numbytes : int, prog_mode : bool = False) -> bytearray:
        """
        Read flash content from the AVR
        """
        self.logger.debug("Reading %d bytes from flash at %X", numbytes, address)
        # The debugger protocols (via pymcuprog) use memory-types with zero-offsets
        # However the address used here is already zero-offset, so no compensation is done here
        if self.memory_info is None:
            raise FatalError("No memory info available")
        return self.device.read(self.memory_info.memory_info_by_name('flash'),
                                    address, numbytes, prog_mode=prog_mode)

    def usig_read(self, address : int, numbytes : int, prog_mode : bool=False) -> bytes:
        """
        Read contents of user signature (does not work with debugWIRE)
        """
        self.logger.debug("Reading %d bytes from USER_ROW at 0x%X", numbytes, address)
        if self.memory_info is None:
            raise FatalError("No memory info available")
        return self.device.read(self.memory_info.memory_info_by_name('user_row'), address,
                                        numbytes, prog_mode)


    def usig_write(self, address : int, data : bytes, prog_mode : bool=False) -> str | None:
        """
        Write user signature (does not work with debugWIRE)
        """
        self.logger.debug("Writing %d bytes to USER_ROW at 0x%X", len(data), address)
        if self.memory_info is None:
            raise FatalError("No memory info available")
        result : str | None = self.device.write(
                                         self.memory_info.memory_info_by_name('user_row'),
                                         address,
                                         data, prog_mode)
        time.sleep(0.07) # 0.02 is strictly necessary, let's be conservative ...
        return result


    def eeprom_read(self, address : int, numbytes : int, prog_mode : bool=False) -> bytes:
        """
        Read EEPROM content from the AVR
        Needs to be handled here because depending on programm_mode, different memtypes have to be used
        """
        self.logger.debug("Reading %d bytes from EEPROM at 0x%X", numbytes, address)
        if self.memory_info is None:
            raise FatalError("No memory info available")
        return self.device.read(self.memory_info.memory_info_by_name('eeprom'), address,
                                        numbytes, prog_mode)

    def eeprom_write(self, address : int , data : bytes, prog_mode : bool=False) -> None:
        """
        Write EEPROM content to the AVR
        Needs to be handled here because depending on programm_mode, different memtypes have to be used
        """
        self.logger.debug("Writing %d bytes to EEPROM at 0x%X", len(data), address)
        if self.memory_info is None:
            raise FatalError("No memory info available")
        return self.device.write(self.memory_info.memory_info_by_name('eeprom'), address,
                                         data, prog_mode)

######## Methods required by DebugBackend

    def is_set_up(self) -> bool:
        """
        True if an NVM provider (and therefore a target) has been set up
        """
        return getattr(self, 'device', None) is not None

    def get_toolname(self) -> str:
        """
        Product string of the probe
        """
        return str(self.transport.device.product_string)

    def guard_transactions(self) -> None:
        """
        All traffic with an EDBG probe passes through the two pyedbglib methods
        that termination.guard_probe_transactions wraps
        """
        guard_probe_transactions()

    # AvrDebugger's implementations, which DebugBackend's abstract or SERVER methods
    # would hide otherwise (see the class docstring)

    def stop(self) -> None:
        """Halt execution"""
        AvrDebugger.stop(self)

    def poll_event(self) -> int | None:
        """PC (byte address) if the target has stopped since the last call, else None"""
        return AvrDebugger.poll_event(self)

    def program_counter_write(self, program_counter : int) -> None:
        """Set PC (word address), and remember that it was written"""
        AvrDebugger.program_counter_write(self, program_counter)
        self._pc_written = True

    def stack_pointer_read(self) -> bytearray:
        """SP, little endian, 2 bytes"""
        return AvrDebugger.stack_pointer_read(self)

    def sram_read(self, address : int, numbytes : int) -> bytearray:
        """Read data space"""
        return AvrDebugger.sram_read(self, address, numbytes)

    def sram_write(self, address : int, data : bytes) -> None:
        """Write data space"""
        AvrDebugger.sram_write(self, address, data)

    def software_breakpoint_clear(self, address : int) -> None:
        """The probe removes the BREAK"""
        AvrDebugger.software_breakpoint_clear(self, address)
        self._swbps.discard(address)

    def software_breakpoint_clear_all(self) -> None:
        """The probe removes all BREAKs"""
        AvrDebugger.software_breakpoint_clear_all(self)
        self._swbps.clear()

    # flash programming, used by memory.py

    def erase_chip(self, prog_mode : bool) -> None:
        """
        Erase the whole chip
        """
        self.device.erase_chip(prog_mode)

    def erase_flash_page(self, address : int, prog_mode : bool) -> bool:
        """
        Erase the flash page at address if necessary; True if erased
        """
        if self.memory_info is None:
            raise FatalError("No memory info available")
        return self.device.erase_page(address, self.memory_info.memory_info_by_name('flash'), prog_mode)

    def write_flash_pages(self, address : int, data : bytes, prog_mode : bool) -> None:
        """
        Program a multi page starting at address
        """
        if self.memory_info is None:
            raise FatalError("No memory info available")
        self.device.avr.write_memory_section(self.flashmemtype, address, data,
                                                 self.memory_info.memory_info_by_name('flash')['page_size'],
                                                 allow_blank_skip=False)

    # optional capabilities

    def can_set_run_timers(self) -> bool:
        """
        All EDBG probes can let the timers run or freeze them while stopped
        """
        return True

    def set_run_timers(self, run : bool) -> None:
        """
        Let the timers run (True) or freeze them (False) while stopped; takes effect
        after reactivate()
        """
        self.device.avr.protocol.set_byte(Avr8Protocol.AVR8_CTXT_OPTIONS,
                                              Avr8Protocol.AVR8_OPT_RUN_TIMERS, int(run))

    def can_switch_target_power(self) -> bool:
        """
        Target power is switched through the EDBG protocol
        """
        return self.edbg_protocol is not None

    def set_target_power(self, on : bool) -> None:
        """
        Switch the target supply
        """
        if self.edbg_protocol is None:
            raise FatalError("EDBG protocol not initialized")
        self.edbg_protocol.set_byte(EdbgProtocol.EDBG_CTXT_CONTROL,
                                        EdbgProtocol.EDBG_CONTROL_TARGET_POWER, int(on))

    def can_power_cycle(self) -> bool:
        """
        mEDBG are the only ones it will work with, I believe. I tried to use a try/except
        construction, but this confuses the debugger and it is stuck in an illegal state
        (the housekeeper does not respond)
        """
        return str(self.transport.device.product_string).lower().startswith('medbg')

def _translate_errors(method : Callable[..., Any]) -> Callable[..., Any]:
    """
    Turn the pymcuprog/pyedbglib exceptions that the upper layers tell apart into
    backend exceptions (design rule 2 of backend.py). Everything else passes unchanged,
    so that the upper layers treat it as before.
    """
    @functools.wraps(method)
    def wrapper(*args : Any, **kwargs : Any) -> Any:
        try:
            return method(*args, **kwargs)
        except AvrIspProtocolError as e:
            raise IspConnectionError(str(e)) from e
        except Jtagice3ResponseError as e:
            if e.code == Avr8Protocol.AVR8_FAILURE_INVALID_ADDRESS:
                raise InvalidAddressError(str(e)) from e
            raise
        except PymcuprogNotSupportedError as e:
            raise BackendNotSupportedError(str(e)) from e
        except PymcuprogError as e:
            raise BackendError(str(e)) from e
    return wrapper

# wrap every method of the interface, nothing else
for _name in [ n for n, v in vars(DebugBackend).items() if callable(v) and not n.startswith('_') ]:
    setattr(EdbgBackend, _name, _translate_errors(getattr(EdbgBackend, _name)))
