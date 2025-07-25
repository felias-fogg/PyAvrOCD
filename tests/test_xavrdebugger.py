"""
The test suit for the XAvrDebugger class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
from unittest.mock import MagicMock, patch
from unittest import TestCase

from pyedbglib.protocols.avr8protocol import Avr8Protocol

from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.xavr8target import XTinyAvrTarget

class TestXAvrDebugger(TestCase):

    @patch('pyavrocd.xavrdebugger.AvrDebugger.__init__',MagicMock())
    def setUp(self):
        mock_transport = MagicMock()
        self.xa = XAvrDebugger(mock_transport, "attiny85")
        self.xa.logger = MagicMock()
        self.xa.transport = mock_transport
        self.xa.housekeeper = MagicMock()
        self.xa.use_events_for_run_stop_state = True

    @patch('pyavrocd.xavrdebugger.XNvmAccessProviderCmsisDapDebugwire', MagicMock())
    def test_setup_session(self):
        self.xa.setup_session("attiny85")
        self.xa.device.avr.setup_debug_session.assert_called_once()

    def test_start_debugging(self):
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock()
        self.xa.device.avr.protocol = MagicMock(spec=Avr8Protocol)
        self.xa.device.avr.protocol.poll_events.return_value=True
        self.xa.device.avr.protocol.decode_break_event.return_value = 42
        self.xa.start_debugging()
        self.xa.device.start.assert_called_once()
        self.xa.device.avr.protocol.attach.assert_called_once()

    def test_stack_pointer_write(self):
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        self.xa.stack_pointer_write(b'\x34\x12')
        self.xa.device.avr.stack_pointer_write.assert_called_with(b'\x34\x12')

    def test_stack_pointer_read(self):
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        self.xa.device.avr.stack_pointer_read.return_value = b'\x34\x12'
        self.assertEqual(self.xa.stack_pointer_read(), b'\x34\x12')

    def test_status_register_write(self):
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        self.xa.status_register_write(b'\x12')
        self.xa.device.avr.statreg_write.assert_called_with(b'\x12')

    def test_status_register_read(self):
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        self.xa.device.avr.statreg_read.return_value = b'\x34'
        self.assertEqual(self.xa.status_register_read(),b'\x34')
        self.xa.device.avr.statreg_read.assert_called_once()

    def test_register_file_write(self):
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        rfile = bytearray(list(range(32)))
        self.xa.register_file_write(rfile)
        self.xa.device.regfile_write(rfile)

    def test_register_file_read(self):
        self.xa.device = MagicMock()
        self.xa.device.avr = MagicMock(spec=XTinyAvrTarget)
        rfile = bytearray(list(range(32)))
        self.xa.device.avr.regfile_read.return_value=rfile
        self.assertEqual(self.xa.register_file_read(),rfile)
        self.xa.device.avr.regfile_read.assert_called_once()
