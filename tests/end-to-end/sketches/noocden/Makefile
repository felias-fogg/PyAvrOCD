# Will only  be used for boards with autopc, i.e., the Xplained Mini boards
TARGET = $(lastword $(subst /, ,$(CURDIR)))


$(TARGET).elf:
	touch $(TARGET).elf

all:	$(TARGET).elf

squeaky_clean:
	rm -f *.elf *.hex *.obj *.o *.d *.eep *.lst *.lss *.sym *.map *~ *.eeprom

unprog_ocden:
	- avrdude -c $(PROG) -p $(MCU) -P $(PORT) -T "config ocden=ocd_disabled"

fresh:
	make squeaky_clean
	make all
	make unprog_ocden
