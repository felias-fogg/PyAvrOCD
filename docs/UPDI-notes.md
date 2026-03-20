# Notes about extending PyAvrOCD to UPDI

## EEPROM

EEPROM access over the GDB memory interface is fixed.

The problem was an address translation mismatch between the GDB-facing
`Memory` layer and the UPDI NVM backend:

- GDB accesses EEPROM through the `0x81xxxx` memory segment and already
  passes an EEPROM-relative offset such as `0x0002`.
- The UPDI NVM provider expects exactly that relative offset and adds the
  physical EEPROM base address from the device description, for example
  `0x1400` on parts such as the ATtiny3217.
- The old implementation in `Memory.eeprom_read()` and
  `Memory.eeprom_write()` subtracted the EEPROM base once before calling the
  backend. For UPDI devices with a nonzero EEPROM base, this produced the
  wrong raw address.

The fix is to keep the EEPROM offset relative in the `Memory` layer and let
the transport-specific NVM implementation add the physical base exactly once.
Regression tests now cover this path with a real UPDI device definition
(`attiny3217`) so that nonzero EEPROM bases are exercised.

## Memory access API

Memory access API does not seem to work in the way described in the document.

## General registers and I/O registers

For UPDI targets, addressing of general registers and I/O registers is a bit different from that of JTAG/dw targets:

1. General registers are not addressable as SRAM locations DONE
2. I/O registers are addressed in the usual way in In/Out instructions. However, for ordinary LD/ST direct and indirect addressing, the -0x20 offset for I/O instructions does not apply! DONE

This means

- that in `_filter_unsafe_instruction` in `breakexec.py`, `SREGADDR` needs to be different and the -0x20 does not apply. DONE

- set SREGADDR according to device type DONE

- set IO_offset according to device type DONE

- Check for all places where we use SRAM reads/writes to read/write registers DONE

- We need to have special read/write register functions in xavrdebug, which will "buffer" reads and writes and in the background use register file_read and _write (just before execution/singlestepping starts) DONE





The lower end of the user SRAM (and therefore stack) for UPDI targets is much higher than that of JTAG/dw, i.e.,

- `_stack_pointer_legal` should test against a much higher address. Perhaps, we can just ignore it.



The role of shadow regs in the OCD area is not entirely clear! Do we have to write to them in order to change the regs? I believe not. But this needs to be tested.
