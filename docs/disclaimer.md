# Disclaimer

Note that, as is usual in life, there are some risks involved when using a tool. In particular, [the debugWIRE interface can be a serious health risk to your MCU](debugwire-risks.md). Even worse, all other aspects of the debugging package have the potential of doing harm to the tested MCU, to the target board, or to the attached devices. [Flash wear](flash-wear.md), for instance, is an issue when you use software breakpoints. Further, when using a debugger on an MCU that controls a system, stopping the execution of the controlling program might lead to erroneous behavior of the controlled system.

All in all, bear always in mind that [the software is provided "as is", without warranty of any kind](LICENSE).