#  pyavrocd

This is a Python GDB server for 8-bit AVR MCUs (work in progress, currently only for classic ATtinys and ATmegas with debugWIRE debugging interface). It can communicate with Microchip debuggers such as [Atmel-ICE](https://www.microchip.com/en-us/development-tool/atatmel-ice) and [MPLAB Snap](https://www.microchip.com/en-us/development-tool/pg164100) ([in AVR mode](#switching-to-avr-mode)), and provides a pass-through service for the Uno-based debugger [dw-link](https://github.com/felias-fogg/dw-link). For Microchip debuggers, pyavrocd uses the infrastructure provided by [pymcuprog](https://github.com/microchip-pic-avr-tools/pymcuprog) and [pyedgblib](https://github.com/microchip-pic-avr-tools/pyedbglib).

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



## Supported hardware debuggers

Except for [dw-link](https://github.com/felias-fogg/dw-link), this list is copied from the README file of [pyedbglib](https://github.com/microchip-pic-avr-tools/pyedbglib). Boldface means that I have tested the debuggers and they work with pyavrocd.


* **MPLAB PICkit 4 In-Circuit Debugger** (when in 'AVR mode')
* **MPLAB Snap In-Circuit Debugger** (when in 'AVR mode')
* **Atmel-ICE**
* **Atmel Power Debugger**
* **JTAGICE3 (firmware version 3.0 or newer)**
* EDBG - on-board debuggers on Xplained Pro/Ultra
* **mEDBG - on-board debuggers on Xplained Mini/Nano**
* nEDBG - on-board debuggers on Curiosity Nano
* **[dw-link](https://github.com/felias-fogg/dw-link)** - **DIY debugger running on an Arduino UNO R3** (only debugWIRE)

### Switching to AVR mode

Note that Snap and PICkit4 need to be switched to 'AVR mode'. This can usually be accomplished as follows by using avrdude (>= Version 7.3):

```
> avrdude -c snap_isp -Pusb -xmode=avr
```

With PICkit4, it is similar:

```
> avrdude -c pickit4_isp -Pusb -xmode=avr
```

In both cases, you can check whether you were successful by typing the same command again. If you get the message that the debugger is still in 'PIC' mode, you need to [flash new firmware first using MPLAB X](https://arduino-craft-corner.de/index.php/2025/04/16/snap-debugging-for-the-masses/#appendix-installing-a-recent-firmware-version).



## Currently supported AVR MCUs and Arduino boards

This is the list of all AVR MCUs, which should be compatible with pyavrocd. MCUs tested with pyavrocd are marked bold. MCUs known not to work with pyavrocd are struck out.

### Classic ATtinys and ATmegas with debugWIRE interface

#### ATtiny supported by [*MicroCore*](https://github.com/MCUdude/MicroCore)

- **ATtiny13**

#### ATtinys supported by the [*ATTinyCore*](https://github.com/SpenceKonde/ATTinyCore)

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

#### ATmegas supported by [*MiniCore*](https://github.com/MCUdude/MiniCore)

* <s>__ATmega48__</s>, __ATmega48A__, __ATmega48PA__, ATmega48PB,
* <s>__ATmega88__</s>, __ATmega88A__, __ATmega88PA__, Atmega88PB,
* __ATmega168__, __ATmega168A__, __ATmega168PA__, **ATmega168PB**,
* **ATmega328**, __ATmega328P__, **ATmega328PB**

The ATmega48 and ATmega88 (without the A-suffix) sitting on my desk suffer from stuck-at-one bits in the program counter and are, therefore, not debuggable by GDB. I suspect that this applies to all chips labeled this way. In any case, the test for stuck-at-one-bits is made when connecting to the chips.

#### Other ATmegas

* ATmega8U2, ATmega16U2, ATmega32U2
* ATmega32C1, ATmega64C1, ATmega16M1, ATmega32M1, ATmega64M1
* AT90USB82, AT90USB162
* AT90PWM1, AT90PWM2B, AT90PWM3B
* AT90PWM81, AT90PWM161
* AT90PWM216, AT90PWM316
* ATmega8HVA, ATmega16HVA, ATmega16HVB, ATmega32HVB, ATmega32HVBrevB, ATmega64HVE2

#### Supported Arduino boards

All Arduino boards equipped with one of the chips mentioned above can be debugged. This includes the **Arduino Uno R3**, **Arduino Nano**, and **Arduino Pro Mini** (as well as clones). Note that in all these cases, one must ensure that the RESET line is not connected to a capacitor and that the pull-up resistor on the RESET line is not stronger than 10 kΩ. This means that the [board must be physically changed](https://github.com/felias-fogg/pyavrocd/blob/main/docs/board-preparation.md) before debugging is possible.

<!--

### ATmegas with JTAG interface

*(not yet supported, but will be real soon)*

#### ATmegas supported by [*MightyCore*](https://github.com/MCUdude/MightyCore)

* ATmega16(A), ATmega32(A)
* ATmega164(P)(A), ATmega324(P)(A/B), ATmega644, ATmega1284

#### ATmegas supported by [*MegaCore*](https://github.com/MCUdude/MegaCore)

* ATmega64(A), ATmega128(A) (no SW breakpoints?)
* ATmega640, ATmega1280, ATmega2560
* ATmega1281, ATmega2561
* ATmega165(P)(A), ATmega325(P)(A), ATmega645(P)(A)
* ATmega169(P)(A), ATmega329(P)(A), ATmega649
* ATmega3250(P)(A), ATmega6450(P)(A)
* ATmega3290(P)(A), ATmega6490(P)(A)
* AT90CAN32, AT90CAN64, AT90CAN128

#### ATmega supported by [*MajorCore*](https://github.com/MCUdude/MajorCore)

* ATmega162

#### Other ATmegas

* AT90USB646, AT90USB647, AT90USB1286, AT90USB1287
* ATmega644rfr2, ATmega1284rfr2, ATmega2564rfr2
* ATmega64rfr2, ATmega128rfr2, ATmega256rfr2
* ATmega128rfa1
* ATmega16U4, ATmega32U4
* ATmega406

#### Supported Arduino boards

All boards with the chips listed above can be debugged. This is, in particular, the **Arduino Mega (2560)**, **Arduino Leonardo**, and **Arduino Micro**. Note that you should not connect any load to the JTAG lines. Furthermore, you must first enable the JTAG pins by ISP programming because on the Arduino boards, JTAG is disabled by default.

-->

## What to expect in the future

The package now has its full functionality and seems to work pretty well with debugWIRE MCUs. It has also been integrated into MiniCore, MicroCore, and my fork of ATTinyCore. Currently, I am working on implementing the JTAG part. UPDI will follow soon, hopefully.
