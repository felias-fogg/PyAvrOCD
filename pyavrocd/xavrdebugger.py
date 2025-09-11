"""
Python AVR MCU debugger
"""
# utilities
import time
from logging import getLogger

#edbg library
from pyedbglib.protocols.jtagice3protocol import Jtagice3ResponseError
from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.protocols.avrispprotocol import AvrIspProtocol #pylint: disable=unused-import
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
    def __init__(self, transport, devicename, iface, manage, clkprg, clkdeb):
        """
        We do not want to make use of the base class' init method,
        because all startup code is collected in the start_debugging method!
        """
        self.logger = getLogger(__name__)
        self.transport = transport
        self.devicename = devicename
        self.iface = iface
        self.manage = manage
        self.clkprg = clkprg
        self.clkdeb = clkdeb
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
        # Edbg protocol instance, necessary to access target power control
        if transport and transport.hid_device is not None:
            self.edbg_protocol = EdbgProtocol(transport)
            self.logger.debug("EdbgProtcol instance created")

        # Now attach the right NVM device
        self.device = None
        if self.iface == "updi":
            self.device = XNvmAccessProviderCmsisDapUpdi(self.transport, self.device_info)
        elif self.iface == "debugwire":
            self.device = XNvmAccessProviderCmsisDapDebugwire(self.transport, self.device_info)
        elif self.iface == "jtag" and self.architecture =="avr8":
            self.device = XNvmAccessProviderCmsisDapMegaAvrJtag(self.transport, self.device_info)
        self.logger.info("Nvm instance created")


    def start_debugging(self, flash_data=None, warmstart=False):
        """
        Start the debug session, i.e., initialize everything and start the debug engine.
        A warm start will assume that the OCD has already been activated, and will gracefully
        fail if not. Warmstarts happen only with debugWIRE.
        """
        _dummy = flash_data
        self.logger.info("Starting up debug session...")
        try:
            self.housekeeper = housekeepingprotocol.Jtagice3HousekeepingProtocol(self.transport)
            self.housekeeper.start_session()
            self.logger.info("Signed on to tool")
            self.device.avr.setup_debug_session(clkprg=self.clkprg, clkdeb=self.clkdeb)
            self.logger.info("Session configuration communicated to tool")
            self.device.avr.setup_config(self.device_info)
            self.logger.info("Device configuration communicated to tool")
            dev_id = self._activate_interface()
            if self.iface == 'jtag' and dev_id & 0xFF != 0x3F:
                raise FatalError("Not a Microchip JTAG target")
        except Exception as e:
            if warmstart:
                self.logger.warning("Debug session not started: %s",e)
                self.logger.warning("Try later with 'monitor debugwire enable'")
                return False
            raise FatalError("Debug session not started: %s" % e) #pylint: disable=raise-missing-from
        self.device.avr.attach()
        self.device.avr.switch_to_progmode()
        self.logger.info("Switched to programming mode")
        self._verify_target(dev_id)
        self._post_process_after_start()
        self.logger.info("Post processing finished")
        self.device.avr.switch_to_debmode()
        self.logger.info("Switched to debugging mode")
        self._check_stuck_at_one_pc()
        self.logger.info("Checked for dirty PC")
        self.logger.info("... debug session startup done")
        return True

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
            if 'ocden_base' in self.device_info and 'ocden' in self.manage:
                self.device.avr.switch_to_progmode()
                self.logger.info("Switched to programming mode")
                fuses = self.read_fuse(0, 3)
                self.logger.debug("Fuses read: %X %X %X",fuses[0], fuses[1], fuses[2])
                ofuse_addr = self.device_info['ocden_base']
                ofuse_mask = self.device_info['ocden_mask']
                self.write_fuse(ofuse_addr, bytearray([fuses[ofuse_addr] | ofuse_mask]))
                self.logger.info("OCDEN unprogrammed")
        except Exception as e:
            if not graceful:
                self.logger.error("Error during unprogramming OCDEN: %s", e)
        try:
            # Detach from the OCD
            self.device.avr.protocol.detach()
            self.logger.info("Detached from OCD")
        except Exception as e:
            if not graceful:
                self.logger.error("Error during detaching from OCD: %s", e)
        try:
            # De-activate physical interface
            self.device.avr.deactivate_physical()
            self.logger.info("Physical interface deactivated")
        except Exception as e:
            if not graceful:
                self.logger.error("Error during deactivating interface: %s", e)
        try:
            # Sign off device
            if self.use_events_for_run_stop_state:
                self.housekeeper.end_session()
                self.logger.info("Signed off from tool")
        except Exception as e:
            if not graceful:
                self.logger.info("Error while signing off from tool: %s", e)
        self.logger.info("... terminating debugging session done")

    def _post_process_after_start(self):
        """
        After having attached to the OCD, do a bit of post processing
        (for JTAG targets only): Clear lockbits, unprogram BOOTRST, and program OCDEN.
        We assume that we are in progmode.
        """
        if self.iface != 'jtag':
            return
        # clear lockbits if necessary
        self._handle_lockbits(self.read_lock_one_byte,
                self.device.erase)
        # unprogram BOOTRST fuse if necessary
        self._handle_bootrst(self.read_fuse_one_byte,
                self.write_fuse)
        # program OCDEN
        ofuse_addr = self.device_info['ocden_base']
        ofuse_mask = self.device_info['ocden_mask']
        ofuse = self.read_fuse_one_byte(ofuse_addr)
        self.logger.info("OCDEN read: 0x%X", ofuse[0] & ofuse_mask)
        if ofuse[0] & ofuse_mask == ofuse_mask: # only if OCDEN is not yet programmed
            if 'ocden' not in self.manage:
                self.logger.warning("The fuse OCDEN is not managed by pyavrocd and will therefore not be programmed.")
                self.logger.warning("In order to allow debugging, you need to program this fuse manually.")
                self.logger.warning("Or let payavrocd manage this fuse: '-m ocden'.")
                raise FatalError("Debugging is impossible because OCDEN cannot be programmed")
            newfuse = ofuse[0] & ~ofuse_mask &0xFF
            self.write_fuse(ofuse_addr, bytearray([newfuse]))
            assert newfuse == self.read_fuse_one_byte(ofuse_addr)[0], "OCDEN could not be programmed"
            self.logger.info("OCDEN fuse has been programmed.")
        else:
            self.logger.info("OCDEN is already programmed")

    def _verify_target(self, dev_id):
        """
        Check that the MCU we connected to has a signature that is compatible with the
        one given as an argument when calling the server. The prerequisite for this method is
        that the signature is readable in the mode, in which this method is called (progmode or debmode)
        """
        idbytes = self.read_sig(0,3)
        if self.iface == 'debugwire':
            sig = (0x1E<<16)+dev_id # The id returned from activate_physical
        else:
            sig = (idbytes[2]) + (idbytes[1]<<8) + (idbytes[0]<<16)
        self.logger.info("Device signature expected: %X", self.device_info['device_id'])
        self.logger.info("Device signature of connected chip: %X", sig)
        if sig != self.device_info['device_id']:
            # Some funny special cases of chips pretending to be someone else
            # when in debugWIRE mode
            if (
                # pretends to be a 48P, but is 48
                (not (sig == 0x1E920A and self.device_info['device_id'] == 0x1E9205)) and
                # pretends to be a 88P, but is 88
                (not (sig == 0x1E930F and self.device_info['device_id'] == 0x1E930A)) and
                # pretends to be a 168P, but is 168
                (not (sig == 0x1E940B and self.device_info['device_id'] == 0x1E9406)) and
                # pretends to be a 328P, but is 328
                (not (sig == 0x1E950F and self.device_info['device_id'] == 0x1E9514))):
                raise FatalError("Wrong MCU: '%s', expected: '%s'" %
                        (dev_name.get(sig,"Unknown"),
                        dev_name[self.device_info['device_id']]))

    def _check_stuck_at_one_pc(self):
        """
        Check that the connected MCU does not suffer from stuck-at-1-bits in the program counter.
        There are only very few MCUs with this issue and GDB cannot deal with it at all. Since for the
        MCUs with debugWIRE OCD  (ATmega48, ATmega88), this also lead to other issues,
        we try to terminate debugWIRE mode immediately and then initiate a shutdown sequence.
        For some JTAG MCUs (ATmega16), the debuggers apparently mask out the stuck bit, but
        the stuck bits show when the return address is pushed on the stack.
        """
        self.reset()
        pc = self.program_counter_read()
        self.logger.debug("PC(word)=%X",pc)
        if pc << 1 >= self.memory_info.memory_info_by_name('flash')['size']:
            if self.iface == 'debugwire':
                self.device.avr.protocol.debugwire_disable()
            raise FatalError("MCU cannot be debugged because of stuck-at-1 bit in the PC")
        # special purpose check for ATmega16 (and we try it also for fun an ATmega32)
        if self.device_info['device_id'] in [ 0x1E9403, 0x1E9502 ]:
            self._check_atmega16()

    def _check_atmega16(self):
        """
        Single out the ATmega16 without an A-suffix. In theory that should be possible
        via the revision code present in the JTAG id code. However, unfortunately,
        the data sheets are not conclusive. For this reason, we use the test of
        setting the stack pointer, raising an interrupt, making a single step,
        and then examine the stack.
        """
        self.logger.debug("Check ATmega16 for dirty PC")
        sp = self.memory_info.memory_info_by_name('internal_sram')['size'] + \
          self.memory_info.memory_info_by_name('internal_sram')['address'] - 1
        self.logger.debug("New stack pointer: 0x%X", sp)
        # set stack pointer to top of SRAM
        self.stack_pointer_write(sp.to_bytes(2,byteorder='little'))
        # set INT0 to low level static interrupt
        self.sram_write(0x55, bytearray([0x00]))
        # enable INT0 in GICR
        self.sram_write(0x5B, bytearray([0x40]))
        # enable interrupts in SREG
        self.status_register_write(bytearray([0x80]))
        # set DDR PD2 bit
        self.sram_write(0x31, bytearray([0x04]))
        # now set PD2 = LOW, IRQs are raised now
        self.sram_write(0x32, bytearray([0x00]))
        # make a single step (at 0, instruction does not matter!)
        self.step()
        # PC is pushed to stack
        sp -= 2
        if sp != int.from_bytes(self.stack_pointer_read(),byteorder='little'):
            self.logger.error("IRQ has not been raised!")
            self.reset()
            return
        # now check return address
        retpc = int.from_bytes(self.sram_read(sp+1, 2), byteorder='big')
        self.logger.debug("Return address: 0x%X", retpc)
        if retpc << 1 > self.memory_info.memory_info_by_name('flash')['size']:
            raise FatalError("MCU cannot be debugged because of stuck-at-1 bit in the PC")
        self.reset()

    def _activate_interface(self):
        """
        Activate physical interface (perhaps trying twice)

        """
        try:
            dev_id = self.device.avr.activate_physical()
            dev_code = (dev_id[3]<<24) + (dev_id[2]<<16) + (dev_id[1]<<8) + dev_id[0]
            self.logger.info("Physical interface activated: 0x%X", dev_code)
        except Jtagice3ResponseError as error:
            # The debugger could be out of sync with the target, retry
            if error.code == Avr8Protocol.AVR8_FAILURE_INVALID_PHYSICAL_STATE:
                self.logger.info("Physical state out of sync.  Retrying.")
                self.device.avr.deactivate_physical()
                self.logger.info("Physical interface deactivated")
                dev_id = self.device.avr.activate_physical()
                dev_code = (dev_id[3]<<24) + (dev_id[2]<<16) + (dev_id[1]<<8) + dev_id[0]
                self.logger.info("Physical interface activated. MCU id=0x%X", dev_code)
            else:
                raise
        return dev_code


    def _handle_bootrst(self, read, write):
        """
        Unprogram bootrst (if permitted) for different settings (ISP amd JTAG).
        """
        if 'bootrst_base' in self.device_info:
            bfuse_addr = self.device_info['bootrst_base']
            bfuse_mask = self.device_info['bootrst_mask']
            bfuse = read(bfuse_addr)
            self.logger.debug("BOOTRST addr: 0x%X, mask: 0x%X", bfuse_addr,   bfuse_mask)
            self.logger.debug("BOOTRST fuse byte: 0x%X", bfuse[0])
            if bfuse[0] & bfuse_mask == 0: # if BOOTRST is programmed
                if 'bootrst' not in self.manage:
                    self.logger.warning("BOOTRST is not managed by pyavrocd and will therefore not be cleared.")
                    self.logger.warning("If you do not want to start in the boot loader, clear this fuse manually.")
                    self.logger.warning("Or let payavrocd manage this fuse: '-m bootrst'.")
                else:
                    newfuse = bfuse[0] | bfuse_mask
                    self.logger.debug("Writing new fuse byte: 0x%x", newfuse)
                    write(bfuse_addr, bytearray([newfuse]))
                    if self.iface == 'debugwire': #necessary because otherwise the read may fail
                        self.spidevice.isp.leave_progmode()
                        self.spidevice =  NvmAccessProviderCmsisDapSpi(self.transport, self.device_info)
                        self.logger.debug("Reconnected to SPI programming module")
                    bfuse = read(bfuse_addr)
                    self.logger.debug("BOOTRST fuse byte read: 0x%X", bfuse[0])
                    assert newfuse == bfuse[0], "BOOTRST could not be unprogrammed"
                    self.logger.info("BOOTRST fuse has been unprogrammed.")
            else:
                self.logger.info("BOOTRST was already unprogrammed")

    def _handle_lockbits(self, read, erase):
        """
        Clear lockbits (if permitted) for different settings (JTAG and ISP)
        """
        lockbits = read()
        self.logger.debug("Lockbits read: 0x%X", lockbits[0])
        if lockbits[0] != 0xFF:
            if 'lockbits' in self.manage:
                self.logger.info("MCU is locked.")
                erase()
                lockbits = read()
                self.logger.debug("Lockbits after write: 0x%X", lockbits[0])
                assert lockbits[0] == 0xFF, "Lockbits could not be cleared"
                self.logger.info("MCU has been erased and lockbits have been cleared.")
            else:
                self.logger.warning("pyavrocd is not allowed to clear lockbits.")
                self.logger.warning("This must be done manually by erasing the chip.")
                self.logger.warning("Alternatively, let pyavrocd manage it: '-m lockbits'")
                raise FatalError("Debugging is impossible when lockbits are set.")
        else:
            self.logger.info("MCU is not locked.")


    def prepare_debugging(self, callback=None, recognition=None):
        """
        A function that prepares for starting a debug session. The only use case is
        for the debugWIRE interface, where we need to program the DWEN fuse using ISP.

        On the assumption that we are in ISP mode, the lockbits are cleared (if allowed),
        the BOOTRST fuse is unprogrammed (if allowed), and then DWEN is programmed (if allowed).
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
            device_id = int.from_bytes(self.spidevice.read_device_id(),byteorder='little')
            if self.device_info['device_id'] != device_id:
                raise FatalError("Wrong MCU: '%s' (Sig: %x), expected: '%s (Sig: %x)'" %
                        (dev_name.get(device_id,"Unknown"),
                        device_id,
                        dev_name[self.device_info['device_id']],
                        self.device_info['device_id']))
            self.spidevice.isp.leave_progmode()
            self.spidevice =  NvmAccessProviderCmsisDapSpi(self.transport, self.device_info)
            self.logger.debug("Reconnected to SPI programming module")
            self._handle_lockbits(self.spidevice.isp.read_lockbits, self.spidevice.erase)
            self._handle_bootrst(self.spidevice.isp.read_fuse_byte, self.spidevice.isp.write_fuse_byte)
            # program the DWEN bit
            dwen_addr = self.device_info['dwen_base']
            dwen_mask = self.device_info['dwen_mask']
            self.logger.debug("DWEN addr: 0x%X, DWEN mask: 0x%X", dwen_addr, dwen_mask)
            dwen_byte = self.spidevice.isp.read_fuse_byte(dwen_addr)
            self.logger.debug("DWEN fuse byte: 0x%X", dwen_byte[0])
            if dwen_byte[0] & dwen_mask != 0: # DWEN is not programmed!
                if 'dwen' not in self.manage:
                    self.logger.warning("The DWEN fuse is not managed by pyavrocd.")
                    self.logger.warning("Therefore, the fuse will not be programmed.")
                    self.logger.warning("In order to allow debugging, you need to program this fuse manually.")
                    self.logger.warning("Or let payavrocd manage this fuse: '-m dwen'.")
                    raise FatalError("Debugging is impossible when DWEN is not programmed.")
                if device_id in [ 0x1E9205, 0x1E930A ]:
                    self._check_atmega48_and_88(device_id)
                newfuse = dwen_byte[0] & (0xFF & ~(dwen_mask))
                self.logger.debug("New DWEN fuse: 0x%X", newfuse)
                self.logger.debug("Writing fuse byte: 0x%X", newfuse)
                self.spidevice.isp.write_fuse_byte(dwen_addr, bytearray([newfuse]))
                self.logger.info("DWEN fuse written")
            self.spidevice.isp.leave_progmode()
            self.logger.info("SPI programming terminated")
            # now you need to power-cycle
            self._power_cycle(callback=callback, recognition=recognition)
            # end current tool session and start a new one
        finally:
            try:
                self.spidevice.isp.leave_progmode()
            except Exception:
                pass
            self.housekeeper.end_session()
            self.logger.info("Signed off from tool")
            self.logger.info("... preparation for debugWIRE debugging done")

    def _check_atmega48_and_88(self, device_id):
        """
        The ATmega48 and ATmega88 (without A or P suffix) have a dirty program counter
        and in addition get semi-bricked when trying to program the DWEN fuse. Even
        avrdude cannot resurrect them (but Studio and MPLABX have no problems). The
        only way to recognize them is through looking into the boot_signature, which
        however, is not accessible by SPI programming. So, we flash a short program for
        checking the boot_signature, run the program, and check the lock bits, where
        the result will be stored.
        """
        self.logger.info("Test for dirty PC on ATmega48/88")
        # erase flash (and maybe EEPROM)
        self.spidevice.isp.erase()
        # program flash with test program, depending on MCU type
        if device_id == 0x1E9205: # ATmega48(A)
            self.spidevice.write(self.memory_info.memory_info_by_name('flash'), 0,
                    bytearray.fromhex("19C02CC02BC02AC029C028C027C026C025C024C023C022C021C020C01FC01EC0" +
                                      "1DC01CC01BC01AC019C018C017C016C015C014C011241FBECFEFD2E0DEBFCDBF" +
                                      "14BE0FB6F894A89580916000886180936000109260000FBE02D014C0D1CF81E2" +
                                      "F0E0E0E08093570084918E3141F089E09EEFE1E0F0E0092E80935700E89590E0" +
                                      "80E00895F894FFCF"))
        else:
            self.spidevice.write(self.memory_info.memory_info_by_name('flash'), 0,
                    bytearray.fromhex("19CE2CCE2BCE2ACE29CE28CE27CE26CE25CE24CE23CE22CE21CE20CE1FCE1ECE" +
                                      "1DCE1CCE1BCE1ACE19CE18CE17CE16CE15CE14CEFFFFFFFFFFFFFFFFFFFFFFFF"))
            self.spidevice.write(self.memory_info.memory_info_by_name('flash'), 0x1C30,
                    bytearray.fromhex("FFFFFFFF11241FBECFEFD4E0DEBFCDBF14BE0FB6F894A8958091600088618093" +
                                      "6000109260000FBE02D018C0D1C181E2F0E0E0E08093570084918E3141F089E0" +
                                      "9BEFE1E0F0E0092E80935700E895E4E3F0E0E491E5B990E080E00895F894FFCF"))
        self.spidevice.isp.leave_progmode()
        # now wait a couple of milliseconds
        time.sleep(0.1)
        # start programming mode again and read result
        self.spidevice.isp.enter_progmode()
        result_lockbits = self.spidevice.read(self.memory_info.memory_info_by_name('lockbits'), 0, 1)
        # check result
        self.logger.debug("Result from lockbits: 0x%X",   result_lockbits[0])
        # Now erase chip again
        self.spidevice.isp.erase()
        # and check results
        if result_lockbits[0] != 0xFF:
            raise FatalError("MCU cannot be debugged because of stuck-at-1 bit in the PC")

    def _power_cycle(self, callback=None, recognition=None):
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
                self.logger.info("Power-cycling recognized")
                if recognition:
                    recognition()
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
        if 'dwen' not in self.manage:
            self.logger.warning("Cannot unprogram DWEN since this fuse is not managed by pyavrocd")
            self.logger.warning("Unprogram this fuse before switching the power of the MCU off!")
            self.logger.warning("In order to let payavrocd manage this fuse use: '-m dwen'.")
        else:
            # start housekeeping again
            time.sleep(0.5)
            self.housekeeper = housekeepingprotocol.Jtagice3HousekeepingProtocol(self.transport)
            self.housekeeper.start_session()
            self.logger.info("Signed on to tool again")
            # now open an ISP programming session again
            self.logger.info("Reconnecting in ISP mode")
            self.spidevice = NvmAccessProviderCmsisDapSpi(self.transport, self.device_info)
            self.spidevice.isp.enter_progmode()
            self.logger.info("Entered SPI programming mode")
            dwen_addr = self.device_info['dwen_base']
            dwen_mask = self.device_info['dwen_mask']
            dwen_byte = self.spidevice.isp.read_fuse_byte(dwen_addr)
            self.logger.debug("DWEN byte: 0x%X", dwen_byte[0])
            dwen_byte[0] |= dwen_mask
            self.logger.debug("New DWEN byte: 0x%X", dwen_byte[0])
            self.spidevice.isp.write_fuse_byte(dwen_addr, dwen_byte)
            self.logger.info("Unprogrammed DWEN fuse")
            self.spidevice.isp.leave_progmode()
            self.logger.info("SPI programming terminated")
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

    def read_fuse_one_byte(self, addr):
        """
        Read fuses (does not work with debugWIRE and in JTAG only when programming mode)
        """
        return self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_FUSES, addr, 1)


    def write_fuse(self, addr, data):
        """
        Write fuses (does not work with debugWIRE and in JTAG only in programming mode)
        """
        return self.device.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, addr, data)

    def read_lock(self, addr, size):
        """
        Read lock bits (does not work with debugWIRE and in JTAG only when in programming mode)
        """
        return self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, addr, size)

    def read_lock_one_byte(self):
        """
        Read lock bits (does not work with debugWIRE and in JTAG only when in programming mode)
        """
        return self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, 0, 1)

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
        :param prog_mode: optional, when False, FLASH_SPM is chosen, otherwise FLASH_PAGE
        """
        self.logger.debug("Reading %d bytes from flash at %X", numbytes, address)
        # The debugger protocols (via pymcuprog) use memory-types with zero-offsets
        # However the address used here is already zero-offset, so no compensation is done here
        return self.device.read(self.memory_info.memory_info_by_name('flash'),
                                    address, numbytes, prog_mode=prog_mode)

