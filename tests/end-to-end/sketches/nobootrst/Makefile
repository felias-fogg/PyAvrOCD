# Which fuses this part has depends on its debug interface; rune2e passes DW in.
ifeq ($(filter yes no,$(DW)),)
$(error DW must be set to yes or no: this Makefile sets DWEN, which only debugWIRE parts have)
endif

TARGET = $(lastword $(subst /, ,$(CURDIR)))


$(TARGET).elf:
	touch $(TARGET).elf

all:	$(TARGET).elf

squeaky_clean:
	rm -f *.elf *.hex *.obj *.o *.d *.eep *.lst *.lss *.sym *.map *~ *.eeprom

prog_bootrst:
	sleep 1
ifeq ($(DW),yes)
	python3 ../setfuse.py -- -c "$(PROG)" -p "$(MCU)" -P "$(PORT)" -e -T "config dwen=1"
endif
	python3 ../setfuse.py -- -c "$(PROG)" -p "$(MCU)" -P "$(PORT)" -T "config bootrst=boot_section"

fresh:
	make squeaky_clean
	make all
	make prog_bootrst
