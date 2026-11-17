# Debug-capable Arduino packages

Arduino packages are the key to making debugging available in the *Arduino IDE 2* and the *Arduino Maker Workshop*. You can distinguish them along two dimensions. The first one is the dimension of who maintains the **debug-capable package**. Some of them are **original packages**, maintained by their authors. Others are **forks** of existing packages. The second dimension is how much debug support is integrated into the package. Some are **debug-configured**, meaning that all configuration files have been provided, but the binary debugging tools are missing. For those packages, it is necessary to additionally install the **AvrDebugger board package**. A package is called **debug-ready **when it contains all the configuration files as well as the binary tools.

Up until version 1.7.0, all debug-capable packages had been *debug-ready*. Starting with 2.0.0, new versions of debug-capable packages are set up to be *debug-configured*. The main reasons behind this are that it saves considerable disk space and it allows for centralized updates of the debugging tools.

If you want to install such a debug-capable package, you first have to add a new *boards manager* URL in the `Preferences` dialog.

{!details-boards-manager-url.md!}

Once this has been done, you can search in the <code>Boards Manager</code> for the package and install it or upgrade to the most recent version. In case of a debug-capable fork, the version number is usually suffixed by `-preX,` and the name of the package will have `(Debug capable)` attached to the official name.

{!details-install-package.md!}

## Debug-ready packages

<a id=avrdebugger></a>

### [AvrDebugger](https://github.com/felias-fogg/AvrDebugger)

This is a package that inherits most of its properties from Arduino's AVR Board package. The main difference is that it provides more programmers and has the configurations set up to start a debugger on a limited set of the classic Arduino boards. Most importantly, it provides the debugging tools *PyAvrOCD*, a patched version of *avr-gdb*, and *simavr*.  The plan is to make AvrDebugger the central package for supplying the debugging tools. That means that the other packages mentioned in this section are supposed to slowly migrate to the section with packages of type 2.

### [TinyCore](https://github.com/MCUdude/TinyCore)

This is a fork of ATTinyCore version 2.0.0. It is the preferred way of supporting classic ATtinys.  <s>It does not yet support the micronucleus bootloaders, however.</s> Debugging support has been integrated starting with the release of v0.0.1. You can install it after including the following URL:

```
https://mcudude.github.io/TinyCore/package_MCUdude_TinyCore_index.json
```

### [MicroCore](https://github.com/MCUdude/MicroCore)

This is a package for the ATtiny13(A). Debugging support is integrated since version 2.5.0. You can make it installable by adding the following URL to the Boards Manager URLs:

```
https://mcudude.github.io/MicroCore/package_MCUdude_MicroCore_index.json
```

### [MiniCore](https://github.com/MCUdude/MiniCore)

This is the package for the small ATmegas with a debugWIRE interface, aka, ATmegaX8. PyAvrOCD has been integrated into the package since version 3.1.0. You can make the package installable by adding the following *boards manager URL*:

```
https://mcudude.github.io/MiniCore/package_MCUdude_MiniCore_index.json
```

### [MightyCore](https://github.com/MCUdude/MightyCore)

An Arduino package for ATmega8535, ATmega16, ATmega32, ATmega164, ATmega324, ATmega644, and ATmega1284, whereby ATmega8535 does not have a debugging interface. Debugging is supported since version 3.1.0. You can make it installable by adding the following *boards manager URL*:

```
https://mcudude.github.io/MightyCore/package_MCUdude_MightyCore_index.json
```

### [MegaCore](https://github.com/MCUdude/MegaCore)

A package for most 64- and 100-pin AVRs. For example, the Arduino Mega (2560) is supported by this package. All of the [listed MCUs](https://github.com/MCUdude/MegaCore#supported-microcontrollers) are debuggable, but the ATmega128 has the problem that only hardware breakpoints are allowed. Debugging is supported since version 3.1.0. You can make the package installable by adding the foolowing URL to the *boards manager URL*:

```
https://mcudude.github.io/MegaCore/package_MCUdude_MegaCore_index.json
```

### [MajorCore](https://github.com/MCUdude/MajorCore)

This package covers just ATmega8515 and ATmega162, of which only the latter possesses a debugging interface. Debugging is supported since version 3.1.0. The additional *boards manager URL* is:

```
https://mcudude.github.io/MajorCore/package_MCUdude_MajorCore_index.json
```

### [MegaCoreX](https://github.com/felias-fogg/MegaCoreX)

This is a fork of the package for the megaAVR-0 chip family, such as the ATmega4809, which is used on the Nano Every Board and the Uno WiFi Rev 2. You can make the debug-enabled fork of the package available using the following URL:

```
https://mcudude.github.io/MegaCoreX/package_MCUdude_MegaCoreX_index.json
```

## Debug-configured packages

### [XMiniCore](https://github.com/felias-fogg/XMiniCore)

This is a debug-enabled Arduino package for the Microchip development boards [ATmega328P Xplained Mini](https://www.microchip.com/en-us/development-tool/atmega328p-xmini), [ATmega168BP Xplained Mini](https://www.microchip.com/en-us/development-tool/atmega168pb-xmini), and [ATmega328PB Xplained Mini](https://www.microchip.com/en-us/development-tool/atmega328pb-xmini). It is meant to be a replacement for the *Atmel AVR Xplained-minis* board package of the official Arduino distribution. The new package is a stripped-down and adapted version of MiniCore. The boards, together with PyAvrOCD, work very smoothly (see [quickstart guide for ATmega328P Xplained Mini](quick_arduino.md#quickstart-atmega328p-xplained-mini)). It is just plug-and-play. You can make the board package available by including the following boards manager URL:

```
https://felias-fogg.github.io/XMiniCore/package_felias-fogg_XMiniCore_index.json
```

As with all the other boards in this section, you also need to install the `AvrDebugger` package.

## Debug-ready forks

<a id=arduino-avr-boards></a>
### [Arduino AVR Boards](https://github.com/felias-fogg/ArduinoCore-avr) (debug-capable)

This is the debug-enabled fork of the standard Arduino package, which supports all Arduino AVR boards. The only changes are

- additional programmers,
- changes to platform.txt to enable debugging,
- changes to boards.txt to enable the JTAG pins on boards with the JTAG interface, and
- an upgrade to version 8.0 of avrdude.

You can make this fork available by including:
```
https://felias-fogg.github.io/ArduinoCore-avr/package_felias-fogg_ArduinoCore-avr_index.json
```

Since the AvrDebugger board package is very similar in intention and coverage, this package will be retired soon.

<a id=arduino-megaavr-boards></a>

### [Arduino megaAVR Boards](https://github.com/felias-fogg/ArduinoCore-megaavr) (debug-capable)

This is the debug-enabled fork of the megaAVR Arduino package, which supports the Nano Every as well as the Uno Wifi Rev2 boards. Note that these are also supported (offering more configuration options) by [MegaCoreX](#megacorex). The only changes to the upstream repo are:

- additional programmers,
- changes to platform.txt to enable debugging,
- change to boards.txt to set the default programmer for the Uno Wifi Rev2, and
- an upgrade to version 8.0 of avrdude.

You can make this fork available by including:

```
https://felias-fogg.github.io/ArduinoCore-megaavr/package_felias-fogg_ArduinoCore-megaavr_index.json
```

<a id=megatinycore></a>

### [megaTinyCore](https://github.com/felias-fogg/megaTinyCore) (debug-capable)

This is a fork of the package for modern ATiny Chips (series 0, 1, and 2). Make the debug-enabled fork available using the following URL:

```
https://felias-fogg.github.io/megaTinyCore/package_SpenceKonde_megaTinyCore_index.json
```

<a id=dxcore></a>
### [DxCore](https://github.com/felias-fogg/DxCore) (debug-capable)

This is a fork of DxCore, the package for the most recently marketed AVR chips. Make the debug-enabled fork available by using:

```
https://felias-fogg.github.io/megaTinyCore/package_SpenceKonde_DxCore_index.json
```

<a id=attinycore></a>

### [ATTinyCore](https://github.com/felias-fogg/ATTinyCore) (debug-capable)

This is a debug-enabled fork of ATTinyCore version 1.5.2, which covers all classic ATtinys with a debugWire interface. Nowadays, [TinyCore (see above)](#tinycore) is the preferred package for classic ATtinys. You can make this fork available by including the following URL:

```
https://felias-fogg.github.io/ATTinyCore/package_drazzy.com_ATTinyCore_index.json
```

## Debug-configured forks

Currently, there are no such packages. But this will change quickly.
