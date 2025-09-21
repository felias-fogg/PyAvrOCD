# Supported boards

All boards equipped with one of the supported chips can be used in
one way or another. As usual, tested boards are marked in boldface,
and those known not to work are struck out. In addition, the board
packages supporting the boards and possible board modifications are
mentioned.


### Supported Microchip boards

The supported Microchip boards all have an embedded debugger on board, which makes it easy to work with. You do not have boards physically or, e.g., to change fuses in SPI before switching to JTAG. When working with debugWIRE targets, the power-cycling is done automatically.

- **ATmega328P**, **ATmega168PB**, and **ATmega328PB** **Xplained Mini**: Supported by MiniCore; choose `16 MHz external`, `no bootloader`, the correct `variant`, and as the `Programmer` `Xplained Mini`. The `port` should be set to the USB port opened by the board. You can upload code to the board using the command `Upload Using Programmer`. Serial I/O can be used via the `Serial Monitor` of the IDE. Debugging can be activated by simply using the debugging button. Power-cycling (for enabling debugWIRE mode) is done automatically. Note that you can plug Arduino shields on top of the boards if you solder headers to the boards.
- **ATmega324PB Xplained Pro:** No core yet. Serial I/O is routed via `Serial1` instead of `Serial`. The LED is connected to digital pin 23.
- AT90USBKEY (AT90USB1287): no core yet
- ATmega256RFR2 Xplained Pro: no core yet
- **<u>AVR Butterfly (ATmega169)</u>**: no core yet



### Supported Arduino boards


- Arduino Yún
- **Arduino UNO R3**: Supported by MiniCore;  [the `RESET EN` solder bridge needs to be cut](https://felias-fogg.github.io/PyAvrOCD/board-preparation/#preparing-a-debugwire-target)
- Arduino UNO Mini: Supported by MiniCore; remove capacitor `C3`
- Arduino Duemilanove: Supported by MiniCore; `RESET EN` needs to be cut
- Arduino Diecimila: Supported by MiniCore; [remove 100nF capacitor](https://awtfy.com/2010/02/21/modify-an-arduino-for-debugwire/)
- **Arduino Nano:** Supported by Minicore; [only clones can be modified](https://mtech.dk/thomsen/electro/arduino.php)
- **Arduino Mega**: no core yet
- **Arduino Mega 2560:** no core yet
- Arduino Mega ADK: no core yet
- **Arduino Leonardo**: no core yet
- Arduino Leonardo ETH: no core yet
- Arduino Micro: no core yet
- <s>Arduino Esplora</s>s: JTAG pins are not accessible
- Arduino Mini: Supported by MiniCore; do not connect DTR pin of FTDI header
- Arduino Ethernet (Rev1): MiniCore; do not connect DTR pin of FTDI header
- Arduino Fio: MiniCore; do not connect DTR pin of FTDI header and do not connect XBee
- Arduino BT: MiniCore; remove capacitor `C1`
- LilyPad Arduino USB: no core yet
- LilyPad Arduino: MiniCore; do not connect DTR pin of FTDI header
- Arduino Pro: MiniCore; do not connect DTR pin of FTDI header
- **Arduino Pro Mini**: MiniCore; do not connect DTR pin of FTDI header
- Arduino NG (ATmega168): MiniCore; no modifications necessary
- <s>Arduino NG (ATmega8)</s>: no debugging interface
- Arduino Robot Control: no core yet
- Arduino Robot Motor: no core yet
- **Arduino Gemma**: ATTinyCore; RESET pad on backside
- **Adafruit Circuit Playground 32u4**: no core yet
- Arduino Yún Mini: no core yet
- Arduino Industrial 101: no core yet
- Arduino Linino One: no core yet
- Arduino UNO WiFi (Rev 1): MiniCore; cut `RESET EN` solder bridge

