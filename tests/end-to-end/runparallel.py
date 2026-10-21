#!/usr/bin/env python3
"""
Run the end-to-end tests on several boards at the same time, one debugger each.

    poetry run -- python runparallel.py <device>:<serial>[:<clock>] ... [-- <more rune2e options>]

    poetry run -- python runparallel.py attiny3227:000202 atmega324p:18184:16 -- -t live -t cblink

(The '--' after 'run' keeps poetry from taking --keep and the rune2e options for its own.)

<serial> is the serial number of the debugger, or its end (not its start: -u of rune2e
and pyavrocd both match the end). Every run gets a copy of
this folder of its own -- pyavrocd.options, log/ and the sketches' build output would
otherwise collide -- its own serv.sh and its own GDB port, counting up from 2000.

Boards that need a manual power-cycle (debugWIRE behind anything but an mEDBG) are
better run one at a time: they would all ask at once.

The server is the pyavrocd that serv.sh would start, through $PYAVROCD: the copies
live outside the repository, where 'poetry run' finds no project. Without $PYAVROCD,
the script asks poetry for the virtual environment of this repository.
"""
import argparse
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_PORT = 2000
SUMMARY = re.compile(r"(Successful runs|Compilations failed|Scripts failed|Failed compilations|"
                     r"Failed scripts):\s*(.*)")


def server_program() -> str:
    """The pyavrocd for serv.sh: $PYAVROCD, else the one in this repository's venv"""
    if os.environ.get("PYAVROCD"):
        return os.environ["PYAVROCD"]
    venv = subprocess.run(["poetry", "env", "info", "-p"], cwd=HERE, capture_output=True,
                          text=True, check=True).stdout.strip()
    program = os.path.join(venv, "Scripts" if os.name == "nt" else "bin", "pyavrocd")
    if not os.path.exists(program):
        sys.exit(f"no pyavrocd in {venv}; set PYAVROCD")
    return program


def copy_folder(target : str) -> None:
    """This folder without old logs, server options and Python caches"""
    shutil.copytree(HERE, target, ignore=shutil.ignore_patterns(
        "log", "pyavrocd.options", "pyavrocd.running", "__pycache__", "*~"))
    os.makedirs(os.path.join(target, "log"))


def start(board : str, port : int, workdir : str, server : str, extra : list [ str ]) -> dict:
    """Copy, start serv.sh and rune2e for one board; returns the run's bookkeeping"""
    parts = board.split(":")
    device, serial = parts[0], parts[1]
    copy = os.path.join(workdir, f"{device}-{port}")
    copy_folder(copy)
    env = dict(os.environ, PYAVROCD=server)
    serverlog = open(os.path.join(copy, "server.log"), "w", encoding="utf-8")  # pylint: disable=consider-using-with
    serv = subprocess.Popen(["bash", "./serv.sh", "info"], cwd=copy, env=env,  # pylint: disable=consider-using-with
                            stdout=serverlog, stderr=subprocess.STDOUT, start_new_session=True)
    time.sleep(1)
    cmd = [sys.executable, "-u", "rune2e.py", "-d", device, "-u", serial, "-P", str(port)]
    if len(parts) == 3:
        cmd += ["-c", parts[2]]
    runlog = open(os.path.join(copy, "run.log"), "w", encoding="utf-8")  # pylint: disable=consider-using-with
    run = subprocess.Popen(cmd + extra, cwd=copy, stdout=runlog,  # pylint: disable=consider-using-with
                           stderr=subprocess.STDOUT)
    print(f"started {device} on {serial}, port {port}: {copy}", flush=True)
    return {"board": board, "copy": copy, "serv": serv, "run": run, "logs": (serverlog, runlog)}


def stop(job : dict) -> None:
    """End serv.sh and its server, after the server has had time to clean up"""
    time.sleep(3)
    try:
        os.killpg(job["serv"].pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    job["serv"].wait()
    for log in job["logs"]:
        log.close()


def summary(job : dict) -> list [ str ]:
    """The lines of rune2e's summary"""
    with open(os.path.join(job["copy"], "run.log"), encoding="utf-8") as f:
        return [m.group(0) for m in map(SUMMARY.search, f) if m]


def main() -> int:
    """Start all runs, wait for them, print a summary per board"""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", maxsplit=1)[0])
    parser.add_argument("boards", nargs="+", help="<device>:<serial>[:<clock>]")
    parser.add_argument("--keep", action="store_true", help="keep the copies (they are kept on failure anyway)")
    # everything after '--' belongs to rune2e; split it off before argparse sees it
    argv = sys.argv[1:]
    cut = argv.index("--") if "--" in argv else len(argv)
    args, extra = parser.parse_args(argv[:cut]), argv[cut+1:]
    for board in args.boards: # all of them before anything is started
        if len(board.split(":")) not in (2, 3):
            parser.error(f"'{board}' is not <device>:<serial>[:<clock>]")
    server = server_program()
    workdir = tempfile.mkdtemp(prefix="e2e-parallel-")
    jobs : list [ dict ] = []
    failed = False
    try:
        for i, board in enumerate(args.boards):
            jobs.append(start(board, BASE_PORT + i, workdir, server, extra))
        for job in jobs:
            job["rc"] = job["run"].wait()
            failed = failed or job["rc"] != 0
    finally: # whatever happens, no serv.sh is left behind
        for job in jobs:
            if job["run"].poll() is None:
                job["run"].terminate()
            stop(job)
    print()
    for job in jobs:
        print(f"=== {job['board']}: {'OK' if job['rc'] == 0 else 'FAILED'} (exit {job['rc']})")
        for line in summary(job):
            print("   ", line)
    if failed or args.keep:
        print(f"\nlogs: {workdir}")
    else:
        shutil.rmtree(workdir)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
