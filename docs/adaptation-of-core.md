# How to enable a core for debugging

Extending a core to enable it for debugging (using PyAvrOCD) is almost always the same. There are a few variations, though.

## `platform.txt`

1. Adapt `name` and `version` field (if appropriate).

2. Add the following section under `# AVR compile variables`:

     ```
     # Optimization flags for debugging
     compiler.optimization_flags=-Os -DNDBEUG
     compiler.optimization_flags.release=-Os -DNDBEUG
     compiler.optimization_flags.debug=-Og -ggdb3 -DDEBUG
     ```

3. Change any `-Os`  or equivalent to `{compiler.optimization_flags}` in the section under `# Default "compiler.path" is correct ...`

4. If the `tools` for `upload` and `bootloader` are not defined in the `boards.txt` file, then you may want to add the following under `# AVR Uploader/Programmers tools`

     ```
     upload.tool.default=avrdude
     bootloader.tool.default=avrdude
     ```

5. In the end, add the following section

     ```
     # Debugger configuration (general options)
     # ----------------------------------------
     debug.executable={build.path}/{build.project_name}.elf
     debug.toolchain=gcc
     debug.toolchain.path={runtime.tools.avrocd-tools.path}

     debug.server=openocd
     debug.server.openocd.path={debug.toolchain.path}/pyavrocd
     #next doesn't matter, but should be specified so that cortex-debug is happy
     debug.server.openocd.script=doesnotmatter
     debug.cortex-debug.custom.gdbPath={debug.toolchain.path}/avr-gdb
     debug.cortex-debug.custom.overrideGDBServerStartedRegex=Listening on port \d+ for gdb connection
     debug.cortex-debug.custom.objdumpPath={runtime.tools.avr-gcc.path}/bin/avr-objdump
     debug.cortex-debug.custom.serverArgs.0=-s
     debug.cortex-debug.custom.serverArgs.1=noop
     debug.cortex-debug.custom.serverArgs.2=-d
     debug.cortex-debug.custom.serverArgs.3={build.mcu}
     debug.cortex-debug.custom.serverArgs.4=--manage
     debug.cortex-debug.custom.serverArgs.5=all
     # The next two lines are for boards with auto-power-cycle capabilities
     #debug.cortex-debug.custom.serverArgs.6=--atexit
     #debug.cortex-debug.custom.serverArgs.7=leavedebugwire
     debug.cortex-debug.custom.preLaunchCommands.0=monitor debugwire enable
     debug.cortex-debug.custom.runToEntryPoint=main
     debug.svd_file={debug.toolchain.path}/pyavrocd-util/svd/{build.mcu}.svd
     ```

6. If JTAG boards are debugged and there are no individual clock settings in `board.txt`, then you may want to add (depending on the lowest possible CPU clock):

     ```
     debug.cortex-debug.custom.serverArgs.6=-D
     debug.cortex-debug.custom.serverArgs.7=200
     debug.cortex-debug.custom.serverArgs.8=-P
     debug.cortex-debug.custom.serverArgs.9=3000
     ```

## `boards.txt`

1. The following menus are necessary (if appropriate):

```
menu.jtag=JTAG pins
menu.lto=Compiler LTO
```

2. Add specifications for the two menu entries above. Add `debug.clkdeb` for each clock entry!

## `programmers.txt`

Depending on the debugging interface, the following programmers should be added:

```
#### ISP programmer

atmel_ice_isp.name=Atmel-ICE (AVR) ISP
atmel_ice_isp.communication=usb
atmel_ice_isp.protocol=atmelice_isp
atmel_ice_isp.program.protocol=atmelice_isp
atmel_ice_isp.program.tool=avrdude
atmel_ice_isp.program.extra_params=

atmel_powerdebugger_isp.name=Power Debugger (AVR) ISP
atmel_powerdebugger_isp.communication=usb
atmel_powerdebugger_isp.protocol=powerdebugger_isp
atmel_powerdebugger_isp.program.protocol=powerdebugger_isp
atmel_powerdebugger_isp.program.tool=avrdude
atmel_powerdebugger_isp.program.extra_params=

atmel_jtagice3_isp.name=JTAGICE3 ISP
atmel_jtagice3_isp.communication=usb
atmel_jtagice3_isp.protocol=jtag3isp
atmel_jtagice3_isp.program.protocol=jtag3isp
atmel_jtagice3_isp.program.tool=avrdude
atmel_jtagice3_isp.program.extra_params=

pickit4_isp.name=PICkit4 ISP
pickit4_isp.communication=usb
pickit4_isp.protocol=pickit4_isp
pickit4_isp.program.protocol=pickit4_isp
pickit4_isp.program.tool=avrdude
pickit4_isp.program.extra_params=

snap_isp.name=MPLAB SNAP ISP
snap_isp.communication=usb
snap_isp.protocol=snap_isp
snap_isp.program.protocol=snap_isp
snap_isp.program.tool=avrdude
snap_isp.program.extra_params=

medbg_isp.name=Xplained Mini (mEDBG) UPDI
medbg_isp.communication=usb
medbg_isp.protocol=xplainedmini_isp
medbg_isp.program.protocol=xplainedmini_isp
medbg_isp.program.tool=avrdude
medbg_isp.program.extra_params=

### JTAG programmer

atmel_ice_jtag.name=Atmel-ICE (AVR) JTAG
atmel_ice_jtag.communication=usb
atmel_ice_jtag.protocol=atmelice_jtag
atmel_ice_jtag.program.protocol=atmelice_jtag
atmel_ice_jtag.program.tool=avrdude
atmel_ice_jtag.program.extra_params=

atmel_jtagice3_jtag.name=JTAGICE3 JTAG
atmel_jtagice3_jtag.communication=usb
atmel_jtagice3_jtag.protocol=jtag3
atmel_jtagice3_jtag.program.protocol=jtag3
atmel_jtagice3_jtag.program.tool=avrdude
atmel_jtagice3_jtag.program.extra_params=
atmel_jtagice3_jtag.program.extra_params=-B0.1

atmel_powerdebugger_jtag.name=Power Debugger (AVR) JTAG
atmel_powerdebugger_jtag.communication=usb
atmel_powerdebugger_jtag.protocol=powerdebugger_jtag
atmel_powerdebugger_jtag.program.protocol=powerdebugger_jtag
atmel_powerdebugger_jtag.program.tool=avrdude
atmel_powerdebugger_jtag.program.extra_params=

pickit4_jtag.name=PICkit4 JTAG
pickit4_jtag.communication=usb
pickit4_jtag.protocol=pickit4_jtag
pickit4_jtag.program.protocol=pickit4_jtag
pickit4_jtag.program.tool=avrdude
pickit4_jtag.program.extra_params=

snap_jtag.name=MPLAB SNAP JTAG
snap_jtag.communication=usb
snap_jtag.protocol=snap_jtag
snap_jtag.program.protocol=snap_jtag
snap_jtag.program.tool=avrdude
snap_jtag.program.extra_params=

edbg_jtag.name=Xplained Pro (EDBG) UPDI
edbg_jtag.communication=usb
edbg_jtag.protocol=xplainedpro_jtag
edbg_jtag.program.protocol=xplainedpro_jtag
edbg_jtag.program.tool=avrdude
edbg_jtag.program.extra_params=

### UPDI programmer

atmel_ice_updi.name=Atmel-ICE (AVR) UPDI
atmel_ice_updi.communication=usb
atmel_ice_updi.protocol=atmelice_updi
atmel_ice_updi.program.protocol=atmelice_updi
atmel_ice_updi.program.tool=avrdude
atmel_ice_updi.program.extra_params=

atmel_jtagice3_updi.name=JTAGICE3 UPDI
atmel_jtagice3_updi.communication=usb
atmel_jtagice3_updi.protocol=jtag3updi
atmel_jtagice3_updi.program.protocol=jtag3updi
atmel_jtagice3_updi.program.tool=avrdude
atmel_jtagice3_updi.program.extra_params=-B0.1

atmel_powerdebugger_updi.name=Power Debugger (AVR) UPDI
atmel_powerdebugger_updi.communication=usb
atmel_powerdebugger_updi.protocol=powerdebugger_updi
atmel_powerdebugger_updi.program.protocol=powerdebugger_updi
atmel_powerdebugger_updi.program.tool=avrdude
atmel_powerdebugger_updi.program.extra_params=

edbg_updi.name=Xplained Pro (EDBG) UPDI
edbg_updi.communication=usb
edbg_updi.protocol=xplainedpro_updi
edbg_updi.program.protocol=xplainedpro_updi
edbg_updi.program.tool=avrdude
edbg_updi.program.extra_params=

medbg_updi.name=Xplained Mini / microUPDI (mEDBG) UPDI
medbg_updi.communication=usb
medbg_updi.protocol=xplainedmini_updi
medbg_updi.program.protocol=xplainedmini_updi
medbg_updi.program.tool=avrdude
medbg_updi.program.extra_params=

nedbg_updi.name=Curiosity Nano (nEDBG) UPDI
nedbg_updi.communication=usb
nedbg_updi.protocol=pkobn_updi
nedbg_updi.program.protocol=pkobn_updi
nedbg_updi.program.tool=avrdude
nedbg_updi.program.extra_params=

pickit4_updi.name=PICkit4 UPDI
pickit4_updi.communication=usb
pickit4_updi.protocol=pickit4_updi
pickit4_updi.program.protocol=pickit4_updi
pickit4_updi.program.tool=avrdude
pickit4_updi.program.extra_params=

snap_updi.name=MPLAB SNAP UPDI
snap_updi.communication=usb
snap_updi.protocol=snap_updi
snap_updi.program.protocol=snap_updi
snap_updi.program.tool=avrdude
snap_updi.program.extra_params=

```



