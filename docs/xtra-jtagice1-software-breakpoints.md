# How to Implement Software Breakpoints for the JTAGICE mkI

The `Jtag1Backend` offers hardware breakpoints only (`SwbpSupport.NONE`). This note records what was measured on 2026-11-17 and how software breakpoints could be implemented on top of it. Nothing of this has been implemented yet.

## What was measured

Two clones were used, both with the same ATmega32 target:

- an Olimex-style clone with an FTDI chip, HW version 0xCE, SW version 0x80;
- a clone with a CH340 chip, HW version 0xC0, SW version 0x80.

Both behaved identically in everything below.

### Erasing a flash page

`Cmd_ERASEPAGE_SPM` (0xA1) works in debug mode. The address is the **word address of the page in three bytes, MSB first**: the page at byte address 0x6000 is erased by `A1 00 30 00` followed by EOP. Each erase takes 25–32 ms.

The probe seems to ignore the first of the three bytes. `A1 60 00 00` therefore erases page 0. That is how the program on an ATmega16 lost its first page in an earlier test.

`Jtag1Protocol.erase_page_spm` currently sends the byte address in two bytes plus a zero byte. This has to be changed to `(address // 2).to_bytes(3, 'big')`.

### Writing flash

Writing memory type 0xA0 (PML) works only for **complete pages**. A write of a few words is acknowledged but changes nothing. So planting a BREAK means: read the page, change the word, erase the page, write the whole page.

### Executing an instruction instead of the BREAK (IReg)

AVR060 describes the parameters IReg High/Low (0x81/0x82) for this purpose: the original instruction is put into the instruction register instead of the BREAK, so the flash is not touched.

The following was measured:

1. **When IReg is used.** The probe uses IReg only if the last thing the CPU did was execute the BREAK, either by hitting it during a go or by a single step onto it. **Any memory access in between** (reading registers, SRAM, I/O or flash; any write; setting PSB0/1 through memory type 0x60) makes the probe ignore IReg. The CPU then executes the BREAK again and stops at the same address. Reading the PC and getting or setting parameters do no harm.

2. **Re-arming.** A single step at the BREAK, without IReg, executes the BREAK again. The PC stays where it is, and no break message is sent. After that, IReg works again. This also works when the PC has only been written to the address of the BREAK, without a hit.

3. **Byte order.** IReg High (0x81) takes the *low* byte of the opcode, IReg Low (0x82) the high byte, i.e., the order in flash. In the order AVR060 suggests, a different instruction is executed.

4. **A single step executes one instruction too many.** With IReg, a single step executes the IReg instruction and then the following instruction from flash, which has already been fetched. This does not happen:
    - after a jump, a taken branch or a skip (the fetched word is discarded, and the step is exact);
    - when the following instruction is a BREAK (the CPU stops after the IReg instruction).

    A hardware breakpoint on the following address does not catch the extra instruction either.

5. **Two-word instructions.** If the BREAK replaces the first word of `lds`, the second word is taken from flash, and the instruction works correctly.

6. **`rcall`.** The jump target is correct, but the return address pushed onto the stack is the address of the BREAK instead of the next word. `icall` has not been measured, but probably behaves the same way.

7. **Go.** Re-arming, setting IReg and then go executes the program correctly from the breakpoint onwards. The only exception is `rcall` (see 6).

## How it could be implemented

The backend would get `SwbpSupport.SERVER`, so that the generic code in `backend.py` plants the BREAKs page by page, with `program_flash_page` doing erase plus full-page write. All of the special cases below apply to the `Jtag1Backend` only.

### Continuing from a breakpoint

When GDB continues from a breakpoint, it removes the breakpoint, single-steps, inserts the breakpoint again and continues (`z0`, `s`, `Z0`, `c`). The server keeps the BREAK in flash in this situation and executes the original instruction by injection. On the mkI, an injection means: re-arm by a single step, set IReg (low byte first), then step or go.

If this single step executes two instructions instead of one, nothing is lost, because GDB continues anyway. Two cases need care:

- **`rcall`/`icall` at the breakpoint.** Inject it by a single step, which is exact for these, then write the correct return address (breakpoint address + 1) into the two stack bytes at SP+1 (high byte) and SP+2 (low byte). Alternatively, simulate the instruction completely (push the return address, set the PC). `call` and `jmp` are two-word instructions, which `breakexec` simulates anyway.
- **A hardware breakpoint on the address right after a software breakpoint** is passed over. When the server chooses the kind of breakpoint, it can avoid this combination: a software breakpoint at the following address works, because the fetched BREAK stops the CPU. For a breakpoint set with `hbreak`, the step has to be done exactly instead (see below).

### Single-stepping from a breakpoint

A `stepi` at a breakpoint reaches the server as the same `s` packet as the step that is part of continuing. For instructions that jump, branch or skip, the injected step is exact. For all other instructions, one instruction too many would be executed.

An exact step can be done in one of two ways:

- put the original instruction back into flash for this one step (two erase/write cycles);
- simulate the instruction in the server.

Doing either on every continue from a breakpoint would cost the flash wear or the code that injection is meant to avoid. A way out is to **defer the step**:

1. On `s` at a breakpoint whose instruction is sequential, execute nothing yet. Answer with a stop at PC+1 and remember the pending step.
2. If GDB's next packets are `Z0` and `c` (the step was part of continuing), re-arm, set IReg and go.
3. On any other packet, first carry out the pending step exactly, then answer the packet.

Correctness then does not depend on GDB's packet sequence, only speed does. If a future GDB sent something else, case 3 would apply.

Two points have to be checked before implementing this:

- The stop reply currently expedites SREG, SP and PC (`handler.py`). After a deferred step, only the PC is known, so the reply would have to carry the PC alone, and GDB would have to cope with that.
- An RSP log of a continue from a breakpoint has to confirm that GDB sends `Z0` and `c` after the step without reading registers in between.

The range-stepping heuristic (see [Potential Speedup for Rangestepping](xtra-rangestepping-speedup.md)) also looks at the context of packets. The two should be considered together.

## Effort

This is a fair amount of special-casing for a probe that is rarely used: the re-arming, the swapped byte order, the deferred step, the return-address correction and the breakpoint allocation. Until then, the mkI stays with its four hardware breakpoints. The only change worth making independently is the address format in `erase_page_spm`, since the current one is wrong.
