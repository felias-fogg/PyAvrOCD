#!/usr/bin/env python3
"""
Run avrdude for the fuse setup of a test sketch, and fail when it did not work.

The Makefiles used to prefix these calls with '-', which let make swallow every
failure: a missing programmer, an avrdude too old for 'config', a target that
does not answer. The test then ran against fuses that were never changed and
measured something other than what it claimed to.

Usage:
    setfuse.py [--allow TEXT] -- <avrdude arguments>

Everything after '--' is handed to avrdude unchanged. A failure whose output
contains one of the --allow texts is reported but accepted, which is how a
recipe declares an outcome it knows about, for instance an ISP access that
cannot work any more because the part has just entered debugWIRE.

Standard library only, so it runs wherever the tests do.
"""

import re
import subprocess
import sys

MIN_VERSION = (8, 0)          # 'config <fuse>=<value>' in terminal mode


def version() -> tuple [ int, int ] | None:
    """Version of the avrdude on PATH, or None when there is none to ask."""
    try:
        done = subprocess.run(["avrdude"], capture_output=True, text=True,
                              timeout=30, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    found = re.search(r"version\s+(\d+)\.(\d+)", done.stdout + done.stderr, re.IGNORECASE)
    return (int(found.group(1)), int(found.group(2))) if found else None


def split_arguments(argv : list [ str ]) -> tuple [ list [ str ], list [ str ] ]:
    """Separate our own options from what goes to avrdude."""
    allowed : list [ str ] = [ ]
    rest = list(argv)
    while rest and rest[0] == "--allow":
        if len(rest) < 2:
            raise SystemExit("--allow needs a text")
        allowed.append(rest[1])
        rest = rest[2:]
    if not rest or rest[0] != "--":
        raise SystemExit("usage: setfuse.py [--allow TEXT] -- <avrdude arguments>")
    return allowed, rest[1:]


def main() -> int:
    """Check that avrdude can do the job, do it, and say so when it did not."""
    allowed, arguments = split_arguments(sys.argv[1:])
    if not arguments:
        raise SystemExit("no avrdude arguments given")

    installed = version()
    if installed is None:
        print("setfuse: no avrdude on PATH, cannot set up the fuses for this test",
              file=sys.stderr)
        return 1
    if "-T" in arguments and installed < MIN_VERSION:
        print(f"setfuse: avrdude {installed[0]}.{installed[1]} does not know "
              f"'-T \"config ...\"'; version {MIN_VERSION[0]}.{MIN_VERSION[1]} "
              "or later is needed to set these fuses", file=sys.stderr)
        return 1

    print("setfuse: avrdude " + " ".join(arguments), flush=True)
    done = subprocess.run(["avrdude"] + arguments, capture_output=True,
                          text=True, check=False)
    output = done.stdout + done.stderr
    sys.stdout.write(output)
    if done.returncode == 0:
        return 0
    for text in allowed:
        if text in output:
            print(f"setfuse: avrdude failed, accepted because of --allow '{text}'")
            return 0
    print(f"setfuse: avrdude exited with {done.returncode}, the fuses are not as "
          "the test needs them", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
