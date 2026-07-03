# PyAvrOCD

PyAvrOCD[^1] is *the missing AVR debugging solution* for  [Arduino IDE 2](https://www.arduino.cc/en/software/) and [PlatformIO](https://platformio.org). It is tightly integrated into both IDEs (see [quickstart guides](quick_arduino.md)).

![ide2-6](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/ide2-6.png)PyAvrOCD is a Python GDB server[^2] for 8-bit AVR MCUs, enabling you to debug programs running on these MCUs using the [GNU Project Debugger GDB](https://www.sourceware.org/gdb/). This means it supports debugging in all IDEs that use GDB as the symbolic debugger. PyAvrOCD communicates with Microchip's debug probes, such as [MPLAB Snap](https://www.microchip.com/en-us/development-tool/pg164100) and the embedded debuggers on AVR Xplained and Curiosity boards. In addition, it provides a pass-through service for the UNO-based debug probe [dw-link](https://felias-fogg.github.io/dw-link) and the simulation tool [simavr](https://github.com/buserror/simavr).

Why another open-source GDB server for AVR MCUs (others are [AVaRICE](https://github.com/avrdudes/avarice) and [Bloom](https://github.com/bloombloombloom/Bloom))? The main intention is to provide a *cross-platform* AVR GDB server, which can be packaged with the Arduino IDE and PlatformIO. In addition to being cross-platform, PyAvrOCD offers some enhancements over its "competitors", particularly in terms of [flash wear](https://arduino-craft-corner.de/index.php/2025/05/05/stop-and-go/) and [single-stepping](https://arduino-craft-corner.de/index.php/2025/03/19/interrupted-and-very-long-single-steps/).

After [installing the package](install.md), the following steps are necessary for successful debugging:

1. [Installing and configuring the appropriate debugging software](debugging-software.md)
2. [Preparing the target board for debugging](board-preparation.md)
3. [Setting the right fuses](fuse-preparation.md)
4. [Connecting the debug probe to the target](connect-to-target.md)
5. [Compiling the program to be tested](compilation-options.md)
6. [Invoking the GDB server](command-line-options.md)
7. [Debugging a program on the target](debugging.md)
8. [Restoring the target board to its original state](restore-original-state.md)

Do not be discouraged by this long list. In your day-to-day business only steps 5-7 are relevant. And they will become routine after a while.

You have [feedback](contributing.md)? Send it immediately!

[^1]: How to pronounce PyAvrOCD? Since AVR and OCD are both initialisms, the canonical pronunciations would be Pie-Ay-Vee-Ar-Oh-See-Dee. However, you are free to pronounce it as 'Piaf rocked'.
[^2]: The term *GDB server* is loosely used for programs that provide an interface similar to what the program `gdbserver` does in the context of the GNU Project Debugger GDB. `gdbserver` runs on the target machine, controlling the program to be debugged and communicating with the GDB on the host machine using the *remote serial protocol* (RSP). In contrast to that, a GDB server in the context of embedded debugging usually does not run on the target machine, but either on the hardware debug adapter or on the host. However, it also uses RSP for communicating with GDB.
