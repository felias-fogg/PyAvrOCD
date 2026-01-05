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
rm -f pyavrocd.options
while :
do
    while [ ! -f pyavrocd.options ]; do sleep 0.3; done
    sleep 0.2
    poetry run pyavrocd -m all -v $verb
    if [ $? -eq 1 ]
    then
	echo "Goodbye"
	exit 0
    fi
    sleep 1
done
