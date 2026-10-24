"""
The test suit for extras/powercycle/supplyctl.py, the gateway to the laboratory supply (with a fake supply)
"""
#pylint: disable=missing-function-docstring,missing-class-docstring,wrong-import-position,import-error
import os
import sys
from unittest import TestCase
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "extras", "powercycle"))
import supplyctl   # type: ignore[import-not-found]
from supplyctl import Refused, parse, execute

CONFIG = {"host": "10.33.0.2", "max_volt": {"1": 12.0}, "max_curr": {"1": 0.25}}

class FakeSupply():
    """Records the switching; answers the setpoint queries with the given values"""
    def __init__(self, volt="10.000", curr="0.120", error="0  No Error"):
        self.setpoints = {"VOLTage": volt, "CURRent": curr}
        self.error = error
        self.switched = []
    def query(self, command):
        return self.setpoints[command.split(":")[1].rstrip("?")]
    def switch(self, channel, state):
        self.switched.append((channel, state))
        return self.error
    def status(self, channel):
        return "CH{}: off".format(channel)

class TestParse(TestCase):

    def test_valid_requests(self):
        self.assertEqual(parse(["cycle", "1"]), ("cycle", 1, 1.0))
        self.assertEqual(parse(["cycle", "2", "1.5"]), ("cycle", 2, 1.5))
        self.assertEqual(parse(["on", "1"]), ("on", 1, 1.0))
        self.assertEqual(parse(["status", "2"]), ("status", 2, 1.0))

    def test_everything_else_is_refused(self):
        for words in ([], ["cycle"], ["volt", "1", "30"], ["on", "3"], ["on", "1", "2"], ["cycle", "1", "x"],
                      ["cycle", "1", "0"], ["cycle", "1", "11"], ["cycle", "1", "2", "3"], ["CH1:VOLT", "30"],
                      ["status", "1;", "rm"]):
            with self.assertRaises(Refused, msg=words):
                parse(words)

class TestExecute(TestCase):

    @patch('supplyctl.time.sleep')
    def test_cycle_within_ceilings(self, sleep):
        supply = FakeSupply()
        self.assertEqual(execute(supply, CONFIG, "cycle", 1, 2.0), "CH1 power-cycled")
        self.assertEqual(supply.switched, [(1, "OFF"), (1, "ON")])
        sleep.assert_called_once_with(2.0)

    def test_on_refused_above_voltage_ceiling(self):
        supply = FakeSupply(volt="30.000")
        with self.assertRaises(Refused):
            execute(supply, CONFIG, "on", 1, 1.0)
        self.assertEqual(supply.switched, [])

    def test_cycle_refused_above_current_ceiling_before_switching_off(self):
        supply = FakeSupply(curr="3.200")
        with self.assertRaises(Refused):
            execute(supply, CONFIG, "cycle", 1, 1.0)
        self.assertEqual(supply.switched, [])

    def test_channel_without_ceiling_cannot_be_switched_on(self):
        supply = FakeSupply()
        with self.assertRaises(Refused):
            execute(supply, CONFIG, "on", 2, 1.0)
        self.assertEqual(supply.switched, [])

    def test_off_and_status_need_no_ceiling(self):
        supply = FakeSupply(volt="30.000")
        self.assertEqual(execute(supply, CONFIG, "off", 2, 1.0), "CH2 off")
        self.assertEqual(execute(supply, CONFIG, "status", 2, 1.0), "CH2: off")
        self.assertEqual(supply.switched, [(2, "OFF")])

    def test_switch_not_accepted(self):
        supply = FakeSupply(error="3  Command keywords were not recognized")
        with self.assertRaises(Refused):
            execute(supply, CONFIG, "off", 1, 1.0)

class TestMain(TestCase):

    @patch.dict(os.environ, {"SSH_ORIGINAL_COMMAND": "volt 1 30"})
    @patch('supplyctl.Supply')
    def test_refused_request_never_connects(self, supply_class):
        with patch('supplyctl.syslog'):
            self.assertEqual(supplyctl.main(), 2)
        supply_class.assert_not_called()
