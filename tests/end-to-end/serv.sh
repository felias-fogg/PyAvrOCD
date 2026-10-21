#!/bin/bash
if [ "$#" -gt 1 ]; then
    echo "usage: serv.sh [<verbosity level>]"
    echo "call always in 'end-to-end' folder"
    exit
fi
if [ "$#" -eq 1 ]; then
    verb=$1
else
    verb=info
fi
# Start the server through poetry when it is there, so that the working tree is
# used. PYAVROCD overrides that, which is how a testbed runner points the script
# at the pyavrocd of its own virtual environment on a machine without poetry.
if [ -n "$PYAVROCD" ]; then
    server=("$PYAVROCD")          # an array, so that a path with a blank survives
elif command -v poetry > /dev/null 2>&1; then
    server=(poetry run pyavrocd)
else
    server=(pyavrocd)
fi

rm -f pyavrocd.options pyavrocd.running
while :
do
    while [ ! -f pyavrocd.options ]; do sleep 0.3; done
    sleep 0.2
    # pyavrocd.running exists while the server runs: rune2e waits for it to go before
    # the next test calls avrdude, which cannot open a probe the server still holds
    touch pyavrocd.running
    "${server[@]}" -m all -v "$verb"
    rc=$?
    rm -f pyavrocd.running
    if [ $rc -eq 1 ]
    then
	echo "Goodbye"
	exit 0
    fi
    sleep 1
done
