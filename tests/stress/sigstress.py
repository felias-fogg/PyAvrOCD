"""
Signals at random moments while transactions with a real probe run, with and without
the guard of pyavrocd.termination. After every interrupt: does a GET still return its
own answer, and is nothing left pending? No target needed, the commands are
housekeeping GETs, padded to three fragments.

Unix: SIGTERM via os.kill. Windows: SIGINT via signal.raise_signal from a timer
thread, so that the C-level handler runs outside the main thread, as with Ctrl-C.

    python tests/stress/sigstress.py list
    python tests/stress/sigstress.py <serial> guarded|unguarded|noop [rounds]
"""
import argparse
import os
import random
import signal
import sys
import threading
from typing import Any

from pyedbglib.hidtransport.hidtransportfactory import hid_transport
from pyedbglib.protocols.housekeepingprotocol import Jtagice3HousekeepingProtocol as HK

from pyavrocd.termination import guard_probe_transactions, interrupt
from pyavrocd.errors import TerminationRequest

WINDOWS = sys.platform == "win32"
SIG = signal.SIGINT if WINDOWS else signal.SIGTERM
SIG_NAME = "SIGINT" if WINDOWS else "SIGTERM"
EXC : type[BaseException] = KeyboardInterrupt if WINDOWS else TerminationRequest
CTX = HK.HOUSEKEEPING_CONTEXT_CONFIG


class Stress():
    """One probe, one mode: interrupt a stream of transactions, then check the probe"""

    def __init__(self, hk : HK, mode : str) -> None:
        self.hk = hk
        self.mode = mode
        self.fired = 0
        self.stats = {"ok": 0, "wrong answer": 0, "error": 0, "left pending": 0,
                      "transactions": 0, "loop errors": 0}
        self.errors : list[str] = []
        self.fw_major = hk.get_byte(CTX, HK.HOUSEKEEPING_CONFIG_FWREV_MAJ)
        self.cmd = [HK.CMD_GET, HK.CMD_VERSION0, CTX, HK.HOUSEKEEPING_CONFIG_BUILD, 2] + \
            [0] * (2 * hk.payload_start + 10)

    def handler(self, _signo : int, _frame : Any) -> None:
        """Signal handler: count, then do what the mode says"""
        self.fired += 1
        if self.mode == "noop":
            return
        if self.mode == "guarded":
            interrupt(EXC())
        else:
            raise EXC()

    @staticmethod
    def fire() -> None:
        """Send the signal, from the timer thread"""
        if WINDOWS:
            signal.raise_signal(SIG)
        else:
            os.kill(os.getpid(), SIG)

    def pending(self) -> bool:
        """Is a response waiting to be fetched? Fetches it if so."""
        r = self.hk.dap_command_response(bytearray([HK.AVR_RESPONSE]))
        return r[1] != HK.AVR_MORE_FRAGMENTS

    def drain(self) -> None:
        """Fetch and discard all pending responses"""
        while self.pending():
            pass

    def round(self, n : int) -> None:
        """Run transactions until the signal comes, then check the probe"""
        goal = self.fired + 1
        threading.Timer(random.uniform(0.005, 0.030), self.fire).start()
        try:
            while self.fired < goal:
                try:
                    self.hk.jtagice3_command_response(self.cmd)
                    self.stats["transactions"] += 1
                except Exception as e: # pylint: disable=broad-exception-caught
                    self.stats["loop errors"] += 1
                    self.errors.append(f"round {n}: {type(e).__name__}: {e}")
                    self.drain()
        except EXC:
            pass
        try:
            v = self.hk.get_byte(CTX, HK.HOUSEKEEPING_CONFIG_FWREV_MAJ)
            self.stats["ok" if v == self.fw_major else "wrong answer"] += 1
        except Exception as e: # pylint: disable=broad-exception-caught
            self.stats["error"] += 1
            self.errors.append(f"check {n}: {type(e).__name__}: {e}")
        if self.pending():
            self.stats["left pending"] += 1
            self.drain()


def main() -> int:
    """Parse the arguments, run the rounds, print the statistics"""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", maxsplit=1)[0])
    parser.add_argument("serial", help="serial number of the probe, or 'list'")
    parser.add_argument("mode", nargs="?", choices=["guarded", "unguarded", "noop"])
    parser.add_argument("rounds", nargs="?", type=int, default=100)
    args = parser.parse_args()
    if args.serial == "list":
        for d in hid_transport().devices:
            print(d.product_string, d.serial_number)
        return 0
    if args.mode is None:
        parser.error("mode is required")
    if args.mode == "guarded":
        guard_probe_transactions()
    transport = hid_transport()
    if not transport.connect(serial_number=args.serial):
        print("no tool found")
        return 1
    hk = HK(transport)
    hk.start_session()
    stress = Stress(hk, args.mode)
    signal.signal(SIG, stress.handler)
    for n in range(args.rounds):
        stress.round(n)
    signal.signal(SIG, signal.SIG_DFL)
    hk.end_session()
    transport.disconnect()
    print(f"{sys.platform} {transport.device.product_string:26s} {SIG_NAME} {args.mode:9s} "
          f"rounds={args.rounds} {stress.stats}")
    if stress.errors:
        print("   first errors:", stress.errors[:3])
    return 0


if __name__ == "__main__":
    sys.exit(main())
