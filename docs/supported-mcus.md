# Supported MCUs

This is the list of the AVR MCUs that should be compatible with PyAvrOCD. MCUs tested with PyAvrOCD are marked in bold. MCUs known not to work with PyAvrOCD are struck out. Underlined MCUs are sitting on my desk and are waiting to be tested. All other MCUs listed are supposed to be compatible because their close cousins are. However, this assumption can be wrong, as I have experienced repeatedly.

The list is structured by the Arduino packages that support the chips, where some of the MCUs are supported by more than one package.

## Classic ATtinys

### ATtinys supported by [MicroCore](supporting-packages.md#microcore)

- **ATtiny13(A)**

Because of its limited flash memory, debugging a sketch on this MCU is rather challenging.

### ATtinys supported by [TinyCore](supporting-packages.md#tinycore) and [ATTinyCore (Debug enabled)](supporting-packages.md#attinycore)

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
- <s>ATtiny20 </s>, <s>ATtiny40</s>
- <s>ATtiny22</s>
- <s>ATtiny26</s>
- <s>ATtiny28</s>
- <s>ATtiny102, ATtiny104</s>

## Modern ATtinys

### ATtiny 0-series supported by [megaTinyCore (Debug enabled)](supporting-packages.md#megatinycore)

- **ATtiny202**, **ATtiny402**
- **ATtiny204**, **ATtiny404,** **ATtiny804**, **ATtiny1604**
- **ATtiny406**, **ATtiny806**, **ATtiny1606**
- ATtiny807, **ATtiny1607**



### ATtiny 1-series supported by [megaTinyCore (Debug enabled)](supporting-packages.md#megatinycore)

- **ATtiny212**, **ATtiny412**
- **ATtiny214**, **ATtiny414**, **ATtiny814,** **ATtiny1614**
- **ATtiny416**, **ATtiny816**, **ATtiny1616**, **ATtiny3216**
- <u>ATtiny417</u>, **ATtiny817**, <u>ATtiny1617</u>, **ATtiny3217**



### ATtiny 2-series supported by [megaTinyCore (Debug enabled)](supporting-packages.md#megatinycore)

- **ATtiny424**, **ATtiny824**, **ATtiny1624**, **ATtiny3224**
- **ATtiny426**, **ATtiny826**, **ATtiny1626**, **ATtiny3226**
- <u>ATtiny427</u>, <u>ATtiny827</u>, <u>ATtiny1627</u>, **ATtiny3237**



## Classic ATmegas

### ATmegas supported by [MiniCore](supporting-packages.md#minicore)

- <s>ATmega8</s>

* **<s>ATmega48</s>,** **ATmega48A,** **ATmega48P**, **ATmega48PA,** **ATmega48PB**,
* **<s>ATmega88</s>,** **ATmega88A,** **ATmega88P**, **ATmega88PA,** **Atmega88PB**,
* **ATmega168,** **ATmega168A**, **ATmega168P**, **ATmega168PA**, **ATmega168PB**,
* **ATmega328,** **ATmega328P**, **ATmega328PB**

The ATmega8 does not possess a debug interface. The ATmega48 and ATmega88 (without the A-suffix) sitting on my desk suffer from the problem that they either cannot be switched to debugWIRE mode, or, if you are successful, they become unresponsive. I suspect that this applies to all chips labeled this way. Even chips recently purchased through an official distributor had these issues. For this reason, PyAvrOCD will identify these chips and refuse to handle them.

### ATmegas supported by [XMiniCore](supporting-packages.md#xminicore)

The following MCUs are already supported by MiniCore. However, XMiniCore goes some way to make it easier to deal with the Microchip Xplained Mini development boards so that debugging becomes plug-and-play.

- **ATmega328P** (Xplained Mini board)
- **ATmega168PB** (Xplained Mini board)
- **ATmega328PB** (Xplained Mini board)

### ATmegas supported by [MightyCore](supporting-packages.md#mightycore)

* **ATmega16(A)**, **ATmega32(A)**
* **ATmega164(P)(A)**, **ATmega324(P)(A)**, **ATmega324PB**, **ATmega644(P)(A)**, **ATmega1284(P)**
* <s>ATmega8535</s>

The ATmega16 MCUs (with and without an A-suffix) have a stuck-at-one-bit in the program counter, which may lead to problems when you use an unpatched version of AVR-GDB. In this case, backtraces are garbled, and line-stepping might not work as expected. Use the AVR-GDB version shipped with PyAvrOCD instead, which can also be downloaded from the [Releases page of my avr-gdb repo](https://github.com/felias-fogg/avr-gdb/releases/latest).

The ATmega8535 does not possess a debug interface.

### ATmegas supported by [MegaCore](supporting-packages.md#megacore)

* **ATmega64(A)**, **ATmega128(A)**
* **ATmega640**, **ATmega1280**, **ATmega2560**
* **ATmega1281**, **ATmega2561**
* **ATmega165(P)(A)**, **ATmega325(P)(A)**, **ATmega645(P)(A)**
* **ATmega169(P)(A)**, **ATmega329(P)(A)**, **ATmega649(P)(A)**
* **ATmega3250(P)(A)**, **ATmega6450(P)(A)**
* **ATmega3290(P)(A)**, **ATmega6490A**
* **AT90CAN32**, **AT90CAN64**, **AT90CAN128**

The Atmega64(A), ATmega329(P)(A), and ATmega3250(P)(A) MCUs have a stuck-at-one-bit in the PC, which might lead to the same problem as for the ATmega16s mentioned above when an older, unpatched AVR-GDB version is used.

The ATmega128(A) MCUs do not allow for software breakpoints. This means that you can use only four hardware breakpoints.

### ATmega supported by [MajorCore](supporting-packages.md#majorcore)

* **ATmega162**
* <s>ATmega8515</s>

The ATmega8515 does not have a debug interface.

### ATmegas supported by [Arduino AVR Boards (Debug enabled)](supporting-packages.md#arduino-avr-boards)

Most of the MCUs covered by this package are already supported by other packages. However, one exception is the ATmega32U4 (e.g., on the Leonardo).

- **ATmega168**
- **Atmega328P**
- **ATmega32U4**
- **ATmega1280**
- **ATmega2560**

### Other ATmegas with debugWIRE interface

* <u>ATmega8U2</u>, ATmega16U2, <u>ATmega32U2</u>
* ATmega32C1, ATmega64C1, ATmega16M1, <u>ATmega32M1</u>, <u>ATmega64M1</u>
* AT90USB82, **AT90USB162**
* AT90PWM1, <u>AT90PWM2B</u>, AT90PWM3B
* <u>AT90PWM81</u>, AT90PWM161
* <u>AT90PWM216</u>, AT90PWM316
* <u>ATmega8HVA</u>, ATmega16HVA, <u>ATmega16HVB</u>, ATmega32HVB, ATmega32HVBrevB, ATmega64HVE2

### Other ATmegas with JTAG interface

* ATmega16U4
* AT90USB646, AT90USB647, <u>AT90USB1286</u>, AT90USB1287
* ATmega644rfr2, ATmega1284rfr2, ATmega2564rfr2
* ATmega64rfr2, ATmega128rfr2, <u>ATmega256rfr2</u>
* ATmega128rfa1
* ATmega406

## Modern ATmegas

### ATmegas supported by [MegaCoreX (Debug enabled)](supporting-packages.md#megacorex)

This is the megaAVR 0-series. The ATmega4809 made it on some Arduino boards.

- **ATmega808**, **ATmega1608**, **ATmega3208**, **ATmega4808**
- **ATmega809**, **ATmega1609**, **ATmega3209**, **ATmega4809**

### ATmega supported by [Arduino megaAVR Boards (Debug enabled)](supporting-packages.md#arduino-megaavr-boards)

There exists only 2 Arduino boards, both using the

- **ATmega4809**

## AVR Dx-, Ex-, Lx-, Sx- devices

### AVR DA series supported by [DxCore (Debug enabled)](supporting-packages.md#dxcore)

- **AVR32DA28(S)**, AVR32DA32(S), AVR32DA48(S)
- **AVR64DA28(S)**, AVR64DA32(S), AVR64DA48(S), AVR32DA64(S)
- **AVR128DA28(S)**, AVR128DA32(S), **AVR128DA48(S)**, AVR128DA64(S)

### AVR DB series supported by  [DxCore (Debug enabled)](supporting-packages.md#dxcore)

- **AVR32DB28**, AVR32DB32, AVR32DB48
- **AVR64DB28**, AVR64DB32, AVR64DB48, AVR32DB64
- **AVR128DB28**, <u>AVR128DB32</u>, **AVR128DB48**, <u>AVR128DB64</u>

### AVR DD series supported by  [DxCore (Debug enabled)](supporting-packages.md#dxcore)

- AVR16DD14, AVR16DD20, **AVR16DD28**, AVR16DD32
- AVR32DD14, AVR32DD20, **AVR32DD28**, AVR32DD32
- <u>AVR64DD14</u>, <u>AVR64DD20</u>, **AVR64DD28**, **AVR64DD32**

### AVR DU series supported by  [DxCore (Debug enabled)](supporting-packages.md#dxcore)

- AVR16DU14, AVR16DU20, **AVR16DU28**, AVR16DU32
- AVR32DU14, AVR32DU20, **AVR32DU28**, AVR32DU32
- **AVR64DU28**, **AVR64DU32**

### AVR EA series supported by  [DxCore (Debug enabled)](supporting-packages.md#dxcore)

- **AVR16EA28**, AVR16EA32, AVR16EA48

- **AVR32EA28**, AVR32EA32, AVR32EA48
- **AVR64EA28**, AVR64EA32, **AVR64EA48**

### AVR EB series supported by  [DxCore (Debug enabled)](supporting-packages.md#dxcore)

- AVR16EB14, AVR16EB20, **AVR16EB28**, **AVR16EB32**
- AVR32EB14, AVR32EB20, AVR32EB28, AVR32EB32

### AVR LA series

No support yet

### AVR SD series

No support yet. Since DxCore will most probably not support these chips, it is questionable whether PyAvrOCD will.

## XMegas

There is no support yet for XMegas. Since they are not supported by any active Arduino packages and do not have any support in PlatformIO, the chances are not very high that I will dive into that.
