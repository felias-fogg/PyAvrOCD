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

    def test_go_waits_longer_for_breakpoints_to_plant(self):
        # measured on the ATmega2560: 0.44 s per 256-byte page at JTAG clock code 0
        with patch('pyavrocd.session.logging.getLogger', MagicMock()):
            backend = Jtag2Backend(ProbeCandidate(tool='jtagice2', product='JTAGICEmkII', address='4262'),
                                   'atmega2560', 'jtag', options(['-d', 'atmega2560']))
        proto = MagicMock()
        proto.byte_ms = jtag2.jtag_byte_ms(0)
        backend.protocol = proto
        backend._go()
        self.assertEqual(proto.go.call_args.args, (jtag2.USB_TIMEOUT,))  # nothing to plant
        backend._swbps = {0x400, 0x800, 0xC00}
        backend._planted = {0x400}
        backend._pending_removals = {0x1000: 0xFFFF}
        backend._go()                                                     # 2 to plant, 1 to remove
        timeout = proto.go.call_args.args[0]
        self.assertEqual(timeout, jtag2.USB_TIMEOUT + int(3 * 256 * 24 * jtag2.jtag_byte_ms(0)))
        self.assertGreater(timeout - jtag2.USB_TIMEOUT, 3 * 440)          # above what was measured
        self.assertEqual(backend._pending_flash_changes(), 0)             # all planted now
        backend._go_to(0x200)
        self.assertEqual(proto.run_to.call_args.args, (0x100, jtag2.USB_TIMEOUT))
        # a timeout is logged with what the probe had to do, and passed on
        backend._swbps.add(0x1400)
        proto.go.side_effect = jtag2.Jtag2UsbTimeout("No response to command 0x08 from the probe")
        with self.assertRaises(jtag2.Jtag2UsbTimeout):
            backend._go()
        message = backend.logger.error.call_args.args
        self.assertIn("software breakpoint(s) to plant or remove", message[0])
        self.assertEqual(message[1:4], ("Go", (jtag2.USB_TIMEOUT + int(256 * 24 * jtag2.jtag_byte_ms(0))) / 1000, 1))

    def test_eeprom_in_jtag_programming_mode_goes_by_whole_pages(self):
        # measured on an ATmega128: EEPROM_PAGE writes take effect only for whole aligned pages
        with patch('pyavrocd.session.logging.getLogger', MagicMock()):
            backend = Jtag2Backend(ProbeCandidate(tool='jtagice2', product='JTAGICEmkII', address='4262'),
                                   'atmega128', 'jtag', options(['-d', 'atmega128']))
        eeprom = bytearray(range(0x80, 0x98))                           # 3 pages of 8 bytes
        proto = MagicMock()
        proto.read_memory.side_effect = lambda memtype, addr, n: bytes(eeprom[addr:addr + n])
        backend.protocol = proto
        backend.eeprom_write(6, b'\x01\x02\x03\x04\x05', prog_mode=True)  # 6..10: two pages, both partial
        writes = [c.args for c in proto.write_memory.call_args_list]
        self.assertEqual([(m, a, len(d)) for m, a, d in writes],
                         [(jtag2.MEMTYPE_EEPROM_PAGE, 0, 8), (jtag2.MEMTYPE_EEPROM_PAGE, 8, 8)])
        self.assertEqual(writes[0][2], bytes(eeprom[0:6]) + b'\x01\x02')
        self.assertEqual(writes[1][2], b'\x03\x04\x05' + bytes(eeprom[11:16]))
        backend.eeprom_read(3, 4, prog_mode=True)
        self.assertEqual(proto.read_memory.call_args.args, (jtag2.MEMTYPE_EEPROM_PAGE, 3, 4))
        proto.reset_mock()
        backend.eeprom_write(6, b'\x01', prog_mode=False)              # debug mode: as before
        self.assertEqual(proto.write_memory.call_args.args, (jtag2.MEMTYPE_EEPROM, 6, b'\x01'))

    def test_chip_erase_keeps_eeprom_with_managed_eesave(self):
        # as the EDBG backend: EESAVE programmed for the erase and restored afterwards
        with patch('pyavrocd.session.logging.getLogger', MagicMock()):
            backend = Jtag2Backend(ProbeCandidate(tool='jtagice2', product='JTAGICEmkII', address='4262'),
                                   'atmega128', 'jtag', options(['-d', 'atmega128', '-m', 'eesave']))
        proto = MagicMock()
        proto.read_memory.return_value = b'\x89'                       # hfuse of the ATmega128A: EESAVE off
        backend.protocol = proto
        backend.erase_chip(prog_mode=True)
        self.assertEqual([c.args for c in proto.write_memory.call_args_list],
                         [(jtag2.MEMTYPE_FUSE, 1, b'\x81'), (jtag2.MEMTYPE_FUSE, 1, b'\x89')])
        self.assertEqual([c[0] for c in proto.mock_calls].index('chip_erase'), 2) # between the fuse writes
        proto.reset_mock()
        proto.read_memory.return_value = b'\x81'                       # EESAVE already programmed
        backend.erase_chip(prog_mode=True)
        proto.write_memory.assert_not_called()

    def test_sleeping_jtag_target_reached_with_reset_held(self):
        # measured on an ATmega16 in power-down: no JTAG ID until the reset line is held and the
        # emulator mode is set again; the reset is released once programming mode holds the MCU
        with patch('pyavrocd.session.logging.getLogger', MagicMock()):
            backend = Jtag2Backend(ProbeCandidate(tool='jtagice2', product='JTAGICEmkII', address='4262'),
                                   'atmega16', 'jtag', options(['-d', 'atmega16']))
        proto = MagicMock()
        backend.protocol = proto
        ids = iter([b'\xff\xff\xff\xff', (0x0940303F).to_bytes(4, 'little')])
        proto.get_parameter.side_effect = lambda par: (5000).to_bytes(2, 'little') \
            if par == jtag2.PAR_OCD_VTARGET else next(ids)
        self.assertEqual(backend._activate_interface(), 0x0940303F)
        resets = [c.args[1] for c in proto.set_parameter.call_args_list if c.args[0] == jtag2.PAR_EXTERNAL_RESET]
        modes = [c for c in proto.set_parameter.call_args_list if c.args[0] == jtag2.PAR_EMULATOR_MODE]
        self.assertEqual((resets, len(modes)), ([b'\x01'], 1))
        backend.switch_to_progmode()
        resets = [c.args[1] for c in proto.set_parameter.call_args_list if c.args[0] == jtag2.PAR_EXTERNAL_RESET]
        self.assertEqual(resets, [b'\x01', b'\x00'])
        backend.switch_to_progmode()                                    # released only once
        self.assertEqual(sum(c.args[0] == jtag2.PAR_EXTERNAL_RESET for c in proto.set_parameter.call_args_list), 2)

    def test_sph_masked_on_parts_with_8bit_sp(self):
        # the t2313 has no SPH; the mkII returned 0x21 there, EDBG returns 0
        self.assertNotIn(0x5E, self.backend.masked_registers)          # m328p: 16-bit SP
        with patch('pyavrocd.session.logging.getLogger', MagicMock()):
            small = Jtag2Backend(ProbeCandidate(tool='jtagice2', product='JTAGICEmkII', address='4262'),
                                 'attiny2313', 'debugwire', options(['-d', 'attiny2313']))
        self.assertIn(0x5E, small.masked_registers)
        self.assertNotIn(0x5E, small.device_info['masked_registers']) # the device info stays as generated
        sph_read_bit = (0x5E - 0x20) // 8, 1 << ((0x5E - 0x20) % 8)
        masks = jtag2.make_device_descriptor(small.device_info, small.masked_registers)[:240]
        self.assertFalse(masks[sph_read_bit[0]] & sph_read_bit[1])
        context = dict(jtag2.make_device_context(small.device_info, small.masked_registers))
        self.assertFalse(context[0x80][sph_read_bit[0]] & sph_read_bit[1])
        self.assertTrue(context[0x80][(0x5D - 0x20) // 8] & 1 << ((0x5D - 0x20) % 8))   # SPL stays readable
        # dw-link ignores the mask and delivers what the chip has at 0x5E: the high byte is dropped
        small.protocol = MagicMock()
        small.protocol.read_memory.return_value = bytes([0x23, 0x23])
        self.assertEqual(small.stack_pointer_read(), bytearray([0x23, 0x00]))
        self.backend.protocol = MagicMock()
        self.backend.protocol.read_memory.return_value = bytes([0xFF, 0x08])
        self.assertEqual(self.backend.stack_pointer_read(), bytearray([0xFF, 0x08]))   # m328p untouched

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


class TestSoftReset(TestCase):
    """PAR_SOFT_RESET (0x2D) is left at its default: with 3, the AVR Dragon hangs at the next target power cycle"""

    def make(self):
        with patch('pyavrocd.session.logging.getLogger', MagicMock()):
            backend = Jtag2Backend(ProbeCandidate(tool='dragon', product='AVRDRAGON', address='0860'),
                                   'atmega328p', 'debugwire', options(['-d', 'atmega328p']))
        backend.protocol = MagicMock()
        backend.protocol.sign_on.return_value = MagicMock(master_firmware=(7, 0x27))
        return backend

    def test_not_set_at_sign_on(self):
        backend = self.make()
        backend._sign_on()
        self.assertIsNotNone(backend.sign_on_info)
        for call in backend.protocol.set_parameter.call_args_list:
            self.assertNotEqual(call.args[0], jtag2.PAR_SOFT_RESET)


class TestRelease(TestCase):
    """At the end of the server, a real sign-off, so that the AVR Dragon resets"""

    def make(self):
        with patch('pyavrocd.session.logging.getLogger', MagicMock()):
            backend = Jtag2Backend(ProbeCandidate(tool='dragon', product='AVRDRAGON', address='0860'),
                                   'atmega328p', 'debugwire', options(['-d', 'atmega328p']))
        backend.protocol = proto = MagicMock()
        backend.transport = transport = MagicMock()
        return backend, proto, transport

    def test_signs_off_and_closes(self):
        backend, proto, transport = self.make()
        backend._mode_set = True
        backend.release()
        proto.set_parameter.assert_called_once_with(jtag2.PAR_EMULATOR_MODE,
                                                    bytes([jtag2.EMULATOR_MODE_UNKNOWN]))
        proto.sign_off.assert_called_once_with()
        transport.close.assert_called_once_with()
        self.assertIsNone(backend.protocol)

    def test_errors_are_swallowed_and_closed(self):
        backend, proto, transport = self.make()
        proto.sign_off.side_effect = jtag2.Jtag2UsbTimeout("No response to command 0x00")
        backend.release()
        transport.close.assert_called_once_with()
        self.assertIsNone(backend.protocol)

    def test_nothing_to_do_without_probe(self):
        backend, _, _ = self.make()
        backend.protocol = None
        backend.release()


DRAGON = ProbeCandidate(tool='dragon', product='AVRDRAGON', address='00A200050860')
SIGN_ON = bytes([jtag2.RSP_SIGN_ON, 1, 0xFF, 0, 0x27, 1, 0xFF, 0, 0x27, 1]) + \
  bytes.fromhex("00A200050860") + b"AVRDRAGON\0"

def closable(answers):
    fake = FakeTransport(answers)
    fake.close = MagicMock()
    return fake

class TestReboot(TestCase):
    """--reboot-debugger: sign off with PAR_SOFT_RESET 0, wait until the probe is back, sign on again"""

    @patch('pyavrocd.jtag2backend.wait_for_reenumeration', return_value=True)
    @patch('pyavrocd.jtag2backend.jtag2.Jtag2UsbTransport.open')
    def test_reboot(self, mock_open, mock_wait):
        first = closable([('same', SIGN_ON), ('same', b"\x80"), ('same', b"\x80")])
        second = closable([('same', SIGN_ON)])
        mock_open.side_effect = [first, second]
        self.assertTrue(Jtag2Backend.reboot_probe(DRAGON, MagicMock(), MagicMock()))
        self.assertEqual([body for _, body in first.sent],
                         [bytes([jtag2.CMND_GET_SIGN_ON]),
                          bytes([jtag2.CMND_SET_PARAMETER, jtag2.PAR_SOFT_RESET, jtag2.SOFT_RESET_HARD]),
                          bytes([jtag2.CMND_SIGN_OFF])])
        self.assertEqual([body for _, body in second.sent], [bytes([jtag2.CMND_GET_SIGN_ON])])
        first.close.assert_called_once()
        second.close.assert_called_once()
        mock_wait.assert_called_once()

    @patch('pyavrocd.jtag2backend.wait_for_reenumeration', return_value=False)
    @patch('pyavrocd.jtag2backend.jtag2.Jtag2UsbTransport.open')
    def test_not_back(self, mock_open, _mock_wait):
        mock_open.return_value = closable([('same', SIGN_ON), ('same', b"\x80"), ('same', b"\x80")])
        logger = MagicMock()
        self.assertFalse(Jtag2Backend.reboot_probe(DRAGON, MagicMock(), logger))
        logger.critical.assert_called_once_with("... could not reconnect")

    @patch('pyavrocd.jtag2backend.jtag2.Jtag2UsbTransport.open')
    def test_no_answer(self, mock_open):
        mock_open.return_value = closable([])
        logger = MagicMock()
        self.assertFalse(Jtag2Backend.reboot_probe(DRAGON, MagicMock(), logger))
        mock_open.return_value.close.assert_called_once()
        self.assertIn("Could not reboot", logger.critical.call_args.args[0])


class TestJtagClock(TestCase):
    """-D while debugging, -P in programming mode; only on JTAG targets"""

    def make(self, iface, args, device='atmega324p'):
        with patch('pyavrocd.session.logging.getLogger', MagicMock()):
            backend = Jtag2Backend(ProbeCandidate(tool='jtagice2', product='JTAGICE mkII', address='4262'),
                                   device, iface, options(['-d', device] + args))
        backend.protocol = MagicMock()
        return backend

    def clock_codes(self, backend):
        return [c.args[1][0] for c in backend.protocol.set_parameter.call_args_list
                if c.args[0] == jtag2.PAR_OCD_JTAG_CLK]

    def test_switches_with_the_mode(self):
        backend = self.make('jtag', ['-D', '200', '-P', '1000'])
        backend.switch_to_progmode()
        backend.switch_to_debmode()
        self.assertEqual(self.clock_codes(backend), [jtag2.jtag_clock_code(1000), jtag2.jtag_clock_code(200)])
        backend.protocol.enter_progmode.assert_called_once()

    def test_not_on_debugwire(self):
        backend = self.make('debugwire', ['-D', '200'], 'atmega328p')
        backend._set_jtag_clock(200)
        backend.switch_to_progmode()
        self.assertEqual(self.clock_codes(backend), [])

    def test_warning_below_minimum(self):
        backend = self.make('jtag', ['-D', '5'])
        backend.logger.warning.assert_called_once()


class TestClockHint(TestCase):
    """A failed stop or single step on JTAG points to -F and -D, once; the error itself goes on"""

    def make(self, iface, device):
        with patch('pyavrocd.session.logging.getLogger', MagicMock()):
            backend = Jtag2Backend(ProbeCandidate(tool='jtagice2', product='JTAGICE mkII', address='4262'),
                                   device, iface, options(['-d', device, '-F', '128000']))
        backend.protocol = MagicMock()
        return backend

    def test_stop_timeout(self):
        backend = self.make('jtag', 'atmega324p')
        backend.protocol.forced_stop.side_effect = jtag2.Jtag2UsbTimeout("No response to command 0x0A")
        for _ in range(2):
            with self.assertRaises(jtag2.Jtag2UsbTimeout):
                backend.stop()
        backend.logger.warning.assert_called_once()
        self.assertIn("-F", backend.logger.warning.call_args.args[0])
        self.assertEqual(backend.logger.warning.call_args.args[1:], (jtag2.jtag_clock_khz(6), '128000'))

    def test_single_step(self):
        backend = self.make('jtag', 'atmega324p')
        backend._set_jtag_clock(25)
        backend.protocol.single_step.side_effect = jtag2.Jtag2Error("Single step: RSP_ILLEGAL_MCU_STATE")
        with self.assertRaises(jtag2.Jtag2Error):
            backend._single_step()
        self.assertEqual(backend.logger.warning.call_args.args[1], jtag2.jtag_clock_khz(53))

    def test_not_on_debugwire(self):
        backend = self.make('debugwire', 'atmega328p')
        backend.protocol.single_step.side_effect = jtag2.Jtag2Error("Single step: RSP_ILLEGAL_MCU_STATE")
        with self.assertRaises(jtag2.Jtag2Error):
            backend._single_step()
        backend.logger.warning.assert_not_called()
