"""
The test suit for the jtag1 module (JTAGICE mkI protocol, AVR060)
"""
#pylint: disable=protected-access,missing-function-docstring,missing-class-docstring,invalid-name
from unittest import TestCase

from pyavrocd import jtag1
from pyavrocd.jtag1 import Jtag1Protocol, Jtag1Error, Jtag1Timeout, EOP
from pyavrocd.deviceinfo.devices import atmega16, atmega128, atmega162, atmega169p, atmega169a, atmega32


class FakeTransport():
    """A probe whose answers are given as one byte string; reads past its end time out"""
    def __init__(self, answers : bytes = b''):
        self.answers = bytearray(answers)
        self.written = b''
        self.baudrates = []
    def write(self, data):
        self.written += data
    def read(self, count, timeout=1.0): # pylint: disable=unused-argument
        if len(self.answers) < count:
            data = bytes(self.answers)
            self.answers.clear()
            raise TimeoutError("only {}".format(data.hex()))
        data = bytes(self.answers[:count])
        del self.answers[:count]
        return data
    def flush(self):
        pass
    def set_baudrate(self, baud):
        self.baudrates.append(baud)


def protocol(answers : bytes = b'') -> Jtag1Protocol:
    return Jtag1Protocol(FakeTransport(answers))


class TestDescriptor(TestCase):

    def test_atmega16_tail_as_avr060_except_eeprom_page_and_boot(self):
        # AVR060: 31 57 00 80 00 00 80 1F 00 00 00 -- its EEPROM page size 0 is not the part's 4,
        # and the boot address is the start of the smallest boot section, ours the last page
        desc = jtag1.make_device_descriptor(atmega16.DEVICE_INFO)
        self.assertEqual(len(desc), jtag1.DESCRIPTOR_SIZE)
        self.assertEqual(desc[112:], bytes.fromhex("31 57 00 80 00 04 c0 1f 00 00 00"))

    def test_atmega128_tail(self):
        # AVR060: 22 68 3B 00 01 08 00 FE 00 00 9D (boot address: smallest boot section)
        desc = jtag1.make_device_descriptor(atmega128.DEVICE_INFO)
        self.assertEqual(desc[112:], bytes.fromhex("22 68 3b 00 01 08 80 ff 00 00 9d"))

    def test_upper_ext_io(self):
        self.assertEqual(jtag1.upper_ext_io(atmega16.DEVICE_INFO), 0)
        self.assertEqual(jtag1.upper_ext_io(atmega32.DEVICE_INFO), 0)
        self.assertEqual(jtag1.upper_ext_io(atmega162.DEVICE_INFO), 0x8B)
        self.assertEqual(jtag1.upper_ext_io(atmega169p.DEVICE_INFO), 0xFE)

    def test_masks_leave_out_masked_and_read_only_registers(self):
        info = atmega16.DEVICE_INFO
        masks = jtag1.io_masks(info)
        def bit(array_start, address):
            n = address - 0x20
            return (masks[array_start + n // 8] >> (n % 8)) & 1
        masked = info['masked_registers'][0]
        ronly = info['ronly_registers'][0]
        self.assertEqual((bit(0, masked), bit(8, masked)), (0, 0))      # neither read nor written
        self.assertEqual((bit(0, ronly), bit(8, ronly)), (1, 0))        # read, not written
        self.assertEqual((bit(0, 0x5F), bit(8, 0x5F)), (1, 1))          # SREG
        self.assertEqual(masks[16:32], bytes(16))                       # shadows
        self.assertEqual(masks[32:], bytes(80))                         # no extended I/O

    def test_extended_io_masks(self):
        masks = jtag1.io_masks(atmega128.DEVICE_INFO)
        self.assertNotEqual(masks[32:52], bytes(20))                    # ucReadExtIO
        self.assertNotEqual(masks[52:72], bytes(20))                    # ucWriteExtIO
        self.assertEqual(masks[72:], bytes(40))                         # shadows

    def test_extended_io_only_existing_registers(self):
        # measured on the ATmega169A: read bits for addresses without a register hang the probe
        for info in (atmega169a.DEVICE_INFO, atmega128.DEVICE_INFO):
            desc = jtag1.make_device_descriptor(info)
            existing = jtag1.existing_ext_io(info)
            self.assertTrue(all(d & ~e == 0 for d, e in zip(desc[32:52], existing)))
            self.assertTrue(all(d & ~e == 0 for d, e in zip(desc[52:72], existing)))
        desc = jtag1.make_device_descriptor(atmega169a.DEVICE_INFO)
        self.assertEqual(desc[32 + (0xE4 - 0x60) // 8] >> ((0xE4 - 0x60) % 8) & 1, 1)   # LCDCRA readable
        self.assertEqual(desc[32 + (0x61 - 0x60) // 8] >> 1 & 1, 1)                      # CLKPR readable
        self.assertEqual(desc[32 + (0x63 - 0x60) // 8] >> 3 & 1, 0)                      # nothing at 0x63
        self.assertEqual(desc[32 + (0x64 - 0x60) // 8] >> 4 & 1, 1)                      # PRR, not in AVR060
        self.assertIsNone(jtag1.existing_ext_io(atmega16.DEVICE_INFO))

    def test_descriptor_size_checked(self):
        with self.assertRaises(Jtag1Error):
            protocol().set_device_descriptor(bytes(122))


class TestCommands(TestCase):

    def test_sign_on(self):
        p = protocol(b'AAVRNOCDA')
        self.assertEqual(p.sign_on(), 'AVRNOCD')
        self.assertEqual(p.transport.written, b'S' + EOP)

    def test_get_and_set_parameter(self):
        p = protocol(b'A\xc0A' + b'AA')
        self.assertEqual(p.get_parameter(jtag1.PAR_HW_VERSION), 0xC0)
        p.set_parameter(jtag1.PAR_OCD_JTAG_CLOCK, 0xFE)
        self.assertEqual(p.transport.written, b'\x71\x7a' + EOP + b'\x42\x86\xfe' + EOP)

    def test_unknown_parameter_fails(self):
        with self.assertRaises(Jtag1Error):
            protocol(b'AFF').get_parameter(0x85)  # measured answer to the unknown parameter

    def test_jtag_id(self):
        p = protocol(b'A\x3fA' + b'A\x30A' + b'A\x40A' + b'A\x09A')  # measured on the ATmega16
        self.assertEqual(p.jtag_id(), 0x0940303F)

    def test_pc_is_word_address_plus_one(self):
        p = protocol(b'A\x00\x00\x2dA' + b'AA')
        self.assertEqual(p.read_pc(), 44)
        p.write_pc(42)
        self.assertEqual(p.transport.written[-6:], b'\x33\x00\x00\x2b' + EOP)

    def test_pc_zero_after_programming_mode(self):
        # measured: 0 right after OCDEN was programmed and programming mode left
        self.assertEqual(protocol(b'A\x00\x00\x00A').read_pc(), 0)

    def test_pc_while_running(self):
        with self.assertRaises(Jtag1Error):
            protocol(b'A\xaa\x55\xaaA').read_pc()

    def test_set_baud(self):
        p = protocol(b'AA')
        p.set_baud(115200)
        self.assertEqual(p.transport.written, b'\x42\x62\xff' + EOP)
        self.assertEqual(p.transport.baudrates, [115200])
        with self.assertRaises(Jtag1Error):
            p.set_baud(14400)


class TestMemory(TestCase):

    def test_read_sram(self):
        p = protocol(b'A' + bytes(range(8)) + b'\x00A')
        self.assertEqual(p.read_memory(jtag1.MEMTYPE_SRAM, 0, 8), bytes(range(8)))
        self.assertEqual(p.transport.written, b'\x52\x20\x07\x00\x00\x00' + EOP)

    def test_read_pml_comes_msb_first(self):
        p = protocol(b'A\x94\x0c\x00\x2a\x00A')            # measured: jmp 0x2A
        self.assertEqual(p.read_memory(jtag1.MEMTYPE_PML, 0, 4), bytes.fromhex("0c 94 2a 00"))
        self.assertEqual(p.transport.written, b'\x52\xa0\x01\x00\x00\x00' + EOP)   # two words

    def test_read_flash_page_in_flash_order(self):
        p = protocol(b'A\x0c\x94\x2a\x00\x00A')
        self.assertEqual(p.read_memory(jtag1.MEMTYPE_FLASH_PAGE, 0, 4), bytes.fromhex("0c 94 2a 00"))

    def test_incomplete_flash_read_is_repeated(self):
        # 2 of 4 data bytes lost, then a resync ('A' for Get Sync) and the complete answer
        p = protocol(b'A\x0c\x94\x00A' + b'A' + b'A\x0c\x94\x2a\x00\x00A')
        p.transport.read = _short_then(p.transport.read, 5)
        self.assertEqual(p.read_memory(jtag1.MEMTYPE_FLASH_PAGE, 0, 4), bytes.fromhex("0c 94 2a 00"))

    def test_incomplete_sram_read_is_not_repeated(self):
        with self.assertRaises(Jtag1Timeout):
            protocol(b'A\x01\x02').read_memory(jtag1.MEMTYPE_SRAM, 0x20, 4)

    def test_odd_flash_count(self):
        with self.assertRaises(Jtag1Error):
            protocol().read_memory(jtag1.MEMTYPE_PML, 0, 3)

    def test_read_failed(self):
        with self.assertRaises(Jtag1Error):
            protocol(b'A' + b'\x07' * 2 + b'\x00F').read_memory(jtag1.MEMTYPE_SRAM, 0, 2)

    def test_long_read_in_chunks(self):
        p = protocol(b'A' + bytes(256) + b'\x00A' + b'A' + bytes(256) + b'\x00A' + b'A' + bytes(88) + b'\x00A')
        self.assertEqual(len(p.read_memory(jtag1.MEMTYPE_SRAM, 0x100, 600)), 600)
        commands = p.transport.written.split(EOP)[:-1]
        self.assertEqual(commands, [b'\x52\x20\xff\x00\x01\x00', b'\x52\x20\xff\x00\x02\x00',
                                    b'\x52\x20\x57\x00\x03\x00'])

    def test_write_is_acknowledged_twice(self):
        p = protocol(b'A' + b'AA' + b'A\x01\x02\x00A')
        p.write_memory(jtag1.MEMTYPE_SRAM, 0x10, b'\x01\x02')
        self.assertEqual(p.read_memory(jtag1.MEMTYPE_SRAM, 0x10, 2), b'\x01\x02')
        written = b'\x57\x20\x01\x00\x00\x10' + EOP + b'h\x01\x02' + EOP
        self.assertEqual(p.transport.written[:len(written)], written)

    def test_write_pml_sends_msb_first(self):
        p = protocol(b'AAA')
        p.write_memory(jtag1.MEMTYPE_PML, 0x40, bytes.fromhex("98 95"))     # BREAK
        self.assertEqual(p.transport.written, b'\x57\xa0\x00\x00\x00\x40' + EOP + b'h\x95\x98' + EOP)

    def test_erase_page_takes_word_address_in_three_bytes(self):
        p = protocol(b'AA')
        p.erase_page_spm(0x6000)
        self.assertEqual(p.transport.written, b'\xa1\x00\x30\x00' + EOP)

    def test_program_breakpoint(self):
        p = protocol(b'AAA')
        p.set_program_breakpoint(1, 44)
        self.assertEqual(p.transport.written, b'\x57\x60\x00\x00\x00\x2c' + EOP + b'h\x01' + EOP)


class TestEventsAndSync(TestCase):

    def test_break_before_answer_is_set_aside(self):
        p = protocol(b'B\x00\x20' + b'AAVRNOCDA')
        self.assertEqual(p.sign_on(), 'AVRNOCD')
        self.assertEqual(p.poll_break(), 0x0020)

    def test_info_and_sleep_dropped(self):
        p = protocol(b'G\x55A' + b'H\x01A' + b'I' + b'B\x00\x20')
        self.assertEqual(p.poll_break(0.01), 0x0020)

    def test_poll_without_break(self):
        p = protocol(b'A')                       # a stray byte
        self.assertIsNone(p.poll_break(0.01))

    def test_go_and_break(self):
        p = protocol(b'A' + b'B\x00\x20')
        p.go()
        self.assertEqual(p.transport.written, b'G' + EOP)
        self.assertEqual(p.wait_for_break(0.1), 0x0020)

    def test_no_break(self):
        with self.assertRaises(Jtag1Error):
            protocol(b'').wait_for_break(0.01)

    def test_sync_error_resynchronizes(self):
        p = protocol(b'E' + b'A')
        with self.assertRaises(Jtag1Error):
            p.read_pc()
        self.assertTrue(p.transport.written.endswith(bytes([jtag1.CMD_GET_SYNC])))

    def test_resync_gives_up(self):
        with self.assertRaises(Jtag1Timeout):
            protocol(b'').resync()

    def test_timeout(self):
        with self.assertRaises(Jtag1Timeout):
            protocol(b'A').sign_on()

    def test_sync_tries_the_next_speed(self):
        p = protocol(b'AAVRNOCDA')
        p.transport.read = _fail_first_two(p.transport.read)   # nothing at 19200 (two tries)
        self.assertEqual(p.sync(), 115200)
        self.assertEqual(p.transport.baudrates, [19200, 115200])
        self.assertTrue(p.transport.written.startswith(b'SE' + EOP + b'S' + EOP))

    def test_no_probe(self):
        with self.assertRaises(Jtag1Timeout):
            protocol(b'').sync(bauds=(19200,))


def _fail_first_two(read):
    calls = [0]
    def wrapped(count, timeout=1.0):
        calls[0] += 1
        if calls[0] <= 2:
            raise TimeoutError("silent")
        return read(count, timeout)
    return wrapped


def _short_then(read, short_bytes):
    """The first answer stops after short_bytes bytes (a timeout); afterwards, normal reads"""
    state = {'left': short_bytes, 'cut': False}
    def wrapped(count, timeout=1.0):
        if not state['cut']:
            if count > state['left']:
                data = read(state['left']) if state['left'] else b''
                state['cut'] = True
                raise TimeoutError("short: {}".format(data.hex()))
            state['left'] -= count
        return read(count, timeout)
    return wrapped
