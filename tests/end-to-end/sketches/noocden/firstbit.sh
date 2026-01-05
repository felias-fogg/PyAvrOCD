#!/bin/bash
F=`cat fuse.txt`
printf "0x%x" $(($F | 0x80)) > fuse.txt
