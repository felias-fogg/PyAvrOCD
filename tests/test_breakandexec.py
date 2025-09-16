"""
The test suit for the BreakAndExec class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
import logging
from unittest.mock import Mock, call, create_autospec
from unittest import TestCase
from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.monitor import MonitorCommand
from pyavrocd.breakexec import BreakAndExec, SIGTRAP, SIGABRT, SIGILL, BREAKCODE, SLEEPCODE
from .util.instr import instrmap

logging.basicConfig(level=logging.CRITICAL)

class TestBreakAndExec(TestCase):

    def setUp(self):
        mock_mon = create_autospec(MonitorCommand, specSet=True, instance=True)
        mock_dbg = create_autospec(XAvrDebugger, spec_set=False, instance=True)
        mock_dbg.memory_info = Mock()
        mock_dbg.memory_info.memory_info_by_name.return_value = {'size' : 100 }
        self.bp = BreakAndExec(1, mock_mon, mock_dbg, Mock())
        self.bp.mon.is_old_exec.return_value = False
        self.bp.mon.is_safe.return_value = True

    def test_insert_breakpoint_old_exec(self):
        self.bp.mon.is_old_exec.return_value = True
        self.bp.insert_breakpoint(2)
        self.bp.dbg.software_breakpoint_set.assert_called_with(2)
        self.assertFalse(bool(self.bp._bp))

    def test_insert_breakpoint_odd(self):
        self.bp.mon.is_onlyhwbps.return_value = False
        self.bp.insert_breakpoint(3)
        self.assertFalse(bool(self.bp._bp))
        self.bp.insert_breakpoint(2)
        self.assertTrue(bool(self.bp._bp[2]))

    def test_insert_breakpoints_regular(self):
        self.bp.mon.is_onlyhwbps.return_value = False
        self.bp._read_flash_word.side_effect = [ BREAKCODE, 0x1111, 0x2222, 0x3333 ]
        self.bp.insert_breakpoint(100)
        self.bp.insert_breakpoint(200)
        self.assertEqual(self.bp._bp, {100: { 'active': True, 'inflash': False, 'hwbp' : None,
                                    'opcode': BREAKCODE, 'secondword' : 0x1111, 'timestamp' : 1 },
                                       200:  { 'active': True, 'inflash': False, 'hwbp' : None,
                                    'opcode': 0x2222, 'secondword' : 0x3333, 'timestamp' : 2 }})

    def test_remove_breakpoint_old_exec(self):
        self.bp.mon.is_old_exec.return_value = True
        self.bp.remove_breakpoint(2)
        self.bp.dbg.software_breakpoint_clear.assert_called_with(2)

    def test_remove_breakpoints_regular_idempotent(self):
        self.bp.mon.is_onlyhwbps.return_value = False
        self.bp._bp = {100: { 'active': True, 'inflash': False, 'hwbp' : None,
                                 'opcode': BREAKCODE, 'secondword' : 0x1111, 'timestamp' : 1 },
                       200:  { 'active': True, 'inflash': False, 'hwbp' : None,
                                  'opcode': 0x2222, 'secondword' : 0x3333, 'timestamp' : 2 }}
        self.bp._bpactive = 2
        self.bp.remove_breakpoint(100)
        self.assertEqual(self.bp._bpactive, 1)
        self.bp.remove_breakpoint(100)
        self.assertEqual(self.bp._bpactive, 1)
        self.bp.remove_breakpoint(200)
        self.assertEqual(self.bp._bpactive, 0)
        self.bp.remove_breakpoint(200)
        self.assertEqual(self.bp._bpactive, 0)
        self.bp.remove_breakpoint(200)
        self.assertEqual(self.bp._bpactive, 0)
        self.assertEqual(self.bp._bp, {100: { 'active': False, 'inflash': False, 'hwbp' : None,
                                    'opcode': BREAKCODE, 'secondword' : 0x1111, 'timestamp' : 1 },
                                       200:  { 'active': False, 'inflash': False, 'hwbp' : None,
                                    'opcode': 0x2222, 'secondword' : 0x3333, 'timestamp' : 2 }})

    def test_update_breakpoints_update_remove_sethwbp(self):
        self.maxDiff = None
        self.bp._hw[1] = 0x300
        self.bp.mon.is_onlyhwbps.return_value = False
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp._bstamp = 6
        self.bp._bp = {100: { 'active': True, 'inflash': False, 'hwbp' : None, # will get swbp
                                 'opcode': BREAKCODE, 'secondword' : 0x1111, 'timestamp' : 2 },
                       200:  { 'active': False, 'inflash': True, 'hwbp' : None, # will remove swbp
                                  'opcode': 0x2221, 'secondword' : 0x3331, 'timestamp' : 5 },
                       300:  { 'active': False, 'inflash': False, 'hwbp' : 1, # will remove hwbp
                                  'opcode': 0x2222, 'secondword' : 0x3332, 'timestamp' : 1 },
                       400:  { 'active': True, 'inflash': False, 'hwbp' : None, # gets an hwbp
                                  'opcode': 0x2223, 'secondword' : 0x3333, 'timestamp' : 3 }}
        self.bp.update_breakpoints(0, -1)
        self.assertEqual(self.bp._bp, {100: { 'active': True, 'inflash': True, 'hwbp' : None,
                                    'opcode': BREAKCODE, 'secondword' : 0x1111, 'timestamp' : 2 },
                                       400:  { 'active': True, 'inflash': False, 'hwbp' : 1,
                                    'opcode': 0x2223, 'secondword' : 0x3333, 'timestamp' : 3 }})
        self.assertEqual(self.bp._hw, [-1, 400 ])
        self.bp.dbg.software_breakpoint_clear.assert_called_with(200)
        self.bp.dbg.software_breakpoint_set.assert_called_with(100)

    def test_update_breakpoints_with_protected_bp_and_reserved_hwbp(self):
        self.maxDiff = None
        self.bp._hw[1] = 0x300
        self.bp.mon.is_onlyhwbps.return_value = False
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp._bstamp = 6
        self.bp._bp = {100: { 'active': True, 'inflash': False, 'hwbp' : None, # will get swbp
                                 'opcode': BREAKCODE, 'secondword' : 0x1111, 'timestamp' : 2 },
                       200:  { 'active': False, 'inflash': True, 'hwbp' : None, # will remove swbp
                                  'opcode': 0x2221, 'secondword' : 0x3331, 'timestamp' : 5 },
                       300:  { 'active': False, 'inflash': False, 'hwbp' : 1, # will remove hwbp
                                  'opcode': 0x2222, 'secondword' : 0x3332, 'timestamp' : 1 },
                       400:  { 'active': True, 'inflash': False, 'hwbp' : None, # gets an hwbp
                                  'opcode': 0x2223, 'secondword' : 0x3333, 'timestamp' : 3 }}
        self.bp.update_breakpoints(1, 300)
        self.assertEqual(self.bp._bp, {100: { 'active': True, 'inflash': True, 'hwbp' : None,
                                        'opcode': BREAKCODE, 'secondword' : 0x1111, 'timestamp' : 2 },
                                        400:  { 'active': True, 'inflash': True, 'hwbp' : None,
                                        'opcode': 0x2223, 'secondword' : 0x3333, 'timestamp' : 3 }})
        self.assertEqual(self.bp._hw, [-1, None ])
        self.bp.dbg.software_breakpoint_clear.assert_called_with(200)
        self.bp.dbg.software_breakpoint_set.assert_has_calls([call(100), call(400)], any_order=True)

    def test_update_breakpoints_update_remove_stealhwbp(self):
        self.maxDiff = None
        self.bp._hw = [-1, 0x100 ]
        self.bp.mon.is_onlyhwbps.return_value = False
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp._bstamp = 6
        self.bp._bpactive = 3
        self.bp._bp = {100: { 'active': True, 'inflash': False, 'hwbp' : 1, # will have to give up hwbp
                                 'opcode': BREAKCODE, 'secondword' : 0x1111, 'timestamp' : 1 },
                       200:  { 'active': False, 'inflash': True, 'hwbp' : None, # will remove swbp
                                  'opcode': 0x2221, 'secondword' : 0x3331, 'timestamp' : 2 },
                       300:  { 'active': False, 'inflash': True, 'hwbp' : None, # will remove swbp
                                  'opcode': 0x2222, 'secondword' : 0x3332, 'timestamp' : 3 },
                       400:  { 'active': True, 'inflash': False, 'hwbp' : None, # will become swbp
                                  'opcode': 0x2223, 'secondword' : 0x3333, 'timestamp' : 4 },
                       500:  { 'active': True, 'inflash': False, 'hwbp' : None, # gets hwbp
                                  'opcode': 0x2224, 'secondword' : 0x3334, 'timestamp' : 5 }}
        self.bp.update_breakpoints(0, -1)
        self.assertEqual(self.bp._bp, {100: { 'active': True, 'inflash': True, 'hwbp' : None,
                                    'opcode': BREAKCODE, 'secondword' : 0x1111, 'timestamp' : 1 },
                                       400:  { 'active': True, 'inflash': True, 'hwbp' : None,
                                    'opcode': 0x2223, 'secondword' : 0x3333, 'timestamp' : 4 },
                                       500:  { 'active': True, 'inflash': False, 'hwbp' : 1,
                                    'opcode': 0x2224, 'secondword' : 0x3334, 'timestamp' : 5 }})
        self.assertEqual(self.bp._hw, [-1, 500 ])
        self.bp.dbg.software_breakpoint_clear.assert_has_calls([call(200), call(300)], any_order=True)
        self.bp.dbg.software_breakpoint_set.assert_has_calls([call(100), call(400)], any_order=True)
        self.assertEqual(self.bp._bpactive, 3)

    def test_cleanup_breakpoints(self):
        self.bp._hw = [-1,1]
        self.bp._bp = { 1: 1}
        self.bp._bpactive = 1
        self.bp.cleanup_breakpoints()
        self.assertEqual(self.bp._hw, [-1, None])
        self.assertEqual(self.bp._bp, {})
        self.assertEqual(self.bp._bpactive, 0)
        self.bp.dbg.software_breakpoint_clear_all.assert_called_once()

    def test_resume_execution_old_exec(self):
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.mon.is_old_exec.return_value = True
        self.bp.resume_execution(2224)
        self.bp.dbg.program_counter_write(1112)
        self.bp.dbg.run.assert_called_once()

    def test_resume_execution_with_hwbp(self):
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.mon.is_onlyhwbps.return_value = False
        self.bp._hw[1] = 8888
        self.bp.resume_execution(2224)
        self.bp.dbg.program_counter_write.assert_called_with(1112)
        self.bp.dbg.run_to.assert_called_with(8888)

    def test_resume_execution_break(self):
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.mon.is_onlyhwbps.return_value = False
        self.bp._read_flash_word.side_effect = [ BREAKCODE ]
        self.assertEqual(self.bp.resume_execution(2224), SIGILL)
        self.bp.dbg.program_counter_write.assert_called_with(1112)

    def test_resume_execution_sleep(self):
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.mon.is_onlyhwbps.return_value = False
        self.bp._read_flash_word.side_effect = [ SLEEPCODE ]
        self.bp._hw[1] = 8888
        self.assertEqual(self.bp.resume_execution(2224), None)
        self.bp.dbg.program_counter_write.assert_has_calls([call(1112), call(1113)])
        self.bp.dbg.run_to.assert_called_with(8888)

    def test_resume_execution_without_hwbp(self):
        self.bp.mon.is_onlyswbps.return_value = True
        self.bp._hw[1] = None
        self.bp.resume_execution(None)
        self.bp.dbg.program_counter_read.assert_called_once()
        self.bp.dbg.run.assert_called_once()

    def test_resume_execution_at_break_one_word_with_hwbp(self):
        self.bp._bstamp = 3
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.mon.is_onlyhwbps.return_value = False
        self.bp._hw = [ -1, 100 ]
        self.bp._bp[100] = {'opcode' : 0x9000, 'secondword' : 0xFFFF, 'hwbp' : 1, 'active' : True, 'timestamp' : 2, 'inflash' : False }
        self.bp._bp[2224] = {'opcode' : 0xffb6, 'secondword' : 0xFFFF, 'hwbp' : None, 'active' : True,
                                 'timestamp' : 1, 'inflash' : None }
        self.bp.resume_execution(2224)
        self.bp.dbg.run_to.assert_called_with(100)

    def test_resume_execution_at_break_two_word_instr_with_hwbp(self):
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.mon.is_onlyhwbps.return_value = False
        self.bp._hw = [ -1, 100 ]
        self.bp._bp[100] = {'opcode' : 0x9000, 'secondword' : 0xFFFF, 'hwbp' : 1, 'active' : True, 'timestamp' : 2, 'inflash' : False }
        self.bp._bp[2224] = {'opcode' : 0x9000, 'secondword' : 0xFFFF, 'active' : True, 'hwbp' : None, 'timestamp' : 1, 'inflash' : True}
        self.bp.resume_execution(2224)
        self.bp.dbg.run_to.assert_called_with(100)

    def test_single_step_old_exec(self):
        self.bp.mon.is_old_exec.return_value = True
        self.bp.dbg.program_counter_read.return_value = 22
        self.assertTrue(self.bp.single_step(None), SIGTRAP)
        self.bp.dbg.program_counter_read.assert_called_once()
        self.bp.dbg.step.assert_called_once()
        self.bp.dbg.run_to.assert_not_called()

    def test_single_step_break(self):
        self.bp.mon.is_safe.return_value = False
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.dbg.program_counter_read.return_value = 22
        self.bp._read_flash_word.side_effect = [ BREAKCODE ]
        self.assertEqual(self.bp.single_step(None), SIGILL)
        self.bp._read_flash_word.assert_called_once()

    def test_single_step_sleep(self):
        self.bp.mon.is_safe.return_value = False
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.dbg.program_counter_read.return_value = 22
        self.bp._read_flash_word.side_effect = [ SLEEPCODE ]
        self.assertEqual(self.bp.single_step(None), SIGTRAP)
        self.bp._read_flash_word.assert_called_once()
        self.bp.dbg.program_counter_write.assert_has_calls([call(23)])

    def test_single_step_two_word_instr_at_BP_without_start(self):
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.mon.is_onlyhwbps.return_value = False
        self.bp.dbg.program_counter_read.return_value = 22
        self.bp._bp[44] = { 'inflash' : True, 'opcode' : 0x9000, 'secondword' :  0xFFFF, 'hwbp' : None, 'active': True, 'timestamp' : 1}
        self.bp._read_flash_word.assert_not_called()
        self.assertEqual(self.bp.single_step(None), SIGTRAP)
        self.bp.dbg.program_counter_write.assert_called_with(24)
        self.bp.dbg.step.assert_not_called()
        self.bp.dbg.run_to.assert_not_called()


    def test_single_step_unsafe_with_start(self):
        self.bp.mon.is_safe.return_value = False
        self.bp.mon.is_onlyswbps.return_value = False
        self.assertEqual(self.bp.single_step(42), SIGTRAP)
        self.bp.dbg.program_counter_write.assert_called_with(21)
        self.bp.dbg.program_counter_read.assert_not_called()
        self.bp._read_flash_word.assert_called_once()
        self.bp.dbg.step.assert_called_once()
        self.bp.dbg.run_to.assert_not_called()

    def test_single_step_safe_nobranch_oneWordInstr(self):
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.dbg.program_counter_read.return_value = 22
        self.bp._read_flash_word.side_effect = [ 0x8FF4, 0x8FF4, 0x8FFF ]
        self.assertFalse(self.bp.two_word_instr(0x8FF4))
        self.assertFalse(self.bp.branch_instr(0x8FF4))
        self.assertEqual(self.bp.single_step(None), None)
        self.bp._read_flash_word.assert_has_calls([call(44), call(44)], any_order=True )
        self.bp.dbg.step.assert_not_called()
        self.bp.dbg.run_to.assert_called_with(46)

    def test_single_step_safe_nobranch_two_word_instr(self):
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.dbg.program_counter_read.return_value = 22
        self.bp._read_flash_word.side_effect = [ 0x9000, 0x9000, 0x88FF ]
        self.assertTrue(self.bp.two_word_instr(0x9000))
        self.assertFalse(self.bp.branch_instr(0x9000))
        self.assertEqual(self.bp.single_step(None), None)
        self.bp.dbg.step.assert_not_called()
        self.bp.dbg.run_to.assert_called_with(48)

    def test_single_step_safe_branch_one_word_instr(self):
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.dbg.program_counter_read.return_value = 22
        self.bp._read_flash_word.side_effect = [ 0x9518, 0x9518, 0x8FFF ]
        self.assertFalse(self.bp.two_word_instr(0x9518))
        self.assertTrue(self.bp.branch_instr(0x9518))
        self.bp.dbg.status_register_read.side_effect = [ bytearray([0x88]), bytearray([0x07]) ]
        self.assertEqual(self.bp.single_step(None), SIGTRAP)
        self.bp._read_flash_word.assert_has_calls([call(44), call(44)], any_order=True)
        self.bp.dbg.status_register_write.assert_has_calls([ call(bytearray([0x08])), call(bytearray([0x87])) ])
        self.assertEqual(self.bp.dbg.status_register_read.call_count, 2)
        self.bp.dbg.step.assert_called_once()
        self.bp.dbg.run_to.assert_not_called()

    def test_single_step_safe_branch_two_word_instr(self):
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.dbg.program_counter_read.return_value = 22
        self.bp._read_flash_word.side_effect = [ 0x950C, 0x950C, 0x8FFF ]
        self.assertTrue(self.bp.two_word_instr(0x950C))
        self.assertTrue(self.bp.branch_instr(0x950C))
        self.bp.dbg.status_register_read.side_effect = [ bytearray([0x88]), bytearray([0x07]) ]
        self.assertEqual(self.bp.single_step(None), 5)
        self.bp._read_flash_word.assert_has_calls([call(44), call(44)], any_order=True)
        self.bp.dbg.status_register_write.assert_has_calls([ call(bytearray([0x08])), call(bytearray([0x87])) ])
        self.assertEqual(self.bp.dbg.status_register_read.call_count, 2)
        self.bp.dbg.step.assert_called_once()
        self.bp.dbg.run_to.assert_not_called()

    def test_single_step_safe_brie(self):
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.dbg.program_counter_read.return_value = 22
        self.bp._read_flash_word.side_effect = [ 0xF017, 0xF017 ]
        self.assertTrue(self.bp.branch_on_ibit(0xF017)) # BRIE .+2
        self.bp.dbg.status_register_read.side_effect = [ bytearray([0x88]) ]
        self.assertEqual(self.bp.single_step(None), None)
        self.bp._read_flash_word.assert_has_calls([call(44), call(44)], any_order=True)
        self.assertEqual(self.bp.dbg.status_register_read.call_count, 1)
        self.bp.dbg.step.assert_not_called()
        self.bp.dbg.run_to.assert_called_with(50)

    def test_range_step_impossible_mon(self):
        self.bp.mon.is_old_exec.return_value = True
        self.bp.mon.is_range.return_value = False
        self.bp.mon.is_onlyswbps.return_value = False
        self.assertEqual(self.bp.range_step(10,20), SIGTRAP)
        self.bp.dbg.program_counter_read.assert_called_once()
        self.bp.dbg.step.assert_called_once()
        self.bp.dbg.run.assert_not_called()
        self.bp.dbg.run_to.assert_not_called()
        self.bp._read_flash_word.assert_called_once()

    def test_range_step_impossible_odd(self):
        self.bp.mon.is_old_exec.return_value = False
        self.bp.mon.is_range.return_value = True
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.dbg.program_counter_read.return_value = 10
        self.bp._read_flash_word.return_value = 0x0000
        self.assertEqual(self.bp.range_step(9,50), None)
        self.bp.dbg.program_counter_read.assert_called_once()
        self.bp._read_flash_word.assert_called_with(20)
        self.bp.dbg.run_to.assert_called_with(22)
        self.bp.dbg.run.assert_not_called()
        self.bp.dbg.step.assert_not_called()

    def test_range_step_impossible_onlyhwbp(self):
        self.bp.mon.is_old_exec.return_value = False
        self.bp.mon.is_range.return_value = True
        self.bp.mon.is_onlyhwbps.return_value = True
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.insert_breakpoint(100)
        code = [ 0xef2f, 0xee81, 0xe094 ]
        self.bp._read_flash_word.side_effect = code
        self.assertEqual(self.bp.range_step(10,14), SIGABRT)
        self.bp.dbg.step.assert_not_called()
        self.bp.dbg.run.assert_not_called()
        self.bp.dbg.run_to.assert_not_called()

    def test_range_step_break(self):
        self.bp.mon.is_old_exec.return_value = False
        self.bp.mon.is_range.return_value = True
        self.bp.mon.is_onlyhwbps.return_value = False
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.insert_breakpoint(100)
        self.bp.dbg.program_counter_read.return_value = 10
        code = [ BREAKCODE, 0xef2f, 0xee81, 0xe094, BREAKCODE ]
        self.bp._read_flash_word.side_effect = code
        self.assertEqual(self.bp.range_step(10,16), SIGILL)
        self.bp.dbg.step.assert_not_called()
        self.bp.dbg.run.assert_not_called()
        self.bp.dbg.run_to.assert_not_called()

    def test_range_step_sleep(self):
        self.bp.mon.is_old_exec.return_value = False
        self.bp.mon.is_range.return_value = True
        self.bp.mon.is_onlyhwbps.return_value = False
        self.bp.mon.is_onlyswbps.return_value = False
        self.bp.insert_breakpoint(100)
        self.bp.dbg.program_counter_read.return_value = 10
        code = [ SLEEPCODE, 0xef2f, 0xee81, 0xe094, SLEEPCODE ]
        self.bp._read_flash_word.side_effect = code
        self.assertEqual(self.bp.range_step(10,16), SIGTRAP)
        self.bp.dbg.program_counter_write.assert_called_with(11)
        self.bp.dbg.step.assert_not_called()
        self.bp.dbg.run.assert_not_called()
        self.bp.dbg.run_to.assert_not_called()

    def test_range_step_race_to_branch(self):
        self.bp.mon.is_onlyswbps.return_value = False
        # while (++i) { if ( i < 0 ) return(i); }
        code = [ 0x2f98, 0x5f8f, 0xf011, 0xf7e2, 0x9508, 0xe083, 0x2f98, ]
        self.bp._read_flash_word.side_effect = code
        start = 0x033a
        end = 0x0344
        self.bp.build_range(start, end)
        self.bp.dbg.program_counter_read.return_value = start >> 1
        self.assertEqual(self.bp.range_step(start, end), None)
        self.bp.dbg.run_to.assert_called_with(0x033e)

    def test_range_step_return_after_first_step(self):
        self.bp.mon.is_onlyswbps.return_value = False
        # while (++i) { if ( i < 0 ) return(i); }
        code = [ 0x2f98, 0x5f8f, 0xf011, 0xf7e2, 0x9508, 0xe083, 0x2f98, 0x2f98, 0x2f98, 0x2f98 ]
        self.bp._read_flash_word.side_effect = code
        start = 0x033a
        end = 0x0344
        self.bp.dbg.program_counter_read.return_value = start >> 1
        self.assertEqual(self.bp.range_step(start, end), None)
        self.bp.dbg.run_to.assert_called_with(0x33c)

    def test_build_range_one_exit(self):
        # _delay_ms(100)
        code = [ 0xef2f, 0xee81, 0xe094, 0x5021, 0x4080, 0x0490, 0xf7e1, 0xc000, 0x0000, 0xe061 ]
        self.bp._read_flash_word.side_effect = code
        start = 0x0364
        end = 0x0376
        self.bp.build_range(start, end)
        self.assertEqual(start, self.bp._range_start)
        self.assertEqual(end, self.bp._range_end)
        self.assertEqual(code, self.bp._range_word)
        self.assertEqual(set([0x376]), self.bp._range_exit)
        self.assertEqual([ 0x370, 0x372, 0x376], self.bp._range_branch)

    def test_build_range_two_exits(self):
        # while (++i) { if ( i < 0 ) return(i); }
        code = [ 0x2f98, 0x5f8f, 0xf011, 0xf7e2, 0x9508, 0xe083 ]
        self.bp._read_flash_word.side_effect = code
        start = 0x033a
        end = 0x0344
        self.bp.build_range(start, end)
        self.assertEqual(start, self.bp._range_start)
        self.assertEqual(end, self.bp._range_end)
        self.assertEqual(code, self.bp._range_word)
        self.assertEqual(set([0x342, 0x344]), self.bp._range_exit)
        self.assertEqual([ 0x33e, 0x340, 0x342, 0x344], self.bp._range_branch)

    def test_store_instr(self):
        for instr in range(0x10000):
            self.assertEqual(self.bp.store_instr(instr),
                                 instrmap.get(instr,(None, None, None))[2] in ['store'],
                                 "Failed at 0x%04X" % instr)


    def test_branch_instr(self):
        for instr in range(0x10000):
            self.assertEqual(self.bp.branch_instr(instr),
                                 instrmap.get(instr,(None, None, None))[2] in ['branch', 'cond', 'icond'],
                                 "Failed at 0x%04X" % instr)

    def test_relative_branch_operation(self):
        for instr in range(0x10000):
            self.assertEqual(self.bp.relative_branch_operation(instr), instrmap.get(instr,(None, None, None))[0] in ['rcall', 'rjmp'])

    def test_compute_destination_of_relative_branch(self):
        self.assertEqual(self.bp.compute_destination_of_relative_branch(0xD100, 0x2000), 0x2202)
        self.assertEqual(self.bp.compute_destination_of_relative_branch(0xCFFF, 0x2000), 0x2000)

    def test_skip_operation(self):
        for instr in range(0x10000):
            self.assertEqual(self.bp.skip_operation(instr),
                                 instrmap.get(instr,(None, None, None))[0] in ['cpse', 'sbic', 'sbis', 'sbrc', 'sbrs'],
                                 "Failed at 0x%04X" % instr)

    def test_cond_branch_operation(self):
        for instr in range(0x10000):
            self.assertEqual(self.bp.cond_branch_operation(instr),
                                 instrmap.get(instr,('None', None, None))[0][:2] == 'br' and \
                                 instrmap.get(instr,(None, None, None))[2] in ['cond', 'icond'],
                                 "Failed at 0x%04X" % instr)

    def test_branch_on_ibit(self):
        for instr in range(0x10000):
            self.assertEqual(self.bp.branch_on_ibit(instr),
                                 instrmap.get(instr,(None, None, None))[2] in ['icond'],
                                 "Failed at 0x%04X" % instr)

    def test_compute_possible_destination_of_branch(self):
        self.assertEqual(self.bp.compute_possible_destination_of_branch(0xF02F, 20), 32)
        self.assertEqual(self.bp.compute_possible_destination_of_branch(0xF7FF, 20), 20)


    def test_computeDestinationOfBranch(self):
        self.assertEqual(self.bp.compute_destination_of_ibranch(0xF02F, 1, 20), 32)
        self.assertEqual(self.bp.compute_destination_of_ibranch(0xF3FF, 1, 20), 20)
        self.assertEqual(self.bp.compute_destination_of_ibranch(0xF02F, 0, 20), 22)
        self.assertEqual(self.bp.compute_destination_of_ibranch(0xF3FF, 0, 20), 22)
        self.assertEqual(self.bp.compute_destination_of_ibranch(0xF42F, 0, 20), 32)
        self.assertEqual(self.bp.compute_destination_of_ibranch(0xF7FF, 0, 20), 20)
        self.assertEqual(self.bp.compute_destination_of_ibranch(0xF42F, 1, 20), 22)
        self.assertEqual(self.bp.compute_destination_of_ibranch(0xF7FF, 1, 20), 22)

    def test_two_word_instr(self):
        for instr in range(0x10000):
            self.assertEqual(self.bp.two_word_instr(instr),
                                 instrmap.get(instr,(None, None, None))[1] == 2,
                                 "Failed at 0x%04X" % instr)

    def test_sim_two_word_instr_lds(self):
        self.bp.dbg.sram_read.return_value = bytearray(0x55)
        self.assertTrue(self.bp.two_word_instr(0x90F0))
        self.assertEqual(self.bp.sim_two_word_instr(0x90F0, 0x1000, 0x2002), 0x2006)
        self.bp.dbg.sram_read.assert_called_with(0x1000,1)
        self.bp.dbg.sram_write.assert_called_with(15,bytearray(0x55))

    def test_sim_two_word_instr_sts(self):
        self.bp.dbg.sram_read.return_value = bytearray(0x44)
        self.assertTrue(self.bp.two_word_instr(0x92E0))
        self.assertEqual(self.bp.sim_two_word_instr(0x92E0, 0x1000, 0x2002), 0x2006)
        self.bp.dbg.sram_read.assert_called_with(14,1)
        self.bp.dbg.sram_write.assert_called_with(0x1000,bytearray(0x44))

    def test_sim_two_word_instr_jmp_small(self):
        self.assertTrue(self.bp.two_word_instr(0x940C))
        self.assertEqual(self.bp.sim_two_word_instr(0x940C, 0x2244, 0x2002), 0x4488)

    def test_sim_two_word_instr_call_small(self):
        self.bp.dbg.stack_pointer_read.return_value = bytearray([0x02, 0x01])
        self.assertEqual(self.bp.sim_two_word_instr(0x940E, 0x2244, 0x2002), 0x4488)
        self.bp.dbg.stack_pointer_write.assert_called_with(bytearray([0x00, 0x01]))
        self.bp.dbg.sram_write.assert_called_with(0x101, bytearray([0x10, 0x03]))
