"""
Test suite for the HardwareBP class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods

from unittest.mock import call, create_autospec,  Mock
from unittest import TestCase
from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.hardwarebp import HardwareBP

class TestHardwareBP(TestCase):

    def setUp(self):
        self.hbp = None

    def set_up(self):
        mock_dbg = create_autospec(XAvrDebugger)
        mock_dbg.get_hwbpnum.return_value = 3
        self.hbp = HardwareBP(mock_dbg)

    def test_execute_no_hwbp(self):
        self.set_up()
        self.hbp.execute()
        self.hbp.dbg.run.assert_called_once()
        self.hbp.dbg.run_to.assert_not_called()

    def test_execute_with_hwbp0(self):
        self.set_up()
        self.hbp.set(100)
        self.hbp.execute()
        self.hbp.dbg.run.assert_not_called()
        self.hbp.dbg.run_to.assert_called_with(100)

    def test_clear_all_full(self):
        self.set_up()
        self.hbp.set(100)
        self.hbp.set(200)
        self.hbp.clear_all()
        self.assertTrue(self.hbp._hwbplist == [ None, None, None ])
        self.hbp.dbg.hardware_breakpoint_clear.assert_has_calls([call(1), call(2)], any_order=True)

    def test_clear_all_hwbp0(self):
        self.set_up()
        self.hbp.set(100)
        self.hbp.clear_all()
        self.assertTrue(self.hbp._hwbplist == [ None, None, None ])
        self.hbp.dbg.hardware_breakpoint_clear.assert_has_calls([call(1), call(2)], any_order=True)

    def test_clear_present(self):
        self.set_up()
        self.hbp.set(100)
        self.hbp.set(200)
        self.assertTrue(self.hbp.clear(100))
        self.assertEqual(self.hbp._hwbplist, [ None, 200, None ])

    def test_clear_not_present(self):
        self.set_up()
        self.hbp.set(100)
        self.hbp.set(200)
        self.assertFalse(self.hbp.clear(150))
        self.assertEqual(self.hbp._hwbplist, [ 100, 200, None ])

    def test_free_present(self):
        self.set_up()
        self.hbp.set(100)
        self.hbp.set(200)
        self.assertTrue(self.hbp._free(1))
        self.assertEqual(self.hbp._hwbplist, [ 100, None, None ])

    def test_free_not_present(self):
        self.set_up()
        self.hbp.set(100)
        self.hbp.set(200)
        self.assertFalse(self.hbp._free(2))
        self.assertEqual(self.hbp._hwbplist, [ 100, 200, None ])

    def test_available_3(self):
        self.set_up()
        self.assertEqual(self.hbp.available(), 3)

    def test_available_1(self):
        self.set_up()
        self.hbp.set(100)
        self.hbp.set(200)
        self.assertEqual(self.hbp.available(), 1)

    def test_set_succ(self):
        self.set_up()
        self.hbp._hwbplist = [ 100, None, 200 ]
        self.assertEqual(self.hbp.set(998), 1)
        self.assertEqual(self.hbp.available(), 0)

    def test_set_fail(self):
        self.set_up()
        self.hbp._hwbplist = [ 100, 200, 300 ]
        self.assertEqual(self.hbp.set(998), None)
        self.assertEqual(self.hbp.available(), 0)

    def test_set_temp_imposs(self):
        self.set_up()
        self.hbp._hwbplist = [ 100, 200, 300 ]
        self.assertEqual(self.hbp.set_temp([2,4,6,8]), None)
        self.assertEqual(self.hbp._hwbplist, [ 100, 200, 300 ])
        self.assertEqual(self.hbp._tempalloc, None)

    def test_set_temp_poss2(self):
        self.set_up()
        self.hbp._hwbplist = [ 100, 200, 300 ]
        self.assertEqual(self.hbp.set_temp([4, 2]), [ 300, 200 ])
        self.assertEqual(self.hbp._tempalloc, [2, 1])
        self.assertEqual(self.hbp._hwbplist, [ 100, 2, 4 ])

    def test_clear_temp(self):
        self.set_up()
        self.hbp.logger = Mock()
        self.hbp._hwbplist = [ 100, 200, 300 ]
        self.hbp.set_temp([10,20])
        self.hbp.clear_temp()
        self.assertEqual(self.hbp._hwbplist, [ 100, None, None ])
        self.assertEqual(self.hbp._tempalloc, None)
        self.hbp.clear_temp()
        self.assertEqual(self.hbp._tempalloc, None)
        self.assertEqual(self.hbp._hwbplist, [ 100, None, None ])
        self.hbp.logger.debug.assert_has_calls([call('Trying to allocate %d temp HWBPs', 2),
                call('Trying to allocate HWBP for addr 0x%X', 10),
                call('Could not allocate a HWBP'),
                call('HWBP %d at addr 0x%X freed', 2, 300),
                call('Trying to allocate HWBP for addr 0x%X', 10),
                call('Successfully allocated HWBP %d', 2),
                call('Trying to allocate HWBP for addr 0x%X', 20),
                call('Could not allocate a HWBP'),
                call('HWBP %d at addr 0x%X freed', 1, 200),
                call('Trying to allocate HWBP for addr 0x%X', 20),
                call('Successfully allocated HWBP %d', 1),
                call('Allocated %d temp HWBPs', 2),
                call('HWBP %d at addr 0x%X freed', 2, 10),
                call('HWBP %d at addr 0x%X freed', 1, 20),
                call('HWBP temp allocation cleared: %d HWBPs cleared', 2)])

    def test_hwbp_borrow_empty(self):
        self.set_up()
        self.hbp.logger = Mock()
        self.hbp._hwbplist = [ None, None, None ]
        self.assertEqual(self.hbp.borrow_hwbp0(), None)

    def test_hwbp_borrow_free_slot(self):
        self.set_up()
        self.hbp.logger = Mock()
        self.hbp._hwbplist = [ 100, None, 200 ]
        self.assertEqual(self.hbp.borrow_hwbp0(), None)
        self.assertEqual(self.hbp._hwbplist, [ None, 100, 200 ])

    def test_hwbp_borrow_no_free_slot(self):
        self.set_up()
        self.hbp.logger = Mock()
        self.hbp._hwbplist = [ 100, 200, 300 ]
        self.assertEqual(self.hbp.borrow_hwbp0(), 100)
        self.assertEqual(self.hbp._hwbplist, [ None, 200, 300 ])


