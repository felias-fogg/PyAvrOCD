"""
The test suit for the Jtag1Backend class (JTAGICE mkI)
"""
#pylint: disable=protected-access,missing-function-docstring,missing-class-docstring
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from pyavrocd import jtag1
from pyavrocd.backend import ProbeCandidate, BackendError, BackendNotSupportedError
from pyavrocd.jtag1backend import Jtag1Backend, jtag_clock_code, supported_part, discover, TOOL
from pyavrocd.errors import FatalError
from pyavrocd.main import options
from pyavrocd.monitor import MonitorCommand

CANDIDATE = ProbeCandidate(tool=TOOL, product='JTAGICE mkI', address='/dev/cu.usbserial-23210')


def backend(device='atmega16', iface='jtag'):
    with patch('pyavrocd.session.logging.getLogger', MagicMock()):
        b = Jtag1Backend(CANDIDATE, device, iface, options(['-d', device]))
    b.protocol = MagicMock()
    b.protocol.poll_break.return_value = None    # no break messages pending
    return b


class TestJtag1Backend(TestCase):

    def test_parts(self):
        self.assertTrue(supported_part('atmega16'))
        self.assertTrue(supported_part('ATmega169A'))
        self.assertFalse(supported_part('atmega169p'))      # works, but not documented for the mkI
        self.assertFalse(supported_part('atmega324p'))
        with self.assertRaises(BackendNotSupportedError):
            backend('atmega324p')
        with self.assertRaises(BackendError):
            backend('atmega16', 'debugwire')

    def test_hardware_breakpoints_only(self):
        b = backend()
        self.assertEqual(b.get_hwbpnum(), 4)
        self.assertFalse(b.software_breakpoint_set(0x100))

    def test_jtag_clock_codes(self):
        self.assertEqual(jtag_clock_code(1000), (0xFF, 1000))
        self.assertEqual(jtag_clock_code(300), (0xFD, 250))
        self.assertEqual(jtag_clock_code(50), (0xFB, 125))   # the minimum

    def test_one_breakpoint_on_psb0(self):
        b = backend()
        b.hardware_breakpoint_set(1, 0x100)
        b._go()
        b.protocol.set_program_breakpoint.assert_called_once_with(0, 0x80)
        b.protocol.set_parameter.assert_not_called()
        b.protocol.go.assert_called_once()

    def test_four_breakpoints_with_cursor(self):
        b = backend()
        for ix, address in ((1, 0x200), (2, 0x300), (3, 0x400)):
            b.hardware_breakpoint_set(ix, address)
        b._go_to(0x100)
        self.assertEqual(b.protocol.set_program_breakpoint.call_args_list, [call(0, 0x80), call(1, 0x100)])
        b.protocol.set_parameter.assert_has_calls([
            call(jtag1.PAR_BREAK_ADDR1_HIGH, 0x01), call(jtag1.PAR_BREAK_ADDR1_LOW, 0x80),
            call(jtag1.PAR_BREAK_ADDR2_HIGH, 0x02), call(jtag1.PAR_BREAK_ADDR2_LOW, 0x00),
            call(jtag1.PAR_COMB_BREAK_CTRL, 0x3F)])

    def test_breakpoints_are_sent_again_and_cleared(self):
        b = backend()
        b.hardware_breakpoint_set(1, 0x100)
        b._go()
        b._go()
        self.assertEqual(b.protocol.set_program_breakpoint.call_count, 2)  # the mkI forgets them at a break
        b.hardware_breakpoint_clear(1)
        b._go()
        self.assertEqual(b.protocol.set_program_breakpoint.call_count, 2)

    def test_too_many_breakpoints(self):
        b = backend()
        for ix in (1, 2, 3, 4):
            b.hardware_breakpoint_set(ix, 0x100 * ix)
        with self.assertRaises(BackendError):
            b._go_to(0x80)

    def test_poll_event_reads_the_pc(self):
        b = backend()
        b.protocol.poll_break.return_value = None
        self.assertIsNone(b.poll_event())
        b.protocol.poll_break.return_value = 0x0020
        b.protocol.read_pc.return_value = 44
        self.assertEqual(b.poll_event(), 88)

    def test_stop_only_a_running_target(self):
        # measured: FORCED_STOP on a stopped target lets it run on by a few instructions
        b = backend()
        b.stop()                                   # state unknown at the start: counts as running
        b.stop()
        b.protocol.forced_stop.assert_called_once()
        b._go()
        b.stop()
        self.assertEqual(b.protocol.forced_stop.call_count, 2)
        b.reset()
        b.stop()
        self.assertEqual(b.protocol.forced_stop.call_count, 2)

    def test_no_polling_while_stopped(self):
        b = backend()
        b.stop()
        self.assertIsNone(b.poll_event())
        b.protocol.poll_break.assert_not_called()
        b._go()
        b.protocol.poll_break.return_value = 0x0020
        b.protocol.read_pc.return_value = 44
        self.assertEqual(b.poll_event(), 88)
        b.stop()
        b.protocol.forced_stop.assert_called_once()  # the break has stopped it already

    def test_flash_read_odd_address(self):
        b = backend()
        b.protocol.read_memory.return_value = bytes(range(4))
        self.assertEqual(b._flash_read(0x101, 2), bytearray([1, 2]))
        b.protocol.read_memory.assert_called_with(jtag1.MEMTYPE_PML, 0x80, 4)
        b._flash_read(0x100, 2, prog_mode=True)
        b.protocol.read_memory.assert_called_with(jtag1.MEMTYPE_FLASH_PAGE, 0x80, 2)

    def test_flash_write_in_pages_in_programming_mode_only(self):
        b = backend()
        b.write_flash_pages(0x100, bytes(256), prog_mode=True)
        self.assertEqual([c.args[:2] for c in b.protocol.write_memory.call_args_list],
                         [(jtag1.MEMTYPE_FLASH_PAGE, 0x80), (jtag1.MEMTYPE_FLASH_PAGE, 0xC0)])
        with self.assertRaises(FatalError):
            b.write_flash_pages(0x100, bytes(128), prog_mode=False)

    def test_no_page_erase(self):
        with self.assertRaises(FatalError):
            backend().erase_flash_page(0x100, prog_mode=True)

    def test_no_isp(self):
        with self.assertRaises(BackendNotSupportedError):
            backend()._isp_open()

    def test_release_switches_back(self):
        b = backend()
        proto = b.protocol
        transport = MagicMock()
        b.transport = transport
        b.release()
        proto.set_baud.assert_called_once_with(jtag1.START_BAUD)
        transport.close.assert_called_once()
        self.assertIsNone(b.protocol)

    def test_stack_pointer_without_sph(self):
        b = backend('atmega16')
        b.protocol.read_memory.return_value = b'\x5f\x04'
        self.assertEqual(b.stack_pointer_read(), bytearray(b'\x5f\x04'))   # the m16 has SPH

    @patch('pyavrocd.jtag1backend.list_ports.comports')
    def test_discover(self, comports):
        comports.return_value = [MagicMock(device='/dev/cu.usbserial-23210', vid=0x1A86, serial_number=None),
                                 MagicMock(device='/dev/cu.Bluetooth', vid=None, serial_number=None)]
        self.assertEqual(discover(), [ProbeCandidate(TOOL, 'JTAGICE mkI', '/dev/cu.usbserial-23210', '')])


class TestMonitorWithMkI(TestCase):

    def test_breakpoints_fixed_to_hardware(self):
        b = backend()
        mon = MonitorCommand('jtag', options(['-d', 'atmega16']), 'JTAGICE mkI', b)
        self.assertTrue(mon.is_onlyhwbps())
        self.assertEqual(mon.dispatch(['breakpoints']),
                         ("", "With this debugger, only hardware breakpoints are allowed"))
        self.assertEqual(mon.dispatch(['breakpoints', 'all']),
                         ("", "Breakpoint mode cannot be changed with this debugger"))

    def test_atmega128_keeps_its_message(self):
        b = backend('atmega128')
        mon = MonitorCommand('jtag', options(['-d', 'atmega128']), 'JTAGICE mkI', b)
        self.assertEqual(mon.dispatch(['breakpoints']),
                         ("", "On this MCU, only hardware breakpoints are allowed"))
