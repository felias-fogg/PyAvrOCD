# Debugging on a target



## Debugging using the Arduino IDE 2

Before you start debugging, you first need to [compile the sketch](compilation-options.md#compiling-an-arduino-sketch-in-the-arduino-ide-2), preferably with the `Optimize for Debugging` option enabled.

### Simulating or connecting to a target

Instead of connecting to a target, it is also possible to run a simulator (for some MCU types). This is done by choosing `Simulator (simavr)` as the `Programmer` in the `Tools` menu.  When you request to start debugging (see below), the simulator is chosen instead of making a connection to the target board.

### Starting the debugger

After c[ompiling the sketch](compilation-options.md#compiling-an-arduino-sketch-in-the-arduino-ide-2), it is time to start debugging by clicking the debug button in the top row. This will start the GDB server.

Instead of the message shown in the following screenshot, an error message "No compatible tool" may be displayed. The reason may be that the Arduino IDE 2 reserved the debugger's serial line for the `Serial Monitor`. Simply close the `Serial Monitor` console and try again. On Linux, another reason could be that the udev rules have not yet been installed (see [installation instructions](install.md#installation)). Or maybe you forgot to connect a debug probe altogether.

![ide2-2](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/ide2-2.png)

If there is a connection to the debugger and the target, the GDB server will start up. When you deal with a debugWIRE target, you may be asked to power-cycle the target, i.e., to disconnect and reconnect power to the target. As mentioned above, power cycling is only necessary once. The next time you start a debugging session, the MCU will already be in debugWIRE mode, and the GDB server will not stop at this point.

After power-cycling the target, the symbolic debugger starts. Eventually, execution is stopped in the first line of the internal `main` function at an initial internal breakpoint, indicated by the yellow triangle (not on Windows) left of line 35 in the following screenshot. It may take some time before we reach that point, as the debugger must also load the program.

After stopping, the IDE rearranges the layout, showing the debugging panes on the left and the sketch and other relevant source files on the right. It will also switch from displaying the `gdb-server` console to the `Debug Console`, which displays the output of the GDB debugger. In the last line of this console, a prompt symbol`>` is shown, where you can enter any GDB command, in particular the [`monitor` commands](monitor-commands.md) to control the GDB server.

![ide2-3](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/ide2-3-new.png)

Now is a good time to familiarize yourself with the window's layout. The source code is on the right side. Below that is a console window, and to the left are the debug panes. To set a breakpoint, click to the left of the line numbers. Such breakpoints are displayed as red dots, such as those located to the left of lines 8 and 13 in the picture below.

![ide2-4](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/ide2-4.png)

### Debugging

The debugging panes are organized as follows (see picture above). Pane A contains the debug controls. From left to right:

- *Reset*ting the device
- *Continue* execution or *pause*
- *Step over*: execute one source line
- *Step into*: execute stepping into the function, if in this line one is called
- *Step out*: finish the current function and stop after the line where it was called
- *Restart*: Same as Reset
- *Stop*: Terminate debugging

Pane B shows the active threads, but there is just one in our case. Pane C displays the call stack starting from the bottom, i.e., the current frame is the topmost. Pane D displays variable values. Unfortunately, global variables are not shown if *link-time optimizations* are enabled, which is the default. Pane E can be populated with watch expressions, for example, with the names of global variables.  Finally, in pane F, the active breakpoints are listed.

The panes below pane F are interesting if you are deep into the MCU hardware. The `CORTEX PERIPHERALS` pane displays all I/O registers of the MCU, decodes their meanings, and allows you to change the contents of these registers. The `CORTEX REGISTERS` pane displays the general registers. For more information on debugging, refer to the Arduino [debugging tutorial](https://docs.arduino.cc/software/ide-v2/tutorials/ide-v2-debugger/).

### Correcting the bug and starting over

Let us assume you found the bug and made a correction in the source code. Note that it is not enough to `restart` or `reset` the device in order to try out the correction! This will only restart, but it will not compile and reload the program.  Instead, do the following:

1. Terminate debugging by clicking on the red square.
2. Click again on the `Verify` button to start a new compilation.
3. Restart the debugger by clicking on the `Debugging` button in the top line in order to try out your correction.

### Finishing the debug session

If everything now works out, you may consider calling it a day and stopping work on the program. If you were debugging on a debugWIRE target, consider typing the command `monitor debugwire disable` into the last line of the `Debug Console` before terminating the debugger.  This is necessary to bring the target chip back into normal mode, where it accepts SPI programming.

You may finally want to disable the `Optimize for Debugging` option in the `Sketch` menu. If you leave it enabled, then all future compilation actions will use this option and produce much larger code than necessary.

## Debugging using PlatformIO/VSC

Debugging a program/sketch in PlatformIO/VSC is very similar to doing the same thing in the Arduino IDE 2. The reason is that both IDEs are based on VS Code. Compared to the Arduino IDE 2, PlatformIO/VSC offers several features that work better, such as easy adaptability through the `platformio.ini` configuration file and support for disassembled code. However, it may not be the proper IDE for beginners.

In any case, if you are opting for PlatformIO/VSC, you are probably familiar with the tool, and I do not need to preach to the converted. The necessary  `platform.ini`  that can be used to integrate PyAvrOCD and to start the debugger is provided [here](debugging-software.md#platformio-and-visual-studio-code).

## Debugging using Gede

[Gede](https://github.com/jhn98032/gede) is a lean and clean GUI for GDB. It can be built and run on almost all Linux distros, FreeBSD, and macOS. You need an avr-gdb client with a version greater than or equal to 10.2. If you have installed Gede somewhere in your PATH, you can start Gede by specifying the option `--gede` or `-g` when starting PyAvrOCD.

![Gede](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/gede.png)

`Project dir` and `Program` are specific to your debugging session. The rest should be copied as it is shown. Before you click `OK`, you should switch to the `Commands` section, where you need to enter the command `monitor debugwire enable` if you are working with a debugWIRE target.

![ ](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/gede-cmds.png)

Clicking on OK, you start a debugging session. The startup may take a while because the debugger always loads the object file into memory. After a while, you will see a window similar to what is shown below.

![Gede section](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/gede-window.png)

## Debugging with a command-line interface

If you are more into command-line interface programming, simply using avr-gdb may be the right approach for you.

After [compiling your program](compilation-options.md#compiling-in-other-environments), e.g., varblink0.ino, you can start the GDB server and the GDB debugger. When starting the GDB server from the command line, you need to specify the MCU you want to connect to. In addition, you should specify the option `-m all`, so that the GDB server manages the debug-related fuses (see [Setting the right fuses](fuse-preparation.md#general-considerations)):

```log
> pyavrocd -d atmega328p -m all
[INFO] Connecting to anything possible
[INFO] Connected to Atmel-ICE CMSIS-DAP
[INFO] Starting pyavrocd
[INFO] Looking for device atmega328p
[INFO] Listening on port 2000 for gdb connection

```

In another terminal window, you can now start a GDB session:

```gdb
> avr-gdb varblink0.ino.elf
GNU gdb (GDB) 15.2
Copyright (C) 2024 Free Software Foundation, Inc.
...
(gdb) target remote :2000
Remote debugging using :2000
0x00000000 in __vectors ()
(gdb) monitor debugwire
debugWIRE mode is disabled
(gdb) monitor debugwire enable
*** Please power-cycle the target system ***
Ignoring packet error, continuing...
debugWIRE mode is enabled
(gdb) load
Loading section .text, size 0x596 lma 0x0
Start address 0x00000000, load size 1430
Transfer rate: 1 KB/sec, 1430 bytes/write.
(gdb) break loop
Breakpoint 1 at 0x470: file /Users/.../varblink0.ino, line 13.
Note: automatically using hardware breakpoints for read-only addresses.
(gdb) continue
...
```

In the above dialog, note the request to power-cycle the target system, which will only appear when dealing with debugWIRE targets. You then need to disconnect and reconnect the power to the target. Afterward, debugWIRE mode is enabled, and you can debug. The debugWIRE mode will not be disabled when you leave the debugger! It will only be disabled when you issue the command `monitor debugwire disable`.  This means that until then, the RESET button will not be of any use; you cannot upload anything using SPI programming, nor can you change fuses. Since PyAvrOCD needs to delete the bootloader as well, you also cannot upload anything over the serial line.

If you have reached this point, I trust that you are familiar with GDB and know how to proceed. I should point out one very convenient command, however: `monitor ioregister <ioreg-expression>` [`<int>`]. It will output the descriptions and contents of the I/O registers and/or bitfields that are referred to by `<ioreg-expression>`. This is a wildcard, case-insensitive expression over the names of the I/O registers and bitfields using the notation [`<peripheral>`.]`<register>`[`.<field>`]. If you specify an integer in addition, this will be used to set the value of the register or bitfield if uniquely described by `<ioreg-expression>`. This could look like as follows.

```
...
(gdb) monitor ioregister tc0.tc*
TC0.TCCR0A (@0x800044, 8-bits) = 0x3, 0b11, 3 (Timer/Counter  Control Register A)
TC0.TCCR0B (@0x800045, 8-bits) = 0x3, 0b11, 3 (Timer/Counter Control Register B)
TC0.TCNT0 (@0x800046, 8-bits) = 0x23, 0b100011, 35 (Timer/Counter0)
(gdb) monitor ioregister tccr0a
TC0.TCCR0A (@0x800044, 8-bits) = 0x3, 0b11, 3 (Timer/Counter  Control Register A)
TC0.TCCR0A.WGM0 (@0x800044[1:0]) = 0x3, 0b11, 3 (Waveform Generation Mode)
TC0.TCCR0A.COM0B (@0x800044[5:4]) = 0x0, 0b0, 0 (Compare Output Mode, Fast PWm)
TC0.TCCR0A.COM0A (@0x800044[7:6]) = 0x0, 0b0, 0 (Compare Output Mode, Phase Correct PWM Mode)
(gdb) mo io tccr0a.wgm0 1
TC0.TCCR0A.WGM0 = 1 (old value was: 3)
(gdb)
```



## Persistent Debugging

Most of the time, one-shot debugging will be enough to locate a problem. This means that you start the debugger, switch the MCU into debugging mode, upload the program, start it, and then try to find the bug. After you have located and fixed the bug, the MCU will then be brought into the normal mode again.

Sometimes, however, you may want to have a more persistent debugging scenario. If a bug shows up only after some time, you may want to leave the MCU running without the debug probe connected to it until the point that something goes wrong, and then *attach* to the MCU without going through the motion of setting fuses and resetting the MCU. This is supported by the monitor command `monitor atexit stay` and the command-line option `--attach`. With the mentioned monitor command, PyAvrOCD is instructed not to leave the debugging mode when the GDB server is terminated. When later PyAvrOCD is started with the command line option `--attach`, it will try to connect to the on-chip debugging module without setting any fuses and without a reset. If successful, you can then inspect the state of the program, change things, and continue execution.

Note that for UPDI targets, it is not necessary to use the `monitor atexit stay` command because UPDI targets do not have any special debug fuses. So, you can always attach.

