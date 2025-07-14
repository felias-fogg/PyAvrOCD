#  pyavrocd

This Python script serves as a gdbserver for almost all 8-bit AVR MCUs (currently only classic ATtinys and tinyMega MCUs).  It can communicate with Microchip debuggers such as [Atmel-ICE](https://www.microchip.com/en-us/development-tool/atatmel-ice) and [MPLAB SNAP](https://www.microchip.com/en-us/development-tool/pg164100) (in AVR mode), and provides a pass-through service for the DIY debugWIRE debugger [dw-link](https://github.com/felias-fogg/dw-link). For Microchip debuggers, the Python script uses the infrastructure provided by [pymcuprog](https://github.com/microchip-pic-avr-tools/pymcuprog) and [pyedgblib](https://github.com/microchip-pic-avr-tools/pyedbglib) to implement a full-blown gdbserver. With pyavrocd, you can utilize the debug interfaces integrated into IDEs such as Arduino IDE 2 or PlatformIO.

So, why another open-source gdbserver for AVR MCUs? The main intention behind it is to provide a gdbserver that is easily installable on Linux, macOS, and Windows. In addition, it provides some enhancements compared to its competitors, e.g., concerning [flash wear](https://arduino-craft-corner.de/index.php/2025/05/05/stop-and-go/) and [single-stepping](https://arduino-craft-corner.de/index.php/2025/03/19/interrupted-and-very-long-single-steps/).

## Table of Contents

- [1. Switching SNAP and PICkit4 to AVR mode](#1-switching-snap-and-pickit4-to-avr-mode)
- [2. Installation](#2-installation)
  * [2.1 Installation by downloading binaries](#21-installation-by-downloading-binaries)
  * [2.2 PyPI installation](#22-pypi-installation)
    + [2.2.1 Linux](#221-linux)
    + [2.2.2 Windows and macOS](#222-windows-and-macos)
  * [2.3 GitHub installation](#23-github-installation)
- [3. Usage](#3-usage)
  * [3.1 Compiling the program](#31-compiling-the-program)
  * [3.2 Preparing the target](#32-preparing-the-target)
  * [3.3 Starting a debug session](#33-starting-a-debug-session)
  * [3.4 Pyavrocd command line options](#34-pyavrocd-command-line-options)
  * [3.5 Monitor commands](#35-monitor-commands)
- [4. Integrated Development Environments and Graphical User Interfaces](#4-integrated-development-environments-and-graphical-user-interfaces)
  * [4.1 Arduino IDE 2](#41-arduino-ide-2)
  * [4.2 PlatformIO and Visual Studio Code](#42-platformio-and-visual-studio-code)
  * [4.3 Gede](#43-gede)
- [5. Prepapring a target for debugging and restoring the original state](#5-prepapring-a-target-for-debugging-and-restoring-the-original-state)
  * [5.1 Preparing a debugWIRE target](#51-preparing-a-debugwire-target)
    + [5.1.1 How to get into and out of debugWIRE mode](#511-how-to-get-into-and-out-of-debugwire-mode)
    + [5.1.2 Restoring an Arduino Uno R3 to its original state after debugging](#512-restoring-an-arduino-uno-r3-to-its-original-state-after-debugging)
  * [5.2 Preparing a JTAG target](#52-preparing-a-jtag-target)
  * [5.3 Preparing a PDI target](#53-preparing-a-pdi-target)
  * [5.4 Preparing a UPDI target](#54-preparing-a-updi-target)
- [6. Connecting the hardware debugger to a target](#6-connecting-the-hardware-debugger-to-a-target)
  * [6.1 Connecting a debugWIRE target](#61-connecting-a-debugwire-target)
    + [6.1.1 SPI programming header](#611-spi-programming-header)
    + [6.1.2 Connecting to targets with an SPI programming header](#612-connecting-to-targets-with-an-spi-programming-header)
    + [6.1.3 Connecting to targets without an SPI programming header](#613-connecting-to-targets-without-an-spi-programming-header)
    + [6.1.4 Powering the target board](#614-powering-the-target-board)
  * [6.2 Connecting a JTAG target](#62-connecting-a-jtag-target)
  * [6.3 Connecting a PDI target](#63-connecting-a-pdi-target)
  * [6.4 Connecting a UPDI target](#64-connecting-a-updi-target)
- [7. Supported devices](#7-supported-devices)
  * [7.1 Supported and tested hardware debuggers](#71-supported-and-tested-hardware-debuggers)
  * [7.2 Supported and tested MCUs](#72-supported-and-tested-mcus)
    + [7.2.1 Classic ATtinys and ATmegsa with debugWIRE interface](#721-classic-attinys-and-atmegsa-with-debugwire-interface)
      - [7.2.1.1 ATtiny covered by MicroCore](#7211-attiny-covered-by-microcore)
      - [7.2.1.2 ATtinys -- covered by the ATTinyCore](#7212-attinys----covered-by-the-attinycore)
      - [7.2.1.3 ATmegas covered by MiniCore](#7213-atmegas-covered-by-minicore)
      - [7.2.1.4 Other ATmegas](#7214-other-atmegas)
    + [7.2.2 ATmegas with JTAG interface](#722-atmegas-with-jtag-interface)
      - [7.2.2.1 ATmegas covered by MajorCode](#7221-atmegas-covered-by-majorcode)
      - [7.2.2.2 ATmegas covered by MegaCore](#7222-atmegas-covered-by-megacore)
      - [7.2.2.3 ATmegas covered by MightyCore](#7223-atmegas-covered-by-mightycore)
- [8. Notes for Linux systems](#8-notes-for-linux-systems)
- [9. What the future has in store for us](#9-what-the-future-has-in-store-for-us)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## 1. Switching SNAP and PICkit4 to AVR mode

SNAP and PICkit4 need to be switched to AVR mode before they can be used with pyavrocd. Switching to AVR mode in the SNAP debugger is easily accomplished by using avrdude (>= Version 7.3):

```
> avrdude -c snap_isp -Pusb -xmode=avr
```

With PICkit4 it is similar:

```
> avrdude -c pickit4_isp -Pusb -xmode=avr
```

In both cases, you can check whether you were successful by typing the same command again. If you get the message that the debugger is still in 'PIC' mode, you need to flash new firmware first using MPLAB X.

## 2. Installation

If you want to use pyavrocd as part of Arduino IDE 2, you do not need to install it explicitly. It is enough [to add an "additional boards manager URL" and install the respective core](#Arduino-IDE-2). As a Linux user, you may have to set additionally some permissions.

### 2.1 Installation by downloading binaries

Go to the GitHub page (if you are not already there), select the latest release (right-hand side of page), download the archive with the binary for your architecture, and untar the archive. It contains the executable `pyavrocd` and a folder `pyavrocd-util`. Store both of them somewhere in the same folder and include this folder in your `PATH` variable.

Since the binaries were generated on very recent versions of the respective operating systems (Windows 11, MacOS 15.4, Ubuntu 24.04), it can happen that the binary is not compatible with your operating system. In this case, use one oft the methods [below](#notes-for-linux-systems).

### 2.2 PyPI installation

I assume you already installed a recent Python version (>=3.9).

It will be necessary to install [pipx](https://pipx.pypa.io/) first. If you have not done so, follow the instructions on the [pipx website](https://pipx.pypa.io/stable/installation/). Then proceed as follows.

#### 2.2.1 Linux

```
> pipx install pyavrocd
> pipx ensurepath
> sudo ~/.local/bin/pyavrocd --install-udev-rules
```

After unplugging and replugging the debugger and restarting your shell, you can invoke the gdbserver by simply typing `pyavrocd` into a shell. The binary is stored under `~/.local/bin/`

#### 2.2.2 Windows and macOS

```
> pipx install pyavrocd
> pipx ensurepath
```

After restarting the shell, you should be able to start the gdbserver. The binary is stored under `~/.local/bin/`

### 2.3 GitHub installation

Alternatively, you can download or clone the GitHub repository. You need then to install the package poetry:

```
> pipx install poetry
```

With that, you can start executing the script inside the downloaded folder as follows:

```
> poetry install
> poetry run pyavrocd ...
```

Furthermore, you can create a binary standalone package as follows (after having installed the pyinstaller package):

```
> poetry run pyinstaller pyavrocd.spec
```

After that, you find an executable `pyavrocd` (or `pyavrocd.exe`) in the directory `dist/pyavrocd/` together with the folder `pyavrocd-util`. You can copy those to a place in your `PATH`. If you want to generate a binary on a Mac that can be shipped to other Macs, you should use `arm64-apple-pyavrocd.spec` or `intel-apple-pyavrocd.spec` in order to include `libusb`.

## 3. Usage

### 3.1 Compiling the program

You need to compile your programs with the optimization options `-Og`, which generates debugger friendly code. The default optimization option `-Os`, which optimizes for space, will rearrange the code leading to confusion when single-stepping. 

In addition, you may want to use the otpion `-ggdb3`, which will put as many symbols from the source program into the executable. 

### 3.2 Preparing the target

Before you can start debugging, you may need to modify the target board. In particular, for the popular Arduino UNO R3 board, you [must modify it by disconnecting the capacitor responsible for the auto-reset feature](https://debugwire.de/board-modifications/). However, also for other targets modifications may be necessary.

Second, you may need to change some hardware fuses in order to enable debug I/O pins. This applies mainly to targets with JTAG interface. 

### 3.3 Starting a debug session

Once you have done that and you [connected a hardware debugger to your target board](#connecting-a-debugwire-debugger-to-a-target), you can start the  gdbserver in a terminal window. 

```
> pyavrocd -d atmega328p
[INFO] Connecting to anything possible
[INFO] Connected to Atmel-ICE CMSIS-DAP
[INFO] Starting pyavrocd
[INFO] Looking for device atmega328p
[INFO] Listening on port 2000 for gdb connection

```

In another terminal window, you can now start a GDB session:

```
> avr-gdb <progname>.elf
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

If, instead of using a CLI, you want to use an IDE (e.g., Arduino IDE 2) or GUI, there are a [couple of possibilities](#integrated-development-environments-and-graphical-user-interfaces).

### 3.4 Pyavrocd command line options

The gdbserver can be started with a number of command line options, as detailed below.

| Optionname             | Description                                                  |
| ---------------------- | ------------------------------------------------------------ |
| `--device` <br>`-d`    | The argument to this option specifies the MCU type of the target chip in lower case.  This option is mandatory. If a '?' mark is given, all supported MCUs are listed. |
| `--gede`<br>`-g`       | No argument for this option. This option will start the `Gede` debugger GUI. |
| `--port` <br>`-p`      | IP port on the local host to which GDB can connect.          |
| `--start` <br>`-s`     | Program to start or the string `noop`, when no program should be started |
| `--tool`<br>`-t`       | Specifying the debug tool. Possible values are `atmelice`, `edbg`, `jtagice3`, `medbg`, `nedbg`, `pickit4`, `powerdebugger`, `snap`, `dwlink`. Use of this option is necessary only if more than one debugging tool is connected to the computer. |
| `--usbsn` <br>`-u`     | USB serial number of the tool. This is only necessary if one has multiple debugging tools connected to the computer. |
| `--verbose` <br>`-v`   | Specify verbosity level. Possible values are `debug`, `info`, `warning`, `error`, or `critical`. The default is `info`. |
| `--version` <br>`-V`   | Print pyavrocd version number and exit.                      |
| `--install-udev-rules` | Install the udev rules necessary for Microchip's EDBG debuggers. Needs to be run with `sudo` and is only present under Linux. |

### 3.5 Monitor commands

Pyavrocd implements a number of `monitor` commands. These can be used to control important aspected of the gdbserver. One important command is the `monitor debugwire enable` command, which enables debugWIRE mode on MCUs supporting this interface.

| Command                                               | Action                                                       |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| `monitor breakpoints` [`all`\|`software`\|`hardware`] | Restricts the kind of breakpoints the hardware debugger can use. Either *all* types are permitted, only *software* breakpoints are allowed, or only *hardware* breakpoints can be used. Using all kinds is the default. |
| `monitor caching` [`enable`\|`disable`]               | The loaded executable is cached in the gdbserver when *enabled*, which is the default. |
| `monitor debugwire` [`enable`\|`disable`]             | DebugWIRE mode will be enabled or disabled. When enabling it, the MCU will be reset and you may be asked to power-cycle the target. After disabling debugWIRE mode, the MCU can be programmed again using SPI programming. |
| `monitor help`                                        | Display help text.                                           |
| `monitor info`                                        | Display information about the target and the state of the debugger. |
| `monitor load` [`readbeforewrite`\|`writeonly`]       | When loading an executable, either each flash page is compared with the content to be loaded, and flashing is skipped if the content is already there, or each flash page is written without reading the current contents beforehand. The first option is the default option and there is no reason to change it. |
| `monitor onlyloaded` [`enable`\|`disable`]            | Execution is only possible when a `load` command was previously executed, which is the default. If you want to start execution without previously loading an executable, you need to disable this mode. |
| `monitor rangestepping `[`enable`\|`disable`]         | The GDB range-stepping command is supported or disabled.     |
| `monitor reset`                                       | Resets the MCU.                                              |
| `monitor singlestep` [`safe`\|`interruptible`]        | Single-stepping can either be performed in a *safe* way, where single steps are shielded against interrupts or in a way, where a single step can lead to a jump into the interrupt dispatch table. The *safe* option is the default. |
| `monitor timer` [`freeze`\|`run`]                     | Timers can either be *frozen* when execution is stopped, or they can *run* freely. The later option is helpful when PWM output is crucial. |
| `monitor verify` [`enable`\|`disable`]                | Verify flash after loading each flash page. The cost for verifying is negligible, and doing so might diagnose flash wear problems. The default is that this option is *enabled*. |
| `monitor version`                                     | Show version of the gdbserver.                               |

The default setting is always the first one listed, except for `debugwire`, which depends on the MCU itself. All commands can, as usual, be abbreviated. For example, `mo d e` is equivalent to `monitor debugwire enable`.

## 4. Integrated Development Environments and Graphical User Interfaces

There are several possible options for using an IDE or a GUI that make use of pyavrocd to enable a debugging solution.

### 4.1 Arduino IDE 2

Arduino IDE 2 is probably the most straightforward option. You only need to add `Additional Boards Manager URLs` in the `Preference` dialog:

```
https://felias-fogg.github.io/ATTinyCore/package_drazzy.com_ATTinyCore_index.json
https://mcudude.github.io/MicroCore/package_MCUdude_MicroCore_index.json
https://mcudude.github.io/MiniCore/package_MCUdude_MiniCore_index.json
```

After that, you must install the respective cores, which enables you to debug almost all classic AVR chips that use the debugWIRE interface. And this is all! Now, you can press the debug button and start debugging. See, e.g., this [short tutorial](https://docs.arduino.cc/software/ide-v2/tutorials/ide-v2-debugger/) about debugging in the Arduino IDE 2 documentation.

Linux users may need to add a few udev rules. When you first start the Arduino IDE debugger and the hardware debuggers are not recognized, you will get a hint in the `gdb-server` window of how to set the udev rules. You simply have to execute pyavrocd once using the command line option `--install-udev-rules`. Instead, you can create a udev-rules file along the lines described below.

### 4.2 PlatformIO and Visual Studio Code

PlatformIO is a cross-platform, cross-architecture, multiple framework professional tool for embedded systems engineers. Installed as an extension to the popular Visual Studio Code, it provides a powerful IDE for embedded programming and debugging. Using the `platformio.ini` file, integrating an external debugging framework is very easy. If you want to debug a program on an ATmega328P, the `platformio.ini` file could look as follows:

```
[platformio]
default_envs = debug

[env:atmega328p]
platform = atmelavr
framework = arduino
board = ATmega328P
board_build.f_cpu = 16000000L
board_hardware.oscillator = external

[env:debug]
extends = env:atmega328p              ;; <--- substitute the right board here
build_type = debug
debug_tool = custom
debug_server = /path/to/pyavrocd  ;; <-- specify path to gdbserver
    --port=3333
    --device=${env:debug.board}
debug_init_cmds =
    define pio_reset_halt_target
         monitor reset
    end
    define pio_reset_run_target
         monitor reset
	       continue
    end
    target remote $DEBUG_PORT
    monitor debugwire enable
    $LOAD_CMDS
    $INIT_BREAK
debug_build_flags =
    -Og
    -ggdb3
```

Note that the debug environment should be the default one. It should be the first if no default environment has been declared.

I further noticed that the avr-gdb debugger in the PlatformIO toolchain is quite dated and does not start (e.g. under Ubuntu 24.04 and macOS 15.5). Simply replace it with a more recent version from /usr/bin or /usr/local/bin, perhaps after having it installed with you local packet manager. The location where PlatformIO stores its copy of avr-gdb is `~/.platformio/packages/toolchain-atmelavr/` , where the tilde symbol signifies the home directory of the user.

### 4.3 Gede

[Gede](https://github.com/jhn98032/gede) is a lean and clean GUI for GDB. It can be built and run on almost all Linux distros, FreeBSD, and macOS. You need an avr-gdb client with a version >= 10.2. If you have installed Gede somewhere in your PATH, you can start it by specifying the option `--gede` or `-g` when starting pyavrocd.

![Gede](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/gede.png)

`Project dir` and `Program` are specific to your debugging session. The rest should be copied as it is shown. Before you click `OK`, you should switch to the `Commands` section, where you need to enter the command `monitor debugwire enable`.

![Command section](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/gede-cmds.png)

Clicking on OK, you start a debugging session. The startup may take a while because the debugger always loads the object file into memory.

## 5. Prepapring a target for debugging and restoring the original state

As mentioned above, it may be necessary to prepare your target for a debugging session. Depending on what kind of debugging interface the MCU provides, different actions need to be taken.

### 5.1 Preparing a debugWIRE target

#### 5.1.1 How to get into and out of debugWIRE mode

When the MCU is not already in debugWIRE mode,  you must request the switch to debugWIRE mode using the command `monitor debugwire enable` in GDB. The debugger will then enable the DWEN fuse and either power-cycles the target by itself (if possible) or ask you to power-cycle the target system. Once this is done, the chip will stay in debugWIRE mode, even after terminating the debugging session. In other words, when starting the next debug session, the MCU is already in debugWIRE mode.

You can switch back to normal mode using the command `monitor debugwire disable` before leaving the debugger. Inside the Arduino IDE 2 with the ATTinyCore, MiniCore, or MicroCore, you can instead just use the `Burn Bootloader` command in the `Tools` menu. This will switch back the MCU to normal mode and burn the right fuses and the bootloader of this core.

#### 5.1.2 Restoring an Arduino Uno R3 to its original state after debugging

If, after debugging, you want to restore an Arduino Uno or similar board to its original state, two things have to be done:

1. You need to enable the RESET capacitor again, either by closing the opened solder bridge or by reinserting the removed capacitor. My advice is not to do that, but mark the board instead for debug use only.  In this case, you can also ignore step 2. Another possibility is to leave out the capacitor and use a manual reset just before avrdude starts the upload.

2. You need to reflash the bootloader and set the right fuses. In the Arduino IDE, you can do this by using the `Burn Bootloader` command in the `Tools` menu. Note that when using MiniCore, this means that the *urboot* bootloader is installed. In other words, you then need to use MiniCore when programming the board.

   If you want to reinstall the original Optiboot bootloader, you have to select `Arduino Uno` as the board under the `Tools` menu and have to use either `Arduino as ISP` or any other simple ISP programmer, e.g.,  USBasp or USBtinyISP, for flashing the bootloader.

### 5.2 Preparing a JTAG target

### 5.3 Preparing a PDI target

### 5.4 Preparing a UPDI target

## 6. Connecting the hardware debugger to a target

### 6.1 Connecting a debugWIRE target

In principle, only two wires are necessary to connect your hardware debugger to a target chip or board: the debugWIRE line, which is the target chip's RESET line, and GND. However, when one wants to change into and out of debugWIRE mode, change fuses, or upload firmware, it is necessary to connect all 6 SPI programming lines to the target: VTG, GND, RESET, MOSI, MISO, and SCK. For this reason, using all SPI programming lines makes a lot of sense. Moreover, most of the time, an SPI connector is already on the target board.

#### 6.1.1 SPI programming header

There are two types of SPI programming connectors. The more recent type has six pins, and the older type has 10 pins, as shown in the following diagram (based on a diagram from Wikipedia https://commons.wikimedia.org/wiki/user:Osiixy), which provides a top view of the headers on a PCB.

![ISP headers](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/Isp_headers.svg.png)

Note the notches on the left side of the headers. Since almost all SPI programming plugs are keyed, you can only plug them in in the correct orientation. However, the headers sometimes do not have notches. In this case, pin 1 is usually marked in some way, either with a dot, a star, or with the number 1. Similarly, plugs also come unkeyed. In this case, again, pin 1 is marked in some way.

#### 6.1.2 Connecting to targets with an SPI programming header

If the target board has an SPI programming header, it is easy to connect to it. **Atmel-ICE**, **Power Debugge**r, and **JTAGICE3** have a cable you can plug into a 6-pin SPI programming header. If you only have a 10-pin header on the target, you need an adapter. **PICKit4** and **SNAP** do not come with SPI programming headers. However, you can buy an [AVR programming adapter](https://www.microchip.com/en-us/development-tool/ac31s18a) from Microchip, an [adapter PCB from OSH Park](https://oshpark.com/shared_projects/eZiws6Jb), or [a more luxurious version from eBay](https://www.ebay.de/itm/186561251300). Finally, for **dw-link**, I propose preparing a [modified SPI programming cable](https://arduino-craft-corner.de/index.php/2022/01/13/a-debugwire-hardware-debugger-for-less-than-10-e/) or buying the [dw-link probe programmer shield](https://www.tindie.com/products/fogg/dw-link-probe-a-debugwire-hardware-debugger/), which has an SPI programming header on board.

![atmel-ice-connect](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/atmel-ice-connect.png)


#### 6.1.3 Connecting to targets without an SPI programming header

If the target does not feature an SPI programming header, you need to connect 6 cables. If you are working with a breadboard, you may consider buying an [SPI header breadboard adapter](https://www.adafruit.com/product/1465). Otherwise, you need to connect each pin individually. **Atmel-ICE**, **Power Debugge**r, and **JTAGICE3** have a so-called 10-pin mini-squid cable. The pin mapping for those debuggers is as follows.

| Atmel Debugger | Mini-squid pin | Target pin | SPI pin |
| -------------- | -------------- | ---------- | ------- |
| Pin 1 (TCK)    | 1              | SCK        | 3       |
| Pin 2 (GND)    | 2              | GND        | 6       |
| Pin 3 (TDO)    | 3              | MISO       | 1       |
| Pin 4 (VTG)    | 4              | VTG        | 2       |
| Pin 5 (TMS)    | 5              | &nbsp;     | &nbsp;  |
| Pin 6 (nSRST)  | 6              | RESET      | 5       |
| Pin  (N.C.)    | 7&nbsp;        | &nbsp;     | &nbsp;  |
| Pin 8 (nTRST)  | 8              | &nbsp;     | &nbsp;  |
| Pin 9 (TDI)    | 9              | MOSI       | 4       |
| Pin 10 (GND)   | 0              | &nbsp;     | &nbsp;  |

For **PICkit4** and **SNAP**, such a table looks as follows, with pin 1 marked by a triangle.

| MBLAP Debugger | Pin # | Target pin | SPI pin |
| -------------- | ----- | ---------- | ------- |
| Pin 1 (TVPP)   | 1     | &nbsp;     | &nbsp;  |
| Pin 2 (TVDD)   | 2     | VTG        | 2       |
| Pin 3 (GND)    | 3     | GND        | 6       |
| Pin 4 (PGD)    | 4     | MISO       | 1       |
| Pin 5 (PGC)    | 5     | SCK        | 3       |
| Pin 6 (TAUX)   | 6     | RESET      | 5       |
| Pin 7 (TTDI)   | 7     | MOSI       | 4       |
| Pin 8 (TTMS)   | 8     | &nbsp;     | &nbsp;  |

![picki4-connect](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pickit4-connect.png)

When you want to connect a **dw-link** debugger without a dw-link probe shield to a target, you can use jumper cables using the following pin mapping.

| dw-link Arduino Uno pins    | Target pin | SPI pin |
| --------------------------- | ---------- | ------- |
| D8                          | RESET      | 5       |
| D11                         | MOSI       | 4       |
| D12                         | MISO       | 1       |
| D13                         | SCK        | 3       |
| 5V (if powered by debugger) | Vcc        | 2       |
| GND                         | GND        | 6       |

With a dw-link probe shield, it is best to construct or buy a cable with a 6-pin SPI programming plug on one end and single Dupont pins on the other.

#### 6.1.4 Powering the target board

When using one of the commercial debuggers, you need to power the target board from an external source. With dw-link, you can choose to power the target board from the debugger or an external source.

### 6.2 Connecting a JTAG target

### 6.3 Connecting a PDI target

### 6.4 Connecting a UPDI target

## 7. Supported devices

### 7.1 Supported and tested hardware debuggers

Except for [dw-link](https://github.com/felias-fogg/dw-link), this list is copied from the readme file of [pyedbglib](https://github.com/microchip-pic-avr-tools/pyedbglib). Boldface means that the debuggers have been tested by me and work with this Python script.


* **MPLAB PICkit 4 In-Circuit Debugger** (when in 'AVR mode')
* **MPLAB Snap In-Circuit Debugger** (when in 'AVR mode')
* **Atmel-ICE**
* **Atmel Power Debugger**
* **EDBG - on-board debuggers on Xplained Mini/Nano, Curiosity boards and alike**
* **JTAGICE3 (firmware version 3.0 or newer)**
* **[dw-link](https://github.com/felias-fogg/dw-link)** - **DIY debugWIRE debugger running on an Arduino UNO R3**


### 7.2 Supported and tested MCUs

This is the list of all AVR MCUs, which should all be compatible with pyavrocd. MCUs tested with pyavrocd  are marked bold. MCUs known not to work with the script are struck out. 

#### 7.2.1 Classic ATtinys and ATmegsa with debugWIRE interface

##### 7.2.1.1 ATtiny covered by MicroCore

- **ATtiny13**

##### 7.2.1.2 ATtinys -- covered by the ATTinyCore

* **ATtiny43U**
* **ATtiny2313(A), ATtiny4313**
* **ATtiny24(A), ATtiny44(A), ATtiny84(A)**
* **ATtiny441, ATtiny841**
* **ATtiny25, ATtiny45**, **ATtiny85**
* **ATtiny261(A), ATtiny461(A), ATtiny861(A)**
* **ATtiny87, ATtiny167**
* **ATtiny828**
* **ATtiny48, ATtiny88**
* **ATtiny1634**

##### 7.2.1.3 ATmegas covered by MiniCore

* <s>__ATmega48__</s>, __ATmega48A__, __ATmega48PA__, ATmega48PB,
* <s>__ATmega88__</s>, __ATmega88A__, __ATmega88PA__, Atmega88PB,
* __ATmega168__, __ATmega168A__, __ATmega168PA__, ATmega168PB,
* **ATmega328**, __ATmega328P__, **ATmega328PB**

The ATmega48 and ATmega88 (without the A-suffix) sitting on my desk suffer from stuck-at-one bits in the program counter and are, therefore, not debuggable by GDB. I suspect that this applies to all chips labeled this way. In any case, the test for stuck-at-one-bits is made when connecting to the chips.

##### 7.2.1.4 Other ATmegas

* ATmega8U2, ATmega16U2, ATmega32U2
* ATmega32C1, ATmega64C1, ATmega16M1, ATmega32M1, ATmega64M1
* AT90USB82, AT90USB162
* AT90PWM1, AT90PWM2B, AT90PWM3B
* AT90PWM81, AT90PWM161
* AT90PWM216, AT90PWM316
* ATmega8HVA, ATmega16HVA, ATmega16HVB, ATmega32HVB, ATmega64HVE2

#### 7.2.2 ATmegas with JTAG interface

##### 7.2.2.1 ATmegas covered by MajorCode

- ATmega8515
- ATmega162

##### 7.2.2.2 ATmegas covered by MegaCore

- ATmega64, ATmega128 (no SW breakpoints?)

- ATmega640, ATmega1280, ATmega2560
- ATmega1281, ATmega2561
- ATmega165, ATmega325, ATmega645
- ATmega169, ATmega329, ATmega649
- ATmega3250, ATmega6450
- ATmega3290, ATmega6490
- AT90CAN32, AT90CAN64, AT90CAN128

##### 7.2.2.3 ATmegas covered by MightyCore

- ATmega8535
- ATmega16, ATmega32
- ATmega164, ATmega324, ATmega644, ATmega1284

## 8. Notes for Linux systems

The following text is copied verbatim from the README of pyedbglib. The udev rules will be added when you call pyavrocd with the option --install-udev-rules in sudo-mode. Permission for serial lines, as described in the end, needs to be set manually. However, the hardware debuggers only use USB.

> HIDAPI needs to build using packages: libusb-1.0.0-dev, libudev-dev
>
> USB devices need udev rules to be added to a file in /etc/udev/rules.d Example of udev rules for supported debuggers:
>
> ```bash
> # HIDAPI/libusb:
>
> # JTAGICE3
> SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2140", MODE="0666"
> # Atmel-ICE
> SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2141", MODE="0666"
> # Power Debugger
> SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2144", MODE="0666"
> # EDBG - debugger on Xplained Pro
> SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2111", MODE="0666"
> # EDBG - debugger on Xplained Pro (MSD mode)
> SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2169", MODE="0666"
> # mEDBG - debugger on Xplained Mini
> SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2145", MODE="0666"
> # PKOB nano (nEDBG) - debugger on Curiosity Nano
> SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2175", MODE="0666"
> # PKOB nano (nEDBG) in DFU mode - bootloader of debugger on Curiosity Nano
> SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2fc0", MODE="0666"
> # MPLAB PICkit 4 In-Circuit Debugger
> SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2177", MODE="0666"
> # MPLAB Snap In-Circuit Debugger
> SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2180", MODE="0666"
> ```
>
> pyedbglib also provides helper functions for accessing serial ports.  The user has to be part of the 'dialout' group to allow this.  This can be done by executing:
> ```bash
> sudo adduser $USER dialout
> ```
>
> It may also be necessary to grant read+write permission to the port, for example:
> ```bash
> sudo chmod a+rw /dev/ttyACM0
> ```
>



## 9. What the future has in store for us

The script has now its full functionality and seems to work pretty well. It has also been integrated into MiniCore, MicroCore and my fork of ATTinyCore.

Now, it is only a "tiny" step to generalize it to the JTAG and UPDI AVR MCUs. So, stay tuned. Before working on that, I plan to deploy a test battery on the GDB/arduino-cli level, however.
