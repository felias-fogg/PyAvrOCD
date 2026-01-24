# Supported boards

Almost all boards equipped with one of the supported chips can be used in one way or another. Tested boards are marked in boldface, and those known not to work are struck out. The ones that are underlined are sitting on my desk and are waiting to be tested. If no core is mentioned, then there is no support yet.

In addition, the board packages supporting the boards, possible board modifications, and other information are mentioned.

Currently, there are only a few cores operational. In the near future, all of MCUdude's cores will be added.


## Microchip boards

Most of the supported Microchip boards have an embedded debugger on board, which makes it easy to work with. You do not have to modify the boards physically or change fuses. When working with debugWIRE targets, the power cycling is done automatically.

- **ATmega328P** **Xplained Mini**:  [Atmel AVR Xplained-minis (Debug enabled)](supporting-cores.md#atmel-avr-xplained-minis-debug-enabled); no physical modifications or fuse settings necessary,  power-cycling is automatic.

- **ATmega168PB** **Xplained Mini**: [Atmel AVR Xplained-minis (Debug enabled)](supporting-cores.md#atmel-avr-xplained-minis-debug-enabled); no physical modifications or fuse settings necessary,  power-cycling is automatic.

- **ATmega328PB** **Xplained Mini**: [Atmel AVR Xplained-minis (Debug enabled)](supporting-cores.md#atmel-avr-xplained-minis-debug-enabled); no physical modifications or fuse settings necessary,  power-cycling is automatic.

- **ATmega324PB Xplained Pro:** Serial I/O is routed via
  `Serial1` instead of `Serial`. The LED is connected to digital
  pin 23. No physical modifications or fuse settings necessary.
- <u>AT90USBKEY2 (AT90USB1287)</u>
- <u>ATmega256RFR2 Xplained Pro</u>
- **AVR Butterfly (ATmega169)**
- <u>MEGA-1284P Xplained</u>



## Arduino boards


- Arduino Yún
- **Arduino UNO R3**:   [MiniCore](supporting-cores.md#minicore), [the `RESET EN` solder bridge needs to be cut](board-preparation.md#preparing-a-debugwire-target)
- Arduino UNO Mini:  [MiniCore](supporting-cores.md#minicore), remove capacitor `C3`
- Arduino Duemilanove:  [MiniCore](supporting-cores.md#minicore), `RESET EN` needs to be cut
- Arduino Diecimila:  [MiniCore](supporting-cores.md#minicore), [remove 100nF capacitor](https://awtfy.com/2010/02/21/modify-an-arduino-for-debugwire/)
- **Arduino Nano:** [100 nF cap and 1kΩ resistor needs to be removed](board-preparation.md#arduino-nano-and-clones)
- **Arduino Mega**: JTAG pins are A4-A7, use [this board adapter](https://github.com/felias-fogg/PyAvrOCD/tree/main/pcbs/arduino-jtag), `RESET EN` does not need to be opened
- **Arduino Mega 2560:** JTAG pins are A4-A7, use [this board adapter](https://github.com/felias-fogg/PyAvrOCD/tree/main/pcbs/arduino-jtag), `RESET EN` does not need to be opened
- Arduino Mega ADK
- **Arduino Leonardo**: JTAG pins are A0-A3, use [this board adapter](https://github.com/felias-fogg/PyAvrOCD/tree/main/pcbs/arduino-jtag)
- Arduino Leonardo ETH
- <u>Arduino Micro</u>
- <s>Arduino Esplora</s>
- Arduino Mini
- Arduino Ethernet
- <u>Arduino Fio</u>:  do not connect DTR pin of FTDI header and do not connect XBee
- Arduino BT:  remove capacitor `C1`
- <s>LilyPad Arduino USB</s>: JTAG pins are not accessible
- <u>LilyPad Arduino</u>:  do not connect DTR pin of FTDI header
- <u>Arduino Pro</u>:  do not connect DTR pin of FTDI header
- <u>Arduino Pro Mini</u>:  do not connect DTR pin of FTDI header
- Arduino NG (ATmega168):  no modifications necessary
- <s>Arduino NG (ATmega8)</s>: no debugging interface
- Arduino Robot Control
- Arduino Robot Motor
- <u>Arduino Gemma</u>:  [ATTinyCore (Debug enabled)](supporting-cores.md#attinycore-debug-enabled), RESET pad on backside
- <u>Adafruit Circuit Playground 32u4</u>
- Arduino Yún Mini
- Arduino Industrial 101
- Arduino Linino One
- Arduino UNO WiFi (Rev 1):  cut `RESET EN` solder bridge

## Supported Sparkfun boards

- RedBoard (ATmega328P): [MiniCore](supporting-cores.md#minicore), remove `C8`
- <u>Pro Micro 3.3V (ATmega32U4)</u>
- <u>Pro Micro 5V (ATmega32U4)</u>
- Fio v3
- Qduino Mini (ATmega32U4)
- Mega Pro 3.3V
- Mega Pro 5V
- RedBot (ATmega328P)
- <u>Serial-7-Segment-Display</u> (ATmega328P)
- ATmega128RFA1 Development board
- LilyPad USB Plus
- SerLcd
- Digital Sandbox (ATmega328P)
- Microview (ATmega328P)

## Supported Adafruit boards

- <s>Flora (ATmega32U4)</s>: JTAG pins are not accessible
- Feather 32U4
- Feather 328P: [MiniCore](supporting-cores.md#minicore)
- Gemma (ATtiny85):  [ATTinyCore (Debug enabled)](supporting-cores.md#attinycore-debug-enabled),
- Trinket 3.3V (ATtiny85): [ATTinyCore (Debug enabled)](supporting-cores.md#attinycore-debug-enabled)
- Trinket 5V (ATtiny85): [ATTinyCore (Debug enabled)](supporting-cores.md#attinycore-debug-enabled)
- Metro (ATmega328P):  [MiniCore](supporting-cores.md#minicore), cut `RESET EN` solder bridge
- Metro Mini V2:  [MiniCore](supporting-cores.md#minicore), you have to figure out which cap to remove
- Circuit Playground Classic (ATmega32U4)
- Pro Trinket 5V/16MHz (USB): MiniCore
- Pro Trinket 3V/12MHz (USB): MiniCore
- Pro Trinket 5V/16MHz (FTDI): MiniCore
- Pro Trinket 3V/12MHz (FTDI): MiniCore
- ItsyBitsy 32u4 (3V)
- ItsyBitsy 32u4 (5V)
- Bluefruit Micro
- ATmega32u4 Breakout Board

## Teensy boards

- <u>Teensy 2.0 (ATmega32U4)</u>
- <u>Teensy++ (AT90USB1286)</u>

## Olimex boards

- Olimex-328: [MiniCore](supporting-cores.md#minicore)
- Olimex-32u4
- <s>eduArdu</s>: JTAG pins are not accessible
- Olimex-Nano: [MiniCore](supporting-cores.md#minicore)
- RGB-Glasses
- Olimexino-2560
- **AVR-CAN (AT90CAN128)**
- AVR-GSM (ATMega32)
- AVR-IO-M16 (ATmega16): MCU has a PC with a stuck-at-one bit
- **AVR-MT128 (ATmega128)**: only hardware breakpoints (!)
- AVR-USB-STK (AT90USB162)
- **AVR-USB-162 (AT90USB162)**

## Seeed Studio boards

- Seeeduino V3.0: [MiniCore](supporting-cores.md#minicore)
- <u>Seeeduino v4</u>:  remove `C14` and RESET LED (next to RESET button)
- <u>Stalker</u>: do not connect DTR
- Seeeduino Lotus
- Seeeduino Lite
- Seeeduino Nano

## Azduino boards by Spence Konde

- **ATtiny841 dev. board**: [ATTinyCore (Debug enabled)](supporting-cores.md#attinycore-debug-enabled)
- **ATtiny1634 dev. board**: [ATTinyCore (Debug enabled)](supporting-cores.md#attinycore-debug-enabled)
- **ATtiny88 breakout board (assembled)**: [ATTinyCore (Debug enabled)](supporting-cores.md#attinycore-debug-enabled)
- **ATtiny828 breakout board (assembled)**: [ATTinyCore (Debug enabled)](supporting-cores.md#attinycore-debug-enabled)
- **ATtiny167 dev. board**: [ATTinyCore (Debug enabled)](supporting-cores.md#attinycore-debug-enabled)
- **ATtiny43 dev. board**: [ATTinyCore (Debug enabled)](supporting-cores.md#attinycore-debug-enabled)

