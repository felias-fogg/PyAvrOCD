# Testing



## Running tests

### Pylint

Run pylint in the root folder:

```shell
poetry run pylint pyavrocd/
```



### Unit tests

Run unit tests in the root folder using:

```shell
poetry run pytest
```

With the following command, you generate a coverage report in the folder `cov/`

```bash
 poetry run pytest --cov-report=html:cov --cov=pyavrocd/
```

### Type checking

Run the static type checker with

```
poetry run mypy .
```



### End-to-end tests

Run end-to-end test (GDB CLI level) in folder `end-to-end` (probably only works on POSIX
OSs). First start the server in one terminal window:

```
serv.sh [<verbosity level>]
```
Then start the end-to-end tests in another window (also in the `end-to-end` folder)

```shell
poetry run python3 e2e_test.py -d <mcu> -c <clock in MHz>
```

Afterwards, you need to kill the `serv.sh` script with CTRL-C



## Developing new tests

### Unit tests

The idea with unit tests is clear: Write a test for each and every method and try to cover as many corner cases as possible.



### End-to-end tests

The end-to-end tests test the interaction in the entire system from the MCU over the GDB server to the GDB debugger. It should cover as many cases as possible (and feasible).



#### Challenges of the different test scripts

- **live:** Running live tests with optionally enable debugWIRE and then the live tests `monitor Livetests`
- **monitor commands**: Check all monitor command outputs that work on all servers, check timers run/freeze
- **blink:** breaks in ISR, disable and delete breaks, conditional breaks, info about breakpoints, display command, asynchronous stop
- **break:** hardware breakpoints only (needs to get extra script for JTAG)
- **flash**: Test load command (flash is filled up)
- **fibonacci:** go stack up (and down), backtrace, set (software) watchpoint
- **oop:** Debug OOP program (no-lto!), whatis, ptype
- **tictactoe:** Complex program, input simulated by setting variables.
- **single-step:** demonstrates interrupt-safe single-stepping
- **eeprom**: Demonstrates loading directly into EEPROM, EEPROM manipulation in the program, and on the debugger level.
- **fuse:** Demonstrates that including fuses and lockbits is tolerated but ignored. Signatures are compared to the actual MCU, however.
- **off**: Disables debugWIRE,
- **dirty:** Script for testing whether MCUs with stuck-at-1 bits are identified.



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
| <s>add-symbol-file</s>                                       | <s>Loads additional debug information into the debugger.</s> |
| ***advance***                                                | Sets a temporary breakpoint at the specified address and calls the debugger `continue`command.<br> *When used after a reset tries to set a breakpoint in an area outside the memory limits. No idea why.* |
| <s>append</s>                                                | <s>Reads data from memory or the result of an expression and appends it to an existing file.</s> |
| <s>awatch</s>                                                | <s>Sets a watchpoint for a data symbol.</s>                  |
| **backtrace**                                                | Displays a numbered list of the calling stack frames including the function names and source line numbers. |
| **break**                                                    | Sets an execution breakpoint at a specific location.         |
| <s>cd</s>                                                    | <s>Changes the current working directory.</s>                |
| **clear**                                                    | Deletes a breakpoint at a specific location.                 |
| **condition**                                                | Sets a stop condition for a specific breakpoint or watchpoint. |
| **continue**                                                 | Continues running the target.                                |
| <s>define</s>                                                | <s>Derives new user-defined commands from existing commands.</s> |
| **delete breakpoints**                                       | Deletes one or more breakpoints or watchpoints.              |
| <s>directory</s>                                             | <s>Defines additional directories to search for source files.</s> |
| **disable breakpoints**                                      | Disables one or more breakpoints or watchpoints.             |
| <s>disassemble</s>                                           | <s>Displays the disassembly for the function surrounding a specific address or the disassembly for a specific address range.</s> |
| <s>document</s>                                              | <s>Adds integrated help for a new user-defined command.</s>  |
| **down**                                                     | Moves and displays the current frame pointer down the call stack towards the bottom frame. |
| <s>down-silently</s>                                         | <s>Moves the current frame pointer down the call stack towards the bottom frame.</s> |
| <s>dump</s>                                                  | <s>Reads data from memory or the result of an expression and writes it to a file.</s> |
| <s>echo</s>                                                  | <s>Displays only textual strings.</s>                        |
| **enable breakpoints**                                       | Enables one or more breakpoints or watchpoints by number.    |
| <s>end</s>                                                   | <s>Terminates conditional blocks when using the `define`, `if`, and `while` commands.</s> |
| **exit**                                                     | Quits the debugger session.                                  |
| file                                                         | Loads debug information from an image into the debugger and records the entry point address for future use by the `run` and `start` commands. |
| finish                                                       | Continues running the device to the next instruction after the selected stack frame finishes. |
| flash erase-device                                           | Erases the memory on a specified flash device.               |
| <s>flash erase-image-sectors</s>                             | <s>Erases all sectors of flash memory in the specified image.</s> |
| <s>flash load</s>                                            | <s>Loads sections from an image into one or more flash devices.</s> |
| <s>flash load-multiple</s>                                   | <s>Load multiple images on to your target.</s>               |
| frame                                                        | Sets the current frame pointer in the call stack and also displays the function name and source line number for the specified frame. |
| <s>[handle](https://developer.arm.com/documentation/101471/6-6-0/Arm-Debugger-commands/Arm-Debugger-commands-listed-in-alphabetical-order/handle?lang=en)</s> | <s>Controls the handler settings for one or more signals or exceptions.</s> |
| <s>hbreak</s>                                                | <s>Sets a hardware execution breakpoint at a specific location.</s> |
| <s>help</s>                                                  | <s>Displays help information for a specific command or a group of commands listed according to specific debugging tasks.</s> |
| <s>if</s>                                                    | <s>Allows you to write scripts that conditionally execute debugger commands.</s> |
| ignore                                                       | Sets the ignore counter for a breakpoint or watchpoint condition. |
| info address                                                 | Displays the location of a symbol.                           |
| <s>info all-registers</s>                                    | <s>Displays the name and content of grouped registers for the current stack frame.</s> |
| **info breakpoints**                                         | Displays information about the status of all breakpoints and watchpoints. |
| <s>info breakpoints capabilities</s>                         | <s>Displays a list of parameters that you can use with breakpoint commands for the current connection.</s> |
| info classes                                                 | Displays C++ class names.                                    |
| info files                                                   | Displays information about the loaded image and symbols.     |
| info frame                                                   | Displays stack frame information at the selected position.   |
| info functions                                               | Displays the name and data types for all functions.          |
| <s>info handle</s>                                           | <s>Displays information about the handling of signals or processor exceptions.</s> |
| info locals                                                  | Displays all local variables for the current stack frame.    |
| info members                                                 | Displays the name and data types for all class member variables that are accessible in the function corresponding to the selected stack frame. |
| <s>info os</s>                                               | <s>Displays the current state of the Operating System (OS) support.</s> |
| info registers                                               | Displays the name and content of all application level registers for the current stack frame. |
| <s>info sharedlibrary</s>                                    | <s>Displays the names of the loaded shared libraries, the base address, and whether the debug symbols of the shared libraries are loaded or not.</s> |
| <s>info signals</s>                                          | <s>Displays information about the handling of signals or processor exceptions.</s> |
| info sources                                                 | Displays the names of the source files used in the current image being debugged. |
| info stack                                                   | Displays a numbered list of the calling stack frames including the function names and source line numbers. |
| info symbol                                                  | Displays the symbol name at a specific address.              |
| info target                                                  | Displays information about the loaded image and symbols.     |
| <s>info threads</s>                                          | <s>Displays information about the available threads.</s>     |
| info variables                                               | Displays the name and data types for all global and static variables. |
| <s>info watchpoints</s>                                      | <s>Displays information about the status of all breakpoints and watchpoints.</s> |
| <s>info watchpoints capabilities</s>                         | <s>Displays a list of parameters that you can use with watchpoint commands for the current connection.</s> |
| inspect                                                      | Displays the output of an expression and also records the result in a new debugger variable. |
| **interrupt, stop**                                          | Interrupts the target and stops the application if it is running. |
| **list**                                                     | Displays lines of source code surrounding the current or specified location. |
| **load**                                                     | Loads an image on to the target and records the entry point address for future use by the `run` and `start` commands. |
| <s>newvar</s>                                                | <s>Declares and initializes a new debugger convenience variable or register alias.</s> |
| **next**                                                     | Steps through an application at the source level stopping at the first instruction of each source line but stepping over all function calls. |
| nexti                                                        | Steps through an application at the instruction level but stepping over all function calls. |
| **nexts**                                                    | Steps through an application at the source level stopping at the first instruction of each source statement but stepping over all function calls. |
| <s>nosharedlibrary</s>                                       | <s>Discards all loaded shared library symbols.</s>           |
| **print**                                                    | Displays the output of an expression and also records the result in a new debugger variable. |
| **ptype**                                                    |                                                              |
| <s>pwd</s>                                                   | <s>Displays the current working directory.</s>               |
| **quit**                                                     | Quits the debugger session.                                  |
| restore                                                      | Reads data from a file and writes it to memory.              |
| run                                                          | Starts running the target.                                   |
| <s>rwatch</s>                                                | <s>Sets a watchpoint for a data symbol.</s>                  |
| select-frame                                                 | Moves the current frame pointer in the call stack.           |
| <s>set backtrace</s>                                         | <s>Controls the default behavior when using the `info stack` command.</s> |
| <s>set breakpoint</s>                                        | <s>Controls the automatic behavior of breakpoints and watchpoints.</s> |
| <s>set-directories</s>                                       | <s>Defines additional directories to search for source files.</s> |
| <s>set endian</s>                                            | <s>Specifies the byte order for use by the debugger.</s>     |
| <s>set listsize</s>                                          | <s>Modifies the default number of source lines that the `list` command displays.</s> |
| <s>set os</s>                                                | <s>Controls operating system settings in the debugger.</s>   |
| <s>set print</s>                                             | <s>Controls the current debugger print settings.</s>         |
| <s>set step-mode</s>                                         | <s>Controls the default behavior of the `step` and `steps` commands.</s> |
| <s>set substitute-path</s>                                   | <s>Modifies the search paths used by the debugger when it executes any of the commands that look up and display source code.</s> |
| <s>set sysroot</s>                                           | <s>Specifies the system root directory to search for shared library symbols.</s> |
| **set variable, set**                                        | Evaluates an expression and assigns the result to a variable, register, or memory address. |
| <s>sharedlibrary</s>                                         | <s>Loads symbols from shared libraries.</s>                  |
| <s>shell</s>                                                 | <s>Runs a shell command in the debug session.</s>            |
| <s>show</s>                                                  | <s>Displays the debugger settings.</s>                       |
| <s>show architecture</s>                                     | <s>Displays the architecture of the target.</s>              |
| <s>show backtrace</s>                                        | <s>Displays the behavior settings for use with the `info stack` command.</s> |
| <s>show breakpoint</s>                                       | <s>Displays the breakpoint and watchpoint behavior settings.</s> |
| <s>show directories</s>                                      | <s>Displays the list of directories to search for source files.</s> |
| <s>show endian</s>                                           | <s>Displays the byte order setting in use by the debugger.</s> |
| <s>show listsize</s>                                         | <s>Displays the number of source lines that the `list` command displays.</s> |
| <s>show print</s>                                            | <s>Displays the debugger print settings.</s>                 |
| <s>show step-mode</s>                                        | <s>Displays the step setting for functions without debug information.</s> |
| <s>show substitute-path</s>                                  | <s>Displays the search path substitution rules in use by the debugger when searching for source files.</s> |
| <s>show sysroot</s>                                          | <s>Displays the system root directory in use by the debugger when searching for shared library symbols.</s> |
| <s>show version</s>                                          | <s>Displays the version number of the debugger.</s>          |
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
| <s>thbreak</s>                                               | <s>Sets a hardware execution breakpoint at a specific location and deletes the breakpoint when it is hit.</s> |
| <s>thread</s>                                                | <s>Displays information about the current thread.</s>        |
| <s>thread apply</s>                                          | <s>Switches control to a specific thread to execute a debugger command and then switches back to the original state.</s> |
| unset                                                        | Modifies the current debugger settings.                      |
| **up**                                                       | Moves and displays the current frame pointer up the call stack towards the top frame. |
| <s>up-silently</s>                                           | <s>Moves the current frame pointer up the call stack towards the top frame.</s> |
| **watch**                                                    | Sets a watchpoint for a data symbol.                         |
| <s>watch-set-property</s>                                    | <s>Updates the properties of an existing watchpoint.</s>     |
| **whatis**                                                   | Displays the data type of an expression.                     |
| where                                                        | Displays a numbered list of the calling stack frames including the function names and source line numbers. |
| <s>while</s>                                                 | <s>Allows you to write scripts with conditional loops that execute debugger commands.</s> |
| x                                                            | Displays the content of memory at a specific address.        |



## Deployment tests

What tests to run before a new release is published?

- [ ] Before producing binaries, running tests on Mac:
     - [ ] dw-link + ATtiny85:
          - [ ] Erase
          - [ ] Upload Blink with avrdude
          - [ ] Run e2e tests
     - [ ] SNAP + ATtiny2313:
          - [ ] Erase
          - [ ] Upload blink
          - [ ] e2e
     - [ ] SNAP + Mega16:
          - [ ] e2e
     - [ ] Atmel-ICE + UNO: e2e
          - [ ] Erase
          - [ ] Upload Blink
          - [ ] e2e
     - [ ] Atmel-ICE + ATmega1284
          - [ ] e2e
     - [ ] UNO Wifi Rev2
          - [ ] e2e
     - [ ] CNano 417
          - [ ] e2e
     - [ ] Curiosity AVR128DB48
          - [ ] e2e
- [ ] Before producing binaries, test on platforms (pulling from GitHub and installing avr-gdb)
     - [ ] Mac/Windows under Parallels
          - [ ] dw-link + ATtiny861
               - [ ] Erase
               - [ ] Upload Blink
               - [ ] run e2e?
          - [ ] Curiosity ATmega4809
               - [ ] e2e?
     - [ ] Raspi/Trixie
          - [ ] dw-link + ATtiny861
               - [ ] Erase
               - [ ] Upload Blink
               - [ ] e2e
          - [ ] Curiosity AVR128DB48
     - [ ] Prodesk/Linux
          - [ ] dw-link + ATtiny861
               - [ ] Erase
               - [ ] Upload Blink
               - [ ] e2e
          - [ ] XNano416
               - [ ] e2e
- [ ] After generating new release candidate and generating pre-screen downloads
     - [ ] Mac
          - [ ] Arduino IDE 2 + PlatformIO
               - [ ] dw-link + ATtiny1634
                    - [ ] Upload Blink
                    - [ ] Debug vblink
               - [ ] XMini328
                    - [ ] Upload Blink
                    - [ ] Debug vblink
               - [ ] Atmel-ICE + ATmega2560
                    - [ ] Debug vblink
               - [ ] UNO Wifi Rev2
                    - [ ] Debug vblink
               - [ ] Curiosity AVR128DB48
                    - [ ] Debug vblink
     - [ ] Prodesk/Windows
          - [ ] Arduino IDE 2 + PlatformIO
               - [ ] dw-link + ATtiny1634
               - [ ] Curiosity AVR128DB48
     - [ ] Prodesk/Linux
          - [ ] Arduino IDE 2 + PlatformIO
               - [ ] dw-link + ATtiny1634
               - [ ] Curiosity AVR128DB48
