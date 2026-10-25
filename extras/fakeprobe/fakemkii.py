#!/usr/bin/env python3
"""
A fake JTAGICE mkII on a pseudo terminal, for finding out what a host sends to a serial mkII
(AVR067) and for testing the host side without hardware. It prints the pty's name, then logs
every frame it receives and every answer it sends.

It answers sign-on, sign-off, GET_SYNC, SET/GET_PARAMETER (with PAR_BAUD_RATE, which only
records the requested rate: a pty has no speed) and CMND_ISP_PACKET, whose AVRISP mkII commands
(AVR069) go to a small emulated ISP target: signature, fuses and lock byte of an ATmega328P.
In the debugWIRE emulator mode it emulates the debug side of the same chip: device descriptor,
memories (registers, I/O and SRAM in one data space, flash, EEPROM, signature), PC, go, stop,
single step, reset and breakpoints, with EVT_BREAK after stop, step and reset. The target does
not execute anything: a step only advances the PC by one word.
Everything else gets RSP_FAILED, or for an ISP command STATUS_CMD_FAILED, and is marked UNHANDLED
in the log, so that one sees what is still missing.

The answers follow the real probe where it has been measured (with the Waveshare clone, firmware
7.27, see pyavrocd/jtag2.py), otherwise AVR067 -- never avrdude's expectations, which are what
the fake is there to observe. Unmeasured choices are marked ASSUMPTION.

    fakemkii.py [--quiet]

Standard library only and independent of pyavrocd.jtag2, so that a bug in the host's framing
is not repeated here. The CRC is the one of AVR067 section 12.
"""
import argparse
import os
import select
import struct
import sys

MESSAGE_START : int = 0x1B
TOKEN : int = 0x0E
EVENT_SEQUENCE : int = 0xFFFF

RSP_OK, RSP_PARAMETER, RSP_MEMORY, RSP_PC, RSP_SIGN_ON, RSP_SPI_DATA = 0x80, 0x81, 0x82, 0x84, 0x86, 0x88
EVT_BREAK : int = 0xE0
MEMTYPE_SRAM, MEMTYPE_EEPROM, MEMTYPE_SPM = 0x20, 0x22, 0xA0
MEMTYPE_FLASH_PAGE, MEMTYPE_EEPROM_PAGE, MEMTYPE_SIGNATURE = 0xB0, 0xB1, 0xB4
BREAK_CAUSE_STOP : int = 0x00     # cause byte of EVT_BREAK after FORCED_STOP, step, reset and
                                  # RUN_TO_ADDR (measured on dW, 2026-10-25); a SW BP hit gives 0x01
RSP_FAILED, RSP_ILLEGAL_PARAMETER, RSP_ILLEGAL_COMMAND = 0xA0, 0xA1, 0xAA
STATUS_CMD_OK, STATUS_CMD_FAILED = 0x00, 0xC0

# the answer to GET_SIGN_ON of the Waveshare clone (captured 2026-10-23), firmware 7.27
SIGN_ON = bytes.fromhex("8601ff270700ff2707010900000042624a5441474943456d6b494900")
BAUD_CODES : dict[int, int] = {1: 2400, 2: 4800, 3: 9600, 4: 19200, 5: 38400, 6: 57600, 7: 115200, 8: 14400}

def _crc_table() -> list[int]:
    table = []
    for byte in range(256):
        crc = byte
        for _ in range(8):
            crc = (crc >> 1) ^ 0x8408 if crc & 1 else crc >> 1
        table.append(crc)
    return table

CRC_TABLE : list[int] = _crc_table()

def crc16(data : bytes) -> int:
    """AVR067 section 12: reflected CCITT polynomial, initial value 0xFFFF, no final xor"""
    crc = 0xFFFF
    for byte in data:
        crc = (crc >> 8) ^ CRC_TABLE[(crc ^ byte) & 0xFF]
    return crc

def frame(sequence : int, body : bytes) -> bytes:
    """A complete message: header, body, CRC"""
    head = struct.pack("<BHIB", MESSAGE_START, sequence, len(body), TOKEN) + body
    return head + struct.pack("<H", crc16(head))

class IspTarget():
    """The SPI instructions of a classic AVR, as far as the fake needs them: an ATmega328P"""
    def __init__(self) -> None:
        self.signature = bytes([0x1E, 0x95, 0x0F])
        self.fuses = {"low": 0xFF, "high": 0xDE, "ext": 0xFD}
        self.lock = 0xFF
        self.calibration = 0x9C
        self.programming = False

    def instruction(self, ins : bytes) -> int:
        """Execute one 4-byte SPI instruction; the byte the target shifts out last"""
        a, b, c, d = ins
        if a == 0x30:
            return self.signature[c & 3] if c < 3 else 0xFF
        if (a, b) == (0x50, 0x00):
            return self.fuses["low"]
        if (a, b) == (0x58, 0x08):
            return self.fuses["high"]
        if (a, b) == (0x50, 0x08):
            return self.fuses["ext"]
        if (a, b) == (0x58, 0x00):
            return self.lock
        if a == 0x38:
            return self.calibration
        if a == 0xAC:
            writes = {0xA0: "low", 0xA8: "high", 0xA4: "ext"}
            if b in writes:
                self.fuses[writes[b]] = d
            elif b == 0xE0:
                self.lock = d
            elif b == 0x80:
                self.lock = 0xFF                       # chip erase
            elif b == 0x53:
                return 0x00
            return d
        return 0x00

def isp_command(target : IspTarget, packet : bytes) -> tuple[bytes, bool]:
    """An AVRISP mkII (AVR069) command: its answer packet, and whether the fake knows it"""
    cmd = packet[0]
    if cmd == 0x10:                                    # CMD_ENTER_PROGMODE_ISP
        target.programming = True
        return bytes([cmd, STATUS_CMD_OK]), True
    if cmd == 0x11:                                    # CMD_LEAVE_PROGMODE_ISP
        target.programming = False
        return bytes([cmd, STATUS_CMD_OK]), True
    if cmd == 0x12:                                    # CMD_CHIP_ERASE_ISP
        target.lock = 0xFF
        return bytes([cmd, STATUS_CMD_OK]), True
    if cmd in (0x18, 0x1A, 0x1B, 0x1C):                # READ_FUSE, READ_LOCK, READ_SIGNATURE, READ_OSCCAL
        return bytes([cmd, STATUS_CMD_OK, target.instruction(packet[2:6]), STATUS_CMD_OK]), True
    if cmd in (0x17, 0x19):                            # PROGRAM_FUSE, PROGRAM_LOCK
        target.instruction(packet[1:5])
        return bytes([cmd, STATUS_CMD_OK, STATUS_CMD_OK]), True
    if cmd == 0x1D:                                    # CMD_SPI_MULTI: numTx, numRx, rxStart, data
        num_tx, num_rx, rx_start = packet[1], packet[2], packet[3]
        data = packet[4:4 + num_tx]
        out = bytes(3) + bytes([target.instruction(data[:4])]) if num_tx >= 4 else bytes(num_tx)
        rx = (out + bytes(256))[rx_start:rx_start + num_rx]
        return bytes([cmd, STATUS_CMD_OK]) + rx + bytes([STATUS_CMD_OK]), True
    return bytes([cmd, STATUS_CMD_FAILED]), False

class DwTarget():
    """The debug side of an ATmega328P: data space, flash, EEPROM, PC (a word address)"""
    def __init__(self) -> None:
        self.data = bytearray(0x900)                   # r0-r31, I/O 0x20-0xFF, SRAM 0x100-0x8FF
        self.flash = bytearray([0xFF] * 0x8000)
        self.eeprom = bytearray([0xFF] * 0x400)
        self.signature = bytes([0x1E, 0x95, 0x0F])
        self.pc = 0
        self.running = False
        self.descriptor = b""

    def memory(self, memtype : int) -> bytearray | bytes | None:
        """The memory a memory type addresses, None if the fake does not know it"""
        return {MEMTYPE_SRAM: self.data, MEMTYPE_SPM: self.flash, MEMTYPE_FLASH_PAGE: self.flash,
                MEMTYPE_EEPROM: self.eeprom, MEMTYPE_EEPROM_PAGE: self.eeprom,
                MEMTYPE_SIGNATURE: self.signature}.get(memtype)

class FakeMkII():
    """The probe: one frame in, one frame out"""
    def __init__(self, log : bool = True) -> None:
        self.log = log
        self.target = IspTarget()
        self.dw = DwTarget()
        self.emulator_mode = 2
        self.baud = 19200

    def say(self, text : str) -> None:
        """Log one line"""
        if self.log:
            print(text, flush=True)

    def stopped(self) -> bytes:
        """The EVT_BREAK the probe sends when the target has stopped"""
        self.dw.running = False
        return struct.pack("<BIB", EVT_BREAK, self.dw.pc, BREAK_CAUSE_STOP)

    def debug_command(self, body : bytes) -> tuple[bytes, list[bytes]] | None:
        """A debugWIRE command: its answer and the events that follow; None if not one of them"""
        cmd, dw = body[0], self.dw
        if cmd == 0x0C:                                    # SET_DEVICE_DESCRIPTOR
            dw.descriptor = body[1:]
            self.say("    device descriptor, {} bytes".format(len(dw.descriptor)))
            return bytes([RSP_OK]), []
        if cmd == 0x0A:                                    # FORCED_STOP
            return bytes([RSP_OK]), [self.stopped()]
        if cmd == 0x08:                                    # GO
            dw.running = True
            return bytes([RSP_OK]), []
        if cmd == 0x09:                                    # SINGLE_STEP: no execution, one word on
            dw.pc = (dw.pc + 1) % (len(dw.flash) // 2)
            return bytes([RSP_OK]), [self.stopped()]
        if cmd == 0x0B:                                    # RESET (flag 0x04: debugWIRE disable)
            if len(body) > 1 and body[1] & 0x04:
                self.say("    debugWIRE disabled")
                return bytes([RSP_OK]), []
            dw.pc = 0
            return bytes([RSP_OK]), [self.stopped()]
        if cmd == 0x07:                                    # READ_PC
            return struct.pack("<BI", RSP_PC, dw.pc), []
        if cmd == 0x06 and len(body) >= 5:                 # WRITE_PC
            dw.pc = struct.unpack("<I", body[1:5])[0]
            return bytes([RSP_OK]), []
        if cmd in (0x04, 0x05) and len(body) >= 10:       # WRITE_MEMORY, READ_MEMORY
            memtype, count, address = struct.unpack("<BII", body[1:10])
            memory = dw.memory(memtype)
            if memory is None or address + count > len(memory):
                self.say("    UNHANDLED memory type 0x{:02X} or range 0x{:X}+{}".format(memtype, address, count))
                return bytes([RSP_FAILED]), []
            if cmd == 0x05:
                return bytes([RSP_MEMORY]) + bytes(memory[address:address + count]), []
            if not isinstance(memory, bytearray):
                return bytes([RSP_FAILED]), []
            memory[address:address + count] = body[10:10 + count]
            return bytes([RSP_OK]), []
        if cmd == 0x11 and len(body) >= 3 and body[2] != 0:  # SET_BREAK on a comparator: dW has none
            return bytes([RSP_ILLEGAL_COMMAND]), []          # free (measured)
        if cmd in (0x11, 0x1A, 0x14, 0x15):                # SET/CLR_BREAK, ENTER/LEAVE_PROGMODE
            return bytes([RSP_OK]), []
        if cmd == 0x1C and len(body) >= 5:                 # RUN_TO_ADDR
            dw.running = True
            return bytes([RSP_OK]), []
        return None

    def answer(self, body : bytes) -> tuple[bytes, list[bytes]]:
        """The answer body to a command body, and the event bodies to send after it"""
        cmd = body[0]
        if self.emulator_mode == 0:
            debug = self.debug_command(body)
            if debug is not None:
                return debug
        if cmd == 0x01:
            return SIGN_ON, []
        if cmd in (0x00, 0x0F):                          # SIGN_OFF, GET_SYNC
            return bytes([RSP_OK]), []
        if cmd == 0x02 and len(body) >= 3:                 # SET_PARAMETER
            if body[1] == 0x03:
                self.emulator_mode = body[2]
            elif body[1] == 0x05:
                self.baud = BAUD_CODES.get(body[2], 0)
                self.say("    baud rate code 0x{:02X} = {} bps".format(body[2], self.baud or "unknown"))
            return bytes([RSP_OK]), []
        if cmd == 0x03 and len(body) >= 2:                 # GET_PARAMETER
            values = {0x01: bytes([0x00, 0x01]),          # HW version master, slave (measured)
                      0x02: bytes.fromhex("27072707"),    # FW version master, slave (measured)
                      0x03: bytes([self.emulator_mode]), 0x06: struct.pack("<H", 5000),
                      0x1D: bytes([self.dw.signature[2], self.dw.signature[1]]),   # LSB first (measured)
                      0x05: bytes([next((k for k, v in BAUD_CODES.items() if v == self.baud), 4)])}
            if body[1] in values:
                return bytes([RSP_PARAMETER]) + values[body[1]], []
            self.say("    UNHANDLED parameter 0x{:02X}".format(body[1]))
            return bytes([RSP_ILLEGAL_PARAMETER]), []
        if cmd == 0x2F and len(body) >= 4:                 # CMND_ISP_PACKET: answer length, packet
            if self.emulator_mode != 3:
                self.say("    ISP packet outside the SPI emulator mode")
            packet, known = isp_command(self.target, body[3:])
            if not known:
                self.say("    UNHANDLED ISP command 0x{:02X}".format(body[3]))
            return bytes([RSP_SPI_DATA]) + packet, []
        self.say("    UNHANDLED command 0x{:02X}".format(cmd))
        return bytes([RSP_FAILED]), []

    def serve(self, fd : int) -> None:
        """Read frames from the pty master and answer them, until the process is stopped"""
        buffer = b""
        while True:
            select.select([fd], [], [])
            try:
                buffer += os.read(fd, 4096)
            except OSError:                            # the host has closed the slave side
                continue
            while True:
                start = buffer.find(bytes([MESSAGE_START]))
                if start < 0:
                    buffer = b""
                    break
                if start > 0:
                    self.say("<- garbage {}".format(buffer[:start].hex()))
                    buffer = buffer[start:]
                if len(buffer) < 8:
                    break
                sequence, size, token = struct.unpack("<HIB", buffer[1:8])
                if token != TOKEN or size > 4096:
                    self.say("<- bad header {}".format(buffer[:8].hex()))
                    buffer = buffer[1:]
                    continue
                if len(buffer) < 8 + size + 2:
                    break
                message, buffer = buffer[:8 + size + 2], buffer[8 + size + 2:]
                body = message[8:8 + size]
                if struct.unpack("<H", message[-2:])[0] != crc16(message[:-2]):
                    self.say("<- CRC error {}".format(message.hex()))
                    continue
                self.say("<- seq {:5d}  {}".format(sequence, body.hex()))
                reply, events = self.answer(body)
                self.say("-> seq {:5d}  {}".format(sequence, reply.hex()))
                os.write(fd, frame(sequence, reply))
                for event in events:
                    self.say("-> event    {}".format(event.hex()))
                    os.write(fd, frame(EVENT_SEQUENCE, event))

def main() -> int:
    """Open a pty, print its name, serve it"""
    parser = argparse.ArgumentParser(description="A fake JTAGICE mkII on a pseudo terminal")
    parser.add_argument("--quiet", action="store_true", help="do not log the frames")
    args = parser.parse_args()
    master, slave = os.openpty()      # the slave stays open here, so the pty survives a host's close
    print(os.ttyname(slave), flush=True)
    try:
        FakeMkII(log=not args.quiet).serve(master)
    except KeyboardInterrupt:
        pass
    finally:
        os.close(slave)
        os.close(master)
    return 0

if __name__ == "__main__":
    sys.exit(main())
