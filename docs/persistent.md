# Persistent Debugging

Most of the time, one-shot debugging will be enough to locate a problem. Sometimes, however, you may need to have a more persistent debugging scenario. If a bug shows up only after some time, you may want to leave the MCU running until the point at which something goes wrong, and then continue with your debugging efforts. There are basically three possible ways to achieve that.

## Extended debugging session

The most straightforward way is to start a debugging session and then run the program on the MCU until something happens, even if this takes a couple of days. However, it may be the case that you need the debug probe for something different, or that you want to terminate the debugging session temporarily. For these situations, the two approaches below can be helpful.

## Disconnecting from the MCU

One could think about disconnecting the debug probe from the MCU and then waiting for the disaster to happen. Only then, one reconnects the debug probe to the MCU and studies the state the program is in. In order to support such an approach, PyAvrOCD provides the command-line option `--attach`. If this option is specified, PyAvrOCD will try to connect to the on-chip debugging module without setting any fuses and without a reset. If successful, you can then inspect the state of the program, change things, and continue execution.

This works always for UPDI targets. For debugWIRE targets, you need to have started the target using a debugger and switched the target to debugWIRE mode. For JTAG targets, you need to have started the MCU using a debugger and used the command `monitor atexit stay` before terminating the debugging session.

## Disconnecting from PyAvrOCD

Instead of disconnecting from the MCU and terminating the GDB server, one could leave the GDB server running. This is supported in the *extended remote mode*, which you enter when you use the GDB command `target extended-remote <port>` instead of `target remote <port>`. When disconnecting, quitting, detaching, or killing, PyAvrOCD will not terminate but will wait for GDB to reconnect, attach, or run again. In addition, in this mode, the `run` and `attach` commands are available.

If PyAvrOCD is invoked with the `--once` option, the GDB commands `disconnect`, `detach`, and `quit` will immediately terminate the GDB server, even when in extended remote mode. The command `monitor exit` will also lead to the immediate termination of PyAvrOCD, regardless of mode and option. The following table summarizes this somewhat complicated state of affairs.

| GDB Command    | Normal remote mode          | Extended remote mode                                         | Extended remote mode with option `--once`                    |
| -------------- | --------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `disconnect`   | Terminates PyAvrOCD         | Disconnects GDB from PyAvrOCD                                | Terminates PyAvrOCD                                          |
| `detach`       | Terminates PyAvrOCD         | Continues execution of the current program and detaches from it, but does not disconnect from PyAvrOCD | Terminates PyAvrOCD                                          |
| `kill`         | Terminates PyAvrOCD         | MCU reset                                                    | MCU reset                                                    |
| `quit`         | Terminates PyAvrOCD and GDB | Continues execution of the current program, detaches from it, and terminates GDB | Terminates PyAvrOCD and GDB                                  |
| `run`          | Not available               | Restarts execution of the current program (arguments are ignored) | Restarts execution of the current program (arguments are ignored) |
| `attach <num>` | Not available               | Attaches to detached program (argument is ignored)           | Useless because it is not possible to detach from a program  |
| `monitor exit` | Terminates PyAvrOCD         | Terminates PyAvrOCD                                          | Terminates PyAvrOCD                                          |

