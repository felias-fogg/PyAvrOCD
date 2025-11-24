# Binaries for avrocd-tools

The binaries in this folder provide the debug support for AVR chips to be used in the Arduino IDE 2. For each host architecture, there is an avr-gdb program and a  PyAvrOCD server. The avr-gdb programs have version 16.3 and have been generated as follows:

- **Apple (x86_64 + ARM)**: Using the [compilation.md](https://github.com/guyush1/gdb-static/blob/develop/compilation.md) recipe from the [gdb-static](https://github.com/guyush1/gdb-static) repo, I generated binaries that only rely on Mac system libraries. So it is not necessary to install Homebrew. The dependencies are actually similar to what the Microchip avr-gdb binaries require. Note that for building the binaries, it is probably essential to uninstall all the Homebrew libs that might interfere. And it is advisable to use the `--with-system-zlib` option, because the binutils version of the lib is not compatible with clang.
- **Linux (x86_64)**: I simply used the version from Zak's repo [avr-gcc-build](https://github.com/ZakKemble/avr-gcc-build). It is not static, but has only a limited number of dependencies on dynamic libraries.
- **Linux (AARCH64):** I used the Docker provided by Zak (see above) and generated an ARM64 version on my ARM64 VM.
- **Windows (x86_64)**: Again, I used Zak's version. Seems to work on Window10 as well.
- **Windows (i686):** And again Zak's version.

PyAvrOCD is generated using PyInstaller on GitHub runners:

- **Apple (x86_64)**: macOS 13 / Python 3.13, libusb 1.0.29
- **Apple (ARM64)**: macOS 14 / Python 3.13, libusb 1.0.29
- **Linux (x86_64)**: Ubuntu 22.04 / Python 3.13
- **Linux (ARM64)**: Ubuntu 22.04 / Python 3.13
- **Windows (x86_64)**: Windows 10 (2025) / Python 3.13
- **Windows (i686)**: Windows 10 (2022) / Python 3.13, architecture: x86

There are also two folders for 32-bit OSs (Linux Intel+Arm), which, however, contain only dummy executables that output an error message. These are necessary so that people can download a package even when debug support is not possible.