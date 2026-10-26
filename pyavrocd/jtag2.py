"""
The JTAGICE mkII protocol (Atmel application note AVR067) over USB bulk transfers,
spoken by the JTAGICE mkII, its clones, and the AVR Dragon, and over a serial line,
spoken by dw-link from version 7 on.

This module covers the layers below the debugging commands: framing and CRC,
the USB and the serial transport, discovery of the probes, and sign-on.
"""
from dataclasses import dataclass
import logging
import struct
import time

import serial
import usb.core
import usb.util

from pyavrocd.backend import BackendError, ProbeCandidate
from pyavrocd.termination import transaction
from pyavrocd.xavr8target import tiny_device_data

VENDOR_ATMEL : int = 0x03EB
PRODUCTS : dict[int, str] = { 0x2103 : 'jtagice2', # JTAGICE mkII and clones
                              0x2107 : 'dragon' }  # AVR Dragon

MESSAGE_START : int = 0x1B
TOKEN : int = 0x0E
EVENT_SEQUENCE : int = 0xFFFF # sequence number of messages the probe sends on its own
HEADER_SIZE : int = 8         # MESSAGE_START, SEQUENCE_NUMBER (2), MESSAGE_SIZE (4), TOKEN
CRC_SIZE : int = 2

CMND_SIGN_OFF : int = 0x00
CMND_GET_SIGN_ON : int = 0x01
CMND_SET_PARAMETER : int = 0x02
CMND_GET_PARAMETER : int = 0x03
CMND_WRITE_MEMORY : int = 0x04
CMND_READ_MEMORY : int = 0x05
CMND_WRITE_PC : int = 0x06
CMND_READ_PC : int = 0x07
CMND_GO : int = 0x08
CMND_SINGLE_STEP : int = 0x09
CMND_FORCED_STOP : int = 0x0A
CMND_RESET : int = 0x0B
CMND_SET_DEVICE_DESCRIPTOR : int = 0x0C
CMND_ERASEPAGE_SPM : int = 0x0D
CMND_SET_BREAK : int = 0x11
CMND_CHIP_ERASE : int = 0x13
CMND_ENTER_PROGMODE : int = 0x14
CMND_LEAVE_PROGMODE : int = 0x15
CMND_CLR_BREAK : int = 0x1A
CMND_RUN_TO_ADDR : int = 0x1C
CMND_RESTORE_TARGET : int = 0x23
CMND_ISP_PACKET : int = 0x2F
CMND_SET_DEVICE_CONTEXT : int = 0x36 # not in AVR067; Microchip Studio 7 sends it (see make_device_context)
RSP_SPI_DATA : int = 0x88
RESET_DEBUGWIRE_DISABLE : int = 0x04  # flag of CMND_RESET
BREAK_PROGRAM : int = 0x01           # type of CMND_SET_BREAK
BREAK_MODE_PROGRAM : int = 0x03      # mode of CMND_SET_BREAK
SOFTWARE_BREAKPOINT : int = 0x00     # breakpoint number of a software breakpoint
RSP_OK : int = 0x80
RSP_PARAMETER : int = 0x81
RSP_MEMORY : int = 0x82
RSP_PC : int = 0x84
RSP_SIGN_ON : int = 0x86
EVT_BREAK : int = 0xE0
EVT_IDR_DIRTY : int = 0xEC   # the target program wrote OCDR (AVR067 6.2.9); dropped so far
LOW_LEVEL : int = 0x01       # flag of CMND_SINGLE_STEP, CMND_FORCED_STOP, CMND_RESET
STEP_INTO : int = 0x01
RSP_FAILURES : dict[int, str] = { 0xA0 : "RSP_FAILED", 0xA1 : "RSP_ILLEGAL_PARAMETER",
                                  0xA2 : "RSP_ILLEGAL_MEMORY_TYPE", 0xA3 : "RSP_ILLEGAL_MEMORY_RANGE",
                                  0xA4 : "RSP_ILLEGAL_EMULATOR_MODE", 0xA5 : "RSP_ILLEGAL_MCU_STATE",
                                  0xA6 : "RSP_ILLEGAL_VALUE", 0xA8 : "RSP_ILLEGAL_BREAKPOINT",
                                  0xA9 : "RSP_ILLEGAL_JTAG_ID", 0xAA : "RSP_ILLEGAL_COMMAND",
                                  0xAB : "RSP_NO_TARGET_POWER", 0xAC : "RSP_DEBUGWIRE_SYNC_FAILED",
                                  0xAD : "RSP_ILLEGAL_POWER_STATE" }

# parameters (AVR067 section 8)
PAR_HW_VERSION : int = 0x01
PAR_FW_VERSION : int = 0x02
PAR_EMULATOR_MODE : int = 0x03
PAR_BAUD_RATE : int = 0x05
EMULATOR_MODE_DEBUGWIRE : int = 0x00
EMULATOR_MODE_JTAG : int = 0x01
EMULATOR_MODE_UNKNOWN : int = 0x02
EMULATOR_MODE_SPI : int = 0x03
PAR_OCD_VTARGET : int = 0x06
PAR_OCD_JTAG_CLK : int = 0x07
PAR_OCD_BREAK_CAUSE : int = 0x08
PAR_TIMERS_RUNNING : int = 0x09
PAR_JTAGID : int = 0x0E
PAR_EXTERNAL_RESET : int = 0x13
PAR_MCU_STATE : int = 0x1A
PAR_TARGET_SIGNATURE : int = 0x1D   # in debugWIRE mode, LSB first
PAR_SOFT_RESET : int = 0x2D         # AVR067 rev. D: 'soft reset (after signing off)', write only
SOFT_RESET_NONE : int = 0x03        # no reset: the probe stays on the bus after CMND_SIGN_OFF; 0x00 (hard
                                    # reset, the default after power-up) makes it re-enumerate (measured)
MCU_STATES : dict[int, str] = { 0x00 : "STOPPED", 0x01 : "RUNNING", 0x02 : "PROGRAMMING" }

# memory types (AVR067 section 10); addresses are byte addresses for all of them
MEMTYPE_SRAM : int = 0x20   # 0x00-0x1F registers, then I/O, then SRAM
MEMTYPE_EEPROM : int = 0x22
MEMTYPE_SPM : int = 0xA0    # flash, readable in debug mode
MEMTYPE_FLASH_PAGE : int = 0xB0
MEMTYPE_EEPROM_PAGE : int = 0xB1
MEMTYPE_FUSE : int = 0xB2
MEMTYPE_LOCK : int = 0xB3
MEMTYPE_SIGNATURE : int = 0xB4

USB_TIMEOUT : int = 2000      # ms for one USB packet
SERIAL_START_BAUD : int = 19200 # a serial mkII starts at this speed (AVR067 section 2.1.1)
BAUD_CODES : dict[int, int] = { 2400 : 1, 4800 : 2, 9600 : 3, 14400 : 8, 19200 : 4, 38400 : 5,
                                57600 : 6, 115200 : 7 }  # values of PAR_BAUD_RATE
MAX_SERIAL_BODY : int = 1024  # a longer announced body is noise, and the receiver resynchronizes
MODE_TIMEOUT : int = 5000     # ms for switching the emulator mode, which talks to the target: refusing
                              # the SPI mode while debugWIRE is active took 1 s once, more than 2 s another time


class Jtag2Error(BackendError):
    """A frame or a response that does not follow the protocol"""

class Jtag2UsbError(Jtag2Error):
    """The USB transfer of a command or its response failed"""

class Jtag2Timeout(Jtag2Error):
    """No response within the timeout, whatever the transport"""

class Jtag2UsbTimeout(Jtag2UsbError, Jtag2Timeout):
    """No response within the timeout on USB"""


def _crc_table() -> list[int]:
    """CRC-16 table of AVR067 section 12: reflected CCITT polynomial 0x8408"""
    table = []
    for i in range(256):
        crc = i
        for _ in range(8):
            crc = (crc >> 1) ^ 0x8408 if crc & 1 else crc >> 1
        table.append(crc)
    return table

CRC_TABLE : list[int] = _crc_table()


def crc16(data : bytes, crc : int = 0xFFFF) -> int:
    """CRC-16 of AVR067: initial value 0xFFFF, no final xor"""
    for byte in data:
        crc = (crc >> 8) ^ CRC_TABLE[(crc ^ byte) & 0xFF]
    return crc


def make_frame(sequence : int, body : bytes) -> bytes:
    """A complete message: header, body, CRC (all LSB first)"""
    frame = struct.pack("<BHIB", MESSAGE_START, sequence, len(body), TOKEN) + bytes(body)
    return frame + struct.pack("<H", crc16(frame))


def parse_frame(frame : bytes) -> tuple[int, bytes]:
    """
    Check a received message and return its sequence number and body
    """
    if len(frame) < HEADER_SIZE + 1 + CRC_SIZE:
        raise Jtag2Error("Frame too short: {}".format(bytes(frame).hex()))
    start, sequence, size, token = struct.unpack_from("<BHIB", frame)
    if start != MESSAGE_START or token != TOKEN:
        raise Jtag2Error("Not a JTAGICE mkII frame: {}".format(bytes(frame[:HEADER_SIZE]).hex()))
    if len(frame) < HEADER_SIZE + size + CRC_SIZE:
        raise Jtag2Error("Frame of {} bytes announces a body of {}".format(len(frame), size))
    end = HEADER_SIZE + size
    if struct.unpack_from("<H", frame, end)[0] != crc16(frame[:end]):
        raise Jtag2Error("CRC error in frame {}".format(bytes(frame[:end + CRC_SIZE]).hex()))
    return sequence, bytes(frame[HEADER_SIZE:end])


@dataclass(frozen=True)
class SignOn:
    """Contents of RSP_SIGN_ON (AVR067 section 5.2.16)"""
    protocol : int
    master_firmware : tuple[int, int]  # (major, minor)
    master_hardware : int
    slave_firmware : tuple[int, int]
    slave_hardware : int
    serial : str                       # as the USB descriptor shows it
    ident : str                        # 'JTAGICEmkII', 'AVRDRAGON'


def parse_sign_on(body : bytes) -> SignOn:
    """Decode RSP_SIGN_ON"""
    if len(body) < 17 or body[0] != RSP_SIGN_ON:
        raise Jtag2Error("Not a sign-on response: {}".format(body.hex()))
    return SignOn(protocol=body[1],
                  master_firmware=(body[4], body[3]), master_hardware=body[5],
                  slave_firmware=(body[8], body[7]), slave_hardware=body[9],
                  # AVR067 calls the serial number 'LSB first'; in this order it is
                  # exactly the serial number of the USB descriptor
                  serial=body[10:16].hex().upper(),
                  ident=body[16:].split(b"\0")[0].decode(errors="replace"))


# the layout of CMND_SET_DEVICE_DESCRIPTOR after the 240 bytes of I/O masks (AVR067 section 9;
# the field order as avrdude sends it, which decodes a captured frame consistently)
DESCRIPTOR_TAIL = struct.Struct("<BBBHBIHI20s3sBBHBBBHBBHBBBBH")
DESCRIPTOR_SIZE : int = 240 + DESCRIPTOR_TAIL.size  # 298

def io_masks(device_info : dict) -> bytes:
    """
    The 240 bytes of I/O masks: ucReadIO, ucReadIOShadow, ucWriteIO, ucWriteIOShadow (8 bytes each,
    memory addresses 0x20-0x5F), then the four ext arrays (52 bytes each, from 0x60). Measured on the
    mkII clone: at every break the probe reads the registers whose ucReadIO bit is set, and serves
    reads from that copy; registers without the bit read as 0 (only PINA and SREG were read anyway).
    So the read-sensitive ones (masked_registers) must stay out. Writes reach the target with or
    without the bit; the write bits go to neither ronly nor masked registers, presumably because the
    probe writes them back at GO -- which would clear interrupt flags or send a byte through UDR.
    The shadow arrays stay zero. The ext range ends where the SRAM begins.
    """
    masks = bytearray(240)
    masked = device_info.get('masked_registers', [])
    ronly = device_info.get('ronly_registers', [])
    for address in range(0x20, min(device_info['internal_sram_address_byte'], 0x60 + 52 * 8)):
        read_at, write_at, bit = ((0, 16, address - 0x20) if address < 0x60 else
                                  (32, 136, address - 0x60))
        if address not in masked:
            masks[read_at + bit // 8] |= 1 << (bit % 8)
            if address not in ronly:
                masks[write_at + bit // 8] |= 1 << (bit % 8)
    return bytes(masks)

def _in(register : int, address : int) -> int:
    """opcode of 'in register, address'"""
    return 0xB000 | (address & 0x30) << 5 | register << 4 | address & 0x0F

def _out(address : int, register : int) -> int:
    """opcode of 'out address, register'"""
    return 0xB800 | (address & 0x30) << 5 | register << 4 | address & 0x0F

def _sbic(address : int, bit : int) -> int:
    """opcode of 'sbic address, bit'"""
    return 0x9900 | address << 3 | bit

def debugwire_instructions(device_info : dict) -> tuple[bytes, bytes]:
    """
    ucEepromInst and ucFlashInst: opcodes, high byte first, that the probe executes on a debugWIRE
    target. Derived from the I/O addresses; checked against avrdude.conf for m328p, m168pb, m88,
    t85, t13, t2313 and t441 (its t1634 entry carries the m328p addresses, the device info does not).
    The third byte of ucFlashInst is the low byte of 'out DWDR, r1'.
    """
    eear, eecr, eedr = device_info['eear_base'], device_info['eecr_base'], device_info['eedr_base']
    dwdr = device_info['ocd_base']
    eeprom = [_out(eear + device_info.get('eear_size', 1) - 1, 31), _out(eear, 30), _out(eecr, 28),
              _in(0, eedr), _out(dwdr, 0), _in(0, dwdr), _out(eedr, 0), _out(eecr, 27),
              _sbic(eecr, 1), _out(eecr, 26)]
    return (b"".join(op.to_bytes(2, 'big') for op in eeprom),
            _in(0, dwdr).to_bytes(2, 'big') + bytes([_out(dwdr, 1) & 0xFF]))

def make_device_descriptor(device_info : dict) -> bytes:
    """
    The device descriptor for CMND_SET_DEVICE_DESCRIPTOR from PyAvrOCD's device info.
    I/O addresses as the mkII expects them, which is not the convention of the device info:
    IDR, RAMPZ as I/O addresses; SPMCR, EECR as memory addresses.
    The probe applies a new descriptor only from the next break on.
    """
    flash_size : int = device_info['flash_size_bytes']
    page_size : int = device_info['flash_page_size_bytes']
    tail = DESCRIPTOR_TAIL.pack(
        device_info.get('ocd_base', 0),                      # ucIDRAddress
        device_info.get('spmcsr_base', 0),                   # ucSPMCRAddress
        0x3B if flash_size > 0x10000 else 0,                 # ucRAMPZAddress
        page_size,                                           # uiFlashPageSize
        device_info['eeprom_page_size_bytes'],               # ucEepromPageSize
        (flash_size - page_size) // 2,                       # ulBootAddress: last page, in words. Measured on
                                                             # the mkII: the probe plants software breakpoints
                                                             # with SPM from here; with 0 (as avrdude sends it)
                                                             # they are never planted and GO takes 2.7 s
        0,                                                   # uiUpperExtIOLoc
        flash_size,                                          # ulFlashSize
        *(debugwire_instructions(device_info) if 'debugWIRE' in device_info.get('interface', '')
          else (bytes(20), bytes(3))),                       # ucEepromInst, ucFlashInst
        0, 0,                                                # ucSPHaddr, ucSPLaddr
        flash_size // page_size,                             # uiFlashpages
        0, 0, 0,                                             # ucDWDRAddress, ucDWBasePC, ucAllowFullPageBitstream
        ((flash_size - page_size) // 2) & 0xFFFF,            # uiStartSmallestBootLoaderSection: last page,
                                                             # as EDBG's boot_base, in words; 16 bits only,
                                                             # avrdude truncates it the same way (m2560)
        1,                                                   # EnablePageProgramming: avrdude sends 1, also for dW
        0,                                                   # ucCacheType
        0,                                                   # uiSramStartAddr
        0, 0, 0,                                             # ucResetType, ucPCMaskExtended, ucPCMaskHigh
        0,                                                   # ucEindAddress: avrdude sends 0 even for the m2560
        device_info['eecr_base'] + 0x20)                     # EECRAddress
    return io_masks(device_info) + tail

def make_device_context(device_info : dict) -> list[tuple[int, bytes]]:
    """
    The sections of CMND_SET_DEVICE_CONTEXT (0x36, undocumented; avrdude names it
    CMND_SET_XMEGA_PARAMS), as Microchip Studio 7 sends them to the JTAGICE mkII (captured): 0x02 the
    31 bytes of EDBG's TINY device data, 0x80/0x88 the read/write masks of I/O 0x20-0x5F, 0x81/0x89
    those of the extended I/O 0x60-0xFF. Unlike the device descriptor, the device data carry the page
    buffers per flash block, which the parts with a 4-page erase need.
    """
    masks = io_masks(device_info)
    return [(0x02, bytes(tiny_device_data(device_info))), (0x80, masks[0:8]), (0x88, masks[16:24]),
            (0x81, masks[32:52]), (0x89, masks[136:156])]


class Jtag2Isp():
    """
    ISP programming through a probe speaking the mkII protocol: the AVRISP mkII commands, with the
    parameters and the SPI instructions pyedbglib's avrispprotocol uses for the classic AVRs
    """
    ENTER_PROGMODE : int = 0x10
    LEAVE_PROGMODE : int = 0x11
    CHIP_ERASE : int = 0x12
    PROGRAM_FLASH : int = 0x13
    LOAD_ADDRESS : int = 0x06
    PROGRAM_FUSE : int = 0x17
    READ_FUSE : int = 0x18
    PROGRAM_LOCK : int = 0x19
    READ_LOCK : int = 0x1A
    READ_SIGNATURE : int = 0x1B
    READ_FUSE_INSTRUCTIONS : tuple[bytes, ...] = (b"\x50\x00\x00\x00", b"\x58\x08\x00\x00", b"\x50\x08\x00\x00")
    WRITE_FUSE_INSTRUCTIONS : tuple[bytes, ...] = (b"\xac\xa0\x00", b"\xac\xa8\x00", b"\xac\xa4\x00")

    def __init__(self, protocol : 'Jtag2Protocol') -> None:
        self.protocol = protocol
        self.spi_mode : bool = False      # SPI emulator mode set
        self.programming : bool = False   # ISP programming mode entered

    def enter(self) -> None:
        """
        SPI emulator mode, then ISP programming mode: timeout 200 (as avrdude), stabilisation delay
        100, command delay 25, 32 sync loops, poll value 0x53 at index 3, 'Programming Enable'.
        Each step only if not done yet: the SPI mode set again while in programming mode is
        answered with RSP_FAILED (measured on the AVR Dragon).
        """
        if not self.spi_mode:
            self.protocol.set_parameter(PAR_EMULATOR_MODE, bytes([EMULATOR_MODE_SPI]), MODE_TIMEOUT)
            self.spi_mode = True
        if not self.programming:
            self.protocol.isp(bytes([self.ENTER_PROGMODE, 200, 100, 25, 32, 0, 0x53, 3, 0xAC, 0x53, 0, 0]), 2)
            self.programming = True

    def leave(self) -> None:
        """Leave ISP programming mode (1 ms before and after releasing RESET); the SPI mode stays"""
        if self.programming:
            self.protocol.isp(bytes([self.LEAVE_PROGMODE, 1, 1]), 2)
            self.programming = False

    def close(self) -> None:
        """Leave programming mode and the SPI emulator mode"""
        self.leave()
        if self.spi_mode:
            self.protocol.set_parameter(PAR_EMULATOR_MODE, bytes([EMULATOR_MODE_UNKNOWN]), MODE_TIMEOUT)
            self.spi_mode = False

    def _read(self, command : int, instruction : bytes) -> int:
        return self.protocol.isp(bytes([command, 4]) + instruction, 4)[0]

    def signature(self) -> int:
        """The three signature bytes as one number, e.g. 0x1E950F"""
        return int.from_bytes(bytes(self._read(self.READ_SIGNATURE, bytes([0x30, 0, i, 0])) for i in range(3)), 'big')

    def read_fuse(self, index : int) -> int:
        """Low (0), high (1) or extended (2) fuse"""
        return self._read(self.READ_FUSE, self.READ_FUSE_INSTRUCTIONS[index])

    def write_fuse(self, index : int, value : int) -> None:
        """Program low (0), high (1) or extended (2) fuse; the answer has a second status byte"""
        self.protocol.isp(bytes([self.PROGRAM_FUSE]) + self.WRITE_FUSE_INSTRUCTIONS[index] + bytes([value]), 3)

    def read_lock(self) -> int:
        """Lock byte"""
        return self._read(self.READ_LOCK, b"\x58\x00\x00\x00")

    def write_lock(self, value : int) -> None:
        """Program the lock byte; the answer has a second status byte, as for the fuses"""
        self.protocol.isp(bytes([self.PROGRAM_LOCK, 0xAC, 0xE0, 0x00, value]), 3)

    def chip_erase(self) -> None:
        """Chip erase: 45 ms, polling by RDY/BSY, 'Chip Erase'"""
        self.protocol.isp(bytes([self.CHIP_ERASE, 45, 1, 0xAC, 0x80, 0, 0]), 2)

    def write_flash_page(self, address : int, data : bytes) -> None:
        """
        Load the word address, then program one page: page mode with the page write, 'Load Program
        Memory Page' and 'Write Program Memory Page' (needed only by the dirty-PC test of the
        ATmega48/88; not measured on hardware yet)
        """
        self.protocol.isp(bytes([self.LOAD_ADDRESS]) + (address >> 1).to_bytes(4, 'big'), 2)
        self.protocol.isp(bytes([self.PROGRAM_FLASH]) + len(data).to_bytes(2, 'big') +
                          bytes([0x81, 0, 0x40, 0x4C, 0, 0, 0]) + bytes(data), 2)


def usb_serial(device : usb.core.Device) -> str:
    """Serial number from the USB descriptor; both probes end it with a NUL"""
    try:
        return str(usb.util.get_string(device, device.iSerialNumber) or "").rstrip("\0")
    except (usb.core.USBError, ValueError, NotImplementedError):
        return ""


def discover(tool : str | None = None) -> list[ProbeCandidate]:
    """All attached probes speaking this protocol, optionally only those of one kind"""
    found : list[ProbeCandidate] = []
    for device in usb.core.find(find_all=True, idVendor=VENDOR_ATMEL):
        name = PRODUCTS.get(device.idProduct)
        if name is None or (tool is not None and name != tool):
            continue
        try:
            product = str(usb.util.get_string(device, device.iProduct) or name)
        except (usb.core.USBError, ValueError, NotImplementedError):
            product = name
        found.append(ProbeCandidate(tool=name, product=product, address=usb_serial(device)))
    return found



class Jtag2UsbTransport():
    """
    One probe on USB: the frames go through two bulk endpoints, and a short packet
    marks the end of a frame in both directions (AVR067 section 2.1.3).
    """
    def __init__(self, device : usb.core.Device) -> None:
        self.logger : logging.Logger = logging.getLogger(__name__)
        self.device : usb.core.Device = device
        device.set_configuration()
        interface = device.get_active_configuration()[(0, 0)]
        usb.util.claim_interface(device, interface.bInterfaceNumber)
        self.interface : int = interface.bInterfaceNumber
        self.ep_out = usb.util.find_descriptor(interface, custom_match=lambda e:
                          usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
        self.ep_in = usb.util.find_descriptor(interface, custom_match=lambda e:
                          usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)
        if self.ep_out is None or self.ep_in is None:
            raise Jtag2Error("Probe has no pair of bulk endpoints")
        self.packet_size : int = self.ep_in.wMaxPacketSize
        self.flush()

    def flush(self) -> None:
        """
        Discard what the probe still has to say: a session that ended in a timeout leaves its late
        answer behind, and the next session would take it for the answer to its first command
        """
        while True:
            try:
                stale = self.ep_in.read(self.packet_size, timeout=50)
            except usb.core.USBTimeoutError:
                return
            self.logger.debug("Stale data discarded: %s", bytes(stale).hex())

    @staticmethod
    def open(tool : str | None = None, serial_suffix : str | None = None) -> 'Jtag2UsbTransport':
        """Open the one probe that matches"""
        devices = [d for d in usb.core.find(find_all=True, idVendor=VENDOR_ATMEL)
                   if d.idProduct in PRODUCTS and (tool is None or PRODUCTS[d.idProduct] == tool)
                   and (not serial_suffix or usb_serial(d).lower().endswith(serial_suffix.lower()))]
        if not devices:
            raise Jtag2Error("No matching JTAGICE mkII / AVR Dragon found")
        if len(devices) > 1:
            raise Jtag2Error("More than one matching probe; select one by its serial number")
        return Jtag2UsbTransport(devices[0])

    def write_frame(self, frame : bytes) -> None:
        """Send one frame; a frame that fills its last packet gets a zero-length one after it"""
        self.ep_out.write(frame, timeout=USB_TIMEOUT)
        if len(frame) % self.packet_size == 0:
            self.ep_out.write(b"", timeout=USB_TIMEOUT)

    def read_frame(self, timeout : int = USB_TIMEOUT) -> bytes:
        """Receive one frame: packets up to the first short one"""
        data = bytearray()
        while True:
            packet = self.ep_in.read(self.packet_size, timeout=timeout)
            data += bytes(packet)
            if len(packet) < self.packet_size:
                return bytes(data)

    def close(self) -> None:
        """Release the probe"""
        usb.util.release_interface(self.device, self.interface)
        usb.util.dispose_resources(self.device)


class Jtag2SerialTransport():
    """
    A probe on a serial port (dw-link): the frames of the USB transport as a byte stream (AVR067
    section 2.1.1). A frame is recognized by MESSAGE_START, a plausible size and TOKEN; bytes
    before it are skipped. Read timeouts are raised as TimeoutError.
    """
    def __init__(self, port : str) -> None:
        self.logger : logging.Logger = logging.getLogger(__name__)
        self.port : str = port
        self.buffer : bytearray = bytearray()
        self.serial : serial.Serial = serial.Serial()
        self.serial.port = port
        self.serial.baudrate = SERIAL_START_BAUD
        self.serial.timeout = 0.01
        # an Arduino resets when DTR is asserted at opening; where the OS lets us, it is not
        self.serial.dtr = False
        self.serial.rts = False
        self.serial.exclusive = True   # no serial monitor at the same time
        try:
            self.serial.open()
        except serial.SerialException as e:
            raise Jtag2Error("Cannot open {}: {}".format(port, e)) from e

    def flush(self) -> None:
        """Discard what has arrived so far"""
        self.serial.reset_input_buffer()
        self.buffer.clear()

    def write_frame(self, frame : bytes) -> None:
        """Send one frame"""
        try:
            self.serial.write(frame)
        except serial.SerialException as e:
            raise Jtag2Error("Serial error on {}: {}".format(self.port, e)) from e

    def read_frame(self, timeout : int = USB_TIMEOUT) -> bytes:
        """Receive one frame, waiting at most timeout ms"""
        deadline = time.monotonic() + timeout / 1000
        while True:
            start = self.buffer.find(MESSAGE_START)
            if start != 0:
                if self.buffer:
                    self.logger.debug("Skipped on %s: %s", self.port,
                                          bytes(self.buffer[:start if start > 0 else None]).hex())
                del self.buffer[:start if start > 0 else len(self.buffer)]
            if len(self.buffer) >= HEADER_SIZE:
                size = int.from_bytes(self.buffer[3:7], 'little')
                if self.buffer[7] != TOKEN or size > MAX_SERIAL_BODY:
                    del self.buffer[:1]       # not the start of a frame: look for the next one
                    continue
                if len(self.buffer) >= HEADER_SIZE + size + CRC_SIZE:
                    frame = bytes(self.buffer[:HEADER_SIZE + size + CRC_SIZE])
                    del self.buffer[:len(frame)]
                    return frame
            if time.monotonic() >= deadline:
                raise TimeoutError("No complete frame on {} within {} ms".format(self.port, timeout))
            try:
                self.buffer += self.serial.read(max(1, self.serial.in_waiting))
            except serial.SerialException as e:
                raise Jtag2Error("Serial error on {}: {}".format(self.port, e)) from e

    def set_baudrate(self, baud : int) -> None:
        """
        Switch the host side, after the probe has acknowledged PAR_BAUD_RATE at the old speed.
        Measured with dw-link on an Uno: after switching down, the first frame got lost without
        a pause (the USB-serial chip of the Uno delivers a garbage byte); 10 ms are enough.
        """
        self.serial.baudrate = baud
        time.sleep(0.01)

    def close(self) -> None:
        """Release the port"""
        try:
            self.serial.close()
        except serial.SerialException:
            pass


#pylint: disable=too-many-public-methods # one method per AVR067 command
class Jtag2Protocol():
    """
    Commands and responses with sequence numbers. Unlike pyedbglib, the sequence
    number of every response is checked; events, which carry 0xFFFF, are set aside.
    """
    def __init__(self, transport : Jtag2UsbTransport | Jtag2SerialTransport) -> None:
        self.logger : logging.Logger = logging.getLogger(__name__)
        self.transport : Jtag2UsbTransport | Jtag2SerialTransport = transport
        self.sequence : int = 0
        self.events : list[bytes] = []

    def command(self, body : bytes, timeout : int = USB_TIMEOUT) -> bytes:
        """Send a command and return the body of its response"""
        sequence = self.sequence
        self.sequence = (self.sequence + 1) % EVENT_SEQUENCE # wraps to zero after 0xFFFE
        with transaction(): # SIGTERM/SIGINT must not cut a command from its response
            try:
                self.transport.write_frame(make_frame(sequence, body))
                while True:
                    answer, response = parse_frame(self.transport.read_frame(timeout))
                    if answer == EVENT_SEQUENCE:
                        self.logger.debug("Event set aside: %s", response.hex())
                        self.events.append(response)
                        continue
                    if answer != sequence:
                        raise Jtag2Error("Response to message {} while waiting for {}".format(answer, sequence))
                    return response
            except usb.core.USBTimeoutError as e:
                # as a BackendError, the handler reports it to GDB instead of ending the packet with SIGABRT
                raise Jtag2UsbTimeout("No response to command 0x{:02X} from the probe: {}".format(body[0], e)) from e
            except TimeoutError as e:                   # the serial transport
                raise Jtag2Timeout("No response to command 0x{:02X} from the probe: {}".format(body[0], e)) from e
            except usb.core.USBError as e:
                raise Jtag2UsbError("USB error in command 0x{:02X}: {}".format(body[0], e)) from e

    def expect(self, response : bytes, wanted : int, what : str) -> bytes:
        """The response, if its MESSAGE_ID is the wanted one; otherwise an error naming the failure"""
        if not response or response[0] != wanted:
            name = RSP_FAILURES.get(response[0], "0x{:02X}".format(response[0])) if response else "empty"
            raise Jtag2Error("{}: {}".format(what, name))
        return response

    def get_parameter(self, parameter : int) -> bytes:
        """CMND_GET_PARAMETER: the value bytes of RSP_PARAMETER"""
        return self.expect(self.command(bytes([CMND_GET_PARAMETER, parameter])), RSP_PARAMETER,
                           "Get parameter 0x{:02X}".format(parameter))[1:]

    def set_parameter(self, parameter : int, value : bytes, timeout : int = USB_TIMEOUT) -> None:
        """CMND_SET_PARAMETER"""
        self.expect(self.command(bytes([CMND_SET_PARAMETER, parameter]) + bytes(value), timeout), RSP_OK,
                    "Set parameter 0x{:02X}".format(parameter))

    def set_device_descriptor(self, descriptor : bytes) -> None:
        """CMND_SET_DEVICE_DESCRIPTOR"""
        self.expect(self.command(bytes([CMND_SET_DEVICE_DESCRIPTOR]) + descriptor), RSP_OK,
                    "Set device descriptor")

    def set_device_context(self, sections : list[tuple[int, bytes]]) -> None:
        """CMND_SET_DEVICE_CONTEXT, one command per section: section, length (MSB first), data"""
        for section, data in sections:
            self.ok(bytes([CMND_SET_DEVICE_CONTEXT, section]) + len(data).to_bytes(2, 'big') + bytes(data),
                    "Set device context 0x{:02X}".format(section))

    def set_baud(self, baud : int) -> None:
        """
        PAR_BAUD_RATE on a serial line: the probe answers at the old speed and switches after it,
        then the host follows
        """
        if baud not in BAUD_CODES:
            raise Jtag2Error("{} bps is not a speed of the protocol".format(baud))
        if not isinstance(self.transport, Jtag2SerialTransport):
            raise Jtag2Error("The speed can only be set on a serial line")
        self.set_parameter(PAR_BAUD_RATE, bytes([BAUD_CODES[baud]]))
        self.transport.set_baudrate(baud)

    def ok(self, body : bytes, what : str) -> None:
        """A command answered by RSP_OK"""
        self.expect(self.command(body), RSP_OK, what)

    def read_memory(self, memtype : int, address : int, count : int) -> bytes:
        """CMND_READ_MEMORY"""
        return self.expect(self.command(struct.pack("<BBII", CMND_READ_MEMORY, memtype, count, address)),
                           RSP_MEMORY, "Read memory 0x{:02X}:0x{:X}".format(memtype, address))[1:]

    def write_memory(self, memtype : int, address : int, data : bytes) -> None:
        """CMND_WRITE_MEMORY"""
        self.ok(struct.pack("<BBII", CMND_WRITE_MEMORY, memtype, len(data), address) + bytes(data),
                "Write memory 0x{:02X}:0x{:X}".format(memtype, address))

    def read_pc(self) -> int:
        """CMND_READ_PC: a word address"""
        return int.from_bytes(self.expect(self.command(bytes([CMND_READ_PC])), RSP_PC, "Read PC")[1:5], 'little')

    def write_pc(self, pc : int) -> None:
        """CMND_WRITE_PC: a word address"""
        self.ok(struct.pack("<BI", CMND_WRITE_PC, pc), "Write PC")

    def go(self) -> None:
        """CMND_GO"""
        self.ok(bytes([CMND_GO]), "Go")

    def forced_stop(self) -> None:
        """CMND_FORCED_STOP; the probe confirms the stop with EVT_BREAK (see wait_for_break)"""
        self.ok(bytes([CMND_FORCED_STOP, LOW_LEVEL]), "Stop")

    def single_step(self) -> None:
        """CMND_SINGLE_STEP; EVT_BREAK follows"""
        self.ok(bytes([CMND_SINGLE_STEP, LOW_LEVEL, STEP_INTO]), "Single step")

    def reset(self) -> None:
        """CMND_RESET: the target stops at 0; EVT_BREAK follows"""
        self.ok(bytes([CMND_RESET, LOW_LEVEL]), "Reset")

    def debugwire_disable(self) -> None:
        """CMND_RESET with the debugWIRE disable flag: ISP works again until the next power cycle"""
        self.ok(bytes([CMND_RESET, RESET_DEBUGWIRE_DISABLE]), "debugWIRE disable")

    def restore_target(self) -> None:
        """
        CMND_RESTORE_TARGET: stop, replace the software breakpoints with the original instructions,
        reset, run. Measured: immediate (not deferred to the next go like CMND_CLR_BREAK), and the
        probe forgets all software breakpoints; EVT_BREAKs may follow
        """
        self.ok(bytes([CMND_RESTORE_TARGET]), "Restore target")

    def run_to(self, pc : int) -> None:
        """CMND_RUN_TO_ADDR: run until the word address pc"""
        self.ok(struct.pack("<BI", CMND_RUN_TO_ADDR, pc), "Run to address")

    def set_break(self, number : int, pc : int) -> None:
        """
        CMND_SET_BREAK for a program breakpoint at word address pc: number 1-3 are the hardware
        comparators (4 is reserved for stepping), SOFTWARE_BREAKPOINT a BREAK the probe plants
        """
        self.ok(struct.pack("<BBBIB", CMND_SET_BREAK, BREAK_PROGRAM, number, pc, BREAK_MODE_PROGRAM),
                "Set breakpoint {} at 0x{:X}".format(number, pc))

    def clr_break(self, number : int, pc : int = 0) -> None:
        """CMND_CLR_BREAK; a software breakpoint is identified by its word address"""
        self.ok(struct.pack("<BBI", CMND_CLR_BREAK, number, pc), "Clear breakpoint {}".format(number))

    def enter_progmode(self) -> None:
        """CMND_ENTER_PROGMODE"""
        self.ok(bytes([CMND_ENTER_PROGMODE]), "Enter programming mode")

    def leave_progmode(self) -> None:
        """CMND_LEAVE_PROGMODE; leaves two EVT_BREAKs behind (measured), drained by the caller"""
        self.ok(bytes([CMND_LEAVE_PROGMODE]), "Leave programming mode")

    def chip_erase(self) -> None:
        """CMD_CHIP_ERASE, in programming mode (JTAG only)"""
        self.ok(bytes([CMND_CHIP_ERASE]), "Chip erase")

    def erase_page_spm(self, address : int) -> None:
        """CMND_ERASEPAGE_SPM: erase the flash page at a byte address, in debug mode"""
        self.ok(struct.pack("<BI", CMND_ERASEPAGE_SPM, address), "Erase page 0x{:X}".format(address))

    def isp(self, packet : bytes, answer : int) -> bytes:
        """
        CMND_ISP_PACKET: an AVRISP mkII command (AVR069), in the SPI emulator mode. Between the
        MESSAGE_ID and the packet go two bytes, LSB first, with the length of the expected answer
        (taken from avrdude's frames; without them the probe never answers). The answer comes as
        RSP_SPI_DATA with the command, a status (0 = OK) and the data; returned without the first two.
        """
        response = self.expect(self.command(bytes([CMND_ISP_PACKET]) + answer.to_bytes(2, 'little') +
                                            bytes(packet)), RSP_SPI_DATA,
                               "ISP command 0x{:02X}".format(packet[0]))
        if len(response) < 3 or response[1] != packet[0] or response[2] != 0:
            raise Jtag2Error("ISP command 0x{:02X} failed: {}".format(packet[0], response.hex()))
        return response[3:]

    def drain_breaks(self) -> None:
        """Discard pending break events, e.g. the ones LEAVE_PROGMODE leaves behind"""
        while self.poll_break(20) is not None:
            pass

    def poll_break(self, timeout : int = 0) -> tuple[int, int] | None:
        """
        (PC, break cause) of the next EVT_BREAK, waiting at most timeout ms; None if there is none.
        Other events are logged and dropped. Measured on the mkII clone: a descriptor sent after a
        stop, but before its EVT_BREAK has arrived, is lost and never answered; small commands are not
        affected. So after stop, step and reset, wait for the event before going on.
        """
        deadline = time.monotonic() + timeout / 1000
        while True:
            while self.events:
                event = self.events.pop(0)
                if event[0] == EVT_BREAK and len(event) >= 6:
                    return int.from_bytes(event[1:5], 'little'), event[5]
                self.logger.debug("Event dropped: %s", event.hex())
            remaining = int((deadline - time.monotonic()) * 1000)
            try:
                sequence, body = parse_frame(self.transport.read_frame(max(remaining, 1)))
            except (usb.core.USBTimeoutError, TimeoutError):
                return None
            if sequence == EVENT_SEQUENCE:
                self.events.append(body)
            else:
                self.logger.warning("Unexpected response to message %d dropped: %s", sequence, body.hex())
            if remaining <= 0 and not self.events:
                return None

    def wait_for_break(self, timeout : int = USB_TIMEOUT) -> tuple[int, int]:
        """(PC, break cause) of the next EVT_BREAK; an error if it does not come in time"""
        result = self.poll_break(timeout)
        if result is None:
            raise Jtag2Error("No break event within {} ms".format(timeout))
        return result

    def sign_on(self, timeout : int = USB_TIMEOUT) -> SignOn:
        """CMND_GET_SIGN_ON: is the probe there, and which one is it"""
        return parse_sign_on(self.command(bytes([CMND_GET_SIGN_ON]), timeout))

    def sign_off(self) -> None:
        """CMND_SIGN_OFF: end of the session"""
        response = self.command(bytes([CMND_SIGN_OFF]))
        if response[:1] != bytes([RSP_OK]):
            raise Jtag2Error("Sign-off refused: {}".format(response.hex()))
