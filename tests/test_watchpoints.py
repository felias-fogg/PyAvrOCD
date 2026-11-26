"""
Hardware watchpoints on JTAG megaAVRs: data breakpoints 2 and 3, one per byte, so either two 1-byte
watchpoints or one 2-byte watchpoint. The comparators are taken away from the code breakpoints.
"""
#pylint: disable=protected-access,missing-function-docstring
import unittest
from unittest.mock import MagicMock, call, patch

from pyavrocd.backend import DebugBackend
from pyavrocd.hardwarebp import HardwareBP, RESERVED
from pyavrocd.xavrdebugger import EdbgBackend


def jtag_dbg():
    """A JTAG backend stand-in: HWBP 0 (run-to) and 1..3, data comparators on 2 and 3"""
    dbg = MagicMock()
    dbg.get_hwbpnum.return_value = 4
    dbg.data_breakpoint_slots.return_value = [2, 3]
    return dbg


class TestHardwareBPWatch(unittest.TestCase):
    """The reservation of data comparators in the hardware breakpoint manager"""

    def test_two_one_byte_watchpoints(self):
        dbg = jtag_dbg()
        hw = HardwareBP(dbg)
        self.assertEqual(hw.set_watch(2, 0x65, 1), (True, []))
        self.assertEqual(hw.set_watch(3, 0x60, 1), (True, []))
        dbg.data_breakpoint_set.assert_has_calls([call(2, 0x65, DebugBackend.DATA_WRITE),
                                                  call(3, 0x60, DebugBackend.DATA_READ)])
        self.assertEqual(hw.usable(), 2)
        self.assertEqual(hw.set_watch(4, 0x62, 1), (False, []))   # no comparator left

    def test_one_two_byte_watchpoint_at_odd_address(self):
        dbg = jtag_dbg()
        hw = HardwareBP(dbg)
        self.assertEqual(hw.set_watch(4, 0x63, 2), (True, []))
        dbg.data_breakpoint_set.assert_has_calls([call(2, 0x63, DebugBackend.DATA_ACCESS),
                                                  call(3, 0x64, DebugBackend.DATA_ACCESS)])
        self.assertEqual(hw.set_watch(2, 0x65, 1), (False, []))

    def test_longer_than_two_bytes_refused(self):
        hw = HardwareBP(jtag_dbg())
        self.assertEqual(hw.set_watch(2, 0x60, 4), (False, []))

    def test_no_comparators(self):
        dbg = jtag_dbg()
        dbg.data_breakpoint_slots.return_value = []
        hw = HardwareBP(dbg)
        self.assertEqual(hw.set_watch(2, 0x60, 1), (False, []))

    def test_code_breakpoint_is_displaced(self):
        dbg = jtag_dbg()
        hw = HardwareBP(dbg)
        for addr in (0x100, 0x200, 0x300):     # HWBP 0, 1, 2
            hw.set(addr)
        self.assertEqual(hw.set_watch(2, 0x65, 1), (True, [0x300]))
        self.assertEqual(hw._hwbplist, [0x100, 0x200, RESERVED, None])

    def test_code_breakpoints_avoid_reserved(self):
        hw = HardwareBP(jtag_dbg())
        hw.set_watch(2, 0x65, 1)
        self.assertEqual([hw.set(a) for a in (0x100, 0x200, 0x300, 0x400)], [0, 1, 3, None])

    def test_clear_and_hit(self):
        dbg = jtag_dbg()
        hw = HardwareBP(dbg)
        hw.set_watch(2, 0x65, 1)
        hw.set_watch(3, 0x60, 1)
        self.assertEqual(hw.watch_hit([3]), ('rwatch', 0x60))
        self.assertEqual(hw.watch_hit([2]), ('watch', 0x65))
        self.assertIsNone(hw.watch_hit([]))
        self.assertTrue(hw.clear_watch(2, 0x65, 1))
        self.assertFalse(hw.clear_watch(2, 0x65, 1))
        self.assertEqual(hw.usable(), 3)
        dbg.hardware_breakpoint_clear.assert_called_with(2)

    def test_range_stepping_scaffold_respects_reservation(self):
        hw = HardwareBP(jtag_dbg())
        hw.set_watch(2, 0x63, 2)              # 2 and 3 reserved, 0 and 1 left
        hw.set(0x100)
        hw.set(0x200)
        reassign = hw.set_temp([0x300, 0x400])
        self.assertEqual(sorted(reassign), [0x100, 0x200])
        self.assertEqual(hw._hwbplist[2:], [RESERVED, RESERVED])


class TestWatchForAccess(unittest.TestCase):
    """Accesses the server simulates (LDS/STS at a software breakpoint) are matched in software"""

    def test_kinds(self):
        hw = HardwareBP(jtag_dbg())
        hw.set_watch(2, 0x65, 1)          # watch
        hw.set_watch(4, 0x63, 1)          # awatch
        self.assertEqual(hw.watch_for_access(0x65, True), ('watch', 0x65))
        self.assertIsNone(hw.watch_for_access(0x65, False))      # a read does not trigger 'watch'
        self.assertEqual(hw.watch_for_access(0x63, False), ('awatch', 0x63))
        self.assertIsNone(hw.watch_for_access(0x64, True))

    def test_read_and_two_bytes(self):
        hw = HardwareBP(jtag_dbg())
        hw.set_watch(3, 0x63, 2)          # rwatch on 2 bytes
        self.assertEqual(hw.watch_for_access(0x64, False), ('rwatch', 0x63))
        self.assertIsNone(hw.watch_for_access(0x64, True))


class TestStepHandsOverDataBreakpoints(unittest.TestCase):
    """
    The probe hands data breakpoints to the OCD at RUN/RUN_TO only, so while they have changed
    since the last run, a step over a straight-line instruction is a run to the next one
    """

    def backend(self, opcode, dirty=True):
        b = MagicMock()
        b._data_dirty = dirty
        b._step_off_written_pc_bp.return_value = False
        b.bad_pc_bit_mask = 0
        b.program_counter_read.return_value = 0xe6 >> 1
        b.flash_read.return_value = bytearray(opcode.to_bytes(2, 'little'))
        b.poll_event.return_value = 0xea
        b._step_by_running_to_next = lambda: EdbgBackend._step_by_running_to_next(b)
        return b

    def test_sts_is_run_over(self):
        b = self.backend(0x9380)          # sts k, r24 (two words)
        with patch('pyavrocd.xavrdebugger.AvrDebugger.run_to') as run_to, \
             patch('pyavrocd.xavrdebugger.AvrDebugger.step') as step:
            EdbgBackend._single_step(b)
        run_to.assert_called_once_with(b, 0xea)
        step.assert_not_called()
        self.assertFalse(b._data_dirty)

    def test_one_word_instruction(self):
        b = self.backend(0x5f8f)          # subi r24, 0xff
        with patch('pyavrocd.xavrdebugger.AvrDebugger.run_to') as run_to:
            EdbgBackend._single_step(b)
        run_to.assert_called_once_with(b, 0xe8)

    def test_plain_step_reads_event_with_data_breakpoints(self):
        # handed over already (not dirty): a usual step, whose event says whether #2/#3 fired
        for armed, polls in ((set(), 0), ({2}, 1)):
            b = self.backend(0x9380, dirty=False)
            b._data_bps = armed
            with patch('pyavrocd.xavrdebugger.AvrDebugger.step') as step:
                EdbgBackend._single_step(b)
            step.assert_called_once()
            self.assertEqual(b.poll_event.call_count, polls)

    def test_branches_and_clean_state_step(self):
        for opcode, dirty in ((0xcfff, True), (0x9508, True), (0x9380, False)):   # rjmp, ret, clean
            b = self.backend(opcode, dirty)
            with patch('pyavrocd.xavrdebugger.AvrDebugger.run_to') as run_to, \
                 patch('pyavrocd.xavrdebugger.AvrDebugger.step') as step:
                EdbgBackend._single_step(b)
            run_to.assert_not_called()
            step.assert_called_once()


class TestEdbgBreakEvent(unittest.TestCase):
    """The extended info of the EDBG break event names the hardware breakpoints that fired"""

    def poll(self, ext_hi, ext_lo):
        backend = MagicMock()
        backend.device.avr.protocol.poll_events.return_value = \
            bytearray([0x12, 0x40, 0x00, 0x01, 0x00, 0x00, 0x02, ext_hi, ext_lo])
        backend.device.avr.protocol.decode_break_event.return_value = 0x100
        self.assertEqual(EdbgBackend.poll_event(backend), 0x100)
        return EdbgBackend.data_breakpoints_hit(backend)

    def test_bits(self):
        self.assertEqual(self.poll(0x08, 0x00), [2])     # measured: #2 -> 0x0800
        self.assertEqual(self.poll(0x04, 0x00), [3])     # #3 -> 0x0400
        self.assertEqual(self.poll(0x18, 0x00), [2])     # code #1 together with data #2
        self.assertEqual(self.poll(0x10, 0x00), [])      # code #1 alone

    def test_resume_forgets_the_last_stop(self):
        backend = MagicMock()
        backend._break_ext_info = 0x0800
        with patch('pyavrocd.xavrdebugger.AvrDebugger.run'):
            EdbgBackend._go(backend)
        self.assertEqual(EdbgBackend.data_breakpoints_hit(backend), [])

    def test_no_event(self):
        backend = MagicMock()
        backend.device.avr.protocol.poll_events.return_value = None
        self.assertIsNone(EdbgBackend.poll_event(backend))


if __name__ == '__main__':
    unittest.main()
