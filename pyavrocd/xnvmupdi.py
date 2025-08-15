"""
UPDI NVM implementation - extended
"""
#Implementation is only a stub:
#pylint: disable=unused-import
from logging import getLogger

from pyedbglib.protocols.jtagice3protocol import Jtagice3ResponseError
from pyedbglib.protocols.avr8protocol import Avr8Protocol

from pymcuprog.nvmupdi import NvmAccessProviderCmsisDapUpdi
from pymcuprog.nvm import NvmAccessProviderCmsisDapAvr
from pymcuprog.pymcuprog_errors import PymcuprogError

from pymcuprog.deviceinfo.deviceinfokeys import DeviceMemoryInfoKeys
from pymcuprog.deviceinfo.memorynames import MemoryNames

from pymcuprog import utils

from pyavrocd.xavr8target import XTinyXAvrTarget

class XNvmAccessProviderCmsisDapUpdi(NvmAccessProviderCmsisDapUpdi):
    """
    NVM Access the DW way
    """
    #pylint: disable=non-parent-init-called, super-init-not-called
    #we want to set up the debug session much later
    def __init__(self, transport, device_info):
        self.logger_local = getLogger('pyavrocd.nvmupdi')
        NvmAccessProviderCmsisDapAvr.__init__(self, device_info)
        self.avr = XTinyXAvrTarget(transport)
        self.logger_local.debug("Setting up device info ...")
        self.avr.setup_config(device_info)
        self.logger_local.debug("... setup done")

    def __del__(self):
        pass
