# Release Notes

## Release v0.19.0

- From this version on, dw-link (if used) is required to send its version number and it will be required to honor the monitor option value commands and the fuse bit manage requests.

- It is now possible to specify a `--dw-link-baud` option (for, e.g., the Xplained boards)

- The `ArduinoCore-avr (1.8.6)` fork has been removed to avoid confusion.

## Release v0.18.1

- Fixed a few `simavr` integration problems.

## Release v0.18.0

- `simavr` has been added to the binary tools. With that, one can now start the simulator by using the "virtual programmer" simavr when starting the debugging process.

## Release v0.17.1

- From now on, releases will also contain a working 32-bit package for Windows.

## Release v0.17.0

- The use of the simulator `simavr` is now supported. If this program is specified with the `-s` option, then the simulator is started with the right options, and no hardware probe will be used. Note that the current version of simavr (1.7) will not work. You can build simavr from source from the main branch of the current repo, however.
- New option `-F` for specifying the CPU clock frequency (in the same way as when specifying it in the compilation process). It will be used to derive a default value for the JTAG debugging frequency and to pass it on to `simavr` if used.

## Release v0.16.5

- The SVD files have been re-generated in order to remove FUSEs and LOCKBITs and add SREG and SP (that was a regression).
- New option value for `monitor load`: `onlycache`. This is helpful when dealing with the Xplained Mini boards. It will load the GDB server cache only instead of flashing the MCU memory. Of course, this only makes sense if you are sure that the program has already been loaded into flash memory. It is not a default setting. You have to activate it by supplying a `pyavrocd.option` file.
- Added three debug-enabled cores: ArduinoCore-avr (1.8.6), ATTinyCore (2.0.0), and Atmel Xplained Mini.

## Release v0.16.4

- On an ATmega328P XPlained Mini, I sometimes got errors when activating the physical interface: "AVR8_FAILURE_CLOCK_ERROR: Failure when increasing communication clock rate". If this error occurs, we now simply retry. This appears to work smoothly.
- Captured "Cannot open HID" exception when trying to connect to a busy debug probe.

- Instead of ignoring SLEEP instructions when single-stepping, we now do "sleep walking", i.e., use the hardware breakpoint to wait for a wake-up after the SLEEP instruction.

- Integration tests now also work for non-Arduino MCUs.

## Release v0.16.3

- Refreshed svd and device files.
- Svd files are now distributed as part of `pyavrocd-util` folder.

## Release v0.16.2

- The assets files names now also contain the PyAvrOCD version number.
- For the ATmega128, the breakpoint mode is now hardware-only and cannot be changed.


## Release v0.16.0

- The tool files are now only distributed as assets in the GitHub release. This means for the Arduino board packages that the tools files needs to be sourced from a new place.

## Release v0.15.0

This is considered a pre-release in order to give people a chance to play around with PyAvrOCD. The following things have changed since the last release of dw-gdbserver:

- Support for JTAG debugging has been added.
- A number of command-line options have been added, and one option has been removed:
    -   `--debug-clock` for setting the JTAG clock frequency for debugging
    -   `--prog-clock` for setting the JTAG clock frequency for programming
    -   `--manage` in order to specify which fuses and lock bits should be managed by the GDB server
    -   and all `monitor` settings can now be done at the command-line, e.g., `--timers freeze`.
    -   In addition, you can set options in the file `pyavrocd.options` that will override the options on the command line.
    -   Using the notation `@file.ext`, any arguments in the file `file.ext` will be spliced into  the command line.
    -   The option `-g`/`--gede` has been removed since the effect of this option can be achieved with the `-s` option.
- A few monitor commands have been added or modified:
    -   `atexit`: With this option, one can control whether the debugWIRE mode will be left when the debugging session is terminated.
    -   `erasebeforeload`: With this option, one can control whether flash memory is completely erased before a file is loaded.
     -   Some defaults have been adapted, e.g., `readbeforewrite` is only enabled for debugWIRE targets, because for other targets it is counter-productive.
- The breakpoint management has been redesigned and can now deal with multiple hardware breakpoints (as offered by the JTAG targets).
- Single-stepping has been reworked so that no hardware breakpoint is needed any longer.
- The problematic ATmega48 and 88 are now recognized before an attempt is made to switch them into debugWIRE mode. This helps to avoid "bricking" chips.
- The CI/CD has been enhanced so that we can now see a number of indicators in real-time.
- Executables are now generated on the GitHub hosts, which makes my life much easier.
-  The documentation now uses mkdocs and the readthedocs theme, which looks much better and is more readable, I believe.
