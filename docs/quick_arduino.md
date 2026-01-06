# Quickstart Guides: Arduino IDE 2

Since PyAvrOCD is integrated into the Arduino IDE 2, it is pretty easy to start debugging. In general, the following steps have to be performed:

1. Install a debug-enabled core (see list of [debug-enabled Arduino cores](supporting-cores.md)).
2. Perhaps some [changes on the board](board-preparation.md) are necessary, e.g., disconnecting some components or opening a solder bridge.
3. On JTAG targets, you may need to [enable the JTAG pins](fuse-preparation.md).
4. [Connect the target board](connect-to-target.md) to the debugger.
5. Start debugging!
6. Restore the board by using the `Burn Bootloader` action and reconnect disconnected components and/or re-solder the opened solder bridge.

The following two quickstart guides should pave the way to AVR debugging in the Arduino IDE 2:

- [Debugging using the ATmega328P Xplained Mini board](#quickstart-guide-atmega328p-xplained-mini), which has an Arduino UNO footprint, is very care-free because the debugger is already on the board. So, no board preparations or connections are necessary.
- [Debugging using the dw-link debugger](#quickstart-guide-dw-link-attiny85) lowers the entry to serious embedded debugging because the debug probe is an Arduino UNO.

{!quick_arduino_xmini.md!}

{!quick_arduino_attiny.md!}