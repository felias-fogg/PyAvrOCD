"""
This an integration test running both the gdbserver and avr-gdb
debugging different test programs testing the outputs of avr-gdb with Pexpect.
"""
#pylint: disable=line-too-long,too-many-locals
import argparse
import logging
import textwrap
import sys
from time import sleep
import pexpect

# enables debugging
# and runs live tests
on_script = ("live", "", "",
    ("set style enabled off", ""),
    ("set trace-commands on", ""),
    ("set logging file tests/log/live.log", ""),
    ("set logging overwrite on", ""),
    ("set logging on",  ""),
    ("target remote :2000", "0x00000000 in ?? ()"),
    ("monitor debugwire enable", "enabled", "This is not a debugWIRE target"),
    ("monitor reset", ""),
    ("monitor LiveTests", "live tests successfully finished"),
    ("detach",  "Detaching from"),
    ("quit", ""))

# tests monitor commands across different gdb servers
mon_script = ("monitor commands", "blink", "",
    ("set style enabled off", ""),
    ("set trace-commands on", ""),
    ("set logging file tests/log/monitor.log", ""),
    ("set logging overwrite on", ""),
    ("set logging on",  ""),
    ("target remote :2000", "0x00000000 in __vectors ()"),
    ("monitor debugwire enable", "debugWIRE is enabled", "This is not a debugWIRE target"),
    ("monitor reset", "MCU has been reset"),
    ("monitor help", "monitor info"),
    ("monitor info", "Target:"),
    ("monitor version", "version"),
    ("monitor atexit leave", "MCU will leave debugWIRE mode on exit"),
    ("monitor atexit stayindebugwire", "MCU will stay in debugWIRE mode on exit"),
    ("monitor load readbeforewrite", "Reading before writing when loading"),
    ("monitor load writeonly", "No reading before writing when loading"),
    ("monitor load",  "No reading before writing when loading"),
    ("monitor verify enable", "Verifying flash after load"),
    ("monitor verify disable", "Load operations are not verified"),
    ("monitor verify", "Load operations are not verified"),
    ("monitor onlywhenloaded enable", "Execution is only possible after a previous load command"),
    ("monitor onlywhenloaded", "Execution is only possible after a previous load command"),
    ("continue", "No program loaded"),
    ("next", "No program loaded"),
    ("monitor onlywhenloaded disable", "Execution is always possible"),
    ("next", "Single stepping until"),
    ("load", "Loading"),
    ("break loop", "Breakpoint 1"),
    ("continue", "Breakpoint 1"),
    ("monitor timers freeze", "Timers are frozen when execution is stopped"),
    ("print TCNT0==TCNT0", " = true", " = 1"),
    ("monitor timers run", "Timers will run when execution is stopped"),
    ("monitor timers", "Timers will run when execution is stopped"),
    ("print TCNT0==TCNT0", " = false", " = 0"),
    ("monitor singlestep safe",  "Single-stepping is interrupt-safe"),
    ("monitor singlestep interruptible",  "Single-stepping is interruptible"),
    ("monitor singlestep",  "Single-stepping is interruptible"),
    ("monitor ver", "Ambiguous 'monitor' command string"),
    ("monitor xxx", "Unknown 'monitor' command"),
    ("monitor load xxx", "Unknown argument in 'monitor' command"),
    ("detach",  "Detaching from"),
    ("quit", ""))

# tests breaks in ISRs
# tests asynchronous stop
# tests display
blink_script =("blink", "blink", "",
    ("set style enabled off", ""),
    ("set trace-commands on", ""),
    ("set logging file tests/log/blink.log", ""),
    ("set logging overwrite on", ""),
    ("set logging on",  ""),
    ("target remote :2000", "0x00000000 in __vectors ()"),
    ("monitor debugwire enable", "enabled", "This is not a debugWIRE target"),
    ("monitor reset", ""),
    ("load", "Start address 0x"),
    ("break irq_routine",  "Breakpoint 1"),
    ("continue",  "if (cycle < 5)"),
    ("display privmillis", "privmillis = 0"),
    ("continue", "privmillis ="),
    ("print cycle", "$1 = 0"),
    ("break loop", "Breakpoint 2"),
    ("delete 1", ""),
    ("continue", "Breakpoint 2, loop"),
    ("next", "mydelay(1000)"),
    ("break irq_routine", "Breakpoint 3 at"),
    ("continue", "if (cycle < 5)" ),
    ("continue", "if (cycle < 5)" ),
    ("print cycle", "$2 = " ),
    ("delete 3", ""),
    ("break test_cycle", "Breakpoint 4"),
    ("cond 4 cycle == 4", ""),
    ("disable 2", ""),
    ("info b",  "stop only if cycle == 4"),
    ("continue", "Breakpoint 4"),
    ("delete 1-10", "No breakpoint number 10"),
    ("continue&", ""),
    ("$SLEEP", 3),
    ("interrupt", ""),
    ("$SLEEP", 0.5),
    ("", "Program received signal SIGINT, Interrupt"), # this message comes asynchronously
    ("i b","No breakpoints"),
    ("detach",  "Detaching from"),
    ("quit", ""))

break_script = ("break", "blink", "",
    ("set style enabled off", ""),
    ("set trace-commands on", ""),
    ("set logging file tests/log/break.log", ""),
    ("set logging overwrite on", ""),
    ("set logging on",  ""),
    ("target remote :2000", "0x00000000 in __vectors ()"),
    ("monitor debugwire enable", "enabled", "This is not a debugWIRE target"),
    ("monitor reset", ""),
    ("load", "Start address 0x"),
    ("monitor breakpoints hardware", "hardware"),
    ("tbreak setup", "Temporary breakpoint 1"),
    ("break loop", "Breakpoint 2"),
    ("continue", "SIGABRT"),
    ("delete 2", ""),
    ("continue", "Temporary breakpoint 1"),
    ("info breakpoints", "No breakpoints"),
    ("break loop", "Breakpoint 3"),
    ("continue", "Breakpoint 3, loop"),
    ("next", "SIGABRT"),
    ("step", "SIGABRT"),
    ("delete 3", ""),
    ("finish", "mydelay"),
    ("monitor breakpoints all", "All breakpoints"),
    ("break loop", "Breakpoint 4"),
    ("continue", "Breakpoint 4, loop"),
    ("next", "mydelay"),
    ("detach", "Detaching from"),
    ("quit", ""))

# test whether flash memory is loaded up without any error
flash_script = ("flash", "flashed", "",
    ("set style enabled off", ""),
    ("set trace-commands on", ""),
    ("set logging file tests/log/flash.log", ""),
    ("set logging overwrite on", ""),
    ("set logging on",  ""),
    ("target remote :2000", "0x00000000 in __vectors ()"),
    ("monitor debugwire enable", "enabled", "This is not a debugWIRE target"),
    ("monitor reset", ""),
    ("load", "Start address 0x"),
    ("break flashOK", "Breakpoint 1 at"),
    ("break flashError", "Breakpoint 2 at"),
    ("continue", "Breakpoint 1, flashOK ()"),
    ("detach", "Detaching from"),
    ("quit", ""))

# test recursive functions
# test up/down
# test conditional stop
# test run command
# software watchpoint
fib_script = ("fibonacci", "fibonacci", "",
    ("set style enabled off", ""),
    ("set trace-commands on", ""),
    ("set logging file tests/log/fib.log", ""),
    ("set logging overwrite on", ""),
    ("set logging on",  ""),
    ("target extended-remote :2000", "0x00000000 in __vectors ()"),
    ("monitor debugwire enable", "enabled", "This is not a debugWIRE target"),
    ("monitor reset", ""),
    ("load", "Start address 0x"),
    ("list loop","int result, arg;"),
    ("b 62", "Breakpoint 1 at"),
    ("b 84", "Breakpoint 2 at"),
    ("cont", "Breakpoint 1, loop ()"),
    ("p result", "$1 = 13"),
    ("p callcnt", "$2 = 25"),
    ("continue", "84	  delay(result);"),
    ("p result", "$3 = 1"),
    ("p callcnt", "$4 = 1"),
    ("b fib", "Breakpoint 3"),
    ("b mfib", "Breakpoint 4"),
    ("dis 1", ""),
    ("continue", "Breakpoint 3, fib (n=7)"),
    ("continue", "Breakpoint 3, fib (n=6)"),
    ("continue", "Breakpoint 3, fib (n=5)"),
    ("continue", "Breakpoint 3, fib (n=4)"),
    ("continue", "Breakpoint 3, fib (n=3)"),
    ("backtrace", "in fib (n=7)"),
    ("backtrace", "in loop ()"),
    ("up", "in fib (n=4)"),
    ("up", "in fib (n=5)"),
    ("up", "in fib (n=6)"),
    ("down", "in fib (n=5)"),
    ("down", "in fib (n=4)"),
    ("p n", "$5 = 4"),
    ("clear fib", "Deleted breakpoint 3"),
    ("continue", "Breakpoint 4, mfib (n=7)"),
    ("set remote hardware-watchpoint-limit 0", ""),
    ("watch memo[7]", "Watchpoint 5: memo[7]"),
    ("continue", "Watchpoint 5: memo[7]"),
    ("p memo[7]", "$6 = 1"),
    ("p memo", "$7 = {0, 0, 0, 0, 0, 0, 0}"),
    ("set memo[7] = 0", ""),
    ("p callcnt", "$8 = 0"),
    ("dis 4-5", ""),
    ("continue", "Breakpoint 2"),
    ("p result", "$9 = 13"),
    ("p callcnt", "$10 = 13"),
    ("enable 1", ""),
    ("monitor reset", "reset"),
    ("continue", "Breakpoint 1"),
    ("detach", "Detaching from"),
    ("quit", ""))

# test OOP debugging - make sure, that LTO is disabled!
# test maximal BP setting (set to 4!)
oop_script = ("oop", "oop", "-fno-lto",
    ("set style enabled off", ""),
    ("set trace-commands on", ""),
    ("set logging file tests/log/oop.log", ""),
    ("set logging overwrite on", ""),
    ("set logging on",  ""),
    ("target extended-remote :2000", "0x00000000 in __vectors ()"),
    ("monitor debugwire enable",  "enabled", "This is not a debugWIRE target"),
    ("monitor reset", ""),
    ("load", "Start address 0x"),
    ("whatis r", "Rectangle"),
    ("ptype r", "type = class Rectangle : public TwoDObject"),
    ("print r", "$1 = {<TwoDObject> = {x ="),
    ("list setup", "setup(void)"),
    ("b 83", "Breakpoint 1"),
    ("b 92", "Breakpoint 2"),
    ("b 111", "Breakpoint 3"),
    ("continue", "Breakpoint 1"),
    ("print r","$2 = {<TwoDObject> = {x = 10, y = 11}, height = 5, width = 8}"),
    ("continue", "Serial.println(F(\"Move s by +10, +10:\"));"),
    ("dis 1", ""),
    ("continue", "Breakpoint 3"),
    ("print s", "$3 = {<Rectangle> = {<TwoDObject> = {x = 15, y = 15}, height = 5,"),
    ("detach","Detaching from"),
    ("quit", ""))

#tests terminal I/O and heavy IRQ load
tictactoe_script = ("tictactoe", "tictactoe", "",
    ("set style enabled off", ""),
    ("set trace-commands on", ""),
    ("set logging file tests/log/tictactoe.log", ""),
    ("set logging overwrite on", ""),
    ("set logging on",  ""),
    ("target extended-remote :2000", "0x00000000 in __vectors ()"),
    ("monitor debugwire enable",  "enabled", "This is not a debugWIRE target"),
    ("monitor reset", ""),
    ("load", "Start address 0x"),
    ("b tictactoe.ino:211","line 211"),
    ("b tictactoe.ino:176","line 176"),
    ("b minimax", "Breakpoint 3"),
    ("c", "211"),
    ("set key='Y'", ""),
    ("p key", "$1 = 89 'Y'"),
    ("n", "215"),
    ("n", "219"),
    ("n", "210"),
    ("n", "211"),
    ("n", "212"),
    ("n", "return LEFTKEY"),
    ("c", "176"),
    ("set key='9'", ""), # we play 9
    ("c", "Breakpoint 3, minimax (player=1"),
    ("c", "Breakpoint 3, minimax (player=player@entry=-1"),
    ("disable 3", ""),
    ("c", "176"), # player played 5
    ("set key='3'", ""), # we play 3
    ("c", "176"), # player played 6
    ("set key='1'", ""), # we play 1
    ("c", "211"), # player playd 4 -- and won
    ("set key='N'", ""), # we do not want play any longer
    ("c", "211"),
    ("detach","Detaching from"),
    ("quit", ""))

# tests safe and interruptible single-step execution
# INT 0 is enabled and switched active by setting the IRQ pin as an output
isr_script = ("single-step", "isr", "",
    ("set style enabled off", ""),
    ("set trace-commands on", ""),
    ("set logging file tests/log/isr.log", ""),
    ("set logging overwrite on", ""),
    ("set logging on",  ""),
    ("target extended-remote :2000", "0x00000000 in __vectors ()"),
    ("monitor debugwire enable",  "enabled", "This is not a debugWIRE target"),
    ("monitor reset", ""),
    ("load", "Start address 0x"),
    ("b isr.ino:shortwait", "Breakpoint 1"),
    ("c", "shortwait"),
    ("n", ""),
    ("n", "outsidecount++"),
    ("c", "shortwait"),
    ("n", ""),
    ("n", "outsidecount++"),
    ("c", "shortwait"),
    ("n", ""),
    ("n", "outsidecount++"),
    ("c", "shortwait"),
    ("n", ""),
    ("n", "outsidecount++"),
    ("c", "shortwait"),
    ("monitor singlestep interruptible", "interruptible"),
    ("n", ""),
    ("n", "in __vectors"),
    ("detach", "Detaching from"),
    ("quit", ""))

# load something into EEPROM
eeprom_script = ("eeprom", "eeprom", "",
    ("set style enabled off", ""),
    ("set trace-commands on", ""),
    ("set logging file tests/log/eeprom.log", ""),
    ("set logging overwrite on", ""),
    ("set logging on",  ""),
    ("target extended-remote :2000", "0x00000000 in __vectors ()"),
    ("monitor debugwire enable",  "enabled", "This is not a debugWIRE target"),
    ("monitor reset", ""),
    ("load", "Start address 0x"),
    ("break loop", ""),
    ("continue", "Breakpoint 1, loop"),
    ("p ee_data", "data that's loaded straight into EEPROM"),
    ("p ver", "data that's loaded straight into EEPROM"),
    ("delete 1", ""),
    ("break blink_exit", "Breakpoint 2"),
    ("cont", "Breakpoint 2, blink_exit (OK=true)"),
    ("set var ee_data[0] = 'X'", ""),
    ("p ee_data", "Xata that's loaded straight into EEPROM"),
    ("detach", "Detaching from"),
    ("quit", ""))

# loads fuses and lockbits, which is silently ignored
# also loads signature, which is compared with the signature
# given when inoking pyavrocd
fuse_script = ("fuses, lockbits, and signature", "fuses", "",
    ("set style enabled off", ""),
    ("set trace-commands on", ""),
    ("set logging file tests/log/fuses.log", ""),
    ("set logging overwrite on", ""),
    ("set logging on",  ""),
    ("target extended-remote :2000", "0x00000000 in __vectors ()"),
    ("monitor debugwire enable",  "enabled", "This is not a debugWIRE target"),
    ("monitor reset", ""),
    ("load", "Start address 0x"),
    ("detach", "Detaching from"),
    ("quit", ""))

# tests of the ability to simulate a two-word call/jmp instruction
# on a ATmega2560 in the high area of the memory (for all others
# it is just computing the average of 10 numbers)
simhigh_script = ("simulate 2 word call in high memory (if possible)", "sim2word_highjmp", "",
    ("set style enabled off", ""),
    ("set trace-commands on", ""),
    ("set logging file tests/log/sim2word_highjmp.log", ""),
    ("set logging overwrite on", ""),
    ("set logging on",  ""),
    ("target remote :2000", "0x00000000 in __vectors ()"),
    ("monitor debugwire enable",  "enabled", "This is not a debugWIRE target"),
    ("monitor reset", ""),
    ("load", "Start address 0x"),
    ("monitor break soft", ""),
    ("break loop", ""),
    ("continue", "Breakpoint 1, loop ()"),
    ("break +4", "Breakpoint 2"),
    ("break +8", "Breakpoint 3"),
    ("continue", "val = random();"),
    ("continue", "val = random();"),
    ("continue", "val = random();"),
    ("delete 2", ""),
    ("continue", "Serial.println(avg);"),
    ("print avg", "= -7196"),
    ("detach", "Detaching from"),
    ("quit", ""))



# switch off debugWIRE mode (if applicable)
# this test script should be run last for each MCU/clock combination
off_script = ("off", "", "",
    ("set style enabled off", ""),
    ("set trace-commands on", ""),
    ("set logging file tests/log/off.log", ""),
    ("set logging overwrite on", ""),
    ("set logging on",  ""),
    ("target extended-remote :2000", "0x00000000 in ?? ()"),
    ("monitor debugwire disable",  "disabled", "This is not a debugWIRE target"),
    ("detach","Detaching from"),
    ("quit", ""))

# check that MCU is categorized as a MCU with a dirty PC
dirty_script = ("dirty", "", "",
    ("set style enabled off", ""),
    ("set trace-commands on", ""),
    ("set logging file tests/log/dirty.log", ""),
    ("set logging overwrite on", ""),
    ("set logging on",  ""),
    ("target extended-remote :2000", "0x00000000 in ?? ()"),
    ("monitor debugwire enable",  "Fatal error:", "This is not a debugWIRE target"),
    ("monitor info", "MCU cannot be debugged because of stuck-at-1 bit"),
    ("detach","Detaching from"),
    ("quit", ""))


# Clock combinations and naming
MicroClock = {'1.2' : '1M2', '9.6' : '9M6', '16' : '16M'}
MiniClock = {'1' : '1MHz_internal', '8' : '8MHz_internal', '16' : '16MHz_external'}
ATTRcClock = {'1' : '1internal', '8' : '8internal'}
ATTClock = {'1' : '1internal', '8' : '8internal', '16' : '16external'}
NoClock = {'none' : ''}

# the on_script needs always to run first because it enables debugWIRE
# the off_script should run last in order to set the MCU back to normal mode
small_arduino = (on_script, blink_script, mon_script, break_script, flash_script, fib_script,
                     isr_script, off_script)
medium_arduino = (on_script, blink_script, mon_script ,break_script, flash_script, fib_script,
                      oop_script, isr_script, eeprom_script, fuse_script, off_script)
large_arduino =  (on_script, blink_script, mon_script, break_script, flash_script, fib_script,
                      oop_script, tictactoe_script, isr_script, eeprom_script,
                      fuse_script, simhigh_script, off_script)
exotic_arduino =  (on_script, fuse_script, off_script)
dirty_arduino  =  (dirty_script,)

test_devices = {"attiny13" : (MicroClock, small_arduino,
                                   "MicroCore:avr:13:clock=", "Dev Board"),
                "attiny2313" : (ATTClock, small_arduino,
                                   "ATTinyCore:avr:attinyx313:chip=2313,clock=", "Programmer-ZF"),
                "attiny4313" : (ATTClock, medium_arduino,
                                   "ATTinyCore:avr:attinyx313:chip=4313,clock=", "Programmer-ZF"),
                "attiny43u" : (ATTRcClock,  medium_arduino,
                                   "ATTinyCore:avr:attiny43:clock=", "Breakout Board"),
                "attiny24" : (ATTClock, small_arduino,
                                   "ATTinyCore:avr:attinyx4:chip=24,clock=", "Dev Board"),
                "attiny44" : (ATTClock, medium_arduino,
                                   "ATTinyCore:avr:attinyx4:chip=44,clock=", "Dev Board"),
                "attiny84" : (ATTClock, large_arduino,
                                   "ATTinyCore:avr:attinyx4:chip=84,clock=", "Dev Board"),
                "attiny841" : (ATTRcClock, large_arduino,
                                   "ATTinyCore:avr:attinyx41:chip=841,clock=", "Breakout Board"),
                "attiny441" : (ATTRcClock, medium_arduino,
                                   "ATTinyCore:avr:attinyx41:chip=441,clock=", "Breadboard setup"),
                "attiny25" : (ATTClock, small_arduino,
                                   "ATTinyCore:avr:attinyx5:chip=25,clock=", "Dev Board"),
                "attiny45" : (ATTClock, medium_arduino,
                                   "ATTinyCore:avr:attinyx5:chip=45,clock=", "Dev Board"),
                "attiny85" : (ATTClock, large_arduino,
                                   "ATTinyCore:avr:attinyx5:chip=85,clock=", "Dev Board"),
                "attiny261" : (ATTClock, small_arduino,
                                    "ATTinyCore:avr:attinyx61:chip=261,clock=", "Dev Board"),
                "attiny461" : (ATTClock, medium_arduino,
                                    "ATTinyCore:avr:attinyx61:chip=461,clock=", "Dev Board"),
                "attiny861" : (ATTClock, large_arduino,
                                    "ATTinyCore:avr:attinyx61:chip=861,clock=", "Dev Board"),
                "attiny87" : (ATTClock, large_arduino,
                                   "ATTinyCore:avr:attinyx7:chip=87,clock=", "Breakout Board"),
                "attiny167" : (ATTClock, large_arduino,
                                    "ATTinyCore:avr:attinyx7:chip=167,clock=", "Breakout Board"),
                "attiny48" : (ATTRcClock, medium_arduino,
                                   "ATTinyCore:avr:attinyx8:chip=48,clock=", "Programmer-ZF"),
                "attiny88" : (ATTRcClock, large_arduino,
                                   "ATTinyCore:avr:attinyx8:chip=88,clock=", "Programmer-ZF"),
                "attiny828" : (ATTRcClock, large_arduino,
                                    "ATTinyCore:avr:attiny828:clock=", "Breakout Board"),
                "attiny1634" : (ATTRcClock, large_arduino,
                                     "ATTinyCore:avr:attiny1634:clock=", "Breakout Board"),
                "atmega48a" : (MiniClock, medium_arduino,
                                    "MiniCore:avr:48:variant=modelNonP,bootloader=no_bootloader," +
                                    "clock=", "Programmer-ZF"),
                "atmega48pa" : (MiniClock, medium_arduino,
                                    "MiniCore:avr:48:variant=modelP,bootloader=no_bootloader," +
                                    "clock=", "Programmer-ZF"),
                "atmega88a" : (MiniClock, large_arduino,
                                    "MiniCore:avr:88:variant=modelNonP,bootloader=no_bootloader," +
                                    "clock=", "Programmer-ZF"),
                "atmega88pa" : (MiniClock, large_arduino,
                                    "MiniCore:avr:88:variant=modelP,bootloader=no_bootloader,clock=",
                                    "Programmer-ZF"),
                "atmega168a" : (MiniClock, large_arduino,
                                    "MiniCore:avr:168:variant=modelNonP,bootloader=no_bootloader,clock=",
                                    "Programmer-ZF"),
                "atmega168pa" : (MiniClock, large_arduino,
                                    "MiniCore:avr:168:variant=modelP,bootloader=no_bootloader,clock=",
                                    "Programmer-ZF / XPLAINED Mini Board"),
                "atmega328" : (MiniClock, large_arduino,
                                    "MiniCore:avr:328:variant=modelNonP,bootloader=no_bootloader,clock=",
                                    "Programmer-ZF"),
                "atmega328p" : (MiniClock, large_arduino,
                                    "MiniCore:avr:328:variant=modelP,bootloader=no_bootloader,clock=",
                                    "Programmer-ZF / XPLAINED Mini Board"),
                "atmega328pb" : (MiniClock, large_arduino,
                                    "MiniCore:avr:328:variant=modelPB,bootloader=no_bootloader,clock=",
                                    "XPLAINED Mini Board"),

                # JTAG targets: MightyCore
                "atmega324pb" : (MiniClock, large_arduino,
                                     "MightyCore:avr:324:variant=modelPB,bootloader=no_bootloader,clock=",
                                     "XPLAINED Pro Board"),
                "atmega16" : (MiniClock, dirty_arduino,
                                     "MightyCore:avr:16:bootloader=no_bootloader,clock=",
                                     "MightyCore development board"),
                "atmega32" : (MiniClock, large_arduino,
                                     "MightyCore:avr:32:bootloader=no_bootloader,clock=",
                                     "MightyCore development board"),
                "atmega164pa" : (MiniClock, large_arduino,
                                     "MightyCore:avr:164:variant=modelP,bootloader=no_bootloader,clock=",
                                     "MightyCore development board"),
                "atmega644" : (MiniClock, large_arduino,
                                     "MightyCore:avr:644:variant=modelA,bootloader=no_bootloader,clock=",
                                     "MightyCore development board"),
                "atmega1284p" : (MiniClock, large_arduino,
                                     "MightyCore:avr:1284:variant=modelP,bootloader=no_bootloader,clock=",
                                     "MightyCore development board"),

                # JTAG targets: MegaCore
                "atmega2560": (MiniClock, large_arduino,
                                   "MegaCore:avr:2560:bootloader=no_bootloader,clock=",
                                   "Arduino Mega"),
                "atmega1280": (MiniClock, large_arduino,
                                   "MegaCore:avr:1280:bootloader=no_bootloader,clock=",
                                   "Arduino Mega 1280"),
                "atmega169P": (MiniClock, large_arduino,
                                   "MegaCore:avr:169:variant=modelP,bootloader=no_bootloader,clock=",
                                   "Butterfly"),

                "atmega128": (MiniClock, large_arduino,
                                   "MegaCore:avr:128:bootloader=no_bootloader,clock=",
                                   "Olimex AVR-MT-128"),

                # JTAG targets: MajorCore
                "atmega162": (MiniClock, large_arduino,
                                   "MajorCore:avr:162:bootloader=no_bootloader,clock=",
                                   "Butterfly"),

                # JTAG targets: Arduino AVR Core
                "atmega32u4": (NoClock, large_arduino,
                                   "arduino:avr:leonardo",
                                   "Leonardo"),

                    }

#pylint: disable=too-many-statements
def main():
    """
    Main routine. Sets up everything and runs the tests.
    """
    parser = argparse.ArgumentParser(usage="%(prog)s [options]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\n\
    Integration test for GDBserver
            '''))
    parser.add_argument('-c', '--clock',
                            type=str,
                            dest='clock',
                            help='MCU clock frequency in MHz',
                            choices=['1', '8', '16', '1.2', '9.6', 'none' ],
                            required=True)
    parser.add_argument('-d', '--device',
                            type=str,
                            dest='dev',
                            help='Device to debug',
                            required=True)
    parser.add_argument("-v", "--verbose",
                        default="info", choices=['debug', 'info',
                                                     'warning', 'error', 'critical'],
                        help="Logging verbosity level")

    args = parser.parse_args()

    # set up logging
    args.verbose = args.verbose.strip()
    if args.verbose.upper() in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
        form = "[%(levelname)s] %(message)s"
    else:
        form = "[%(levelname)s] %(name)s: %(message)s"
    logging.basicConfig(stream=sys.stderr,level=args.verbose.upper(), format = form)
    logger = logging.getLogger()

    if args.dev.lower() not in test_devices:
        logger.critical("%s is not supported for live tests", args.dev)
        return 1
    mcu_name = args.dev.lower()
    mcu_clocks, script_list, fqbn, test_board = test_devices[mcu_name]
    if args.clock in mcu_clocks:
        clock = mcu_clocks[args.clock]
    else:
        logger.critical("Clock frequency %s MHz is not supported for integration tests on %s",
                            args.clock, mcu_name)
        return 1

    logger.info("Starting integration testing on %s.", mcu_name)
    logger.warning("Prepare debugging with %s.", test_board)
    logger.warning("Make sure that 'serv.sh' is running")
    logger.warning("Press <RETURN> when everything has been set up.")
    input()

    failed_comp = 0
    failed_scripts = 0
    tests_done = 0
    for script in script_list:
        logger.info("Try: %s", script[0])
        exit_status = 0
        cmd_out = ""
        if script[1]:
            logger.info("Compile %s.ino for '%s' clock on %s", script[1], clock, mcu_name)
            cmd = "arduino-cli compile -b " + fqbn + clock + \
                  ' -e --build-property="build.extra_flags=-Og -ggdb3 ' + script[2] + '" --output-dir ' + \
                  "tests/sketches/" + script[1] + " tests/sketches/" + script[1]
            logger.debug("Compile command: '%s'", cmd)
            cmd_out, exit_status =  pexpect.run(cmd, withexitstatus=1)
        tests_done += 1
        if exit_status != 0:
            logger.error("Failed compilation: %s", cmd_out)
            failed_comp += 1
            continue
        if not run_script(logger, script):
            logger.error("Failed to run script '%s'", script[0])
            failed_scripts += 1
        else:
            logger.info("Succeeded: %s", script[0])
    if failed_comp + failed_scripts == 0:
        logger.info("All of the %s tests succeeded", tests_done)
    else:
        logger.info("Test runs:           %s", tests_done)
        logger.info("Compilations failed: %s", failed_comp)
        logger.info("Scripts failed:      %s", failed_scripts)
    return 0

#pylint: disable=too-many-return-statements,too-many-branches,too-many-statements
def run_script(logger, script):
    """
    Execute one script and compare with expected replies.
    """
    test_name = script[0]
    print("Running", test_name, end='')
    test_binary = "tests/sketches/" + script[1] + "/" + script[1] + ".ino.elf"
    if script[1] == "":
        test_binary = ""
    child = pexpect.spawn("avr-gdb " + test_binary + " -n")
    sleep(2)
    ix = 3
    resp = child.expect([r"\(gdb\)",pexpect.TIMEOUT,pexpect.EOF],timeout=1)
    logger.debug("Initial response: %s", child.before.decode())
    if resp >= 1:
        logger.error("Failed %s calling avr-gdb", test_name)
        child.close()
        print()
        return False
    while ix < len(script):
        print(".",end='')
        sys.stdout.flush()
        interact = script[ix]
        if interact[0] == "$SLEEP":
            logger.debug("COMMAND: Sleep(%s)",interact[1])
            sleep(interact[1])
            ix += 1
            continue
        logger.debug("COMMAND: %s", interact[0])
        child.sendline(interact[0])
        resp = child.expect([ r"\(gdb\)", pexpect.TIMEOUT, pexpect.EOF,
                                r'Please power-cycle the target system' ],
                                timeout=(300 if interact[0] == 'load' else 120))
        if resp == 1:
            if interact[1] == pexpect.TIMEOUT:
                logger.debug("RESPONSE: TIMEOUT")
                continue
            logger.error("Failed %s in line %s with TIMEOUT", test_name, ix-1)
            logger.error("Expected: '%s' in response to: '%s'", interact[1], interact[0])
            logger.debug("FAILED: %s", script[0])
            child.close()
            print()
            return False
        if resp == 2:
            if ix == len(script) - 1:
                logger.debug("SUCCEEDED: " + script[0])
                print("OK")
                return True
            logger.debug("FAILED: %s in line %s with EOF from child",  test_name, ix-1)
            child.close()
            print()
            return False
        if resp == 3:
            logger.warning("*** Power-cycle target system! ***")
            resp = child.expect([ r"\(gdb\)", pexpect.TIMEOUT, pexpect.EOF], timeout=30)
            if resp != 0:
                logger.debug("Failed during power-cycling")
                child.close()
                print()
                return False
        logger.debug("RESPONSE: '%s'", child.before.decode())
        if child.before.decode().find(interact[1]) >= 0 or \
            len(interact) > 2 and child.before.decode().find(interact[2]) or \
            len(interact) > 3 and child.before.decode().find(interact[3]):
            ix += 1
        else:
            logger.error("Failed %s in line %s with unexpected response:", test_name, ix-1)
            logger.error("      '%s'",  child.before.decode())
            logger.error("Expected: '%s' in response to: '%s'", interact[1], interact[0])
            logger.debug("FAILED: %s", script[0])
            print()
            child.close()
            return False
    logger.debug("SUCCEEDED: %s", script[0])
    child.close()
    print("OK")
    return True

if __name__ == '__main__':
    sys.exit(main())
