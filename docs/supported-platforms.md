# Supported platforms

As the name suggests, PyAvrOCD is a Python script, which means it is basically platform-independent. Of course, you need a Python interpreter on board (>=3.10, and currently <= 3.13), provided you download the source code. When you install an Arduino core, which includes PyAvrOCD as a binary tool, even the Python interpreter is included.

A further critical dependence is the [HIDAPI library](https://github.com/libusb/hidapi/) and the [Python interface](https://pypi.org/project/hidapi/) to it. This works apparently for Linux, FreeBSD, macOS, and Windows. For other platforms, you have to build it from sources.

Furthermore, you can distinguish the support on whether you can install the package via PyPI using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/#use-pip-for-installing), or even better [pipx](https://pipx.pypa.io/stable/), or whether there is also Arduino IDE 2 support, meaning that you install an Arduino core and you get all tools and configurations with it. In the table below, you can see which platform is supported in which way. Anything in boldface means that I have tested it.

| Platform                          | PyPI support | Arduino IDE 2 support  |
| --------------------------------- | ------------ | ---------------------- |
| macOS 15, Apple Silicon 64-bit    | **yes**      | **yes** **(native)**   |
| macOS 15, Intel 64-bit            | **yes**      | **yes**                |
| Linux, Ubuntu 22.02, ARM 64-bit   | **yes**      | **yes**                |
| Linux, Ubuntu 22.02, ARM 32-bit   | yes          | no                     |
| Linux, Ubuntu 22.02, Intel 64-bit | **yes**      | **yes**                |
| Linux, Ubuntu 22.02, Intel 32-bit | yes          | no                     |
| Windows 11, ARM 64-bit            | **yes**      | **yes** **(emulated)** |
| Windows 11, Intel 64-bit          | **yes**      | **yes**                |
| Windows 11, Intel 32-bit          | yes          | no                     |

As mentioned above, FreeBSD should work as well, but I couldn't convince myself so far to install another OS on my machines in order to test it. 