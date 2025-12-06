# Invoking PyAvrOCD

In a terminal window, you invoke PyAvrOCD as follows:

```
> pyavrocd [options]
```

PyAvrOCD will then look for a debug probe, establish a connection to it, and wait for the GDB debugger to connect to it. You can influence its behavior with the command-line options shown below.

If you are using an IDE, then the IDE will invoke the GDB server. Nevertheless, the command line options may be interesting to you because you may want to change some of them using a [configuration file](install-link.md#configuration).

| Option&nbsp;Name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `--help`<br/> `-h`                                           | Gives help text and exits.                                   |
| `--command`<br>`-c`                                          | Command to set the gdb port (OpenOCD style), which is used in the Arduino IDE 2. This is an alternative to the `--port` option. |
| `--device` <br>`-d`                                          | The argument to this option specifies the MCU type of the target chip in lower case.  This option is mandatory. If a '?' mark is given, all supported MCUs are listed. |
| `--debug-clock`<br>`-D`                                      | JTAG clock frequency for debugging in kHz. This value should be less than a quarter of the MCU clock frequency. The default is min(2000, `F_CPU`/5000) in kHz. |
| `--F_CPU`<br>`-F`                                            | Frequency of CPU clock (Hz). It is used to determine the default value for `--debug-clock` and will be passed to `simavr` if called. The default is 1,000,000 Hz. |
| `--interface`<br>`-i`                                        | Debugging interface to use. Should be one of `debugwire`, `jtag`, `pdi`, or `updi`. Only necessary if an MCU supports more than one interface or if one wants to see only the supported chips with a particular interface. |
| `--manage`<br/>`-m`                                          | Can be given multiple times and specifies which fuses should be managed by PyAvrOCD. Possible arguments are `all`, `none`, `bootrst`, `nobootrst`,  `dwen`, `nodwen`, `ocden`, `noocden`, `eesave`, `noeesave`, `lockbits`, and `nolockbits`. Later values in the command line override earlier ones. Any fuses not managed by PyAvrOCD need to be changed 'manually' before and/or after the GDB server is activated. The default for this option is `none`, i.e., all fuses have to be dealt with by the user. Note that dw-link ignores this option. It will manage all fuses. |
| `--port` <br>`-p`                                            | IP port on the local host to which GDB can connect. The default is 2000. |
| `--prog-clock`<br>`-P`                                       | JTAG programming clock frequency in kHz. This is limited only by the target MCU silicon, not by the actual MCU clock frequency used. The default is (a conservative) 1000 kHz. |
| `--start` <br>`-s`                                           | Program to start in the background, e.g., a debugging GUI, such as `gede`. If the program name is `nop`, then no program is started. If the program name is `simavr`, then instead of connecting to a debug probe, `simavr` is started with the specified port (`-p`), MCU (`-d`), and CPU frequency (`-F`). |
| `--tool`<br>`-t`                                             | Specifying the debug tool. Possible values are `atmelice`, `edbg`, `jtagice3`, `medbg`, `nedbg`, `pickit4`, `powerdebugger`, `snap`, `dwlink`. Use of this option is necessary only if more than one debugging tool is connected to the computer. |
| `--usbsn` <br>`-u`                                           | USB serial number of the tool. This is only necessary if one has multiple debugging tools connected to the computer. |
| `--verbose` <br>`-v`                                         | Specify verbosity level. Possible values are `all`, `debug`, `info`, `warning`, `error`, or `critical`. The option value `all` means that, in addition to the `debug` output, all communication with GDB is logged. The default is `info`. |
| `--version` <br>`-V`                                         | Print PyAvrOCD version number and exit.                      |
| `--xargs`<br> `-x`                                           | Extra arguments for `simavr`.                                |
| `--install-udev-rules`                                       | Install the udev rules necessary for Microchip's EDBG debuggers. Needs to be run with `sudo` and is only present under Linux. |

You can also use the [monitor command options](monitor-commands.md) as command-line options in order to set debugger values already at startup. For example, you may specify `--timers freeze,` which has the same effect as issuing the command `monitor timers freeze` in the debugger at startup. One-character abbreviations for such option values are possible, and with the usual abbreviation rules for options, one can shorten this to `--ti f` .

In addition to options, one can specify file names prefixed with a '@'-sign. Such files can contain additional arguments. Arguments read from such a file must be one per line and are treated as if they were in the same place as the original file referencing argument on the command line. If the file does not exist, no error is raised.

The argument `@pyavrocd.options` is always added to the end of the command line. In other words, if there is such a file in the folder where the GDB server is invoked, then the arguments in this file will have precedence over the arguments on the command line. This is the way to override options on a per-project basis in an IDE, where the IDE invokes the GDB server.



