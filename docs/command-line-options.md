# Invoking PyAvrOCD

In a terminal window, you invoke PyAvrOCD as follows, whereby the only mandatory option is the `-d` or `--device` option, specifying the MCU:

```
> pyavrocd [options]
```

PyAvrOCD will then look for a debug probe, establish a connection to it, and wait for the GDB debugger to connect to it. You can influence its behavior with the command-line options shown below.

If you are using an IDE, then the IDE will invoke the GDB server. Nevertheless, the command line options may be interesting to you because you may want to change some of them using a [configuration file](#providing-command-line-options-in-configuration-files).

## Command-line options

| Option&nbsp;Name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `--help`<br/> `-h`                                           | Gives help text and exits.                                   |
| `--webhelp`<br/>`-H`                                         | Opens web page with help text.                               |
| `--attach`<br/>`-a`                                          | Connect to the target without a `RESET`. This works only if the debugging mode has been activated in a previous session and not terminated when leaving the debugger. This means you need to have terminated the previous session with `monitor atexit stay` (default with debugWIRE). |
| `-c`                                                         | Command to set the gdb port (OpenOCD style), which is employed in the Arduino IDE 2 debugging interface by using. e.g., `-c "gdb_port 50000"`. This is an alternative to using the `--port` option. |
| `--comm-speed`<br>`-C`                                       | Communication speed for (U)PDI in kbps (default 750). Note that values that are too low may lead to erroneous behavior of the debugger. Safe values are apparently strictly higher than 400 kbps if the CPU clock is 16 MHz or higher. Use with care. |
| `--device` <br>`-d`                                          | The MCU type of the target chip.  This option is mandatory. If a '?' mark is given, all supported MCUs are listed. |
| `--elf-file`<br>`-e`                                         | ELF file containing the executable to be debugged. If the file is specified, it will be checked whether it has been compiled with the [`-mrelax` option](compilation-options.md#relax). If so, debugging is refused because the line-numbering debug information is, in this case, completely distorted. |
| `--debug-clock`<br>`-D`                                      | JTAG clock frequency for debugging in kHz. This value should be less than a quarter of the MCU clock frequency. The default is min(2000, `F_CPU`/5000) in kHz. |
| `-f`                                                         | OpenOCD command line option with one argument that is used by the Arduino IDE 2 debugging interface. It is ignored by PyAvrOCD. |
| `--F_CPU`<br>`-F`                                            | Frequency of CPU clock (Hz). It is used to determine the default value for `--debug-clock` and will be passed to `simavr` if called. The default is 1,000,000 Hz. |
| `--interface`<br>`-i`                                        | Debugging interface to use. Should be one of `debugwire`, `jtag`, `pdi`, or `updi`. Only necessary if an MCU supports more than one interface or if one wants to see only the supported chips with a particular interface. |
| `--manage`<br/>`-m`                                          | Can be given multiple times and specifies which fuses should be managed by PyAvrOCD. Possible arguments are `all`, `none`, `bootrst`, `nobootrst`,  `dwen`, `nodwen`, `ocden`, `noocden`, `eesave`, `noeesave`, `lockbits`, and `nolockbits`. Later values in the command line override earlier ones. Any fuses not managed by PyAvrOCD need to be changed 'manually' before and/or after the GDB server is activated. The default for this option is `none`, i.e., all fuses have to be dealt with by the user. |
| `--port` <br>`-p`                                            | IP port on the local host to which GDB can connect. The default is 2000. |
| `--prog-clock`<br>`-P`                                       | JTAG programming clock frequency in kHz. This is limited only by the target MCU silicon, not by the actual MCU clock frequency used. The default is (a conservative) 1000 kHz. |
| `--start` <br>`-s`                                           | Program to start in the background, e.g., a debugging GUI, such as `gede`. If the program name is `nop`, then no program is started. If the program name is `simavr`, then instead of connecting to a debug probe, `simavr` is started with the specified port (`-p`), MCU (`-d`), and CPU frequency (`-F`). |
| `--tool`<br>`-t`                                             | Specifying the debug tool. Possible values are `atmelice`, `edbg`, `jtagice3`, `medbg`, `nedbg`, `pickit4`, `powerdebugger`, `snap`, `dwlink`. Use of this option is necessary only if more than one debugging tool is connected to the computer. |
| `--usbsn` <br>`-u`                                           | USB serial number of the tool. This is only necessary if one has multiple debugging tools connected to the computer. |
| `--verbose` <br>`-v`                                         | Specify verbosity level. Possible values are `all`, `debug`, `info`, `warning`, `error`, or `critical`. The option value `all` means that, in addition to the `debug` output, all communication with GDB is logged. The default is `info`. |
| `--version` <br>`-V`                                         | Print PyAvrOCD version number and exit.                      |
| `--xargs`<br> `-x`                                           | Extra arguments for `simavr`.                                |
| `--reboot-debugger`                                          | Will reboot the debugger before starting the debug session. This can take up to 10 seconds on a PICkit4. |
| `--dw-link-baud`                                             | Communication speed for the serial line to dw-link, default is 115200. Needs only be specified if dw-link is compiled with a different value. |
| `--memory-map-disable`                                       | This option, which does not take a value, will disable the usage of the XML memory map. This option is only there for testing purposes. |
| `--skip-signature-verification`                              | Do not perform chip signature verification. This is another option for testing purposes. |

## Additional command-line options derived from monitor commands

You can also use the [monitor command options](monitor-commands.md) as command-line options when invoking PyAvrOCD. For example, you may specify `--verify enable,` which has the same effect as issuing the command `monitor verify enable` in the debugger after a connection to the GDB server has been established. One-character abbreviations for such option values are possible, and with the usual abbreviation rules for options, one can shorten this to `--veri e`.

## Providing command-line options in configuration files

If you place the string `@file.ext` on the command line, then arguments are read from `file.ext` and spliced into the command line. These arguments are read line by line.

<details>
<summary><b>Example</b></summary>
<p></p>
<p>
Let us assume, <code>file.ext</code> contains the following lines:
</p>
<pre>
<code class="language-bash hljs">--manage
eesave
--prog=3000
--to
atmelice
--veri=e</code>
</pre>
<p>
When you now invoke PyAvrOCD with <code>pyavrocd -d attiny13 -t dwlink @file.ext</code>,, then this is expanded into
</p>
<pre>
<code class="language-bash hljs">pyavrocd -d attiny13 -t dwlink --manage eesave --prog=3000 --to atmelice --veri=e</code>
</pre>
<p>
With the usual abbreviation rules, the fact that the equal sign can simply be substituted by space,  and the rule that later arguments override earlier ones, this is equivalent to
</p>
<pre>
<code class="language-bash hljs">pyavrocd --device attiny13 --manage eesave --prog-clock 3000 --tool atmelice --verify enable</code>
</pre>
</details>
<p></p>

Note that implicitly `@pyavrocd.options` is added to the end of the command line. This means that even if you cannot change the command line that invokes PyAvrOCD, because, e.g., PyAvrOCD is invoked by an IDE, you still can specify arguments that have precedence by using the configuration file `pyavrocd.options`.
