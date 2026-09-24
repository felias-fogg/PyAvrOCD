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

# A file the shared folder must contain. An unmounted mount point is an ordinary
# empty directory, and a runner started against one works away at nothing while
# looking perfectly healthy from its own side.
MARKER = ".testbed"



def readable(command: list) -> str:
    """
    A command as one line, with quotes where an argument contains a blank. The
    runner passes argument lists and never a command line, but a log that drops
    the quotes reads like something that would not work.
    """
    return " ".join(f'"{part}"' if " " in part else part for part in command)


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
    script = os.path.join(cfg["repo"], "extras", "testbed", "hostinfo.py")
    return ([[cfg["python"], script],
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
    if params.get("verbose"):
        cmd += ["-v", str(params["verbose"])]
    if params.get("baud"):
        cmd += ["-b", str(params["baud"])]
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


def act_cores(cfg: dict, params: dict) -> tuple:
    """
    Install or update an Arduino core. This is the one action that puts software on
    a host rather than only looking at it, which is why the core is named by the job
    and the list of what is installed afterwards ends up in the log.
    """
    extra = []
    for url in params.get("urls", []):
        extra += ["--additional-urls", str(url)]
    return ([["arduino-cli", "core", "update-index"] + extra,
             ["arduino-cli", "core", "install", str(params["core"])] + extra,
             ["arduino-cli", "core", "list"]], cfg["repo"])


def act_corebuild(cfg: dict, params: dict) -> tuple:
    """
    Compile an Arduino core for its boards and menu combinations, with the script
    that lives in the core. For a host whose 'repo' is a core rather than
    PyAvrOCD: measuring how long Windows takes needs a machine one can ask again
    without waiting twelve minutes for a CI run.
    """
    script = os.path.join(cfg["repo"], "extras", "compile_all.py")
    cmd = [cfg["python"], script, "--fqbn-prefix", str(params["prefix"])]
    for name in ("coverage", "menus", "work-dir"):
        if params.get(name):
            cmd += [f"--{name}", str(params[name])]
    if params.get("max-builds"):
        cmd += ["--max-builds", str(params["max-builds"])]
    if params.get("all-menus"):
        cmd += ["--all-menus"]
    return ([cmd], cfg["repo"])


def act_corehooks(cfg: dict, params: dict) -> tuple:
    """Check that the core's prebuild hook delivers the pragma flags."""
    script = os.path.join(cfg["repo"], "extras", "check_hooks.py")
    cmd = [cfg["python"], script, "--fqbn", str(params["fqbn"])]
    if params.get("work-dir"):
        cmd += ["--work-dir", str(params["work-dir"])]
    return ([cmd], cfg["repo"])


def act_sync(cfg: dict, params: dict) -> tuple:
    """
    Copy what has been staged for this host in the shared folder into the repository,
    so that a change can be tried without a commit and a push. The working tree then
    matches no revision, which is why the git status at the end is part of the output.
    """
    staging = os.path.join(cfg["shared"], "staging", cfg["host"])
    script = os.path.join(cfg["repo"], "extras", "testbed", "syncfiles.py")
    # 'restore' has to remove what an earlier sync left behind completely: files it
    # changed, and files it added, which would otherwise block the next checkout.
    # 'git clean -fd' leaves ignored files such as build output alone.
    commands = ([["git", "restore", "."], ["git", "clean", "-fd"]]
                if params.get("restore") else [])
    commands += [[cfg["python"], script, staging, cfg["repo"]],
                 ["git", "status", "--short"]]
    return (commands, cfg["repo"])


ACTIONS = {"info": act_info, "pytest": act_pytest, "lint": act_lint,
           "typecheck": act_typecheck, "e2e": act_e2e, "checkout": act_checkout,
           "sync": act_sync, "cores": act_cores,
           "corebuild": act_corebuild, "corehooks": act_corehooks}


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

    def server_env(self) -> dict:
        """
        Tell serv.sh which pyavrocd to start. Without this it falls back to poetry,
        which not every machine has.
        """
        env = os.environ.copy()
        server = self.cfg.get("server") or os.path.join(
            os.path.dirname(os.path.abspath(self.cfg["python"])), "pyavrocd")
        if os.path.exists(server):
            env["PYAVROCD"] = server
        return env

    def start_server(self, logpath: str):
        """Start the GDB server the e2e tests connect to, keeping its output."""
        where = os.path.join(self.cfg["repo"], "tests", "end-to-end")
        log = open(logpath, "w", encoding="utf-8", errors="replace")   # closed in stop_server
        proc = subprocess.Popen(["bash", os.path.join(where, "serv.sh"), "info"], cwd=where,
                                env=self.server_env(), stdout=log, stderr=subprocess.STDOUT)
        proc.logfile = log
        return proc

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
        if getattr(handle, "logfile", None):
            handle.logfile.close()

    def run_job(self, job: dict, logpath: str) -> dict:
        """Execute one job, streaming the output of every command into the log file."""
        def rejected(message: str) -> dict:
            """Say no, and leave the reason in the log as well as in the result."""
            os.makedirs(os.path.dirname(logpath), exist_ok=True)
            with open(logpath, "w", encoding="utf-8") as log:
                log.write(message + "\n")
            return {"status": "rejected", "exit_code": None, "message": message}

        action = job.get("action", "")
        allowed = self.cfg.get("actions", list(ACTIONS))
        if action not in ACTIONS:
            return rejected(f"action '{action}' does not exist")
        if action not in allowed:
            return rejected(f"action '{action}' is not in this host's actions list")
        try:
            commands, cwd = ACTIONS[action](self.cfg, job.get("params", {}))
        except KeyError as err:
            return rejected(f"parameter {err} is missing for action '{action}'")

        timeout = int(job.get("timeout", 900))
        outdir = os.path.dirname(logpath)
        os.makedirs(outdir, exist_ok=True)
        server = (self.start_server(os.path.join(outdir, "server.log"))
                  if action == "e2e" else None)
        started, code, status = now(), None, "ok"
        try:
            with open(logpath, "w", encoding="utf-8", errors="replace") as log:
                for command in commands:
                    log.write(f"$ {readable(command)}\n  (in {cwd})\n\n")
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
    if not os.path.exists(os.path.join(cfg["shared"], MARKER)):
        print(f"{cfg['shared']} does not contain '{MARKER}', so this is not the shared "
              "folder but most likely a mount point with nothing mounted on it")
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
