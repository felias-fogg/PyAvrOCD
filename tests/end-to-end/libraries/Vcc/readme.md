Vcc
===

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Commits since latest](https://img.shields.io/github/commits-since/felias-fogg/Vcc/latest)](https://github.com/felias-fogg/Vcc/commits/master)
[![Build Status](https://github.com/felias-fogg/Vcc/workflows/LibraryBuild/badge.svg)](https://github.com/felias-fogg/Vcc/actions)
![Hit Counter](https://visitor-badge.laobi.icu/badge?page_id=felias-fogg_Vcc)



This is a very small and basic library that contains only two main (static) methods, which return the voltage of an AVR MCU supply in millivolts. The method switches the ADC on (and off again), if necessary, and it works for most of the chips of the AVR family that are supported by the Arduino IDE.

The method, called `measure`, comes in two flavors. It can be called with two parameters, a *repetition counter* and a *calibration value*. The repetition counter specifies how often the measurement should be done in order to enhance accuracy. The calibration value specifies the accurate value of the internal voltage reference in millivolts. Nominally it is 1100 millivolts for most MCU types. However, this can change from chip to chip. If you want a truely accurate measurement, then you should determine this value for each chip, using, for example, the [*intrefTune* sketch](https://github.com/felias-fogg/intrefTune) or even better the fully automatic calibration utility that comes with the [*avrCalibrate* library](https://github.com/felias-fogg/avrCalibrate). 

The other flavor of the method uses a calibration value that is stored in EEPROM (at `E2END-3` and `E2END-2`) or has been globally set using the `setIntref` method. It is called with only one (optional) argument, the repetition counter. So the usage of the method could look like as follows:

    #include<Vcc.h>
    ...
    int milliVolts;
    ...
    milliVolts = Vcc::measure(); // uses calibration value from EEPROM, 10 repetitions
    ...
    Vcc::setIntref(1200); // set global intref variable to 1200
    ...
    milliVolts = Vcc::measure(20); // uses calibration value from global intref var, 20 repetitions
    ...
    milliVolts = Vcc::measure(100, 1100); // 100 repetitions, 1100 as calibration value

The library should work with almost all MCUs supported by ATTinyCore, MiniCore, MightCore, MegaCore, and MajorCore. It will not work with ATtinyX13 because of the lack of an ADC. Similarly, it does not work with ATtiny13 because this chip does not support measuring Vcc. 

The library is licensed under the MIT license.
