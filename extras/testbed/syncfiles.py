#!/usr/bin/env python3
"""
Copy files from a staging directory into the repository, keeping their relative
paths. Run by the testbed runner's 'sync' action so that a change can be tried on
a machine without going through a commit and a push.

What this produces is a working tree that matches no revision. It is for trying
things out; a result that is meant to mean something comes from a 'checkout'.

Standard library only, like the rest of the testbed.
"""

import os
import shutil
import sys


def targets(staging: str, repo: str) -> list:
    """Pair every file under the staging directory with where it goes in the repo."""
    pairs = []
    for folder, _, files in os.walk(staging):
        for name in files:
            source = os.path.join(folder, name)
            relative = os.path.relpath(source, staging)
            destination = os.path.abspath(os.path.join(repo, relative))
            if os.path.commonpath([destination, repo]) != repo:
                print(f"refused, points outside the repository: {relative}")
                sys.exit(1)
            pairs.append((source, destination, relative))
    return pairs


def main() -> int:
    """Copy everything staged, saying what went where."""
    if len(sys.argv) != 3:
        print("usage: syncfiles.py <staging directory> <repository>")
        return 1
    staging, repo = sys.argv[1], os.path.abspath(sys.argv[2])
    if not os.path.isdir(staging):
        print(f"nothing staged: {staging} does not exist")
        return 0
    pairs = targets(staging, repo)
    if not pairs:
        print(f"nothing staged in {staging}")
        return 0
    for source, destination, relative in sorted(pairs, key=lambda p: p[2]):
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy2(source, destination)
        print(f"copied {relative}")
    print(f"{len(pairs)} file(s) copied into {repo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
