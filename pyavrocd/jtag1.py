"""
The JTAGICE mkI protocol (Atmel application note AVR060) over a serial line, spoken by the
JTAGICE mkI and its clones.

Every command ends with Sync_CRC/EOP, two blanks; the probe acknowledges it with Resp_OK ('A')
before it executes the command, and most commands end with another Resp_OK or Resp_FAILED.
There are no sequence numbers and no CRC. While the target runs, the probe may send Resp_BREAK
('B' and the two bytes of the break status register), and at any time Resp_INFO, Resp_SLEEP and
Resp_POWER; these are set aside when they turn up where an answer is expected.

What AVR060 does not say, measured on a clone (CH340, HW 0xC0, SW 0x80) with an ATmega16:
- The program counter is the word address plus one, read as well as written (avarice does the same).
- PML (flash through SPM/LPM) returns words MSB first, FLASH_JTAG in programming mode the bytes in
  flash order. For both, the count in a read or write command is the number of words minus one.
- The break cause is parameter 0x87, as in AVR060 (avrdude's 0x85 is unknown to the probe).
- The two single program breakpoints PSB0/PSB1 are set by writing 0 or 1 to memory type 0x60
  (AVR060's 'Event L'; avarice's breakpoint space) at the word address.
- Reading the baud rate parameter returns 0x17 at any speed, OCD Vtarget always 0xFF.
- The data block of a write is acknowledged twice, for every memory type (avarice reads it so, too).
"""
from dataclasses import dataclass
import logging
import struct
import time

import serial

from pyavrocd.backend import BackendError
from pyavrocd.termination import transaction

EOP : bytes = b'  '              # Sync_CRC/EOP: no CRC, two blanks

CMD_GET_SYNC : int = 0x20
CMD_SINGLE_STEP : int = 0x31
CMD_READ_PC : int = 0x32
CMD_WRITE_PC : int = 0x33
CMD_SET_PARAMETER : int = 0x42
CMD_FORCED_STOP : int = 0x46
CMD_GO : int = 0x47
CMD_READ_MEMORY : int = 0x52
CMD_GET_SIGN_ON : int = 0x53
CMD_WRITE_MEMORY : int = 0x57
CMD_DATA : int = 0x68             # 'h': the data block of a write; named in avrdude, not in AVR060
CMD_GET_PARAMETER : int = 0x71
CMD_RESET : int = 0x78
CMD_SET_DEVICE_DESCRIPTOR : int = 0xA0
CMD_ERASEPAGE_SPM : int = 0xA1
CMD_ENTER_PROGMODE : int = 0xA3
CMD_LEAVE_PROGMODE : int = 0xA4
CMD_CHIP_ERASE : int = 0xA5

RESP_OK : int = 0x41              # 'A'
RESP_BREAK : int = 0x42           # 'B', break status register H, L
RESP_SYNC_ERROR : int = 0x45      # 'E'
RESP_FAILED : int = 0x46          # 'F'
RESP_INFO : int = 0x47            # 'G', IDR, Resp_OK
RESP_SLEEP : int = 0x48           # 'H', status, Resp_OK
RESP_POWER : int = 0x49           # 'I'

PAR_BAUD_RATE : int = 0x62
PAR_HW_VERSION : int = 0x7A
PAR_SW_VERSION : int = 0x7B
PAR_IREG_HIGH : int = 0x81
PAR_IREG_LOW : int = 0x82
PAR_OCD_VTARGET : int = 0x84
PAR_OCD_JTAG_CLOCK : int = 0x86
PAR_OCD_BREAK_CAUSE : int = 0x87
PAR_EXTERNAL_RESET : int = 0x8B
PAR_TIMERS_RUNNING : int = 0xA0
PAR_CHANGE_OF_FLOW : int = 0xA1
PAR_BREAK_ADDR1_HIGH : int = 0xA2
PAR_BREAK_ADDR1_LOW : int = 0xA3
PAR_BREAK_ADDR2_HIGH : int = 0xA4
PAR_BREAK_ADDR2_LOW : int = 0xA5
PAR_COMB_BREAK_CTRL : int = 0xA6
PAR_JTAGID_BYTE0 : int = 0xA7     # to 0xAA
PAR_MCU_MODE : int = 0xB3

MEMTYPE_SRAM : int = 0x20         # registers, I/O and SRAM by data address
MEMTYPE_EEPROM : int = 0x22
MEMTYPE_IO_SHADOW : int = 0x30
MEMTYPE_BREAKPOINT : int = 0x60   # PSB0/PSB1: write 0 or 1 at the word address
MEMTYPE_PML : int = 0xA0          # flash through SPM/LPM, in debug mode
MEMTYPE_FLASH_PAGE : int = 0xB0   # these in programming mode
MEMTYPE_EEPROM_PAGE : int = 0xB1
MEMTYPE_FUSE : int = 0xB2
MEMTYPE_LOCK : int = 0xB3
MEMTYPE_SIGNATURE : int = 0xB4
MEMTYPE_OSCCAL : int = 0xB5

WORD_MEMTYPES : frozenset[int] = frozenset({MEMTYPE_PML, MEMTYPE_FLASH_PAGE})   # counted in words
# memory types whose reading has no side effects, so that an incomplete answer can be read again (not
# MEMTYPE_SRAM, which reaches the I/O registers, where a read may take a received byte out of a UART)
REREADABLE_MEMTYPES : frozenset[int] = frozenset({MEMTYPE_EEPROM, MEMTYPE_PML, MEMTYPE_FLASH_PAGE,
                                                  MEMTYPE_EEPROM_PAGE, MEMTYPE_FUSE, MEMTYPE_LOCK,
                                                  MEMTYPE_SIGNATURE, MEMTYPE_OSCCAL})
MAX_UNITS : int = 256             # words or bytes per read or write command

BAUD_CODES : dict[int, int] = { 9600 : 0xF4, 19200 : 0xFA, 38400 : 0xFD, 57600 : 0xFE, 115200 : 0xFF }
START_BAUD : int = 19200          # after power-up
SYNC_BAUDS : tuple[int, ...] = (19200, 115200, 57600, 38400, 9600)  # after a session that ended badly
FAST_BAUD : int = 115200
JTAG_CLOCK_CODES : dict[int, int] = { 1000 : 0xFF, 500 : 0xFE, 250 : 0xFD, 125 : 0xFB }  # kHz
PC_INVALID : int = 0xAA55AA       # READ_PC while the target runs
SIGN_ON : bytes = b'AVRNOCD'

TIMEOUT : float = 1.0             # s for an answer
POLL_SLICE : float = 0.1          # s, longest read in poll_break, during which a signal is deferred

DESCRIPTOR_SIZE : int = 123


class Jtag1Error(BackendError):
    """An answer that does not follow the protocol, or a command the probe refused"""

class Jtag1Timeout(Jtag1Error):
    """No answer within the timeout"""


@dataclass(frozen=True)
class Event:
    """A message the probe sent on its own"""
    kind : int                   # RESP_BREAK, RESP_INFO, RESP_SLEEP, RESP_POWER
    value : int                  # break status, IDR, sleep status; 0 for power


def io_masks(device_info : dict, masked : list[int] | None = None) -> bytes:
    """
    The 112 bytes of I/O masks of the mkI descriptor, in the order avrdude declares them:
    ucReadIO, ucWriteIO, ucReadIOShadow, ucWriteIOShadow (8 bytes each, memory addresses
    0x20-0x5F), then ucReadExtIO, ucWriteExtIO, ucReadIOExtShadow, ucWriteIOExtShadow (20 bytes
    each, 0x60-0xFF). The bits as for the mkII (see jtag2.io_masks): read except the read-sensitive
    registers, write except those and the read-only ones; the shadows stay zero.
    """
    masks = bytearray(112)
    if masked is None:
        masked = device_info.get('masked_registers', [])
    ronly = device_info.get('ronly_registers', [])
    for address in range(0x20, min(device_info['internal_sram_address_byte'], 0x100)):
        read_at, write_at, bit = ((0, 8, address - 0x20) if address < 0x60 else
                                  (32, 52, address - 0x60))
        if address not in masked:
            masks[read_at + bit // 8] |= 1 << (bit % 8)
            if address not in ronly:
                masks[write_at + bit // 8] |= 1 << (bit % 8)
    return bytes(masks)


# The extended I/O registers that exist (20 bytes from 0x60, a bit per address): those in the SVD
# data of the device files and those in AVR060's example descriptors, which lack some (PRR and TIMSK2
# of the ATmega169A, ADCSRB of the ATmega64) and have one the SVD data lack (0x7D on the ATmega169).
# Measured on an ATmega169A: with the read bit set for every address up to 0xFE, including those
# without a register, the probe hangs at the first I/O access after a stop; restricted to these,
# it does not (the ATmega128 was not affected). Taken once from the SVD data, which are to leave
# the device files. Read-sensitive and read-only registers stay out as before (io_masks).
EXT_IO_EXISTING : dict[str, bytes] = {
    'atmega64' : bytes.fromhex("3eb51f37ff5f213f000000000000000000000000"),
    'atmega64a' : bytes.fromhex("3eb51f37ff5f213f000000000000000000000000"),
    'atmega128' : bytes.fromhex("3eb51f37ff1f213f000000000000000000000000"),
    'atmega128a' : bytes.fromhex("3eb51f37ff1f213f000000000000000000000000"),
    'atmega162' : bytes.fromhex("02180030f30f0000000000000000000000000000"),
    'atmega169a' : bytes.fromhex("53da01fff70f000000004d0777000000f0f0de7b"),
    'atmega165a' : bytes.fromhex("53da01dff70f000000004d077700000000000000"),   # SVD only
    'atmega165p' : bytes.fromhex("53da01dff70f000000004d077700000000000000"),   # SVD only
    'atmega165pa' : bytes.fromhex("53da01dff70f000000004d077700000000000000"),   # SVD only
    'atmega645a' : bytes.fromhex("53da01dff70f000000004d077700000000000000"),   # SVD only
    # without the CAN controller (0xD8-0xFA): measured, with it the probe's refresh of its copy after a
    # step makes the next command fail (synchronization error); without it, or without 0xF0-0xFA, not
    'at90can128' : bytes.fromhex("43c633dff73ff73f00004d1f7777000000000000"),
    }


def existing_ext_io(device_info : dict) -> bytes | None:
    """The mask of the existing extended I/O registers, if known for this part"""
    return EXT_IO_EXISTING.get(device_info['name'])


# after the masks: ucIDRAddress, ucSPMCRAddress, ucRAMPZAddress, uiFlashPageSize, ucEepromPageSize,
# ulBootAddress, ucUpperExtIOLoc (avrdude's struct; AVR060's examples have the same 11 bytes)
DESCRIPTOR_TAIL = struct.Struct("<BBBHBIB")

def make_device_descriptor(device_info : dict, masked : list[int] | None = None) -> bytes:
    """
    The 123 bytes of Cmnd_Set_Device_Descriptor. Addresses as in AVR060's examples: IDR and RAMPZ
    as I/O addresses, SPMCR as a memory address (ATmega16: 0x31, 0x57). ulBootAddress is a word
    address; AVR060's examples give the start of the smallest boot section, the mkII descriptor
    the last page, which lies inside it.
    """
    flash_size : int = device_info['flash_size_bytes']
    page_size : int = device_info['flash_page_size_bytes']
    tail = DESCRIPTOR_TAIL.pack(
        device_info.get('ocd_base', 0),                      # ucIDRAddress
        device_info.get('spmcsr_base', 0),                   # ucSPMCRAddress
        0x3B if flash_size > 0x10000 else 0,                 # ucRAMPZAddress
        page_size,                                           # uiFlashPageSize
        device_info['eeprom_page_size_bytes'],               # ucEepromPageSize
        (flash_size - page_size) // 2,                       # ulBootAddress
        upper_ext_io(device_info))                           # ucUpperExtIOLoc
    masks = bytearray(io_masks(device_info, masked))
    existing = existing_ext_io(device_info)
    if existing is not None:
        for i in range(20):
            masks[32 + i] &= existing[i]
            masks[52 + i] &= existing[i]
    return bytes(masks) + tail


# ucUpperExtIOLoc, the topmost extended I/O register, for the mkI parts that have extended I/O. The
# same values as in AVR060's examples, and as the highest register below the SRAM in the SVD data
# (checked for ATmega64, 128, 162, 169P); not computed from the SVD dict, which is to leave the
# device files.
UPPER_EXT_IO : dict[str, int] = { 'atmega64' : 0x9D, 'atmega128' : 0x9D, 'atmega162' : 0x8B,
                                  'atmega169' : 0xFE, 'atmega165' : 0xC6, 'at90can128' : 0xFA,
                                  'atmega645' : 0xC6 }

def upper_ext_io(device_info : dict) -> int:
    """The topmost extended I/O location, 0 without extended I/O"""
    if device_info['internal_sram_address_byte'] <= 0x60:
        return 0
    for prefix, top in UPPER_EXT_IO.items():
        if device_info['name'].startswith(prefix):
            return top
    return min(device_info['internal_sram_address_byte'], 0x100) - 1


def pc_bytes(word_address : int) -> bytes:
    """The program counter as the probe expects it: word address plus one, three bytes MSB first"""
    return (word_address + 1).to_bytes(3, 'big')


class Jtag1SerialTransport():
    """The serial line to the probe. Read timeouts are raised as TimeoutError."""
    def __init__(self, port : str) -> None:
        self.logger : logging.Logger = logging.getLogger(__name__)
        self.port : str = port
        self.serial : serial.Serial = serial.Serial()
        self.serial.port = port
        self.serial.baudrate = START_BAUD
        self.serial.timeout = 0.01
        self.serial.dtr = False
        self.serial.rts = False
        self.serial.exclusive = True
        try:
            self.serial.open()
        except serial.SerialException as e:
            raise Jtag1Error("Cannot open {}: {}".format(port, e)) from e

    def flush(self) -> None:
        """Discard what has arrived so far"""
        self.serial.reset_input_buffer()

    def write(self, data : bytes) -> None:
        """Send bytes"""
        try:
            self.serial.write(data)
        except serial.SerialException as e:
            raise Jtag1Error("Serial error on {}: {}".format(self.port, e)) from e

    def read(self, count : int, timeout : float = TIMEOUT) -> bytes:
        """Exactly count bytes, waiting at most timeout seconds"""
        deadline = time.monotonic() + timeout
        data = bytearray()
        while len(data) < count:
            try:
                data += self.serial.read(count - len(data))
            except serial.SerialException as e:
                raise Jtag1Error("Serial error on {}: {}".format(self.port, e)) from e
            if len(data) < count and time.monotonic() >= deadline:
                raise TimeoutError("{} of {} bytes on {} within {} s: {}".format(
                    len(data), count, self.port, timeout, bytes(data).hex()))
        return bytes(data)

    def set_baudrate(self, baud : int) -> None:
        """Switch the host side"""
        self.serial.baudrate = baud
        time.sleep(0.01)

    def close(self) -> None:
        """Release the port"""
        try:
            self.serial.close()
        except serial.SerialException:
            pass


#pylint: disable=too-many-public-methods # one method per AVR060 command
class Jtag1Protocol():
    """The commands of AVR060 and their answers"""
    def __init__(self, transport : Jtag1SerialTransport) -> None:
        self.logger : logging.Logger = logging.getLogger(__name__)
        self.transport : Jtag1SerialTransport = transport
        self.events : list[Event] = []

    # --- answers ---

    def _byte(self, timeout : float = TIMEOUT) -> int:
        try:
            return self.transport.read(1, timeout)[0]
        except TimeoutError as e:
            raise Jtag1Timeout("No answer from the probe: {}".format(e)) from e

    def _bytes(self, count : int, timeout : float = TIMEOUT) -> bytes:
        try:
            return self.transport.read(count, timeout)
        except TimeoutError as e:
            raise Jtag1Timeout("Incomplete answer from the probe: {}".format(e)) from e

    def _event(self, kind : int, timeout : float = TIMEOUT) -> Event:
        """The rest of a message the probe sent on its own, whose first byte was 'kind'"""
        if kind == RESP_BREAK:
            return Event(kind, int.from_bytes(self._bytes(2, timeout), 'big'))
        if kind in (RESP_INFO, RESP_SLEEP):
            value, ok = self._bytes(2, timeout)
            if ok != RESP_OK:
                self.logger.debug("Message 0x%02X 0x%02X ends with 0x%02X", kind, value, ok)
            return Event(kind, value)
        return Event(kind, 0)                             # RESP_POWER

    def _ack(self, what : str, timeout : float = TIMEOUT) -> None:
        """
        The Resp_OK for the Sync_CRC/EOP of a command. Messages the probe sent on its own before
        it are set aside; after Resp_SYNC_ERROR the command has not been executed.
        """
        while True:
            first = self._byte(timeout)
            if first == RESP_OK:
                return
            if first in (RESP_BREAK, RESP_INFO, RESP_SLEEP, RESP_POWER):
                event = self._event(first, timeout)
                self.logger.debug("Set aside: %s", event)
                self.events.append(event)
                continue
            if first == RESP_SYNC_ERROR:
                self.resync()
                raise Jtag1Error("{}: synchronization error".format(what))
            self.resync()
            raise Jtag1Error("{}: unexpected answer 0x{:02X}".format(what, first))

    def _status(self, what : str, timeout : float = TIMEOUT) -> None:
        """The Resp_OK or Resp_FAILED that ends an answer"""
        last = self._byte(timeout)
        if last == RESP_FAILED:
            raise Jtag1Error("{}: failed".format(what))
        if last != RESP_OK:
            self.resync()
            raise Jtag1Error("{}: unexpected end of answer 0x{:02X}".format(what, last))

    def command(self, cmd : bytes, answer : int, what : str, timeout : float = TIMEOUT) -> bytes:
        """
        Send cmd with Sync_CRC/EOP, take the acknowledgment, then 'answer' bytes and the closing
        Resp_OK/Resp_FAILED; returns the 'answer' bytes
        """
        with transaction(): # SIGTERM/SIGINT must not cut a command from its answer
            self.transport.write(bytes(cmd) + EOP)
            self._ack(what, timeout)
            data = self._bytes(answer, timeout) if answer else b''
            self._status(what, timeout)
            return data

    def resync(self) -> None:
        """
        Get back in step: send Cmd_GET_SYNC until the probe answers Resp_OK (AVR060), dropping what
        else arrives
        """
        for _ in range(20):
            self.transport.flush()
            self.transport.write(bytes([CMD_GET_SYNC]))
            try:
                if self.transport.read(1, 0.1)[0] == RESP_OK:
                    time.sleep(0.02)
                    self.transport.flush()
                    return
            except TimeoutError:
                pass
        raise Jtag1Timeout("The probe does not answer Get Sync")

    # --- connection ---

    def sync(self, bauds : tuple[int, ...] = SYNC_BAUDS) -> int:
        """
        Find the speed the probe listens at: after power-up 19200, after a session that ended
        without switching back the last one. 'SE' and EOP first: after other characters the probe
        is in some internal mode that this ends (avarice). Returns the speed.
        """
        for baud in bauds:
            self.transport.set_baudrate(baud)
            for _ in range(2):
                self.transport.write(b'SE' + EOP)
                time.sleep(0.1)
                self.transport.flush()
                try:
                    if self.sign_on(timeout=0.3) == SIGN_ON.decode():
                        return baud
                except Jtag1Error:
                    pass
        raise Jtag1Timeout("No JTAGICE mkI answers at {} bps".format(", ".join(str(b) for b in bauds)))

    def sign_on(self, timeout : float = TIMEOUT) -> str:
        """Cmd_GET_SIGN_ON: 'AVRNOCD'"""
        return self.command(bytes([CMD_GET_SIGN_ON]), len(SIGN_ON), "Sign-on", timeout).decode(errors='replace')

    def get_parameter(self, parameter : int) -> int:
        """Cmd_GET_PARAMETER"""
        return self.command(bytes([CMD_GET_PARAMETER, parameter]), 1,
                            "Get parameter 0x{:02X}".format(parameter))[0]

    def set_parameter(self, parameter : int, value : int) -> None:
        """Cmd_SET_PARAMETER"""
        self.command(bytes([CMD_SET_PARAMETER, parameter, value]), 0, "Set parameter 0x{:02X}".format(parameter))

    def set_baud(self, baud : int) -> None:
        """The probe acknowledges at the old speed and switches after it; then the host follows"""
        if baud not in BAUD_CODES:
            raise Jtag1Error("{} bps is not a speed of the JTAGICE mkI".format(baud))
        self.set_parameter(PAR_BAUD_RATE, BAUD_CODES[baud])
        self.transport.set_baudrate(baud)

    def set_device_descriptor(self, descriptor : bytes) -> None:
        """Cmd_Set_Device_Descriptor"""
        if len(descriptor) != DESCRIPTOR_SIZE:
            raise Jtag1Error("A device descriptor has {} bytes, not {}".format(DESCRIPTOR_SIZE, len(descriptor)))
        self.command(bytes([CMD_SET_DEVICE_DESCRIPTOR]) + bytes(descriptor), 0, "Set device descriptor")

    def jtag_id(self) -> int:
        """The JTAG ID of the target, from parameters 0xA7-0xAA"""
        return int.from_bytes(bytes(self.get_parameter(PAR_JTAGID_BYTE0 + i) for i in range(4)), 'little')

    # --- memory ---

    def read_memory(self, memtype : int, address : int, numbytes : int) -> bytes:
        """
        Cmd_READ_MEMORY: numbytes from address (a word address for the flash types, a byte address
        otherwise), in commands of at most MAX_UNITS units. PML words come MSB first and are
        returned in flash order.
        """
        unit = 2 if memtype in WORD_MEMTYPES else 1
        if numbytes % unit:
            raise Jtag1Error("Flash is read in words: odd count {}".format(numbytes))
        data = bytearray()
        while len(data) < numbytes:
            units = min(MAX_UNITS, (numbytes - len(data)) // unit)
            chunk = self._read_chunk(memtype, address, units, unit)
            if memtype == MEMTYPE_PML:
                chunk = b''.join(chunk[i + 1:i + 2] + chunk[i:i + 1] for i in range(0, len(chunk), 2))
            data += chunk
            address += units
        return bytes(data)

    def _read_chunk(self, memtype : int, address : int, units : int, unit : int) -> bytes:
        """
        One Cmd_READ_MEMORY. Measured on an AT90CAN128 in the e2e runs: now and then bytes of a flash page
        get lost on the way (16 in the middle of 256, the end arrived); not reproducible in 200 reads
        and writes in a row. So an incomplete answer is read once more where reading has no side effects.
        """
        command = bytes([CMD_READ_MEMORY, memtype, units - 1]) + address.to_bytes(3, 'big')
        what = "Read memory 0x{:02X}:0x{:X}".format(memtype, address)
        try:
            return self.command(command, units * unit + 1, what)[:-1]   # and the checksum, always 0
        except Jtag1Timeout as e:
            if memtype not in REREADABLE_MEMTYPES:
                raise
            self.logger.warning("%s: incomplete answer, reading again (%s)", what, e)
            self.transport.flush()
            self.resync()
            return self.command(command, units * unit + 1, what)[:-1]

    def write_memory(self, memtype : int, address : int, data : bytes, timeout : float = TIMEOUT) -> None:
        """
        Cmd_WRITE_MEMORY and the data block (Cmd_DATA), in commands of at most MAX_UNITS units;
        address as for read_memory. PML words are sent MSB first.
        """
        unit = 2 if memtype in WORD_MEMTYPES else 1
        if len(data) % unit:
            raise Jtag1Error("Flash is written in words: odd count {}".format(len(data)))
        what = "Write memory 0x{:02X}:0x{:X}".format(memtype, address)
        for start in range(0, len(data), MAX_UNITS * unit):
            chunk = bytes(data[start:start + MAX_UNITS * unit])
            if memtype == MEMTYPE_PML:
                chunk = b''.join(chunk[i + 1:i + 2] + chunk[i:i + 1] for i in range(0, len(chunk), 2))
            with transaction():
                self.transport.write(bytes([CMD_WRITE_MEMORY, memtype, len(chunk) // unit - 1]) +
                                     address.to_bytes(3, 'big') + EOP)
                self._ack(what)
                self.transport.write(bytes([CMD_DATA]) + chunk + EOP)
                self._ack(what, timeout)
                self._status(what, timeout)
            address += len(chunk) // unit

    def erase_page_spm(self, address : int) -> None:
        """
        Cmd_ERASEPAGE_SPM: erase the flash page at a byte address, in debug mode. AVR060 gives the
        address as a word; the probe waits for a third byte (avarice sends a zero there).
        """
        self.command(bytes([CMD_ERASEPAGE_SPM]) + address.to_bytes(2, 'big') + b'\x00', 0,
                     "Erase page 0x{:X}".format(address))

    # --- execution ---

    def read_pc(self) -> int:
        """Cmd_READ_PC: a word address; an error while the target runs"""
        raw = int.from_bytes(self.command(bytes([CMD_READ_PC]), 3, "Read PC"), 'big')
        if raw == PC_INVALID:
            raise Jtag1Error("Read PC: the target runs")
        # Measured: right after OCDEN has been programmed and programming mode left, the probe
        # reports 0, which is no PC plus one; the target is at the reset vector then
        return max(raw - 1, 0)

    def write_pc(self, pc : int) -> None:
        """Cmd_WRITE_PC: a word address"""
        self.command(bytes([CMD_WRITE_PC]) + pc_bytes(pc), 0, "Write PC")

    def go(self) -> None:
        """Cmd_GO"""
        with transaction():
            self.transport.write(bytes([CMD_GO]) + EOP)
            self._ack("Go")

    def single_step(self, timeout : float = TIMEOUT) -> None:
        """Cmd_SINGLE_STEP"""
        self.command(bytes([CMD_SINGLE_STEP]), 0, "Single step", timeout)

    def forced_stop(self) -> None:
        """
        Cmd_FORCED_STOP. The program counter in the answer is ignored: avarice found it wrong after
        branches, and READ_PC gives it anyway.
        """
        self.command(bytes([CMD_FORCED_STOP]), 3, "Stop")

    def reset(self, timeout : float = TIMEOUT) -> None:
        """Cmd_RESET: the target stops at 0"""
        self.command(bytes([CMD_RESET]), 0, "Reset", timeout)

    def set_program_breakpoint(self, number : int, pc : int) -> None:
        """PSB0 (number 0) or PSB1 (number 1) at a word address, valid for the next GO"""
        self.write_memory(MEMTYPE_BREAKPOINT, pc, bytes([number]))

    def poll_break(self, timeout : float = 0) -> int | None:
        """
        The break status of the next Resp_BREAK, waiting at most timeout seconds; None if there is
        none. Other messages are logged and dropped, stray bytes too.
        """
        deadline = time.monotonic() + timeout
        while True:
            while self.events:
                event = self.events.pop(0)
                if event.kind == RESP_BREAK:
                    return event.value
                self.logger.debug("Message dropped: %s", event)
            remaining = deadline - time.monotonic()
            with transaction():
                try:
                    first : int | None = self.transport.read(1, min(max(remaining, 0.001), POLL_SLICE))[0]
                except TimeoutError:
                    first = None
                if first in (RESP_BREAK, RESP_INFO, RESP_SLEEP, RESP_POWER):
                    self.events.append(self._event(first))
                elif first is not None and first != RESP_OK:
                    self.logger.debug("Unexpected byte while running: 0x%02X", first)
            if first is None and remaining <= POLL_SLICE:
                return None

    def wait_for_break(self, timeout : float = TIMEOUT) -> int:
        """The break status of the next Resp_BREAK; an error if it does not come in time"""
        result = self.poll_break(timeout)
        if result is None:
            raise Jtag1Error("No break within {} s".format(timeout))
        return result

    # --- programming mode ---

    def enter_progmode(self) -> None:
        """Enter Progmode"""
        self.command(bytes([CMD_ENTER_PROGMODE]), 0, "Enter programming mode", 2 * TIMEOUT)

    def leave_progmode(self) -> None:
        """Leave Progmode"""
        self.command(bytes([CMD_LEAVE_PROGMODE]), 0, "Leave programming mode", 2 * TIMEOUT)

    def chip_erase(self) -> None:
        """Chip Erase, in programming mode"""
        self.command(bytes([CMD_CHIP_ERASE]), 0, "Chip erase", 5 * TIMEOUT)
