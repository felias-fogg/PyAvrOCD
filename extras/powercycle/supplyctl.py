#!/usr/bin/env python3
"""
Gateway to the laboratory supply, run on the Raspberry Pi as an SSH forced command. The supply sits
on a private link of the Pi only, so the development machine cannot reach it except through this
program, and this program does nothing but:

    cycle <channel> [<seconds off>]     power-cycle an output
    on <channel>                        switch an output on
    off <channel>                       switch an output off
    status <channel>                    output state, setpoints, measured values

Before an output is switched on (also in 'cycle'), the setpoints are read and checked against the
ceilings in the configuration; above one, nothing is switched on. Setpoints are never changed.

The request comes in SSH_ORIGINAL_COMMAND (set by sshd for a forced command), or as arguments when
started by hand. The configuration is /etc/supplyctl.json, or the file named in SUPPLYCTL_CONFIG:

    {"host": "10.33.0.2", "max_volt": {"1": 12.0, "2": 12.0}, "max_curr": {"1": 0.25, "2": 0.25}}

A channel without a ceiling in the configuration cannot be switched on. Every request is logged to
syslog. Calls are serialised with a lock file, so that two of them never talk to the supply at once.
"""
import fcntl
import json
import os
import sys
import syslog
import time
from typing import Any, TYPE_CHECKING

# On the Pi both files lie in one directory; mypy, walking the repository, knows the module by
# its package path only
if TYPE_CHECKING:
    from extras.powercycle.spd3303x import Supply
else:
    from spd3303x import Supply

CONFIG : str = "/etc/supplyctl.json"
LOCK : str = "/tmp/supplyctl.lock"
MAX_OFF : float = 10.0          # seconds an output may stay off in 'cycle'
ACTIONS : tuple[str, ...] = ("cycle", "on", "off", "status")

class Refused(Exception):
    """The request is not allowed; nothing has been switched"""

def parse(words : list[str]) -> tuple[str, int, float]:
    """The request as (action, channel, seconds off); Refused for anything else"""
    if len(words) not in (2, 3) or words[0] not in ACTIONS:
        raise Refused("usage: cycle <channel> [<seconds>] | on <channel> | off <channel> | status <channel>")
    if words[1] not in ("1", "2"):
        raise Refused("channel must be 1 or 2")
    seconds = 1.0
    if len(words) == 3:
        if words[0] != "cycle":
            raise Refused("only 'cycle' takes a time")
        try:
            seconds = float(words[2])
        except ValueError:
            raise Refused("time must be a number of seconds") from None
        if not 0 < seconds <= MAX_OFF:
            raise Refused("time must be more than 0 and at most {} seconds".format(MAX_OFF))
    return words[0], int(words[1]), seconds

def check_setpoints(supply : Supply, config : dict[str, Any], channel : int) -> None:
    """Refused if a setpoint of the channel is above its ceiling, or the channel has none"""
    for quantity, key in (("VOLTage", "max_volt"), ("CURRent", "max_curr")):
        ceiling = config.get(key, {}).get(str(channel))
        if ceiling is None:
            raise Refused("no {} configured for CH{}".format(key, channel))
        value = float(supply.query("CH{}:{}?".format(channel, quantity)))
        if value > ceiling:
            raise Refused("CH{} {} setpoint {} is above the ceiling {}".format(channel, quantity.lower(),
                                                                                 value, ceiling))

def switch(supply : Supply, channel : int, state : str) -> None:
    """Switch the output; Refused if the supply does not accept it"""
    error = supply.switch(channel, state)
    if not error.startswith("0"):
        raise Refused("switching CH{} {} failed: {}".format(channel, state, error))

def execute(supply : Supply, config : dict[str, Any], action : str, channel : int, seconds : float) -> str:
    """Carry out a parsed request; the line to report"""
    if action == "status":
        return supply.status(channel)
    if action == "off":
        switch(supply, channel, "OFF")
        return "CH{} off".format(channel)
    check_setpoints(supply, config, channel)      # before anything is switched
    if action == "cycle":
        switch(supply, channel, "OFF")
        time.sleep(seconds)
    switch(supply, channel, "ON")
    return "CH{} {}".format(channel, "power-cycled" if action == "cycle" else "on")

def main() -> int:
    """Read the request, check it, carry it out under the lock"""
    request = os.environ.get("SSH_ORIGINAL_COMMAND")
    words = request.split() if request is not None else sys.argv[1:]
    syslog.openlog("supplyctl")
    syslog.syslog("request from {}: {}".format(os.environ.get("SSH_CLIENT", "local").split(" ")[0],
                                                " ".join(words)))
    try:
        action, channel, seconds = parse(words)
        with open(os.environ.get("SUPPLYCTL_CONFIG", CONFIG), encoding="utf-8") as file:
            config = json.load(file)
        with open(LOCK, "w", encoding="utf-8") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            supply = Supply(config["host"])
            try:
                result = execute(supply, config, action, channel, seconds)
            finally:
                supply.close()
    except Refused as e:
        syslog.syslog(syslog.LOG_WARNING, "refused: {}".format(e))
        print("refused: {}".format(e), file=sys.stderr)
        return 2
    except (OSError, ValueError, KeyError) as e:
        syslog.syslog(syslog.LOG_ERR, "failed: {}".format(e))
        print("failed: {}".format(e), file=sys.stderr)
        return 1
    syslog.syslog(result)
    print(result)
    return 0

if __name__ == "__main__":
    sys.exit(main())
