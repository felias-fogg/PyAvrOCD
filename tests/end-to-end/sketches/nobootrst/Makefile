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

# The test: with BOOTRST programmed and the part locked, PyAvrOCD started with
# -m nobootrst clears the lock (lockbits are managed) but leaves BOOTRST alone.
# The erase comes first on every part, because a part left locked by an earlier
# test (nolock) would not take the fuse; the lock comes last, because a locked
# part would not take it either.
prog_bootrst:
	sleep 1
ifeq ($(DW),yes)
	python3 ../setfuse.py -- -c "$(PROG)" -p "$(MCU)" -P "$(PORT)" -e -T "config dwen=1"
else
	python3 ../setfuse.py -- -c "$(PROG)" -p "$(MCU)" -P "$(PORT)" -e
endif
	python3 ../setfuse.py -- -c "$(PROG)" -p "$(MCU)" -P "$(PORT)" -T "config bootrst=boot_section"
ifeq ($(LOCK),yes)
	python3 ../setfuse.py -- -c "$(PROG)" -p "$(MCU)" -P "$(PORT)" -U lock:w:0x00:m
else
	@echo "nobootrst: this debugger cannot write lock bits, only BOOTRST is checked"
endif

fresh:
	make squeaky_clean
	make all
	make prog_bootrst
