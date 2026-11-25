# Problems that occurred during end-to-end testing

While running the end-to-end test, I had to make some amends to get them through:

- ATmega32 and PICkit4: I had to introduce a decoupling break between single tests of 2.5 seconds. In addition.
- ATtiny13: Sometimes, the lockbits are not set by the Makefile. Actually, this happened with other MCUs as well.
- The new ATTinyCore produced very different code for the ATtiny841. It made the isr.ino sketch undebuggable!  Problems were: Code inlining and a strange handling of interrupts. So, I switched back to the old core.
     - It turned out that many things were at play here. Most importantly, I use the wrong pin mapping leading to the wrong pin for INT0, which meant that IRQs were active during I/O. Using the right pin, everything worked out. Big question: Why did it work with the old core, although the mapping was wrong?
- ATmega2561 and Atmel-ICE: After a few tests, the MCU gives the error "`Debug session not started: AVR8_FAILURE_NO_DEVICE_FOUND: no devices detected`". This happens when "Error while connecting to target OCD:". However, no problem with SNAP.
     - I just had to remove the deactive_physical/activate_physical when switching between modes.
- Turned out that ATmega64 also has a stuck-at-one bit in the PC
- I added in `_activate_interface` (in xavrdebug) to the call `self.device.avr.protocol.activate_physical()`  the parameter `use_reset=False`. This will try to reset the chip in order to gain control of JTAG again, when this has been disabled with the JTD bit.  This is OK as long as we do not have a EDBG debugger! In this case, we get the error message "AVR8_FAILURE_TIMEOUT: It just took too long"
     - So for EDBG debuggers, we do not request a RESET
- It seems that GDB mixes up where to look for return addresses if we have a function with a non-empty stack frame (see pctest). This happens with the old and new compiler code.
- Microchip Studio also loses the stack backtrace when the MCUs have a non-zero unused bit!
- When checking for stuck 1-bits in the program counter, I so far assumed that flash size is a power of two. This is not true for the ATmega4809! I now have to check how many bits are used and then compute the mask from that.
- Beware of setting UPDI communication speed too low. This can lead to single-step skidding (with speeds below 400 kbps).
- My CNANO attiny3227 gets a flash verification error at 0x01480 when loading `tictactoe` after `flashed.ino`. It goes away when erasing the chip completely before loading. And then, after buying a second sample, it works without a hitch.
- My CNANO attiny1607 chokes after clearing the lock bits with `AVR8_FAILURE_PDI_TIMEOUT: PDI physical timed out` after having been switched to debmode. Waiting for 0.3 seconds after switching to deb mode helped.
- With the AVR Dx and Ex devices, the C-program ceeprom.c writing into EEPROM chokes (GCC 15.2, avrlibc 2.2.1). After calling `write_eprom_byte`, the value is unchanged and you cannoz write to EEPROM anymore from the debugger! For this reason, I will use the Arduino program again, which works flawlessly. My guess: A bug in avr-libc 2.2.1, but then I am not sure about that.
- The AVR64EA48 crashes on `flashed.ino` when there is a `Serial.begin(9600)` in `setup`. All other chips do OK.
- <s>The DX/EX CNANO boards do not communicate over the virtual serial line.</s> You have to figure out, which serial line and which Swap Microchip used for each board.
- The AVR16DU28 and AVR32DU28 did not compile with the homebrew GCC toolchain because some files were missing.
- AVR32EB28 device spec is missing from homebrew version of GCC15 toolchain. And it is locked and cannot be unlocked.