# Troubleshooting

Sometimes, things do not go according to plan, and it becomes necessary to debug the debugging setup. A first good step is to have a look at the logging output. If you spot a log entry marked `[CRITICAL]`, it may tell you already what went wrong. If you see, for example, the message

```text
[CRITICAL] Target is not powered
```

then it is very likely that you forgot to power the target board, or you made a wiring error.

In general, one can distinguish between problems that prohibit the start of the GDB server and problems appearing while debugging.

## Debugging does not start

For most of the error messages, it should be obvious what to do. However, there are a few messages that look cryptic, and/or a solution is not apparent.

* `Apple could not verify “...” is free of malware that may harm your Mac or compromise your privacy.`  This is an error message you may get under macOS. It happens when you download executables with a browser or from e-mail, which sets a particular extended attribute. You can remove this extended attribute from the file `FILE` as follows. Afterward, macOS will start these executables without a hitch.


```bash
> xattr -d com.apple.quarantine FILE
```

* `No compatible tool discovered`: This could mean that no debug tool is connected, that you specified an incompatible debug probe using the `--tool` option, that another process currently uses it, that the serial line the tool is attached to is busy, or that [you have not yet installed the necessary udev rules under Linux](install-link.md).

- `[Errno 48] Address already in use`: This error can happen after the GDB server was terminated before the debugger. If you are working in a CLI environment, you can start PyAvrOCD with a different port using the `--port` option and tell GDB about the port when connecting with the `target remote` command. However, waiting a few minutes will also resolve the problem.
- `ISP programming failed. Wrong connection or wrong MCU?` This error message is displayed when, on a debugWIRE target, the DWEN fuse cannot be set because ISP/SPI programming cannot be initiated. It could be a wiring problem, which, in my experience, is the most likely reason. It could also mean that the MCU is not accessible anymore by ISP programming. One can try to [forcefully exit debugWIRE mode](limitations.md#exit-debugwire-mode). Otherwise, [high-voltage programming](limitations.md#high-voltage-programming) might be the last resort.
- `Debug session not started: debugWIRE not activated by power-cycling. Parasitic power supply?` debugWIRE was not activated despite (automatic) power-cycling. Perhaps there is a [parasitic power supply](https://arduino-craft-corner.de/index.php/2022/03/15/parasitic-power-supply/) problem? This happens in particular on Xplained-Mini boards since the board power is not switched when an automatic power cycle is performed. A cure can be to power the application circuit connected to the board through the `IOREF` pin instead of using the `5V`  or `3.3V` pin.

## Problems while debugging

### Loading code and/or debugging feels sluggish

When using *debugWIRE*, the communication speed is severely limited from the beginning. With Atmel-ICE, the upload speed is roughly one kByte/sec; with the Xplained-Mini boards, it is 0.3 kBytes/sec.  Using the `readbeforewrite` option (which is the default), subsequent uploads may be faster. If the MCU clock frequency is lower than 16 MHz, upload speed is even slower, and below a clock frequency of 1 MHz, it is no fun at all. Similarly, debugging operations are also somewhat slow. With *JTAG*, the situation is much better. Default speed is 1 MHz for programming and 200 kHz for debugging. However, you can request higher values when starting PyAvrOCD. Programming speed is only limited by the MCU's maximal frequency (and the wiring). Debugging speed should be no more than a quarter of the actual clock frequency of the target MCU.

### The debugger does not stop at a line with a set breakpoint, but only later

This happens when the line marked to be stopped at does not contain any machine code. The problem gets worse when the switch `Optimize for Debugging` in the Arduino IDE 2 is not activated or, if you are working in a CLI environment, you did not use the `-Og` compiler option.

### Variables cannot be accessed in the debugger

Again, this might be because you forgot to activate the optimization option for debugging. Or, it can be that [link time optimization](limitations.md#link-time-optimization) has optimized away your variable.

### The values of a local variable cannot be changed, or a wrong value is displayed in the debugger

This [happened to me recently](https://gist.github.com/felias-fogg/8f4e1fdb3be14a598467842b03a3aef9). The culprit is avr-gcc (version 7.3.0 as distributed with the Arduino IDE). The only way to fix that is to use a more recent compiler version. If you have one at hand, together with the binary utilities, you can put a file `platform.local.txt` into the [platform folder](https://support.arduino.cc/hc/en-us/articles/4415103213714-Find-sketches-libraries-board-cores-and-other-files-on-your-computer#boards) of your core and write the line `compiler.path=/path/to/bin-folder/` into it.

## Signals and error messages

{!signals_and_errors.md!}

## Internal and fatal dw-link errors

When using the dw-link debug probe, internal errors are reported directly by the dw-link firmware.

If the LED blinks furiously (0.1 seconds on/ 0.1 seconds off), then the debug server has hit an unrecoverable error. This might not be immediately reported by GDB, but one can get information about the specific error by using the `monitor info` command. The errors are only reported by number. {!../../dw-link/docs/internal_errors.md!}
