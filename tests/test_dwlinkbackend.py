"""
The test suite for the DwlinkBackend class (dw-link 7 and later) and its discovery
"""
#pylint: disable=protected-access,missing-function-docstring,missing-class-docstring
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from pyavrocd import jtag2
from pyavrocd.backend import ProbeCandidate, BackendNotSupportedError, BREAKCODE
from pyavrocd.dwlinkbackend import DwlinkBackend, DwlinkProtocol, discover, reboot_probe, \
     CMND_EXECUTE_INSTRUCTION, PAR_TARGET_POWER, PAR_DWLINK_ERROR
from pyavrocd.errors import FatalError
from pyavrocd.main import options, find_dwlink
from tests.test_jtag2 import FakeTransport

CANDIDATE = ProbeCandidate(tool='dwlink', product='dw-link', address='/dev/cu.usbmodem242101')

def sign_on_body(ident=b"dw-link", major=7, hardware=1):
    return bytes([jtag2.RSP_SIGN_ON, 1, 0xFF, 0, major, hardware, 0xFF, 0, major, hardware]) + \
      bytes.fromhex("4703FD76C712") + ident + b"\0"

def make_backend(args=None):
    with patch('pyavrocd.session.logging.getLogger', MagicMock()):
        return DwlinkBackend(CANDIDATE, 'attiny1634', 'debugwire',
                             options(args or ['-d', 'attiny1634']))

def attach(backend, answers):
    """A protocol on a fake transport that answers with the given (sequence, body) pairs"""
    backend.transport = MagicMock(spec=jtag2.Jtag2SerialTransport)
    backend.protocol = DwlinkProtocol(FakeTransport(answers))
    return backend.protocol.transport


class TestDiscovery(TestCase):

    @patch('pyavrocd.dwlinkbackend.list_ports.comports')
    def test_only_usb_serial_ports(self, mock_ports):
        mock_ports.return_value = [SimpleNamespace(device='/dev/cu.Bluetooth-Incoming-Port', vid=None),
                                   SimpleNamespace(device='/dev/cu.usbmodem242101', vid=0x2341),
                                   SimpleNamespace(device='/dev/cu.usbserial-24210', vid=0x1A86)]
        self.assertEqual([c.address for c in discover()], ['/dev/cu.usbmodem242101', '/dev/cu.usbserial-24210'])

    @patch('pyavrocd.main.dwlinkbackend.discover')
    def test_find_dwlink(self, mock_discover):
        logger = MagicMock()
        ports = [ProbeCandidate('dwlink', 'dw-link', '/dev/cu.usbmodem242101'),
                 ProbeCandidate('dwlink', 'dw-link', '/dev/cu.usbserial-24210')]
        mock_discover.return_value = ports
        self.assertEqual(find_dwlink(options(['-d', 'attiny1634']), 'debugwire', logger), (True, None))
        logger.critical.assert_any_call(" Port: %s", '/dev/cu.usbserial-24210')
        self.assertEqual(find_dwlink(options(['-d', 'attiny1634', '-u', '242101']), 'debugwire', logger),
                         (False, ports[0]))
        mock_discover.return_value = ports[1:]
        self.assertEqual(find_dwlink(options(['-d', 'attiny1634']), 'debugwire', logger), (False, ports[1]))
        mock_discover.return_value = []
        self.assertEqual(find_dwlink(options(['-d', 'attiny1634']), 'debugwire', logger), (True, None))
        logger.critical.assert_called_with("No compatible tool discovered")

    def test_find_dwlink_refuses(self):
        logger = MagicMock()
        self.assertEqual(find_dwlink(options(['-d', 'atmega4809', '-t', 'dwlink']), 'updi', logger), (True, None))
        logger.critical.assert_called_with("dw-link can only debug debugWIRE targets")
        self.assertEqual(find_dwlink(options(['-d', 'attiny1634', '--dw-link-baud', '250000']), 'debugwire',
                                     logger), (True, None))


class TestErrorNumber(TestCase):

    def test_failure_explained(self):
        proto = DwlinkProtocol(FakeTransport([('same', b"\xa0"), ('same', bytes([0x81, 113]))]))
        with self.assertRaises(jtag2.Jtag2Error) as caught:
            proto.write_memory(jtag2.MEMTYPE_FLASH_PAGE, 0x100, bytes(32))
        self.assertIn("dw-link error 113: flash page verification failed", str(caught.exception))
        self.assertEqual(proto.transport.sent[1][1], bytes([jtag2.CMND_GET_PARAMETER, PAR_DWLINK_ERROR]))

    def test_no_error_number(self):
        proto = DwlinkProtocol(FakeTransport([('same', b"\xac"), ('same', b"\x81\x00")]))
        with self.assertRaises(jtag2.Jtag2Error) as caught:
            proto.set_parameter(jtag2.PAR_EMULATOR_MODE, b"\x00")
        self.assertNotIn("dw-link error", str(caught.exception))

    def test_other_refusals_unchanged(self):
        proto = DwlinkProtocol(FakeTransport([('same', b"\xaa")]))
        with self.assertRaises(jtag2.Jtag2Error):
            proto.ok(b"\x11", "Set breakpoint")
        self.assertEqual(len(proto.transport.sent), 1)    # no question for the error number


class TestSignOn(TestCase):

    def test_only_debugwire(self):
        with patch('pyavrocd.session.logging.getLogger', MagicMock()):
            with self.assertRaises(BackendNotSupportedError):
                DwlinkBackend(CANDIDATE, 'atmega324p', 'jtag', options(['-d', 'atmega324p']))

    @patch('pyavrocd.dwlinkbackend.time.monotonic', side_effect=[0, 0, 0, 1])
    def test_retries_then_switches_speed(self, _monotonic):
        backend = make_backend()
        fake = attach(backend, [('same', sign_on_body()), ('same', b"\x80")])
        backend.protocol.sign_on = MagicMock(side_effect=[jtag2.Jtag2Timeout("boot"), jtag2.Jtag2Timeout("boot"),
                                                          jtag2.parse_sign_on(sign_on_body())])
        backend.protocol.set_baud = MagicMock()
        backend._sign_on(announce=True)
        self.assertEqual(backend.protocol.sign_on.call_count, 3)
        backend.transport.set_baudrate.assert_has_calls([call(19200), call(115200), call(57600)])
        backend.protocol.set_baud.assert_called_once_with(115200)
        backend._sign_on()                       # signed on: nothing more
        self.assertEqual(backend.protocol.sign_on.call_count, 3)
        self.assertEqual(fake.sent, [])

    @patch('pyavrocd.dwlinkbackend.time.monotonic', return_value=0)
    def test_found_at_another_speed(self, _monotonic):
        # left at 38400 by a server with another --dw-link-baud that did not sign off
        backend = make_backend()
        attach(backend, [])
        speed = {}
        backend.transport.set_baudrate.side_effect = lambda b: speed.update(now=b)
        def sign_on(_timeout):
            if speed['now'] != 38400:
                raise jtag2.Jtag2Timeout("wrong speed")
            return jtag2.parse_sign_on(sign_on_body())
        backend.protocol.sign_on = MagicMock(side_effect=sign_on)
        backend.protocol.set_baud = MagicMock()
        backend._sign_on()
        tried = [c.args[0] for c in backend.transport.set_baudrate.call_args_list]
        self.assertEqual(tried, [19200, 115200, 57600, 38400])
        backend.protocol.set_baud.assert_called_once_with(115200)

    def test_not_dwlink(self):
        backend = make_backend()
        attach(backend, [('same', sign_on_body(ident=b"JTAGICEmkII"))])
        with self.assertRaises(FatalError):
            backend._sign_on()

    def test_too_old(self):
        backend = make_backend()
        attach(backend, [('same', sign_on_body(major=6))])
        with self.assertRaises(FatalError):
            backend._sign_on()

    def test_start_speed_needs_no_switch(self):
        backend = make_backend(['-d', 'attiny1634', '--dw-link-baud', '19200'])
        fake = attach(backend, [('same', sign_on_body())])
        backend._sign_on()
        self.assertEqual(len(fake.sent), 1)


class TestSession(TestCase):

    def setUp(self):
        self.backend = make_backend()
        self.backend.sign_on_info = jtag2.parse_sign_on(sign_on_body())

    def test_enter_mode_syncs_and_sends_context(self):
        fake = attach(self.backend, [('same', b"\x81\x88\x13")] + [('same', b"\x80")] * 7)
        self.backend._enter_mode()
        commands = [body for _, body in fake.sent]
        self.assertEqual(commands[1], bytes([jtag2.CMND_SET_PARAMETER, jtag2.PAR_EMULATOR_MODE, 0]))
        self.assertEqual([c[1] for c in commands[2:7]], [0x02, 0x80, 0x88, 0x81, 0x89])
        self.assertTrue(all(c[0] == jtag2.CMND_SET_DEVICE_CONTEXT for c in commands[2:7]))
        self.assertEqual(commands[7][:2], bytes([jtag2.CMND_SET_PARAMETER, jtag2.PAR_TIMERS_RUNNING]))
        self.assertTrue(self.backend._mode_set)

    def test_enter_mode_without_debugwire(self):
        attach(self.backend, [('same', b"\x81\x88\x13"), ('same', b"\xac"), ('same', b"\x81\x02")])
        with self.assertRaises(FatalError):
            self.backend._enter_mode()

    def test_execute_instruction(self):
        fake = attach(self.backend, [('same', b"\x80")])
        self.backend.execute_instruction(0x9180)
        self.assertEqual(fake.sent[0][1], bytes([CMND_EXECUTE_INSTRUCTION, 0x80, 0x91]))

    def test_step_over_planted_break_injects(self):
        self.backend._swbp_planted = {0xB2: 0x940E}
        self.backend._swbp_wanted = {0xB2}
        self.backend.program_counter_read = MagicMock(return_value=0x59)
        self.backend.execute_instruction = MagicMock()
        self.backend._step = MagicMock()
        self.backend.step()
        self.backend.execute_instruction.assert_called_once_with(0x940E)
        self.backend._step.assert_not_called()

    def test_software_breakpoints_planted_by_server(self):
        self.assertTrue(self.backend.software_breakpoint_set(0xB2))
        self.assertEqual(self.backend._swbp_wanted, {0xB2})
        page = bytearray(range(32))
        self.backend._flash_read = MagicMock(return_value=page)
        self.backend.program_flash_page = MagicMock()
        self.backend._sync_software_breakpoints()
        written = self.backend.program_flash_page.call_args[0][1]
        self.assertEqual(written[0x12:0x14], BREAKCODE.to_bytes(2, 'little'))

    def test_load_forgets_planted_breaks(self):
        self.backend._swbp_planted = {0x100: 0x1234, 0x400: 0x5678}
        fake = attach(self.backend, [('same', b"\x80")] * 2)
        self.backend.write_flash_pages(0x100, bytes(384), False)
        self.assertEqual(self.backend._swbp_planted, {0x400: 0x5678})
        self.assertEqual([len(body) - 10 for _, body in fake.sent], [256, 128])  # one command per 256 bytes

    def test_hardware_breakpoints(self):
        with self.assertRaises(BackendNotSupportedError):
            self.backend.hardware_breakpoint_set(1, 0x100)
        self.backend.hardware_breakpoint_clear(1)

    def test_power_cycle_on_the_shield(self):
        fake = attach(self.backend, [('same', b"\x81\x03"), ('same', b"\x80")])
        self.assertTrue(self.backend.power_cycle())
        self.assertEqual(fake.sent[1][1], bytes([jtag2.CMND_SET_PARAMETER, PAR_TARGET_POWER, 2]))

    def test_no_power_cycle_without_shield(self):
        attach(self.backend, [('same', b"\x81\x01")])
        self.assertFalse(self.backend.power_cycle())

    def test_stop_debugging_signs_off_and_keeps_the_port(self):
        attach(self.backend, [('same', b"\x80")])
        transport = self.backend.transport
        with patch('pyavrocd.jtag2backend.Jtag2Backend.stop_debugging') as mock_stop:
            self.backend.stop_debugging(leave=True)
        mock_stop.assert_called_once()
        self.assertEqual(self.backend.protocol.transport.sent[0][1], bytes([jtag2.CMND_SIGN_OFF]))
        transport.set_baudrate.assert_called_once_with(19200)
        self.assertIsNone(self.backend.sign_on_info)
        self.assertIsNotNone(self.backend.protocol)


class TestSignOff(TestCase):
    """Every sign-off of the session is real, back at the start speed (a session can end without stop_debugging)"""

    def test_sign_off_once(self):
        backend = make_backend()
        backend.sign_on_info = jtag2.parse_sign_on(sign_on_body())
        fake = attach(backend, [('same', b"\x80")])
        backend._sign_off()
        self.assertEqual(fake.sent[0][1], bytes([jtag2.CMND_SIGN_OFF]))
        backend.transport.set_baudrate.assert_called_once_with(19200)
        self.assertIsNone(backend.sign_on_info)
        backend._sign_off()                                  # nothing more to sign off
        self.assertEqual(len(fake.sent), 1)

    def test_release_signs_off(self):
        backend = make_backend()
        backend.sign_on_info = jtag2.parse_sign_on(sign_on_body())
        fake = attach(backend, [('same', b"\x80")])
        backend.release()
        self.assertEqual(fake.sent[0][1], bytes([jtag2.CMND_SIGN_OFF]))
        backend.transport.set_baudrate.assert_called_once_with(19200)


def serial_fake(answers):
    fake = FakeTransport(answers)
    fake.set_baudrate = MagicMock()
    fake.flush = MagicMock()
    fake.close = MagicMock()
    return fake

class TestReboot(TestCase):
    """--reboot-debugger: sign off with PAR_SOFT_RESET 0 (dw-link restarts by its watchdog), sign on again"""

    @patch('pyavrocd.dwlinkbackend.time.sleep')
    @patch('pyavrocd.dwlinkbackend.jtag2.Jtag2SerialTransport')
    def test_reboot(self, mock_transport, _sleep):
        fake = serial_fake([('same', sign_on_body()), ('same', b"\x80"), ('same', b"\x80"),
                            ('same', sign_on_body()), ('same', b"\x80")])
        mock_transport.return_value = fake
        self.assertTrue(reboot_probe(CANDIDATE, 115200, MagicMock()))
        mock_transport.assert_called_once_with(CANDIDATE.address)    # one port open, one Arduino reset
        self.assertEqual([body for _, body in fake.sent],
                         [bytes([jtag2.CMND_GET_SIGN_ON]),
                          bytes([jtag2.CMND_SET_PARAMETER, jtag2.PAR_SOFT_RESET, jtag2.SOFT_RESET_HARD]),
                          bytes([jtag2.CMND_SIGN_OFF]),
                          bytes([jtag2.CMND_GET_SIGN_ON]),
                          bytes([jtag2.CMND_SIGN_OFF])])
        fake.close.assert_called_once()

    @patch('pyavrocd.dwlinkbackend.jtag2.Jtag2SerialTransport')
    def test_not_dwlink(self, mock_transport):
        fake = serial_fake([('same', sign_on_body(ident=b"JTAGICEmkII"))])
        mock_transport.return_value = fake
        logger = MagicMock()
        self.assertFalse(reboot_probe(CANDIDATE, 115200, logger))
        self.assertEqual(len(fake.sent), 1)                          # nothing after the sign-on
        fake.close.assert_called_once()
        logger.critical.assert_called_once()

    @patch('pyavrocd.dwlinkbackend.time.sleep')
    @patch('pyavrocd.dwlinkbackend.time.monotonic', side_effect=[0, 0, 10])
    @patch('pyavrocd.dwlinkbackend.jtag2.Jtag2SerialTransport')
    def test_not_back(self, mock_transport, _monotonic, _sleep):
        fake = serial_fake([('same', sign_on_body()), ('same', b"\x80"), ('same', b"\x80")])
        mock_transport.return_value = fake
        logger = MagicMock()
        self.assertFalse(reboot_probe(CANDIDATE, 115200, logger))
        fake.close.assert_called_once()
        self.assertIn("Could not reboot", logger.critical.call_args.args[0])
