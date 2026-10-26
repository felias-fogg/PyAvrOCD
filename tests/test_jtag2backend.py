"""
The test suit for the Jtag2Backend class (JTAGICE mkII and AVR Dragon)
"""
#pylint: disable=protected-access,missing-function-docstring,missing-class-docstring
from unittest import TestCase
from unittest.mock import MagicMock, patch, create_autospec

import usb.core

from pyavrocd import jtag2
from pyavrocd.backend import ProbeCandidate
from pyavrocd.jtag2backend import Jtag2Backend
from pyavrocd.errors import FatalError
from pyavrocd.main import options
from pyavrocd.handler import GdbHandler
from pyavrocd.monitor import MonitorCommand
from pyavrocd.breakexec import BreakAndExec
from tests.test_jtag2 import FakeTransport

class TestJtag2Backend(TestCase):

    def setUp(self):
        with patch('pyavrocd.session.logging.getLogger', MagicMock()):
            self.backend = Jtag2Backend(ProbeCandidate(tool='dragon', product='AVRDRAGON', address='0860'),
                                        'atmega328p', 'debugwire', options(['-d', 'atmega328p']))

    @patch('pyavrocd.jtag2backend.jtag2.Jtag2Protocol')
    @patch('pyavrocd.jtag2backend.jtag2.Jtag2UsbTransport.open')
    def test_sign_on_reopens_after_timeout(self, mock_open, mock_protocol):
        # after a power cycle of the target, the Dragon does not answer the first command
        first, second = MagicMock(), MagicMock()
        first.sign_on.side_effect = jtag2.Jtag2UsbTimeout("No response")
        second.sign_on.return_value = MagicMock(master_firmware=(0x27, 7))
        mock_protocol.side_effect = [first, second]
        self.backend._sign_on()
        self.assertEqual(mock_open.call_count, 2)
        mock_open.return_value.close.assert_called_once()
        self.assertIs(self.backend.protocol, second)
        self.assertIs(self.backend.sign_on_info, second.sign_on.return_value)

    @patch('pyavrocd.jtag2backend.jtag2.Jtag2Protocol')
    @patch('pyavrocd.jtag2backend.jtag2.Jtag2UsbTransport.open')
    def test_sign_on_without_reopen(self, mock_open, mock_protocol):
        self.backend._sign_on()
        mock_open.assert_called_once()
        mock_protocol.return_value.sign_on.assert_called_once()

    def test_close_forgets_the_isp_session(self):
        self.backend.transport = MagicMock()
        self.backend.transport.close.side_effect = usb.core.USBError("gone")
        self.backend.protocol = MagicMock()
        self.backend._isp = jtag2.Jtag2Isp(self.backend.protocol)
        self.backend._close()
        self.assertIsNone(self.backend.transport)
        self.assertIsNone(self.backend.protocol)
        self.assertIsNone(self.backend._isp)


class TestPendingRemovals(TestCase):
    """The probe removes cleared SW BPs only at the next go or step (measured on dW and JTAG)"""

    def make(self, iface='debugwire', device='atmega328p'):
        with patch('pyavrocd.session.logging.getLogger', MagicMock()):
            backend = Jtag2Backend(ProbeCandidate(tool='dragon', product='AVRDRAGON', address='0860'),
                                   device, iface, options(['-d', device]))
        backend.protocol = MagicMock()
        page = backend.device_info['flash_page_size_bytes']
        flash = bytearray(page)
        flash[0x100 % page:0x100 % page + 2] = b"\xc9\xf7"      # the original word 0xF7C9
        backend.protocol.read_memory.side_effect = lambda _memtype, _base, size: bytes(flash[:size])
        backend.flash = flash
        return backend

    def planted_and_cleared(self, backend):
        def unfiltered(*_):    # after CLR_BREAK the probe stops filtering, the BREAK stays
            backend.flash[0x100 % len(backend.flash):0x100 % len(backend.flash) + 2] = b"\x98\x95"
        backend.protocol.clr_break.side_effect = unfiltered
        backend.software_breakpoint_set(0x100)
        backend._go()
        backend.software_breakpoint_clear(0x100)

    def test_cleared_breakpoint_reads_as_original(self):
        backend = self.make()
        self.planted_and_cleared(backend)
        self.assertEqual(backend._pending_removals, {0x100: 0xF7C9})
        self.assertEqual(bytes(backend._flash_read(0x100, 2)), b"\xc9\xf7")

    def test_cleared_before_any_go_is_not_pending(self):
        backend = self.make()
        backend.software_breakpoint_set(0x100)
        backend.software_breakpoint_clear(0x100)
        self.assertEqual(backend._pending_removals, {})
        backend.protocol.read_memory.assert_not_called()

    def test_go_and_step_end_pending_removals(self):
        backend = self.make()
        self.planted_and_cleared(backend)
        backend._single_step()
        self.assertEqual(backend._pending_removals, {})
        backend.protocol.restore_target.assert_not_called()

    def test_write_on_debugwire_restores_target_first(self):
        backend = self.make()
        self.planted_and_cleared(backend)
        backend.software_breakpoint_set(0x200)          # still set: has to be set again afterwards
        backend.protocol.reset_mock()
        backend.write_flash_pages(0, bytes(len(backend.flash)), True)
        names = [c[0] for c in backend.protocol.method_calls]
        self.assertLess(names.index('restore_target'), names.index('write_memory'))
        backend.protocol.set_break.assert_called_once_with(0, 0x100)    # 0x200 as word address
        self.assertEqual(backend._pending_removals, {})

    def test_write_without_pending_removals(self):
        backend = self.make()
        backend.write_flash_pages(0, bytes(len(backend.flash)), True)
        backend.protocol.restore_target.assert_not_called()

    def test_jtag_restores_target_before_progmode(self):
        backend = self.make('jtag', 'atmega324p')
        self.planted_and_cleared(backend)
        backend.protocol.reset_mock()
        backend.switch_to_progmode()
        names = [c[0] for c in backend.protocol.method_calls]
        self.assertLess(names.index('restore_target'), names.index('enter_progmode'))
        backend.protocol.reset_mock()
        backend.write_flash_pages(0, bytes(len(backend.flash)), True)   # in progmode: nothing more
        backend.protocol.restore_target.assert_not_called()


class TestUsbErrorsReachGdb(TestCase):
    """A USB error inside a monitor command is reported to GDB, not turned into a stop packet"""

    @patch('pyavrocd.handler.logging.getLogger', MagicMock())
    def test_monitor_reset_with_lost_response(self):
        with patch('pyavrocd.session.logging.getLogger', MagicMock()):
            backend = Jtag2Backend(ProbeCandidate(tool='dragon', product='AVRDRAGON', address='0860'),
                                   'atmega328p', 'debugwire', options(['-d', 'atmega328p']))
        backend.protocol = jtag2.Jtag2Protocol(FakeTransport([]))     # every response is lost
        sock = MagicMock()
        handler = GdbHandler(sock, backend, "atmega328p", options(['-d', 'atmega328p']), "Tool")
        handler.mon = create_autospec(MonitorCommand, specSet=True, instance=True)
        handler.mon.dispatch.return_value = ('reset', 'Bla')
        handler.mon.is_debugger_active.return_value = True
        handler.bp = create_autospec(BreakAndExec, specSet=True, instance=True)
        handler.dispatch('qRcmd', b',7265736574')                   # monitor reset
        reply = sock.sendall.call_args[0][0].decode()
        text = bytes.fromhex(reply[1:reply.index('#')]).decode()
        self.assertTrue(text.startswith("Fatal error: No response to command 0x"), text)
        self.assertEqual(handler.critical, text[len("Fatal error: "):].strip())


class TestDeviceData(TestCase):
    """debugWIRE, 4-page part, firmware 7: the device context (0x36) for the page buffers, then the descriptor"""

    def entered(self, firmware, device='attiny1634'):
        with patch('pyavrocd.session.logging.getLogger', MagicMock()):
            backend = Jtag2Backend(ProbeCandidate(tool='jtagice2', product='JTAGICEmkII', address='0700'),
                                   device, 'debugwire', options(['-d', device]))
        backend.sign_on_info = MagicMock(master_firmware=firmware)
        backend.protocol = MagicMock()
        backend._target_voltage = MagicMock(return_value=5.0)
        backend._debugwire_active = MagicMock(return_value=True)
        backend._enter_mode()
        return backend.protocol

    def test_firmware_7_sends_the_context_then_the_descriptor(self):
        proto = self.entered((7, 0x27))
        self.assertEqual(proto.set_device_context.call_args[0][0][0][1][20], 4)   # page buffers per flash block
        names = [c[0] for c in proto.method_calls if c[0] in ('set_device_context', 'set_device_descriptor')]
        self.assertEqual(names, ['set_device_context', 'set_device_descriptor'])  # the descriptor last

    def test_firmware_6_refuses_4_page_parts(self):
        with self.assertRaises(FatalError) as caught:
            self.entered((6, 0x0B))
        self.assertIn("Firmware 6.0B", str(caught.exception))

    def test_firmware_6_sends_the_descriptor_to_others(self):
        proto = self.entered((6, 0x0B), 'atmega328p')
        proto.set_device_descriptor.assert_called_once()
        proto.set_device_context.assert_not_called()

    def test_one_page_parts_keep_the_descriptor(self):
        proto = self.entered((7, 0x27), 'atmega328p')
        proto.set_device_descriptor.assert_called_once()
        proto.set_device_context.assert_not_called()
