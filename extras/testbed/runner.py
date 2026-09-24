#!/usr/bin/env python3
"""
Test runner for the PyAvrOCD testbed.

The runner watches a shared folder for job files, executes the requested action on
this machine and writes the output back into the shared folder. It only executes
actions from the repertoire below; a job file selects an action and its parameters,
it never carries a command line.

Standard library only, so that it runs on a Raspberry Pi, on a Linux box and under
Windows without installing anything.

Usage:
    python3 runner.py --config runner.json
    python3 runner.py --config runner.json --once     # one pass, then exit
"""

import argparse
import json
import os
import platform
import signal
import socket
import subprocess
import sys
import tempfile
import threading
from datetime import datetime, timezone

POLL_SECONDS = 2
HEARTBEAT_SECONDS = 10

INFO_SCRIPT = (
    "import platform, shutil, sys;"
    "print('platform:', platform.platform());"
    "print('python  :', sys.version.split()[0]);"
    "print('avr-gdb :', shutil.which('avr-gdb'));"
    "print('avrdude :', shutil.which('avrdude'));"
    "print('git     :', shutil.which('git'))"
)


def now() -> str:
    """Timestamp in UTC, seconds resolution."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_json(path: str, data: dict) -> None:
    """Write a JSON file atomically, so that a reader never sees half a file."""
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    handle, tmp = tempfile.mkstemp(dir=directory, suffix=".tmp")
    with os.fdopen(handle, "w", encoding="utf-8") as out:
        json.dump(data, out, indent=1)
    os.replace(tmp, path)


def read_json(path: str) -> dict:
    """Read a JSON file, returning an empty dict when it cannot be read."""
    try:
        with open(path, encoding="utf-8") as src:
            return json.load(src)
    except (OSError, ValueError):
        return {}


# --------------------------------------------------------------------------- #
# The repertoire. Every action returns a list of commands and the directory they
# run in. Parameters become separate arguments, never a shell string.
# --------------------------------------------------------------------------- #

def act_info(cfg: dict, params: dict) -> tuple:
    """Report what this machine is and which tools it has."""
    del params
    return ([[cfg["python"], "-c", INFO_SCRIPT],
             ["git", "log", "--oneline", "-1"]], cfg["repo"])


def act_pytest(cfg: dict, params: dict) -> tuple:
    """Run the unit test suite."""
    del params
    return ([cfg["run"] + [cfg["python"], "-m", "pytest", "-q", "-p", "no:cacheprovider"]],
            cfg["repo"])


def act_lint(cfg: dict, params: dict) -> tuple:
    """Run pylint over package and tests."""
    del params
    return ([cfg["run"] + [cfg["python"], "-m", "pylint", "-rn", "-sn",
                           "--disable=similarities,import-error", "pyavrocd", "tests"]],
            cfg["repo"])


def act_typecheck(cfg: dict, params: dict) -> tuple:
    """Run mypy over the package."""
    del params
    return ([cfg["run"] + [cfg["python"], "-m", "mypy", "pyavrocd"]], cfg["repo"])


def act_e2e(cfg: dict, params: dict) -> tuple:
    """
    Run end-to-end tests against real hardware. The runner starts and stops the GDB
    server around the test (see run_job). The e2e framework uses pexpect, so this
    action is not available under Windows.
    """
    cmd = cfg["run"] + [cfg["python"], "rune2e.py", "-d", str(params["device"])]
    for test in params.get("tests", []):
        cmd += ["-t", str(test)]
    if params.get("clock") is not None:
        cmd += ["-c", str(params["clock"])]
    if params.get("spec"):
        cmd += ["-s", str(params["spec"])]
    return ([cmd], os.path.join(cfg["repo"], "tests", "end-to-end"))


def act_checkout(cfg: dict, params: dict) -> tuple:
    """Fetch and check out a revision, so that a job can name what it wants tested."""
    rev = str(params["rev"])
    return ([["git", "fetch", "--all", "--quiet"],
             ["git", "-c", "advice.detachedHead=false", "checkout", "--quiet", rev],
             ["git", "log", "--oneline", "-1"]], cfg["repo"])


ACTIONS = {"info": act_info, "pytest": act_pytest, "lint": act_lint,
           "typecheck": act_typecheck, "e2e": act_e2e, "checkout": act_checkout}


# --------------------------------------------------------------------------- #

class Runner:
    """Polls the shared folder and executes one job at a time."""

    def __init__(self, cfg: dict) -> None:
        self.cfg = cfg
        self.host = cfg["host"]
        self.shared = cfg["shared"]
        self.state = "idle"
        self.current = None
        self.stop = threading.Event()
        for path in (os.path.join(self.shared, "jobs", self.host),
                     os.path.join(self.shared, "taken", self.host),
                     os.path.join(self.shared, "results", self.host),
                     os.path.join(self.shared, "hosts")):
            os.makedirs(path, exist_ok=True)

    # -- bookkeeping -------------------------------------------------------- #

    def heartbeat(self) -> None:
        """Announce that this runner is alive, so that a missing machine is visible."""
        while not self.stop.is_set():
            write_json(os.path.join(self.shared, "hosts", self.host + ".json"),
                       {"host": self.host, "state": self.state, "job": self.current,
                        "time": now(), "platform": platform.platform(),
                        "python": sys.version.split()[0], "node": socket.gethostname(),
                        "actions": sorted(self.cfg.get("actions", list(ACTIONS)))})
            self.stop.wait(HEARTBEAT_SECONDS)

    def claim(self, path: str) -> str:
        """Move a job file out of the inbox. The rename decides who got it."""
        target = os.path.join(self.shared, "taken", self.host, os.path.basename(path))
        try:
            os.replace(path, target)
            return target
        except OSError:
            return ""

    # -- execution ---------------------------------------------------------- #

    def start_server(self):
        """Start the GDB server the e2e tests connect to."""
        where = os.path.join(self.cfg["repo"], "tests", "end-to-end")
        return subprocess.Popen(["bash", os.path.join(where, "serv.sh"), "info"], cwd=where,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    @staticmethod
    def stop_server(handle) -> None:
        """Stop the GDB server again."""
        if handle is None:
            return
        handle.terminate()
        try:
            handle.wait(timeout=10)
        except subprocess.TimeoutExpired:
            handle.kill()

    def run_job(self, job: dict, logpath: str) -> dict:
        """Execute one job, streaming the output of every command into the log file."""
        action = job.get("action", "")
        allowed = self.cfg.get("actions", list(ACTIONS))
        if action not in ACTIONS or action not in allowed:
            return {"status": "rejected", "exit_code": None,
                    "message": f"action '{action}' is not available on this host"}
        try:
            commands, cwd = ACTIONS[action](self.cfg, job.get("params", {}))
        except KeyError as err:
            return {"status": "rejected", "exit_code": None,
                    "message": f"parameter {err} is missing for action '{action}'"}

        timeout = int(job.get("timeout", 900))
        server = self.start_server() if action == "e2e" else None
        started, code, status = now(), None, "ok"
        os.makedirs(os.path.dirname(logpath), exist_ok=True)
        try:
            with open(logpath, "w", encoding="utf-8", errors="replace") as log:
                for command in commands:
                    log.write(f"$ {' '.join(command)}\n  (in {cwd})\n\n")
                    log.flush()
                    proc = subprocess.Popen(command, cwd=cwd, stdout=log,
                                            stderr=subprocess.STDOUT)
                    try:
                        code = proc.wait(timeout=timeout)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                        code, status = None, "timeout"
                        break
                    log.write(f"\n[exit {code}]\n\n")
                    if code != 0:
                        status = "failed"
                        break
        except (OSError, ValueError) as err:
            code, status = None, "error"
            with open(logpath, "a", encoding="utf-8") as log:
                log.write(f"\nrunner error: {err}\n")
        finally:
            self.stop_server(server)
        return {"status": status, "exit_code": code, "started": started, "finished": now()}

    # -- main loop ---------------------------------------------------------- #

    def pass_once(self) -> int:
        """Look for jobs and execute what is there. Returns the number of jobs done."""
        inbox = os.path.join(self.shared, "jobs", self.host)
        os.makedirs(inbox, exist_ok=True)
        done = 0
        for name in sorted(os.listdir(inbox)):
            if not name.endswith(".json"):
                continue
            taken = self.claim(os.path.join(inbox, name))
            if not taken:
                continue
            job = read_json(taken)
            jobid = job.get("id") or os.path.splitext(name)[0]
            self.state, self.current = "busy", jobid
            outdir = os.path.join(self.shared, "results", self.host, jobid)
            result = self.run_job(job, os.path.join(outdir, "output.log"))
            result.update({"id": jobid, "host": self.host, "action": job.get("action"),
                           "params": job.get("params", {})})
            write_json(os.path.join(outdir, "result.json"), result)
            print(f"{now()}  {jobid}  {job.get('action')}  -> {result['status']}")
            self.state, self.current = "idle", None
            done += 1
        return done

    def loop(self) -> None:
        """Poll until interrupted."""
        print(f"runner '{self.host}' watching {self.shared}, actions: "
              f"{', '.join(sorted(self.cfg.get('actions', list(ACTIONS))))}")
        while not self.stop.is_set():
            try:
                if self.pass_once() == 0:
                    self.stop.wait(POLL_SECONDS)
            except OSError as err:               # shared folder unreachable for a moment
                print(f"{now()}  shared folder not reachable: {err}")
                self.stop.wait(POLL_SECONDS * 5)


def main() -> int:
    """Read the configuration and start polling."""
    parser = argparse.ArgumentParser(description="PyAvrOCD testbed runner")
    parser.add_argument("--config", default="runner.json", help="configuration file")
    parser.add_argument("--once", action="store_true", help="one pass, then exit")
    args = parser.parse_args()

    cfg = read_json(args.config)
    for key in ("host", "shared", "repo"):
        if key not in cfg:
            print(f"configuration is missing '{key}'")
            return 1
    cfg.setdefault("python", sys.executable)
    cfg.setdefault("run", [])              # e.g. ["poetry", "run"] where poetry is used
    if not os.path.isdir(cfg["repo"]):
        print(f"repository not found: {cfg['repo']}")
        return 1
    if not os.path.isdir(cfg["shared"]):
        print(f"shared folder not found: {cfg['shared']}")
        return 1

    runner = Runner(cfg)
    threading.Thread(target=runner.heartbeat, daemon=True).start()
    signal.signal(signal.SIGINT, lambda *_: runner.stop.set())
    if args.once:
        runner.pass_once()
    else:
        runner.loop()
    runner.stop.set()
    return 0


if __name__ == "__main__":
    sys.exit(main())
