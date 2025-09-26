"""
Test suite for the HardwareBP class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods

import logging
from unittest.mock import call, create_autospec
from unittest import TestCase
from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.hardwarebp import HardwareBP

logging.basicConfig(level=logging.CRITICAL)

class TestHardwareBP(TestCase):

    def setUp(self):
        mock_dbg = create_autospec(XAvrDebugger)
        mock_dbg.get_hwbpnum.return_value = 3
        self.hbp = HardwareBP(mock_dbg)

    def test_execute_no_hwbp(self):
        self.hbp.execute()
        self.hbp.dbg.run.assert_called_once()
        self.hbp.dbg.run_to.assert_not_called()

    def test_execute_with_hwbp0(self):
        self.hbp.set(100)
        self.hbp.execute()
        self.hbp.dbg.run.assert_not_called()
        self.hbp.dbg.run_to.assert_called_with(100)

    def test_clear_all_full(self):
        self.hbp.set(100)
        self.hbp.set(200)
        self.hbp.clear_all()
        self.assertTrue(self.hbp._hwbplist == [ None, None, None ])
        self.hbp.dbg.hardware_breakpoint_clear.assert_has_calls([call(1), call(2)], any_order=True)

    def test_clear_all_hwbp0(self):
        self.hbp.set(100)
        self.hbp.clear_all()
        self.assertTrue(self.hbp._hwbplist == [ None, None, None ])
        self.hbp.dbg.hardware_breakpoint_clear.assert_has_calls([call(1), call(2)], any_order=True)

    def test_clear_present(self):
        self.hbp.set(100)
        self.hbp.set(200)
        self.assertTrue(self.hbp.clear(100))
        self.assertEqual(self.hbp._hwbplist, [ None, 200, None ])

    def test_clear_not_present(self):
        self.hbp.set(100)
        self.hbp.set(200)
        self.assertFalse(self.hbp.clear(150))
        self.assertEqual(self.hbp._hwbplist, [ 100, 200, None ])

    def test_free_present(self):
        self.hbp.set(100)
        self.hbp.set(200)
        self.assertTrue(self.hbp._free(1))
        self.assertEqual(self.hbp._hwbplist, [ 100, None, None ])

    def test_free_not_present(self):
        self.hbp.set(100)
        self.hbp.set(200)
        self.assertFalse(self.hbp._free(2))
        self.assertEqual(self.hbp._hwbplist, [ 100, 200, None ])

    def test_available_3(self):
        self.assertEqual(self.hbp.available(), 3)

    def test_available_1(self):
        self.hbp.set(100)
        self.hbp.set(200)
        self.assertEqual(self.hbp.available(), 1)

    def test_set_succ(self):
        self.hbp._hwbplist = [ 100, None, 200 ]
        self.assertEqual(self.hbp.set(999), 1)
        self.assertEqual(self.hbp.available(), 0)

    def test_set_fail(self):
        self.hbp._hwbplist = [ 100, 200, 300 ]
        self.assertEqual(self.hbp.set(999), None)
        self.assertEqual(self.hbp.available(), 0)

    def test_set_temp_imposs(self):
        self.hbp._hwbplist = [ 100, 200, 300 ]
        self.assertEqual(self.hbp.set_temp([1,2,3,4]), None)
        self.assertEqual(self.hbp._hwbplist, [ 100, 200, 300 ])
        self.assertEqual(self.hbp._tempalloc, None)

    def test_set_temp_poss2(self):
        self.hbp._hwbplist = [ 100, 200, 300 ]
        self.assertEqual(self.hbp.set_temp([1,2]), [ 300, 200 ])
        self.assertEqual(self.hbp._hwbplist, [ 100, 2, 1 ])
        self.assertEqual(self.hbp._tempalloc, [2, 1])

    def tes_clear_temp(self):
        self.hbp._hwbplist = [ 100, 200, 300 ]
        self.hbp.set_temp([10,20])
        self.hbp.clear_temp()
        self.assertEqual(self.hbp._hwbplist, [ 100, None, None ])
        self.assertEqual(self.hbp._tempalloc, None)







