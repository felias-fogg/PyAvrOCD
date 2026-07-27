#!/bin/bash
DEFAULT_SERVER=fattrixie
if [[ "$(pwd)" != "/Users/nebel/GitHub/PyAvrOCD" ]]; then
    echo "Invoke the script only in the root folder of the repo!"
    exit 1
fi
if [[ -z "$1" ]] || [[ "$1" == "-h" ]] || [[ -n "$3" ]]; then
    echo "Usage: ./extra/prepare_release <release id> [ <server> ]"
    exit 1
fi
echo "Preparing everything for a release ..."
if [[ -n "$2" ]]; then
    SERVER=$2
else
    SERVER=$DEFAULT_SERVER
fi

if [[ -n $(git status -s -uno 2>/dev/null) ]]; then
    echo "Please commit changes first"
    exit 1
fi
if [[ -n $(git log origin/main..HEAD 2>/dev/null) ]]; then
    echo "There are unpushed commits"
    exit 1
fi
poetry install -q
VER=$(poetry run pyavrocd -V)
VERSTR=v${VER#*version }
if [[ "$VERSTR" != "$1" ]]; then
    echo "Used release id is not identical to version number of system"
    echo "System version: ${VERSTR}"
    exit 1
fi
echo "Trying to reach server ${SERVER} ..."
if ping -c 3 ${SERVER} &>/dev/null; then
    echo "... ${SERVER} is reachable"
else
    echo "${SERVER} is not reachable"
    exit 1
fi

echo "Updating repo on server ..."
ssh ${SERVER} "cd GitHub/PyAvrOCD; git pull"
if [[ $? != 0 ]]; then
    exit 1
fi

echo "Setting up virtual environment ..."
ssh ${SERVER} "cd GitHub/PyAvrOCD; python -m venv env; env/bin/python -m pip install --upgrade pip"
if [[ $? != 0 ]]; then
    exit 1
fi

echo "Installing everything ..."
ssh ${SERVER} "cd GitHub/PyAvrOCD; env/bin/pip install ."
if [[ $? != 0 ]]; then
    exit 1
fi

echo "Cleaning build directories ..."
ssh ${SERVER} "cd GitHub/PyAvrOCD; rm -rf dist build"
if [[ $? != 0 ]]; then
    exit 1
fi

echo "Running pyinstaller ..."
ssh ${SERVER} "cd GitHub/PyAvrOCD; env/bin/pyinstaller -y pyavrocd.spec"
if [[ $? != 0 ]]; then
    exit 1
fi

echo "Test run ..."
ssh ${SERVER} "cd GitHub/PyAvrOCD; ./dist/pyavrocd/pyavocd -V"
if [[ $? != 0 ]]; then
    exit 1
fi

echo "Remove old version ..."
rm -rf extras/binaries/arm-linux-gnueabihf/pyavrocd*

echo "Download new version from server ..."
scp -r ${SERVER}:./GitHub/PyAvrOCD/dist/pyavrocd/* extras/binaries/arm-linux-gnueabihf/
if [[ $? != 0 ]]; then
    exit 1
fi

echo "Add VERSION file ..."
echo -n "${VERSTR}" > extras/binaries/arm-linux-gnueabihf/VERSION

echo "Commit and upload to GitHub remote repo ..."
git add extras/binaries/arm-linux-gnueabihf/
git commit -m "New arm-linux-gnueabihf binaries ${VERSTR}"
git push

echo "Now you can create a new release ..."