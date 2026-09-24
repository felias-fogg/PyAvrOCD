#!/usr/bin/env python3
"""
Hand a job to a testbed runner and wait for the result.

    python3 submit.py --shared ~/testbed --host raspi --action pytest
    python3 submit.py --shared ~/testbed --host raspi --action e2e \
            --param device=atmega328p --param tests=basic,ioreg-classic

Standard library only, like the runner itself.
"""

import argparse
import json
import os
import sys
import tempfile
import time
from datetime import datetime

ACTIONS = ("info", "checkout", "pytest", "lint", "typecheck", "e2e")
LIST_PARAMS = ("tests",)


def parse_params(pairs: list) -> dict:
    """Turn --param key=value options into a parameter dictionary."""
    params = {}
    for pair in pairs:
        if "=" not in pair:
            raise SystemExit(f"--param needs key=value, got '{pair}'")
        key, value = pair.split("=", 1)
        params[key] = value.split(",") if key in LIST_PARAMS else value
    return params


def deposit(shared: str, host: str, job: dict) -> str:
    """Write the job into the inbox under a temporary name, then rename it in."""
    inbox = os.path.join(shared, "jobs", host)
    os.makedirs(inbox, exist_ok=True)
    handle, tmp = tempfile.mkstemp(dir=inbox, suffix=".tmp")
    with os.fdopen(handle, "w", encoding="utf-8") as out:
        json.dump(job, out, indent=1)
    final = os.path.join(inbox, job["id"] + ".json")
    os.replace(tmp, final)
    return final


def wait_for(path: str, timeout: int) -> dict:
    """Wait until the result file appears."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if os.path.exists(path):
            time.sleep(0.5)                       # let the writer finish the rename
            with open(path, encoding="utf-8") as src:
                return json.load(src)
        time.sleep(2)
    return {}


def main() -> int:
    """Read the options, deposit the job, report what came back."""
    parser = argparse.ArgumentParser(description="submit a testbed job")
    parser.add_argument("--shared", required=True, help="the shared folder")
    parser.add_argument("--host", required=True, help="which runner should do it")
    parser.add_argument("--action", required=True, choices=ACTIONS)
    parser.add_argument("--param", action="append", default=[], metavar="KEY=VALUE")
    parser.add_argument("--timeout", type=int, default=900, help="seconds, for the job")
    parser.add_argument("--wait", type=int, default=3600, help="seconds, for the result")
    parser.add_argument("--no-wait", action="store_true", help="deposit and return")
    args = parser.parse_args()

    shared = os.path.expanduser(args.shared)
    if not os.path.isdir(shared):
        print(f"shared folder not found: {shared}")
        return 1

    beat = os.path.join(shared, "hosts", args.host + ".json")
    if not os.path.exists(beat):
        print(f"note: no heartbeat for '{args.host}' yet — is its runner started?")

    jobid = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + args.action
    job = {"id": jobid, "action": args.action, "timeout": args.timeout,
           "params": parse_params(args.param)}
    deposit(shared, args.host, job)
    print(f"{jobid} -> {args.host}")
    if args.no_wait:
        return 0

    outdir = os.path.join(shared, "results", args.host, jobid)
    result = wait_for(os.path.join(outdir, "result.json"), args.wait)
    if not result:
        print(f"no result after {args.wait} s, look in {outdir}")
        return 1
    log = os.path.join(outdir, "output.log")
    if os.path.exists(log):
        with open(log, encoding="utf-8", errors="replace") as src:
            sys.stdout.write(src.read())
    print(f"\n{result['status']}  (exit {result.get('exit_code')})  {log}")
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
