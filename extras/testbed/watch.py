#!/usr/bin/env python3
"""
Watch the testbed: show which hosts are alive and follow the output of whatever
they are running, the way tail -f would if one knew the file name in advance.

    python3 watch.py --shared ~/GitHub/DEBUG/testbed
    python3 watch.py --shared ~/testbed --host raspi     # only that one

Stops with Ctrl-C. Standard library only, like the rest of the testbed.
"""

import argparse
import json
import os
import sys
import time

POLL_SECONDS = 1
STALE_SECONDS = 40


def read_json(path: str) -> dict:
    """Read a JSON file, returning an empty dict when it cannot be read."""
    try:
        with open(path, encoding="utf-8") as src:
            return json.load(src)
    except (OSError, ValueError):
        return {}


def age_of(path: str) -> float:
    """
    How long ago this host last wrote its heartbeat, by the age of the file rather
    than the time written inside it. Machines disagree about the time - a clock
    two hours out would otherwise look like a host that died two hours ago.
    """
    try:
        return max(0.0, time.time() - os.path.getmtime(path))
    except OSError:
        return 1e9


def hosts(shared: str, only: str) -> list:
    """Every host that has left a heartbeat, or just the one that was asked for."""
    folder = os.path.join(shared, "hosts")
    found = []
    for name in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        if not name.endswith(".json"):
            continue
        path = os.path.join(folder, name)
        beat = read_json(path)
        if beat and (only is None or beat.get("host") == only):
            beat["age"] = age_of(path)
            found.append(beat)
    return found


def follow(shared: str, host: str, job: str, out) -> bool:
    """
    Print whatever the log gains while the job runs. Returns once the result is
    there, or when the log stops existing.
    """
    outdir = os.path.join(shared, "results", host, job)
    logpath = os.path.join(outdir, "output.log")
    resultpath = os.path.join(outdir, "result.json")
    out.write(f"\n--- {host}: {job} ---\n")
    out.flush()
    position, waited = 0, 0.0
    while True:
        try:
            size = os.path.getsize(logpath)
            if size > position:
                with open(logpath, encoding="utf-8", errors="replace") as src:
                    src.seek(position)
                    out.write(src.read())
                    out.flush()
                    position = src.tell()
        except OSError:
            pass
        if os.path.exists(resultpath):
            time.sleep(0.5)                     # let the writer finish the rename
            result = read_json(resultpath)
            out.write(f"--- {job}: {result.get('status')} "
                      f"(exit {result.get('exit_code')}) ---\n\n")
            out.flush()
            return True
        waited += POLL_SECONDS
        if waited > 3600:
            return False
        time.sleep(POLL_SECONDS)


def main() -> int:
    """Wait for something to happen and show it as it happens."""
    parser = argparse.ArgumentParser(description="watch the testbed")
    parser.add_argument("--shared", required=True, help="the shared folder")
    parser.add_argument("--host", help="only this host")
    args = parser.parse_args()

    shared = os.path.expanduser(args.shared)
    if not os.path.isdir(shared):
        print(f"shared folder not found: {shared}")
        return 1

    print(f"watching {shared}, Ctrl-C to stop")
    seen: set = set()
    state: dict = {}
    while True:
        for beat in hosts(shared, args.host):
            host, job = beat.get("host"), beat.get("job")
            stale = beat["age"] > STALE_SECONDS
            was = state.get(host)
            now = "silent" if stale else (f"busy:{job}" if job else "idle")
            if was != now:
                if stale:
                    print(f"[{host}] no heartbeat for {int(beat['age'])} s")
                elif not job:
                    print(f"[{host}] idle "
                          f"({', '.join(beat.get('actions', []))})")
                state[host] = now
            if job and not stale and (host, job) not in seen:
                seen.add((host, job))
                follow(shared, host, job, sys.stdout)
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
