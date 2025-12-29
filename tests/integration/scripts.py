#pylint: disable=missing-module-docstring
# Tags for scripts. Only if the MCU descriptoion contains a matching tag, then the script
# will be selected
all_tags = ('first', 'last', 'small', 'medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi',
                'dirty', 'arduino', 'nonarduino', 'noadc', 'noautopc')

# This is the prelude for (almost) every script
prolog = (
    ("set style enabled off", ""),
    ("set trace-commands on", ""),
    ("set logging overwrite on", ""),
    ("set logging on",  ""),
    ("target remote :2000", "0x00000000 in"),
    ("monitor debugwire enable", "enabled", "This is not a debugWIRE target"),
    ("!rm pyavrocd.options", ""),
    ("monitor reset", ""))

# The epilog of (almost) every script
epilog = (
    ("detach",  "Detaching from"),
    ("quit", ""))

# List of scripts:
#   Key is the name of the script
#   First item is a tag list (of requirements the script fulfills)
#   Second item is the name of a sketch/program folder
#   Third item is a string containing additional compiler flags
#   Fourth item is a string containing options to PyAvrOCD
#   Fifth item is a sequence of interactive tuples, first item an input, the other items potential responses

all_scripts = {
# enables debugging and runs live tests
    "live" : (
    ('first', 'small', 'medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'arduino',
         'nonarduino', 'noadc', 'noautopc'),
    "",
    "",
    "",
    (("set logging file log/live.log", ""),) + prolog + \
    (("monitor LiveTests", "live tests successfully finished"),) + epilog),

# C blink program built using make
    "cblink" : (
    ('small', 'medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'nonarduino', 'noadc', 'noautopc'),
    "cblink",
    "",
    "",
    (("set logging file log/cblink.log", ""),) + prolog + \
    (("load", "Start address 0x"),
     ("break main", "Breakpoint 1"),
     ("cont", "Breakpoint 1, main"),
     ("next", "setBit(LED2_DDR, LED2);"),
     ("next", "setBit(LED1_PORT, LED1);"),
     ("break", "Breakpoint 2"),
     ("ignore 2 5", ""),
     ("delete 1", ""),
     ("continue", "Breakpoint 2"),
     ("n", "setBit(LED2_PORT, LED2);"),
     ("n", "_delay_ms(DELAYTIME);"),
     ("monitor range", ""),
     ("$SUCCESS_IF", "Range stepping is not yet implemented"),
     ("next", "clearBit(LED1_PORT, LED1);")) + epilog),

# Tests all ways how signals are raised
# SIGHUP will be tested in the "off" script, SIGABRT cannot be tested
     "signals" : (
      ('small', 'medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'nonarduino', 'noadc', 'noautopc'),
      "break",
      "",
      "",
      (("set logging file log/signals.log", ""),) + prolog + \
      (("cont", "SIGSEGV"),
       ("load", "Start address 0x"),
       ("monitor break hardware",""),
       ("break main", "Breakpoint 1"),
       ("cont", "break.c:19"),
       ("break 20", "line 20"),
       ("break 21", "line 21"),
       ("break 22", "line 22"),
       ("break 24", "line 24"),
       ("cont", "SIGSYS"),
       ("delete 1-5", ""),
       ("cont", "SIGTRAP"),
       ("cont", "SIGILL"),
       ("next", "SIGILL"),
       ("step", "SIGILL"),
       ("monitor reset", ""),
       ("break 27", ""),
       ("cont", ""),
       ("set $sp=0x5e", ""),
       ("cont", "SIGBUS")) + epilog),

# Checks range stepping for debugWIRE targets
# _delay_ms (will be fast), loop with 2 exits (will be slow), loop with 0 exits (will be fast again)
    "range_dw" : (
    ('small', 'medium', 'large', 'huge', 'dw', 'arduino', 'noadc', 'noautopc'),
    "range_dw",
    "",
    "",
    (("set logging file log/range_dw.log", ""),) + prolog + \
    (("load",  "Start address 0x"),
     ("break range_dw.ino:23", "Breakpoint 1"),
     ("cont", "LedOn"),
     ("next", "_delay_ms"),
     ("next", "LedOff"),
     ("break range_dw.ino:30", "Breakpoint 2"),
     ("cont", "Breakpoint 2"),
     ("next", "while"),
     ("next &", ""),
     ("$SLEEP", 3),
     ("interrupt", ""),
     ("$SLEEP", 0.5),
     ("", "SIGINT"),
     ("print cnt > 1", "= true", "= 1"),
     ("print cnt < 30", "= true", "= 1"),
     ("break 33", "Breakpoint 3"),
     ("cont", "cnt = 0"),
     ("next", "while"),
     ("next &", ""),
     ("$SLEEP", 3),
     ("interrupt", ""),
     ("$SLEEP", 0.5),
     ("interrupt", ""),
     ("$SLEEP", 0.5),
     ("interrupt", ""),
     ("$SLEEP", 0.5),
     ("print cnt > 100000", "= true", "= 1")) + epilog),

# Checks range stepping for JTAG targets
# _delay_ms (will be fast), loop with 4 exits (will be relatively fast),
# loop with 5 exits (will be slow), deadloop (will be fast again)
# Note that the current version of GCC is not able to stop in front of the while statements.
# Maybe the next version?
    "range_jtag" : (
    ('small', 'medium', 'large', 'huge', 'jtag', 'arduino', 'noadc', 'noautopc'),
    "range_jtag",
    "",
    "",
    (("set logging file log/range_jtag.log", ""),) + prolog + \
    (("load",  "Start address 0x"),
     ("break range_jtag.ino:32", "Breakpoint 1"),
     ("cont", "LedOn"),
     ("next", "_delay_ms"),
     ("next", "LedOff"),
     ("delete 1", ""),
     ("break loop", "Breakpoint 2"),
     ("cont", "LedOn"),
     ("next", "LedOff"),
     ("next &", ""),
     ("$SLEEP", 3),
     ("interrupt", ""),
     ("$SLEEP", 1),
     ("", "SIGINT"),
     ("print cnt2", ""),
     ("print cnt2 > 0", "= true", "= 1"),
     ("print cnt2 < 10", "= true", "= 1"),
     ("break 42", ""),
     ("cont", "LedOn"),
     ("next &", ""),
     ("$SLEEP", 3),
     ("interrupt", ""),
     ("$SLEEP", 1),
     ("", "SIGINT"),
     ("print cnt3", ""),
     ("print cnt3 > 100000", "= true", "= 1")) + epilog),

# Test sleep walking
    "sleepwalk" : (
    ('small', 'medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'arduino', 'noadc', 'noautopc'),
    "sleepwalk",
    "",
    "",
    (("set logging file log/sleepwalk.log", ""),) + prolog + \
    (("load", "Start address 0x"),
     ("break sleepwalk.ino:13", "Breakpoint 1"),
     ("cont", "sei"),
     ("next", "sleep_cpu"),
     ("next &", ""),
     ("$SLEEP", 2),
     ("interrupt", "SIGINT"))
     + epilog),

# C++ program to measure supply voltage
    "measure" : (
    ('small', 'medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'nonarduino', 'noautopc'),
    "measure",
    "",
    "",
    (("set logging file log/measure.log", ""),) + prolog + \
    (("load", "Start address 0x"),
     ("break Vcc.cpp:Vcc::setIntref", "Breakpoint 1"),
     ("cont", ""),
     ("p intref", "$1 = 1"),
     ("fin", "result ="),
     ("next", "if (result"),
     ("p result", "$2 = "),
     ("b success", "Breakpoint 2"),
     ("b fail", "Breakpoint 3"),
     ("cont", "success () at")) + epilog),

# tests monitor commands across different gdb servers
    "monitor" : (
    ('small', 'medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'arduino', 'noadc', 'noautopc'),
    "blink",
    "",
    "",
    (("set logging file log/monitor.log", ""),) + prolog + \
    (("monitor help", "monitor info"),
     ("monitor info", "Target:"),
     ("monitor version", "version"),
     ("monitor atexit leave", "MCU will leave debugWIRE mode on exit", "Leave debugWIRE at exit"),
     ("monitor atexit stayindebugwire", "MCU will stay in debugWIRE mode on exit", "Stay in debugWIRE at exit"),
     ("monitor breakpoints software", "Only software breakpoints",
          "Breakpoint mode cannot be changed on this MCU"),
     ("monitor breakpoints hardware", "Only hardware breakpoints",
          "Breakpoint mode cannot be changed on this MCU"),
     ("monitor breakpoints all", "All breakpoints are allowed",
          "Breakpoint mode cannot be changed on this MCU"),
     ("monitor caching disable", "Flash memory will not be cached",
         "Caching is not implemented"),
     ("monitor caching enable", "Flash memory will be cached",
         "Caching is not implemented"),
     ("monitor caching", "Flash memory will be cached",
         "Caching is not implemented"),
     ("monitor erasebeforeload disable",
         "Flash memory will not be erased before loading executable",
         "On debugWIRE targets, flash memory cannot be erased before loading executable",
         "'Erase-before-load' is not supported on debugWIRE targets"),
     ("monitor erasebeforeload enable",
         "Flash memory will be erased before loading executable",
         "On debugWIRE targets, flash memory cannot be erased before loading executable",
         "'Erase-before-load' is not supported on debugWIRE targets"),
     ("monitor erasebeforeload",
         "Flash memory will be erased before loading executable",
         "On debugWIRE targets, flash memory cannot be erased before loading executable",
         "'Erase-before-load' is not supported on debugWIRE targets"),
     ("monitor load onlycache", "Only reading, but no flashing", "Only caching when loading"),
     ("monitor load readbeforewrite", "Reading before writing when loading"),
     ("monitor load writeonly", "No reading before writing when loading"),
     ("monitor load",  "No reading before writing when loading"),
     ("monitor rangestepping disable", "Range stepping is disabled", "No range stepping"),
     ("monitor rangestepping enable", "Range stepping is enabled", "Range stepping allowed"),
     ("monitor verify enable", "Verifying flash after load"),
     ("monitor verify disable", "Load operations are not verified"),
     ("monitor verify", "Load operations are not verified"),
     ("monitor onlywhenloaded enable", "Execution is only possible after a previous load command"),
     ("monitor onlywhenloaded", "Execution is only possible after a previous load command"),
     ("continue", "No program loaded"),
     ("stepi", "No program loaded"),
     ("monitor onlywhenloaded disable", "Execution is always possible"),
     ("monitor reset", ""),
     ("stepi", "()"),
     ("load", "Loading"),
     ("break main", "Breakpoint 1"),
     ("continue", "Breakpoint 1"),
     ("monitor timers freeze", "Timers are frozen when execution is stopped"),
     ("monitor timers run", "Timers will run when execution is stopped"),
     ("monitor timers", "Timers will run when execution is stopped"),
     ("monitor singlestep safe",  "Single-stepping is interrupt-safe"),
     ("monitor singlestep interruptible",  "Single-stepping is interruptible"),
     ("monitor singlestep",  "Single-stepping is interruptible"),
     ("monitor ver", "Ambiguous 'monitor' command string"),
     ("monitor xxx", "Unknown 'monitor' command"),
     ("monitor load xxx", "Unknown argument in 'monitor' command")) + epilog),

# test timer settings
    "timers" : (
    ('small', 'medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'arduino', 'noadc', 'noautopc'),
    "blink",
    "",
    "",
    (("set logging file log/blink.log", ""),) + prolog + \
    (("load", "Loading"),
     ("break loop", "Breakpoint 1"),
     ("continue", "Breakpoint 1"),
     ("monitor timers freeze", "Timers are frozen when execution is stopped"),
     ("print TCNT0==TCNT0", " = true", " = 1"),
     ("monitor timers run", "Timers will run when execution is stopped"),
     ("print TCNT0==TCNT0", " = false", " = 0")) + epilog),

# tests extended-remote target
    "extended" : (
    ('small', 'medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'nonarduino', 'noadc', 'noautopc'),
    "cblink",
    "",
    "",
    (("set style enabled off", ""),
     ("set logging file log/extended.log", ""),
     ("set trace-commands on", ""),
     ("set logging overwrite on", ""),
     ("set logging on",  ""),
     ("target extended-remote :2000", "0x00000000 in"),
     ("monitor debugwire enable", "enabled", "This is not a debugWIRE target"),
     ("monitor reset", ""),
     ("load", "Start address 0x"),
     ("break main", "Breakpoint 1"),
     ("run\ny", "Starting program:"),
     ("kill\nn", "Not confirmed"))  + epilog),

# tests breaks in ISRs
# tests asynchronous stop
# tests display
    "blink" : (
    ('small', 'medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'arduino', 'noadc', 'noautopc'),
    "blink",
    "",
    "",
    (("set logging file log/blink.log", ""),) + prolog + \
    (("load", "Start address 0x"),
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
     ("$SLEEP", 1),
     ("", "Program received signal SIGINT, Interrupt"), # this message comes asynchronously
     ("i b","No breakpoints")) + epilog),

# Testing 'hardware-only' breakpoints for debugWIRE targets (1 HWBP only)
    "breakdw" : (
    ('small', 'medium', 'large', 'huge', 'dw', 'arduino', 'noadc', 'noautopc'),
    "blink",
    "",
    "",
    (("set logging file log/break.log", ""),) + prolog + \
    (("load", "Start address 0x"),
     ("monitor breakpoints hardware", "hardware"),
     ("tbreak blink.ino:setup", "Temporary breakpoint 1"),
     ("break loop", "Breakpoint 2"),
     ("continue", "SIGSYS"),
     ("delete 2", ""),
     ("continue", "Temporary breakpoint 1"),
     ("info breakpoints", "No breakpoints"),
     ("break loop", "Breakpoint 3"),
     ("continue", "Breakpoint 3, loop"),
     ("next", "SIGSYS"),
     ("step", "SIGSYS"),
     ("delete 3", ""),
     ("finish", "LedOn"),
     ("monitor breakpoints all", "All breakpoints"),
     ("break loop", "Breakpoint 4"),
     ("continue", "Breakpoint 4, loop"),
     ("next", "mydelay")) + epilog),

# Testing 'hardware-only' breakpoints for JTAG targets (4 HWBPs)
    "breakjtag" : (
    ('small', 'medium', 'large', 'huge', 'jtag', 'arduino', 'noadc', 'noautopc'),
    "blink",
    "",
    "",
    (("set logging file log/break.log", ""),) + prolog + \
    (("load", "Start address 0x"),
     ("monitor breakpoints hardware", "hardware"),
     ("break blink.ino:setup", "Breakpoint 1"),
     ("break loop", "Breakpoint 2"),
     ("break LedOn","Breakpoint 3"),
     ("break LedOff", "Breakpoint 4"),
     ("break LedInit", "Breakpoint 5"),
     ("continue", "SIGSYS"),
     ("delete 3", ""),
     ("continue", "Breakpoint 1, setup"),
     ("continue", "Breakpoint 5, LedInit"),
     ("continue", "Breakpoint 2, loop"),
     ("next", "SIGSYS"),
     ("delete 5", ""),
     ("finish", "LedOn"),
     ("monitor breakpoints all"),
     ("$SUCCESS-IF", "Breakpoint mode cannot be changed on this MCU"),
     ("break LedInit", "Breakpoint 6"),
     ("continue", "Breakpoint 4, LedOff"),
     ("next", "}"),
     ("next", "delay(1000)")) + epilog),


# test whether flash memory is loaded up without any error
    "flash" : (
    ('small', 'medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'arduino', 'noadc', 'noautopc'),
    "flashed",
    "",
    "",
    (("set logging file log/flash.log", ""),) + prolog + \
    (("load", "Start address 0x"),
     ("break flashOK", "Breakpoint 1 at"),
     ("break flashError", "Breakpoint 2 at"),
     ("continue", "Breakpoint 1, flashOK ()")) + epilog),

# test recursive functions
# test up/down
# test conditional stop
# test run command
# software watchpoint
    "fibonacci" : (
    ('small', 'medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'arduino', 'noadc', 'noautopc'),
    "fibonacci",
    "",
    "",
    (("set logging file log/fib.log", ""),) + prolog + \
    (("load", "Start address 0x"),
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
     ("continue", "Breakpoint 1")) + epilog),

# test OOP debugging - make sure, that LTO is disabled!
# test maximal BP setting (set to 4!)
    "oop" : (
    ('medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'arduino', 'noadc', 'noautopc'),
    "oop",
    "-fno-lto",
    "",
    (("set logging file log/oop.log", ""),) + prolog + \
    (("load", "Start address 0x"),
     ("whatis r", "Rectangle"),
     ("ptype r", "type = class Rectangle : public TwoDObject"),
     ("print r", "$1 = {<TwoDObject> = {x ="),
     ("list oop.ino:setup", "setup(void)"),
     ("b 83", "Breakpoint 1"),
     ("b 92", "Breakpoint 2"),
     ("b 111", "Breakpoint 3"),
     ("continue", "Breakpoint 1"),
     ("print r","$2 = {<TwoDObject> = {x = 10, y = 11}, height = 5, width = 8}"),
     ("continue", "Serial.println(F(\"Move s by +10, +10:\"));"),
     ("dis 1", ""),
     ("continue", "Breakpoint 3"),
     ("print s", "$3 = {<Rectangle> = {<TwoDObject> = {x = 15, y = 15}, height = 5,")) + epilog),

#tests terminal I/O and heavy IRQ load
    "tictactoe" : (
    ('large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'arduino', 'noadc', 'noautopc'),
    "tictactoe",
    "",
    "",
    (("set logging file log/tictactoe.log", ""),) + prolog + \
    (("load", "Start address 0x"),
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
     ("c", "211")) + epilog),

# tests safe and interruptible single-step execution
# INT 0 is enabled and switched active by setting the IRQ pin as an output
    "singlestep" : (
    ('small', 'medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'arduino', 'noadc', 'noautopc'),
    "isr",
    "",
    "",
    (("set logging file log/isr.log", ""),) + prolog +
    (("load", "Start address 0x"),
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
     ("n", "__vectors")) + epilog),

# load something into EEPROM
    "eeprom" : (
    ('small', 'medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'nonarduino', 'noadc', 'noautopc'),
    "ceeprom",
    "",
    "",
    (("set logging file log/eeprom.log", ""),) + prolog + \
    (("load", "Start address 0x"),
     ("break loop", ""),
     ("continue", "Breakpoint 1, loop"),
     ("p ee_data", "data that's loaded straight into EEPROM"),
     ("p ver", "data that's loaded straight into EEPROM"),
     ("delete 1", ""),
     ("break final", "Breakpoint 2"),
     ("cont", "Breakpoint 2, final (OK=true)"),
     ("set var ee_data[0] = 'X'", ""),
     ("p ee_data", "Xata that's loaded straight into EEPROM")) + epilog),

# loads fuses and lockbits, which is silently ignored
# also loads signature, which is compared with the signature
# given when inoking pyavrocd
    "fuses" : (
    ('small', 'medium', 'large', 'huge', 'dw', 'jtag', 'pdi', 'updi', 'nonarduino', 'noadc', 'noautopc'),
    "fuses",
    "",
    "",
    (("set logging file log/fuses.log", ""),) + prolog + \
    (("load", "Start address 0x"),) + epilog),

# tests of the ability to simulate a two-word call/jmp instruction
# on a ATmega2560 in the high area of the memory (for all others
# it is just computing the average of 10 numbers)
    "simhigh" : (
    ('huge', 'dw', 'jtag', 'pdi', 'updi', 'arduino', 'noadc'),
    "sim2word_highjmp",
    "",
    "",
    (("set logging file log/sim2word_highjmp.log", ""),) + prolog + \
    (("load", "Start address 0x"),
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
     ("print avg", "= -7196"),) + epilog),

# switch off debugWIRE mode (if applicable)
# this test script should be run last in each sequence in order to disable debugWIRE
# We will check that SIGHUP is generated
    "off" : (
    ('last', 'small', 'medium', 'large', 'huge', 'dw', 'arduino', 'nonarduino', 'noadc', 'noautopc'),
    "",
    "",
    "",
    (("set logging file log/off.log", ""),) + prolog + \
    (("monitor debugwire disable",  ""),
     ("$SUCCESS_IF", "This is not a debugWIRE target"),
     ("continue", "SIGHUP"),) + epilog),

# check that MCU is categorized as a MCU with a dirty PC
    "dirty" : (
    ('dirty', 'dw', 'jtag'),
    "",
    "",
    "",
    (("set logging file log/dirty.log", ""),) + prolog + \
    (("monitor debugwire enable",  "Fatal error:", "This is not a debugWIRE target"),
     ("monitor info", "MCU cannot be debugged because of stuck-at-1 bit")) + epilog) }

