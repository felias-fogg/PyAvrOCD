# PyAvrOCD Installation

### Arduino IDE 2

If you want to use PyAvrOCD as part of Arduino IDE 2, you do not need to install it explicitly. It is sufficient [to add an "additional boards manager URL" ](http://pyavrocd.io/debugging-software/#arduino-ide-2) and [install the respective core](http://PyAvrOCD.io/supporting-cores/). It will then be installed as a tool for this core. Together with PyAvrOCD, you will also get the GDB client `avr-gdb` and the simulator (for some AVR chips) `simavr`.

If you want to use PyAvrOCD stand-alone or as part of another IDE, you need to install the PyAvrOCD package explicitly, as described below.

### Downloading binaries

Go to the [GitHub page](https://github.com/felias-fogg/PyAvrOCD), click on the label `Latest` below the section title `Releases` (located on the right-hand side of the page), download the archive containing the binary for your architecture, and then untar the archive. It includes the folder `tools`, which in turn contains the executable `pyavrocd` (or `pyavrocd.exe`), a folder `pyavrocd-util`,  `avr-gdb` (or `avr-gdb.exe`), the GDB debugger for AVR chips, and additionally `simavr` (or `simavr.exe`), a software simulator of some of the AVR chips.

Store all of it somewhere in the same folder and preferably include this folder in your `PATH` variable. My preference for such a folder is `~/.local/bin` , which will be used throughout this document. So, in order to store everything there, use the following shell commands (PowerShell on Windows):

```sh
mv tools/* ~/.local/bin
```

The avr-gdb debugger has version 17.1, which is relatively recent, and has been compiled for your architecture with only a minimal amount of references to dynamic libraries. It is strongly advised to use this version since it contains a few patches.

Since the binaries were generated on very recent versions of the respective operating systems, it can happen that the binary is not compatible with your operating system. In this case, use one of the methods below.

### PyPI

I assume you already installed a recent Python version (>=3.10). Then [PyPI](https://pypi.org/project/pyavrocd/) will bring you the most recent version of PyAvrOCD to your computer.

It is possible to install PyAvrOCD using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/). However, it is recommended to use [pipx](https://pipx.pypa.io/) instead. Pipx installs packages in a way such that they are entirely isolated from the rest of your Python installation and can be invoked as an ordinary binary executable. So, if you haven't done so already, install pipx following the instructions on the [pipx website](https://pipx.pypa.io/stable/installation/). Then proceed as follows.

```bash
> pipx install pyavrocd
> pipx ensurepath
```

After restarting the shell, you should be able to start the GDB server. The binary is stored under `~/.local/bin/`.

Note that the folder with [SVD](https://arduino-craft-corner.de/index.php/2025/08/01/system-view-descriptions-of-avr-mcus/) files is not part of the PyPI installation. If you want to use SVD files, they have to be downloaded separately from the [release page](https://github.com/felias-fogg/PyAvrOCD/releases/tag/v0.22.0) of the GitHub repo. The release asset is called `svd.tar.gz`.

### GitHub

Alternatively, you can download or clone the [GitHub repository](https://github.com/felias-fogg/PyAvrOCD). Additionally, you need to install a Python package manager, for instance, [Poetry](https://python-poetry.org):

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

As a result, you find an executable `pyavrocd` (or `pyavrocd.exe`) in the directory `dist/pyavrocd/` together with the folder `pyavrocd-util`. You can copy those two to a place in your `PATH`.

### Some OS idiosyncrasies

**Linux**: On a Linux installation, users may need to add a few `udev` rules after having installed PyAvrOCD. On a Linux installation, users may need to add a few `udev` rules after having installed PyAvrOCD. Download [https://pyavrocd.io/99-edbg-debuggers.rules](https://pyavrocd.io/99-edbg-debuggers.rules), edit if you want, and copy to `/etc/udev/rules.d/`.

**Mac**: On a Mac, files downloaded through a browser or from an email are marked as potentially dangerous, and the system may not allow them to be executed.  In this case, use the command

```bash
xattr -d com.apple.quarantine FILE
```

in order to remove the extended attribute `com.apple.quarantine` from the binary executable FILE.
