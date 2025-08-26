# Monitor commands

Pyavrocd implements several `monitor` commands. These can be used to control important aspects of the GDB server. One important command is the `monitor debugwire enable` command, which enables debugWIRE mode on MCUs supporting this interface.

| Command                                               | Action                                                       |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| `monitor breakpoints` [`all`\|`software`\|`hardware`] | Restricts the kind of breakpoints the hardware debugger can use. Either *all* types are permitted, only *software* breakpoints are allowed, or only *hardware* breakpoints can be used. Using all kinds is the default. |
| `monitor caching` [`enable`\|`disable`]               | The loaded executable is cached in the gdbserver when *enabled*, which is the default setting. **(+)** |
| `monitor debugwire` [`enable`\|`disable`]             | DebugWIRE mode will be enabled or disabled. When enabling it, the MCU will be reset, and you may be asked to power-cycle the target. After disabling debugWIRE mode, one has to exit the debugger. Afterward, the MCU can be programmed again using SPI programming. |
| `monitor help`                                        | Display help text.                                           |
| `monitor info`                                        | Display information about the target and the state of the debugger. |
| `monitor load` [`readbeforewrite`\|`writeonly`]       | When loading an executable, either each flash page is compared with the content to be loaded, and flashing is skipped if the content is already there, or each flash page is written without reading the current contents beforehand. The first option is the default option for debugWIRE targets. For JTAG targets, the overhead of checking whether the page content is identical is so high that the *writeonly* option is the default. |
| `monitor onlyloaded` [`enable`\|`disable`]            | Execution is only possible when a `load` command was previously executed, which is the default. If you want to start execution without loading an executable first, you need to disable this mode. |
| `monitor rangestepping `[`enable`\|`disable`]         | The GDB range-stepping command is supported or disabled. Default is that it is *enabled*.  **(+)** |
| `monitor reset`                                       | Resets the MCU.                                              |
| `monitor singlestep` [`safe`\|`interruptible`]        | Single-stepping can be performed in a *safe* way, where single steps are shielded against interrupts. Otherwise, a single step can lead to a jump into the interrupt dispatch table. The *safe* option is the default. |
| `monitor speed` [`low`\|`high`]                       | Set the communication speed limit to the target to `low` (=150kbps) (default) or to `high` (=300kbps); without an argument, the current communication speed and speed limit are printed.**(*)** |
| `monitor timer` [`freeze`\|`run`]                     | Timers can either be *frozen* when execution is stopped, or they can *run* freely. The latter option is helpful when PWM output is crucial and is the default. |
| `monitor verify` [`enable`\|`disable`]                | Verify flash after loading each flash page. Since the cost of verification is not negligible, the default setting is for this option to be *disabled*. |
| `monitor version`                                     | Show version of the gdbserver.                               |

All commands can, as usual, be abbreviated. For example, `mo d e` is equivalent to `monitor debugwire enable`. If you use a command without an argument, the current setting is printed.

Commands marked with **(+)** are not implemented in dw-link; those marked with **(*)** are specific to dw-link.

