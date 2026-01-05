#pylint: disable=missing-module-docstring
# Clock combinations and naming
micro_clock = {'1.2' : '1M2', '9.6' : '9M6', '16' : '16M'}
mini_clock = {'1' : '1MHz_internal', '8' : '8MHz_internal', '16' : '16MHz_external'}
new_attiny_rc_clock = {'1' : 'internal_1m', '8' : 'internal_8m'}
attiny_rc_clock = {'1' : '1internal', '8' : '8internal'}
new_attiny_clock = {'1' : 'internal_1m', '8' : 'internal_8m', '16' : 'external_16m'}
attiny_clock = {'1' : '1internal', '8' : '8internal', '16': '16external'}
c_clock = {'1' : '1000000UL', '8' : '8000000UL', '16' : '16000000UL'}
no_clock = {'none' : ''}

# Tag list: for each tag in the list for one device, this tag has to be present in the script tag list
# Example: For attiny13 only scripts are selected that have  'small', 'arduino', 'dw'. and 'noadc' in their description
test_devices = {"attiny13" : (micro_clock, ('small', 'arduino', 'dw', 'noadc', 'noautopc'),
                                   "MicroCore:avr:13:clock=", "Dev Board"),
                "attiny2313" : (attiny_clock, ('small',  'dw', 'noadc', 'noautopc'),
                                   "ATTinyCore:avr:attinyx313:chip=2313,clock=", "Programmer-ZF"),
                "attiny2313a" : (attiny_clock, ('small',  'dw', 'noadc', 'noautopc'),
                                   "ATTinyCore:avr:attinyx313:chip=2313,clock=", "Programmer-ZF"),
                "attiny4313" : (attiny_clock, ('medium',  'dw', 'noadc', 'noautopc'),
                                   "ATTinyCore:avr:attinyx313:chip=4313,clock=", "Programmer-ZF"),
                "attiny43u" : (attiny_rc_clock,  ('medium', 'dw', 'noautopc', 'noadc'),
                                   "ATTinyCore:avr:attiny43:clock=", "Breakout Board"), # changed name with v2.0.0!
                "attiny24" : (attiny_clock, ('small',  'dw', 'noautopc'),
                                   "ATTinyCore:avr:attinyx4:chip=24,clock=", "Dev Board"),
                "attiny44" : (attiny_clock, ('medium',  'dw', 'noautopc'),
                                   "ATTinyCore:avr:attinyx4:chip=44,clock=", "Dev Board"),
                "attiny84" : (attiny_clock, ('large',   'dw', 'noautopc'),
                                   "ATTinyCore:avr:attinyx4:chip=84,clock=", "Dev Board"),
                "attiny841" : (attiny_rc_clock, ('large',   'dw', 'noautopc'),
                                   "ATTinyCore:avr:attinyx41:chip=841,clock=", "Breakout Board"),
                "attiny441" : (attiny_rc_clock, ('medium',  'dw', 'noautopc'),
                                   "ATTinyCore:avr:attinyx41:chip=441,clock=", "Breadboard setup"),
                "attiny25" : (attiny_clock, ('small',   'dw', 'noautopc'),
                                   "ATTinyCore:avr:attinyx5:chip=25,clock=", "Dev Board"),
                "attiny45" : (attiny_clock, ('medium',  'dw', 'noautopc'),
                                   "ATTinyCore:avr:attinyx5:chip=45,clock=", "Dev Board"),
                "attiny85" : (attiny_clock, ('large', 'dw', 'noautopc'),
                                   "ATTinyCore:avr:attinyx5:chip=85,clock=", "Dev Board"),
                "attiny261" : (attiny_clock, ('small',  'dw', 'noautopc'),
                                    "ATTinyCore:avr:attinyx61:chip=261,clock=", "Dev Board"),
                "attiny461" : (attiny_clock, ('medium',   'dw', 'noautopc'),
                                    "ATTinyCore:avr:attinyx61:chip=461,clock=", "Dev Board"),
                "attiny861" : (attiny_clock, ('large',   'dw', 'noautopc'),
                                    "ATTinyCore:avr:attinyx61:chip=861,clock=", "Dev Board"),
                "attiny87" : (attiny_clock, ('large',  'dw', 'noautopc'),
                                   "ATTinyCore:avr:attinyx7:chip=87,clock=", "Breakout Board"),
                "attiny167" : (attiny_clock, ('large',  'dw', 'noautopc'),
                                    "ATTinyCore:avr:attinyx7:chip=167,clock=", "Breakout Board"),
                "attiny48" : (attiny_rc_clock, ('medium',  'dw', 'noautopc'),
                                   "ATTinyCore:avr:attinyx8:chip=48,clock=", "Programmer-ZF"),
                "attiny88" : (attiny_rc_clock, ('large',  'dw', 'noautopc'),
                                   "ATTinyCore:avr:attinyx8:chip=88,clock=", "Programmer-ZF"),
                "attiny828" : (attiny_rc_clock, ('large',   'dw', 'noautopc'),
                                    "ATTinyCore:avr:attiny828:clock=", "Breakout Board"),
                "attiny1634" : (attiny_rc_clock, ('large',  'dw', 'noautopc'),
                                     "ATTinyCore:avr:attiny1634:clock=", "Breakout Board"),
                "atmega48" : (mini_clock, ('dirty', 'dw'),
                                    "MiniCore:avr:48:variant=modelNonP,bootloader=no_bootloader," +
                                    "clock=", "Programmer-ZF"),
                "atmega48a" : (mini_clock, ('medium',  'dw', 'noautopc'),
                                    "MiniCore:avr:48:variant=modelNonP,bootloader=no_bootloader," +
                                    "clock=", "Programmer-ZF"),
                "atmega48p" : (mini_clock, ('medium',  'dw', 'noautopc'),
                                    "MiniCore:avr:48:variant=modelP,bootloader=no_bootloader," +
                                    "clock=", "Programmer-ZF"),
                "atmega48pa" : (mini_clock, ('medium',  'dw', 'noautopc'),
                                    "MiniCore:avr:48:variant=modelP,bootloader=no_bootloader," +
                                    "clock=", "Programmer-ZF"),
                "atmega88" : (mini_clock, ('dw', 'dirty'),
                                    "MiniCore:avr:88:variant=modelNonP,bootloader=no_bootloader," +
                                    "clock=", "Programmer-ZF"),
                "atmega88a" : (mini_clock, ('large', 'arduino', 'dw', 'noautopc'),
                                    "MiniCore:avr:88:variant=modelNonP,bootloader=no_bootloader," +
                                    "clock=", "Programmer-ZF"),
                "atmega88p" : (mini_clock, ('large',  'dw', 'noautopc'),
                                    "MiniCore:avr:88:variant=modelP,bootloader=no_bootloader,clock=",
                                    "Programmer-ZF"),
                "atmega88pa" : (mini_clock, ('large',  'dw', 'noautopc'),
                                    "MiniCore:avr:88:variant=modelP,bootloader=no_bootloader,clock=",
                                    "Programmer-ZF"),
                "atmega168" : (mini_clock, ('large',  'dw', 'noautopc'),
                                    "MiniCore:avr:168:variant=modelNonP,bootloader=no_bootloader,clock=",
                                    "Programmer-ZF"),
                "atmega168a" : (mini_clock, ('large',  'dw', 'noautopc'),
                                    "MiniCore:avr:168:variant=modelNonP,bootloader=no_bootloader,clock=",
                                    "Programmer-ZF"),
                "atmega168p" : (mini_clock, ('large',  'dw', 'noautopc'),
                                    "MiniCore:avr:168:variant=modelP,bootloader=no_bootloader,clock=",
                                    "Programmer-ZF / XPLAINED Mini Board"),
                "atmega168pa" : (mini_clock, ('large',  'dw', 'noautopc'),
                                    "MiniCore:avr:168:variant=modelP,bootloader=no_bootloader,clock=",
                                    "Programmer-ZF / XPLAINED Mini Board"),
                "atmega328" : (mini_clock, ('large',  'dw', 'noautopc'),
                                    "MiniCore:avr:328:variant=modelNonP,bootloader=no_bootloader,clock=",
                                    "Programmer-ZF"),
                "atmega328p" : (mini_clock, ('large',  'dw'),
                                    "MiniCore:avr:328:variant=modelP,bootloader=no_bootloader,clock=",
                                    "Programmer-ZIF"),
                "atmega328pb" : (mini_clock, ('large',  'dw'),
                                    "MiniCore:avr:328:variant=modelPB,bootloader=no_bootloader,clock=",
                                     "Programmer-ZIF"),
                "atmega168pb" : (mini_clock, ('large',  'dw'),
                                    "MiniCore:avr:168:variant=modelPB,bootloader=no_bootloader,clock=",
                                    "Programmer-ZIF"),

                # debugWIRE targets with no Core support
                "at90usb162" : (c_clock, ('large', 'nonarduino', 'dw', 'noadc', 'noautopc'), "",
                                    "AVR-USB-162 Olimex board"),

                # JTAG targets: MightyCore
                "atmega16" : (mini_clock, ('dirty', 'jtag'),
                                     "MightyCore:avr:16:bootloader=no_bootloader,clock=",
                                     "MightyCore development board"),
                "atmega16a" : (mini_clock, ('dirty', 'jtag'),
                                     "MightyCore:avr:16:bootloader=no_bootloader,clock=",
                                     "MightyCore development board"),
                "atmega32" : (mini_clock, ('large', 'jtag'),
                                     "MightyCore:avr:32:bootloader=no_bootloader,clock=",
                                     "MightyCore development board"),
                "atmega164pa" : (mini_clock, ('large', 'jtag'),
                                     "MightyCore:avr:164:variant=modelP,bootloader=no_bootloader,clock=",
                                     "MightyCore development board"),
                "atmega324p" : (mini_clock, ('large', 'jtag'),
                                     "MightyCore:avr:324:variant=modelP,bootloader=no_bootloader,clock=",
                                     "MightyCore development board"),
                "atmega644" : (mini_clock, ('large',  'jtag'),
                                     "MightyCore:avr:644:variant=modelA,bootloader=no_bootloader,clock=",
                                     "MightyCore development board"),
                "atmega1284p" : (mini_clock, ('huge',  'jtag'),
                                     "MightyCore:avr:1284:variant=modelP,bootloader=no_bootloader,clock=",
                                     "MightyCore development board"),
                "atmega324pb" : (mini_clock, ('large', 'jtag'),
                                     "MightyCore:avr:324:variant=modelPB,bootloader=no_bootloader,clock=",
                                     "XPLAINED Pro Board"),

                # JTAG targets: MegaCore
                "atmega2560": (mini_clock, ('huge',  'jtag'),
                                   "MegaCore:avr:2560:bootloader=no_bootloader,clock=",
                                   "Arduino Mega"),
                "atmega1280": (mini_clock, ('huge',   'jtag'),
                                   "MegaCore:avr:1280:bootloader=no_bootloader,clock=",
                                   "Arduino Mega 1280"),
                "atmega169P": (mini_clock, ('large',   'jtag'),
                                   "MegaCore:avr:169:variant=modelP,bootloader=no_bootloader,clock=",
                                   "Butterfly"),

                "atmega128": (mini_clock, ('huge',   'jtag'),
                                   "MegaCore:avr:128:bootloader=no_bootloader,clock=",
                                   "Olimex AVR-MT-128"),

                # JTAG targets: MajorCore
                "atmega162": (mini_clock, ('large',  'jtag'),
                                   "MajorCore:avr:162:bootloader=no_bootloader,clock=",
                                   "Butterfly"),

                # JTAG targets: Arduino AVR Core
                "atmega32u4": (no_clock, ('large', 'jtag'),
                                   "arduino:avr:leonardo",
                                   "Leonardo"),

                    }
