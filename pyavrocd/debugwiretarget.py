"""
This module is responsible for connecting and disconnecting to and from an debugWIRE target.
"""
#pylint: disable=trailing-newlines, consider-using-f-string
# args, logging
from logging import getLogger


# utilities
import time

# debugger modules
from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pymcuprog.nvmspi import NvmAccessProviderCmsisDapSpi
from pymcuprog.utils import read_target_voltage
from pymcuprog.pymcuprog_errors import PymcuprogError

from pyavrocd.errors import  FatalError
from pyavrocd.deviceinfo.devices.alldevices import dev_name

class DebugWIRE():
    """
    This class takes care of attaching to and detaching from a debugWIRE target, which is a bit
    complicated. The target is either in ISP or debugWIRE mode and the transition from ISP to
    debugWIRE involves power-cycling the target, which one would not like to do every time
    connecting to the target. Further, if one does this transition, it is necessary to restart
    the debugging tool by a housekeeping end_session/start_session sequence.
    """
    def __init__(self, dbg, devicename):
        self.dbg = dbg
        self.spidevice = None
        self._devicename = devicename
        self.logger = getLogger('DebugWIRE')

    def warm_start(self, graceful=True):
        """
        Try to establish a connection to the debugWIRE OCD. If not possible
        (because we are still in ISP mode) and graceful=True, the function returns false,
        otherwise true. If not graceful, an exception is thrown when we are
        unsuccessul in establishing the connection.
        """
        if graceful:
            self.logger.info("debugWIRE warm start")
        try:
            self.dbg.setup_session(self._devicename)
            idbytes = self.dbg.device.read_device_id()
            sig = (0x1E<<16) + (idbytes[1]<<8) + idbytes[0]
            self.logger.debug("Device signature by debugWIRE: %X", sig)
            self.dbg.start_debugging()
            self.dbg.reset()
        except FatalError:
            raise
        except Exception as e: # pylint: disable=broad-exception-caught
            if graceful:
                self.logger.debug("Graceful exception: %s",e)
                self.logger.info("Warm start was unsuccessful")
                return False  # we will try to connect later
            raise
        # Check device signature
        self.logger.debug("Device signature expected: %X", self.dbg.device_info['device_id'])
        if sig != self.dbg.device_info['device_id']:
            # Some funny special cases of chips pretending to be someone else
            # when in debugWIRE mode
            if (
                # pretends to be a 88P, but is 88
                (not (sig == 0x1E930F and self.dbg.device_info['device_id'] == 0x1E930A)) and
                # pretends to be a 168P, but is 168
                (not (sig == 0x1E940B and self.dbg.device_info['device_id'] == 0x1E9406)) and
                # pretends to be a 328P, but is 328
                (not (sig == 0x1E950F and self.dbg.device_info['device_id'] == 0x1E9514))):
                raise FatalError("Wrong MCU: '{}', expected: '{}'".\
                                     format(dev_name[sig],
                                            dev_name[self.dbg.device_info['device_id']]))
        # read out program counter and check whether it contains stuck to 1 bits
        pc = self.dbg.program_counter_read()
        self.logger.debug("PC(word)=%X",pc)
        if pc << 1 > self.dbg.memory_info.memory_info_by_name('flash')['size']:
            raise FatalError("Program counter of MCU has stuck-at-1-bits")
        # disable running timers while stopped
        self.dbg.device.avr.protocol.set_byte(Avr8Protocol.AVR8_CTXT_OPTIONS,
                                                  Avr8Protocol.AVR8_OPT_RUN_TIMERS,
                                                  0)
        return True

    def cold_start(self, graceful=False, callback=None, allow_erase=True):
        """
        On the assumption that we are in ISP mode, first DWEN is programmed,
        then a power-cycle is performed and finally, we enter debugWIRE mode.
        If graceful is True, we allow for a failed attempt to connect to
        the ISP core assuming that we are already in debugWIRE mode. If
        callback is Null or returns False, we wait for a manual power cycle.
        Otherwise, we assume that the callback function does the job.
        """
        self.logger.info("debugWIRE cold start")
        try:
            self.enable(erase_if_locked=allow_erase)
            self.power_cycle(callback=callback)
        except (PymcuprogError, FatalError):
            raise
        except Exception as e: # pylint: disable=broad-exception-caught
            self.logger.debug("Graceful exception: %s",e)
            if not graceful:
                raise
        # end current tool session and start a new one
        self.logger.info("Restarting the debug tool before entering debugWIRE mode")
        self.dbg.housekeeper.end_session()
        self.dbg.housekeeper.start_session()
        # now start the debugWIRE session
        return self.warm_start(graceful=False)


    def power_cycle(self, callback=None):
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
        self.dbg.housekeeper.end_session() # might be necessary after an unsuccessful power-cycle
        self.dbg.housekeeper.start_session()
        while time.monotonic() - wait_start < 150:
            if time.monotonic() - last_message > 20:
                self.logger.warning("*** Please power-cycle the target system ***")
                last_message = time.monotonic()
            if read_target_voltage(self.dbg.housekeeper) < 0.5:
                wait_start = time.monotonic()
                self.logger.debug("Power-cycle recognized")
                while  read_target_voltage(self.dbg.housekeeper) < 1.5 and \
                  time.monotonic() - wait_start < 20:
                    time.sleep(0.1)
                if read_target_voltage(self.dbg.housekeeper) < 1.5:
                    raise FatalError("Timed out waiting for repowering target")
                time.sleep(1) # wait for debugWIRE system to be ready to accept connections
                return
            time.sleep(0.1)
        raise FatalError("Timed out waiting for power-cycle")

    def disable(self):
        """
        Disables debugWIRE and unprograms the DWEN fusebit. After this call,
        there is no connection to the target anymore. For this reason all critical things
        needs to be done before, such as cleaning up breakpoints.
        """
        # stop core
        self.dbg.device.avr.protocol.stop()
        # clear all breakpoints
        self.dbg.software_breakpoint_clear_all()
        # disable DW
        self.logger.info("Leaving debugWIRE mode")
        self.dbg.device.avr.protocol.debugwire_disable()
        # detach from OCD
        self.dbg.device.avr.protocol.detach()
        # De-activate physical interface
        self.dbg.device.avr.deactivate_physical()
        # it seems necessary to reset the debug tool again
        self.logger.info("Restarting the debug tool before unprogramming the DWEN fuse")
        self.dbg.housekeeper.end_session()
        self.dbg.housekeeper.start_session()
        # now open an ISP programming session again
        self.logger.info("Reconnecting in ISP mode")
        self.spidevice = NvmAccessProviderCmsisDapSpi(self.dbg.transport, self.dbg.device_info)
        self.spidevice.isp.enter_progmode()
        fuses = self.spidevice.read(self.dbg.memory_info.memory_info_by_name('fuses'), 0, 3)
        self.logger.debug("Fuses read: %X %X %X",fuses[0], fuses[1], fuses[2])
        fuses[1] |= self.dbg.device_info['dwen_mask']
        self.logger.debug("New high fuse: 0x%X", fuses[1])
        self.logger.info("Unprogramming DWEN fuse")
        self.spidevice.write(self.dbg.memory_info.memory_info_by_name('fuses'), 1,
                                         fuses[1:2])
        fuses = self.spidevice.read(self.dbg.memory_info.memory_info_by_name('fuses'), 0, 3)
        fuses = self.spidevice.read(self.dbg.memory_info.memory_info_by_name('fuses'), 0, 3)
        self.logger.debug("Fuses read after DWEN disable: %X %X %X",fuses[0], fuses[1], fuses[2])
        self.spidevice.isp.leave_progmode()

    def enable(self, erase_if_locked=True):
        """
        Enables debugWIRE mode by programming the DWEN fuse bit. If the chip is locked,
        it will be erased. Also the BOOTRST fusebit is disabled.
        Since the implementation of ISP programming is somewhat funny, a few stop/start
        sequences and double reads are necessary.
        """
        if read_target_voltage(self.dbg.housekeeper) < 1.5:
            raise FatalError("Target is not powered")
        self.logger.info("Try to connect using ISP")
        self.spidevice = NvmAccessProviderCmsisDapSpi(self.dbg.transport, self.dbg.device_info)
        device_id = int.from_bytes(self.spidevice.read_device_id(),byteorder='little')
        if self.dbg.device_info['device_id'] != device_id:
            raise FatalError("Wrong MCU: '{}', expected: '{}'".format(
                dev_name[device_id],
                dev_name[self.dbg.device_info['device_id']]))
        fuses = self.spidevice.read(self.dbg.memory_info.\
                                        memory_info_by_name('fuses'), 0, 3)
        self.logger.debug("Fuses read: %X %X %X",fuses[0], fuses[1], fuses[2])
        lockbits = self.spidevice.read(self.dbg.memory_info.\
                                           memory_info_by_name('lockbits'), 0, 1)
        self.logger.debug("Lockbits read: %X", lockbits[0])
        if lockbits[0] != 0xFF and erase_if_locked:
            self.logger.info("MCU is locked. Will be erased.")
            self.spidevice.erase()
            lockbits = self.spidevice.read(self.dbg.memory_info.\
                                               memory_info_by_name('lockbits'), 0, 1)
            self.logger.debug("Lockbits after erase: %X", lockbits[0])
        if 'bootrst_fuse' in self.dbg.device_info:
            # unprogramm bit 0 in high or extended fuse
            self.logger.info("BOOTRST fuse will be unprogrammed.")
            bfuse = self.dbg.device_info['bootrst_fuse']
            fuses[bfuse] |= 0x01
            self.spidevice.write(self.dbg.memory_info.memory_info_by_name('fuses'),
                                     bfuse, fuses[bfuse:bfuse+1])
        # program the DWEN bit
        # leaving and re-entering programming mode is necessary, otherwise write has no effect
        self.logger.info("Reentering programming mode")
        self.spidevice.isp.leave_progmode()
        self.spidevice.isp.enter_progmode()
        fuses[1] &= (0xFF & ~(self.dbg.device_info['dwen_mask']))
        self.logger.debug("New high fuse: 0x%X", fuses[1])
        self.logger.info("Programming DWEN fuse")
        self.spidevice.write(self.dbg.memory_info.memory_info_by_name('fuses'), 1, fuses[1:2])
        # needs to be done twice!
        fuses = self.spidevice.read(self.dbg.memory_info.memory_info_by_name('fuses'), 0, 3)
        fuses = self.spidevice.read(self.dbg.memory_info.memory_info_by_name('fuses'), 0, 3)
        self.logger.debug("Fuses read again: %X %X %X",fuses[0], fuses[1], fuses[2])
        self.spidevice.isp.leave_progmode()
        # in order to start a debugWIRE session, a power-cycle is now necessary, but
        # this has to be taken care of by the calling process

