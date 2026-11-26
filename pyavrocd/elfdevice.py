"""
Which chip an ELF file was built for, and whether that is the chip being debugged.

The Arduino IDE debugs the binary of the last Verify or Upload, and it keeps that binary in a
folder that belongs to the sketch, not to the board. Someone who selects another board and starts
debugging without compiling again gets the binary for the previous chip.

avr-libc's start-up code records the chip in the note section .note.gnu.avr.deviceinfo; builds
without it (MicroCore, for instance) still carry the compiler's architecture in the ELF header,
which is compared instead -- coarser, but enough to tell an ATtiny13A binary from an ATmega328P.
"""
import logging
import re

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import NoteSection

# The compiler's architecture for each device PyAvrOCD supports, taken from the device-specs files of
# avr-gcc 7.3.0 (Arduino's and the Azduino builds that megaTinyCore and DxCore ship); they agree on
# every device. Missing (as of 2026-11): the LA and SD families, for which the check is skipped.
GCC_ARCH : dict[str, tuple[str, ...]] = {
    'avr25': (
        'attiny13', 'attiny13a', 'attiny2313', 'attiny2313a', 'attiny24', 'attiny24a', 'attiny25',
        'attiny261', 'attiny261a', 'attiny4313', 'attiny43u', 'attiny44', 'attiny441', 'attiny44a',
        'attiny45', 'attiny461', 'attiny461a', 'attiny48', 'attiny828', 'attiny84', 'attiny841', 'attiny84a',
        'attiny85', 'attiny861', 'attiny861a', 'attiny87', 'attiny88',
    ),
    'avr35': (
        'at90usb162', 'at90usb82', 'atmega16u2', 'atmega32u2', 'atmega8u2', 'attiny1634', 'attiny167',
    ),
    'avr4': (
        'at90pwm1', 'at90pwm2b', 'at90pwm3', 'at90pwm3b', 'at90pwm81', 'atmega48', 'atmega48a', 'atmega48p',
        'atmega48pa', 'atmega48pb', 'atmega88', 'atmega88a', 'atmega88p', 'atmega88pa', 'atmega88pb',
        'atmega8a', 'atmega8hva',
    ),
    'avr5': (
        'at90can32', 'at90can64', 'at90pwm161', 'at90pwm216', 'at90pwm316', 'at90usb646', 'at90usb647',
        'atmega16', 'atmega162', 'atmega164a', 'atmega164p', 'atmega164pa', 'atmega165a', 'atmega165p',
        'atmega165pa', 'atmega168', 'atmega168a', 'atmega168p', 'atmega168pa', 'atmega168pb', 'atmega169a',
        'atmega169p', 'atmega169pa', 'atmega16a', 'atmega16hva', 'atmega16hvb', 'atmega16hvbrevb',
        'atmega16m1', 'atmega16u4', 'atmega32', 'atmega324a', 'atmega324p', 'atmega324pa', 'atmega324pb',
        'atmega325', 'atmega3250', 'atmega3250a', 'atmega3250p', 'atmega3250pa', 'atmega325a', 'atmega325p',
        'atmega325pa', 'atmega328', 'atmega328p', 'atmega328pb', 'atmega329', 'atmega3290', 'atmega3290a',
        'atmega3290p', 'atmega3290pa', 'atmega329a', 'atmega329p', 'atmega329pa', 'atmega32a', 'atmega32c1',
        'atmega32hvb', 'atmega32hvbrevb', 'atmega32m1', 'atmega32u4', 'atmega406', 'atmega64', 'atmega640',
        'atmega644', 'atmega644a', 'atmega644p', 'atmega644pa', 'atmega644rfr2', 'atmega645', 'atmega6450',
        'atmega6450a', 'atmega6450p', 'atmega645a', 'atmega645p', 'atmega649', 'atmega6490', 'atmega6490a',
        'atmega6490p', 'atmega649a', 'atmega649p', 'atmega64a', 'atmega64c1', 'atmega64hve2', 'atmega64m1',
        'atmega64rfr2',
    ),
    'avr51': (
        'at90can128', 'at90usb1286', 'at90usb1287', 'atmega128', 'atmega1280', 'atmega1281', 'atmega1284',
        'atmega1284p', 'atmega1284rfr2', 'atmega128a', 'atmega128rfa1', 'atmega128rfr2',
    ),
    'avr6': (
        'atmega2560', 'atmega2561', 'atmega2564rfr2', 'atmega256rfr2',
    ),
    'avrxmega2': (
        'avr64da28', 'avr64da28s', 'avr64da32', 'avr64da32s', 'avr64da48', 'avr64da48s', 'avr64da64',
        'avr64da64s', 'avr64db28', 'avr64db32', 'avr64db48', 'avr64db64', 'avr64dd14', 'avr64dd20',
        'avr64dd28', 'avr64dd32', 'avr64du28', 'avr64du32', 'avr64ea28', 'avr64ea32', 'avr64ea48',
    ),
    'avrxmega3': (
        'atmega1608', 'atmega1609', 'atmega3208', 'atmega3209', 'atmega4808', 'atmega4809', 'atmega808',
        'atmega809', 'attiny1604', 'attiny1606', 'attiny1607', 'attiny1614', 'attiny1616', 'attiny1617',
        'attiny1624', 'attiny1626', 'attiny1627', 'attiny202', 'attiny204', 'attiny212', 'attiny214',
        'attiny3216', 'attiny3217', 'attiny3224', 'attiny3226', 'attiny3227', 'attiny402', 'attiny404',
        'attiny406', 'attiny412', 'attiny414', 'attiny416', 'attiny417', 'attiny424', 'attiny426',
        'attiny427', 'attiny804', 'attiny806', 'attiny807', 'attiny814', 'attiny816', 'attiny817',
        'attiny824', 'attiny826', 'attiny827', 'avr16dd14', 'avr16dd20', 'avr16dd28', 'avr16dd32',
        'avr16du14', 'avr16du20', 'avr16du28', 'avr16du32', 'avr16ea28', 'avr16ea32', 'avr16ea48',
        'avr16eb14', 'avr16eb20', 'avr16eb28', 'avr16eb32', 'avr32da28', 'avr32da28s', 'avr32da32',
        'avr32da32s', 'avr32da48', 'avr32da48s', 'avr32db28', 'avr32db32', 'avr32db48', 'avr32dd14',
        'avr32dd20', 'avr32dd28', 'avr32dd32', 'avr32du14', 'avr32du20', 'avr32du28', 'avr32du32',
        'avr32ea28', 'avr32ea32', 'avr32ea48', 'avr32eb14', 'avr32eb20', 'avr32eb28', 'avr32eb32',
    ),
    'avrxmega4': (
        'avr128da28', 'avr128da28s', 'avr128da32', 'avr128da32s', 'avr128da48', 'avr128da48s', 'avr128da64',
        'avr128da64s', 'avr128db28', 'avr128db32', 'avr128db48', 'avr128db64',
    ),
}
ARCH_OF_DEVICE : dict[str, str] = { dev : arch for arch, devs in GCC_ARCH.items() for dev in devs }

# The number the ELF header holds in the low seven bits of e_flags (bit 7: prepared for linker relaxation)
ARCH_NUMBER : dict[str, int] = { 'avr1' : 1, 'avr2' : 2, 'avr25' : 25, 'avr3' : 3, 'avr31' : 31, 'avr35' : 35,
                                 'avr4' : 4, 'avr5' : 5, 'avr51' : 51, 'avr6' : 6, 'avrtiny' : 100,
                                 'avrxmega2' : 102, 'avrxmega3' : 103, 'avrxmega4' : 104,
                                 'avrxmega5' : 105, 'avrxmega6' : 106, 'avrxmega7' : 107 }
ARCH_NAME : dict[int, str] = { num : name for name, num in ARCH_NUMBER.items() }

def note_device(ef : ELFFile) -> str | None:
    """
    The device name from .note.gnu.avr.deviceinfo, or None. The note's description is six 32-bit
    words (flash, SRAM and EEPROM start and size), a word with the value 8, the offset of the
    device name and the string table it points into (measured: 8, 1, then b'\\0atmega2560\\0').
    """
    section = ef.get_section_by_name('.note.gnu.avr.deviceinfo')
    if not isinstance(section, NoteSection):
        return None
    for note in section.iter_notes():
        if note['n_name'] != 'AVR':
            continue
        desc = note['n_desc']
        if isinstance(desc, str):          # pyelftools hands over unknown note types as text
            desc = desc.encode('latin-1')
        if len(desc) < 32:
            return None
        offset = int.from_bytes(desc[28:32], 'little')
        strings = desc[32:]
        name = strings[offset:].split(b'\0', 1)[0].decode('ascii', errors='replace')
        return name.lower() if re.fullmatch(r'[a-z0-9]+', name.lower()) else None
    return None

def elf_target(elf_file : str) -> tuple[str | None, str | None]:
    """(device from the note or None, architecture from the ELF header or None)"""
    with open(elf_file, 'rb') as f:
        ef = ELFFile(f)
        if ef['e_machine'] != 'EM_AVR':
            return None, None
        return note_device(ef), ARCH_NAME.get(ef['e_flags'] & 0x7F)

def check_elf_device(elf_file : str | None, device : str | None, logger : logging.Logger) -> bool:
    """
    Refuse (critical message, True) if the ELF file was built for another chip than the one to be
    debugged: such a program cannot run correctly there, so unlike an outdated ELF file this is
    never only a warning. --skip-signature-verification skips this check (in main.py) as well.
    Anything that cannot be read or is not known passes quietly.
    """
    if not elf_file or not device:
        return False
    try:
        built_for, arch = elf_target(elf_file)
    except Exception as e: # pylint: disable=broad-exception-caught
        logger.debug("Could not read the target of '%s': %s", elf_file, e)
        return False
    if built_for:
        if built_for == device:
            return False
        what = built_for
    else:
        expected = ARCH_OF_DEVICE.get(device)
        if arch is None or expected is None or arch == expected:
            return False
        what = "the architecture " + arch
        logger.debug("ELF architecture %s, %s needs %s", arch, device, expected)
    logger.critical("The program was built for %s, not for %s", what, device)
    logger.critical("Select the right board, or verify (compile) the sketch for this one, "
                        "then start debugging again")
    return True
