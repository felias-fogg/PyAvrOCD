#!/usr/bin/env python3
"""
What this machine is and what it has. Run by the testbed runner's 'info' action,
but useful on its own when setting a machine up.

Standard library only, like the rest of the testbed.
"""

import glob
import importlib.util
import os
import platform
import re
import shutil
import subprocess
import sys

try:
    import grp                                     # not available under Windows
except ImportError:
    grp = None

TOOLS = ("avr-gdb", "avrdude", "arduino-cli", "git", "poetry", "pyavrocd")
MODULES = ("pyavrocd", "pymcuprog", "pyedbglib", "pexpect", "pytest", "pylint", "mypy")

# Not everything answers to --version: avrdude prints its banner when called
# without arguments, arduino-cli wants a subcommand.
VERSION_ARGS = {"avrdude": [], "arduino-cli": ["version"]}

# The sketch Makefiles of nolock, nodwen, noocden and nobootrst set fuses with
# 'avrdude -T "config ..."', which arrived with avrdude 8.
AVRDUDE_MIN = (8, 0)


def too_old(reported: str) -> bool:
    """Whether the avrdude that said this is older than the fuse tests need."""
    found = re.search(r"version\s+(\d+)\.(\d+)", reported, re.IGNORECASE)
    return bool(found) and (int(found.group(1)), int(found.group(2))) < AVRDUDE_MIN


def version_of(tool: str) -> str:
    """What the tool says about itself, or why that did not work."""
    try:
        done = subprocess.run([tool] + VERSION_ARGS.get(tool, ["--version"]),
                              capture_output=True, text=True, timeout=30, check=False)
    except (OSError, subprocess.SubprocessError) as err:
        return f"({err})"
    out = (done.stdout + done.stderr).strip().splitlines()
    for line in out:                       # avrdude buries it in its usage text
        if re.search(r"\d+\.\d+", line):
            return line.strip()
    return out[0].strip() if out else "(said nothing)"


def main() -> None:
    """Print one block about the machine and one about what is installed."""
    print("platform :", platform.platform())
    print("python   :", sys.version.split()[0], "at", sys.executable)
    own = os.path.join(os.path.dirname(os.path.abspath(sys.executable)), "pyavrocd")
    print("pyavrocd :", version_of(own) if os.path.exists(own) else "NOT in this venv",
          "\n          ", own)
    print()
    print("on PATH, which is not necessarily what the runner uses:")
    for tool in TOOLS:
        where = shutil.which(tool)
        if where is None:
            print(f"{tool:<12} MISSING")
        else:
            reported = version_of(tool)
            note = "   <- older than 8.0, the fuse-setting tests need that" \
                   if tool == "avrdude" and too_old(reported) else ""
            print(f"{tool:<12} {reported}{note}")
            print(f"{'':<12} {where}")
    print()
    missing = [m for m in MODULES if importlib.util.find_spec(m) is None]
    print("modules  :", ", ".join(MODULES))
    print("missing  :", ", ".join(missing) if missing else "none")
    print()
    print("serial ports and the right to use them, which is what dw-link needs:")
    ports = sorted(glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
                   + glob.glob("/dev/cu.usb*"))
    print("  ports  :", ", ".join(ports) if ports else "none found")
    try:
        names = [] if grp is None else sorted(grp.getgrgid(gid).gr_name for gid in os.getgroups())
        print("  groups :", ", ".join(names))
        for needed in ("dialout", "uucp"):
            if needed in names:
                print(f"  member of {needed}")
    except (AttributeError, KeyError, OSError):    # no groups under Windows
        pass
    print()
    print("avrdude shipped with the installed cores, which is what uploads use:")
    found = sorted(glob.glob(os.path.join(
        os.path.expanduser("~"), ".arduino15", "packages", "*", "tools",
        "avrdude", "*", "bin", "avrdude")))
    for binary in found:
        print(f"  {version_of(binary)}")
        print(f"    {binary}")
    if not found:
        print("  none found under ~/.arduino15")


if __name__ == "__main__":
    main()
