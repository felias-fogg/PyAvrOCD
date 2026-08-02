# Supported platforms

As the name suggests, PyAvrOCD is a Python script, which means it is basically platform-agnostic. A critical dependence is the [HIDAPI library](https://github.com/libusb/hidapi/) and the [Python interface](https://pypi.org/project/hidapi/) to it. The HIDAPI library works apparently for Linux, FreeBSD, macOS, and Windows. It may be possible to build it also for other platforms.

One can distinguish the support of PyAvrOCD based on whether one can install the package via PyPI using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/#use-pip-for-installing), or even better [pipx](https://pipx.pypa.io/stable/), or whether there is additionally Arduino support, meaning that you install an Arduino core and you get all tools (avr-gdb, simavr) and configurations (svd files) with it. In the table below, you can see which platform is supported in which way. Anything in boldface means that I have tested it.

| Platform                                          | PyPI    | Arduino<br> support |
| ------------------------------------------------- | ------- | ------------------- |
| macOS 14, Intel 64-bit                            | **yes** | **yes**             |
| macOS 14, Apple Silicon 64-bit                    | **yes** | **yes**             |
| Linux Ubuntu 24.02, Intel 64-bit                  | **yes** | **yes**             |
| Linux Ubuntu 24.02, ARM 64-bit                    | **yes** | **yes**             |
| Linux Debian 12 (Bookworm), Intel 32-bit          | **yes** | **yes**             |
| Linux Raspi Pi OS 6 (Trixie), ARM 32-bit (armv6l) | **yes** | **yes**             |
| Windows 10 (2022), Intel 64-bit                   | **yes** | **yes**             |
| Windows 11 (2022), ARM 64-bit<br> (emulated)      | **yes** | **yes**             |
| Windows 10 (2022), Intel 32-bit                   | **yes** | **yes**             |

As mentioned above, FreeBSD should work as well, but I couldn't convince myself so far to install another OS on my machines in order to test it.

While some efforts have been made to make the software as broadly compatible as possible, it can happen that some tools may fail if you use a platform different from the above or an older version than the one stated above (see [Troubleshooting](troubleshooting.md) section). More recent versions are usually OK.

