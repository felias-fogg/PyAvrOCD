"""
The test suit for the backend module: the parts of DebugBackend that are not abstract
"""
#pylint: disable=protected-access,missing-function-docstring,missing-class-docstring,invalid-name
# The fake backend is built with type(), which pylint cannot follow:
#pylint: disable=no-member,abstract-class-instantiated
from unittest import TestCase
from unittest.mock import Mock

from pyavrocd.backend import DebugBackend, SwbpSupport, BREAKCODE, BackendNotSupportedError

PAGE = 128

def make_backend(support):
    """A backend with 1 kB of flash in memory; all other abstract methods do nothing"""
    abstract = {name: (lambda *args, **kwargs: None) for name in DebugBackend.__abstractmethods__}
    cls = type("FakeBackend", (DebugBackend,), abstract)
    cls.SWBP_SUPPORT = support
    be = cls("atmega328p", "debugwire")
    be.flash = bytearray(range(256)) * 4
    be.pc = 0
    be.memory_info = Mock()
    be.memory_info.memory_info_by_name.return_value = {'page_size': PAGE}
    be._flash_read = lambda address, numbytes, prog_mode=False: bytearray(be.flash[address:address+numbytes])
    def program(address, data):
        assert address % PAGE == 0 and len(data) == PAGE
        be.flash[address:address+PAGE] = data
    be.program_flash_page = Mock(side_effect=program)
    be.program_counter_read = lambda: be.pc >> 1
    be.execute_instruction = Mock()
    be._step = Mock()
    be._run = Mock()
    return be

def word(flash, address):
    return flash[address] | (flash[address+1] << 8)

class TestServerSoftwareBreakpoints(TestCase):

    def test_set_takes_effect_before_running_one_write_per_page(self):
        be = make_backend(SwbpSupport.SERVER)
        orig = bytes(be.flash)
        for a in (0x10, 0x20, 0x90): # two on page 0, one on page 1
            self.assertTrue(be.software_breakpoint_set(a))
        be.program_flash_page.assert_not_called() # nothing yet
        be.run()
        self.assertEqual(be.program_flash_page.call_count, 2)
        for a in (0x10, 0x20, 0x90):
            self.assertEqual(word(be.flash, a), BREAKCODE)
        self.assertEqual(be._swbp_planted[0x10], word(orig, 0x10))
        be._run.assert_called_once()

    def test_flash_read_returns_original_words(self):
        be = make_backend(SwbpSupport.SERVER)
        orig = bytes(be.flash)
        be.software_breakpoint_set(0x10)
        be.run()
        self.assertEqual(be.flash_read(0, 0x40), bytearray(orig[0:0x40]))
        self.assertEqual(be.flash_read(0x11, 1), bytearray(orig[0x11:0x12])) # odd start, one byte

    def test_unchanged_breakpoints_cost_no_writes(self):
        be = make_backend(SwbpSupport.SERVER)
        be.software_breakpoint_set(0x10)
        be.run()
        be.software_breakpoint_clear(0x10) # what GDB does after a stop ...
        be.software_breakpoint_set(0x10)   # ... and before the next run
        be.run()
        self.assertEqual(be.program_flash_page.call_count, 1)

    def test_step_over_breakpoint_injects_original(self):
        be = make_backend(SwbpSupport.SERVER)
        orig = bytes(be.flash)
        be.software_breakpoint_set(0x10)
        be.run()
        be.pc = 0x10
        be.step()
        be.execute_instruction.assert_called_once_with(word(orig, 0x10))
        be._step.assert_not_called()
        self.assertEqual(word(be.flash, 0x10), BREAKCODE) # stays in flash
        be.pc = 0x12
        be.step()
        be._step.assert_called_once()

    def test_clear_restores_and_clear_all_is_immediate(self):
        be = make_backend(SwbpSupport.SERVER)
        orig = bytes(be.flash)
        be.software_breakpoint_set(0x10)
        be.software_breakpoint_set(0x90)
        be.run()
        be.software_breakpoint_clear(0x10)
        be.run()
        self.assertEqual(word(be.flash, 0x10), word(orig, 0x10))
        self.assertEqual(word(be.flash, 0x90), BREAKCODE)
        be.software_breakpoint_clear_all()
        self.assertEqual(bytes(be.flash), orig)
        self.assertEqual(be._swbp_planted, {})

    def test_none_refuses_and_probe_does_nothing_itself(self):
        be = make_backend(SwbpSupport.NONE)
        self.assertFalse(be.software_breakpoint_set(0x10))
        be = make_backend(SwbpSupport.PROBE)
        be.software_breakpoint_set(0x10) # base implementation only records it
        be.run()
        be.program_flash_page.assert_not_called()

class TestOptionalCapabilities(TestCase):

    def test_defaults(self):
        be = make_backend(SwbpSupport.PROBE)
        self.assertFalse(be.can_power_cycle())
        self.assertFalse(be.power_cycle())
        self.assertFalse(be.can_switch_target_power())
        with self.assertRaises(BackendNotSupportedError):
            be.set_target_power(True)
