#!/bin/bash
# Generate i686 Linux binary
DEFAULT_SERVER=macmini
if [[ "$(pwd)" != "/home/nebel/GitHub/PyAvrOCD" ]]; then
    echo "Invoke the script only in the root folder of the repo!"
    exit 1
fi
if [[ -z "$1" ]] || [[ "$1" == "-h" ]] || [[ -n "$3" ]]; then
    echo "Usage: ./extra/gen_i686_linux.sh <release id> [ <server> ]"
    exit 1
fi
if [[ $(uname -m) != "i686" ]]; then
    echo "Machine type is: $(uname -m)"
    echo "Should be: i686"
    exit 1
fi
if [[ $(uname -a | awk '{ print $2 }') != "bookworm" ]]; then
    echo "Distro is: $(uname -a | awk '{ print $2 }')"
    echo "Should be: bookworm"
fi

echo "Preparing everything for a creating release binary ..."
if [[ -n "$2" ]]; then
    SERVER=$2
else
    SERVER=$DEFAULT_SERVER
fi

echo "Install needed packages ..."
# you need to add the line
# nebel ALL=(ALL:ALL) NOPASSWD: ALL
# to /etc/sudoers in order to make the next
# lines work without asking for a password
sudo apt update -y
sudo apt upgrade -y
sudo apt install -y python3
sudo apt install -y python3-pip
sudo apt install -y python3.11-venv
sudo apt install -y git
sudo apt install -y scons

echo "Fetch updates from repo ..."
git pull

echo "Install PyAvrOCD ..."
python3 -m venv env
source ./env/bin/activate
python3 -m pip install --upgrade pip
pip install .
VER=$(pyavrocd -V)
VERSTR=v${VER#*version }
if [[ $VERSTR != $1 ]]; then
    echo "Wrong PyAvrOCD version number: $VERSTR"
    exit 1
fi

echo "Generate pyinstaller binary ..."
rm -rf dist
pyinstaller -y --clean pyavrocd.spec

echo "Transform into a 'statically linked' binary ..."
pip install patchelf-wrapper
pip install staticx
mv dist/pyavrocd dist/pyavrocd-dyn
staticx dist/pyavrocd-dyn dist/pyavrocd
rm dist/pyavrocd-dyn
mkdir -p dist/pyavrocd-util/svd
cp -r svd/*svd dist/pyavrocd-util/svd/

echo "Transfer to main development host ..."
ssh nebel@${SERVER} "rm -rf Github/PyAvrOCD/extras/binaries/i686-linux-gnu/pyavrocd-util"
scp -r dist/pyavrocd* nebel@${SERVER}:Github/PyAvrOCD/extras/binaries/i686-linux-gnu/
