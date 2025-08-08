# Changelog

### 0.9.2

- **Added:**
  - Ran tests on ATmega168PB and, unsurprisingly, the chip does not present any problem

- **Fixed:**
  - Fixed all broken unit tests
  -

### 0.9.1

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
- **Fixed:**
  - Omissions and errors patched in ATDF files (read README in the atdf folder)




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