## Quickstart: Curiosity Nano

The [Curiosity Nano](https://www.microchip.com/en-us/development-tools-tools-and-software/development-tools-category-explorer?category=curiosityboards&subcategory=8-bit-curiosity-nano-boards) development boards provide an ideal and affordable entry into embedded programming and debugging because they have a debugger already on board. This makes it a plug-and-play experience.

### Required hardware

You need a Curiosity Nano board and a USB cable to connect the board to your computer.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/cnano.png" width="55%">
</p>

### Step 1: Install a debug-capable Arduino package

Add one of the following URLs, depending on [what board you want to deal with](supported-boards.md), to the list of *boards manager URL*s in the `Preferences` dialog:

```
https://felias-fogg.github.io/MegaCoreX/package_MCUdude_MegaCoreX_index.json
https://felias-fogg.github.io/megaTinyCore/package_SpenceKonde_megaTinyCore_index.json
https://felias-fogg.github.io/DxCore/package_SpenceKonde_DxCore_index.json
```

In addition, you need the `AvrDebugger` board package as well.[^*] So add the following URL:

```
https://felias-fogg.github.io/AvrDebugger/package_felias-fogg_AvrDebugger_index.json
```

{!details-boards-manager-url.md!}

Next, you have to install the appropriate Arduino packages. Activate the `Boards Manager`, select the most recent versions of the package you want to install, and click on `Install`.

{!details-install-package.md!}

!!! info "Linux systems"
    After the installation, users of Linux systems will need to add `udev` rules. Download [https://pyavrocd.io/99-edbg-debuggers.rules](https://pyavrocd.io/99-edbg-debuggers.rules), edit if you want, and copy to `/etc/udev/rules.d/`.

### Step 2: Load sketch and select board

Load a sketch, e.g., the `Blink` sketch, and select the right board: `Tools -> Board -> <package> -> <board>`. If you want to use serial I/O, you need to select the right `Port` in the `Tools` menu. The boards do not always use the standard serial interface. Check out the [section on supported Microchip boards](supported-boards.md). Finally, you may want to set a few additional options in the `Tools` menu, such as the chip, the pinout, etc.

### Step 3: Compile the sketch

Activate `Optimize for Debugging` in the `Sketch` menu. This only needs to be done once. Then click on the `Verify` button (checkmark) in the top bar. This will compile the sketch.

### Step 4: Debug the sketch

It is time to start debugging by clicking the `Debug` button (bug in front of a triangle) in the top bar. This will open the `DEBUG` pane after a while. Now you can start and stop execution, inspect variables, set breakpoints, and the like (see section on [debugging](debugging.md)). Clicking on the red square in the top bar of the DEBUG pane will terminate the current debugging episode.

### Step 5: Start over or terminate the debugging session

You can now edit the sketch and start again at step 3. Note that you always have to recompile and restart the debugger before any changes you made to the sketch are effective.

If you want to stop debugging, it may be a good idea to deactivate the `Optimize for Debugging` option.

### Potential problems

If something goes wrong, it is a good idea to have a look at the output of the `gdb-server` console. Messages with the prefix \[CRITICAL] often tell what went wrong. It may also be a good idea to consult the [Troubleshooting](troubleshooting.md) and the [Limitations](limitations.md) section of the PyAvrOCD manual.

[^*]: Strictly speaking, you need to install it only for future board packages. But then it does not hurt to do that right now, already.
