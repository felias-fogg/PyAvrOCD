"""
This module defers SIGTERM and SIGINT while a transaction with the debug probe is under way.

A transaction cut short confuses the probe: if the response is never fetched, SNAP,
PICkit4, nEDBG and mEDBG drop the next command and hand out the old response instead;
if a command is cut between its fragments, all EDBG-based probes take the next command
as its missing tail. Either way, the cleanup after the interrupt would run on a
confused probe. A transaction lasts milliseconds, so waiting for its end costs nothing.

Deferring the Python-level handler alone is not enough: on macOS, a signal that arrives
while hidapi is inside a C call makes that call fail, even with a handler that does
nothing. Where the OS allows it, the signals are therefore also blocked for the duration
of the transaction; the kernel delivers them as soon as the block is lifted.
"""
import functools
import signal
import sys
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any

from pyedbglib.protocols.dapwrapper import DapWrapper
from pyedbglib.protocols.avrcmsisdap import AvrCommand

_DEFERRED_SIGNALS : set[signal.Signals] = {signal.SIGTERM, signal.SIGINT}

# mypy understands the platform check, pylint does not: under Windows it finds no
# pthread_sigmask, SIG_BLOCK or SIG_SETMASK in the signal module, hence the disables
if sys.platform != "win32":
    def _block_signals() -> set[int | signal.Signals]:
        return signal.pthread_sigmask(signal.SIG_BLOCK, _DEFERRED_SIGNALS) # pylint: disable=no-member

    def _restore_signals(mask : set[int | signal.Signals]) -> None:
        signal.pthread_sigmask(signal.SIG_SETMASK, mask) # pylint: disable=no-member
else: # no signal masks under Windows
    def _block_signals() -> set[int | signal.Signals]:
        return set()

    def _restore_signals(_mask : set[int | signal.Signals]) -> None:
        pass

class _Deferral():
    """
    Nesting depth of the running transactions and the interrupt waiting for their end

    The guard covers only the EDBG-based probes, whose traffic passes through the two
    pyedbglib methods wrapped by guard_probe_transactions. Any other transport has to be
    wrapped in transaction() the same way: dw-link over serial, and the bulk-transport
    tools (AVRISP mkII, Dragon, PICkit5) through libusb, once they arrive. What counts as
    one transaction there -- a command together with its complete response -- depends on
    the transport, so the wrapped methods will look different.
    """
    def __init__(self) -> None:
        self.depth : int = 0
        self.pending : BaseException | None = None
        self.saved_mask : set[int | signal.Signals] = set()

    def interrupt(self, exc : BaseException) -> None:
        """
        Raise exc now, or at the end of the current transaction if one is under way.
        Called from signal handlers, which run in the main thread between two bytecodes.
        """
        if self.depth > 0:
            if self.pending is None:
                self.pending = exc
            return
        raise exc

    @contextmanager
    def transaction(self) -> Iterator[None]:
        """
        Context in which interrupts are deferred
        """
        if self.depth == 0:
            self.saved_mask = _block_signals()
        self.depth += 1
        try:
            yield
        finally:
            self.depth -= 1
            if self.depth == 0:
                # take the pending interrupt first: unblocking may raise right away
                exc : BaseException | None = self.pending
                self.pending = None
                # a signal held back by the kernel is handled right here, at depth 0
                _restore_signals(self.saved_mask)
                if exc is not None:
                    raise exc

_deferral = _Deferral()
interrupt = _deferral.interrupt
transaction = _deferral.transaction


def _guarded(method : Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(method)
    def wrapper(*args : Any, **kwargs : Any) -> Any:
        with transaction():
            return method(*args, **kwargs)
    setattr(wrapper, '_guarded', True)
    return wrapper


def guard_probe_transactions() -> None:
    """
    Wrap the two pyedbglib methods through which all traffic with the probe passes:
    dap_command_response sends one HID report and reads the answer, avr_command_response
    sends all fragments of a command and collects all fragments of the response.
    Can be called more than once.
    """
    for cls, name in ((DapWrapper, 'dap_command_response'), (AvrCommand, 'avr_command_response')):
        method = getattr(cls, name)
        if not getattr(method, '_guarded', False):
            setattr(cls, name, _guarded(method))
