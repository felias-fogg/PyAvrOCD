# Credits

This project owes its success to the following people and organizations:

## Contributors

- [@maxgerhard](https://github.com/maxgerhardt)


## Third-party libraries & systems

- [pyedbglib](https://github.com/microchip-pic-avr-tools/pyedbglib): The low-level implementation of the EDBG protocol, which is the essential component to establish communication with EDBG debuggers.
- [pymcuprog](https://github.com/microchip-pic-avr-tools/pymcuprog): This package provides the base for the GDB server. Without it, I probably would have never started to write PyAvrOCD. Great job by Microchip to publish these two packages!
- [PyUSB](https://github.com/pyusb/pyusb): The essential library for communicating over USB.
- [PyInstaller](https://github.com/pyinstaller/pyinstaller): The package that can create executables from Python packages.
- [simavr](https://github.com/buserror/simavr): The AVR simulation package.
- [GDB](https://sourceware.org/gdb/): The GNU Project Debugger
- [MkDocs](https://github.com/mkdocs/mkdocs): Generates gorgeous online documentation.

## Financial support

This project did not receive any financial support. And, currently, there is no need for it. If you want to support it, please consider donating MCUs or boards that have not been tested yet (see [supported MCUs](https://felias-fogg.github.io/PyAvrOCD/supported-mcus/) and [boards](https://felias-fogg.github.io/PyAvrOCD/supported-boards/)).

## Special thanks

Without the effort of the Arduino community, I would not have started to work on the GDB server. So thanks go to:

- The [**Arduino**](https://www.arduino.cc) project: for obvious reasons.
- [@MCUdude](https://github.com/MCUdude): For creating the cool additional cores for ATmegas, and for incorporating PyAvrOCD into it.
- [@SpenceKonde](https://github.com/SpenceKonde) (aka Dr. Azzy): For creating the great additional cores for ATtinys and the awesome DxCore.
- And many more ...

I built PyAvrOCD on top of two earlier implementations of Python AVR GDB servers:

- [pyAVRdbg](https://github.com/stemnic/pyAVRdbg) by [@stemic](https://github.com/stemnic)
- [pyavrdebug](https://github.com/mraardvark/pyavrdebug) by [@mraadvark](https://github.com/mraardvark)

Both of them worked as an inspiration and as a first scaffold for setting up my server.

## License

This project is licensed under the [MIT license](https://felias-fogg.github.io/PyAvrOCD/license-link/).

## Acknowledgments

- [@jdolinay](https://github.com/jdolinay), who drew my interest to debugging AVRs with his [avr_debug](https://github.com/jdolinay/avr_debug) GDB stub.
- [@xedbg](https://github.com/xedbg) for patiently answering questions about pymcuprog and the EDBG protocol in general.

### Closing

This document is a way to publicly appreciate the contributions of those who have helped make this project what it is today. Thank you!

***Generated using [CREDITS Generator](https://scottgriv.github.io/CREDITS-Generator/).***
