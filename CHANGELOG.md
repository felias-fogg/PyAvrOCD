# Changelog

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
