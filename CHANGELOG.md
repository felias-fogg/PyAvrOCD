# Changelog

### 0.21.0

- **Fixed:**
     - After the change to the timer mode (0.20.0), it became necessary to change the monitor command so that no reset is issued when one only queries the state. In addition, one will now also get a message that the MCU has been reset when timer mode is changed.
     - The LiveTests had a problem when single-stepping: The status register was queried before the MCU had stopped (although _wait_for_break had returned). This happened only for the JTAGICE3, PowerDebugger, and Atmel-ICE. Changing in _wait_for_break to polling (`use_events_for_run_stop_state = False`) mitigated the problem.
     - For the combination PICkit4 and ATmega32, it is necessary to 'deactivate' and 'activate the physical' when switching between debug and program mode.  So, this is now done in general.
     - It was also necessary to introduce some decoupling time between running the test scripts when using PICkit4: 2.5 secs
     - In dw-link in the connection_lost method, the os._exit(0) call will now always be made, terminating the entire process when the serial connection is lost.
     - In server.py, in the `__del__` method, the `time.sleep(0.5)` will only be done on non-Windows machines because Windows chokes on this call.
     - An annoying error message about `Nonetype` not having the attribute `mon` when shutting down has been eliminated in the same `__del__` method.
- **Added:**
     - A new field in the `monitor info`  describing the connected debugger.
     - The manual now contains a link to a udev rules file that can be downloaded and installed.
- **Changed:**
     - `stop_debugging` runs gracefully (not spitting out error messages) when debugging is stopped.
     - The critical error message about udev rules is now only given when a debugger is connected via USB.
     - Instead of referring to an installation command, the Linux user is asked to download a rule file that needs to be installed manually.
     - Refactored `startup` to simplify the logic and to make testing easier.
- **Removed**:
     - The option `--install-udev-rules` has been removed. I trust that Linux users are able to download and install a udev rules file manually, and they probably feel much more confident when doing it this way.




### 0.20.0 (27-Dec-2025):

- **Changed**:
     - We now allow Python 3.14 since the hidapi package has apparently been built under Windows.
     - CI workflows use Python 3.14
     - In CI workflow `release.yml`, we run pyavrocd with `-V` and `-d ? -t ?`
     - The initial single step in range stepping has been eliminated because GDB oversteps breakpoints using a single-step command anyway.
     - In the manual, the quickstart guides for each IDE have been joined.
     - The protocol for switching between debug mode and programming has been simplified. Simply attach/detach for debugging mode and enter_progmode/leave_progmode for programming mode. I have no idea why I did not try this in the first place.

- **Fixed**:

  - After loading and after changing the timer mode, a new AVR8 method called `reactivate` is called. This method deactivates and reactivates the physical in order to set the timer mode (I have no idea why this is necessary, but it works).
  - In order to set the initial value for timer mode according to the command-line argument, a further parameter for XAvrDebugger is defined (`timers_run`), which is used when calling the `setup_debug_session` method in `xavr8target.py`.
  - CTRL-C is now brought into synchronization with the packet flow in order to allow interruption of heavy single-stepping. Works perfectly.
  - When accessing the DWDR in simulating a two-word instruction, an INVALID ADDRESS error was raised. This is nothing that is likely to happen ever, but it is now caught, an error is logged, and debugging can continue.

- **Added**:

     - New method `reactivate`  in `xavr8target` (for each target).

     - New integration sketches: `range_dw.ino`, `range_jtag.ino`, `sleepwalk.ino`, `break.c`
     - New header file in integration directory: `irqpin.h`
     -


### 0.19.0 (17-Dec-2025)

- **Changed**:
     - PyAvrOCD from this version on requires that dw-link attach the version number to its initial response string 'dw-link' with a version >= 6.0.0. This is required so that one can be sure that the 'manage' requests from PyAcrOCD (e.g., `nodwen`) are indeed honored by dw-link.

- **Added**:
  - The `dwlink` module sends all provided monitor value arguments as qRcmd packets to dw-link.

  - The `dwlink` module sends all non-managed fuses to dw-link.

  - New (hidden) command line option: `--dw-link-baud`. It can be used to specify a different baud value for communication with dw-link.

- **Removed**:
     - `device` files with a debugging interface other than debugWIRE and JTAG only.
     - The `monitor speed` command (for dw-link use only) has been removed. One can still recompile dw-link with a higher communication speed limit.
     - The Arduino AVR Boards core fork has been removed from the list of 'debug-enabled' cores in order to avoid confusion for people who use both, and also to avoid unclear support relationships. Functionality is not affected because there are always other cores that can take the role, e.g., MiniCore, MegaCore, and ATTinyCore. The only uncovered MCU is the 32U4, for which a separate core will be created.
     - The methods `_eesave_set_and_save` and `_eesave_restore` have been removed from the class `XAvrDebugger`. Their use in order to protect EEPROM content when doing a chip erase in order to clear the lockbits was unfortunately useless. When lockbits are set, you cannot change fuses!
     - The 's', 'S', 'c', and 'C' packets have been removed from GdbHandler because the 'vCont' packets fill this place.



### 0.18.1 (02-Dec-2025)

- **Fixed:**
     - Unfortunately, Windows command lines cannot be parsed with the Python module `shlex`, which led to the problem that `simavr` could not be started under Windows. Now, the `-s` option expects the path to a program (without any arguments). If extra arguments to `simavr` are necessary, one has to use the new `-x` option.
     - On Linux, the simavr executables use dynamic libraries. They have now been added. This also means that the path to access the executable had to be adapted.
     - Not `simavr.protocol` but `simavr.upload.protocol` needs to be set to a strange name to signal the user that `Simulator (simavr)` is not a regular programmer.

### 0.18.0 (30-Nov-2025)

- **Added:**
     - `simavr` has been added to the binary tools. With that, one can now start the simulator by using the "virtual programmer" simavr when starting the debugging process. This looks strange but it appeared to be the only straightforward way of starting simavr without using `pyavrcod.options`. Using `pyavrocd.options` still works and can be used to start simavr with extra arguments.

### 0.17.1 (24-Nov-2025)

- **Added:**
     - More unit tests
     - 32-bit Windows version (meaning, we do not have to explain that one
          has to re-install when working on a 64-bit Windows system, sigh!)

### 0.17.0 (20-Nov-2025)

- **Added:**
     - Support for `simavr` (needs to be built from source or downloaded from PIO repo) and an explanation of how to use it in the documentation: Simply use the `-s` option with `simavr` as the program name. In this case, no connection to a hardware debug probe is made, and simavr is invoked. After termination of simavr, PyAvrOCD is also immediately terminated.
     - New option `-F` for the F_CPU value. Needed for simavr and as a default value for `-D`.
     - New unit tests: Borrow HWBP0 and -F option
     - Meaningful error message in `_activate_interface` when debugWIRE could not be entered despite seemingly successful power-cycling.
- **Changed:**
     - Increased sleep time after powering up from 0.1 to  0.2 seconds.
     - Changed name for no program in `-s` option from `noop` to `nop`.

### 0.16.5 (05-Nov-2025)

- **Fixed:**
     - The SVD files contained FUSEs and LOCKBITs, but not SP and SREG. For some reason, a wrong version of atdf2svd was invoked, and the option value was misspelled. Perhaps there should be a unit test here as well.
     - It could happen that when lazy loading (with X-records), another record is received before the timeout in the server loop calls for finalizing the load operation. Now, we catch that by checking whether a non-X record is received while lazy loading.
- **Added:**
     - The command `monitor load onlycache` will disable flashing when loading. It is useful when one can use ordinary programming for debugWIRE targets, e.g., when using the Xplained-Mini boards. This will disable flashing in the `flash_pages` method. The switch is disabled after the initial load and changed to read-before-write.
     - Three debug-enabled cores:
          - ArduinoCore-avr-debug-enabled: the usual classic Arduino boards,
          - ATTinyCore-debug-enabled (2.0.0-dev): all classic ATtinys with the brand-new core
          - avr-xminis-debug-enabled: Looks like a debug-enabled core of the ATmel Xplained core, but it is really MiniCore stripped down, making working with it very easy.
     - A remark in the installation guide on how to make binaries on macOS executable when they have been downloaded with a browser.

- **Changed**:
     - Handling of the 'timeout' record (`_set_binary_memory_finalize`) is now moved inside the try/except construct in order to be able to catch exceptions. In other words, it is now a 'normal' command.
     - Added `switch_to_debmode` and `switch_to_progmode` to xavrdebug.py so that we are not forced to call `self.dbg.device.avr.switch_to...`.


### 0.16.4 (02-Nov-2025)

- **Fixed:**
     - On an ATmega328P XPlained Mini, I sometimes got errors when activating the physical interface: "AVR8_FAILURE_CLOCK_ERROR: Failure when increasing communication clock rate". If this error occurs, we now simply retry. This appears to work smoothly.
     - Captured "Cannot open HID" exception when trying to connect to a busy debug probe in main.py
- **Added:**
     - Added 'borrow_hwbp0' in hardwarebp.py: Borrow the temporary HWBP. If HWBP0 is not used, used only by range-stepping, or one can move the HWBP to another slot, we simply return  None (and the HWBP0 can be used implicitly using run_to). Otherwise, we return the address of the blocking BP, which then has to be changed into a SWBP in order to free HWBP0.
     - 'Sleep walking' in breakandexec.py: Instead of skipping a SLEEP instruction when single-stepping, we now place a hardware breakpoint after the SLEEP instruction, which is 'borrowed' (see above).
     - Added the possibility in the integration tests to compile pure C/C++ programs that do not depend on the Arduino framework.
     - Added tags for scripts and MCUs. All MCU tags must be mentioned in the list of script tags for the test to be included.
     - Added a keyword $SUCCESS_IF for test scripts in order to terminate a test prematurely (when something is not implemented) based on the output of the previous command.
     - New integration test: cblink (a C program implementing a blinky).
     - New integration test: measure (a C++ program to measure supply voltage).
     - Added timers script (used to be part of monitor script)

- **Changed:**
     - In the `platform.txt`  files, I changed from setting a temporary breakpoint in `setup` to breaking just after starting `main`. The main reason is that setup is not always defined, sometimes it is ambiguous, and when one tries to disambiguating by mentioning the source file, then it is again wrong when optimization for debug is disabled. Finally, when debugging on USB-MCUs, the enumeration times out. So, in summary, it seems more robust to stop in main, although the user may not have seen that before.
     - Refactored the integration tests. Now we have two modules and the test driver.  Everything is now in the `integration` folder below `tests`.
     - Changed monitor script so that it can now be used for non-Arduino targets as well.
     - Changed 'hardware debugger' to 'debug probe' in the documentation, which seems to be the more common term.

- **Removed:**
     - Removed paragraph about "Single-stepping SLEEP instructions" in the limitations doc.



### 0.16.3 (15-Oct-2025)

- **Fixed:**
   - SVD and device files freshly generated, now with read-only registers
   - During startup, we handle now situations with more than one connected tool and requiring the connection to a third one. It used to fail silently after trying to connect to dw-link. Now, a critical error message is printed without trying to connect to dw-link.
- **Changed:**
   - The `svd` folder is now located in pyavrocd-util.

### 0.16.2 (13-Oct-2025)

- **Fixed:**
  - In livetests.py:
       - Some internal data structures were referenced, which had changed (hardware breakpoint structures). Now tests work again.
  - In integration_tests.py:
       - Because JTAG MCUs have four instead of one hardware breakpoints, the breakpoint integration test did not work. Now we have an extra test for JTAG MCUs.
       - Because we use the original Arduino platform for compiling the ATmega32U4 sketch, we needed to lower the amount of flash used by PROGMEM.
       - On the ATmega32U4, the location specification 'setup' (for setting the initial temporary breakpoint) is ambiguous. For this reason, we have to specify 'blink.ino:setup'. This should be done in general in the all board.txt file for the Arduino!
       - Along the same line, in the oop_script, `list setup` led to a long output and waited for interaction. Here oop.ino:setup helped as well.
       - In the isr_script, for the ATmega32U4, we stop one step earlier already in the interrupt dispatch table. However, fortunately, the string `__vectors` appears also after the additional `next` command. So, I only had to delete the word `in`  in order to make it a test for JTAG and debugWIRE targets alike.
  - In xnvmmegajtag.py
        - In `read` and `write`, the wrong EEPROM memory mode was selected when in debugging mode.

- **Added:**
  - For ATmega128(a), the breakpoint mode is now hardware-only and cannot be changed.

- **Changed**:
  - The release assets now contain the PyAvrOCD version number.

### 0.16.1 (07-Oct-2025)

- **Fixed:**
  - The folders pyavrocd-util were empty and therefore not included in commits. For this reason, the packer script ignored them and the dummy 32-bit archives were not produced. Now these folders contain a copy of the read.me file and are uploaded as well.

### 0.16.0 (07-Oct-2025)

- **Changed:**
  - It turned out that the binary files are too big for the gh-pages. At least, they disappeared after a while. For this reason, the binary executables are now all distributed using GitHub's release mechanism, which permits arbitrarily large files. This means that the archives in the releases have to respect the structure of being in the `tools` directory. And it also implies that the 'stub' archives for the 32-bit architectures should be included. The workflow has been adapted.

### 0.15.0 (06-Oct-2025)

- This is the first 'official' pre-release with a somewhat working CI/CD workflow.

### 0.14.3 (04-Oct-2025)

- **Added:**
  - New tests:
    - test_xnvmmegaavrjtag.py
    - new tests in test_xavrdebugger.py
- **Removed**:
  - `start`/`stop` have been removed from the xmvm* modules because this is handled by xavrdebugger in `start_debugging` and `stop_debugging,` and was not used anyway.

### 0.14.2 (02-Oct-2025)

- **Added:**
  - New tests:
    - test_dwlink.py
    - test_main.py
  - CI on GitHub: PyLint and PyTest with automatic deployment of CI badges.
- **Changed:**
  - All console output of dwlink now goes to `stdout`. Before, there was a mix of `stdout` and `stderr`. With that, all console output of pyavrocd is now going to `stdout`.
  - Moved a few files and the `atdf` folder into extras and integrated `pytest.ini` and `.pylintrc` into `pyproject.toml`.

### 0.14.1 (30-Sep-2025)

- **Added:**
  - Tests for HardwareBP
  - Additional tests for BreakAndExec, because of the new single-stepping method:
    - test\_breakandexec\_classify.py
    - test\_breakandexec\_filter.py

- **Changed:**
  - Signal changed for not enough breakpoints: SIGABRT -> SIGSYS. This means SIGABRT is now only used for Fatal Error.
  - Signal changed for "executable not loaded": SIGILL -> SIGSEGV. This means that SIGILL is now used exclusively for instructions, from which we cannot continue.

### 0.14.0 (28-Sep-2025)

- **Fixed:**
  - Using the temporary HWBP for safe single-stepping had the problem that one might miss a BP in an interrupt routine. Accounting for that by reassigning the HWBP to a SWBP had the implication that one increases flash wear and makes safe single-stepping impossible when running with HWBP-only under dW. For this reason, filter_safe_instructions has been introduced (see below), and single-stepping using the HWBP has been removed (see below).
- **Added:**
  - `ronly_registers` have been added in the device files.
  - `sram_masked_write` writes only to unmasked bates (i.e., those that are not read-only).
  - New class HardwareBP that allows us to manage hardware breakpoints in a similar way as software breakpoints, i.e., by using the break address only.
  - New method filter_unsafe_instructions: Identifies instructions that modify or read SREG and simulates them. This does not include PUSH/POP and CALL/RET/RETI
  - Check for trouble in single-stepping: If the stack pointer is below SRAM_START, and a stack operation is attempted, then stop execution with a SIGBUS signal, which will be caught on the GdbHandler level.
  - If SRAM > 64k or architecture != avr8, a fatal error is raised in filter_unsafe_instructions.This is mainly a reminder to myself.
  - Entries in the readthedocs documentation: Limitations, Contributing, Code of Conduct.
- **Changed:**
  - `update_breakpoints` has been changed significantly (and is much smaller now). Now, only the most recently introduced breakpoint that has no SW/HW BP allocated yet will allocate the temporary HWBP 0. This is forced by unallocating HWBP 0 (the respective BP will later allocate an SWBP)
  - All internal methods in BreakAndExec have been prefixed with an underscore.
  - `RspServer` got its own module `server`
  - `HardwareBP` got its own module `hardwarebp`
- **Removed:**
  - Safe stepping using the temporary HWBP.


### 0.13.5 (15-Sep-2025)

- **Added:**
  - Installed mkdocs in order to provide a nice UI for the documentation.
  - `eesave` and `noeesave` are now values for the `--manage` option. If the EESAVE fuse is managed, EEPROM will be preserved when chip erase operations are necessary.
  - Setting EESAVE temporarily has been added to `_check_atmega48_and_88`  in xavrdebugger.py.
  - Made note in the documentation that some install methods are not yet implemented.
- **Changed:**
  - The official name and the GitHub repo name have changed to PyAvrOCD. This does not make it easier to pronounce, but it shows better what it is about.


### 0.13.4 (12-Sep-2025)

- **Added:**
  - A somewhat convoluted procedure for recognizing the bad apples among the ATmega48/88 has been added to xavrdebug.py. ATmega48 and 88 with stuck-at-1 bits in their program counter (and other issues) are now identified before the DWEN fuse is programmed. This means that they will not be bricked!
- **Removed:**
  - The option `--allow-potentially-bricking-actions` has been removed because it is not needed any longer.

### 0.13.3 (11-Sep-2025)

- **Fixed:**
  - livetests.py: Also cater now for the case that sram_start can be 0x200. Until then, only the cases 0x60 and 0x100 were considered, which broke the step test.
  - isr.ino: In this test sketch, a lot of interrupts are raised that may stop the printing process, a problem that came up before. I increased the waiting time and increased the communication speed so that the test could be passed. I had this before!
  - breakandexec.py: sim_two_words needed to be adapted so that it can be used for interrupt-safe single-stepping. The isr.ino test works now, but the implementation should be tested in the upper part of memory (maybe a special LiveTest?).
  - main.py: Now, a CTRL-C will stop the server so that we terminate with an error code.
  - xavrdebug.py: A special test for ATmega16 has been introduced for testing whether it is a non-A version, which has a stuck-at-1-bit. Interestingly, this only shows when looking at return addresses on the stack, but not when reading the PC through the debugger.
- **Added:**
  - A `sim2word_jmphigh.ino` test sketch that checks whether single-stepping (by simulation) over two-word instructions works even in the high part of flash memory
  - A `fuses.ino` test sketch has been added to the integration tests, testing fuses, lockbits, and signature loading.
  - Added test "(the pagetoflash is not blank or memory has not been erased before loading)" before programming a flash page and before verifying it. This speeds up the  `sim2word_jmphigh.ino`  test sketch.


### 0.13.2 (07-Sep-2025)

- **Fixed:**
  - nvmmegajtag.py: EEPROM is saved when JTAG 'chip erase' is performed. This is done by temporarily programming the `EESAVE` fuse. Without it, one could not load the EEPROM in an ELF file when `EESAVE` was not programmed.
  - memory.py: For fuses and lock bits, an error log message is printed when trying to access these memory areas. However, we fail silently, i.e., loading will nevertheless be successful. This kind of handling of these areas will avoid problems during debugging (by fuse or lock bits), but it will nonetheless allow debugging programs that contain such data.
- **Added:**
  - When adding #include <signature.h> to your file, the signature of the MCU you provided at compilation time is added to the ELF file. The GDB server compares this to the device specified when starting the server, and loading will fail if there is a mismatch.
  - harvest.py: `eesave_base` and `_mask` is harvested.
  - `eeprom.ino` sketch has been added to the test suite.
  - The `ledsignal.h` header has been added to the test suite that provides blinking/error signaling in a uniform way. This needs to be added by a soft link to every sketch that wants to use it.


### 0.13.1 (04-Sep-2025)

- **Fixed:**
  - memory.py: In `flash_pages`, flash page reading before writing is only done when requested and we do not have erase-before-load!
  - memory.py: In `flash_pages`, the test on a blank page before flash page erase is only done when the page has actually been read.
  - memory.py: `eeprom_read` and `eeprom_write` moved from avrdebugger to memory.py because only at this place do we know whether we are in programming or debugging mode. And this is important to pass that on to the read/write routines in the nvm modules so that they can pick the right memory type.
  - xnvmmegaavrjtag.py: `erase_page` did not have the progmode parameter and did not switch between progmode and debmode.
  - xnvmmegaavrjtag.py: Added missing `erase_chip` method.
  - handler.py: `self.bp.cleanup_breakpoints` has been moved from `_vflash_done_handler` to `_vflash_erase_handler`.
  - handler.py: In `_vflash_erase_handler` the chip `erase` has been added (provided `is_erase_before_load` is True)
  - test_memory.py: Added `self.mem.mon.is_read_before_write.return_value = True` and `self.mem.mon.is_erase_before_load.return_value = False` to `test_flash_pages...`.
  - test_gdbhandler.py: Imported `options` function from `main.py` and used that to pass the `args` argument to GdbHandler.
  - test_xavrdebugger.py: Added the two new clock parameters to the class creation call.
  - test_monitorcommand.py: Imported `options` as above; wrong test with empty second string in `dispatch`.
  - livetests.py: In `_live_test_load` a "virtual timeout" via `self.handler.dispatch(None, None)`  had to be added so that the simulated load will be terminated with flashing the last pending record (see `lazy_loading` added in 0.9.6).
  - livetests.py: Four tests cannot be run on JTAG megaAVRs because reading from flash in debugging mode filters out the breakpoints.

- **Added:**
  - Now you can use one-character abbreviations of the option values for the monitor options on the command line, e.g., `--timers f` instead of `--timers freeze`. Since you can abbreviate command-line options anyway, `--ti f` also works.
- **Changed:**
  - The response from `monitor reset` when the debugger is not active has been changed to "Debugger is not enabled".


### 0.13.0 (26-Aug-2025)

- **Fixed:**
  - The Arduino IDE 2 was killing the server using SIGTERM without giving it a chance to clean up. Unfortunately, catching the signal did not help because the tool was apparently already disconnected somehow. We now capture both the SIGTERM signal and a disconnect from GDB, setting `self._terminate` to `True`, which ends the loop in the `server` method of `RspServer` and provides us a chance to terminate the GDB server cleanly.
  - Address translation in memory.py assumed that all addresses have only 16 bits and that all digits before the 16-bit address are a memory segment identifier. That does not work with flash memory larger than 64k, though. So, this has been adapted. All addresses not starting with an '8' are taken literally. The '8' addresses are SRAM, EEPROM, etc.
- **Added:**
  - New option `-P`/`--prog-clock` for setting the JTAG programming clock frequency in kHz.
  - New option `-D`/`--debug-clock` for setting the JTAG debugging clock frequency in kHz (should be at most a quarter of the MCU clock frequency).
  - These two options are now set in the MightyCore/MegaCore board files according to the MCU speed.
  - Two new monitor options: `monitor atexit leavedebugwire` and `monitor atexit stayindebugwire`, where the second is the default. The first one is useful when one has an embedded debugger.
  - Two new monitor options: `monitor erasebeforeload enable` and `disable`. The first one is the default; however, it does not affect debugWIRE targets, because we can only erase page by page. Disabling it might be helpful for MightyCore and MegaCore in order to protect the bootloader, which offers some functionality.
  - All monitor commands that change state can now be used as command-line options. For example, one can specify `--timers=freeze` on the command line.
  - We now also accept the `-f` option and ignore everything about it. This option is not shown in the 'usage' text (because it is suppressed).
  - In order to safeguard the user against debugging non-A ATmega48/88, pyavrocd refuses to debug any such non-A/P device. If an A-device (e.g., ATmega88A) is specified, a warning message is given that it is necessary to specify `--allow-potentially-bricking-actions` on the command line or in the `pyavrocd.options` file.  The option itself is not displayed in the help text since it would clutter the help text too much.
- **Changed:**
  - `monitor onlyloaded` was changed to `monitor onlywhenloaded`
  - Since we now also deal with the `-f` option needed for the openOCD invocation by cortex-debug, we no longer tolerate unknown options.
  - Because printing the possible choices for option values looked very ugly, the help text now states that the choices can be asked for by using a '?'.  The help text looks very tidy now.
- **Removed:**
     - The `-g/--gede` option has been removed because `-s` also gives its functionality.
     - The `-M/--monitor` option has been removed because now all state-changing monitor commands can be used as command-line options.


### 0.12.0 (26-Aug-2025)

- **Added:**
  - `-M`/`--monitor` command line option can now be used to set monitor default option in the command line, e.g., `-M v:e` will enable verification after load.
  - With a @-prefix to a file name, one can now request to read further command-line options from a file. If the file does not exist, the @-argument is simply ignored. This can, for example, be used to override options set by the IDE when a fixed name, such as `debug.opt`, is used.
  - A new method in `handler` for telling the user that power-down has been sensed, and a new parameter in power cycle methods to pass this message method down to where it will be called.

### 0.11.1 (21-Aug-2025)

- **Fixed:**
  - ATmega88 and ATmega48 (without P or A suffix) act very strangely (and we are not talking about non-genuine chips here!):
    - The DWEN fuse of ATmega48 cannot be programmed through the SPI module of pyedbglib.
    - If one does that with avrdude, the chip cannot be accessed anymore from avrdude, although programming the fuse alone should not pose a problem.
    - One cannot recover with the debugWIRE recovery method of avrdude, which usually simply disables debugWIRE.
    - If the fuse can be changed, as in the case of ATmega88, one cannot unprogram the fuse after having noticed that the chip has a stuck-at-1-bit in the program counter. Again, even avrdude fails.
    - The only recovery methods for both chips are through dw-link or high-voltage programming.
    - For these reasons, debugging these chips is refused by pyavrocd (except when the dw-link debugger is used).
    - Note: This will require a change in MiniCore (distinguish between the A and the non-A chips)

  - The existing tests had to be adapted to the refactored code.
    - test_breakandexec: everything OK
    - test_debugwire: needs to be redesigned and integrated into test_xavrdebugger
    - test_gdbhandler: test_send_power_cycle_*** moved to test_xavrdebugger, added programming_mode as attribute to mock object self.gh.mem.
    - test_memory: test_memory_map - adapted, test_readmem_sram_masked_register -- value for programming_mode needs to be False !
    - test_monitorcommand: _timersfreeze is now False, _verify is now False, _fastload has been renamed to _read_before_write, remains True for debugWIRE
    - test_xavr8target: osccal register; fixed in source - not sram address, but 'ioreg' address
    - test_xavrdebug:
      - had to remove `setup_config` from `__init__` in xnvmdebugwire. This is now done in `start_debugging` in xavrdebug!
      - New tests for: start_debugging, stop_debugging, _post_process_afetr_start,


### 0.11.0 (21-Aug-2025)

- **Fixed:**
  - The root cause of the annoying problem noted in version 0.10.0 has now been found, and a kludge to solve the issue has been implemented. SNAP and PICkit4 simply do not implement the protocol as described in the EDBG manual. For this reason, `switch_to_progmode` and `switch_to_debmode` have been implemented for the device-specific parts of `avr8target`, which uses a restart of the debugging session: `detach`/`deactivate_physical`/`activate_physical`/`enter_progmode` when switching to programming mode. This is followed by `leave_progmode`, if one wants to enter debugging mode. In the debugWIRE specific part, these are simply no-ops.
  - debugWIRE loading did not work any longer because the `prog_mode` argument in the read nvm method was not present. Now it has been added.

- **Added:**

  - `erase_page` and `erase_chip` in the nvm classes. If they cannot be effective, they return False.
  - Extensive warning messages concerning fuse management.

- **Changed**:

  - Flash programming has been adapted to the new regime

  - New monitor default value: *Verify after load* is now off, because it significantly slows down JTAG loading.

  - New monitor default value:  *read-before-write* is now the default only for debugWIRE. For JTAG, it is a real slowdown.

  - New monitor default value: Timers now run freely when execution is stopped because that is the more natural thing for an embedded system.


### 0.10.1 (17-Aug-2025)

- **Fixed:**
  - Since megaAVRs make a difference between FLASH_PAGE (during programming) and SPM (during debugging), I added an optional parameter to the read routines in avrdebugger and nvmmegajtag `prog_mode`. While flashing the program, it is true; otherwise, it is false. Seems to do the trick.

### 0.10.0 (15-Aug-2025)

- **Fixed:**
  - One can now enter debugging even when OCDEN was not set. This is now done when connecting.
- **Added:**
  - Option value `all` for `-v` if the full RSP communication should be displayed during debugging.
  - New option `-f`/`--fuse`, which can be used to specify which fuses shall be managed by the GDB server. So, if you want to have automated changes of DWEN, OCDEN, BOOTRST, and automatic clearance of the lockbits, you need to specify `-f all`.
- **Changed:**
  - Reorganized the initialization process completely. Now all of it takes place in `XAvrDebugger`. All classes have `init` methods that set up the data structure, but do not contain code to initialize anything in the debugging tool (or such code is not inherited). The `start_debugging` method in `XAvrDebugger` does all the heavy lifting (including calls to special code for debugWIRE and JTAG/Mega).

- **Note:**
  - Memory type for access to flash is not set to MEMTYPE_SPM as it should be
  - While the Atmel debugger all work, SNAP and PICkit4 choke. There is some problem with memory access, I believe.


### 0.9.7 (12-Aug-2025)

- **Added:**
  - The first part of integrating JTAG in xmvmegaavrjtag.py (basically the stuff I added for debugwire), xavr8target.py, jtagtarget.py (first steps and starting and stopping JTAG), and in xavrdebugger.py is working. I can now enter debugging mode on an Xplained324pb board!
  - Added code to revert to debugging mode while flashing a program, enabling the erasure of a single page when using the read-before-write strategy. It turns out that this strategy is now no longer dominant, so defaults should probably be dependent on the debugging interface.
  - New memory areas and methods to access them have been integrated.

### 0.9.6 (10-Aug-2025)

- **Added:**
  - The attribute `lazy_loading` is added to the class `Memory`. It will be set to `True` by the first X-record concerning flash memory, and it is used to leave excess memory unprogrammed in each step (in `flash_pages`). If, in the end, the server times out not receiving any new records, then it will send an empty packet to the handler, which will be taken as an indication that now flashing should be finalised, i.e., setting `lazy_loading` to `False` again, calling `flash_pages` a last time, and disabling prog mode. This provides a reasonable solution for loading executables in clients without XML support.

### 0.9.5 (10-Aug-2025)

- **Added:**
  - Some dynamic info messages when flashing large files

### 0.9.4 (09-Aug-2025)

- **Fixed:**
  - Binary load with X-records broke when a ':' appeared in the binary string. This showed only when the GDB version did not support XML (usually Windows GDB clients).
  - With the large receive buffer of 16k, the binary load did not work because of the GDB timeouts. For this reason, the buffer was scaled back to 1k. Loading when expat is present is as fast as before. But without it, it is less than optimal because a large number of pages have to be written twice. Maybe one should use the same strategy as in dw-link.
- **Added:**
  - `enter_/leave_prog_mode` in `flash_pages` in class `Memory`
  - constant `RECEIVE_BUFFER` in handler.py
  - some info messages concerning housekeeping/attaching/activating
  - try/exception in stop_debugging
  - local loggers in xavr8target and xnvmdebugwire
- **Changed**:
  - Logger names have been adapted to Python naming
  - Renamed `AvrGdbRspServer` to `RspServer`

### 0.9.3 (09-Aug-2025)

- **Added**:
  - `self.dbg.housekeeper.end_session` in disable in class DebugWIRE
    in the end. I am not sure whether this helps, but it is the right
    way to do! One now has only to protect the calls in
    `stop_debugging`
  - `self.spidevice.isp.enter_progmode()` before reading `device_id`
    in `enable`
  -  `self.dbg.housekeeper.start_session()` after
       read_target_voltage because this function explicitly ends a
       session
  - Methods in XAVR8Target for handling JTAG. They look very similar
      to the debugwire ones. Maybe refactoring later?
- **Changed:**
	- Changed pylint rules globally and removed a number of pylint exceptions from the sources
  - Split up the main function
- **Removed**:
	- Check whether there is a connection to the OCD in set/clear
    breakpoint. This test muddied the water since the real error
    message "not connected to OCD" by `continue` or `step` was not printed
  - Clear software_breakpoints in `__del__` of server removed because this is done in `stop_debugging` anyways.

### 0.9.2 (08-Aug-2025)

- **Fixed:**
  - Fixed all broken unit tests

- **Added:**
  - Ran tests on ATmega168PB and, unsurprisingly, the chip does not present any problem



### 0.9.1 (08-Aug-2025)

- **Fixed:**
  - Omissions and errors patched in ATDF files (read README in the atdf folder)

- **Added:**

  - Added option "-i", "--interface" for choosing the debug interface
  - Checking whether the device is compatible with the interface
  - New argument and state variable for XAvrDebugger class: iface
  - New attribute for `GdbHandler`: `_debugger_active`, which will be true if the debugger has been activated (and not deactivated yet).
  - New internal method in `GdbHandler`: `_debugger_is_active()`. Will issue error messages and return False if the debugger is not (yet) active.
  - New internal method in `GdbHandler`: `_send_execution_result_signal(signal)`. Will send a signal when `signal` variable is not none.
  - A reset call after dw on and off
  - Argument to `MonitorCommand`: `iface`
  - Check in `_mon_debugwire` for the right interface
  - Return interface on `monitor info` and give information on whether OCD connection has been established.
  - Added an analysis of the `ocd-rw` attribute usage to the ATDF folder: `OCD-access.md`
  - Added baseAddress patch to `gensvd.py` so that now all registers can be addressed by the GCC addressing scheme in the SVD file.
  - Added a patch to extend the description of a register in the SVD file when it is marked as `ocd-rw=""`.

- **Changed:**
  - Changed the names of the atdf folders to `mega-<version>` and `tiny-<version>` and included them in the repo. In addition added `tiny` and `mega` soft links (so that patches are independent of the concrete version)
  - Refactored pyavrocd.py: all classes now have their own module


### 0.9.0 (27-Jul-2025)

- **Added:**

  - dw-gdbserver version 2.3.2 code from other repo
  - Exception handling for initialising the debugger and the RSP server objects (graceful exit)

  - Device description `atmega328pb.py`
  - New modular documentation about JTAG and UPDI interfaces in addition to debugWIRE
  - Class diagram sketch

- **Changed:**
  - Replaced all occurrences of "dw-gdbserver" and "dwgdbserver" with "pyavrocd".
  - Some cosmetic changes in xnvmdebugwire.py, pyavrocd.py
- **Removed:**
  - Removed argument `user_interaction_callback` from `start` method in `XNvmAccessProviderCmsisDapDebugwire` (because pylint complained about it).
  - Removed arguments `no_hw_dbg_error` and `no_backend_error` to  `AvrGdbRspServer` (and further down in this class) because the server will have been stopped before if one of those turned out to be true. The crucial "libusb" and "udev" information is provided by critical server messages anyway.

### Initial commit (03-Jul-2025)
