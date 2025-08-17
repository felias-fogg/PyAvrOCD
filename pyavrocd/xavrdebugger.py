"""
Python AVR MCU debugger
"""
# utilities
import time
from logging import getLogger

#edbg library
from pyedbglib.protocols.jtagice3protocol import Jtagice3ResponseError
from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.protocols.edbgprotocol import EdbgProtocol
from pyedbglib.protocols import housekeepingprotocol

# pymcuorig library
from pymcuprog.avrdebugger import AvrDebugger
from pymcuprog.deviceinfo import deviceinfo
from pymcuprog.nvmspi import NvmAccessProviderCmsisDapSpi
from pymcuprog.pymcuprog_errors import PymcuprogToolConfigurationError,\
     PymcuprogNotSupportedError
from pymcuprog.utils import read_target_voltage


from pyavrocd.xnvmdebugwire import XNvmAccessProviderCmsisDapDebugwire
from pyavrocd.xnvmmegaavrjtag import XNvmAccessProviderCmsisDapMegaAvrJtag
from pyavrocd.xnvmupdi import XNvmAccessProviderCmsisDapUpdi
from pyavrocd.errors import FatalError
from pyavrocd.deviceinfo.devices.alldevices import dev_name

class XAvrDebugger(AvrDebugger):
    """
    AVR debugger wrapper

    :param transport: transport object to communicate through
    :type transport: object(hid_transport)
    :param devicename: MCU device name
    :type string
    :param iface debugging interface to used
    :type string
    :param use_events_for_run_stop_state: True to use HID event channel, False to polling
    :type use_events_for_run_stop_state: boolean
    """
    #pylint: disable=super-init-not-called,too-many-positional-arguments
    def __init__(self, transport, devicename, iface, manage):
        """
        We do not want to make use of the base class' init method,
        because all startup code is collected in the start_debugging method!
        """
        self.logger = getLogger(__name__)
        self.transport = transport
        self.devicename = devicename
        self.iface = iface
        self.manage = manage
        self.housekeeper = None
        self.use_events_for_run_stop_state = True # we use the polling feature!
        # Gather device info
        # moved here so that we have mem + device info before the debug process starts
        try:
            self.device_info = deviceinfo.getdeviceinfo("pyavrocd.deviceinfo.devices." + devicename)
        except ImportError:
            raise PymcuprogNotSupportedError("No device info for device: {}".format(devicename)) #pylint: disable=raise-missing-from
        if iface not in self.device_info['interface'].lower():
            raise PymcuprogToolConfigurationError("Incompatible debugging interface")

        self.architecture = self.device_info['architecture'].lower()

        # Memory info for the device
        self.memory_info = deviceinfo.DeviceMemoryInfo(self.device_info)

        # ISP interface in order to program DWEN fuse
        self.spidevice = None

        self.edbg_protocol = None
        # Edbg protcol instance, necessary to access target power control
        if transport and transport.hid_device is not None:
            self.edbg_protocol = EdbgProtocol(transport) # 
            self.logger.debug("EdbgProtcol instance created")


        # Now attach the right NVM device
        self.device = None
        if self.iface == "updi":
            self.device = XNvmAccessProviderCmsisDapUpdi(self.transport, self.device_info)
        elif self.iface == "debugwire":
            self.device = XNvmAccessProviderCmsisDapDebugwire(self.transport, self.device_info)
        elif self.iface == "jtag" and self.architecture =="avr8":
            self.device = XNvmAccessProviderCmsisDapMegaAvrJtag(self.transport, self.device_info)
        self.logger.debug("Nvm instance created")

    # Cleanup code for detaching from target
    def stop_debugging(self, graceful=True):
        """
        Stop the debug session and clean up in a safe way
        """
        self.logger.info("Terminating debugging session ...")
        try:
            # Switch to debugging mode
            self.device.avr.switch_to_debmode()
            self.logger.info("Switched to debugging mode")
            # Halt the core
            self.device.avr.protocol.stop()
            self.logger.info("AVR core stopped")
            # Remove all software breakpoints
            self.device.avr.protocol.software_breakpoint_clear_all()
            self.logger.info("All software breakpoints removed")
            # Remove all hardware  breakpoints
            self.device.avr.breakpoint_clear()
            self.logger.info("All hardware breakpoints removed")
        except Exception as e:
            if not graceful:
                self.logger.info("Error during stopping core and removing BPs: %s", e)
        try:
            # Disable OCDEN
            if 'bootrst_base' in self.device_info and 'bootrst' in self.manage:
                self.device.avr.switch_to_progmode()
                fuses = self.read_fuse(0, 3)
                self.logger.debug("Fuses read: %X %X %X",fuses[0], fuses[1], fuses[2])
                ofuse_addr = self.device_info['ocden_base']
                ofuse_mask = self.device_info['ocden_mask']
                self.write_fuse(ofuse_addr, bytearray([fuses[ofuse_addr] | ofuse_mask]))
                self.logger.info("OCDEN unprogrammed")
        except Exception as e:
            if not graceful:
                self.logger.info("Error during unprogramming OCDEN: %s", e)
        try:
            # Detach from the OCD
            self.device.avr.protocol.detach()
            self.logger.info("Detached from OCD")
        except Exception as e:
            if not graceful:
                self.logger.info("Error during detaching from OCD: %s", e)
        try:
            # De-activate physical interface
            self.device.avr.deactivate_physical()
            self.logger.info("Physical interface deactivated")
        except Exception as e:
            if not graceful:
                self.logger.info("Error during deactivating interface: %s", e)
        try:
            # Sign off device
            if self.use_events_for_run_stop_state:
                self.housekeeper.end_session()
                self.logger.info("Signed off from tool")
        except Exception as e:
            if not graceful:
                self.logger.info("Error while signing off from tool: %s", e)
        self.logger.info("... terminating debugging session done")


    def start_debugging(self, flash_data=None, warmstart=False):
        """
        Start the debug session, i.e., initialize everything and start the debug engine.
        A warm start will assume that the OCD has already been activated, and will gracefully
        fail if not. Warmstarts happen only with debugWIRE.
        """
        self.logger.info("Starting up debug session...")
        try:
            self.housekeeper = housekeepingprotocol.Jtagice3HousekeepingProtocol(self.transport)
            self.housekeeper.start_session()
            self.logger.info("Signed on to tool")
            self.device.avr.setup_debug_session()
            self.logger.info("Session configuration communicated to tool")
            self.device.avr.setup_config(self.device_info)
            self.logger.info("Device configuration communicated to tool")
            dev_id = self.activate_interface()
            self.logger.info("MCU id=0x%x", dev_id)
            if self.iface == 'jtag' and dev_id & 0xFF != 0x3F:
                raise FatalError("Not a Microchip JTAG target")
        except Exception as e:
            self.stop_debugging()
            if warmstart:
                self.logger.warning("Debug session not started: %s",e)
                self.logger.warning("Try later with 'monitor debugwire enable'")
                return False
            raise FatalError("Debug session not started: %s" % e) #pylint: disable=raise-missing-from
        self.device.avr.switch_to_progmode()
        self.logger.info("Switched to programming mode")
        self.verify_target()
        self.logger.info("Target verified")
        self.post_process_after_start()
        self.logger.info("Post processing finished")
        self.device.avr.switch_to_debmode()
        self.logger.info("Switched to debugging mode")
        self.check_stuck_at_one_pc()
        self.logger.info("Checked that there is no stuck-at-1-bit in the PC")
        self.logger.info("... debug session startup done")
        return True

    def post_process_after_start(self):
        """
        After having attached to the OCD, do a bit of post processing
        (for JTAG targets only): Clear lockbits, unprogram BOOTRST, and program OCDEN.
        We assume that we are in progmode.
        """
        if self.iface != 'jtag':
            return
        # clear lockbits if necessary
        self.handle_lockbits(self.device.avr.memory_read,
                self.device.erase)
        # unprogram BOOTRST fuse if necessary
        self.handle_bootrst(self.device.avr.memory_read,
                self.device.avr.memory_write)
        # program OCDEN
        fuses = self.read_fuse(0, 3)
        self.logger.debug("Fuses read: %X %X %X",fuses[0], fuses[1], fuses[2])
        ofuse_addr = self.device_info['ocden_base']
        ofuse_mask = self.device_info['ocden_mask']
        if fuses[ofuse_addr] & ofuse_mask == ofuse_mask: # only if OCDEN is not yet programmed
            if 'ocden' not in self.manage:
                self.logger.warning("The fuse OCDEN is not managed by pyavrocd and will therefore not be programmed.")
                self.logger.warning("In order to allow debugging, you need to program this fuse manually.")
                self.logger.warning("Or let payavrocd manage this fuse: '-m ocden'.")
                raise FatalError("Debugging is impossible because OCDEN cannot be programmed")
            newfuse = fuses[ofuse_addr] & ~ofuse_mask
            self.write_fuse(ofuse_addr, bytearray([newfuse]))
            fuses = self.read_fuse(0, 3)
            assert newfuse == fuses[ofuse_addr], "OCDEN could not be uprogrammed"
            self.logger.info("OCDEN fuse has been programmed.")
        else:
            self.logger.info("OCDEN is already programmed")

    def verify_target(self):
        """
        Check that the MCU we connected to has a signature that is compatible with the
        one given as an argument when calling the server. The prerequisite for this method is
        that the signature is readable in the mode, in which this method is called (progmode or debmode)
        """
        idbytes = self.read_sig(0,3)
        sig = (idbytes[2]) + (idbytes[1]<<8) + (idbytes[0]<<16)
        self.logger.info("Device signature expected: %X", self.device_info['device_id'])
        self.logger.info("Device signature of connected chip: %X", sig)
        if sig != self.device_info['device_id']:
            # Some funny special cases of chips pretending to be someone else
            # when in debugWIRE mode
            if (
                # pretends to be a 88P, but is 88
                (not (sig == 0x1E930F and self.device_info['device_id'] == 0x1E930A)) and
                # pretends to be a 168P, but is 168
                (not (sig == 0x1E940B and self.device_info['device_id'] == 0x1E9406)) and
                # pretends to be a 328P, but is 328
                (not (sig == 0x1E950F and self.device_info['device_id'] == 0x1E9514))):
                raise FatalError("Wrong MCU: '%s', expected: '%s'" %
                        (dev_name.get(sig,"Unknown"),
                        dev_name[self.device_info['device_id']]))

    def check_stuck_at_one_pc(self):
        """
        Check that the connected MCU does not suffer from stuck-at-1-bits in the program counter.
        There are only very few MCUs with this issue and GDB cannot deal with it at all.
        """
        time.sleep(0.5)
        self.reset()
        pc = self.program_counter_read()
        self.logger.debug("PC(word)=%X",pc)
        if pc << 1 > self.memory_info.memory_info_by_name('flash')['size']:
            raise FatalError("Program counter of MCU has stuck-at-1-bits")

    def activate_interface(self):
        """
        Activate physical interface (perhaps trying twice)

        """
        try:
            devid = self.device.avr.activate_physical()
            self.logger.info("Physical interface activated")
        except Jtagice3ResponseError as error:
            # The debugger could be out of sync with the target, retry
            if error.code == Avr8Protocol.AVR8_FAILURE_INVALID_PHYSICAL_STATE:
                self.logger.info("Physical state out of sync.  Retrying.")
                self.device.avr.deactivate_physical()
                self.logger.info("Physical interface deactivated")
                devid = self.device.avr.activate_physical()
                self.logger.info("Physical interface activated")
            else:
                raise
        return (devid[3]<<24) + (devid[2]<<16) + (devid[1]<<8) + devid[0]


    def handle_bootrst(self, read, write):
        """
        Unprogram bootrst (if permitted) for different settings (ISP amd JTAG).
        """
        if 'bootrst_base' in self.device_info:
            self.logger.info("Programming mode entered")
            fuses = read(Avr8Protocol.AVR8_MEMTYPE_FUSES, 0, 3)
            self.logger.debug("Fuses read: %X %X %X",fuses[0], fuses[1], fuses[2])
            bfuse_addr = self.device_info['bootrst_base']
            bfuse_mask = self.device_info['bootrst_mask']
            self.logger.info("BOOTRST read: 0x%X", fuses[bfuse_addr] & bfuse_mask)
            if fuses[bfuse_addr] & bfuse_mask == 0: # if BOOTRST is programmed
                if 'bootrst' not in self.manage:
                    self.logger.warning("BOOTRST is not managed by pyavrocd and will therefore not be cleared.")
                    self.logger.warning("If you do not want to start in the boot loader, clear this fuse manually.")
                    self.logger.warning("Or let payavrocd manage this fuse: '-m bootrst'.")
                else:
                    newfuse = fuses[bfuse_addr] | bfuse_mask
                    write(Avr8Protocol.AVR8_MEMTYPE_FUSES,
                              bfuse_addr, bytearray([newfuse]))
                    fuses = read(Avr8Protocol.AVR8_MEMTYPE_FUSES, 0, 3)
                    assert newfuse == fuses[bfuse_addr], "BOOTRST could not be unprogrammed"
                    self.logger.info("BOOTRST fuse has been unprogrammed.")
            else:
                self.logger.info("BOOTRST is unprogrammed")

    def handle_lockbits(self, read, erase):
        """
        Clear lockbits (if permitted) for different settings (JTAG and ISP)
        """
        self.logger.info("Programming mode entered")
        lockbits = read(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, 0, 1)
        self.logger.info("Lockbits read: 0x%X", lockbits[0])
        if lockbits[0] != 0xFF:
            if 'lockbits' in self.manage:
                self.logger.info("MCU is locked.")
                erase()
                lockbits = read(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, 0, 1)
                assert lockbits == 0xFF, "Lockbits could not be cleared"
                self.logger.info("MCU has been erased and lockbits have been cleared.")
            else:
                self.logger.warning("pyavrocd is not allowed to clear lockbits.")
                self.logger.warning("This must be done manually by erasing the chip.")
                self.logger.warning("Alternatively, let pyavrocd manage it: '-m lockbits'")
                raise FatalError("Debugging is impossible when lockbits are set.")
        else:
            self.logger.info("MCU is not locked.")

            
    def prepare_debugging(self, callback=None):
        """
        A function that prepares for starting a debug session. The only use case is
        for the debugWIRE interface, where we need to program the DWEN fuse using ISP.

        On the assumption that we are in ISP mode, the lockbits are cleared (if allowed),
        the BOOTRST fuse is unprogrammed (is allowed), and then DWEN is programmed.
        After that, a power-cycle is performed and finally, we enter debugWIRE mode.
        If callback is Null or returns False, we wait for a manual power cycle.
        Otherwise, we assume that the callback function does the job.
        """
        if self.iface != 'debugwire':
            return
        self.logger.info("Prepare for debugWIRE debugging...")
        try:
            if read_target_voltage(self.housekeeper) < 1.5:
                raise FatalError("Target is not powered")
            self.housekeeper.start_session() # need to start a new session after reading target voltage
            self.logger.info("Signed on to tool")
            self.spidevice = NvmAccessProviderCmsisDapSpi(self.transport, self.device_info)
            self.logger.info("Connected to SPI programming module")
            self.spidevice.isp.enter_progmode()
            self.logger.info("Switched to SPI programming mode")
            device_id = int.from_bytes(self.spidevice.read_device_id(),byteorder='little')
            if self.device_info['device_id'] != device_id:
                raise FatalError("Wrong MCU: '%s' (Sig: %x), expected: '%s (Sig: %x)'" %
                        (dev_name.get(device_id,"Unknown"),
                        device_id,
                        dev_name[self.device_info['device_id']],
                        self.device_info['device_id']))
            self.spidevice.isp.leave_progmode()
            self.spidevice.isp.enter_progmode()
            self.logger.info("Restarted SPI programming mode")
            self.handle_lockbits(self.spidevice.read, self.spidevice.write)
            self.handle_bootrst(self.spidevice.read, self.spidevice.erase)
            # program the DWEN bit
            # leaving and re-entering programming mode is necessary, otherwise write has no effect
            dwen_addr = self.device_info['dwen_base']
            dwen_mask = self.device_info['dwen_mask']
            self.spidevice.isp.leave_progmode()
            self.spidevice.isp.enter_progmode()
            self.logger.info("Restarted SPI programming mode")
            self.spidevice.read(Avr8Protocol.AVR8_MEMTYPE_FUSES, 0, 3)
            self.logger.info("DWEN fuse read: 0x%x", fuses[dwen_addr] & dwen_mask)
            if fuses[dwen_addr] & dwen_mask != 0: # DWEN is not programmed!
                if 'dwen' not in self.manage:
                    self.logger.warning("The DWEN fuse is not managed by pyavrocd and will therefore not be programmed.")
                    self.logger.warning("In order to allow debugging, you need to program this fuse manually.")
                    self.logger.warning("Or let payavrocd manage this fuse: '-m dwen'.")
                    raise FatalError("Debugging is impossible when DWEN is not programmed.")
                newfuse = fuses[dwen_addr] & (0xFF & ~(dwen_mask))
                self.logger.debug("New DWEN fuse: 0x%X", newfuse)
                self.spidevice.write(Avr8Protocol.AVR8_MEMTYPE_FUSES, dwen_addr, bytearray([newfuse]))
                # reading needs to be done twice!
                fuses = self.spidevice.read(Avr8Protocol.AVR8_MEMTYPE_FUSES, 0, 3)
                fuses = self.spidevice.read(Avr8Protocol.AVR8_MEMTYPE_FUSES, 0, 3)
                self.logger.debug("Fuses read again: %X %X %X",fuses[0], fuses[1], fuses[2])
                assert fuses[dwen_addr] & dwen_mask != 0, "DWEN fuse could not be programmed"
                self.logger.info("DWEN fuse has been programmed")
            self.spidevice.isp.leave_progmode()
            self.logger.info("SPI programming terminated")
            # now you need to power-cycle
            self._power_cycle(callback=callback)
            # end current tool session and start a new one
        finally:
            try:
                self.spidevice.isp.leave_progmode()
            except Exception:
                pass
            self.housekeeper.end_session()
            self.logger.info("Signed off from tool")
            self.logger.info("... preparation for debugWIRE debugging done")

    def _power_cycle(self, callback=None):
        """
        Ask user for power-cycle and wait for voltage to come up again.
        If callback is callable, we try that first. It might magically
        perform a power cycle.
        """
        wait_start = time.monotonic()
        last_message = 0
        magic = False
        if callback:
            magic = callback()
        if magic: # callback has done all the work
            return
        self.logger.info("Restarting the debug tool before power-cycling")
        self.housekeeper.end_session() # might be necessary after an unsuccessful power-cycle
        self.logger.info("Signed off from tool")
        while time.monotonic() - wait_start < 150:
            if time.monotonic() - last_message > 20:
                self.logger.warning("*** Please power-cycle the target system ***")
                last_message = time.monotonic()
            if read_target_voltage(self.housekeeper) < 0.5:
                wait_start = time.monotonic()
                self.logger.debug("Power-cycle recognized")
                while  read_target_voltage(self.housekeeper) < 1.5 and \
                  time.monotonic() - wait_start < 20:
                    time.sleep(0.1)
                if read_target_voltage(self.housekeeper) < 1.5:
                    raise FatalError("Timed out waiting for repowering target")
                time.sleep(1) # wait for debugWIRE system to be ready to accept connections
                self.housekeeper.start_session()
                self.logger.info("Signed on to tool again")
                return
            time.sleep(0.1)
        raise FatalError("Timed out waiting for power-cycle")

    def dw_disable(self):
        """
        Disables debugWIRE and unprograms the DWEN fusebit. After this call,
        there is no connection to the target anymore. For this reason all critical things
        needs to be done before, such as cleaning up breakpoints.
        """
        # stop core
        self.logger.info("Disabling debugWIRE mode...")
        self.device.avr.protocol.stop()
        self.logger.info("AVR core stopped")
        # clear all breakpoints
        self.software_breakpoint_clear_all()
        self.logger.info("All software breakpoints removed")
        # disable DW
        self.device.avr.protocol.debugwire_disable()
        self.logger.info("DebugWIRE mode disabled")
        # stop all debugging activities
        self.device.avr.protocol.detach()
        self.logger.info("Detached from OCD")
        self.device.avr.deactivate_physical()
        self.logger.info("Physical interface deactivated")
        self.housekeeper.end_session()
        self.logger.info("Signed off from tool")
        if 'dwen' in self.manage:
            self.logger.warning("Cannot unprogram DWEN since this fuse is not managed by pyavrocd")
            self.logger.warning("Unprogram this fuse before switching the power of the MCU off")
        else:
            # start housekeeping again
            self.housekeeper.start_session()
            self.logger.info("Signed on to tool again")
            # now open an ISP programming session again
            self.logger.info("Reconnecting in ISP mode")
            self.spidevice = NvmAccessProviderCmsisDapSpi(self.transport, self.device_info)
            self.spidevice.isp.enter_progmode()
            self.logger.info("Entered programming mode")
            dwen_addr = self.device_info['dwen_base']
            dwen_mask = self.device_info['dwen_mask']
            fuses = self.spidevice.read(Avr8Protocol.AVR8_MEMTYPE_FUSES, 0, 3)
            self.logger.debug("Fuses read: %X %X %X",fuses[0], fuses[1], fuses[2])
            fuses[dwen_addr] |= dwen_mask
            self.logger.debug("New high fuse: 0x%X", fuses[dwen_addr])
            self.spidevice.write(Avr8Protocol.AVR8_MEMTYPE_FUSES, dwen_addr,
                                     fuses[dwen_addr:dwen_addr+1])
            self.logger.info("Unprogrammed DWEN fuse")
            fuses = self.spidevice.read(Avr8Protocol.AVR8_MEMTYPE_FUSES, 0, 3)
            fuses = self.spidevice.read(Avr8Protocol.AVR8_MEMTYPE_FUSES, 0, 3)
            self.logger.debug("Fuses read after DWEN disable: %X %X %X",fuses[0], fuses[1], fuses[2])
            assert fuses[dwen_addr] & dwen_mask != 0, "DWEN fuse could not be unprogrammed"
        self.spidevice.isp.leave_progmode()
        self.logger.info("Programming mode terminated")
        # we do not interact with the tool anymore after this
        self.housekeeper.end_session()
        self.logger.info("Signed off from tool")
        self.logger.info("... disabling debugWIRE mode done")


    def stack_pointer_write(self, data):
        """
        Writes the stack pointer

        :param data: 2 bytes representing stackpointer in little endian
        :type: bytearray
        """
        self.logger.debug("Writing stack pointer")
        self.device.avr.stack_pointer_write(data)

    def status_register_read(self):
        """
        Reads the status register from the AVR

        :return: 8-bit SREG value
        :rytpe: one byte
        """
        self.logger.debug("Reading status register")
        return self.device.avr.statreg_read()

    def status_register_write(self, data):
        """
        Writes new value to status register
        :param data: SREG
        :type: one byte
        """

        self.logger.debug("Write status register: %s", data)
        self.device.avr.statreg_write(data)

    def register_file_read(self):
        """
        Reads out the AVR register file (R0::R31)

        :return: 32 bytes of register file content as bytearray
        :rtype: bytearray
        """
        self.logger.debug("Reading register file")
        return self.device.avr.regfile_read()

    def register_file_write(self, regs):
        """
        Writes the AVR register file (R0::R31)

        :param data: 32 byte register file content as bytearray
        :raises ValueError: if 32 bytes are not given
        """
        self.logger.debug("Writing register file")
        self.device.avr.regfile_write(regs)

    def reset(self):
        """
        Reset the AVR core.
        The PC will point to the first instruction to be executed.
        """
        self.logger.info("MCU reset")
        self.device.avr.protocol.reset()
        self._wait_for_break()

    def read_fuse(self, addr, size):
        """
        Read fuses (does not work with debugWIRE and in JTAG only when programming mode)
        """
        return self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_FUSES, addr, size)

    def write_fuse(self, addr, data):
        """
        Write fuses (does not work with debugWIRE and in JTAG only in programming mode)
        """
        return self.device.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, addr, data)

    def read_lock(self, addr, size):
        """
        Read lock bits (does not work with debugWIRE and in JTAG only when programming mode)
        """
        return self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, addr, size)

    def write_lock(self, addr, data):
        """
        Write lock bits (does not work with debugWIRE and in JTAG only in programming mode)
        """
        return self.device.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, addr, data)

    def read_sig(self, addr, size):
        """
        Read signature in a liberal way, i.e., throwing no errors
        """
        resp = self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_SIGNATURE, 0, 3)
        if size+addr > 3:
            resp += [0xFF]*(addr+size)
        return bytearray(resp[addr:addr+size])

    def read_usig(self, addr, size):
        """
        Read contents of user signature (does not work with debugWIRE)
        """
        return self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_USER_SIGNATURE, addr, size)

    def write_usig(self, addr, data):
        """
        Write user signature
        """
        return self.device.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_USER_SIGNATURE, addr, data)

    def flash_read(self, address, numbytes, prog_mode=False):
        """
        Read flash content from the AVR

        :param address: absolute address to start reading from
        :param numbytes: number of bytes to read
        :param prog_mode: optinal, when False, FLASH_SPM is chosen, otherwise FLASH_PAGE
        """
        self.logger.debug("Reading %d bytes from flash at %X", numbytes, address)
        # The debugger protocols (via pymcuprog) use memory-types with zero-offsets
        # However the address used here is already zero-offset, so no compensation is done here
        return self.device.read(self.memory_info.memory_info_by_name('flash'),
                                    address, numbytes, prog_mode=prog_mode)

