# Problems that occurred during end-to-end testing

While running the end-to-end test, I had to make some amends to get them through:

- ATmega32 and PICkit4: I had to introduce a decoupling break between single tests of 2.5 seconds. In addition, I had to extend
- ATtiny13: Sometimes, the lockbits are not set by the Makefile. Actually, this happened with other MCUs as well.
- The new ATTinyCore produced very different code for the ATtiny841. It made the isr.ino sketch undebuggable!  Problems were: Code inlining and a strange handling of interrupts. So, I switched back to the old core.
- ATmega2561 and Atmel-ICE: After a few tests, the MCU gives the error "Debug session not started: AVR8_FAILURE_NO_DEVICE_FOUND: no devices detected". This happens when "Error while connecting to target OCD:". However, no problem with SNAP.
     - I just had to remove the deactive_physical/activate_physical when switching between modes.
- Turned out that ATmega64 also has a stuck-at-one bit in the PC
- I added in `_activate_interface` (in xavrdebug) to the call `self.device.avr.protocol.activate_physical()`  the parameter `use_reset=False`. This will try to reset the chip in order to gain control of JTAG again, when this has been disabled with the JTD bit.  This is OK as long as we do not have a EDBG debugger! In this case, we get the error message "AVR8_FAILURE_TIMEOUT: It just took too long"
     - So for EDBG debuggers, we do not request a RESET
- It seems that GDB mix up where to look for return addresses if we have a function with a non-empty stack frame (see pctest). This happens with the old and new compiler code.
- Microchip Studio also loses the stack backtrace when the MCUs have a non-zero unused bit!