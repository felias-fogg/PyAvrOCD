# Changelog

### New:

- **Fixed:** 
  - Using the temporary HWBP for safe single-stepping had the problem that one might miss a BP in an interrupt routine. Accounting for that by reassigning the HWBP to a SWBP had the implication that one increases flash wear and make safe single-stepping impossible when running with HWBP only under dW. For this reason, filter_safe_instructions has been introduced (see below) and single-stepping using the HWBP has been removed (see below).

- **Added:**
  - filter_unsafe_instructions: Identifies instructions that modify or read SREG and simulate them. This does not include PUSH/POP and CALL/RET/RETI
  - Check for trouble in single-stepping: If the stackpointer is below SRAM_START, and a stack operation is attempted, then stop execution with a SIGBUS signal, which will be caught on the GdbHandler level.
  - If SRAM > 64k or architecture != avr8, a fatal error is raised in filter_unsafe_instructions.This is mainly a reminder to myself.
- **Removed:**
  - Safe stepping using the temporary HWBP. 

### 0.13.5:

- **Added:**
  - Installed mkdocs in order to provide a nice UI for the documentation.
  - `eesave` and `noeesave` are now values for the `--manage` option. If the EESAVE fuse is managed, EEPROM will be preserved when chip erase operations are necessary.
  - Setting EESAVE temporarily has been added to `_check_atmega48_and_88`  in xavrdebugger.py.
- Changed:
  - The official name and the GitHub repo name have changed to PyAvrOCD. This does not make it easier to pronounce, but it shows better what it is about.


### 0.13.4

- **Added:**
  - A somewhat convoluted procedure for recognizing the bad apples among the ATmega48/88 has been added to xavrdebug.py. ATmega48 and 88 with stuck-at-1 bits in their program counter (and other issues) are now identified before the DWEN fuse is programmed. This means that they will not be bricked!
- **Removed:**
  - The option `--allow-potentially-bricking-actions` has been removed because it is not needed any longer.

### 0.13.3

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


### 0.13.2

- **Fixed:**
  - nvmmegajtag.py: EEPROM is saved when JTAG 'chip erase' is performed. This is done by temporarily programming the `EESAVE` fuse. Without it, one could not load the EEPROM in an ELF file when `EESAVE` was not programmed.
  - memory.py: For fuses and lock bits, an error log message is printed when trying to access these memory areas. However, we fail silently, i.e., loading will nevertheless be successful. This kind of handling of these areas will avoid problems during debugging (by fuse or lock bits), but it will nonetheless allow debugging programs that contain such data.
- **Added:**
  - When adding #include <signature.h> to your file, the signature of the MCU you provided at compilation time is added to the ELF file. The GDB server compares this to the device specified when starting the server, and loading will fail if there is a mismatch.
  - harvest.py: `eesave_base` and `_mask` is harvested.
  - `eeprom.ino` sketch has been added to the test suite.
  - The `ledsignal.h` header has been added to the test suite that provides blinking/error signaling in a uniform way. This needs to be added by a soft link to every sketch that wants to use it.


### 0.13.1

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


### 0.13.0

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
- **Removed:**
  - The `-g/--gede` option has been removed because `-s` also gives its functionality.
  - The `-M/--monitor` option has been removed because now all state-changing monitor commands can be used as command-line options.

- **Changed:**
  - `monitor onlyloaded` was changed to `monitor onlywhenloaded`
  - Since we now also deal with the `-f` option needed for the openOCD invocation by cortex-debug, we no longer tolerate unknown options.
  - Because printing the possible choices for option values looked very ugly, the help text now states that the choices can be asked for by using a '?'.  The help text looks very tidy now.


### 0.12.0

- **Added:**
  - `-M`/`--monitor` command line option can now be used to set monitor default option in the command line, e.g., `-M v:e` will enable verification after load.
  - With a @-prefix to a file name, one can now request to read further command-line options from a file. If the file does not exist, the @-argument is simply ignored. This can, for example, be used to override options set by the IDE when a fixed name, such as `debug.opt`, is used.
  - A new method in `handler` for telling the user that power-down has been sensed, and a new parameter in power cycle methods to pass this message method down to where it will be called.

### 0.11.1

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


### 0.11.0

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


### 0.10.1

- **Fixed:**
  - Since megaAVRs make a difference between FLASH_PAGE (during programming) and SPM 8during debugging, I added an optional parameter to the read routines in avrdebugger and nvmmegajtag `prog_mode`. While flashing the program, it is true; otherwise, it is false. Seems to do the trick.

### 0.10.0

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


### 0.9.7

- **Added:**
  - The first part of integrating JTAG in xmvmegaavrjtag.py (basically the stuff I added for debugwire), xavr8target.py, jtagtarget.py (first steps and starting and stopping JTAG), and in xavrdebugger.py is working. I can now enter debugging mode on an Xplained324pb board!
  - Added code to revert to debugging mode while flashing a program, enabling the erasure of a single page when using the read-before-write strategy. It turns out that this strategy is now no longer dominant, so defaults should probably be dependent on the debugging interface.
  - New memory areas and methods to access them have been integrated.

### 0.9.6

- **Added:**
  - The attribute `lazy_loading` is added to the class `Memory`. It will be set to `True` by the first X-record concerning flash memory, and it is used to leave excess memory unprogrammed in each step (in `flash_pages`). If, in the end, the server times out not receiving any new records, then it will send an empty packet to the handler, which will be taken as an indication that now flashing should be finalised, i.e., setting `lazy_loading` to `False` again, calling `flash_pages` a last time, and disabling prog mode. This provides a reasonable solution for loading executables in clients without XML support.

### 0.9.5

- **Added:**
  - Some dynamic info messages when flashing large files

### 0.9.4

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

### 0.9.3

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

### 0.9.2

- **Fixed:**
  - Fixed all broken unit tests

- **Added:**
  - Ran tests on ATmega168PB and, unsurprisingly, the chip does not present any problem



### 0.9.1

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
