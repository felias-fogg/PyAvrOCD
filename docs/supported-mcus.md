# Supported MCUs



This is the list of all AVR MCUs, which should be compatible with PyAvrOCD. However, the cores have not been extended yet to allow for debugging with the Arduino IDE 2. MCUs tested with PyAvrOCD are marked in bold. MCUs known not to work with PyAvrOCD are struck out. Underlined MCUs are sitting on my desk and are waiting to be tested.

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
* AT90USB82, **AT90USB162**
* AT90PWM1, <u>AT90PWM2B</u>, AT90PWM3B
* <u>AT90PWM81</u>, AT90PWM161
* <u>AT90PWM216</u>, AT90PWM316
* <u>ATmega8HVA</u>, ATmega16HVA, <u>ATmega16HVB</u>, ATmega32HVB, ATmega32HVBrevB, ATmega64HVE2

## ATmegas with JTAG interface

The MCUs in the lists below are all supported by PyAvrOCD. However, the cores have not been extended yet to allow for debugging with the Arduino IDE 2. Again, the MCUs marked in bold face have been actually tested to work, and the struck-out MCUs are known not to work. Underlined MCUs are already sitting on the desk and are waiting to be tested.

### ATmegas supported by [*MightyCore*](https://github.com/MCUdude/MightyCore)

* <s>**ATmega16(A)**</s>, **ATmega32(A)**
* **ATmega164(P)(A)**, <u>ATmega324(P)(A)</u>, **ATmega324PB**, **ATmega644(P)(A)**, **ATmega1284(P)**

The ATmega16 MCUs (with and without an A-suffix) have a stuck-at-one-bit in the program counter, which does not show when reading the program counter in the debugger. But when retrieving return addresses from the stack, it is apparent. Since this confuses GDB, this MCU cannot be debugged. The datasheet seems to suggest that the variant with an A-suffix does not suffer from this feat. However, interestingly, the same phenomenon appeared on chips labeled with an A-suffix. In any case, all chips with this signature will be tested for stuck-at-one-bits and rejected if they have a stuck-at-one-bit.

### ATmegas supported by [*MegaCore*](https://github.com/MCUdude/MegaCore)

* <u>ATmega64(A)</u>, **ATmega128(A)**
* ATmega640, **ATmega1280**, **ATmega2560**
* <u>ATmega1281</u>, <u>ATmega2561</u>
* <u>ATmega165(P)(A)</u>, <u>ATmega325(P)(A)</u>, <u>ATmega645(P)(A)</u>
* <u>ATmega169(P)(A)</u>, <u>ATmega329(P)(A)</u>, <u>ATmega649(P)(A)</u>
* <u>ATmega3250(P)(A)</u>, <u>ATmega6450(P)(A)</u>
* <u>ATmega3290(P)(A)</u>, <u>ATmega6490A</u>
* <u>AT90CAN32</u>, AT90CAN64, <u>AT90CAN128</u>

The ATmega128(A) MCUs do not allow for software breakpoints. This
means that you can use only four hardware breakpoints.

### ATmega supported by [*MajorCore*](https://github.com/MCUdude/MajorCore)

* <u>ATmega162</u>

### ATmega supporter by *[ArduinoCore-avr-debug-enabled](https://github.com/felias-fogg/ArduinoCore-avr-debug-enabled)*

- **ATmega32U4**

### Other ATmegas

* AT90USB646, AT90USB647, <u>AT90USB1286</u>, AT90USB1287
* ATmega644rfr2, ATmega1284rfr2, ATmega2564rfr2
* ATmega64rfr2, ATmega128rfr2, <u>ATmega256rfr2</u>
* ATmega128rfa1
* ATmega16U4
* ATmega406

