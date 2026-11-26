"""
The check whether the ELF file was built for the MCU being debugged
"""
#pylint: disable=missing-function-docstring
import logging
import unittest
from unittest.mock import MagicMock, patch

from elftools.elf.sections import NoteSection

from pyavrocd import elfdevice
from pyavrocd.elfdevice import check_elf_device, note_device, ARCH_OF_DEVICE

# The description of the note as avr-libc writes it for an ATmega2560 (dumped from a real ELF)
DESC_2560 = bytes.fromhex("00000000 00000400 00020000 00200000 00000000 00100000 08000000 01000000"
                          "0061746d 65676132 35363000".replace(" ", ""))


def elf_with_note(desc, name='AVR'):
    ef = MagicMock()
    section = MagicMock(spec=NoteSection)
    section.iter_notes.return_value = [{'n_name': name, 'n_desc': desc}]
    ef.get_section_by_name.return_value = section
    return ef


class TestNote(unittest.TestCase):
    """The device name in avr-libc's note section"""

    def test_device_name(self):
        self.assertEqual(note_device(elf_with_note(DESC_2560)), 'atmega2560')

    def test_description_as_text(self):
        # pyelftools may hand over the description of an unknown note type as a string
        self.assertEqual(note_device(elf_with_note(DESC_2560.decode('latin-1'))), 'atmega2560')

    def test_no_note(self):
        ef = MagicMock()
        ef.get_section_by_name.return_value = None
        self.assertIsNone(note_device(ef))

    def test_other_owner_or_short(self):
        self.assertIsNone(note_device(elf_with_note(DESC_2560, name='GNU')))
        self.assertIsNone(note_device(elf_with_note(DESC_2560[:20])))


class TestTable(unittest.TestCase):
    """The table of compiler architectures"""

    def test_measured_architectures(self):
        # what real ELFs of these devices carry in their headers
        for dev, arch in (('atmega2560', 'avr6'), ('atmega328p', 'avr5'), ('attiny85', 'avr25'),
                          ('attiny13a', 'avr25'), ('atmega4809', 'avrxmega3'), ('avr64dd32', 'avrxmega2'),
                          ('avr16du14', 'avrxmega3'), ('avr64ea48', 'avrxmega2')):
            self.assertEqual(ARCH_OF_DEVICE[dev], arch, dev)

    def test_each_device_once(self):
        listed = [dev for devs in elfdevice.GCC_ARCH.values() for dev in devs]
        self.assertEqual(len(listed), len(set(listed)))


class TestCheck(unittest.TestCase):
    """Refusing an ELF file built for another MCU"""

    def check(self, target, device='atmega328p'):
        logger = MagicMock(spec=logging.Logger)
        with patch('pyavrocd.elfdevice.elf_target', return_value=target):
            result = check_elf_device('x.elf', device, logger)
        return result, logger

    def test_same_device(self):
        result, logger = self.check(('atmega328p', 'avr5'))
        self.assertFalse(result)
        logger.critical.assert_not_called()

    def test_other_device_refused(self):
        result, logger = self.check(('attiny85', 'avr25'))
        self.assertTrue(result)
        self.assertIn('attiny85', logger.critical.call_args_list[0].args)

    def test_no_note_architecture_decides(self):
        self.assertFalse(self.check((None, 'avr25'), device='attiny13a')[0])
        result, logger = self.check((None, 'avr25'), device='atmega328p')
        self.assertTrue(result)
        self.assertIn('the architecture avr25', logger.critical.call_args_list[0].args)

    def test_unknown_passes(self):
        self.assertFalse(self.check((None, None))[0])                       # no note, odd flags
        self.assertFalse(self.check((None, 'avrxmega3'), device='avr16la28')[0])   # not in the table

    def test_nothing_to_check(self):
        logger = MagicMock(spec=logging.Logger)
        self.assertFalse(check_elf_device(None, 'atmega328p', logger))
        self.assertFalse(check_elf_device('x.elf', None, logger))

    def test_unreadable_file_passes(self):
        logger = MagicMock(spec=logging.Logger)
        with patch('pyavrocd.elfdevice.elf_target', side_effect=OSError("gone")):
            self.assertFalse(check_elf_device('x.elf', 'atmega328p', logger))


if __name__ == '__main__':
    unittest.main()
