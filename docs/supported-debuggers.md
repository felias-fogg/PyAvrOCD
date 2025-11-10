# Supported debug probes

Except for dw-link and microUPDI, this list is copied from the README file of [pyedbglib](https://github.com/microchip-pic-avr-tools/pyedbglib). Boldface means that I have tested the debuggers and they work with PyAvrOCD, underlined means that the debugger is waiting to be tested:


* **[MPLAB PICkit 4 In-Circuit Debugger](https://www.microchip.com/en-us/development-tool/pg164140)** ([when in 'AVR mode'](#switching-to-avr-mode))
* **[MPLAB Snap In-Circuit Debugger](https://www.microchip.com/en-us/development-tool/pg164100)** ([when in 'AVR mode'](#switching-to-avr-mode))
* [**Atmel-ICE**](https://www.microchip.com/en-us/development-tool/atatmel-ice)
* **[Atmel Power Debugger](https://www.microchip.com/en-us/development-tool/atpowerdebugger)**
* **[JTAGICE3](https://www.microchip.com/en-us/development-tool/atjtagice3) (firmware version 3.0 or newer)**
* **[EDBG](http://content.alexandria.atmel.com/webhelp/GUID-43D69EB5-28C5-4F23-97B7-43CD3961DC33-en-US-3/index.html?GUID-180AB3C3-775A-482F-961D-D9862473CD85) - on-board debuggers on Xplained Pro/Ultra**
* **[mEDBG](https://onlinedocs.microchip.com/oxy/GUID-FC2A0384-AC9D-45B4-951E-5C0DEFE8B2E9-en-US-5/GUID-4063E88C-69CE-4393-ABBF-46E406D92BD3.html) - on-board debuggers on Xplained Mini/Nano**
* <u>[microUPDI](https://github.com/MCUdude/microUPDI)</u> - an mEDBG clone by MCUdude (only UPDI)
* <u>[nEDBG](https://www.microchipdirect.com/dev-tools/curiosityboards_curiositynanoboards?allDevTools=true)</u> - on-board debuggers on Curiosity Nano
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

