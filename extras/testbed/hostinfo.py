#!/usr/bin/env python3
"""
What this machine is and what it has. Run by the testbed runner's 'info' action,
but useful on its own when setting a machine up.

Standard library only, like the rest of the testbed.
"""

import importlib.util
import os
import platform
import shutil
import subprocess
import sys

TOOLS = ("avr-gdb", "avrdude", "arduino-cli", "git", "poetry", "pyavrocd")
MODULES = ("pyavrocd", "pymcuprog", "pyedbglib", "pexpect", "pytest", "pylint", "mypy")

# Not everything answers to --version: avrdude prints its banner when called
# without arguments, arduino-cli wants a subcommand.
VERSION_ARGS = {"avrdude": [], "arduino-cli": ["version"]}


def version_of(tool: str) -> str:
    """What the tool says about itself, or why that did not work."""
    try:
        done = subprocess.run([tool] + VERSION_ARGS.get(tool, ["--version"]),
                              capture_output=True, text=True, timeout=30, check=False)
    except (OSError, subprocess.SubprocessError) as err:
        return f"({err})"
    out = (done.stdout + done.stderr).strip().splitlines()
    for line in out:                       # avrdude buries it in its usage text
        if "ersion" in line:
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
            print(f"{tool:<12} {version_of(tool)}")
            print(f"{'':<12} {where}")
    print()
    missing = [m for m in MODULES if importlib.util.find_spec(m) is None]
    print("modules  :", ", ".join(MODULES))
    print("missing  :", ", ".join(missing) if missing else "none")


if __name__ == "__main__":
    main()
