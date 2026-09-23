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

## Debugger writes to the 16-bit ADC registers lose the low byte - worked around

The 16-bit I/O registers are accessed through a TEMP register, and the data sheets are
explicit about the order (ATtiny3216/17, §8.5.6): on the modern MCUs the *low* byte has
to be written first, where it is stored in TEMP, and writing the high byte copies TEMP
into the low byte of the register in the same clock cycle.

That is how the CPU behaves. Writes coming from the debugger do not behave that way at
all, and the deviation is not uniform:

| access path                       | 16-bit registers in general            | ADC0.WINLT / ADC0.WINHT              |
|-----------------------------------|----------------------------------------|--------------------------------------|
| CPU (code running on the target)  | as documented: low byte first           | as documented: low byte first        |
| debugger, modern MCUs (UPDI)      | TEMP is bypassed, both orders work      | high byte first, or the low byte is lost |
| debugger, classic MCUs (dW, JTAG) | as documented: high byte first          | (no writable 16-bit ADC register)    |

So on the modern MCUs the debugger writes both bytes straight into the register - which
is what one wants from a debugger - except for the two ADC window comparator registers,
where writing the high byte additionally triggers the TEMP transfer and overwrites a low
byte written before it.

TEMP is an ordinary read/write register of the peripheral, so this can be measured rather
than inferred (`draft/temp_probe.py`, reading TEMP after every single byte write and the
16-bit register only at the very end, because reading its low byte latches the high byte
into TEMP):

- Writing a byte through the debugger never puts it into TEMP - TEMP stays 0x00
  throughout, for the ADC as well as for TCB0. The buffering half of the mechanism is
  switched off for this access path.
- Preloading TEMP with a marker value of 0xAA and then writing 0x34 and 0x12 in the
  documented order yields `ADC0.WINHT` = 0x12AA, but `TCB0.CCMP` = 0x1234. The high byte
  write therefore does transfer TEMP into the low byte on the ADC, and does not on TCB0.

The ADC access is thus half converted: the low byte is no longer buffered, while the
transfer triggered by the high byte still happens.

Measured on an ATtiny3217 (tinyAVR 1-series, nEDBG), an ATmega4809 and an ATmega4808
(megaAVR 0-series, mEDBG and Atmel-ICE), with pymcuprog alone, no GDB and no PyAvrOCD
involved (`draft/winht_repro.py`):

```
ADC0.WINHT   low first  -> 0x1200      <-- the low byte is gone
ADC0.WINHT   high first -> 0x1234
RTC.PER      low first  -> 0x1234
RTC.PER      high first -> 0x1234
USART0.BAUD  low first  -> 0x1234
USART0.BAUD  high first -> 0x1234
TCB0.CCMP    low first  -> 0x1234
TCB0.CCMP    high first -> 0x1234
```

Further observations:

- Three debuggers of different origin (nEDBG, mEDBG, Atmel-ICE) on three devices from
  two families behave identically, so it is not the firmware of one probe.
- PyAvrOCD and pymcuprog issue exactly one write command per byte, with no read in
  between (checked in the debug log of the GDB server), so nothing on our side reloads
  TEMP.
- Enabling the ADC (`ADC0.CTRLA.ENABLE`) makes no difference, so CLK_ADC is not involved.
- Only writing is affected; reading 16-bit ADC registers returns consistent values.
- A test program running on the target writes both `ADC0.WINHT` and `TCB0.CCMP`
  correctly in the documented order (`tests/end-to-end/sketches/adcwin`), so the
  peripheral itself is fine and ordinary application code is not affected.
- On an ATmega328P, all writable 16-bit registers follow the documented classic order,
  including the rarely written `EEPROM.EEAR` and `USART0.UBRR0`. The classic ADC has no
  writable 16-bit register at all: `ADC.ADC` is the read-only result register.

Neither the data sheets nor the errata documents (DS80000887 rev. C for the
ATtiny3216/17, DS80000886 for the ATtiny1614/16/17) mention any of this. It is plausible
that it has gone unnoticed because `ADC0.WINLT` and `ADC0.WINHT` are the only 16-bit ADC
registers that are ever written, and a debugger rarely writes them at all.

The workaround in `_sram_write16bitreg` in `monitor.py` is to write the bytes in the
order low, high, low, which is correct in every case above: the final write either
repeats a byte that is already in place or restores the low byte that the high byte
write has just destroyed. The e2e test `ioreg-modern` uses `ADC0.WINHT` and therefore
covers this case.
