# DebugWIRE tools under 32-bit operating systems

There is no built-in debugging support for 32-bit operating systems and IDEs (such as the legacy Arduino IDE) because Arduino IDE 2 works only on 64-bit systems.

If you want to use debugging software on a 32-bit system (without the Arduino IDE2), copy a (reasonably recent) AVR-GDB version from somewhere (your package management system on Linux or download from [Zak's webpage](https://blog.zakkemble.net/avr-gcc-builds/) for Windows). In addition, install PyAvrOCD on your system using a 32-bit Python system using pipx as described in  [INSTALL.md](https://github.com/felias-fogg/PyAvrOCD/blob/main/INSTALL.md) file.
