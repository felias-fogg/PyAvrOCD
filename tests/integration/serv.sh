#!/bin/bash
if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
   echo "usage: serv.sh <mcu> [<verbosity level>]"
   exit
fi
if [ "$#" -eq 2 ]; then
    verb=$2
else
    verb=info
fi
while :
do
    poetry run pyavrocd -m all -v $verb -d $1
    if [ $? -eq 1 ]
    then
	echo "Goodbye"
	exit 0
    fi
    sleep 1
done
