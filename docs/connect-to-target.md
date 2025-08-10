# Connecting the hardware debugger to a target

The hardware debuggers have different connectors. The Microchip debuggers Snap and PICkit4 have an eight-pin SIL connector, which is not compatible with any AVR debug connector. Pin 1 is marked by a triangle. If you want to connect to your target board with a standard SPI or JTAG cable, you can buy an adapter board for AVR connectors from Microchip, as shown in the following picture.

![Snap adapter](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/SNAP-adapter.JPG)

Atmel-ICE, Power Debugger, and JTAGICE3 all feature a keyed 10-pin, 50-mil JTAG header. For the Atmel debuggers, adapters are either already included or must be purchased separately.

![Atmel-ICE adapter](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/Atmel-adapter.JPG)

The [dw-link](https://github.com/felias-fogg/dw-link) debugger uses the header on the Arduino Uno. If a dw-link shield is used, one can use the standard 6-pin SPI header.

![dw-link](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/dw-link.jpeg)

Finally, all EDBG debuggers are easy to use. Since they are embedded debuggers, the connection to the target is already on the board.

Depending on which debugging interface the target has, the target board may provide a standard debugging header for this interface. I very much prefer to work with target boards that have the appropriate debugging headers on board. Otherwise, you may easily confuse a connection, and then nothing works. For this reason, I designed some adapter boards for the Arduino Mega and Leonardo. If you have standard headers on the target and the debugger has those (perhaps via adapter PCBs) as well, then the connection is simply to plug in the cable into both headers.

If you do not have the standard headers on board or you are using a breadboard, then you have to connect each line using a jumper cable or the Atmel squid cable, as shown in the following picture.

![picki4-connect](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pickit4-connect.png)

In this case, it is essential to consult the user guide of the programmer and the pinout of the MCU in the datasheet to make the correct connections.

## Connecting to a debugWIRE target

In principle, only two wires are necessary to connect your hardware debugger to a target chip or board: the debugWIRE line, which is the target chip's RESET line, and GND. Since the debugger also needs to know which voltage the target board uses, the Vcc line is also necessary. Note that none of the commercial debuggers source the target. They only have voltage-sensing lines to drive the level-shifting hardware.

Since one also wants to change into and out of debugWIRE mode, change fuses, or upload firmware, it is necessary to connect all 6 SPI programming lines to the target: VTG, GND, RESET, MOSI, MISO, and SCK. For this reason, using all SPI programming lines makes a lot of sense. Moreover, most of the time, an SPI connector is already on the target board.

### SPI programming header

There are two types of SPI programming connectors. The more recent type has six pins, and the older type has 10 pins, as shown in the following diagram (based on a diagram from Wikipedia (https://commons.wikimedia.org/wiki/File:Isp_headers.svg), which provides a top view of the headers on a PCB.

![ISP headers](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/Isp_headers.svg.png)

Note the notches on the left side of the headers. Since almost all SPI programming plugs are keyed, you can only plug them in in the correct orientation. However, the headers sometimes do not have notches. In this case, pin 1 is usually marked in some way, either with a dot, a star, or with the number 1. Similarly, plugs also come unkeyed. In this case, again, pin 1 is marked in some way.

#### Connecting to targets with an SPI programming header

If the target board has an SPI programming header, it is easy to connect to it. Simply use the SPI programming cable and plug it into the target board's header. Be aware of the correct orientation when the header is not keyed! However, if you plug it in the wrong way, nothing will be destroyed.

![atmel-ice-connect](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/atmel-ice-connect.png)


#### Connecting to targets without an SPI programming header

If the target does not feature an SPI programming header, you need to connect 6 cables. If you are working with a breadboard, you may consider buying an [SPI header breadboard adapter](https://www.adafruit.com/product/1465). Otherwise, you need to connect each pin individually. **Atmel-ICE**, **Power Debugge**r, and **JTAGICE3** have a so-called 10-pin mini-squid cable. The pin mapping for those debuggers is as follows.

| Atmel Debugger | Mini-squid pin | Target pin        | SPI pin |
| -------------- | -------------- | ----------------- | ------- |
| Pin 1 (TCK)    | 1              | SCK               | 3       |
| Pin 2 (GND)    | 2              | GND               | 6       |
| Pin 3 (TDO)    | 3              | MISO              | 1       |
| Pin 4 (VTG)    | 4              | VTG               | 2       |
| Pin 5 (TMS)    | 5              | &nbsp;            | &nbsp;  |
| Pin 6 (nSRST)  | 6              | RESET (debugWIRE) | 5       |
| Pin  (N.C.)    | 7&nbsp;        | &nbsp;            | &nbsp;  |
| Pin 8 (nTRST)  | 8              | &nbsp;            | &nbsp;  |
| Pin 9 (TDI)    | 9              | MOSI              | 4       |
| Pin 10 (GND)   | 0              | &nbsp;            | &nbsp;  |

For **PICkit4** and **SNAP**, such a table looks as follows, with pin 1 marked by a triangle.

| MBLAP Debugger | Pin # | Target pin        | SPI pin |
| -------------- | ----- | ----------------- | ------- |
| Pin 1 (TVPP)   | 1     | &nbsp;            | &nbsp;  |
| Pin 2 (TVDD)   | 2     | VTG               | 2       |
| Pin 3 (GND)    | 3     | GND               | 6       |
| Pin 4 (PGD)    | 4     | MISO              | 1       |
| Pin 5 (PGC)    | 5     | SCK               | 3       |
| Pin 6 (TAUX)   | 6     | RESET (debugWIRE) | 5       |
| Pin 7 (TTDI)   | 7     | MOSI              | 4       |
| Pin 8 (TTMS)   | 8     | &nbsp;            | &nbsp;  |

When you want to connect a **dw-link** debugger without a dw-link probe shield to a target, you can use jumper cables using the following pin mapping.

| dw-link Arduino Uno pins    | Target pin        | SPI pin |
| --------------------------- | ----------------- | ------- |
| D8                          | RESET (debugWIRE) | 5       |
| D11                         | MOSI              | 4       |
| D12                         | MISO              | 1       |
| D13                         | SCK               | 3       |
| 5V (if powered by debugger) | Vcc               | 2       |
| GND                         | GND               | 6       |

With a dw-link probe shield, it is best to construct or buy a cable with a 6-pin SPI programming plug on one end and single Dupont pins on the other.

## Connecting to a JTAG target

While there is a standard for the JTAG lines, there is no commonly agreed-upon pinout of the headers. However, for the AVR family, there is a standard pinout as follows.

![ISP headers](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/jtag-header-MC.png)

Sometimes, pin 8 is connected to nTREST, which we do not need, though. The crucial pins are TCK (JTAG clock), TDO and TDI (data lines), TMS (control line). In addition, we have nSRST, the reset line, and VTref and GND.

### Connecting to targets with a JTAG header

Again, if there is a JTAG header on the board, connecting the board is a breeze. Simply use the right cable.

![Atmel-ICI+MCUdude](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/Atmel-ICE+MCUdude.jpeg)

### Connecting to targets without a JTAG header

When debugging a program running on an Arduino Mega, you must connect the wires individually, referring to the Arduino Mega's pinout and the header on the debugger. Here is an example for connecting PICkit4 (or Snap) to an Arduino Mega 2560.

![Atmel-ICI+MCUdude](https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pickit4+mega.jpeg)

The pin mapping for the PICkit4 looks as follows, where I have added the Arduino pins in the last column.

| MBLAP Debugger | Pin # | Target pin | JTAG pin | Mega pin |
| -------------- | ----- | ---------- | -------- | -------- |
| Pin 1 (TVPP)   | 1     | NC&nbsp;   | &nbsp;   |          |
| Pin 2 (TVDD)   | 2     | VTG        | 4        | 5V       |
| Pin 3 (GND)    | 3     | GND        | 2, 10    | GND      |
| Pin 4 (PGD)    | 4     | TDO        | 3        | A6       |
| Pin 5 (PGC)    | 5     | TSCK       | 1        | A4       |
| Pin 6 (TAUX)   | 6     | RESET      | 6        | RESET    |
| Pin 7 (TTDI)   | 7     | TDI        | 9        | A7       |
| Pin 8 (TTMS)   | 8     | TMS&nbsp;  | 5&nbsp;  | A5       |

For the Atmel debuggers, the setup appears as follows, where the JTAG pin corresponds to the mini-squid numbering. I have additionally added the corresponding Mega pin.

| Atmel Debugger | Mini-squid pin = JTAG pin | Target pin | Mega pin |
| -------------- | ------------------------- | ---------- | -------- |
| Pin 1 (TCK)    | 1                         | TCK        | A4       |
| Pin 2 (GND)    | 2                         | GND        | GND      |
| Pin 3 (TDO)    | 3                         | TDO        | A6       |
| Pin 4 (VTG)    | 4                         | VTG        | 5V       |
| Pin 5 (TMS)    | 5                         | TMS&nbsp;  | A5       |
| Pin 6 (nSRST)  | 6                         | RESET      | RESET    |
| Pin  7 (N.C.)  | 7&nbsp;                   | NC&nbsp;   |          |
| Pin 8 (nTRST)  | 8                         | NC&nbsp;   |          |
| Pin 9 (TDI)    | 9                         | TDI        | A7       |
| Pin 10 (GND)   | 0                         | GND&nbsp;  | GND      |

## Connecting to UPDI and PDI

Will be treated later when implemented.

------

[<small><i>Back to pyavrocd README</i></small>](https://github.com/felias-fogg/pyavrocd/blob/main/README.md)

