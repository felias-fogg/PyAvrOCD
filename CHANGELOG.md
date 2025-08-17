# Changelog

### 0.11.0

- **Fixed:**
  - The root cause of the annoying problem noted in version 0.10.0 has now been found, and a kludge to solve the issue has been implemented. SNAP and PICkit4 simply do not implement the protocol as described in the EDBG manual. For this reason, `switch_to_progmode` and `switch_to_debmode` have been implemented for the device-specific parts of `avr8trarget`, which uses a restart of the debugging session: `detach`/`deactivate_physical`/`activate_physical`/`enter_progmode` when switching to programming mode. This is followed by `leave_progmode`, if one wants to enter debugging mode.
  
- **Added:**
  
  - `erase_page` and `erase_chip` in the nvm classes. If they cannot be effective, they return False.
  - Extensive warning messages concerning fuse management.
  
- **Changed**:
  
  - Flash programming has been adapted to the new regime
  
  - New monitor default value: *Verify after load* is now off, because it slows down JTAG loading seriously. 
  
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
