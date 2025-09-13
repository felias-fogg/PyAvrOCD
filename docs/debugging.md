# Debugging the target

## Debugging with a command-line interface

After compiling your program, e.g., varblink0.ino, you can start the GDB server and the GDB debugger. When calling the compiler, you should provide the following two options: `-Og` and `-ggdb3`. The first one optimizes for debugging (instead of size or speed), the second requires including as many symbols from the source program as possible.

When starting the GDB server from the command line, you need to specify the MCU you want to connect to. In addition, you should specify the option `-m all`, so that the GDB server manages the debug-related fuses (see [Preparing a target board](board-preparation.md#general-considerations)):

```
> pyavrocd -d atmega328p -m all
[INFO] Connecting to anything possible
[INFO] Connected to Atmel-ICE CMSIS-DAP
[INFO] Starting pyavrocd
[INFO] Looking for device atmega328p
[INFO] Listening on port 2000 for gdb connection

```

In another terminal window, you can now start a GDB session:

```
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

If you have reached this point, I trust that you are familiar with GDB and know how to proceed.

Note the request to power-cycle the target system, which will only appear when dealing with debugWIRE targets. You then need to disconnect and reconnect the power to the target. Afterward, debugWIRE mode is enabled, and you can debug. The debugWIRE mode will not be disabled when you leave the debugger! It will only be disabled when you issue the command `monitor debugwire disable`.  This means that until then, the RESET button will not be of any use; you cannot upload anything using SPI programming, nor can you change fuses. Since PyAvrOCD needs to delete the bootloader as well, you also cannot upload anything over the serial line.

## Debugging using the Arduino IDE 2

If you prefer to use an IDE instead of a CLI, the Arduino IDE 2 is the most straightforward option.

### Compiling the sketch

You must load the sketch into the editor and select a board as usual. If you want to debug an Arduino Uno R3 board, choose ATmega328 from the `MiniCore` in the `Tools` menu. Before you can debug your code, you need to compile it, which will be done when you click on the Verify button in the upper left corner of the Arduino IDE window (see below).

![ide2-1](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/ide2-1.png)

Before clicking the `Verify` button in the upper left corner, choose `Optimize for Debugging` in the `Sketch` menu. This is necessary so that the compiler optimizes the code in a way that makes debugging straightforward. Otherwise, the compiler may rearrange source code lines, which can be confusing when single-stepping through the code.

### Starting the debugger

After compiling the sketch, it is time to start debugging by clicking the debug button in the top row. This will start the debug server.

Instead of the message shown in the following screenshot, a warning "No hardware debugger discovered" may be displayed. The reason may be that the Arduino IDE 2 reserved the debugger's serial line for the `Serial Monitor`. Simply close the `Serial Monitor` console and try again. On Linux, another reason could be that the udev rules have not yet been installed (see [installation instructions](INSTALL.md#on-linux)). Or maybe you forgot to connect a hardware debugger altogether.

![ide2-2](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/ide2-2.png)

If there is a connection to the debugger and the target, the GDB server will start up. When you deal with a debugWIRE target, you may be asked to power-cycle the target, i.e., to disconnect and reconnect power to the target. As mentioned above, power cycling is only necessary once. The next time you start a debugging session, the MCU will already be in debugWIRE mode, and the debugger will not stop at this point.

After power-cycling the target, the debugger starts. Eventually, execution is stopped in line 4 at an initial internal breakpoint, indicated by the yellow triangle left of line 4 in the following screenshot. It may take some time before we reach that point, as the debugger must also load the program.

After stopping, the IDE rearranges the layout, showing the debugging panes on the left and the sketch on the right. It will also switch from displaying the `gdb-server` console to the `Debug Console`, which displays the output of the GDB debugger. In the last line of this console, a prompt symbol`>` is shown, where you can enter any GDB command, in particular the [`monitor` commands](monitor-commands.md) to control the GDB server. Here, the command `monitor debugwire disable` is crucial because it will disable the debugWIRE mode.

![ide2-3](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/ide2-3.png)

Now is a good time to familiarize yourself with the window's layout. The source code is on the right side. Below that is a console window, and to the left are the debug panes. To set a breakpoint, click to the left of the line numbers. Such breakpoints are displayed as red dots, such as those located to the left of lines 8 and 13.

### Debugging

![ide2-4](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/ide2-4.png)

The debugging panes are organized as follows. Pane A contains the debug controls. From left to right:

- *Reset*ting the device
- *Continue* execution or *pause*
- *Step over*: execute one source line
- *Step into*: execute stepping into the function, if in this line one is called
- *Step out*: finish the current function and stop after the line where it was called
- *Restart*: Same as Reset
- *Stop*: Terminate debugging

Pane B shows the active threads, but there is just one in our case. Pane C displays the call stack starting from the bottom, i.e., the current frame is the topmost. Pane D displays variable values. Unfortunately, global variables are not shown if *link-time optimizations* are enabled, which is the default. Pane E can be populated with watch expressions, for example, with the names of global variables.  Finally, in pane F, the active breakpoints are listed.

The panes below pane F are interesting if you are deep into the MCU hardware. The `CORTEX PERIPHERALS` pane displays all I/O registers of the MCU, decodes their meanings, and allows you to change the contents of these registers. The `CORTEX REGISTERS` pane displays the general registers. For more information on debugging, refer to the Arduino [debugging tutorial](https://docs.arduino.cc/software/ide-v2/tutorials/ide-v2-debugger/).

When you have decided to change the source code, remember to terminate the debugger (red square), then recompile the sketch using the upper left `Verify` button, and finally start another debugging session.

## Debugging using PlatformIO/VSC

Debugging a program/sketch in PlatformIO/VSC is very similar to doing the same thing in the Arduino IDE 2. The reason is that both IDEs are based on VS Code. Compared to the Arduino IDE 2, PlatformIO/VSC offers several features that work better, such as easy adaptability through the `platformio.ini` configuration file and support for disassembled code. However, it may not be the proper IDE for beginners. In any case, if you are opting for PlatformIO/VSC, you are probably familiar with the tool, and I do not need to preach to the converted. A `platform.ini`  that can be used to start the debugger is provided [here](debugging-software.md#platformio-and-visual-studio-code).

## Debugging using Gede

[Gede](https://github.com/jhn98032/gede) is a lean and clean GUI for GDB. It can be built and run on almost all Linux distros, FreeBSD, and macOS. You need an avr-gdb client with a version greater than or equal to 10.2. If you have installed Gede somewhere in your PATH, you can start Gede by specifying the option `--gede` or `-g` when starting PyAvrOCD.

![Gede](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/gede.png)

`Project dir` and `Program` are specific to your debugging session. The rest should be copied as it is shown. Before you click `OK`, you should switch to the `Commands` section, where you need to enter the command `monitor debugwire enable` if you are working with a debugWIRE target (otherwise it does not hurt).

![ ](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/gede-cmds.png)

Clicking on OK, you start a debugging session. The startup may take a while because the debugger always loads the object file into memory. After a while, you will see a window similar to what is shown below.

![Gede section](https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/gede-window.png)

