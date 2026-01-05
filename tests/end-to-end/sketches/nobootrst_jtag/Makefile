# Will only  be used for JTAG targets
fresh:
	- avrdude -c atmelice_jtag -p $(MCU) -e -U hfuse:r:fuse.txt:h
	- avrdude -c jtag3 -p $(MCU) -e -U hfuse:r:fuse.txt:h
	- avrdude -c pickit4_jtag -p $(MCU) -e -U hfuse:r:fuse.txt:h
	- avrdude -c powerdebugger_jtag -p $(MCU) -e -U hfuse:r:fuse.txt:h
	- avrdude -c snap_jtag -p $(MCU) -e -U hfuse:r:fuse.txt:h
	- avrdude -c xplainedpro -p $(MCU) -e -U hfuse:r:fuse.txt:h
	./lastbit.sh
	- avrdude -c atmelice_jtag -p $(MCU) -e -U hfuse:w:fuse.txt:h
	- avrdude -c jtag3 -p $(MCU) -e -U hfuse:w:fuse.txt:h
	- avrdude -c pickit4_jtag -p $(MCU) -e -U hfuse:w:fuse.txt:h
	- avrdude -c powerdebugger_jtag -p $(MCU) -e -U hfuse:w:fuse.txt:h
	- avrdude -c snap_jtag -p $(MCU) -e -U hfuse:w:fuse.txt:h
	- avrdude -c xplainedpro -p $(MCU) -e -U hfuse:w:fuse.txt:h
