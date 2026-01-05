# PyAvrOCD installation & configuration

Both the installation and configuration of PyAvrOCD are straightforward on Windows, macOS, and Linux machines (see [supported platforms](supported-platforms.md)). Mac and Linux users should be aware of some idiosyncrasies, however.

!!! info "Linux"
    On a Linux installation, users may need to add a few `udev` rules after having installed PyAvrOCD. Download [https://pyavrocd.io/99-edbg-debuggers.rules](https://pyavrocd.io/99-edbg-debuggers.rules), edit if you want, and copy to `/etc/udev/rules.d/`.

!!! warning "macOS"
    On a Mac, files downloaded through a browser or from an email are marked as potentially dangerous, and the system may not allow them to be executed. In this case, use the command `xattr -d com.apple.quarantine FILE` in a terminal window to remove the extended attribute `com.apple.quarantine` from the binary executable FILE. After that, you can start the executable without a hitch.

## Installation
{!../INSTALL.md!lines=2-60}

## Configuration

{!configuration.md!lines=2-999}
