# Installing a debug-enabled Arduino core

Arduino cores or platforms are the means to support MCUs and boards for integration into the Arduino IDE 2 (and into the Arduino CLI). They are the key to making debugging for particular chips available in the Arduino IDE 2. Meanwhile, there exists a number of debug-enabled Arduino cores. Sometimes, they are forks, sometimes improved new versions of older cores, and sometimes they are extensions of existing cores. Note that PyAvrOCD can support an MCU, but there is no corresponding core. This means that debugging by means of GDB is possible, but there is no Arduino support (so far).

If you want to install a core, in most cases, you first have to add a *package index json* URL to the list of `Additional boards manager URLs`, which you find in the `Preferences` dialog. Once this has been done, you can search in the `Boards Manager` (accessible through the `Tools` menu or the board icon on the left side of the Arduino IDE 2 window) for the core, and then install it.

### [Arduino AVR Boards (Debug enabled)](https://github.com/felias-fogg/ArduinoCore-avr-debug-enabled)

This is a fork of the official Arduino AVR core 1.8.6, which, among other things, contains the Arduino UNO R3, the Arduino Leonardo, and the Arduino Mega 2560. You get it as an installable core by adding the following URL:

```
 https://downloads.pyavrocd.io/package_debug_enabled_index.json
```

After you have installed this core, you can safely remove the original core `Arduino AVR Boards` in order to avoid confusion. However, you do not have to.

### [ATTinyCore (Debug enabled)](https://github.com/felias-fogg/ATTinyCore-debug-enabled)

This is a fork of Spence Konde's ATTinyCore 2.0.0-dev, which covers all classic ATtinys with a debugWire interface. As above, you can install it after including the following URL

```
 https://downloads.pyavrocd.io/package_debug_enabled_index.json
```

in the additional boards manager URLs. As mentioned in the notes, this core is considered to be a development version. However, this appears to apply mainly to the new bootloaders.

### [Atmel AVR Xplained-minis (Debug enabled)](https://github.com/felias-fogg/avr-xminis-debug-enabled)

This is a debug-enabled Arduino core for the Microchip development boards [ATmega328P Xplained Mini](https://www.microchip.com/en-us/development-tool/atmega328p-xmini), [ATmega168BP Xplained Mini](https://www.microchip.com/en-us/development-tool/atmega168pb-xmini), and [ATmega328PB Xplained Mini](https://www.microchip.com/en-us/development-tool/atmega328pb-xmini). It is meant to be a replacement for the similarly named core in the official Arduino distribution, which is already 10 years old and does not really work. The new core is a stripped-down and adapted version of MCUdude's MiniCore. The boards, together with PyAvrOCD, work very smoothly. It is just plug-and-play. The only thing one must be aware of is that one should power the application circuit attached to the board through the `IOREF` pin (pin 2 of J202 on the Xplained Mini board). Otherwise, the automatic power-cycle feature might not work. Again, you can install this core through the boards manager URL:

```
https://downloads.pyavrocd.io/package_debug_enabled_index.json
```

If you had installed the original core `Atmel AVR Xplained-minis`, you should definitely remove it.

### [MicroCore](https://github.com/MCUdude/MicroCore)

This is a core for the ATtiny13(A). Currently, it is already debug-enabled through [dw-gdbserver](https://github.com/felias-fogg/dw-gdbserver). You can make it installable by adding the following URL to the Boards Manager URLs:

```
https://mcudude.github.io/MicroCore/package_MCUdude_MicroCore_index.json
```

It will be upgraded to work with PyAvrOCD soon.

### [MiniCore](https://github.com/MCUdude/MiniCore)

This is the core for the small ATmegas with a debugWIRE interface, aka, ATmegaX8. As above, it is already debug-enabled through [dw-gdbserver,](https://github.com/felias-fogg/dw-gdbserver) and it will be upgraded to work with PyAvrOCD soon. You can make it installable by adding the following boards manager URL:

```
https://mcudude.github.io/MiniCore/package_MCUdude_MiniCore_index.json
```

### [MightyCore](https://github.com/MCUdude/MightyCore)

An Arduino core for ATmega8535, ATmega16, ATmega32, ATmega164, ATmega324, ATmega644, and ATmega1284, whereby ATmega8353 does not have a debugging interface, and the ATmega16 cannot be debugged with GDB because it has a stuck-to-one bit in the program counter. You can make it installable by adding the following boards manager URL:

```
https://mcudude.github.io/MightyCore/package_MCUdude_MightyCore_index.json
```

The extension of this core is not yet ready.

### [MegaCore](https://github.com/MCUdude/MegaCore)

A core for most 64 and 100-pin AVRs. All of the listed MCUs are debuggable, but the ATmega128 has the problem that only hardware breakpoints are allowed. You can make the core installable by adding:

```
https://mcudude.github.io/MegaCore/package_MCUdude_MegaCore_index.json
```

The extension of this core is not yet ready.

### [MajorCore](https://github.com/MCUdude/MajorCore)

This core covers just ATmega8051 and ATmega162, of which only the latter possesses a debugging interface. The additional board manager URL is:

```
https://mcudude.github.io/MajorCore/package_MCUdude_MajorCore_index.json
```

The extension of this core is not yet ready.