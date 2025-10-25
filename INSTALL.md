# PyAvrOCD Installation

## A note for Linux users

Note that Linux users may need to add a few `udev` rules after having installed PyAvrOCD. This can be accomplished by invoking PyAvrOCD once as root with the option `--install-udev-rules` (assuming that `pyavrocd` has been stored somewhere on the `PATH`):

```
> sudo pyavrocd --install-udev-rules
```

Alternatively, one can add the `udev` rules manually, following the instructions in the [pyedbglib README](https://github.com/microchip-pic-avr-tools/pyedbglib/blob/main/README.md#notes-for-linux-systems).

## Arduino IDE 2 (not implemented yet)

If you want to use PyAvrOCD as part of Arduino IDE 2, you do not need to install it explicitly. It is sufficient [to add an "additional boards manager URL" and install the respective core](https://felias-fogg.github.io/PyAvrOCD/debugging-software/#arduino-ide-2). It will then be installed as a tool for this core. As a Linux user, you may also need to set some permissions and provide udev rules as described above.

If you want to use PyAvrOCD stand-alone or as part of another IDE, you need to install the PyAvrOCD package explicitly, as described below.

## Downloading binaries

Go to the [GitHub page](https://github.com/felias-fogg/PyAvrOCD), select the latest release (located on the right-hand side of the page), download the archive containing the binary for your architecture, and then untar the archive. It includes the executable `pyavrocd` (or `pyavrocd.exe`), a folder `pyavrocd-util`, and additionally `avr-gdb` or (`avr-gdb.exe`), the GDB debugger for AVR chips. Store `pyavrocd` (or `pyavrocd.exe`) and `pyavrocd-util` somewhere in the same folder and include this folder in your `PATH` variable. The avr-gdb debugger has version 16.3, which is relatively recent, and has been compiled for your architecture with only a minimal amount of references to dynamic libraries. It is up to you to decide whether you want to use this version or the one that is already installed on your system.

Since the binaries were generated on very recent versions of the respective operating systems (Windows 11, macOS 15.4, Ubuntu 24.04), it can happen that the binary is not compatible with your operating system. In this case, use one of the methods below.

## PyPI

I assume you already installed a recent Python version (>=3.10).

It is possible to install PyAvrOCD using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/). However, it is recommended to use [pipx](https://pipx.pypa.io/) instead. Pipx installs packages in a way such that they are entirely isolated from the rest of your Python installation and can be invoked as an ordinary binary executable. So, if you haven't done so already, install pipx following the instructions on the [pipx website](https://pipx.pypa.io/stable/installation/). Then proceed as follows.

```bash
> pipx install pyavrocd
> pipx ensurepath
```

After restarting the shell, you should be able to start the GDB server. The binary is stored under `~/.local/bin/`.

## GitHub

Alternatively, you can download or clone the GitHub repository. Additionally, you need to install the Python package manager [Poetry](https://python-poetry.org):

```bash
> pipx install poetry
```

With that, you can start executing the script inside the downloaded folder as follows:

```bash
> poetry install
> poetry run pyavrocd ...
```

Furthermore, you can create a binary standalone package as follows:

```bash
> poetry run pyinstaller pyavrocd.spec
```

As a result, you find an executable `pyavrocd` (or `pyavrocd.exe`) in the directory `dist/pyavrocd/` together with the folder `pyavrocd-util`. You can copy those to a place in your `PATH`.
