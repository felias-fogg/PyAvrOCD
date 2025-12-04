# Supported boards

Almost all boards equipped with one of the supported chips can be used in one way or another. Tested boards are marked in boldface, and those known not to work are struck out. The ones that are underlined are sitting on my desk and are waiting to be tested.

In addition, the board packages supporting the boards, possible board modifications, and other information are mentioned.

Currently, there are only a few cores operational. In the near future, all of MCUdude's Mega cores will be added.


## Supported Microchip boards

Most of the supported Microchip boards have an embedded debugger on board, which makes it easy to work with. You do not have to modify the boards physically or change fuses. When working with debugWIRE targets, the power cycling is done automatically.

- **ATmega328P** **Xplained Mini**:  Supported by `Atmel AVR Xplained-minis (Debug enabled)`; no physical modifications or fuse settings necessary

- **ATmega168PB** **Xplained Mini**: Supported by  `Atmel AVR Xplained-minis (Debug enabled)`; no physical modifications or fuse settings necessary

- **ATmega328PB** **Xplained Mini**: Supported by  `Atmel AVR Xplained-minis (Debug enabled)`; no physical modifications or fuse settings necessary

- **ATmega324PB Xplained Pro:** No core yet. Serial I/O is routed via `Serial1` instead of `Serial`. The LED is connected to digital pin 23. No physical modifications or fuse settings necessary
- <u>AT90USBKEY2 (AT90USB1287)</u>: no core yet
- <u>ATmega256RFR2 Xplained Pro</u>: no core yet. 
- <u>AVR Butterfly (ATmega169)</u>: no core yet.
- <u>MEGA-1284P Xplained</u>: no core yet.



## Supported Arduino boards


- Arduino Yún: Supported by `Arduino AVR Boards (Debug enabled)`
- **Arduino UNO R3**: Supported by `Arduino AVR Boards (Debug enabled)`;  [the `RESET EN` solder bridge needs to be cut](https://felias-fogg.github.io/PyAvrOCD/board-preparation/#preparing-a-debugwire-target)
- Arduino UNO Mini: Supported by `Arduino AVR Boards (Debug enabled)`; remove capacitor `C3`
- Arduino Duemilanove: Supported by `Arduino AVR Boards (Debug enabled)`; `RESET EN` needs to be cut
- Arduino Diecimila: Supported by `Arduino AVR Boards (Debug enabled)`; [remove 100nF capacitor](https://awtfy.com/2010/02/21/modify-an-arduino-for-debugwire/)
- **Arduino Nano:** Supported by `Arduino AVR Boards (Debug enabled)`; [only clones can be modified](https://mtech.dk/thomsen/electro/arduino.php)
- **Arduino Mega**: Supported by `Arduino AVR Boards (Debug enabled)`
- **Arduino Mega 2560:** Supported by `Arduino AVR Boards (Debug enabled)`
- Arduino Mega ADK: Supported by `Arduino AVR Boards (Debug enabled)`
- <u>Arduino Leonardo</u>: Supported by `Arduino AVR Boards (Debug enabled)`
- Arduino Leonardo ETH: Supported by `Arduino AVR Boards (Debug enabled)`
- <u>Arduino Micro</u>: Supported by `Arduino AVR Boards (Debug enabled)`
- <s>Arduino Esplora</s>: JTAG pins are not accessible
- Arduino Mini: Supported by `Arduino AVR Boards (Debug enabled)`; do not connect DTR pin of FTDI header
- Arduino Ethernet: Supported by `Arduino AVR Boards (Debug enabled)`; do not connect DTR pin of FTDI header
- <u>Arduino Fio</u>: Supported by `Arduino AVR Boards (Debug enabled)`; do not connect DTR pin of FTDI header and do not connect XBee
- Arduino BT: Supported by `Arduino AVR Boards (Debug enabled)`; remove capacitor `C1`
- <s>LilyPad Arduino USB</s>: JTAG pins are not accessible
- <u>LilyPad Arduino</u>: Supported by `Arduino AVR Boards (Debug enabled)`; do not connect DTR pin of FTDI header
- <u>Arduino Pro</u>: Supported by `Arduino AVR Boards (Debug enabled)`; do not connect DTR pin of FTDI header
- <u>Arduino Pro Mini</u>: Supported by `Arduino AVR Boards (Debug enabled)`; do not connect DTR pin of FTDI header
- Arduino NG (ATmega168): Supported by `Arduino AVR Boards (Debug enabled)`; no modifications necessary
- <s>Arduino NG (ATmega8)</s>: no debugging interface
- Arduino Robot Control: Supported by `Arduino AVR Boards (Debug enabled)`
- Arduino Robot Motor: Supported by `Arduino AVR Boards (Debug enabled)`
- <u>Arduino Gemma</u>: Supported by `Arduino AVR Boards (Debug enabled)`; RESET pad on backside
- <u>Adafruit Circuit Playground 32u4</u>: Supported by `Arduino AVR Boards (Debug enabled)`
- Arduino Yún Mini: Supported by `Arduino AVR Boards (Debug enabled)`
- Arduino Industrial 101: Supported by `Arduino AVR Boards (Debug enabled)`
- Arduino Linino One: Supported by `Arduino AVR Boards (Debug enabled)`
- Arduino UNO WiFi (Rev 1): Supported by `Arduino AVR Boards (Debug enabled)`; cut `RESET EN` solder bridge

## Supported Sparkfun boards

- RedBoard (ATmega328P): Supported by `Arduino AVR Boards (Debug enabled)`; remove `C8`
- <u>Pro Micro 3.3V (ATmega32U4)</u>: 
- <u>Pro Micro 5V (ATmega32U4)</u>: 
- Qduino Mini (ATmega32U4): 
- Mega Pro 3.3V/5V: 
- RedBot (ATmega328P): Supported by `Arduino AVR Boards (Debug enabled)`
- ATmega128RFA1 Development board: no core yet
- <u>Serial-7-Segment-Display</u> (ATmega328P): no core yet
- LilyPad USB Plus: no core yet
- Digital Sandbox (ATmega328P)
- Microview (ATmega328P)

## Supported Adafruit boards

- ATmega32u4 Breakout Board: no core yet
- Circuit Playground Classic (ATmega32U4):  `Arduino AVR Boards (Debug enabled)`
- Feather 32U4 Basic Proto: no core yet
- Feather 32u4 Bluefruit LE: no core yet
- Feather 32u4 FONA: no core yet
- Feather 328P: Supported by `Arduino AVR Boards (Debug enabled)`
- <s>FLORA (ATmega32U4)</s>: JTAG pins are not accessible
- Gemma (ATtiny85):  `ATTinyCore (Debug enabled)`, `Arduino AVR Boards (Debug enabled)`
- ItsyBitsy 32u4 (3V/5V): no core yet
- Metro (ATmega328P): Supported by `Arduino AVR Boards (Debug enabled)`; cut `RESET EN` solder bridge
- Metro Mini 328P V2: Supported by `Arduino AVR Boards (Debug enabled)`; you have to figure out which cap to remove
- Teensy 2.0 (ATmega32U4): no core yet
- <u>Teensy++ (AT90USB1286)</u>: no core yet
- Trinket - Mini Microcontroller 3.3V/5V Logic: Supported by `ATTinyCore (Debug enabled)`
- Pro Trinket - 5V 16MHz/ 3.3V 12 MHz (ATmega328P): 
- Pro Trinket FTDI - 5V 16MHz/ 3.3V 12 MHz (ATmega328P): 
- Bluefruit Micro (ATmega32U4): no core yet

## Supported Olimex boards

- <u>AVR-CAN (AT90CAN128)</u>: no core yet
- AVR-GSM (ATMega32): no core yet
- <s>AVR-IO-M16 (ATmega16)</s>: MCU has a PC with a stuck-at-one bit
- <u>AVR-MT128 (ATmega128)</u>: no core yet, only hardware breakpoints (!)
- AVR-USB-STK (AT90USB162): no core at all!
- <u>AVR-USB-162 (AT90USB162)</u>: no core at all!

## Supported Seeed Studio boards

- <u>Seeeduino v4.2</u>: Supported by `Arduino AVR Boards (Debug enabled)`; remove `C14` and RESET LED (next to RESET button)
- <u>Stalker</u>: Supported by `Arduino AVR Boards (Debug enabled)`; do not connect DTR
- Seeeduino Lotus: Supported by `Arduino AVR Boards (Debug enabled)`
- Seeeduino Nano: Supported by `Arduino AVR Boards (Debug enabled)`

## Supported Azduino boards by Spence Konde

- **ATtiny841 dev. board**: Supported by `ATTinyCore (Debug enabled)`
- **ATtiny1634 dev. board**: Supported by `ATTinyCore (Debug enabled)`
- **ATtiny88 breakout board (assembled)**: Supported by `ATTinyCore (Debug enabled)`
- **ATtiny828 breakout board (assembled)**: Supported by `ATTinyCore (Debug enabled)`

- **ATtiny167 dev. board**: Supported by `ATTinyCore (Debug enabled)`
- **ATtiny43 dev. board**: Supported by `ATTinyCore (Debug enabled)`
