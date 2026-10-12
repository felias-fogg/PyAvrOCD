# Supported platforms

As the name suggests, PyAvrOCD is a Python package. As such, you can install it from PyPI using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/#use-pip-for-installing), or even better [pipx](https://pipx.pypa.io/stable/). The main requirement is that your Python installation should have a version number between 3.10 and 3.14, inclusively. Since it is Python,  the package is basically platform-agnostic. A critical dependence is the [HIDAPI library](https://github.com/libusb/hidapi/) and the [Python interface](https://pypi.org/project/hidapi/) to it, which is needed to communicate with the EDBG-based debuggers over USB. The HIDAPI library apparently works for Linux, FreeBSD, macOS, and Windows, and there are Python wheels (binaries) that can be used for all of these platforms.

The minimal requirements for binary packages as downloaded, e.g., by the Arduino IDE, are displayed in the following table.

| Computing platform                 | Minimal OS/GLIBC version             |
| ---------------------------------- | ------------------------------------ |
| macOS, Intel 64-bit                | macOS 10.15                          |
| macOS, Apple Silicon 64-bit        | macOS 11.0                           |
| Linux Ubuntu, Intel 64-bit         | GLIBC 2.35 (Ubuntu 22.04, Debian 12) |
| Linux Ubuntu, ARM 64-bit           | GLIBC 2.35 (Ubuntu 22.04, Debian 12) |
| Linux Debian, Intel 32-bit         | GLIBC 2.36 (Debian 12)               |
| Linux Debian, ARM 32-bit (armv6l)  | GLIBC 2.36 (Debian 12, Pi OS 5)      |
| Windows, Intel 64-bit              | Windows 10                           |
| Windows, ARM 64-bit (emulated)[^*] | Windows 11                           |
| Windows, Intel 32-bit              | Windows 10                           |

[^*]: The *libusb* library does not work for programs executed on ARM CPUs when in emulation mode. For this reason, debugging probes using USB bulk transfer are not supported on ARM CPUs. It is planned to build native ARM binaries in the future as well, which will solve this problem.

