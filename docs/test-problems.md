# Problems that occurred during end-to-end testing

While running the end-to-end test, I had to make some amends to get them through:

- ATmega32 and PICkit4: I had to introduce a decoupling break between single tests of 2.5 seconds. In addition, I had to extend
- ATtiny13: Sometimes, the lockbits are not set by the Makefile. Actually, this happened with other MCUs as well.
- The new ATTinyCore produced very different code for the ATtiny841. It made the isr.ino sketch undebuggable!  Problems were: Code inlining and a strange handling of interrupts.