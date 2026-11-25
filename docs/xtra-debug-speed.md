# Debugging Speed

Running the debuggers on the test battery, I got the following results for an ATmega328P.

| Debugger              | Time |
| --------------------- | ---- |
| Atmel-ICE             | 4:08 |
| SNAP                  | 4:16 |
| dw-link               | 4:22 |
| PICkit4               | 4:40 |
| Xplained Mini (mEDBG) | 5:18 |

These times include: (a) compilation, (b) starting up the debugger, (c) loading the binary, (d) interacting with the debugger using Pexpect, and (e) the time needed for executing the debug commands. While (a), (b), and (d) are independent of the debugger, loading and execution are debugger-specific.