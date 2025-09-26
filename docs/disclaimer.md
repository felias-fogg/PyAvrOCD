# Disclaimer

Note that, as is usual in life, there are some risks involved when using a tool. In particular, [the debugWIRE interface can be a serious health risk to your MCU](limitations.md#debugwire-can-brick-mcus). Even worse, all other aspects of the debugging package have the potential of doing harm to the tested MCU or its environment. [Flash wear](limitations.md#flash-wear), for instance, is an issue when you use software breakpoints.  Moreover, the user of a debugger may also be in danger because debugging can drive you crazy. Sometimes [bugs might disappear](limitations.md#disappearing-bugs) while other [bugs appear out of thin air](limitations.md#bugs-appearing-out-of-thin-air) while debugging.

Further, the hardware debuggers, the PyAvrOCD server, and the GDB debugger have a [number of limitations](limitations.md), which may lead to a behavior of the MCU that differs from when no debugger is present. Finally, when using a debugger on an MCU that controls a system in real-time, stopping the execution of the controlling program in the middle of something might lead to erroneous behavior of the controlled system. For example, when communicating with other systems, stopping the communication in the middle of an exchange might violate the communication protocol, which might be tolerable. If you are controlling a chemical plant with your MCU, there might be more dire consequences.

All in all, bear in mind that [the software is provided "as is", without warranty of any kind](license-link.md).

