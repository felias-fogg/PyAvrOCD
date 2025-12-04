Sometimes, GDB commands fail, often showing a signal that has been received, an error code, and/or an error message. The following is a list of those. When using dw-link, error messages might be brief or missing.

| Signal or error code | Error message                                                | Explanation                                                  |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `SIGHUP`             | *Enable debugWIRE first: 'monitor debugwire enable*<br>or<br>*JTAG pins are not enabled*<br>or something similar | If the debugger receives this signal, it means that there is no connection to the target's OCD. You need to enable debugging by setting a fuse or something similar, perhaps by issuing `monitor debugwire enable`. |
| `SIGINT`             |                                                              | This is not an error signal. It rather signals that execution has been stopped by a keyboard interrupt (or something equivalent). |
| `SIGILL`             | *Cannot execute because of  BREAK instruction*               | The debugger receives this signal when one tries to single-step or continue executing at a location where the user has placed a BREAK instruction. Alternatively, the BREAK instruction might be a leftover from a previously interrupted debugging session. |
| `SIGTRAP`            |                                                              | This is not an error signal. Instead, it is issued when execution stops at a place where a breakpoint has been set. |
| `SIGABRT`            | See debug server log                                         | This signal is raised after an unrecoverable internal error or when execution shall be continued after such an error. Use the `monitor info` to get more information about the error. |
| `SIGBUS`             | *Cannot execute because stack pointer is too low*            | This signal is raised if the stack threatens to overwrite I/O registers when execution is about to start. |
| `SIGSEGV`            | *No program loaded; cannot start execution*                  | This signal is raised when execution is about to start, but there is no prior `load` command.  If this is done intentionally (because it is known that the flash memory has been programmed), one can  disable the check by using the command `monitor onlywhenloaded disable`. |
| `SISGSYS`            | *Too many breakpoints set*                                   | Execution cannot continue because too many breakpoints have been set. You need to delete some in order to continue execution. |
| `E01`                |                                                              | Error code returned when attempting to read or write memory contents while there is no connection to the OCD. |
| `E04`                |                                                              | Error signaling that GDB requested a packet longer than the communicated maximal size. |
| `E11`                |                                                              | Error code returned when writing to flash memory was unsuccessful. |
| `E13`                |                                                              | Error code when writing to memory failed.                    |
| `E14`                |                                                              | Error code for a read memory failure.                        |
| `E15`                |                                                              | Error code when GDB sent a data package with the wrong size. |

