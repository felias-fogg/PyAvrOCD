# Notes about extending PyAvrOCD to UPDI

## Single stepping for ATmega808 - solved

Extremely fishy: When running Tictactoe on an ATmega808, it will single-step but then continue to the next breakpoint. Or it does double steps instead of single steps!

This all seems to have to do with the UPDI communication speed being **too low**. 400 kHz and below caused this problem, while everything above

## USER_ROW write leads to a timeout

After writing to USER_ROW, a 20 ms or 70 ms wait interval is necessary. Otherwise, we get a PDI timeout message from the debugger.

## EEPROM - solved

EEPROM access does not work - check!

The problem was that I had copied over the subtraction of the memory segment starting from the SRAM access in the avrdebugger module (without understanding it).  For JTAG and dw, it did not make a difference. However, for UPDI it makes a big difference. Here, we have to add it!

The big question is now, what does it mean for SRAM in the UPDI setting?

## Memory access API - solved

The memory access API does not seem to work in the way described in the document. Well, they do actually. However, when accessing memory, one has to add the MEMTYPE_address_byte, except when we access flash. Also, when accessing RAM, we usually do not want to add the offset, since we want to address everything starting at 0x0000 (but this is taken care of by subtracting the offset beforehand).

## General registers and I/O registers - solved

For UPDI targets, addressing of general registers and I/O registers is a bit different from that of JTAG/dw targets:

1. General registers are not addressable as SRAM locations DONE
2. I/O registers are addressed in the usual way in In/Out instructions. However, for ordinary LD/ST direct and indirect addressing, the -0x20 offset for I/O instructions does not apply! DONE

This means

- that in `_filter_unsafe_instruction` in `breakexec.py`, `SREGADDR` needs to be different and the -0x20 does not apply. DONE

- set SREGADDR according to device type DONE

- set IO_offset according to device type DONE

- Check for all places where we use SRAM reads/writes to read/write registers DONE

- We need to have special read/write register functions in xavrdebug, which will "buffer" reads and writes and in the background use register file_read and _write (just before execution/singlestepping starts) DONE

## Stack pointer check - solved

The lower end of the user SRAM (and therefore stack) for UPDI targets is much higher than that of JTAG/dw, i.e.,

- `_stack_pointer_legal` should test against a much higher address. Perhaps, we can just ignore it.

The check is done, but it is futil because the stack pointer cannot take on such low values!

## Shadow registers - solved

The role of shadow regs in the OCD area is not entirely clear! Do we have to write to them in order to change the regs? I believe not. But this needs to be tested. -> xedbg said: ignore the shadow!