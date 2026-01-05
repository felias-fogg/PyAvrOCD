# Will only  be used for the Xplained Mini boards
fresh:
ifeq ($(MCU),atmega168pb)
	avrdude -c xplainedmini -p $(MCU) -e -U efuse:r:fuse.txt:h
	./lastbit.sh
	avrdude -c xplainedmini -p $(MCU) -e -U efuse:w:fuse.txt:h
else
	avrdude -c xplainedmini -p $(MCU) -e -U hfuse:r:fuse.txt:h
	./lastbit.sh
	avrdude -c xplainedmini -p $(MCU) -e -U hfuse:w:fuse.txt:h
endif