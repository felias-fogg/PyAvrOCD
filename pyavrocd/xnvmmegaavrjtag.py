"""
megaAVR JTAG NVM implementation - extended
"""
from pyedbglib.protocols.jtagice3protocol import Jtagice3ResponseError
from pyedbglib.protocols.avr8protocol import Avr8Protocol

from pymcuprog.nvmmegaavrjtag import NvmAccessProviderCmsisDapMegaAvrJtag
from pymcuprog.nvm import NvmAccessProviderCmsisDapAvr
from pymcuprog.pymcuprog_errors import PymcuprogError

from pymcuprog.deviceinfo.deviceinfokeys import DeviceMemoryInfoKeys
from pymcuprog.deviceinfo.memorynames import MemoryNames

from pymcuprog import utils

from pyavrocd.xavr8target import XMegaAvrJtagTarget

# pylint: disable=consider-using-f-string
class XNvmAccessProviderCmsisDapDebugwire(NvmAccessProviderCmsisDapDebugwire):
    """
    NVM Access the JTAG way
    """
    #pylint: disable=non-parent-init-called, super-init-not-called
    #we want to set up the debug session much later
    def __init__(self, transport, device_info):
        NvmAccessProviderCmsisDapAvr.__init__(self, device_info)
        self.avr = XMegaAvrTarget(transport)
        self.avr.setup_config(device_info)

    #pylint: enable=non-parent-init-called, super-init-not-called
    def __del__(self):
        pass

    def start(self, user_interaction_callback=None):
        """
        Start (activate) session for JTAG targets

        """
        self.logger.info("megaAVR-JTAG-specific initialiser")

        try:
            self.avr.activate_physical()
        except Jtagice3ResponseError as error:
            # The debugger could be out of sync with the target, retry
            if error.code == Avr8Protocol.AVR8_FAILURE_INVALID_PHYSICAL_STATE:
                self.logger.info("Physical state out of sync.  Retrying.")
                self.avr.deactivate_physical()
                self.avr.activate_physical()
            else:
                raise
