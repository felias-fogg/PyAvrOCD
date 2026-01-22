# Binaries for avrocd-tools

The binaries in this folder provide the debug support for AVR chips to be used in the Arduino IDE 2. For each host architecture, there is an avr-gdb program and a  PyAvrOCD server. The avr-gdb programs have version 17.1 and have been generated using the `avr-gdb-build.sh` script in the [avr-gdb repo](https://github.com/felias-fogg/avr-gdb).

PyAvrOCD is generated using PyInstaller on GitHub runners:

- **Apple (x86_64)**: macOS 15 / Python 3.14, libusb 1.0.29
- **Apple (ARM64)**: macOS 15 / Python 3.14, libusb 1.0.29
- **Linux (x86_64)**: Ubuntu 24.04 / Python 3.14
- **Linux (ARM64)**: Ubuntu 24.04 / Python 3.14
- **Windows (x86_64)**: Windows 10 (2025) / Python 3.14
- **Windows (i686)**: Windows 10 (2022) / Python 3.14, architecture: x86

There are also two folders for 32-bit OSs (Linux Intel+Arm), which, however, contain only dummy executables that output an error message. These are necessary so that people can download a package even when debug support is not possible.