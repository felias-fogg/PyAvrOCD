# Testing



## Running tests

### Pylint

Run pylint in the root folder:

```shell
poetry run ./run-pylint.sh
```



### Unit tests

Run unit tests in the root folder using:

```shell
poetry run pytest
```



### Integration tests

Run integration test in root folder (probably only works on POSIX
OSs). First start the server in one terminal window:

```
tests/serv.sh <mcu> [<verbosity level>]
```
Then start the integration tests in another window (root directory)

```shell
poetry run python3 -m tests.integration_test -d <mcu> -c <clock in MHz>
```

Afterwards, you need to kill the `serv.sh` script with CTRL-C



## Developing new tests

### Unit tests

The idea with unit tests is clear: Write a test for each and every method and try to cover as many corner cases as possible.



### Integration tests

The integration tests test the interaction in the entire system from the MCU over the GDB server to the GDB debugger. It should cover as many cases as possible (and feasible).



#### Challenges of the different test sketches

- **live:** Running live tests with optionally enable debugWIRE and then the live tests `monitor Livetests`
- **monitor commands**: Check all monitor command outputs that work on all servers, check timers run/freeze
- **blink:** breaks in ISR, disable and delete breaks, conditional breaks, info about breakpoints, display command, asynchronous stop
- **break:** hardware breakpoints only (needs to get extra script for JTAG)
- **flash**: Test load command (flash is filled up)
- **fibonacci:** go stack up (and down), backtrace, set (software) watchpoint
- **oop:** Debug OOP program (no-lto!), whatis, ptype
- **tictactoe:** Complex program, input simulated by setting variables.
- **single-step:** demonstrates interrupt-safe single-stepping
- **eeprom**: Demonstrates loading directly into EEPROM, EEPROM manipulation in the program and on the debugger level.
- **fuse:** Demonstrates that including fuses and lockbits is tolerated but ignored. Signatures are  compared, however.
- **off**: Disables debugWIRE.



#### Memory types

In the LiveTest, we read and write

- flash memory (no writing for JTAG)
- SRAM
- EEPROM
- general registers
- special registers (PC, SREG, SP)

The following memory areas are not accessible in debugging mode

- fuses (dw: -, JTAG: -)
- lockbits (dw: -, JTAG: -)
- signature (dw: R. JTAG: -)



For programming (loading the ELF binary):

- flash memory
- SRAM (not possible)
- EEPROM (works both in dw + JTAG), for JTAG, it needs protection against chip erase.
- fuse (JTAG could work, dw: -), will be explicitly blocked, since this could interfere with debugging
- lockbits (JTAG could work, dw: -), same thing
- signature (only read. so can be ignored), same thing
- user signature (JTAG could work for ATmegaxxxRFR2)



#### GDB commands

The following table provides an alphabetical list of all ARM GDB commands copied from the [ARM website](https://developer.arm.com/documentation/101471/6-6-0/Arm-Debugger-commands/Arm-Debugger-commands-listed-in-alphabetical-order?lang=en).  Commands undefined in AVR-GDB have been removed. Commands irrelevant for testing are crossed out. Commands appearing in one of the test scripts are marked in bold, and commands that have issues are marked in italics.

| Debugger command                                             | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ~~add-symbol-file~~                                          | ~~Loads additional debug information into the debugger.~~    |
| *advance*                                                    | Sets a temporary breakpoint at the specified address and calls the debugger `continue`command.<br> *When used after a reset tries to set a breakpoint in an area outside the the memory limits. No idea why.* |
| ~~append~~                                                   | ~~Reads data from memory or the result of an expression and appends it to an existing file.~~ |
| ~~awatch~~                                                   | ~~Sets a watchpoint for a data symbol.~~                     |
| **backtrace**                                                | Displays a numbered list of the calling stack frames including the function names and source line numbers. |
| **break**                                                    | Sets an execution breakpoint at a specific location.         |
| ~~cd~~                                                       | ~~Changes the current working directory.~~                   |
| **clear**                                                    | Deletes a breakpoint at a specific location.                 |
| **condition**                                                | Sets a stop condition for a specific breakpoint or watchpoint. |
| **continue**                                                 | Continues running the target.                                |
| define                                                       | Derives new user-defined commands from existing commands.    |
| **delete breakpoints**                                       | Deletes one or more breakpoints or watchpoints.              |
| ~~directory~~                                                | ~~Defines additional directories to search for source files.~~ |
| **disable breakpoints**                                      | Disables one or more breakpoints or watchpoints.             |
| ~~disassemble~~                                              | ~~Displays the disassembly for the function surrounding a specific address or the disassembly for a specific address range.~~ |
| ~~document~~                                                 | ~~Adds integrated help for a new user-defined command.~~     |
| **down**                                                     | Moves and displays the current frame pointer down the call stack towards the bottom frame. |
| ~~down-silently~~                                            | ~~Moves the current frame pointer down the call stack towards the bottom frame.~~ |
| ~~dump~~                                                     | ~~Reads data from memory or the result of an expression and writes it to a file.~~ |
| ~~echo~~                                                     | ~~Displays only textual strings.~~                           |
| **enable breakpoints**                                       | Enables one or more breakpoints or watchpoints by number.    |
| ~~end~~                                                      | ~~Terminates conditional blocks when using the `define`, `if`, and `while` commands.~~ |
| **exit**                                                     | Quits the debugger session.                                  |
| file                                                         | Loads debug information from an image into the debugger and records the entry point address for future use by the `run` and `start` commands. |
| finish                                                       | Continues running the device to the next instruction after the selected stack frame finishes. |
| flash erase-device                                           | Erases the memory on a specified flash device.               |
| ~~flash erase-image-sectors~~                                | ~~Erases all sectors of flash memory in the specified image.~~ |
| ~~flash load~~                                               | ~~Loads sections from an image into one or more flash devices.~~ |
| ~~flash load-multiple~~                                      | ~~Load multiple images on to your target.~~                  |
| frame                                                        | Sets the current frame pointer in the call stack and also displays the function name and source line number for the specified frame. |
| ~~[handle](https://developer.arm.com/documentation/101471/6-6-0/Arm-Debugger-commands/Arm-Debugger-commands-listed-in-alphabetical-order/handle?lang=en)~~ | ~~Controls the handler settings for one or more signals or exceptions.~~ |
| ~~hbreak~~                                                   | ~~Sets a hardware execution breakpoint at a specific location.~~ |
| ~~help~~                                                     | ~~Displays help information for a specific command or a group of commands listed according to specific debugging tasks.~~ |
| ~~if~~                                                       | ~~Allows you to write scripts that conditionally execute debugger commands.~~ |
| ignore                                                       | Sets the ignore counter for a breakpoint or watchpoint condition. |
| info address                                                 | Displays the location of a symbol.                           |
| ~~info all-registers~~                                       | ~~Displays the name and content of grouped registers for the current stack frame.~~ |
| **info breakpoints**                                         | Displays information about the status of all breakpoints and watchpoints. |
| ~~info breakpoints capabilities~~                            | ~~Displays a list of parameters that you can use with breakpoint commands for the current connection.~~ |
| info classes                                                 | Displays C++ class names.                                    |
| info files                                                   | Displays information about the loaded image and symbols.     |
| info frame                                                   | Displays stack frame information at the selected position.   |
| info functions                                               | Displays the name and data types for all functions.          |
| ~~info handle~~                                              | ~~Displays information about the handling of signals or processor exceptions.~~ |
| info locals                                                  | Displays all local variables for the current stack frame.    |
| info members                                                 | Displays the name and data types for all class member variables that are accessible in the function corresponding to the selected stack frame. |
| ~~info os~~                                                  | ~~Displays the current state of the Operating System (OS) support.~~ |
| info registers                                               | Displays the name and content of all application level registers for the current stack frame. |
| ~~info sharedlibrary~~                                       | ~~Displays the names of the loaded shared libraries, the base address, and whether the debug symbols of the shared libraries are loaded or not.~~ |
| ~~info signals~~                                             | ~~Displays information about the handling of signals or processor exceptions.~~ |
| info sources                                                 | Displays the names of the source files used in the current image being debugged. |
| info stack                                                   | Displays a numbered list of the calling stack frames including the function names and source line numbers. |
| info symbol                                                  | Displays the symbol name at a specific address.              |
| info target                                                  | Displays information about the loaded image and symbols.     |
| ~~info threads~~                                             | ~~Displays information about the available threads.~~        |
| info variables                                               | Displays the name and data types for all global and static variables. |
| ~~info watchpoints~~                                         | ~~Displays information about the status of all breakpoints and watchpoints.~~ |
| ~~info watchpoints capabilities~~                            | ~~Displays a list of parameters that you can use with watchpoint commands for the current connection.~~ |
| inspect                                                      | Displays the output of an expression and also records the result in a new debugger variable. |
| **interrupt, stop**                                          | Interrupts the target and stops the application if it is running. |
| **list**                                                     | Displays lines of source code surrounding the current or specified location. |
| **load**                                                     | Loads an image on to the target and records the entry point address for future use by the `run` and `start` commands. |
| ~~newvar~~                                                   | ~~Declares and initializes a new debugger convenience variable or register alias.~~ |
| **next**                                                     | Steps through an application at the source level stopping at the first instruction of each source line but stepping over all function calls. |
| nexti                                                        | Steps through an application at the instruction level but stepping over all function calls. |
| nexts                                                        | Steps through an application at the source level stopping at the first instruction of each source statement but stepping over all function calls. |
| ~~nosharedlibrary~~                                          | ~~Discards all loaded shared library symbols.~~              |
| **print**                                                    | Displays the output of an expression and also records the result in a new debugger variable. |
| **ptype**                                                    |                                                              |
| ~~pwd~~                                                      | ~~Displays the current working directory.~~                  |
| **quit**                                                     | Quits the debugger session.                                  |
| restore                                                      | Reads data from a file and writes it to memory.              |
| run                                                          | Starts running the target.                                   |
| ~~rwatch~~                                                   | ~~Sets a watchpoint for a data symbol.~~                     |
| select-frame                                                 | Moves the current frame pointer in the call stack.           |
| ~~set backtrace~~                                            | ~~Controls the default behavior when using the `info stack` command.~~ |
| ~~set breakpoint~~                                           | ~~Controls the automatic behavior of breakpoints and watchpoints.~~ |
| ~~set-directories~~                                          | ~~Defines additional directories to search for source files.~~ |
| ~~set endian~~                                               | ~~Specifies the byte order for use by the debugger.~~        |
| ~~set listsize~~                                             | ~~Modifies the default number of source lines that the `list` command displays.~~ |
| ~~set os~~                                                   | ~~Controls operating system settings in the debugger.~~      |
| ~~set print~~                                                | ~~Controls the current debugger print settings.~~            |
| ~~set step-mode~~                                            | ~~Controls the default behavior of the `step` and `steps` commands.~~ |
| ~~set substitute-path~~                                      | ~~Modifies the search paths used by the debugger when it executes any of the commands that look up and display source code.~~ |
| ~~set sysroot~~                                              | ~~Specifies the system root directory to search for shared library symbols.~~ |
| **set variable, set**                                        | Evaluates an expression and assigns the result to a variable, register, or memory address. |
| ~~sharedlibrary~~                                            | ~~Loads symbols from shared libraries.~~                     |
| ~~shell~~                                                    | ~~Runs a shell command in the debug session.~~               |
| ~~show~~                                                     | ~~Displays the debugger settings.~~                          |
| ~~show architecture~~                                        | ~~Displays the architecture of the target.~~                 |
| ~~show backtrace~~                                           | ~~Displays the behavior settings for use with the `info stack` command.~~ |
| ~~show breakpoint~~                                          | ~~Displays the breakpoint and watchpoint behavior settings.~~ |
| ~~show directories~~                                         | ~~Displays the list of directories to search for source files.~~ |
| ~~show endian~~                                              | ~~Displays the byte order setting in use by the debugger.~~  |
| ~~show listsize~~                                            | ~~Displays the number of source lines that the `list` command displays.~~ |
| ~~show print~~                                               | ~~Displays the debugger print settings.~~                    |
| ~~show step-mode~~                                           | ~~Displays the step setting for functions without debug information.~~ |
| ~~show substitute-path~~                                     | ~~Displays the search path substitution rules in use by the debugger when searching for source files.~~ |
| ~~show sysroot~~                                             | ~~Displays the system root directory in use by the debugger when searching for shared library symbols.~~ |
| ~~show version~~                                             | ~~Displays the version number of the debugger.~~             |
| source                                                       | Loads and runs a script file to control and debug your target. |
| start                                                        | Sets a temporary breakpoint, calls the debugger `run` command, and then deletes the temporary breakpoint when it is hit. |
| step                                                         | Steps through an application at the source level stopping on the first instruction of each source line including stepping into all function calls. |
| stepi                                                        | Steps through an application at the instruction level including stepping into all function calls. |
| steps                                                        | Steps through an application at the source level stopping on the first instruction of each source statement including stepping into all function calls. |
| **stop**                                                     | stop is an alias for interrupt.                              |
| symbol                                                       | Loads debug information from an image into the debugger and records the entry point address for future use by the `run` and `start` commands. |
| **target remote**                                            |                                                              |
| **target extended-remote**                                   |                                                              |
| **tbreak**                                                   | Sets an execution breakpoint at a specific location and deletes the breakpoint when it is hit. |
| ~~thbreak~~                                                  | ~~Sets a hardware execution breakpoint at a specific location and deletes the breakpoint when it is hit.~~ |
| ~~thread~~                                                   | ~~Displays information about the current thread.~~           |
| ~~thread apply~~                                             | ~~Switches control to a specific thread to execute a debugger command and then switches back to the original state.~~ |
| unset                                                        | Modifies the current debugger settings.                      |
| **up**                                                       | Moves and displays the current frame pointer up the call stack towards the top frame. |
| ~~up-silently~~                                              | ~~Moves the current frame pointer up the call stack towards the top frame.~~ |
| **watch**                                                    | Sets a watchpoint for a data symbol.                         |
| ~~watch-set-property~~                                       | ~~Updates the properties of an existing watchpoint.~~        |
| **whatis**                                                   | Displays the data type of an expression.                     |
| where                                                        | Displays a numbered list of the calling stack frames including the function names and source line numbers. |
| ~~while~~                                                    | ~~Allows you to write scripts with conditional loops that execute debugger commands.~~ |
| x                                                            | Displays the content of memory at a specific address.        |



