# Avrocd tools on 32-bit operating systems

PyAvrOCD is not supported out of the box on 32-bit systems or in 32-bit IDEs (such as the legacy Arduino IDE). The main reason is that GitHub does not provide 32-bit hosts on which the software could be built.

The main reason for the existence of this dummy 32-bit tool package is that without it, you could not install the Arduino board package, even if you do not care about debugging at all.
If you want to use debugging software on a 32-bit system (without the Arduino IDE2), copy a (reasonably recent) 32-bit AVR-GDB version from somewhere (your package management system on Linux or download from [Zak's webpage](https://blog.zakkemble.net/avr-gcc-builds/) for Windows). In addition, install PyAvrOCD on your system using a 32-bit Python system using pipx as described in  [INSTALL.md](https://github.com/felias-fogg/PyAvrOCD/blob/main/INSTALL.md) file.

If, however, this 32-bit tool package ended up on your 64-bit machine, it could be that you installed an Arduino board package through the legacy Arduino IDE, which is a 32-bit Java system. You can get the 64-bit tool package by removing the Arduino board package and reinstalling it from the Arduino IDE 2.
