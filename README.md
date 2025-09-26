#  PyAvrOCD

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Commits since latest](https://img.shields.io/github/commits-since/felias-fogg/PyAvrOCD/latest?include_prereleases)](https://github.com/felias-fogg/PyAvrOCD/commits/master)
![Hit Counter](https://visitor-badge.laobi.icu/badge?page_id=felias-fogg_PyAvrOCD)

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/logo-small.png" width="15%">
</p>
*This is a **work in progress** that is not yet ready for general use yet. Use [dw-gdbserver](https://github.com/felias-fogg/dw-gdbserver) if you are interested in a working system (for debugWIRE targets)*.

------

PyAvrOCD is a [GDB server](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Server.html) for 8-bit AVR MCUs (list of [supported MCUs](https://felias-fogg.github.io/PyAvrOCD/supported-mcus/) and [supported boards](https://felias-fogg.github.io/PyAvrOCD/supported-boards/)). It can communicate with Microchip debuggers such as [Atmel-ICE](https://www.microchip.com/en-us/development-tool/atatmel-ice) and [MPLAB Snap](https://www.microchip.com/en-us/development-tool/pg164100), and provides a pass-through service for the Uno-based debugger [dw-link](https://github.com/felias-fogg/dw-link) (list of [supported hardware debuggers](https://felias-fogg.github.io/PyAvrOCD/supported-debuggers/)).

So, why another open-source GDB server for AVR MCUs? The main intention is to provide a *platform-agnostic* AVR GDB server. In other words, it is ***the missing AVR debugging solution*** for [PlatformIO](https://platformio.org) and the [Arduino IDE 2](https://www.arduino.cc/en/software/). And it excels in [minimizing flash wear](https://arduino-craft-corner.de/index.php/2025/05/05/stop-and-go/) and [protects single-stepping against interrupts](https://arduino-craft-corner.de/index.php/2025/03/19/interrupted-and-very-long-single-steps/).

![ide2-6](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/ide2-6.png)You can [install PyAvrOCD as part of an Arduino core](https://felias-fogg.github.io/PyAvrOCD/install-link/#arduino-ide-2), so that it can be used in the Arduino IDE 2. You can [download binaries](https://felias-fogg.github.io/PyAvrOCD/install-link/#downloading-binaries), you can install PyAvrOCD using [PyPI](https://felias-fogg.github.io/PyAvrOCD/install-link/#pypi), or you can, of course, [clone or download the GitHub repo](https://felias-fogg.github.io/PyAvrOCD/install-link/#github).

[Read the docs](https://felias-fogg.github.io/PyAvrOCD/index.html) for more information.


## What has been done so far and what to expect in the future

The GDB server has been integrated into MiniCore, MicroCore, and my fork of ATTinyCore. Recently, support for JTAG mega chips has been added. However, PyAvrOCD support has not been incorporated into the respective cores yet, but will be soon. UPDI MCUs will follow next. I am unsure about Xmegas.
