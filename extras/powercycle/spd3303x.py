#!/usr/bin/env python3
"""
Power-cycle, switch or read one output of a Siglent SPD3303X/SPD3303X-E laboratory supply over
the network. Only these fixed commands are sent: switching an output on and off, and reading the
status, the setpoints and the measured values. Nothing changes voltage or current limits; they
stay as they are set on the front panel.

The supply takes SCPI commands on a plain TCP socket, port 5025, without any VISA layer.
Measured with an SPD3303X, firmware 1.01.01.02.05: '*IDN?', 'SYSTem:ERRor?', 'SYSTem:STATus?'
and 'CHn:VOLTage?' answer with the '\n'. 'MEAS:VOLT? CHn', 'MEAS:CURR? CHn' answer only WITHOUT
a line terminator, as does the switching: 'OUTP CH1,OFF' is taken after a short pause; with '\n' it
is rejected with '3  Command keywords were not recognized', and ':OUTPut CH1,OFF' is accepted but
ignored. In 'SYSTem:STATus?', bit 4 is CH1 on, bit 5 CH2 on.

    spd3303x.py <host> <channel> [--off <seconds>]     power-cycle
    spd3303x.py <host> <channel> --set on|off          switch
    spd3303x.py <host> <channel> --status              state, setpoints, measured values

Exit status 0 if the switching commands were accepted (the error queue is empty after each).
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

    def send(self, command : str, terminator : str = "\n", pause : float = 0.5) -> None:
        """A command without an answer; the supply needs a moment before the next one"""
        self.sock.sendall((command + terminator).encode())
        time.sleep(pause)

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

    def measure(self, quantity : str, channel : int) -> str:
        """'VOLT' or 'CURR' as measured at the output; these queries answer only without a terminator"""
        self.send("MEAS:{}? CH{}".format(quantity, channel), terminator="", pause=0.5)
        data = b""
        while not data.endswith(b"\n"):
            chunk = self.sock.recv(1024)
            if not chunk:
                break
            data += chunk
        return data.decode(errors="replace").strip()

    def switch(self, channel : int, state : str) -> str:
        """Switch an output 'ON' or 'OFF'; the answer of the error queue ('0  No Error' if accepted)"""
        # without a terminator the supply takes the command only after a pause
        self.send("OUTP CH{},{}".format(channel, state), terminator="", pause=1.0)
        return self.error()

    def status(self, channel : int) -> str:
        """Output state, setpoints and measured values of one channel"""
        on = int(self.query("SYSTem:STATus?"), 16) & (0x10 << (channel - 1))
        return "CH{}: {}, set {} V / {} A, measured {} V / {} A".format(
            channel, "on" if on else "off",
            self.query("CH{}:VOLTage?".format(channel)), self.query("CH{}:CURRent?".format(channel)),
            self.measure("VOLT", channel), self.measure("CURR", channel))

    def error(self) -> str:
        """
        The next entry of the error queue; '0  No Error' when there is none. Asked once more if the
        answer does not come: once in an e2e run, the question right after an unterminated command
        was not answered.
        """
        try:
            return self.query("SYSTem:ERRor?")
        except TimeoutError:
            return self.query("SYSTem:ERRor?")

    def close(self) -> None:
        """End the connection"""
        self.sock.close()

def main() -> int:
    """Power-cycle the channel (default), switch it, or show its status"""
    parser = argparse.ArgumentParser(description="Power-cycle, switch or read one output of a Siglent SPD3303X")
    parser.add_argument("host", help="network name or address of the supply")
    parser.add_argument("channel", type=int, choices=[1, 2], help="output channel")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--off", type=float, default=1.0,
                            help="power-cycle: seconds the output stays off (default 1)")
    action.add_argument("--set", choices=["on", "off"], help="switch the output on or off")
    action.add_argument("--status", action="store_true", help="show state, setpoints and measured values")
    args = parser.parse_args()
    supply = Supply(args.host)
    try:
        if args.status:
            print(supply.status(args.channel))
            return 0
        for state in ([args.set.upper()] if args.set else ["OFF", "ON"]):
            error = supply.switch(args.channel, state)
            if not error.startswith("0"):
                print("Switching CH{} {} failed: {}".format(args.channel, state, error), file=sys.stderr)
                return 1
            if state == "OFF" and not args.set:
                time.sleep(args.off)
    finally:
        supply.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
