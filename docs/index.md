# PyAvrOCD

PyAvrOCD is a Python GDB server for 8-bit AVR MCUs (currently only classic debugWIRE and JTAG ATtinys and ATmegas), enabling you to debug programs running on these MCUs using the [GNU Project Debugger GDB](https://www.sourceware.org/gdb/). PyAvrOCD communicates with Microchip's debug probes, such as [Atmel-ICE](https://www.microchip.com/en-us/development-tool/atatmel-ice) and [MPLAB Snap](https://www.microchip.com/en-us/development-tool/pg164100), using the software infrastructure provided by [pymcuprog](https://github.com/microchip-pic-avr-tools/pymcuprog) and [pyedgblib](https://github.com/microchip-pic-avr-tools/pyedbglib). In addition, it provides a pass-through service for the UNO-based debug probe [dw-link](https://felias-fogg.github.io/dw-link) and the simulation tool [simavr](https://github.com/buserror/simavr).

Why another open-source GDB server for AVR MCUs (others are [AVaRICE](https://github.com/avrdudes/avarice) and [Bloom](https://github.com/bloombloombloom/Bloom))? The main intention is to provide a *cross-platform* AVR GDB server. In other words, it is *the missing AVR debugging solution* for [PlatformIO](https://platformio.org) and the [Arduino IDE 2](https://www.arduino.cc/en/software/).

![ide2-6](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/ide2-6.png)

In addition to being cross-platform, PyAvrOCD offers some enhancements over its "competitors", particularly in terms of [flash wear](https://arduino-craft-corner.de/index.php/2025/05/05/stop-and-go/) and [single-stepping](https://arduino-craft-corner.de/index.php/2025/03/19/interrupted-and-very-long-single-steps/).

After [installing the package](install-link.md), the following steps are necessary for successful debugging:

1. [Installing and configuring the appropriate debugging software](debugging-software.md)
2. [Preparing the target board for debugging](board-preparation.md)
3. [Connecting the debug probe to the target](connect-to-target.md)
4. [Invoking the GDB server](command-line-options.md)
5. [Debugging a program on the target](debugging.md)
6. [Restoring the target board to its original state](restore-original-state.md)

Once you have a symbolic debugger connected to the GDB server, you can control the server's behavior using [`monitor` commands](monitor-commands.md).

While the package appears to function as intended, there is always the chance of a bug, the documentation may need improvements, or a feature may be missing. Or you simply have a question or an idea. We are always happy to receive [contributions](contributing.md) along those lines.

