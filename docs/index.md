# PyAvrOCD

PyAvrOCD is a Python [GDB server](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Server.html) for 8-bit AVR MCUs (currently only classic debugWIRE and JTAG ATtinys and ATmegas). It can communicate with Microchip debuggers such as [Atmel-ICE](https://www.microchip.com/en-us/development-tool/atatmel-ice) and [MPLAB Snap](https://www.microchip.com/en-us/development-tool/pg164100), and provides a pass-through service for the Uno-based debugger [dw-link](https://github.com/felias-fogg/dw-link). For Microchip debuggers, PyAvrOCD uses the infrastructure provided by [pymcuprog](https://github.com/microchip-pic-avr-tools/pymcuprog) and [pyedgblib](https://github.com/microchip-pic-avr-tools/pyedbglib).

Why another open-source GDB server for AVR MCUs (others are [AVaRICE](https://github.com/avrdudes/avarice) and [Bloom](https://github.com/bloombloombloom/Bloom))? The main intention is to provide a *cross-platform* AVR GDB server. In other words, it is ***the missing AVR debugging solution*** for [PlatformIO](https://platformio.org) and the [Arduino IDE 2](https://www.arduino.cc/en/software/).

![ide2-6](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/ide2-6.png)

In addition to being cross-platform, PyAvrOCD offers some enhancements over its "competitors", particularly in terms of [flash wear](https://arduino-craft-corner.de/index.php/2025/05/05/stop-and-go/) and [single-stepping](https://arduino-craft-corner.de/index.php/2025/03/19/interrupted-and-very-long-single-steps/).

After [installing the package](install-link.md), the following steps are necessary for successful debugging:

1. [Installing and configuring the appropriate debugging software](debugging-software.md)
2. [Preparing a target board for debugging](board-preparation.md)
3. [Connecting the debug probe to a target](connect-to-target.md)
4. [Invoking the GDB server](command-line-options.md)
5. [Debugging a program on a target](debugging.md)
6. [Restoring a target to its original state](restore-original-state.md)

Once you have a debugger connected to the server, you can control the server's behavior using [`monitor` commands](monitor-commands.md).

While the package appears to function as intended, there is always the chance of a bug, the documentation may need improvements, or a feature may be missing. Or you simply have a question or an idea. We are always happy to receive [contributions](contributing.md) along those lines.

