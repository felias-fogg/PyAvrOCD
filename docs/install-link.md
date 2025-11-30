# PyAvrOCD installation & configuration

Both the installation and configuration of PyAvrOCD are straightforward on Windows, macOS, and Linux machines (see [supported platforms](supported-platforms.md)). Mac and Linux users should be aware of some idiosyncrasies, however.

!!! info "Linux"
    On a Linux installation, users may need to add a few `udev` rules after having installed PyAvrOCD. One can add these udev rules manually, following the instructions in the [pyedbglib README](https://github.com/microchip-pic-avr-tools/pyedbglib/blob/main/README.md#notes-for-linux-systems). Alternatively, wait until PyAvrOCD is started and cannot find a debug probe. Then it will tell you what to do.

!!! warning "macOS"
    On a Mac, files downloaded through a browser or from an email are marked as potentially dangerous, and the system may not allow them to be executed. In this case, use the command `xattr -d com.apple.quarantine FILE` in order to remove the extended attribute `com.apple.quarantine` from the binary executable FILE.

## Installation
{!../INSTALL.md!lines=2-60}

## Configuration

{!configuration.md!lines=2-999}
