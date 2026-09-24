# Testbed

A small harness for running PyAvrOCD checks on more than one machine. The
development machine (a Mac) exports a folder; every test machine mounts it and
runs `runner.py` against it. Jobs are dropped into the folder as JSON files, the
runners pick them up, execute them and write log and result back.

There is no daemon, no server and no network protocol beyond the file share, and
`runner.py` uses nothing but the Python standard library. That is deliberate: the
Raspberry Pi and the Windows box should need a Python interpreter and a checkout,
nothing else.

## Layout of the shared folder

    testbed/
      jobs/<host>/<id>.json         inbox, one file per job
      taken/<host>/<id>.json        the runner moved it here when it started
      results/<host>/<id>/
        output.log                  everything the commands printed
        result.json                 status, exit code, timestamps
      hosts/<host>.json             heartbeat: alive, idle or busy, platform

`<host>` is the name in the runner's configuration, not the machine's hostname,
so two checkouts on one machine can act as two hosts.

The work happens on `v2`, so that is what the instructions below clone. Use the
`checkout` action to move a runner to a different revision afterwards.

## Actions

A job selects an action and its parameters. It never carries a command line, so a
runner can only ever do these six things:

| action      | what it does                                | parameters               |
|-------------|---------------------------------------------|--------------------------|
| `info`      | platform, Python version, tools found, HEAD  | –                        |
| `checkout`  | `git fetch`, then check out a revision       | `rev`, required          |
| `pytest`    | the unit test suite                          | –                        |
| `lint`      | pylint over `pyavrocd` and `tests`           | –                        |
| `typecheck` | mypy over `pyavrocd`                         | –                        |
| `e2e`       | `rune2e.py` against attached hardware        | `device`, `tests`, `clock`, `spec` |

For `e2e` the runner starts `serv.sh` before the test and stops it afterwards.
The e2e framework needs `pexpect`, which does not work under Windows — leave
`e2e` out of the `actions` list there.

Each host's configuration lists which of the six it offers; anything else comes
back as `rejected`.

## Setting it up

### On the Mac (the machine that hands out work)

1. Create the folder, e.g. `~/GitHub/DEBUG/testbed`. Keeping it inside a folder
   that is already shared with Claude means no further permissions are needed.
2. System Settings → General → Sharing → File Sharing: add that folder, make sure
   SMB is enabled for your user.
3. Note the machine's name (`Sharing → Local hostname`, e.g. `macbook.local`).

### On a Linux machine or a Raspberry Pi

    sudo apt update && sudo apt install cifs-utils git python3-venv
    mkdir -p ~/testbed
    sudo mount -t cifs //macbook.local/testbed ~/testbed \
         -o username=nebel,uid=$(id -u),gid=$(id -g),vers=3.0
    git clone -b v2 https://github.com/felias-fogg/PyAvrOCD.git ~/GitHub/PyAvrOCD
    cd ~/GitHub/PyAvrOCD && python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'
    cp extras/testbed/runner.example.json ~/runner.json    # adjust the paths
    python3 extras/testbed/runner.py --config ~/runner.json

Add the mount to `/etc/fstab` if it should survive a reboot. For hardware tests
the usual udev rule for the debugger and membership in `dialout` are needed.

### On Windows

Map the share to a drive letter (`net use Z: \\macbook.local\testbed`), clone the
branch under test (`git clone -b v2 ...`), create a virtual environment, then:

    python extras\testbed\runner.py --config runner.json

`runner.windows.json` is a starting point. Note the doubled backslashes — JSON
needs them.

## Handing out work

A job is a JSON file in `jobs/<host>/`:

    {"id": "0042-pytest", "action": "pytest", "timeout": 1200}

    {"id": "0043-e2e", "action": "e2e", "timeout": 3600,
     "params": {"device": "atmega328p", "tests": ["basic", "ioreg-classic"]}}

Write it under a temporary name and rename it into place, so that a runner never
reads a half-written file. `submit.py` does that, waits for the result and prints
the log:

    python3 extras/testbed/submit.py --shared ~/GitHub/DEBUG/testbed \
            --host raspi --action pytest

Old jobs stay in `taken/` and `results/`; clean them out when they get in the way.

## What this is not

The share is a trust boundary, not a security boundary: anyone who can write into
it can make the runners check out a revision and run the test suite. That is fine
on a private network and nowhere else. A runner does one job at a time and does
not queue across restarts — a job that was claimed when the runner died stays in
`taken/` and has to be moved back by hand.

## Note: e2e under Windows

The e2e framework uses `pexpect.spawn`, which needs a pty and therefore does not
run under Windows. That is a limitation worth removing at some point, because the
USB/HID layer is exactly what can behave differently there, and the unit tests say
nothing about it.

What it would take: `pexpect.popen_spawn.PopenSpawn` works under Windows and has
the same API, using pipes instead of a pty (gdb flushes its `(gdb)` prompt into a
pipe, so the expect patterns still work). Then `child.close()` needs a wrapper
around `kill()`/`wait()`, `pexpect.run` in `run_compile_command` becomes
`subprocess.run`, and `serv.sh` needs a portable `serv.py`. The one hard part is
`child.sendcontrol('C')`: without a pty there is no line discipline, so writing
0x03 into the pipe raises no SIGINT. The way out is to signal the process group
instead — SIGINT on Linux and macOS, `CREATE_NEW_PROCESS_GROUP` plus
`CTRL_BREAK_EVENT` on Windows.

Not done, because switching the Unix path from pty to pipes puts tests at risk
that currently work.
