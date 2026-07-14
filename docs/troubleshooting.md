# Troubleshooting

If things go not according to plan, a first good step is to have a look at the logging output of PyAvrOCD. If you spot a log entry marked `[CRITICAL]`, it may tell you already what went wrong.

In general, one can distinguish between problems that prohibit the start of the GDB server and problems appearing while debugging.

## Debugging does not start

For most of the error messages, it should be obvious what to do. However, there are a few messages that look cryptic, and/or a solution is not apparent.

### `Apple could not verify “...” is free of malware that may harm your Mac or compromise your privacy.`

This is an error message you may get under macOS. It happens when you download executables with a browser or from e-mail, which sets a particular extended attribute. You can remove this extended attribute from the file `FILE` as follows. Afterward, macOS will start these executables without any problems.


```bash
$ xattr -d com.apple.quarantine FILE
```

### `No compatible tool discovered`

This could mean that no debug tool is connected, that you specified an incompatible debug probe using the `--tool` option, that the serial line the tool is attached to is busy, or that [you have not yet installed the necessary udev rules under Linux](install.md).

### `[Errno 48] Address already in use`

This error can happen after the GDB server was terminated before the debugger. If you are working in a CLI environment, you can start PyAvrOCD with a different port using the `--port` option and tell GDB about the port when connecting with the `target remote` command. However, waiting a few minutes will also resolve the problem.

### `ISP programming failed. Wrong connection or wrong MCU?`

This error message is displayed when, on a debugWIRE target, the DWEN fuse cannot be set because ISP/SPI programming cannot be initiated. It could be a wiring problem, which, in my experience, is the most likely reason. It could also mean that the MCU is not accessible anymore by ISP programming, which can have [many possible causes](limitations.md#debugwire-can-brick-mcus).

### `Debug session not started: debugWIRE not activated by power-cycling. Parasitic power supply?`

DebugWIRE was not activated despite (automatic) power-cycling. Perhaps there is a [parasitic power supply](https://arduino-craft-corner.de/index.php/2022/03/15/parasitic-power-supply/) problem? This happens in particular on Xplained-Mini boards since the board power is not switched when an automatic power cycle is performed. A cure can be to power the application circuit connected to the board through the `IOREF` pin instead of using the `5V`  or `3.3V` pin. If this is not possible, consult the [README file](https://github.com/felias-fogg/XMiniCore#powering-external-circuitry) of XMiniCore.

## Problems while debugging

### Code executes slower or faster than expected

Note that PyAvrOCD by itself does not set any timing-related fuses (`CKDIV8` on classic chips or `FREQSEL` on modern chips). This means before debugging, you need to run `Burn Bootloader` in the Arduino IDE 2 after selecting the right clock settings, or you have to set the timing-related fuses to their desired values by other means.

### Loading code and/or debugging feels sluggish

When using *debugWIRE*, the communication speed is severely limited from the beginning. With Atmel-ICE, the upload speed is roughly one kByte/sec; with the Xplained-Mini boards, it is 0.3 kBytes/sec.  Using the `readbeforewrite` option (which is the default), subsequent uploads may be faster. If the MCU clock frequency is lower than 16 MHz, the upload speed is even slower, and below a clock frequency of 1 MHz, it is no fun at all. Similarly, debugging operations are also somewhat slow.

With *JTAG* and *UPDI* targets, this problem should not happen. For JTAG, the default speed is 1 MHz for programming (`--prog-clock`) and 200 kHz for debugging (`--debug-clock`). However, you can request higher values when starting PyAvrOCD. Programming speed is only limited by the MCU's maximal frequency (and the wiring). Debugging speed should be no more than a quarter of the actual clock frequency of the target MCU. UPDI communication speed is set to 750 kb/s by default (`--comm-speed`). On Dx and Ex series chips, speeds up to 1800 kb/s are possible.  [Refrain from setting speed to 400 kb/s or less](#no-stop).

### The debugger does not stop at a line with a set breakpoint

This happens when the line marked to be stopped at does not contain any machine code. The problem gets worse when the switch `Optimize for Debugging` in the Arduino IDE 2 is not activated or, if you are working in a CLI environment, you did not use the `-Og` compiler option.

<a id=no-stop></a>

### The debugger does not stop at all although only a single-step was requested or it definitely should have stopped at the next breakpoint.

Such behavior could be caused the UPDI communication speed being too slow. I experienced breakpoint and single-step skidding when the UPDI communication speed was too low, e.g., 400 kbps or less when the MCU ran at 16 MHz. And this may lead to missing a breakpoint or stepping too far. Another possible cause is the [`-mrelax` optimization](compilation-options.md#critical-optimization-options) option (see below).

### The debugger seems to be confused about the line where it stopped

If the debugger stopped at a line, but from other evidence it is clear that the program flow is somewhere else, it could be that the [`-mrelax` optimization](compilation-options.md#critical-optimization-options) option had been used, which distorts the line numbering information. Compile and link without this option!

### When single-stepping, execution jumps around

Probably the one of the reasons mentioned above (no `-Og` option set, `-mrelax` set, or UPDI communication speed too low).

### Single-stepping takes forever

You requested a single step, and the debugger seems to take forever to complete this single step. There are a few possible causes. First, when single-stepping a SLEEP instruction, the MCU will go into sleep mode. Second, [single-steping a source code line that contains an (implicit) loop](limitations.md#single-stepping-lines-containing-loops) can lead to a severe slowdown.  Third, this could also be caused by the phenomenon mentioned above (low UPDI communication speed leading to single-step skidding). Fourth, it could be caused by the `-mrelax` option (see above).

In all cases, simply stop with Ctrl-C (or the equivalent on the IDE level), set a breakpoint where you want to stop next, and continue execution.

### Variables cannot be accessed in the debugger

Again, this might be because you forgot to activate the optimization option for debugging. Or, it can be that the compiler has optimized away your variable. If you really are in need to inspect and maybe change the variable. you can declare it as `volatile`. Then it will always be visible when in scope. However, handling of it is rather inefficient.

### Global variables are not listed in the `Global variables` section

The LTO linker optimization does that to you. However, you still can inspect variables by hovering over them or requesting to display them in the `Watch` pane. You can set the value of variables by using the `set var <variable>=<value>` GDB command, which you can type in the last line of the `Debug Console` window.

### The values of a local variable cannot be changed, or a wrong value is displayed in the debugger

This [happened to me recently](https://gist.github.com/felias-fogg/8f4e1fdb3be14a598467842b03a3aef9). The culprit is avr-gcc (version 7.3.0 as distributed with the Arduino IDE). The only way around it is mentioned above. Declare the variable as `volatile`.

### Backtraces are distorted

This sometimes happens when AVR-GDB is not able to figure out the stack frame. I am working on it.

## Problems after Debugging

### After debugging, the MCU does not seem to execute the stored program, but acts funny

Usually, after having finished debugging, the MCU is released, and the uploaded program will continue to execute. However, if the [debugging session has ended abruptly](limitations.md#unsafe-exits-from-debugging), e.g., by disconnecting power, the debugger did not get a chance to replace the software breakpoints with the original instructions. In this case, the MCU may act strangely. The cure is to simply reflash the MCU.

### After debugging, it is impossible to flash a new program using a programmer

 When you deal with a debugWIRE target, note that the debugWIRE mode is only left when the command `monitor debugwire disable` has been typed into the GDB command line before ending the debug session. When you are still in debugWIRE mode, you cannot use SPI programming! You first need to [exit debugwire mode](limitations.md#exit-debugwire-mode). Note also that debugging a debugWIRE target can have [adverse effects](limitations.md#debugwire-can-brick-mcus).

It is also possible that you locked yourself out by setting the wrong fuses (this applies to JTAG and UPDI targets as well).

### After debugging, it is impossible to upload a new program using the bootloader.

Usually, the bootloader is erased before debugging starts. This means that you have to [reflash the bootloader and maybe change some fuses after debugging](restore-original-state.md).



## Signals and error messages

{!signals_and_errors.md!}

## Internal and fatal dw-link errors

When using the dw-link debug probe, internal errors are reported directly by the dw-link firmware.

If the LED blinks furiously (0.1 seconds on/ 0.1 seconds off), then the debug server has hit an unrecoverable error. This might not be immediately reported by GDB, but one can get information about the specific error by using the `monitor info` command. The errors are only reported by number. {!../../dw-link/docs/internal_errors.md!}

## Reporting bugs

If the problematic behavior you have encountered looks like a bug, please send an issue report as described in the [section on contributing](contributing.md#reporting-an-issue).
