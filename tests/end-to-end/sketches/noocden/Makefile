# JTAG parts only. The test: PyAvrOCD started with -m noocden refuses to program OCDEN.
TARGET = $(lastword $(subst /, ,$(CURDIR)))


$(TARGET).elf:
	touch $(TARGET).elf

all:	$(TARGET).elf

squeaky_clean:
	rm -f *.elf *.hex *.obj *.o *.d *.eep *.lst *.lss *.sym *.map *~ *.eeprom

# erase first: a part left locked by an earlier test (nolock) would not take the fuse
unprog_ocden:
	python3 ../setfuse.py -- -c "$(PROG)" -p "$(MCU)" -P "$(PORT)" -e -T "config ocden=ocd_disabled"

fresh:
	make squeaky_clean
	make all
	make unprog_ocden
