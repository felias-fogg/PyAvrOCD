# Supported platforms

As the name suggests, PyAvrOCD is a Python script, which means it is basically platform-independent. Of course, you need a Python interpreter on board (>=3.10, and currently <= 3.13) when you download the PyAvrOCD from PyPI using pip or pipx. When you install an Arduino core that includes PyAvrOCD as a binary tool, even the Python interpreter is already included.

A critical dependence is the [HIDAPI library](https://github.com/libusb/hidapi/) and the [Python interface](https://pypi.org/project/hidapi/) to it. The HIDAPI library works apparently for Linux, FreeBSD, macOS, and Windows. It may be possible to build it also for other platforms.

One can distinguish the support based on whether one can install the package via PyPI using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/#use-pip-for-installing), or even better [pipx](https://pipx.pypa.io/stable/), or whether there is also Arduino IDE 2 support, meaning that you install an Arduino core and you get all tools and configurations with it. In the table below, you can see which platform is supported in which way. Anything in boldface means that I have tested it.

| Platform                                         | PyPI support | Arduino IDE 2 support  |
| ------------------------------------------------ | ------------ | ---------------------- |
| macOS 15, Apple Silicon 64-bit                   | **yes**      | **yes**                |
| macOS 15, Intel 64-bit                           | **yes**      | **yes**                |
| Linux, Ubuntu 22.02, ARM 64-bit                  | **yes**      | **yes**                |
| Linux, Ubuntu 22.02, Intel 64-bit                | **yes**      | **yes**                |
| Linux Debian 13 (Trixie)/Raspi OS 6.0 ARM 32-bit | **yes**[^*]  | **no**                 |
| Linux  Intel 32-bit                              | yes          | **no**                 |
| Windows 10, ARM 64-bit                           | **yes**      | **yes** **(emulated)** |
| Windows 10, Intel 64-bit                         | **yes**      | **yes**                |
| Windows 10, Intel 32-bit                         | **yes**      | **yes**                |

As mentioned above, FreeBSD should work as well, but I couldn't convince myself so far to install another OS on my machines in order to test it.

[^*]: You need to install the two packages `libusb-dev` and `libudev-dev` so that the hidapi package can be built.

