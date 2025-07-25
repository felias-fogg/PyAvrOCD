#!/bin/bash
while :
do
    poetry run dw-gdbserver -d $1
    if [ $? -eq 1 ]
    then
	echo "Goodbye"
	exit 0
    fi
    sleep 1
done
