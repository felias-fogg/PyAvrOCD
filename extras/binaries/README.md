# Binaries for avrocd-tools

The binaries in this folder provide debug support for AVR chips to be used in the Arduino IDE 2. For each host architecture, there is an avr-gdb program, a simavr program, and a  PyAvrOCD server. The avr-gdb programs have version 17.2.3 and have been generated using the `avr-gdb-build.sh` script in the [avr-gdb repo](https://github.com/felias-fogg/avr-gdb).

PyAvrOCD is generated using PyInstaller on GitHub runners:

- **Apple (x86_64)**: macOS 14 / Python 3.14, libusb 1.0.29
- **Apple (ARM64)**: macOS 14 / Python 3.14, libusb 1.0.29
- **Linux (x86_64)**: Ubuntu 22.04 / Python 3.12
- **Linux (i686)**: Debian 12 (Bookworm) in a 32-bit container on an x86_64 runner, Python 3.11
- **Linux (ARM64)**: Ubuntu 22.04 / Python 3.12
- **Linux (armv6l)**: Raspi OS 5 (Bookworm), Python 3.11
- **Windows (x86_64)**: Windows 10 (2022) / Python 3.14
- **Windows (i686)**: Windows 10 (2022) / Python 3.14, architecture: x86

## simavr

The simavr programs come from the release workflow of the
[simavr fork](https://github.com/felias-fogg/simavr), which builds every
platform from the same sources and, for each one, measures afterwards what the
result demands of the system it will run on. Those floors are the reason the
build hosts are pinned rather than set to `latest`: on Linux the GLIBC version
of the build machine becomes the user's requirement.

- **Apple (x86_64)**: macos-15-intel, `MACOSX_DEPLOYMENT_TARGET=10.15` -> macOS 10.15
- **Apple (ARM64)**: macos-15, `MACOSX_DEPLOYMENT_TARGET=11.0` -> macOS 11.0
- **Linux (x86_64)**: Ubuntu 22.04 -> GLIBC 2.34
- **Linux (i686)**: Ubuntu 22.04, i386 packages -> GLIBC 2.34
- **Linux (ARM64)**: Raspberry Pi OS arm64, image 2023-05-03 -> GLIBC 2.17
- **Linux (armv6l)**: Raspberry Pi OS, image 2023-05-03 -> GLIBC 2.28, ARMv6 and hard float, so the Pi 1 and Zero are included
- **Windows (x86_64)**: MSYS2 UCRT64 -> Windows 10, because the Universal CRT is part of it
- **Windows (i686)**: MSYS2 MINGW32 -> the old `msvcrt.dll`, so no Windows 10 requirement

The full table, including what the archives contain and how to measure a floor
by hand, is in `requirements.md` in the simavr repository.

Only the files needed at run time are kept here: `bin/` plus the versioned
`.so.1` libraries beside it. On Linux `bin/simavr` finds them through an RPATH
of `$ORIGIN/../lib`, and each bundled library carries its own `$ORIGIN`, because
an RPATH applies to the object that holds it and is not inherited. `libelf` and
`libz` are part of that set; apart from the C library, nothing has to be
installed. On macOS and Windows both are linked statically, so the executable
stands alone. The development files -- headers, the static library, the
pkg-config files -- are deliberately not here; they are in the release archives,
and packer.sh would drop them from the tool package anyway.

## The i686 Linux client

It used to be built on a Debian virtual machine at home and committed into this
folder by hand. It is built in the release workflow now, like every other one.
PyInstaller cannot cross-compile -- it packs the interpreter it is running
under -- and GitHub has no 32-bit Linux runner, but an x86_64 runner executes
i386 code natively, so a 32-bit Debian container does the job without QEMU.
Debian rather than Ubuntu, because Ubuntu has no `python3` for i386 any more.

The script that used to start that build is gone with it. What is left of it is
`extras/release.sh`, which checks what can be checked at home -- on `main`,
nothing uncommitted, nothing unpushed, the version stated where it belongs --
and then pushes the tag that starts the release.