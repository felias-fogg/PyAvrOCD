# Flash Wear

When setting a breakpoint in a program, one usually does not think about the underlying mechanism that stops the program at the particular point where the breakpoint has been set. Technically, this can be done by *hardware breakpoints* or *software breakpoints*. A hardware breakpoint is implemented as a register that is compared to the actual program counter. If the PC is equal to the register value, execution is stopped. Usually, only a few such hardware breakpoints are available. On a debugWIRE device, there is just one. On AVR JTAG ATmegas, we have four; on UPDI MCUs, there are two. Software breakpoints are implemented by placing a particular trap instruction into the machine code. On AVRs, this is the `BREAK` instruction.

There are pros and cons to each type of breakpoint. Hardware breakpoints are faster to set and to clear because they do not involve reprogramming flash memory. Further, they do not lead to *[flash wear](https://en.wikipedia.org/wiki/Flash_memory#Memory_wear)* as software breakpoints do. However, as mentioned, there are usually only very few hardware breakpoints.

PyAvrOCD will make use of hardware breakpoints whenever possible and use software breakpoints only as a fallback. Further, the most recent breakpoint asserted by GDB will always be implemented as a hardware breakpoint because it is very likely that it is a temporary breakpoint. *(not yet implemented for JTAG)*

## The flash wear problem

So, how severe is the flash wear problem? The data sheets state that for classic AVR MCUs, the guaranteed flash endurance is 10,000 write/erase cycles. For the more recent MCU with UPDI interface, it is only 1000 cycles! These are probably quite conservative numbers guaranteeing endurance even when the chips are operated close to the limits of their specification (e.g., at 50° C).

Let’s assume an eager developer who reprograms the MCU every 10 minutes with an updated version of the program and debugs using five software breakpoints that she sets and clears during each episode. That will probably result on average in 3 additional reprogramming operations on an individual page, leading to 4 such operations in 10 minutes or 192 such operations on one workday. So, she could hit the limit for the modern AVR MCUs after one working week already. The classic AVRs can be used for 10 weeks. This holds only if she does not set and clear breakpoints all the time, but is instead rather careful about doing so. Further, the GDB server needs to make sure not to require superfluous breakpoint set/clear operations.

Different [GDB servers vary in their ability to minimize flash wear](https://arduino-craft-corner.de/index.php/2025/05/05/stop-and-go/), with PyAvrOCD being very competitive. Actually, it is better than all other debugging solutions when it comes to breaking at two-word instructions. All open-source GDB servers and the Microchip solutions, as well, will lead to two flash reprogramming operations for each breakpoint hit at a two-word instruction! Thus, the flash endurance limit might be reached much earlier if our eager software developer uses conditional breakpoints, for example.

All in all, as Microchip states, you should not ship MCUs to customers that have been used heavily in debugging.

## Using only hardware breakpoints

Can it be a solution to use only hardware breakpoints? It will definitely reduce flash wear to zero (well, except for reprogramming the target). However, it can also be very inconvenient because there are only a few of them. You can force the use of only hardware breakpoints by using the following `monitor` command.

```
monitor breakpoint hardware
```

One must be aware, though, that there are some slight problems here when single-stepping. First, the internal stepping function sometimes needs a hardware breakpoint in order to implement interrupt-safe single-stepping. For this reason, the number of available hardware breakpoints is reduced by one if interrupt-safe single-stepping is enabled. This means that in debugWIRE mode, you actually cannot have safe single-stepping when you also want to set break points (including setting temporary breakpoints implicitly by step-over operations).

Second, since a step-over operation uses a temporary breakpoint, this can lead to the situation where, after starting the step-over operation with a single step on the GDB server level, it is discovered that too many breakpoints are necessary to complete the step-over operation. In order to mitigate this problem, the breakpoint at the location where the step-over operation has been initiated will not be asserted, and a warning message is given. This generates the correct behavior except when we are dealing with recursive functions.

Unfortunately, there is no way to detect this problem early enough at the level of the GDB server. And there does not seem to be an easy way to solve the issue on the GDB level. So, when using only hardware breakpoints, do not use the maximum number of breakpoints or refrain from the stepping-over operation (called `next` in GDB).