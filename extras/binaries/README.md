# Binaries for avrocd-tools

The binaries in this folder provide debug support for AVR chips to be used in the Arduino IDE 2. For each host architecture, there is an avr-gdb program, a simavr program, and a  PyAvrOCD server. The avr-gdb programs have version 17.2 and have been generated using the `avr-gdb-build.sh` script in the [avr-gdb repo](https://github.com/felias-fogg/avr-gdb).

PyAvrOCD is generated using PyInstaller on GitHub runners:

- **Apple (x86_64)**: macOS 14 / Python 3.14, libusb 1.0.29
- **Apple (ARM64)**: macOS 14 / Python 3.14, libusb 1.0.29
- **Linux (x86_64)**: Ubuntu 22.04 / Python 3.14
- **Linux (i686)**: Debian 12 (Bookworm), Python 3.11 (generated on my PC)
- **Linux (ARM64)**: Ubuntu 22.04 / Python 3.14
- **Linux (armv6l)**: Raspi OS 5 (Bookworm), Python 3.11
- **Windows (x86_64)**: Windows 10 (2022
- ) / Python 3.14
- **Windows (i686)**: Windows 10 (2022) / Python 3.14, architecture: x86

