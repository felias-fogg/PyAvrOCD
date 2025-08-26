

# Command line options

When starting pyavrocd, you can influence its behavior with several command-line options.

| Option&nbsp;Name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `--command`<br>`-c`                                          | Command to set the gdb port (OpenOCD style), which is used in the Arduino IDE 2. This is an alternative to the `--port` option. |
| `--device` <br>`-d`                                          | The argument to this option specifies the MCU type of the target chip in lower case.  This option is mandatory. If a '?' mark is given, all supported MCUs are listed. |
| `--gede`<br>`-g`                                             | No argument for this option. This option will start the `Gede` debugger GUI. |
| `--interface`<br>`-i`                                        | Debugging interface to use. Should be one of `debugwire`, `jtag`, `pdi`, or `updi`. Only necessary if an MCU supports more than one interface or if one wants to see only the supported chips with a particular interface. |
| `--manage`<br/>`-m`                                          | Can be given multiple times and specifies which fuses should be managed by pyavrocd. Possible arguments are `all`, `none`, `bootrst`, `nobootrst`,  `dwen`, `nodwen`, `ocden`, `noocden`, `lockbits`, and `nolockbits`. Later values in the command line override earlier ones. Any fuses not managed by pyavrocd need to be changed 'manually' before and/or after the GDB server is activated. Note that dw-link ignores this option! |
| `--monitor`<br> `-M`                                         | Can be given multiple times and specifies default values for [monitor options](https://github.com/felias-fogg/pyavrocd/blob/main/docs/monitor-commands.md). These default values are given by using the first letter of the option and the first letter of the value separated by a colon. For instance, for setting the default for the `load` option to `readbeforewrite` use `-monitor l:r` .This option is currently ignored by dw-link. |
| `--port` <br>`-p`                                            | IP port on the local host to which GDB can connect. The default is 2000. |
| `--start` <br>`-s`                                           | Program to start or the string `noop`, when no program should be started |
| `--tool`<br>`-t`                                             | Specifying the debug tool. Possible values are `atmelice`, `edbg`, `jtagice3`, `medbg`, `nedbg`, `pickit4`, `powerdebugger`, `snap`, `dwlink`. Use of this option is necessary only if more than one debugging tool is connected to the computer. |
| `--usbsn` <br>`-u`                                           | USB serial number of the tool. This is only necessary if one has multiple debugging tools connected to the computer. |
| `--verbose` <br>`-v`                                         | Specify verbosity level. Possible values are `all`, `debug`, `info`, `warning`, `error`, or `critical`. The default is `info`.The option value `all` means that, in addition to the debug output, all communication with GDB is logged. |
| `--version` <br>`-V`                                         | Print pyavrocd version number and exit.                      |
| `--install-udev-rules`                                       | Install the udev rules necessary for Microchip's EDBG debuggers. Needs to be run with `sudo` and is only present under Linux. |

In addition to options, one can specify file names prefixed with a '@'-sign. Such files can contain additional arguments. Arguments read from such a file must be one per line and are treated as if they were in the same place as the original file referencing argument on the command line. If the file does not exist, no error is raised.

------

[<small><i>Back to pyavrocd README</i></small>](https://github.com/felias-fogg/pyavrocd/blob/main/README.md)

