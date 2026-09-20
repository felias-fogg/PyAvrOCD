TARGET = $(lastword $(subst /, ,$(CURDIR)))


$(TARGET).elf:
	touch $(TARGET).elf

all:	$(TARGET).elf

squeaky_clean:
	rm -f *.elf *.hex *.obj *.o *.d *.eep *.lst *.lss *.sym *.map *~ *.eeprom

prog_bootrst:
	- sleep 1
	- avrdude -c $(PROG) -p $(MCU) -P $(PORT) -e -T "config dwen=1"
	- avrdude -c $(PROG) -p $(MCU) -P $(PORT) -T "config bootrst=boot_section"

fresh:
	make squeaky_clean
	make all
	make prog_bootrst
