# Release Notes



## Release v0.15.0

This is considered a pre-release in order to give people a chance to play around with PyAvrOCD. The following things have changed since the last release of dw-gdbserver:

- Support for JTAG debugging has been added, and one option has been removed:
- A number of command-line options have been added:
  - `--debug-clock` for setting the JTAG clock frequency for debugging
  - `--prog-clock` for setting the JTAG clock frequency for programming
  - `--manage` in order to specify which fuses and lock bits should be managed by the GDB server
  - and all `monitor` settings can now be done at the command-line, e.g., `--timers freeze`.
  - In addition, you can set options in the file `pyavrocd.options` that will override the options on the command line.
  - Using the notation `@file.ext`, any arguments in the file `file.ext` will be spliced into the command line.
  - The option `-g`/`--gede` has been removed since the effect of this option can be achieved with the `-s` option.
- A few monitor commands have been added or modified:
  - `atexit`: With this option, one can control whether the debugWIRE mode will be left when the debugging session is terminated.
  - `erasebeforeload`: With this option, one can control whether flash memory is completely erased before a file is loaded.
  - Some defaults have been adapted, e.g., `readbeforewrite` is only enabled for debugWIRE targets, because for other targets it is counter-productive.
- The breakpoint management has been redesigned and can now deal with multiple hardware breakpoints (as offered by the JTAG targets).
- Single-stepping has been reworked so that no hardware breakpoint is needed any longer.
- The problematic ATmega48 and 88 are now recognized before an attempt is made to switch them into debugWIRE mode. This helps to avoid "bricking" chips.
- The CI/CD has been enhanced so that we can now see a number of indicators in real-time.
- Executables are now generated on the GitHub hosts, which makes my life much easier.
-  The documentation now uses mkdocs and the readthedocs theme, which looks much better and is more readable, I believe.
