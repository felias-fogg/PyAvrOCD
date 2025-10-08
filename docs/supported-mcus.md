# Supported MCUs



This is the list of all AVR MCUs, which should be compatible with PyAvrOCD. MCUs tested with PyAvrOCD are marked in bold. MCUs known not to work with PyAvrOCD are struck out. Underlined MCUs are sitting on my desk and are waiting to be tested.

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

The ATmega48 and ATmega88 (without the A-suffix) sitting on my desk suffer from stuck-at-one bits in the program counter and are, therefore, not debuggable by GDB. They also act strangely when trying to switch to debugWIRE mode or back (you can easily brick them this way). I suspect that this applies to all chips labeled this way. Even chips recently purchased through an official distributor had these issues. For this reason, PyAvrOCD will identify these chips and refuse to handle them.

### Other ATmegas

* <u>ATmega8U2</u>, ATmega16U2, <u>ATmega32U2</u>
* ATmega32C1, ATmega64C1, ATmega16M1, <u>ATmega32M1</u>, <u>ATmega64M1</u>
* AT90USB82, <u>AT90USB162</u>
* AT90PWM1, <u>AT90PWM2B</u>, AT90PWM3B
* <u>AT90PWM81</u>, AT90PWM161
* <u>AT90PWM216</u>, AT90PWM316
* <u>ATmega8HVA</u>, ATmega16HVA, <u>ATmega16HVB</u>, ATmega32HVB, ATmega32HVBrevB, ATmega64HVE2

## ATmegas with JTAG interface

The MCUs in the lists below are all supported by PyAvrOCD. However, the cores have not been extended yet to allow for debugging with the Arduino IDE 2. Again, the MCUs marked in bold face have been actually tested to work, and the struck-out MCUs are known not to work. Underlined MCUs are already sitting on the desk and are waiting to be tested.

### ATmegas supported by [*MightyCore*](https://github.com/MCUdude/MightyCore)

* <s>**ATmega16**</s>, <s>**ATmega16A**</s>, **ATmega32**, ATmega32A
* ATmega164A, ATmega164P, **ATmega164PA**, ATmega324, ATmega324A, ATmega324PA, **ATmega324PB**, **ATmega644**, ATmega644A, ATmega644PA, <u>ATmega1284</u>, **ATmega1284P**

The ATmega16 MCUs (with and without an A-suffix) have a stuck-at-1-bit in the program counter, which does not show when reading the program counter in the debugger. But when retrieving return addresses from the stack, it is apparent. Since this confuses GDB, this MCU cannot be debugged. The datasheet seems to suggest that the variant with an A-suffix does not suffer from this feat. However, interestingly, the same phenomenon appeared on chips labeled with an A-suffix. In any case, all chips with this signature will be tested for stuck-at-1-bits.

### ATmegas supported by [*MegaCore*](https://github.com/MCUdude/MegaCore)

* ATmega64, ATmega64A, <s>**ATmega128**</s>, <s>**ATmega128A**</s>
* ATmega640, **ATmega1280**, **ATmega2560**
* ATmega1281, <u>ATmega2561</u>
* ATmega165, <u>ATmega165A</u>, ATmega165P, ATmega165PA, ATmega325, <u>ATmega325A</u>, ATmega325P, ATmega325PA, ATmega645, ATmega645A, <u>ATmega645P</u>, ATmega645PA
* ATmega169, ATmega169A, <u>ATmega169P</u>, ATmega169PA, ATmega329, ATmega329A, ATmega329P, ATmega329PA, ATmega649, <u>ATmega649A</u>, ATmega649P, ATmega649PA
* ATmega3250, ATmega3250A, <u>ATmega3250P</u>, ATmega3250PA, ATmega6450, <u>ATmega6450A</u>, ATmega6450P, ATmega6450PA
* ATmega3290, ATmega3290A, ATmega3290P, ATmega3290PA, ATmega6490, <u>ATmega6490A</u>, ATmega6490P, ATmega6490PA
* AT90CAN32, AT90CAN64, <u>AT90CAN128</u>

The ATmega128(A) MCUs do not allow software breakpoints and throw an exception if one tries to set a software breakpoint. For this reason, debugging is currently impossible. This will change in the near future.

### ATmega supported by [*MajorCore*](https://github.com/MCUdude/MajorCore)

* <u>ATmega162</u>

### Other ATmegas

* AT90USB646, AT90USB647, AT90USB1286, AT90USB1287
* ATmega644rfr2, ATmega1284rfr2, ATmega2564rfr2
* ATmega64rfr2, ATmega128rfr2, ATmega256rfr2
* ATmega128rfa1
* ATmega16U4, **ATmega32U4**
* ATmega406

