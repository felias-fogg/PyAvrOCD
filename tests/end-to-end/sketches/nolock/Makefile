TARGET = $(lastword $(subst /, ,$(CURDIR)))


$(TARGET).elf:
	touch $(TARGET).elf

all:	$(TARGET).elf

squeaky_clean:
	rm -f *.elf *.hex *.obj *.o *.d *.eep *.lst *.lss *.sym *.map *~ *.eeprom

lockup:
	avrdude -c $(PROG) -p $(MCU) -P $(PORT) -e -U lock:w:0x00:m

fresh:
	make squeaky_clean
	make all
	make lockup
