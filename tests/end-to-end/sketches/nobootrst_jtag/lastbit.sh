#!/bin/bash
F=`cat fuse.txt`
printf "0x%x" $(($F & ~1)) > fuse.txt
