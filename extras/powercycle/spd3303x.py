#!/usr/bin/env python3
"""
Power-cycle one output of a Siglent SPD3303X/SPD3303X-E laboratory supply over the network:
switch it off, wait, switch it on again. Nothing else on the supply is touched; voltage and
current limits stay as they are set on the front panel.

The supply takes SCPI commands on a plain TCP socket, port 5025, without any VISA layer.
Measured with an SPD3303X, firmware 1.01.01.02.05: '*IDN?', 'SYSTem:ERRor?', 'SYSTem:STATus?'
and 'CHn:VOLTage?' answer, 'MEASure:VOLTage? CHn' does not. The output is switched only by
'OUTP CH1,OFF' sent WITHOUT a line terminator (the supply takes it after a short pause); with
'\n' it is rejected with '3  Command keywords were not recognized', and ':OUTPut CH1,OFF' is
accepted but ignored. Queries, on the other hand, need the '\n'.

    spd3303x.py <host> <channel> [--off <seconds>]

Exit status 0 if both switching commands were accepted (the error queue is empty after each).
"""
import argparse
import socket
import sys
import time

PORT : int = 5025

class Supply():
    """One connection to the supply"""
    def __init__(self, host : str, timeout : float = 3.0) -> None:
        self.sock = socket.create_connection((host, PORT), timeout=timeout)

    def send(self, command : str, terminator : str = "\n") -> None:
        """A command without an answer; the supply needs a moment before the next one"""
        self.sock.sendall((command + terminator).encode())
        time.sleep(0.5)

    def query(self, command : str) -> str:
        """A command with an answer, which ends with a newline"""
        self.send(command)
        data = b""
        while not data.endswith(b"\n"):
            chunk = self.sock.recv(1024)
            if not chunk:
                break
            data += chunk
        return data.decode(errors="replace").strip()

    def error(self) -> str:
        """The next entry of the error queue; '0  No Error' when there is none"""
        return self.query("SYSTem:ERRor?")

    def close(self) -> None:
        """End the connection"""
        self.sock.close()

def main() -> int:
    """Switch the channel off and on again"""
    parser = argparse.ArgumentParser(description="Power-cycle one output of a Siglent SPD3303X")
    parser.add_argument("host", help="network name or address of the supply")
    parser.add_argument("channel", type=int, choices=[1, 2], help="output channel")
    parser.add_argument("--off", type=float, default=1.0, help="seconds the output stays off (default 1)")
    args = parser.parse_args()
    supply = Supply(args.host)
    try:
        for state in ("OFF", "ON"):
            supply.send("OUTP CH{},{}".format(args.channel, state), terminator="")
            error = supply.error()
            if not error.startswith("0"):
                print("Switching CH{} {} failed: {}".format(args.channel, state, error), file=sys.stderr)
                return 1
            if state == "OFF":
                time.sleep(args.off)
    finally:
        supply.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
