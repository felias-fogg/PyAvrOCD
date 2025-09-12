# Supported hardware debuggers

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

## Switching to AVR mode

Note that Snap and PICkit4 need to be switched to 'AVR mode'. This can usually be accomplished as follows by using avrdude (>= Version 7.3):

```
avrdude -c snap_isp -Pusb -xmode=avr
```

With PICkit4, it is similar:

```
avrdude -c pickit4_isp -Pusb -xmode=avr
```

In both cases, you can check whether you were successful by typing the same command again. If you get the message that the debugger is still in 'PIC' mode, you need to [flash new firmware first using MPLAB X](https://arduino-craft-corner.de/index.php/2025/04/16/snap-debugging-for-the-masses/#appendix-installing-a-recent-firmware-version).

