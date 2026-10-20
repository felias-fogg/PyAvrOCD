"""
The test suit for termination module
"""
#pylint: disable=protected-access,missing-function-docstring,missing-class-docstring
import os
import signal
from unittest import TestCase, skipUnless
from unittest.mock import Mock

from pyedbglib.protocols.dapwrapper import DapWrapper
from pyedbglib.protocols.avrcmsisdap import AvrCommand

from pyavrocd import termination
from pyavrocd.termination import interrupt, transaction, guard_probe_transactions
from pyavrocd.errors import TerminationRequest

class TestTermination(TestCase):

    def setUp(self):
        termination._deferral.depth = 0
        termination._deferral.pending = None

    def test_interrupt_outside_transaction(self):
        with self.assertRaises(TerminationRequest):
            interrupt(TerminationRequest())

    def test_interrupt_deferred_to_end_of_transaction(self):
        done = []
        with self.assertRaises(KeyboardInterrupt):
            with transaction():
                interrupt(KeyboardInterrupt())
                done.append(1) # the rest of the transaction still runs
        self.assertEqual(done, [1])
        self.assertEqual(termination._deferral.depth, 0)
        self.assertIsNone(termination._deferral.pending)

    def test_nested_transactions_raise_at_outermost_end(self):
        done = []
        with self.assertRaises(TerminationRequest):
            with transaction():
                with transaction():
                    interrupt(TerminationRequest())
                done.append(1) # not raised at the end of the inner one
        self.assertEqual(done, [1])

    def test_first_interrupt_wins(self):
        with self.assertRaises(TerminationRequest):
            with transaction():
                interrupt(TerminationRequest())
                interrupt(KeyboardInterrupt())

    def test_pending_interrupt_replaces_exception_of_transaction(self):
        with self.assertRaises(TerminationRequest) as cm:
            with transaction():
                interrupt(TerminationRequest())
                raise ValueError("probe error")
        self.assertIsInstance(cm.exception.__context__, ValueError)

    @skipUnless(hasattr(signal, 'pthread_sigmask'), "no signal masks on this OS")
    def test_signals_blocked_during_transaction(self):
        def blocked():
            return signal.pthread_sigmask(signal.SIG_BLOCK, []) # pylint: disable=no-member
        self.assertNotIn(signal.SIGTERM, blocked())
        with transaction():
            with transaction():
                self.assertTrue({signal.SIGTERM, signal.SIGINT} <= blocked())
            self.assertIn(signal.SIGTERM, blocked()) # still blocked after the inner one
        self.assertNotIn(signal.SIGTERM, blocked())
        self.assertNotIn(signal.SIGINT, blocked())

    @skipUnless(hasattr(signal, 'pthread_sigmask'), "no signal masks on this OS")
    def test_real_signal_handled_after_transaction(self):
        log = []
        def handler(_signo, _frame):
            log.append('handler')
            interrupt(TerminationRequest())
        old = signal.signal(signal.SIGTERM, handler)
        try:
            with self.assertRaises(TerminationRequest):
                with transaction():
                    os.kill(os.getpid(), signal.SIGTERM)
                    log.append('transaction completed')
        finally:
            signal.signal(signal.SIGTERM, old)
        self.assertEqual(log, ['transaction completed', 'handler'])

    def test_guard_probe_transactions(self):
        guard_probe_transactions()
        guard_probe_transactions() # idempotent: wrapped once only
        for method in (DapWrapper.dap_command_response, AvrCommand.avr_command_response):
            self.assertTrue(getattr(method, '_guarded'))
            self.assertFalse(getattr(getattr(method, '__wrapped__'), '_guarded', False))
        transport = Mock()
        transport.hid_transfer.side_effect = lambda packet: interrupt(TerminationRequest()) or b'rsp'
        with self.assertRaises(TerminationRequest):
            DapWrapper(transport).dap_command_response(b'cmd')
        transport.hid_transfer.assert_called_once_with(b'cmd') # the transfer was completed
