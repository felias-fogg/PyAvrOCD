# Monitor commands

Pyavrocd implements several `monitor` commands. These can be used to control important aspects of the GDB server. One important command is the `monitor debugwire enable` command, which enables debugWIRE mode on MCUs supporting this interface.

| Command                                                | Action                                                       |
| ------------------------------------------------------ | ------------------------------------------------------------ |
| `monitor atexit` [`stayindebugwire`\|`leavedebugwire`] | When specifying `leavedubgwire`, then debugWIRE mode will be left when exiting the debugger. This is useful when dealing with embedded debuggers. The default is `stayindebugwire`, i.e., debugWIREmode will not be left when exiting the debugger. **(+)** |
| `monitor breakpoints` [`all`\|`software`\|`hardware`]  | Restricts the kind of breakpoints the hardware debugger can use. Either `all` types are permitted, only `software` breakpoints are allowed, or only `hardware` breakpoints can be used. Using `all` kinds is the default. |
| `monitor caching` [`enable`\|`disable`]                | The loaded executable is cached in the gdbserver when `enabled`, which is the default setting. **(+)** |
| `monitor debugwire` [`enable`\|`disable`]              | DebugWIRE mode will be `enable`d or `disable`d. When enabling it, the MCU will be reset, and you may be asked to power-cycle the target. After disabling debugWIRE mode, one has to exit the debugger. Afterward, the MCU can be programmed again using SPI programming.<br> |
| `monitor erasebeforeload` [`enable`\|`disable`]        | This monitor option controls whether the flash is erased before an executable is loaded, which is the default for all targets, except for debugWIRE targets, which do not have a chip erase command in debug mode. **(+)** |
| `monitor help`                                         | Display help text.                                           |
| `monitor info`                                         | Display information about the target and the state of the debugger. |
| `monitor load` [`readbeforewrite`\|`writeonly`]        | When loading an executable, either each flash page is compared with the content to be loaded, and flashing is skipped if the content is already there, or each flash page is written without reading the current contents beforehand. The first option is the default option for debugWIRE targets. For JTAG targets, the overhead of checking whether the page content is identical is so high that the `writeonly` option is the default. |
| `monitor onlywhenloaded` [`enable`\|`disable`]         | Execution is only possible when a `load` command was previously executed, which is the default. If you want to start execution without loading an executable first, you need to `disable` this mode. |
| `monitor rangestepping `[`enable`\|`disable`]          | The GDB range-stepping command is supported or disabled. The default is that it is `enable`d.  **(+)** |
| `monitor reset`                                        | Resets the MCU.                                              |
| `monitor singlestep` [`safe`\|`interruptible`]         | Single-stepping can be performed in a `safe` way, where single steps are shielded against interrupts. Otherwise, a single step can lead to a jump into the interrupt dispatch table. The `safe` option is the default. |
| `monitor speed` [`low`\|`high`]                        | Set the communication speed limit to the target to `low` (=150kbps) (default) or to `high` (=300kbps); without an argument, the current communication speed and speed limit are printed.**(*)** |
| `monitor timer` [`run`\|`freeze`]                      | Timers can either be `frozen` when execution is stopped, or they can `run` freely. The latter option is helpful when PWM output is crucial and is the default. |
| `monitor verify` [`enable`\|`disable`]                 | Verify flash after loading each flash page. The default setting is for this option to be `enable`d. |
| `monitor version`                                      | Show version of the gdbserver.                               |

All commands can, as usual, be abbreviated. For example, `mo d e` is equivalent to `monitor debugwire enable`. If you use a command without an argument, the current setting is printed.

Commands marked with **(+)** are not implemented in dw-link; those marked with **(*)** are specific to dw-link.

