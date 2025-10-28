# Supported boards

Almost all boards equipped with one of the supported chips can be used in
one way or another. Tested boards are marked in boldface,
and those known not to work are struck out. The ones that are underlined are sitting on my desk and are waiting to be tested.

In addition, the board packages supporting the boards, possible board modifications, and other information are mentioned.


## Supported Microchip boards

The supported Microchip boards all have an embedded debugger on board, which makes it easy to work with. You do not have to modify the boards physically or change fuses. When working with debugWIRE targets, the power cycling is done automatically.

- **ATmega328P** **Xplained Mini**,

- **ATmega168PB** **Xplained Mini**, and

- **ATmega328PB** **Xplained Mini**: Supported by [MiniCore](https://github.com/MCUdude/MiniCore); choose `16 MHz external`, `no bootloader`, the correct `variant`, and as the `Programmer` `Xplained Mini`. The `port` should be set to the USB port opened by the board. You can upload code to the board using the command `Upload Using Programmer`. Serial I/O can be used via the `Serial Monitor` of the IDE. Power-cycling (for enabling debugWIRE mode) is done automatically. For these boards, it makes sense to use `--atexit leavedebugwire` because then one can use the much faster upload via SPI programming.

- **ATmega324PB Xplained Pro:** No core yet. Serial I/O is routed via `Serial1` instead of `Serial`. The LED is connected to digital pin 23.
- AT90USBKEY (AT90USB1287): no core yet
- ATmega256RFR2 Xplained Pro: no core yet
- <u>AVR Butterfly (ATmega169)</u>: no core yet
- MEGA-1284P Xplained: no core yet



## Supported Arduino boards


- Arduino Yún: no core yet
- **Arduino UNO R3**: Supported by [MiniCore](https://github.com/MCUdude/MiniCore);  [the `RESET EN` solder bridge needs to be cut](https://felias-fogg.github.io/PyAvrOCD/board-preparation/#preparing-a-debugwire-target)
- Arduino UNO Mini: Supported by [MiniCore](https://github.com/MCUdude/MiniCore); remove capacitor `C3`
- Arduino Duemilanove: Supported by [MiniCore](https://github.com/MCUdude/MiniCore); `RESET EN` needs to be cut
- Arduino Diecimila: Supported by [MiniCore](https://github.com/MCUdude/MiniCore); [remove 100nF capacitor](https://awtfy.com/2010/02/21/modify-an-arduino-for-debugwire/)
- **Arduino Nano:** Supported by [Minicore](https://github.com/MCUdude/MiniCore); [only clones can be modified](https://mtech.dk/thomsen/electro/arduino.php)
- **Arduino Mega**: no core yet
- **Arduino Mega 2560:** no core yet
- Arduino Mega ADK: no core yet
- <u>Arduino Leonardo</u>: no core yet
- Arduino Leonardo ETH: no core yet
- <u>Arduino Micro</u>: no core yet
- <s>Arduino Esplora</s>: JTAG pins are not accessible
- Arduino Mini: Supported by [MiniCore](https://github.com/MCUdude/MiniCore); do not connect DTR pin of FTDI header
- Arduino Ethernet (Rev1): [MiniCore](https://github.com/MCUdude/MiniCore); do not connect DTR pin of FTDI header
- <u>Arduino Fio</u>: [MiniCore](https://github.com/MCUdude/MiniCore); do not connect DTR pin of FTDI header and do not connect XBee
- Arduino BT: [MiniCore](https://github.com/MCUdude/MiniCore); remove capacitor `C1`
- <s>LilyPad Arduino USB</s>: JTAG pins are not accessible
- <u>LilyPad Arduino</u>: [MiniCore](https://github.com/MCUdude/MiniCore); do not connect DTR pin of FTDI header
- <u>Arduino Pro</u>: [MiniCore](https://github.com/MCUdude/MiniCore); do not connect DTR pin of FTDI header
- <u>Arduino Pro Mini</u>: [MiniCore](https://github.com/MCUdude/MiniCore); do not connect DTR pin of FTDI header
- Arduino NG (ATmega168): [MiniCore](https://github.com/MCUdude/MiniCore); no modifications necessary
- <s>Arduino NG (ATmega8)</s>: no debugging interface
- Arduino Robot Control: no core yet
- Arduino Robot Motor: no core yet
- <u>Arduino Gemma</u>: [ATTinyCore for](https://github.com/felias-fogg/ATTinyCore)k; RESET pad on backside
- <u>Adafruit Circuit Playground 32u4</u>: no core yet
- Arduino Yún Mini: no core yet
- Arduino Industrial 101: no core yet
- Arduino Linino One: no core yet
- Arduino UNO WiFi (Rev 1): [MiniCore](https://github.com/MCUdude/MiniCore); cut `RESET EN` solder bridge

## Supported Sparkfun boards

- RedBoard (ATmega328P): MiniCore; remove `C8`
- <u>Pro Micro 3.3V (ATmega32U4)</u>: no core yet
- <u>Pro Micro 5V (ATmega32U4)</u>: no core yet
- Qduino Mini (ATmega32U4): no core yet
- Mega Pro 3.3V/5V: no core yet
- RedBot (ATmega328P): MiniCore
- ATmega128RFA1 Development board: no core yet
- Serial-7-Segment-Display (ATmega328): MiniCore
- LilyPad USB Plus: no core yet

## Supported Adafruit boards

- ATmega32u4 Breakout Board: no core yet
- Feather 32U4 Basic Proto: no core yet
- Feather 32u4 Bluefruit LE: no core yet
- Feather 32u4 FONA: no core yet
- Feather 328P: MiniCore
- <s>FLORA (ATmega32U4)</s>: JTAG pins are not accessible
- ItsyBitsy 32u4 (3V/5V): no core yet
- Metro (ATmega328P): MiniCore; cut `RESET EN` solder bridge
- Metro Mini 328P V2: MiniCore; you have to figure out which cap to remove
- Teensy 2.0 (ATmega32U4): no core yet
- <u>Teensy++ (AT90USB1286)</u>: no core yet
- Trinket - Mini Microcontroller 3.3V/5V Logic: ATTinyCore fork
- Pro Trinket - 5V 16MHz (ATmega328P): MiniCore

## Supported Olimex boards

- <u>AVR-CAN (AT90CAN128)</u>: no core yet
- AVR-GSM (ATMega32): no core yet
- <s>AVR-IO-M16 (ATmega16)</s>: MCU has a PC with a stuck-at-one bit
- <u>AVR-MT128 (ATmega128)</u>: no core yet, only hardware breakpoints (!)
- AVR-USB-STK (AT90USB162): no core at all!
- <u>AVR-USB-162 (AT90USB162)</u>: no core at all!

## Supported Seeed Studio boards

- <u>Seeeduino v4.2</u>: MiniCore; remove `C14` and RESET LED (next to RESET button)
- <u>Stalker</u>: MiniCore; do not connect DTR
- Seeeduino Lotus: MiniCore
- Seeeduino Nano: MiniCore

## Supported Azduino boards by Spence Konde

- **ATtiny841 dev. board**: [ATTinyCore fork](https://github.com/felias-fogg/ATTinyCore)
- **ATtiny1634 dev. board**: [ATTinyCore fork](https://github.com/felias-fogg/ATTinyCore)
- **ATtiny88 breakout board (assembled)**: [ATTinyCore fork](https://github.com/felias-fogg/ATTinyCore)
- **ATtiny828 breakout board (assembled)**: [ATTinyCore fork](https://github.com/felias-fogg/ATTinyCore)

- **ATtiny167 dev. board**: [ATTinyCore fork](https://github.com/felias-fogg/ATTinyCore)
- **ATtiny43 dev. board**: [ATTinyCore fork](https://github.com/felias-fogg/ATTinyCore)
