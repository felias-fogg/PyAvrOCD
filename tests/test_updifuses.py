"""
The UPDI fuses PyAvrOCD sets because the program dictates them: BOOTEND/BOOTSIZE (-m bootend) and the
16/20 MHz oscillator (-m oscfreq). The computation in pyavrocd.updifuses and the session step that
reads and writes the fuses.
"""
#pylint: disable=protected-access,missing-function-docstring
import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch, call

from pyavrocd import updifuses
from pyavrocd.session import AvrSession
from pyavrocd.errors import FatalError
from pyavrocd.deviceinfo.devices import attiny1614, avr64ea32, avr64dd32, avr32la32

SMOKE_ELF = os.path.join(os.path.dirname(__file__), '..', 'extras', 'ci', 'smoke-atmega328p.elf')

class TestDeviceData(unittest.TestCase):
    """The generated device files carry what the policy needs, per family"""

    def test_tinyavr(self):
        info = attiny1614.DEVICE_INFO
        self.assertEqual((info['bootend_base'], info['bootend_unit']), (0x8, 256))
        self.assertEqual((info['oscfreq_base'], info['oscfreq_mask'],
                          info['oscfreq_16mhz'], info['oscfreq_20mhz']), (0x2, 0x03, 0x01, 0x02))

    def test_ea_has_reversed_polarity(self):
        info = avr64ea32.DEVICE_INFO
        self.assertEqual((info['bootend_base'], info['bootend_unit']), (0x8, 256))
        self.assertEqual((info['oscfreq_mask'], info['oscfreq_16mhz'], info['oscfreq_20mhz']),
                         (0x08, 0x08, 0x00))

    def test_dd_has_no_oscillator_choice(self):
        info = avr64dd32.DEVICE_INFO
        self.assertEqual((info['bootend_base'], info['bootend_unit']), (0x8, 512))
        self.assertNotIn('oscfreq_base', info)

    def test_lx_has_no_bootend_unit(self):
        info = avr32la32.DEVICE_INFO
        self.assertNotIn('bootend_base', info)
        self.assertIn('oscfreq_base', info)


class TestOscillator(unittest.TestCase):
    """Which oscillator a clock frequency comes from"""

    def test_only_from_16(self):
        for f in (16_000_000, 8_000_000, 4_000_000, 1_000_000, 250_000):
            self.assertEqual(updifuses.oscillator_for(f), 16, f)

    def test_only_from_20(self):
        for f in (20_000_000, 10_000_000, 5_000_000, 2_500_000, 1_250_000):
            self.assertEqual(updifuses.oscillator_for(f), 20, f)

    def test_both_or_neither_leave_it_alone(self):
        # 2 MHz is 16/8 as well as 20/10; 24 and 32 MHz are tuned or overclocked, 12 MHz needs a
        # crystal or a tuned oscillator, 3333333 Hz is not exactly 20/6
        for f in (2_000_000, 24_000_000, 32_000_000, 12_000_000, 3_333_333, 7_372_800):
            self.assertIsNone(updifuses.oscillator_for(f), f)

    def test_value_keeps_the_other_bits(self):
        info = attiny1614.DEVICE_INFO
        self.assertEqual(updifuses.oscfreq_value(0x7E, 16_000_000, info), 0x7D) # FREQSEL 2 -> 1
        self.assertEqual(updifuses.oscfreq_value(0x81, 20_000_000, info), 0x82) # OSCLOCK kept
        self.assertEqual(updifuses.oscfreq_value(0x7D, 8_000_000, info), 0x7D)  # nothing to do

    def test_value_ea(self):
        info = avr64ea32.DEVICE_INFO
        self.assertEqual(updifuses.oscfreq_value(0x00, 16_000_000, info), 0x08)
        self.assertEqual(updifuses.oscfreq_value(0x0F, 10_000_000, info), 0x07)

    def test_value_none(self):
        self.assertIsNone(updifuses.oscfreq_value(0x7E, 2_000_000, attiny1614.DEVICE_INFO))
        self.assertIsNone(updifuses.oscfreq_value(0x00, 16_000_000, avr64dd32.DEVICE_INFO))


class TestBootend(unittest.TestCase):
    """BOOTEND/BOOTSIZE from where the vector table is"""

    def test_values(self):
        self.assertEqual(updifuses.bootend_value(0, attiny1614.DEVICE_INFO), 0)
        self.assertEqual(updifuses.bootend_value(0x200, attiny1614.DEVICE_INFO), 2)
        self.assertEqual(updifuses.bootend_value(0x200, avr64dd32.DEVICE_INFO), 1)

    def test_not_a_multiple_or_no_fuse(self):
        self.assertIsNone(updifuses.bootend_value(0x100, avr64dd32.DEVICE_INFO))
        self.assertIsNone(updifuses.bootend_value(0, avr32la32.DEVICE_INFO))

    def test_vector_table_of_a_real_elf(self):
        self.assertEqual(updifuses.vector_table_address(SMOKE_ELF), 0)

    def test_vector_table_unreadable(self):
        self.assertIsNone(updifuses.vector_table_address('no-such-file.elf'))


def session(device_info, manage, fuses, *, elffile='x.elf', f_cpu=16_000_000, fcpu_given=True,
            iface='updi', attach=False):
    """An AvrSession stand-in with fuses in a dict, enough for _manage_updi_fuses"""
    sess = MagicMock()
    sess._iface = iface
    sess.manage = manage
    sess.device_info = device_info
    sess.args = SimpleNamespace(elffile=elffile, F_CPU=f_cpu, fcpu_given=fcpu_given, attach=attach)
    sess.read_fuse.side_effect = lambda addr, size: bytearray([fuses[addr]])
    sess.write_fuse.side_effect = lambda addr, data: fuses.__setitem__(addr, data[0])
    sess._updi_fuse_targets = lambda: AvrSession._updi_fuse_targets(sess)
    return sess


@patch('pyavrocd.session.time.sleep', MagicMock())
class TestSession(unittest.TestCase):
    """
    Reading (in debugging mode), deciding, writing (in programming mode, whose end resets the MCU
    and activates the fuses). Programming mode only when something is written: leaving it resets
    the MCU, and on the mEDBG an access right after that timed out (measured, Uno WiFi Rev2).
    """

    @patch('pyavrocd.session.updifuses.vector_table_address', MagicMock(return_value=0))
    def test_issue_21(self):
        # MegaCoreX without bootloader links the vectors at 0, the chip had BOOTEND=2
        fuses = {0x2: 0x7E, 0x8: 0x02}
        sess = session(attiny1614.DEVICE_INFO, ['bootend', 'oscfreq'], fuses, f_cpu=20_000_000)
        AvrSession._manage_updi_fuses(sess)
        self.assertEqual(fuses, {0x2: 0x7E, 0x8: 0x00})
        sess.write_fuse.assert_called_once_with(0x8, bytearray([0x00]))
        names = [c[0] for c in sess.method_calls]
        self.assertLess(names.index('read_fuse'), names.index('switch_to_progmode'))
        self.assertLess(names.index('switch_to_progmode'), names.index('write_fuse'))
        self.assertEqual(sess.method_calls[-1], call.switch_to_debmode())

    @patch('pyavrocd.session.updifuses.vector_table_address', MagicMock(return_value=0x200))
    def test_both_fuses(self):
        fuses = {0x2: 0x7E, 0x8: 0x00}
        sess = session(attiny1614.DEVICE_INFO, ['bootend', 'oscfreq'], fuses, f_cpu=8_000_000)
        AvrSession._manage_updi_fuses(sess)
        self.assertEqual(fuses, {0x2: 0x7D, 0x8: 0x02})

    @patch('pyavrocd.session.updifuses.vector_table_address', MagicMock(return_value=0))
    def test_nothing_to_write(self):
        fuses = {0x2: 0x7D, 0x8: 0x00}
        sess = session(attiny1614.DEVICE_INFO, ['bootend', 'oscfreq'], fuses)
        AvrSession._manage_updi_fuses(sess)
        sess.write_fuse.assert_not_called()
        sess.switch_to_progmode.assert_not_called()   # no reset when nothing changes

    def test_not_managed_not_touched(self):
        fuses = {0x2: 0x7E, 0x8: 0x02}
        sess = session(attiny1614.DEVICE_INFO, ['lockbits', 'eesave'], fuses)
        AvrSession._manage_updi_fuses(sess)
        sess.switch_to_progmode.assert_not_called()
        sess.read_fuse.assert_not_called()

    def test_not_without_elf_and_f_cpu(self):
        # no -e: BOOTEND unknown; no -F: the default 1 MHz must not decide the oscillator
        fuses = {0x2: 0x7E, 0x8: 0x02}
        sess = session(attiny1614.DEVICE_INFO, ['bootend', 'oscfreq'], fuses,
                       elffile=None, f_cpu=1_000_000, fcpu_given=False)
        AvrSession._manage_updi_fuses(sess)
        sess.write_fuse.assert_not_called()

    def test_not_when_attaching_or_other_interface(self):
        for kwargs in ({'attach': True}, {'iface': 'jtag'}):
            sess = session(attiny1614.DEVICE_INFO, ['bootend', 'oscfreq'], {0x2: 0x7E, 0x8: 0x02},
                           **kwargs)
            AvrSession._manage_updi_fuses(sess)
            sess.switch_to_progmode.assert_not_called()

    @patch('pyavrocd.session.updifuses.vector_table_address', MagicMock(return_value=0x100))
    def test_bootsize_not_a_multiple(self):
        fuses = {0x8: 0x01}
        sess = session(avr64dd32.DEVICE_INFO, ['bootend', 'oscfreq'], fuses)
        AvrSession._manage_updi_fuses(sess)
        sess.write_fuse.assert_not_called()
        sess.logger.warning.assert_called_once()

    @patch('pyavrocd.session.updifuses.vector_table_address', MagicMock(return_value=0))
    def test_write_does_not_stick(self):
        fuses = {0x2: 0x7D, 0x8: 0x02}
        sess = session(attiny1614.DEVICE_INFO, ['bootend'], fuses)
        sess.write_fuse.side_effect = None # the chip ignores the write
        with self.assertRaises(FatalError):
            AvrSession._manage_updi_fuses(sess)
        sess.switch_to_debmode.assert_called_once()   # back to debugging mode all the same


if __name__ == '__main__':
    unittest.main()
