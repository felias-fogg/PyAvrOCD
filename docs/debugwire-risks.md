# <s>Smoking</s> debugWIRE can be Dangerous to the Health of your MCU

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/smoking_ic_breit.png" width="90%">
</p>

While debugWIRE is an excellent concept, as it requires no GPIO sacrifice for debugging, it can be harmful to the MCU. Once the MCU has been brought into debugWIRE mode (using, for example, the `monitor debugwire enable` command), the RESET line can no longer be used to reset the chip, and it is impossible to use SPI programming to change fuses, particularly the debugWIRE enable (DWEN) fuse. If something goes wrong while entering debugWIRE mode, this could mean that you "bricked" your chip, since communication with the MCU is no longer possible. So, what can go wrong, and how can you resurrect the chip?

There are essentially five different scenarios:

1. The classical problem is a capacitor on the RESET line, either for noise suppression or as a means to implement auto-reset on an Arduino board such as the Uno. Similarly, a resistor that is too strong or a dedicated reset circuit could pose a problem. In these cases, one can change the DWEN fuse using SPI programming, but communication over the debugWIRE line (the RESET line) is impossible.
The cure is apparent: Remove the resistor, capacitor, or reset circuit (or cut the trace to it). Afterward, it should be possible to connect to the MCU using the debugger (via pyavrocd).

2. All **ATmega48** and **ATmega88** variants without a P or A suffix exhibit unusual behavior. Note that this applies to MCUs purchased from official distributors.  They have stuck-at-1 bits in the program counter, they refuse to let their DWEN fuse be set, or, if one is successful, it is impossible to leave debugWIRE mode again. By now, they are identified by pyavrocd before the DWEN bit is set, so that the only annoying thing about them is that they are not debuggable.

3. Another cause for trouble could be that the MCU is operated in an unstable electrical environment. This could mean that the supply voltage is fluctuating, an unstable external clock is used, blocking capacitors between (A)Vcc and (A)GND are missing, or, another classic, AVcc and/or AGND are not connected to the power rail. In these cases, unpredictable things can happen, and the MCU might not be responsive after having been switched into debugWIRE mode. In this case, repairing the fault, e.g., soldering a blocking capacitor between Vcc and GND, may or may not resolve the issue.

4. The MCU could be a non-genuine product. Since such products do not satisfy all the specifications of genuine MCUs, these MCUs might be able to enter debugWIRE, but then one is stuck. Or debugWIRE mode is not supported at all.

5. It could be that you can enter debugWIRE mode and debug your chip, but getting back to normal mode is impossible. This may be caused by setting some fuses when switching to debugWIRE mode that prevent the return to normal mode. If you unprogrammed `SPIEN` (Serial program downloading) and/or programmed `RSTDSBL`, the fuse to disable the reset line, then it is possible to leave debugWIRE mode, but you cannot use SPI programming afterward. When you let pyavrocd handle the fuses, this cannot happen.

6. There are apparently unknown reasons that can make a chip unresponsive when switching to debugWIRE mode. I have no idea why this happens. And usually, there is no easy recovery method (but see below).

If none of the above-mentioned recovery methods work, the last resort is *high-voltage programming*. This means that 12 volts are applied to the RESET line and then signals are sent to the MCU over different lines. If you have an MCU with a DIP footprint, you can use a [breadboard high-voltage programmer](https://github.com/felias-fogg/RescueAVR) or a specially designed ["HV fuse programmer"](https://www.tindie.com/products/fogg/rescueavr-hv-fuse-programmer-for-avrs/). For MCUs with an SMD footprint, you would need to buy a breadboard adapter.

Having said all that, my experience is that if you take care of the potential problems mentioned in points 1-5, it is unlikely that your MCU will get bricked. But it doesn't mean that it is impossible either. JTAG and UPDI are definitely the more robust debugging interfaces.

