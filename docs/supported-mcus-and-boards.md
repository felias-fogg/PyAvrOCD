# Supported MCUs and Boards



This is the list of all AVR MCUs, which should be compatible with PyAvrOCD. MCUs tested with PyAvrOCD are marked bold. MCUs known not to work with PyAvrOCD are struck out.

## MCUs with debugWIRE interface

### ATtiny supported by [*MicroCore*](https://github.com/MCUdude/MicroCore)

- **ATtiny13**

### ATtinys supported by the [*ATTinyCore*](https://github.com/SpenceKonde/ATTinyCore)

* **ATtiny43U**
* **ATtiny2313, ATtiny2313A, ATtiny4313**
* **ATtiny24(A), ATtiny44(A), ATtiny84(A)**
* **ATtiny441, ATtiny841**
* **ATtiny25, ATtiny45**, **ATtiny85**
* **ATtiny261(A), ATtiny461(A), ATtiny861(A)**
* **ATtiny87, ATtiny167**
* **ATtiny828**
* **ATtiny48, ATtiny88**
* **ATtiny1634**

### ATmegas supported by [*MiniCore*](https://github.com/MCUdude/MiniCore)

* <s>__ATmega48__</s>, __ATmega48A__, __ATmega48PA__, ATmega48PB,
* <s>__ATmega88__</s>, __ATmega88A__, __ATmega88PA__, Atmega88PB,
* __ATmega168__, __ATmega168A__, __ATmega168PA__, **ATmega168PB**,
* **ATmega328**, __ATmega328P__, **ATmega328PB**

The ATmega48 and ATmega88 (without the A-suffix) sitting on my desk suffer from stuck-at-one bits in the program counter and are, therefore, not debuggable by GDB. They also act strangely when trying to switch to debugWIRE mode or back (you can easily brick them this way).

I suspect that this applies to all chips labeled this way. Even chips recently purchased through an official distributor had these issues. For this reason, PyAvrOCD will refuse to handle them.

### Other ATmegas

* ATmega8U2, ATmega16U2, ATmega32U2
* ATmega32C1, ATmega64C1, ATmega16M1, ATmega32M1, ATmega64M1
* AT90USB82, AT90USB162
* AT90PWM1, AT90PWM2B, AT90PWM3B
* AT90PWM81, AT90PWM161
* AT90PWM216, AT90PWM316
* ATmega8HVA, ATmega16HVA, ATmega16HVB, ATmega32HVB, ATmega32HVBrevB, ATmega64HVE2

### Supported Arduino boards

All Arduino boards equipped with one of the chips mentioned above can be debugged. This includes the **Arduino Uno R3**, **Arduino Nano**, and **Arduino Pro Mini** (as well as clones). Note that in all these cases, one must ensure that the RESET line is not connected to a capacitor and that the pull-up resistor on the RESET line is not stronger than 10 kΩ. This means that in most cases, the [board must be physically changed](board-preparation.md) before debugging is possible.



## ATmegas with JTAG interface

The MCUs in the lists below are all supported by PyAvrOCD. However, the cores have not been extended yet to allow for debugging with the Arduino IDE 2.

### ATmegas supported by [*MightyCore*](https://github.com/MCUdude/MightyCore)

* <s>**ATmega16**</s>, ATmega16A, **ATmega32**, ATmega32A
* ATmega164A, ATmega164P, **ATmega164PA**, ATmega324, ATmega324A, ATmega324PA, **ATmega324PB**, **ATmega644**, ATmega644A, ATmega644PA, ATmega1284, **ATmega1284P**

The ATmega16 MCUs (without an A-suffix) have a stuck-at-1-bit in the program counter, which does not show when reading the program counter in the debugger. But when retrieving return addresses from the stack, it is apparent. Since this confuses GDB, this MCU cannot be debugged.

### ATmegas supported by [*MegaCore*](https://github.com/MCUdude/MegaCore)

* ATmega64, ATmega64A, <s>**ATmega128**</s>, <s>**ATmega128A**</s>
* ATmega640, **ATmega1280**, **ATmega2560**
* ATmega1281, ATmega2561
* ATmega165, ATmega165A, ATmega165P, ATmega165PA, ATmega325, ATmega325A, ATmega325P, ATmega325PA, ATmega645, ATmega645A, ATmega645P, ATmega645PA
* ATmega169, ATmega169A, <u>**ATmega169P**</u>, ATmega169PA, ATmega329, ATmega329A, ATmega329P, ATmega329PA, ATmega649, ATmega649A, ATmega649P, ATmega649PA
* ATmega3250, ATmega3250A, ATmega3250P, ATmega3250PA, ATmega6450, ATmega6450A, ATmega6450P, ATmega6450PA
* ATmega3290, ATmega3290A, ATmega3290P, ATmega3290PA, ATmega6490, ATmega6490A, ATmega6490P, ATmega6490PA
* AT90CAN32, AT90CAN64, AT90CAN128

The ATmega128 MCUs do not allow software breakpoints. For this reason, debugging is currently impossible because only 1 hardware breakpoint is permitted. This will change in the near future.

### ATmega supported by [*MajorCore*](https://github.com/MCUdude/MajorCore)

* <u>**ATmega162**</u>

### Other ATmegas

* AT90USB646, AT90USB647, AT90USB1286, AT90USB1287
* ATmega644rfr2, ATmega1284rfr2, ATmega2564rfr2
* ATmega64rfr2, ATmega128rfr2, ATmega256rfr2
* ATmega128rfa1
* ATmega16U4, **<u>ATmega32U4</u>**
* ATmega406

### Supported Arduino boards

All boards with the chips listed above can be debugged. This is, in particular, the **Arduino Mega (2560)**, **Arduino Leonardo**, and **Arduino Micro**. Note that you should not connect any load to the JTAG lines. Furthermore, you must first enable the JTAG pins by SPI programming because on the Arduino boards, JTAG is disabled by default.

