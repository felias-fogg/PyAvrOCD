"""
Signals at random moments while mkII-protocol transactions run with a real JTAGICE mkII,
AVR Dragon or dw-link, with and without the guard of pyavrocd.termination. After every
interrupt: does the next command get its own answer, is nothing left pending, and how many
stale responses did Jtag2Protocol.command have to drop on the way? No target
needed. The commands alternate between a short GET, a device descriptor that spans several
USB packets (several hundred ms on dw-link's serial line), and a poll for break events.

Unix: SIGTERM via os.kill. Windows: SIGINT via signal.raise_signal from a timer thread.

    python tests/stress/sigstress_jtag2.py list
    python tests/stress/sigstress_jtag2.py usb <serial suffix> guarded|unguarded|noop [rounds]
    python tests/stress/sigstress_jtag2.py serial <port> guarded|unguarded|noop [rounds]
"""
import argparse
import contextlib
import logging
import os
import random
import signal
import sys
import threading
import time
from typing import Any

import usb.core

from pyavrocd import jtag2
from pyavrocd.deviceinfo.devices import atmega328p
from pyavrocd.errors import TerminationRequest
from pyavrocd.termination import interrupt

WINDOWS = sys.platform == "win32"
SIG = signal.SIGINT if WINDOWS else signal.SIGTERM
SIG_NAME = "SIGINT" if WINDOWS else "SIGTERM"
EXC : type[BaseException] = KeyboardInterrupt if WINDOWS else TerminationRequest
DESCRIPTOR = jtag2.make_device_descriptor(atmega328p.DEVICE_INFO)


class Stress():
    """One probe, one mode: interrupt a stream of transactions, then check the probe"""

    def __init__(self, proto : jtag2.Jtag2Protocol, mode : str) -> None:
        self.proto = proto
        self.mode = mode
        self.fired = 0
        self.stats = {"ok": 0, "wrong answer": 0, "error": 0, "left pending": 0,
                      "stale dropped": 0, "transactions": 0, "loop errors": 0}
        self.errors : list[str] = []
        self.hw_version = proto.get_parameter(jtag2.PAR_HW_VERSION)
        # Jtag2Protocol.command drops a stale response and reads on; count those from its log
        stats = self.stats
        class Count(logging.Handler):
            """Counts the stale responses Jtag2Protocol.command drops"""
            def emit(self, record : logging.LogRecord) -> None:
                if "dropped while waiting" in record.getMessage():
                    stats["stale dropped"] += 1
        logger = logging.getLogger("pyavrocd.jtag2")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        logger.addHandler(Count())

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
        """Is a frame waiting to be fetched? Discards everything that is there."""
        try:
            frame = self.proto.transport.read_frame(100)
        except (usb.core.USBTimeoutError, TimeoutError):
            return False
        self.proto.transport.flush()
        self.errors.append(f"pending: {frame.hex()[:40]}")
        return True

    def step(self, k : int) -> None:
        """One transaction of the mix"""
        if k % 3 == 0:
            self.proto.get_parameter(jtag2.PAR_HW_VERSION)
        elif k % 3 == 1:
            self.proto.set_device_descriptor(DESCRIPTOR)
        else:
            self.proto.poll_break(1)

    def round(self, n : int) -> None:
        """Run transactions until the signal comes, then check the probe"""
        goal = self.fired + 1
        threading.Timer(random.uniform(0.005, 0.030), self.fire).start()
        k = random.randrange(3)
        try:
            while self.fired < goal:
                try:
                    self.step(k)
                    k += 1
                    self.stats["transactions"] += 1
                except (jtag2.Jtag2Error, usb.core.USBError) as e:
                    self.stats["loop errors"] += 1
                    self.errors.append(f"round {n}: {type(e).__name__}: {e}")
                    self.proto.transport.flush()
        except EXC:
            pass
        try:
            v = self.proto.get_parameter(jtag2.PAR_HW_VERSION)
            self.stats["ok" if v == self.hw_version else "wrong answer"] += 1
        except (jtag2.Jtag2Error, usb.core.USBError) as e:
            self.stats["wrong answer" if "while waiting for" in str(e) else "error"] += 1
            self.errors.append(f"check {n}: {type(e).__name__}: {e}")
        if self.pending():
            self.stats["left pending"] += 1


def open_probe(kind : str, address : str) -> tuple[jtag2.Jtag2Protocol, str]:
    """Open and sign on; returns the protocol and the probe's name"""
    transport : jtag2.Jtag2UsbTransport | jtag2.Jtag2SerialTransport
    if kind == "usb":
        deadline = time.monotonic() + 8   # after a sign-off the probe leaves the bus for 1.5 to 3 s
        while True:
            try:
                transport = jtag2.Jtag2UsbTransport.open(serial_suffix=address)
                break
            except (jtag2.Jtag2Error, usb.core.USBError):
                if time.monotonic() > deadline:
                    raise
                time.sleep(0.3)
    else:
        transport = jtag2.Jtag2SerialTransport(address)
    proto = jtag2.Jtag2Protocol(transport)
    sign_on = None
    for _ in range(20):        # opening the port resets an Arduino; its bootloader waits a moment
        try:
            sign_on = proto.sign_on(300)
            break
        except jtag2.Jtag2Error:
            transport.flush()
    if sign_on is None:
        raise jtag2.Jtag2Error("No sign-on from {}".format(address))
    return proto, "{} {:X}.{:02X}".format(sign_on.ident, *sign_on.master_firmware)


def main() -> int:
    """Parse the arguments, run the rounds, print the statistics"""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", maxsplit=1)[0])
    parser.add_argument("kind", choices=["list", "usb", "serial"])
    parser.add_argument("address", nargs="?", default="", help="end of the USB serial number, or the port")
    parser.add_argument("mode", nargs="?", choices=["guarded", "unguarded", "noop"])
    parser.add_argument("rounds", nargs="?", type=int, default=100)
    args = parser.parse_args()
    if args.kind == "list":
        for c in jtag2.discover():
            print(c.product, c.address)
        return 0
    if args.mode is None:
        parser.error("mode is required")
    if args.mode != "guarded":
        jtag2.transaction = contextlib.nullcontext     # type: ignore[assignment]
    proto, name = open_probe(args.kind, args.address)
    stress = Stress(proto, args.mode)
    signal.signal(SIG, stress.handler)
    for n in range(args.rounds):
        stress.round(n)
    signal.signal(SIG, signal.SIG_DFL)
    try:
        proto.sign_off()
    except jtag2.Jtag2Error as e:
        print("sign-off failed:", e)
    proto.transport.close()
    print(f"{sys.platform} {name:26s} {SIG_NAME} {args.mode:9s} rounds={args.rounds} {stress.stats}")
    if stress.errors:
        print("   first errors:", stress.errors[:3])
    return 0


if __name__ == "__main__":
    sys.exit(main())
