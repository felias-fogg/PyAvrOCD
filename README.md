#  pyavrocd

Pyavrocd is a [GDB server](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Server.html) for 8-bit AVR MCUs ([list of supported MCUs and boards](https://github.com/felias-fogg/pyavrocd/blob/main/docs/supported-mcus-and-boards.md)). It can communicate with Microchip debuggers such as [Atmel-ICE](https://www.microchip.com/en-us/development-tool/atatmel-ice) and [MPLAB Snap](https://www.microchip.com/en-us/development-tool/pg164100) ([in AVR mode](#switching-to-avr-mode)), and provides a pass-through service for the Uno-based debugger [dw-link](https://github.com/felias-fogg/dw-link). For Microchip debuggers, pyavrocd uses the infrastructure provided by [pymcuprog](https://github.com/microchip-pic-avr-tools/pymcuprog) and [pyedgblib](https://github.com/microchip-pic-avr-tools/pyedbglib).

So, why another open-source GDB server for AVR MCUs (others are [AVaRICE](https://github.com/avrdudes/avarice) and [Bloom](https://bloom.oscillate.io))? The main intention is to provide a *platform-agnostic* AVR GDB server. In other words, it is the missing AVR debugging solution for [PlatformIO](https://platformio.org) and the [Arduino IDE 2](https://www.arduino.cc/en/software/).

![ide2-6](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide2-6.png)

In addition to being platform agnostic, pyavrocd offers some enhancements over its "competitors", particularly in terms of [flash wear](https://arduino-craft-corner.de/index.php/2025/05/05/stop-and-go/) and [single-stepping](https://arduino-craft-corner.de/index.php/2025/03/19/interrupted-and-very-long-single-steps/).

After [installing the package](https://github.com/felias-fogg/pyavrocd/blob/main/INSTALL.md), the following steps are necessary for successful debugging:

1. [Installing and configuring the appropriate debugging software](https://github.com/felias-fogg/pyavrocd/blob/main/docs/debugging-software.md)
2. [Preparing the target board for debugging](https://github.com/felias-fogg/pyavrocd/blob/main/docs/board-preparation.md)
3. [Connecting the hardware debugger to the target](https://github.com/felias-fogg/pyavrocd/blob/main/docs/connect-to-target.md)
4. [Debugging a program on the target](https://github.com/felias-fogg/pyavrocd/blob/main/docs/usage.md)
5. [Restoring the target to its original state](https://github.com/felias-fogg/pyavrocd/blob/main/docs/restore-original-state.md)

When starting the GDB server from the command line, there are several *[command-line options](https://github.com/felias-fogg/pyavrocd/blob/main/docs/command-line-options.md)* that will influence the behavior of pyavrocd. Once you have a debugger connected to the server, you can control the server's behavior using *[`monitor` commands](https://github.com/felias-fogg/pyavrocd/blob/main/docs/monitor-commands.md).*

While the package appears to function as intended, there is always the chance of a bug. If you run across a behavior that seems odd, you can report it as an [issue](https://github.com/felias-fogg/pyavrocd/issues). I hope to resolve those over time.

**Disclaimer**: Note that, as is usual in life, there are some risks involved when using a tool. In particular, [the debugWIRE interface can be a serious health risk to your MCU](https://github.com/felias-fogg/pyavrocd/blob/main/docs/debugwire-risks.md). Even worse, all other aspects of the debugging package have the potential of doing harm to the tested MCU, target board or attached devices. Bear in mind that [the software is provided "as is", without warranty of any kind](https://github.com/felias-fogg/pyavrocd/blob/main/LICENSE).

## Supported hardware debuggers

Except for [dw-link](https://github.com/felias-fogg/dw-link), this list is copied from the README file of [pyedbglib](https://github.com/microchip-pic-avr-tools/pyedbglib). Boldface means that I have tested the debuggers and they work with pyavrocd.


* **MPLAB PICkit 4 In-Circuit Debugger** (when in 'AVR mode')
* **MPLAB Snap In-Circuit Debugger** (when in 'AVR mode')
* **Atmel-ICE**
* **Atmel Power Debugger**
* **JTAGICE3 (firmware version 3.0 or newer)**
* **EDBG - on-board debuggers on Xplained Pro/Ultra**
* **mEDBG - on-board debuggers on Xplained Mini/Nano**
* nEDBG - on-board debuggers on Curiosity Nano
* **[dw-link](https://github.com/felias-fogg/dw-link)** - **DIY debugger running on an Arduino UNO R3** (only debugWIRE)

My JTAGICE3, being the oldest one of the set of supported debuggers, is sometimes a bit shaky. In particular, with lower voltages and when the MCU has a clock less than 8 MHz, sometimes it emits errors when other debuggers work without a hitch. It is not clear whether these issues are with my sample or a general problem for these debuggers.

### Switching to AVR mode

Note that Snap and PICkit4 need to be switched to 'AVR mode'. This can usually be accomplished as follows by using avrdude (>= Version 7.3):

```
avrdude -c snap_isp -Pusb -xmode=avr
```

With PICkit4, it is similar:

```
avrdude -c pickit4_isp -Pusb -xmode=avr
```

In both cases, you can check whether you were successful by typing the same command again. If you get the message that the debugger is still in 'PIC' mode, you need to [flash new firmware first using MPLAB X](https://arduino-craft-corner.de/index.php/2025/04/16/snap-debugging-for-the-masses/#appendix-installing-a-recent-firmware-version).



## What to expect in the future

The GDB server has been integrated into MiniCore, MicroCore, and my fork of ATTinyCore. Support for JTAG mega chips has been added, but pyavrocd has not been incorporated into the respective cores yet, but will soon be. UPDI targets will follow next.

