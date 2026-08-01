# Supported platforms

As the name suggests, PyAvrOCD is a Python script, which means it is basically platform-agnostic. A critical dependence is the [HIDAPI library](https://github.com/libusb/hidapi/) and the [Python interface](https://pypi.org/project/hidapi/) to it. The HIDAPI library works apparently for Linux, FreeBSD, macOS, and Windows. It may be possible to build it also for other platforms.

One can distinguish the support of PyAvrOCD based on whether one can install the package via PyPI using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/#use-pip-for-installing), or even better [pipx](https://pipx.pypa.io/stable/), or whether there is additionally Arduino support, meaning that you install an Arduino core and you get all tools (avr-gdb, simavr) and configurations (svd files) with it. In the table below, you can see which platform is supported in which way. Anything in boldface means that I have tested it.

| Platform                                           | PyPI    | Arduino<br> support |
| -------------------------------------------------- | ------- | ------------------- |
| macOS 14, Intel 64-bit                             | **yes** | **yes**             |
| macOS 14, Apple Silicon 64-bit                     | **yes** | **yes**             |
| Linux Ubuntu 22.02, Intel 64-bit                   | **yes** | **yes**             |
| Linux Ubuntu 22.02, ARM 64-bit                     | **yes** | **yes**             |
| Linux Debian 11 (Bookworm), Intel 32-bit           | **yes** | **yes**             |
| Linux Raspi OS 5.0 (Bookworm), ARM 32-bit (armv6l) | **yes** | **yes**             |
| Windows 10, Intel 64-bit                           | **yes** | **yes**             |
| Windows 11, ARM 64-bit<br> (emulated)              | **yes** | **yes**             |
| Windows 10, Intel 32-bit                           | **yes** | **yes**             |


As mentioned above, FreeBSD should work as well, but I couldn't convince myself so far to install another OS on my machines in order to test it.

In general, one expects that the software should run on the platforms they were built on and on newer versions of the respective operating systems. Windows and macOS may also provide some backward compatibility, but I am not able to test that.

The GDB clients for Linux are statically linked and should be able to run on older versions of Debian-based distros and probably on other distros as well. The Linux versions of PyAvrOCD bring all the dynamic libraries with them, meaning that it should be possible to run it on older Debian-based distributions. However, when moving to non-Debian systems, one could expect that HIDAPI support may fail. Simavr is packaged as provided by the original repo. This means that they may fail on older systems.

If a PyAvrOCD binary does not work for you, you may want to fall back on [installing the package with pip or pipx](install.md#pypi).

