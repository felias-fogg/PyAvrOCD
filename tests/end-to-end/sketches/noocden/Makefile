# Only used for the Xplained Mini boards
TARGET = $(lastword $(subst /, ,$(CURDIR)))


$(TARGET).elf:
	touch $(TARGET).elf

all:	$(TARGET).elf

squeaky_clean:
	rm -f *.elf *.hex *.obj *.o *.d *.eep *.lst *.lss *.sym *.map *~ *.eeprom

unprog_ocden:
	python3 ../setfuse.py -- -c "$(PROG)" -p "$(MCU)" -P "$(PORT)" -T "config ocden=ocd_disabled"

fresh:
	make squeaky_clean
	make all
	make unprog_ocden
