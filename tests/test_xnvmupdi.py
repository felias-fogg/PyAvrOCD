"""
The test suit for the XNvmAccessProviderCmsisDapDebugwire class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
import logging
from unittest.mock import Mock, MagicMock, patch, create_autospec #, call
from unittest import TestCase

from pymcuprog.deviceinfo import deviceinfo

#from pyedbglib.protocols.avr8protocol import Avr8Protocol

from pyavrocd.xnvmupdi import XNvmAccessProviderCmsisDapUpdi
from pyavrocd.xavr8target import XTinyXAvrTarget
from pyavrocd.deviceinfo.devices.atmega4809 import DEVICE_INFO

logging.basicConfig(level=logging.DEBUG)

class TestXNvmAccessProviderCmsisDapDebugwire(TestCase):

    @patch('pyavrocd.xnvmdebugwire.XTinyAvrTarget',MagicMock())
    def setUp(self):
        self.nvm = XNvmAccessProviderCmsisDapUpdi(MagicMock(), DEVICE_INFO, manage=None)
        self.nvm.avr = create_autospec(XTinyXAvrTarget)
        self.device_info = deviceinfo.getdeviceinfo("pyavrocd.deviceinfo.devices." + "atmega4809")
        self.memory_info = deviceinfo.DeviceMemoryInfo(self.device_info)
        self.nvm.logger_local.info = Mock()

    def test_init(self):
        self.assertTrue(self.nvm.avr is not None)
