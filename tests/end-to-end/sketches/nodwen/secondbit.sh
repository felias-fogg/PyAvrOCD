#!/bin/bash
F=`cat fuse.txt`
printf "0x%x" $(($F | 0x40)) > fuse.txt
