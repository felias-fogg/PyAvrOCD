# Supported debug probes

PyAvrOCD has been built to provide access to AVR OCDs by means of Microchip's debug probes. In addition, it also provides an interface to some DIY debug probes.

## Hardware debug probes

The following debug probes use the HID USB protocol and can be used without installing any drivers:


* **[MPLAB PICkit 4 In-Circuit Debugger](https://www.microchip.com/en-us/development-tool/pg164140)** ([when in 'AVR mode'](#switching-to-avr-mode)),
* **[MPLAB Snap In-Circuit Debugger](https://www.microchip.com/en-us/development-tool/pg164100)** ([when in 'AVR mode'](#switching-to-avr-mode)),
* [**Atmel-ICE**](https://www.microchip.com/en-us/development-tool/atatmel-ice),
* **[Power Debugger](https://www.microchip.com/en-us/development-tool/atpowerdebugger)**,
* [**JTAGICE3**](https://www.microchip.com/en-us/development-tool/atjtagice3) (firmware version 3.0 or newer),

* [**EDBG**](http://content.alexandria.atmel.com/webhelp/GUID-43D69EB5-28C5-4F23-97B7-43CD3961DC33-en-US-3/index.html?GUID-180AB3C3-775A-482F-961D-D9862473CD85) - on-board debuggers on Xplained Pro/Ultra boards,
* [**mEDBG**](https://onlinedocs.microchip.com/oxy/GUID-FC2A0384-AC9D-45B4-951E-5C0DEFE8B2E9-en-US-5/GUID-4063E88C-69CE-4393-ABBF-46E406D92BD3.html) - on-board debuggers on Xplained Mini/Nano boards,
* [**nEDBG**](https://onlinedocs.microchip.com/oxy/GUID-B4A268FD-55AC-4EA1-A026-5F06B0F3D18E-en-US-1/index.html) - on-board debuggers on Curiosity Nano boards (can also be used stand-alone to debug other UPDI targets),
* [**microUPDI**](https://github.com/MCUdude/microUPDI) - a debugger for UPDI targets based on the mEDBG firmware. It does not work on the Dx-/Ex-/Sx-series chips. And in order to debug on 0-series ATmegas, you need the most recent firmware 1.19.57, which you get from the [microUPDIcore](https://github.com/MCUdude/microUPDIcore) repo. Note that you can use the firmware on any ATmega32U4 development board without additional hardware if you do not need any level-shifting for the serial line. 

In addition, the following probes are supported, which rely on the USB bulk transport mechanism:


* **[AVR Dragon](https://www.microchip.com/en-us/development-tool/atavrdragon)** (firmware version 7.0 or newer),
* [**AVR JTAGICE mkII**](https://www.microchip.com/en-us/development-tool/atjtagice2) (firmware version 7.0 or newer).

Note that under Windows, you may have to install the WinUSB driver using [Zadig](https://zadig.akeo.ie).

Finally, there are debug probes that use the serial line:


* **[dw-link](https://felias-fogg.github.io/dw-link)** (firmware version 7 or newer) - DIY debugger running on an Arduino UNO R3 (only debugWIRE), which uses a variant of the JTAGICE mkÍI protocol.

## Switching to AVR mode

Note that Snap and PICkit4 need to be switched to 'AVR mode'. This can be accomplished as follows by using avrdude (>= Version 7.3):

```
avrdude -c snap_isp -Pusb -xmode=avr
```

With PICkit4, it is similar:

```
avrdude -c pickit4_isp -Pusb -xmode=avr
```

In both cases, you can check whether you were successful by typing the same command again. If you get the message that the debugger is still in 'PIC' mode, the firmware of the debug probe is ancient, and you need to [flash new firmware first using MPLAB X](https://arduino-craft-corner.de/index.php/2025/04/16/snap-debugging-for-the-masses/#appendix-installing-a-recent-firmware-version).

## Downgrading more recent debug probes

If you do not own one of the above debug probes, but you own a [PICkit5](https://www.microchip.com/en-us/development-tool/PG164150) or [PICkit Basic](https://www.microchip.com/en-us/development-tool/PG164110), you can consider [downgrading](https://arduino-craft-corner.de/index.php/2026/05/25/downgrading-your-pickit5/) it to a PICkit4 or SNAP, respectively.
