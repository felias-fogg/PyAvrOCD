# Invoking pyavrocd

You invoke pyavrocd as follows:
```
> pyavrocd [options]
```

Pyavrocd will then look for a hardware debugger, establish a connection to it, and waits for the GDB debugger to connect to it. You can influence its behavior by the following command-line options.

| Option&nbsp;Name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `--command`<br>`-c`                                          | Command to set the gdb port (OpenOCD style), which is used in the Arduino IDE 2. This is an alternative to the `--port` option. |
| `--device` <br>`-d`                                          | The argument to this option specifies the MCU type of the target chip in lower case.  This option is mandatory. If a '?' mark is given, all supported MCUs are listed. |
| `--debug-clock`<br>`-D`                                      | JTAG clock frequency for debugging (kHz). This value should be less than a quarter of the MCU clock frequency. The default is (a conservative) 200 kHz. |
| `--help`<br> `-h`                                            | Gives help text and exits.                                   |
| `--interface`<br>`-i`                                        | Debugging interface to use. Should be one of `debugwire`, `jtag`, `pdi`, or `updi`. Only necessary if an MCU supports more than one interface or if one wants to see only the supported chips with a particular interface. |
| `--manage`<br/>`-m`                                          | Can be given multiple times and specifies which fuses should be managed by pyavrocd. Possible arguments are `all`, `none`, `bootrst`, `nobootrst`,  `dwen`, `nodwen`, `ocden`, `noocden`, `eesave`, `noeesave`, `lockbits`, and `nolockbits`. Later values in the command line override earlier ones. Any fuses not managed by pyavrocd need to be changed 'manually' before and/or after the GDB server is activated. Note that dw-link ignores this option! |
| `--port` <br>`-p`                                            | IP port on the local host to which GDB can connect. The default is 2000. |
| `--prog-clock`<br>`-P`                                         | JTAG programming clock frequency in kHz. This is limited only by the target MCU silicon, not by the actual MCU clock frequency used. The default is (a conservative) 1000 kHz. |
| `--start` <br>`-s`                                           | Program to start or the string `noop`, when no program should be started |
| `--tool`<br>`-t`                                             | Specifying the debug tool. Possible values are `atmelice`, `edbg`, `jtagice3`, `medbg`, `nedbg`, `pickit4`, `powerdebugger`, `snap`, `dwlink`. Use of this option is necessary only if more than one debugging tool is connected to the computer. |
| `--usbsn` <br>`-u`                                           | USB serial number of the tool. This is only necessary if one has multiple debugging tools connected to the computer. |
| `--verbose` <br>`-v`                                         | Specify verbosity level. Possible values are `all`, `debug`, `info`, `warning`, `error`, or `critical`. The default is `info`. The option value `all` means that, in addition to the debug output, all communication with GDB is logged. |
| `--version` <br>`-V`                                         | Print pyavrocd version number and exit.                      |
| `--install-udev-rules`                                       | Install the udev rules necessary for Microchip's EDBG debuggers. Needs to be run with `sudo` and is only present under Linux. |

You can also use the [monitor command options](monitor-commands.md) as command-line options in order to set debugger values already at startup. For example, you may specify `--timers freeze,` which has the same effect as issuing the command `monitor timers freeze` in the debugger at startup. You can also use one-character abbreviations for such option values and the usual abbreviation rules for options, shortening it to `--ti f` .

In addition to options, one can specify file names prefixed with a '@'-sign. Such files can contain additional arguments. Arguments read from such a file must be one per line and are treated as if they were in the same place as the original file referencing argument on the command line. If the file does not exist, no error is raised.

The argument `@pyavrocd.options` is always added to the command line. In other words, if there is such a file in the folder where the GDB server is invoked, then the arguments in this file will override the command line. This is the way to override options on a per-project basis in an IDE, where the IDE invokes the GDB server.


