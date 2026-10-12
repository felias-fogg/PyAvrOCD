#!/bin/bash
# Checks that everything is in place for a release.
#
# Until the i686 Linux client moved into the release workflow -- it is built
# there in a 32-bit Debian container on an ordinary x86_64 runner -- this script
# also built it: boot the Debian VM, build over ssh, copy the result back,
# commit it. None of that is needed any more. What remains are the checks that
# used to precede it.
if [[ "$(pwd)" != "/Users/nebel/GitHub/PyAvrOCD" ]]; then
    echo "Invoke the script only in the root folder of the repo!"
    exit 1
fi
if [[ -z "$1" ]] || [[ "$1" == "-h" ]] || [[ -n "$2" ]]; then
    echo "Usage: ./extras/prepare_release <release id>"
    exit 1
fi
echo "Checking everything for a release ..."
# First, because the check after it compares against origin/main and would be
# meaningless anywhere else: a release is cut from main, and a tag on another
# branch would ship whatever that branch happens to contain.
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
if [[ "$BRANCH" != "main" ]]; then
    echo "A release is built from main, but this is ${BRANCH}"
    echo "Merge into main first, then run the script there"
    exit 1
fi
if [[ -n $(git status -s -uno 2>/dev/null) ]]; then
    echo "Please commit changes first"
    exit 1
fi
if [[ -n $(git log origin/main..HEAD 2>/dev/null) ]]; then
    echo "There are unpushed commits"
    exit 1
fi
poetry install -q --all-extras
VER=$(poetry run pyavrocd -V)
VERSTR=v${VER#*version }
if [[ "$VERSTR" != "$1" ]]; then
    echo "Used release id is not identical to version number of system"
    echo "System version: ${VERSTR}"
    exit 1
fi
echo "Version ${VERSTR} matches, nothing uncommitted, nothing unpushed."
echo "Now you can create a new release ..."
