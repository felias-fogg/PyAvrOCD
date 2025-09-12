#  pyavrocd

Pyavrocd is a [GDB server](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Server.html) for 8-bit AVR MCUs ([list of supported MCUs and boards](https://felias-fogg.github.io/pyavrocd/supported-mcus-and-boards/)). It can communicate with Microchip debuggers such as [Atmel-ICE](https://www.microchip.com/en-us/development-tool/atatmel-ice) and [MPLAB Snap](https://www.microchip.com/en-us/development-tool/pg164100) ([in AVR mode](#switching-to-avr-mode)), and provides a pass-through service for the Uno-based debugger [dw-link](https://github.com/felias-fogg/dw-link) ([list of supported hardware debuggers]()). For Microchip debuggers, pyavrocd uses the infrastructure provided by [pymcuprog](https://github.com/microchip-pic-avr-tools/pymcuprog) and [pyedgblib](https://github.com/microchip-pic-avr-tools/pyedbglib).

So, why another open-source GDB server for AVR MCUs (others are [AVaRICE](https://github.com/avrdudes/avarice) and [Bloom](https://bloom.oscillate.io))? The main intention is to provide a *platform-agnostic* AVR GDB server. In other words, it is the missing AVR debugging solution for [PlatformIO](https://platformio.org) and the [Arduino IDE 2](https://www.arduino.cc/en/software/).

![ide2-6](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide2-6.png)You can [install pyavrocd as part of an Arduino core](https://felias-fogg.github.io/pyavrocd/INSTALL/#arduino-ide-2), so that it can be used in the Arduino IDE 2. You can [download binaries](https://felias-fogg.github.io/pyavrocd/INSTALL/#downloading-binaries), you can install pyavrocd using [PyPI](https://felias-fogg.github.io/pyavrocd/INSTALL/#pypi), or you can, of course, [clone or download the GitHub repo](https://felias-fogg.github.io/pyavrocd/INSTALL/#github). Check the [docs](https://felias-fogg.github.io/pyavrocd/index.html) for more information.


## What to expect in the future

The GDB server has been integrated into MiniCore, MicroCore, and my fork of ATTinyCore. Support for JTAG mega chips has been added, but pyavrocd has not been incorporated into the respective cores yet, but will soon be. UPDI targets will follow next.

