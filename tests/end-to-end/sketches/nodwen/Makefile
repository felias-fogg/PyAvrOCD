# Will only  be used for boards with autopc, i.e., the Xplained Mini boards
fresh:
	avrdude -c xplainedmini -p $(MCU) -e -U hfuse:r:fuse.txt:h
	./secondbit.sh
	avrdude -c xplainedmini -p $(MCU) -e -U hfuse:w:fuse.txt:h
