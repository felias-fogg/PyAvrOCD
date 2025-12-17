# Supported debug probes

PyAvrOCD has been built to provide access to AVR OCDs by means of Microchip's debug probes. However, it also provides a pass-through service for the DIY debug probe [dw-link](https://felias-fogg.github.io/dw-link). And, as a service to Arduino users, it provides access to the software simulation tool [simavr](https://github.com/buserror/simavr) (see [below](#software-simulator)).

## Hardware debug probes

Except for dw-link and microUPDI, the list below is copied from the README file of [pyedbglib](https://github.com/microchip-pic-avr-tools/pyedbglib). Boldface means that I have tested the debuggers and they work with PyAvrOCD; underlined means that the debugger is waiting on my desk to be tested:


* **[MPLAB PICkit 4 In-Circuit Debugger](https://www.microchip.com/en-us/development-tool/pg164140)** ([when in 'AVR mode'](#switching-to-avr-mode))
* **[MPLAB Snap In-Circuit Debugger](https://www.microchip.com/en-us/development-tool/pg164100)** ([when in 'AVR mode'](#switching-to-avr-mode))
* [**Atmel-ICE**](https://www.microchip.com/en-us/development-tool/atatmel-ice)
* **[Atmel Power Debugger](https://www.microchip.com/en-us/development-tool/atpowerdebugger)**
* **[JTAGICE3](https://www.microchip.com/en-us/development-tool/atjtagice3) (firmware version 3.0 or newer)**
* **[EDBG](http://content.alexandria.atmel.com/webhelp/GUID-43D69EB5-28C5-4F23-97B7-43CD3961DC33-en-US-3/index.html?GUID-180AB3C3-775A-482F-961D-D9862473CD85) - on-board debuggers on Xplained Pro/Ultra**
* **[mEDBG](https://onlinedocs.microchip.com/oxy/GUID-FC2A0384-AC9D-45B4-951E-5C0DEFE8B2E9-en-US-5/GUID-4063E88C-69CE-4393-ABBF-46E406D92BD3.html) - on-board debuggers on Xplained Mini/Nano**
* <u>[microUPDI](https://github.com/MCUdude/microUPDI)</u> - an mEDBG clone by MCUdude (only UPDI)
* <u>[nEDBG](https://www.microchipdirect.com/dev-tools/curiosityboards_curiositynanoboards?allDevTools=true)</u> - on-board debuggers on Curiosity Nano
* **[dw-link](https://felias-fogg.github.io/dw-link)** - **DIY debugger running on an Arduino UNO R3** (only debugWIRE)

My **JTAGICE3**, being the oldest one of the set of supported debuggers, is sometimes a bit shaky. In particular, with lower voltages and when the MCU has a clock less than 8 MHz, sometimes it emits error messages when other debuggers work without a hitch. It is not clear whether these issues are with my sample or a general problem for these debuggers.

### Switching to AVR mode

Note that Snap and PICkit4 need to be switched to 'AVR mode'. This can be accomplished as follows by using avrdude (>= Version 7.3):

```
avrdude -c snap_isp -Pusb -xmode=avr
```

With PICkit4, it is similar:

```
avrdude -c pickit4_isp -Pusb -xmode=avr
```

In both cases, you can check whether you were successful by typing the same command again. If you get the message that the debugger is still in 'PIC' mode, the firmware of the debug probe is ancient, and you need to [flash new firmware first using MPLAB X](https://arduino-craft-corner.de/index.php/2025/04/16/snap-debugging-for-the-masses/#appendix-installing-a-recent-firmware-version).

## Software simulator

In addition to the above-mentioned debug probes, PyAvrOCD also supports the simulation tool [`simavr`](https://github.com/buserror/simavr) by providing a pass-through service mainly aimed at Arduino IDE 2 users. If you use this IDE, then the way to start the simulator is as follows:

1. Verify/compile your sketch.
2. Choose as the `Programmer` in the `Tools` menu `Simulator (simavr)`.
3. Click on the Debugger icon at the top of the window.

In this case, the simulator will be started instead of making a connection to a hardware probe. As you will notice, this fake programmer cannot be used to program a chip. It is only used to signal that the simulator should be started when debugging is requested.

An alternative way to start `simavr` is to provide a path argument to the `--start` option that has as its last part `simavr`. If you use another IDE other than the Arduino IDE 2, you can trigger that by putting the file `pyavrocd.options` into the project folder containing the two lines

```text
--start
/path/to/simavr-executable
```

Note that the list of chips supported by `simavr` is much smaller than the one supported by PyAvrOCD. Further, the means of interaction are severely limited. However, the simulator solution may sometimes be the more preferable option.

If you are adventurous, try out a few other things with `simavr`. It is possible to pass arguments to `simavr` using the option `--xargs`. For instance, you can trace the changes of a particular memory location, e.g., PORTB on an ATmega328P, where the built-in LED is usually controlled.  Add the following two lines in the file `pyavrocd.options`:

```text
--xargs
--add-trace LED=trace@0x0025/0xff
```

After terminating the debug session (and waiting some time), a [VCD](https://en.wikipedia.org/wiki/Value_change_dump) trace will show up in the project folder. This can be visualized, for instance, with [gtkwave](https://gtkwave.sourceforge.net) or [pulseview](https://sigrok.org/wiki/Downloads). It is also possible to provide VCD files as input. This is all sketched in a [simavr usage note](https://github.com/gatk555/simavr#using).

