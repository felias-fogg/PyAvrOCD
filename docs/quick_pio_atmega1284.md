## Quickstart: Atmel-ICE & ATmega1284

This quickstart guide shows you how to set up a PlatformIO project for debugging a JTAG target using an EDBG-based debug probe.

### Required hardware

We will use an ATmega1284 (but any other AVR JTAG Mega will do) and the debug probe Atmel-ICE  (any other [EDBG-based debug probe](supported-debuggers.md) is also OK). In addition, we will use the [DIP-40 Arduino-compatible development board](https://www.tindie.com/products/mcudude/dip-40-arduino-compatible-development-board/) to demonstrate basic debugging, but again, any board with a JTAG and ISP connector would do.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/Mighty.png" width="30%">
</p>


In the following, I will assume that PlatformIO, as an extension of VSCode, has been installed already and that you are somewhat familiar with it.

### Step 1: Set up a project with the right platform

Set up a PlatformIO project and instead of using `atmelavr` as the platform, specify the following in your `platformio.ini` configuration file:

```
...
platform = https://github.com/felias-fogg/platform-atmelavr.git
framework = arduino
board = ATmega1284P
...
```

The best way to start is to clone or download the following repository.

```
https://github.com/felias-fogg/pio-atmega1284p-example
```

The `plaformio.ini` file contains the following sections:

```
[env:atmega1284p]
;;contains all information about the platform & chip and
;;how to commuincate with Atmel-ICE
...

[env:debug]
;; enables debugging
...

[env:release]
;; supports uploading in release mode
...
```



### Step 2: Prepare the board for debugging

Before debugging can take place, you need to make sure that the JTAG pins are enabled. On an ATmega1284P, these are the pins  `PC2`&mdash;`PC5`. Fresh from the factory, the JTAG pins are enabled. However, on Arduino boards, they are by default disabled. Since the state is probably unknown, we will set it anyway. In order to activate the JTAG pins, we need to connect the Atmel-ICE to the board using the ISP connection, as shown in the following photo. On this board, the key or marker of the ISP plug should be oriented towards the MCU.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/atmelice_isp.jpg" width="70%">
</p>

In order to set the correct fuses, we now select the `debug` environment by first clicking on the environment symbol in the bottom line and then choosing the right environment at the top.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pio-clone-3.png" width="90%">
</p>

After that, we request that the fuses be set by clicking on `Set Fuses`. The result of this action is displayed in the `Terminal` window and should be as shown in the picture below.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pio-clone-4.png" width="90%">
</p>
Before we can start debugging, we need to change the connection between the debug probe and the target board from ISP to JTAG, as shown in the following picture. As with the ISP plug, the keying or marker should be oriented towards the MCU on this board.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/atmelice_jtag.jpg" width="70%">
</p>


### Step 3: Debug the program

If you have not activated the `debug` environment, now is the time to do it (as shown in the previous step). And then we are ready to go into business seriously. First, click the debug symbol (bug in front of the triangle) in the left side bar, which will bring up the debug panes on the left side. Then, click the green triangle at the top.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pio-debug-1.png" width="90%">
</p>

This will start the compilation process, and after that, the debug server. The code will be uploaded, and execution will begin. A first temporary stop is made in the `main` function. A yellow triangle and the highlighted line signify this. How you can control the program is sketched in the [debugging section](debugging.md).

### Step 4: Start over or terminate the debugging session

If you have found the bug you were hunting, you can now leave the debugger (red square), edit the program, and start again at step 5. Note that you always have to restart the debugger before any changes you made to the program are effective. In fact, changing the source text while you are debugging is not a good idea, because the correspondence between the compiled code and the source code will be lost.

Instead of starting a new edit/compile/debug cycle, you may want to call it a day and end debugging. In this case, you may wish to disable the JTAG pins, perhaps. Switch to the `release` environment and click `Set Fuses` again. Possibly, you even want to restore the bootloader, which was deleted when starting the debugger. In this case, you need to click `Burn Bootloader`.

### Potential Problems

There is always the chance that something goes south, either debugging does not start at all, or something funny happens while debugging. If so, it is a good idea to have a look at the output in the `DEBUG CONSOLE`. Messages with the prefix \[CRITICAL] often tell what went wrong. It may also be a good idea to consult the [Troubleshooting](troubleshooting.md) and the [Limitations](limitations.md) sections of the PyAvrOCD manual.

One common problem is forgetting to change from ISP to JTAG or back. In this case, the debug probe complains that there is no device.
