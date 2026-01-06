### Step 1: Installing PyAvrOCD

Go to the [PyAvrOCD GitHub repo](https://github.com/felias-fogg/PyAvrOCD/) and click on the `Latest` button below **Releases** on the right side of the page.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/repo.png" width="55%">
</p>


This will open the latest release page with all its assets.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/release.png" width="55%">
</p>


Here you can download the debug server executables for your platform. If there is nothing for you, there is an alternative way to install PyAvrOCD described [below](step-1a:-alternative-way-of-installing-pyavrocd). After downloading the archive, extract the files (for Windows, I assume, you use the `Windows PowerShell`):

```sh
> tar xvzf avrocd-tools-X.Y.Z-architecture.tar.gz
```

Once you have downloaded the archive and uncompressed it, you need to decide where to place the files contained in it. I prefer the folder `~/.local/bin/` (where `~` signifies the user folder). Move the three items that you find in the `tools` folder of the uncompressed archive to this folder (or any other place you have chosen):

- `pyavrocd`[`.exe`] - the debug server executable,
- `pyavrocd-util` - a folder with auxiliary code and data that should always be stored alongside the executable, and
- `avr-gdb`[`.exe`] - a current version (16.3) of the GDB debugger for AVR chips with a minimal amount of dependencies on dynamic libraries.

```shell
> mkdir ~/.local
> mkdir ~/.local/bin
> rm -rf ~/.local/bin/pyavrocd-util
> mv tools/* ~/.local/bin/
```

!!! info "Windows"
    On Windows, use `rmdir` instead of `rm -rf` above.

!!! info "Linux"
    Under Linux, you need to install `udev` rules so that the debug probes can communicate with the host. Download [https://pyavrocd.io/99-edbg-debuggers.rules](https://pyavrocd.io/99-edbg-debuggers.rules), edit if you want, and copy to `/etc/udev/rules.d/`.

!!! warning "macOS"
    On a Mac, files downloaded through a browser or from an email are marked as potentially dangerous, and the system may not allow them to be executed. In this case, use the command `xattr -d com.apple.quarantine FILE` in order to remove the extended attribute `com.apple.quarantine` from the binary executable FILE.



### Step 1a: An alternative way of installing PyAvrOCD

When you are not happy with the choices provided to you above, when the PyAvrOCD binaries will not start because of incompatibilities, or when you have a compatible Python installation that you do not want to duplicate, it is also possible to install PyAvrOCD from [PyPI, the Python Package Index](https://pypi.org). The preferred way of doing that is using [pipx](https://pipx.pypa.io/stable/), which will install an executable in the folder `~/.local/bin/` and a virtual Python environment with all the required modules in `~/.local/pipx/`. Although this is, in theory, platform agnostic, you may encounter problems when USB and HIDAPI libraries have to be built from source. Note that Linux users need to install `udev` rules (see above).

Assuming that you have been successful in installing PyAvrOCD using pipx, we also want to download SVD files that we will need during our IDE debugging sessions. Create the folder `pyavrocd-util` in the folder `~/.local/bin` , download the SVD archive into it, and extract the folder:

```sh
> cd ~/.local/bin
> mkdir pyavrocd-util
> cd pyavrocd-util
> wget https://github.com/felias-fogg/PyAvrOCD/releases/latest/download/svd.tar.gz -O svd.tar.gz
> tar xvzf svd.tar.gz
```

### Step 2: Replace the outdated avr-gdb client

The avr-gdb client in the AVR toolchain, as delivered by PlatformIO, is seriously outdated (version 7.8 from 2014). Even worse, under recent versions of macOS and Ubuntu, it will not start because of incompatibilities. For this reason, it makes sense to employ a more recent version of avr-gdb. Either use the one obtainable from your OS or make use of the binary downloaded in [Step 1](#step-1-installing-pyavrocd). The folder you need to copy the client to is `~/.platformio/packages/toolchain-atmelavr/bin`:

```sh
cp ~/.local/bin/avr-gdb .platformio/packages/toolchain-atmelavr/bin/
```

