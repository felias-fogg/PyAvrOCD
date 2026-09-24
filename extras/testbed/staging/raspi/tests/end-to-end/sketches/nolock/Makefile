# Which fuses this part has depends on its debug interface; rune2e passes DW in.
ifeq ($(filter yes no,$(DW)),)
$(error DW must be set to yes or no: this Makefile sets DWEN, which only debugWIRE parts have)
endif
ifeq ($(filter yes no,$(LOCK)),)
$(error LOCK must be set to yes or no: the mEDBG of an Xplained Mini cannot write lock bits)
endif

TARGET = $(lastword $(subst /, ,$(CURDIR)))


$(TARGET).elf:
	touch $(TARGET).elf

all:	$(TARGET).elf

squeaky_clean:
	rm -f *.elf *.hex *.obj *.o *.d *.eep *.lst *.lss *.sym *.map *~ *.eeprom

lockup:
	sleep 1
ifeq ($(DW),yes)
	python3 ../setfuse.py -- -c $(PROG) -p $(MCU) -P $(PORT) -e -T "config dwen=1"
endif
ifeq ($(LOCK),yes)
	python3 ../setfuse.py -- -c $(PROG) -p $(MCU) -P $(PORT) -e -U lock:w:0x00:m
else
	@echo "nolock: this debugger cannot write lock bits, the test will skip itself"
endif

fresh:
	make squeaky_clean
	make all
	make lockup
