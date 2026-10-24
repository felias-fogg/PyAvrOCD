"""
The test suit for the jtag2 module (JTAGICE mkII protocol, AVR067)
"""
#pylint: disable=protected-access,missing-function-docstring,missing-class-docstring,invalid-name
from unittest import TestCase
from unittest.mock import Mock, patch

import usb.core

from pyavrocd import jtag2
from pyavrocd.backend import BackendError
from pyavrocd.deviceinfo.devices import atmega324p, atmega2560, atmega328p, attiny85, attiny13
from pyavrocd.jtag2 import crc16, make_frame, parse_frame, parse_sign_on, Jtag2Error, \
     Jtag2Protocol, Jtag2UsbTransport, EVENT_SEQUENCE

# captured on 2026-10-23: CMND_GET_SIGN_ON with sequence number 7, and the answers
REQUEST = bytes.fromhex("1b0700010000000e01fd0b")
CLONE = bytes.fromhex("1b07001c0000000e8601ff270700ff2707010900000042624a5441474943456d6b4949008e2b")
DRAGON = bytes.fromhex("1b07001a0000000e8601ff0b0601ff0b060700a200050860415652445241474f4e009479")

class TestFraming(TestCase):

    def test_crc_table_as_printed_in_avr067(self):
        self.assertEqual(jtag2.CRC_TABLE[:4], [0x0000, 0x1189, 0x2312, 0x329b])
        self.assertEqual(jtag2.CRC_TABLE[128], 0x8408)
        self.assertEqual(jtag2.CRC_TABLE[255], 0x0f78)

    def test_make_frame_matches_capture(self):
        self.assertEqual(make_frame(7, b"\x01"), REQUEST)

    def test_parse_captured_responses(self):
        for frame in (CLONE, DRAGON):
            sequence, body = parse_frame(frame)
            self.assertEqual(sequence, 7)
            self.assertEqual(body[0], jtag2.RSP_SIGN_ON)

    def test_parse_frame_errors(self):
        bad_crc = CLONE[:-1] + bytes([CLONE[-1] ^ 1])
        bad_token = CLONE[:7] + b"\x0f" + CLONE[8:]
        for frame in (bad_crc, bad_token, CLONE[:20], b"\x1b\x00"):
            with self.assertRaises(Jtag2Error):
                parse_frame(frame)

    def test_round_trip_and_crc_of_whole_frame(self):
        frame = make_frame(0x1234, bytes(range(100)))
        self.assertEqual(parse_frame(frame), (0x1234, bytes(range(100))))
        self.assertEqual(crc16(frame[:-2]), int.from_bytes(frame[-2:], 'little'))

    def test_sign_on(self):
        clone = parse_sign_on(parse_frame(CLONE)[1])
        self.assertEqual((clone.protocol, clone.master_firmware, clone.slave_firmware),
                         (1, (7, 0x27), (7, 0x27)))
        self.assertEqual((clone.master_hardware, clone.slave_hardware), (0, 1))
        self.assertEqual(clone.serial, "090000004262") # = the USB descriptor
        self.assertEqual(clone.ident, "JTAGICEmkII")
        dragon = parse_sign_on(parse_frame(DRAGON)[1])
        self.assertEqual((dragon.master_firmware, dragon.serial, dragon.ident),
                         ((6, 0x0B), "00A200050860", "AVRDRAGON"))
        with self.assertRaises(Jtag2Error):
            parse_sign_on(b"\x80")

    def test_device_descriptor_like_avrdude(self):
        # captured on 2026-10-23: avrdude 8.3 -c jtag2 -p m324p, the descriptor after the 240 zero mask bytes
        avrdude = jtag2.DESCRIPTOR_TAIL.unpack(bytes.fromhex(
            "31570080000400000000000000800000000000000000000000000000000000000000000000000000000001000000003f01"
            "000000000000003f00"))
        descriptor = jtag2.make_device_descriptor(atmega324p.DEVICE_INFO)
        self.assertEqual(len(descriptor), jtag2.DESCRIPTOR_SIZE)
        self.assertEqual(descriptor[:240], jtag2.io_masks(atmega324p.DEVICE_INFO)) # avrdude sends zeros
        ours = jtag2.DESCRIPTOR_TAIL.unpack(descriptor[240:])
        differ = [i for i, (a, b) in enumerate(zip(ours, avrdude)) if a != b]
        self.assertEqual(differ, [5, 16]) # ulBootAddress, uiStartSmallestBootLoaderSection: the last page
        self.assertEqual((ours[5], avrdude[5]), (0x3FC0, 0))
        self.assertEqual((ours[16], avrdude[16]), (0x3FC0, 0x3F00))

    def test_device_descriptor_debugwire_like_avrdude(self):
        # captured on 2026-10-23: avrdude 8.3 -c jtag2dw -p m328p on the mkII clone
        avrdude = jtag2.DESCRIPTOR_TAIL.unpack(bytes.fromhex(
            "31570080000400000000000000800000bdf2bde1bbcfb400be01b601bc00bbbf99f9bbafb6011100000001000000003f01"
            "000000000000003f00"))
        ours = jtag2.DESCRIPTOR_TAIL.unpack(jtag2.make_device_descriptor(atmega328p.DEVICE_INFO)[240:])
        self.assertEqual([i for i, (a, b) in enumerate(zip(ours, avrdude)) if a != b], [5, 16]) # boot fields only

    def test_debugwire_instructions_of_a_tiny(self):
        # avrdude.conf, t85: eeprom_instr and flash_instr
        self.assertEqual(jtag2.debugwire_instructions(attiny85.DEVICE_INFO),
                         (bytes.fromhex("bbffbbeebbccb20dbc02b402ba0dbbbc99e1bbac"), bytes.fromhex("b40212")))
        self.assertEqual(jtag2.debugwire_instructions(attiny13.DEVICE_INFO)[0][:2], b"\xbb\xfe") # 1-byte EEAR

    def test_device_descriptor_large_flash(self):
        # avrdude 8.3 -p m2560 sent RAMPZ 0x3B, flash size 0x40000, boot section 0xFE00 (0x1FE00 truncated), EIND 0
        ours = jtag2.DESCRIPTOR_TAIL.unpack(jtag2.make_device_descriptor(atmega2560.DEVICE_INFO)[240:])
        self.assertEqual((ours[2], ours[7], ours[16], ours[23]), (0x3B, 0x40000, 0xFF80, 0)) # 0x1FF80 truncated
        self.assertEqual(ours[5], 0x1FF80)                    # ulBootAddress has 32 bits

    def test_io_masks(self):
        info = atmega324p.DEVICE_INFO
        masks = jtag2.io_masks(info)
        def bit(offset, index):
            return masks[offset + index // 8] >> (index % 8) & 1
        def read(address):
            return bit(0, address - 0x20) if address < 0x60 else bit(32, address - 0x60)
        def write(address):
            return bit(16, address - 0x20) if address < 0x60 else bit(136, address - 0x60)
        self.assertEqual((read(0x24), write(0x24)), (1, 1))     # DDRB
        self.assertEqual((read(0x20), write(0x20)), (1, 0))     # PINA: ronly
        self.assertEqual((read(0x35), write(0x35)), (1, 0))     # TIFR0: ronly, write-back would clear flags
        self.assertEqual((read(0x4E), write(0x4E)), (0, 0))     # SPDR: masked, reading has side effects
        self.assertEqual((read(0xC6), write(0xC6)), (0, 0))     # UDR0
        self.assertEqual((read(0x5D), read(0x5E), read(0x5F)), (1, 1, 1)) # SP, SREG
        self.assertEqual(masks[8:16] + masks[24:32], bytes(16)) # no shadows
        self.assertEqual(masks[32 + 20:84], bytes(32))          # ext range ends at SRAM start 0x100
        for address in range(0x20, 0x100):
            self.assertEqual(read(address), address not in info['masked_registers'])
            self.assertEqual(write(address), address not in info['masked_registers'] + info['ronly_registers'])


class FakeTransport():
    """Answers every frame with the next of the given (sequence, body) pairs; 'same' echoes"""
    def __init__(self, answers):
        self.answers = list(answers)
        self.sent = []
    def write_frame(self, frame):
        self.sent.append(parse_frame(frame))
    def read_frame(self, _timeout=None):
        if not self.answers:
            raise usb.core.USBTimeoutError("Operation timed out")
        sequence, body = self.answers.pop(0)
        if sequence == 'same':
            sequence = self.sent[-1][0]
        return make_frame(sequence, body)

class TestProtocol(TestCase):

    def test_sequence_numbers_count_and_wrap(self):
        proto = Jtag2Protocol(FakeTransport([('same', b"\x80")] * 3))
        proto.sequence = 0xFFFD
        for _ in range(3):
            proto.command(b"\x00")
        self.assertEqual([s for s, _ in proto.transport.sent], [0xFFFD, 0xFFFE, 0x0000]) # 0xFFFF is for events

    def test_events_set_aside(self):
        proto = Jtag2Protocol(FakeTransport([(EVENT_SEQUENCE, b"\xe0\x01"), ('same', b"\x80")]))
        self.assertEqual(proto.command(b"\x00"), b"\x80")
        self.assertEqual(proto.events, [b"\xe0\x01"])

    def test_wrong_sequence_number(self):
        proto = Jtag2Protocol(FakeTransport([(42, b"\x80")]))
        with self.assertRaises(Jtag2Error):
            proto.command(b"\x00")

    def test_sign_on_and_off(self):
        proto = Jtag2Protocol(FakeTransport([('same', parse_frame(DRAGON)[1]), ('same', b"\x80"), ('same', b"\xa0")]))
        self.assertEqual(proto.sign_on().ident, "AVRDRAGON")
        proto.sign_off()
        with self.assertRaises(Jtag2Error):
            proto.sign_off()

    def test_get_parameter(self):
        # captured on 2026-10-23 from the mkII clone with an ATmega324P: Vtarget 4698 mV
        proto = Jtag2Protocol(FakeTransport([('same', b"\x81\x5a\x12")]))
        self.assertEqual(int.from_bytes(proto.get_parameter(jtag2.PAR_OCD_VTARGET), 'little'), 4698)
        self.assertEqual(proto.transport.sent[-1][1], b"\x03\x06")

    def test_set_parameter(self):
        proto = Jtag2Protocol(FakeTransport([('same', b"\x80")]))
        proto.set_parameter(jtag2.PAR_EMULATOR_MODE, bytes([jtag2.EMULATOR_MODE_JTAG]))
        self.assertEqual(proto.transport.sent[-1][1], b"\x02\x03\x01")

    def test_parameter_failures_are_named(self):
        proto = Jtag2Protocol(FakeTransport([('same', b"\xa4"), ('same', b"\xa1"), ('same', b"\x81\x00"),
                                             ('same', b"\x99")]))
        with self.assertRaisesRegex(Jtag2Error, "0x07: RSP_ILLEGAL_EMULATOR_MODE"):
            proto.get_parameter(jtag2.PAR_OCD_JTAG_CLK)
        with self.assertRaisesRegex(Jtag2Error, "RSP_ILLEGAL_PARAMETER"):
            proto.get_parameter(0x77)
        with self.assertRaisesRegex(Jtag2Error, "0x03: 0x81"): # RSP_PARAMETER is not RSP_OK
            proto.set_parameter(jtag2.PAR_EMULATOR_MODE, b"\x01")
        with self.assertRaisesRegex(Jtag2Error, "0x99"):
            proto.get_parameter(jtag2.PAR_MCU_STATE)

    def test_memory_and_pc(self):
        proto = Jtag2Protocol(FakeTransport([('same', b"\x82\x81\x81"), ('same', b"\x80"),
                                             ('same', b"\x84\x5b\x00\x00\x00"), ('same', b"\x80")]))
        self.assertEqual(proto.read_memory(jtag2.MEMTYPE_SRAM, 0x24, 2), b"\x81\x81")
        proto.write_memory(jtag2.MEMTYPE_SRAM, 0x24, b"\x55")
        self.assertEqual(proto.read_pc(), 0x5B)
        proto.write_pc(0x7D)
        self.assertEqual([body for _, body in proto.transport.sent],
                         [bytes.fromhex("0520020000002400 0000".replace(" ", "")),
                          bytes.fromhex("042001000000240000 0055".replace(" ", "")),
                          b"\x07", bytes.fromhex("067d000000")])

    def test_step_and_break_event(self):
        # captured on 2026-10-23: an EVT_IDR_DIRTY, then EVT_BREAK at word 0x3E after a step
        proto = Jtag2Protocol(FakeTransport([('same', b"\x80"), (EVENT_SEQUENCE, b"\xec\x01"),
                                             (EVENT_SEQUENCE, bytes.fromhex("e03e00000000"))]))
        proto.single_step()
        self.assertEqual(proto.transport.sent[-1][1], b"\x09\x01\x01")
        self.assertEqual(proto.wait_for_break(), (0x3E, 0))
        self.assertIsNone(proto.poll_break())
        with self.assertRaisesRegex(Jtag2Error, "No break event"):
            proto.wait_for_break(10)

    def test_break_event_set_aside_during_command(self):
        proto = Jtag2Protocol(FakeTransport([('same', b"\x80"), (EVENT_SEQUENCE, bytes.fromhex("e06b00000000")),
                                             ('same', b"\x84\x6b\x00\x00\x00")]))
        proto.forced_stop()
        self.assertEqual(proto.read_pc(), 0x6B)    # the event came first and was set aside
        self.assertEqual(proto.poll_break(), (0x6B, 0))

    def test_breakpoint_and_progmode_frames(self):
        # the formats measured on the mkII clone (324P): word addresses, numbers 1-3 and 0 for SW BPs
        proto = Jtag2Protocol(FakeTransport([('same', b"\x80")] * 9))
        proto.set_break(jtag2.SOFTWARE_BREAKPOINT, 0x52)
        proto.set_break(2, 0x52)
        proto.clr_break(jtag2.SOFTWARE_BREAKPOINT, 0x52)
        proto.clr_break(2)
        proto.run_to(0x52)
        proto.enter_progmode()
        proto.erase_page_spm(0x80)
        proto.debugwire_disable()
        proto.restore_target()
        self.assertEqual([body.hex() for _, body in proto.transport.sent],
                         ["1101005200000003", "1101025200000003", "1a0052000000", "1a0200000000",
                          "1c52000000", "14", "0d80000000", "0b04", "23"])


class TestUsbErrors(TestCase):
    """pyusb errors leave command() as Jtag2 errors, which are BackendErrors"""

    def test_lost_response_is_a_timeout(self):
        proto = Jtag2Protocol(FakeTransport([]))         # raises USBTimeoutError when read
        with self.assertRaises(jtag2.Jtag2UsbTimeout) as caught:
            proto.command(bytes([jtag2.CMND_RESET, 1]))
        self.assertIsInstance(caught.exception, BackendError)
        self.assertIn("command 0x0B", str(caught.exception))

    def test_other_usb_error(self):
        transport = FakeTransport([])
        transport.write_frame = Mock(side_effect=usb.core.USBError("Pipe error"))
        with self.assertRaises(jtag2.Jtag2UsbError) as caught:
            Jtag2Protocol(transport).command(bytes([jtag2.CMND_GO]))
        self.assertNotIsInstance(caught.exception, jtag2.Jtag2UsbTimeout)
        self.assertIn("Pipe error", str(caught.exception))

class TestIsp(TestCase):

    def test_enter_and_leave_only_once(self):
        # open + enter, as the session does before unprogramming DWEN: one SPI mode, one ISP entry
        isp = jtag2.Jtag2Isp(Jtag2Protocol(FakeTransport([('same', body) for body in
                                                        (b"\x80", b"\x88\x10\x00", b"\x88\x11\x00",
                                                         b"\x88\x10\x00", b"\x88\x11\x00", b"\x80")])))
        isp.enter()
        isp.enter()
        isp.leave()
        isp.leave()
        isp.enter()   # programming mode again, without the SPI mode
        isp.close()
        self.assertEqual([body.hex() for _, body in isp.protocol.transport.sent],
                         ["020303", "2f020010c8641920005303ac530000", "2f0200110101",
                          "2f020010c8641920005303ac530000", "2f0200110101", "020302"])

class TestTransport(TestCase):

    def transport(self, packets=()):
        tr = Jtag2UsbTransport.__new__(Jtag2UsbTransport)
        tr.packet_size = 64
        tr.ep_out = Mock()
        tr.ep_in = Mock()
        tr.ep_in.read.side_effect = list(packets)
        return tr

    def test_zero_length_packet_after_full_frame(self):
        tr = self.transport()
        tr.write_frame(bytes(64))
        self.assertEqual([c.args[0] for c in tr.ep_out.write.call_args_list], [bytes(64), b""])
        tr.ep_out.write.reset_mock()
        tr.write_frame(bytes(65))
        self.assertEqual(tr.ep_out.write.call_count, 1)

    def test_read_until_short_packet(self):
        tr = self.transport([bytes(64), bytes(64), bytes(3)])
        self.assertEqual(len(tr.read_frame()), 131)
        tr = self.transport([bytes(64), b""]) # a frame of exactly one packet ends with a zero-length one
        self.assertEqual(len(tr.read_frame()), 64)

    def test_discover(self):
        def device(pid, serial, product):
            d = Mock(idVendor=0x03EB, idProduct=pid, iSerialNumber=3, iProduct=2)
            d.strings = {3: serial + "\0", 2: product}
            return d
        devices = [device(0x2103, "090000004262", "JTAGICE mkII"), device(0x2107, "00A200050860", "AVRDRAGON"),
                   device(0x2141, "J42700018184", "Atmel-ICE CMSIS-DAP")]
        with patch('pyavrocd.jtag2.usb.core.find', return_value=devices), \
             patch('pyavrocd.jtag2.usb.util.get_string', side_effect=lambda d, i: d.strings[i]):
            found = jtag2.discover()
            self.assertEqual([(c.tool, c.address) for c in found],
                             [('jtagice2', '090000004262'), ('dragon', '00A200050860')]) # NUL gone, Atmel-ICE not ours
            self.assertEqual([c.tool for c in jtag2.discover('dragon')], ['dragon'])
