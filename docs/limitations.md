# Limitations

The debugging system, consisting of the hardware debugger, the GDB server, and GDB itself, has a number of inherent limitations. Some aspects of the hardware may not be debuggable at all or only with some extra effort. And sometimes it can happen that the behavior of the MCU in a debugging environment is significantly different from the behavior shown in a non-debugging environment. This can, in particular, lead to what has been called [Heisenbugs](https://en.wikipedia.org/wiki/Heisenbug). These are bugs that seem to disappear when one tries to locate them using debugging methods.

## Bootloader

Bootloaders will usually be erased when running the debugger.

In a debugWIRE context, the entire chip needs to be erased if some lock bits are set. Further, the `BOOTRST` fuse is disabled so that execution always starts at location 0x0000. If one wants to have a bootloader present, because it may provide services, such as writing to flash memory, one needs to load it before starting a debugging session without setting any lock bits. If one, in addition, wants to debug the bootloader, one can disallow that PyAvrOCD manages the `BOOTRST` fuse by using the command line option `--manage nobootrst`.

When debugging with JTAG, the chip will be erased each time a new binary is loaded. Suppose you want to keep the bootloader in memory. In that case, you can request not to erase the chip before loading a binary, erasing each flash page only when some code needs to be loaded into this page: `--erasebeforeload disable`. However, this will severely slow down the process of loading a binary.

## Low CPU clock frequency

Low CPU clock frequencies can make the debugging process sluggish or even impossible.

When using debugWIRE, the communication speed with the target is determined by the clock frequency of the target. It is usually clock frequency divided by 8, but not higher than 250k bps. If you use a clock frequency of 128 kHz, then the communication speed will be 16000 bps, which is quite slow. If the `CKDIV8` fuse is programmed, then this would be only 2000 bps, at which point some of the hardware programmers may time out.

With JTAG, things are similar. While the JTAG programming clock frequency is independent of the clock frequency of the target, the JTAG debugging frequency should not be higher than one-quarter of the MCU clock frequency.

In general, one should not choose CPU clock frequencies below 1 MHz while debugging.

## Low-power properties

Almost all power-saving features of the MCU are disabled while debugging.

The reason for this is that all clocks need to be running so that the communication between the hardware debugger and the OCD does not break down. So, the functional behavior of the MCU can be debugged, but low-power properties cannot be tested while debugging.

## Compiler optimizations

When trying to debug a program compiled with the 'usual' compiler options, one often ends up in unexpected places or receives warnings.

Usually, the compiler optimizes for space, trying to fit as much program code as possible into the limited amount of flash memory. This, however, might imply that code is reordered and inlined. This means that single-stepping can be confusing, that one cannot stop at some places, or that a `finish` command will lead to an error message.

When using the `-Og` compiler optimization option, the compiler aims at preserving the structure of the program at the expense of perhaps using more flash memory. In the Arduino IDE 2, this is forced by enabling `Optimize for Debugging` in the `Sketch` menu.

This supports the debugging as long as one is hunting bugs in the program logic. However, some bugs may silently disappear, or the effects of a bug may change. These bugs, which are called Heisenbugs, often appear in connection with access to data on the stack, [with `volatile` data, or with race conditions](https://arduino-craft-corner.de/index.php/2025/01/19/volatilitity-race-conditions-and-heisenbugs/). Thus, if a bug disappears when optimizing for debugging is enabled, one should watch out for such a Heisenbug and perhaps debug a binary that has been compiled without the optimization for debugging option.

## Link-time optimization

Link-time optimization can optimize away important structural debug information about C++ objects and global variables.

Link-time optimization is a relatively new technique and was introduced into the Arudinio IDE only in 2020.  It optimizes across all compilation units and is able to prune away unused functions and data structures, as well as inlining functions across compilation units.

The disadvantage is that [link-time optimization prunes away essential information about C++ objects](https://arduino-craft-corner.de/index.php/2021/12/15/link-time-optimization-and-debugging-of-object-oriented-programs-on-avr-mcus/) so that class instances all of a sudden seem to be variables of a structure type. Furthermore, they prune away the info that variables are global, which means that in the `VARIABLES` debugging pane of the Arduino IDE 2, no variables are displayed. Finally, because of aggressive inlining, this technique can provoke stack overflows.

All these problems disappear when link-time optimization is disabled. However, in this case, much more code space is needed.

## Instruction execution timing



## USB communication

## Breakpoints in interrupt routines

## Conditional breakpoints

## Single-stepping
