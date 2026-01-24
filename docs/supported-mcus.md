# Supported MCUs

This is the list of all AVR MCUs, which should be compatible with PyAvrOCD. Currently, only the classic parts are covered, but MCUs with PDI and UPDI debugging interfaces will follow soon. Some of the MCUs are supported by more than one core. However, not all potential cores have been extended yet to allow for debugging with the Arduino IDE 2 (but will be soon).

MCUs tested with PyAvrOCD are marked in bold. MCUs known not to work with PyAvrOCD are struck out. Underlined MCUs are sitting on my desk and are waiting to be tested.

## Classic ATtinys

### ATtiny supported by [*MicroCore*](https://github.com/MCUdude/MicroCore) (soon)

- **ATtiny13(A)**

### ATtinys supported by [*ATTinyCore (Debug enabled)*](https://github.com/felias-fogg/ATTinyCore-debug-enabled)

* **ATtiny43U**
* **ATtiny2313, ATtiny2313A, ATtiny4313**
* **ATtiny24(A), ATtiny44(A), ATtiny84(A)**
* **ATtiny441**, **ATtiny841**
* **ATtiny25, ATtiny45, ATtiny85**
* **ATtiny261(A), ATtiny461(A), ATtiny861(A)**
* **ATtiny87**, **ATtiny167**
* **ATtiny828**
* **ATtiny48, ATtiny88**
* **ATtiny1634**

### Other ATtinys without a debug interface

- <s>ATtiny4, ATtiny5, ATtiny9, ATtiny10</s>

- <s>ATtiny11, ATtiny12, ATtiny15</s>
- <s>ATtiny20</s>
- <s>ATtiny26</s>
- <s>ATtiny40</s>



## Classic ATmegas

### ATmegas supported by [*MiniCore*](https://github.com/MCUdude/MiniCore) (soon)

- <s>ATmega8</s>

* **<s>ATmega48</s>,** **ATmega48A,** ATmega48P, **ATmega48PA,** ATmega48PB,
* **<s>ATmega88</s>,** **ATmega88A,** ATmega88P, **ATmega88PA,** Atmega88PB,
* **ATmega168,** **ATmega168A**, **ATmega168P**, ATmega168PA, **ATmega168PB**,
* **ATmega328,** **ATmega328P**, **ATmega328PB**

The ATmega8 does not possess a debug interface.

The ATmega48 and ATmega88 (without the A-suffix) sitting on my desk suffer from the problem that they either cannot be switched to dbugWIRE mode, or, if you are successful, they become unresponsive. I suspect that this applies to all chips labeled this way. Even chips recently purchased through an official distributor had these issues. For this reason, PyAvrOCD will identify these chips and refuse to handle them.

### ATmegas supported by [*Atmel AVR Xplained-minis (Debug enabled)*](https://github.com/felias-fogg/avr-xminis-debug-enabled)

- **ATmega328P**
- **ATmega168PB**
- **ATmega328PB**

### ATmegas supported by [*MightyCore*](https://github.com/MCUdude/MightyCore) (soon)

* **ATmega16(A)**, **ATmega32(A)**
* **ATmega164(P)(A)**, **ATmega324(P)(A)**, **ATmega324PB**, **ATmega644(P)(A)**, **ATmega1284(P)**
* <s>**ATmega8535**</s>

The ATmega16 MCUs (with and without an A-suffix) have a stuck-at-one-bit in the program counter, which may lead to problems when you use an unpatched version of AVR-GDB. In this case, backtraces are garbled, and line-stepping might not work as expected. Use the AVR-GDB version shipped with PyAvrOCD instead, which can also be downloaded from the [Releases page of the avr-gdb repo](https://github.com/felias-fogg/avr-gdb/releases/latest).

The ATmega8535 does not possess a debug interface.

### ATmegas supported by [*MegaCore*](https://github.com/MCUdude/MegaCore) (soon)

* **ATmega64(A)**, **ATmega128(A)**
* ATmega640, **ATmega1280**, **ATmega2560**
* **ATmega1281**, **ATmega2561**
* **ATmega165(P)(A)**, **ATmega325(P)(A)**, **ATmega645(P)(A)**
* **ATmega169(P)(A)**, **ATmega329(P)(A)**, **ATmega649(P)(A)**
* **ATmega3250(P)(A)**, **ATmega6450(P)(A)**
* **ATmega3290(P)(A)**, **ATmega6490A**
* **AT90CAN32**, AT90CAN64, **AT90CAN128**

The Atmega64(A), ATmega329(P)(A), and ATmega3250(P)(A) MCUs have stuck-at-one-bit in their PCs, which might lead to the same problem as for the ATmega16s mentioned above when an older, unpatched AVR-GDB version is used.

The ATmega128(A) MCUs do not allow for software breakpoints. This means that you can use only four hardware breakpoints.

### ATmega supported by [*MajorCore*](https://github.com/MCUdude/MajorCore) (soon)

* **ATmega162**
* <s>ATmega8515</s>

The ATmega8515 does not have a debug interface.

### Other ATmegas with JTAG interface

* AT90USB646, AT90USB647, <u>AT90USB1286</u>, AT90USB1287
* ATmega644rfr2, ATmega1284rfr2, ATmega2564rfr2
* ATmega64rfr2, ATmega128rfr2, <u>ATmega256rfr2</u>
* ATmega128rfa1
* ATmega16U4, **ATmega32U4**
* ATmega406

### Other ATmegas with debugWIRE interface

* <u>ATmega8U2</u>, ATmega16U2, <u>ATmega32U2</u>
* ATmega32C1, ATmega64C1, ATmega16M1, <u>ATmega32M1</u>, <u>ATmega64M1</u>
* AT90USB82, **AT90USB162**
* AT90PWM1, <u>AT90PWM2B</u>, AT90PWM3B
* <u>AT90PWM81</u>, AT90PWM161
* <u>AT90PWM216</u>, AT90PWM316
* <u>ATmega8HVA</u>, ATmega16HVA, <u>ATmega16HVB</u>, ATmega32HVB, ATmega32HVBrevB, ATmega64HVE2

### Other ATmegas without a debug interface

- <s>ATmega163</s>

