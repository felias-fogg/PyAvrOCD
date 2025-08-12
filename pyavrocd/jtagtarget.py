"""
This module is responsible for connecting and disconnecting to and from a JTAG target.
"""
# args, logging

from logging import getLogger

from pyedbglib.protocols.avr8protocol import Avr8Protocol

from pyavrocd.errors import  FatalError
from pyavrocd.deviceinfo.devices.alldevices import dev_name

class JTAG():
    """
    This class  makes sure that all the right fuses are set for a JTAG target.
    """

    def __init__(self, dbg, mem, devicename):
        self.dbg = dbg
        self.mem = mem
        self._devicename = devicename
        self.logger = getLogger("pyavrocd.jtag")

    def start(self):
        """
        This is the setup procedure for JTAG
        """
        self.logger.info("Initializing JTAG interface")
        try:
            self.dbg.setup_session(self._devicename)
            self.dbg.start_debugging()
            self.dbg.reset()
            self.dbg.device.avr.protocol.enter_progmode()
            self.mem.programming_mode = True
            self.logger.info("Programming mode entered")
            idbytes = self.mem.sig_read(0,3)
            sig = (idbytes[2]) + (idbytes[1]<<8) + (idbytes[0]<<16)
            self.logger.info("Device signature of chip: %X", sig)
            self.dbg.device.avr.protocol.leave_progmode()
            self.mem.programming_mode = False
            self.logger.info("Programming mode stopped")
        except Exception as e:
            self.logger.critical("Could not connect to JTAG target: %s", e)
            return False
        # Check device signature
        self.logger.debug("Device signature expected: %X", self.dbg.device_info['device_id'])
        if sig != self.dbg.device_info['device_id']:
            raise FatalError("Wrong MCU: '{}', expected: '{}'".\
                                     format(dev_name.get(sig,"Unknown"),
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

