#!/bin/bash
# Try to guess connected programmer/debugger
# First and only argument is debug interface (lower case)
if [[ -z "$1" ]]; then
    echo "First argument should be programming interface"
    exit 1
fi
LSUSB=$(lsusb)
if [[ "${LSUSB}" == *"03eb:2180"* ]]; then
    echo -n "snap_$1"
elif [[ "${LSUSB}" == *"03eb:2141"* ]]; then
    echo -n "atmelice_$1"
elif [[ "${LSUSB}" == *"03eb:2140"* ]]; then
    echo -n "jtag3$1"
elif [[ "${LSUSB}" == *"03eb:2144"* ]]; then
    echo -n "powerdebugger_$1"
elif [[ "${LSUSB}" == *"03eb:2111"* ]]; then
    echo -n "xplainedpro_$1"
elif [[ "${LSUSB}" == *"03eb:2145"* ]]; then
    echo -n "xplainedmini_$1"
elif [[ "${LSUSB}" == *"03eb:2175"* ]]; then
    echo -n "pkobn_$1"
elif [[ "${LSUSB}" == *"03eb:2177"* ]]; then
    echo -n "pickit4_$1"
elif [[ "$1" == "isp" ]]; then
    echo -n "arduino_as_isp"
else
    echo -n "unknown"
fi
    