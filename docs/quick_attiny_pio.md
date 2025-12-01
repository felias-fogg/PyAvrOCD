

# Quickstart guide: dw-link & ATtiny85

This quickstart guide demonstrates how to set up a PlatformIO project for debugging on an ATtiny85 without requiring you to invest in a debug probe.

 It explains

- how to install the PyAvrOCD GDB server,

- how to turn an Arduino UNO R3 into a [debugWIRE](https://debugwire.de/) debug probe using the [dw-link](https://github.com/felias-fogg/dw-link/) firmware,
- how to set up the breadboard with the ATtiny85 on it, and
- how to use PlatformIO for debugging a program on the ATtiny.



## Required hardware

* Arduino Uno (will become the *debug probe*)
* USB cable
* ATtiny85 as the *target*
* In order to connect the debug probe to the target, you need:
     * a breadboard together with
     * 11 Jumper wires (male-to-male)
     * 2 LEDs
     * 3 Resistors (10 kΩ, 220Ω, 220Ω)
     * 2 Capacitors (100 nF, 10 µF)

{!pio_quick_install.md!}

## Step 3: Turn an UNO into a debug probe

Download the dw-link firmware. This means you should

* go to the [dw-link GitHub repo](https://github.com/felias-fogg/dw-link),
* as in Step 1, click on the  `Latest` label below **Releases**,
* download the **Source Code**, either zip or tar.gz,
* extract the project files using `unzip` or `tar -xvzf`.

In order to install the firmware,

* connect the Arduino Uno to your computer with a USB cable,
* open VSCode/PlatformIO,
* open the folder  `dw-link-x.y.z` with the extracted project files in VSCode,
* and load the program`dw-link-x.y.z/src/dw-link.ino` into the editor (ignore the warnings from PlatformIO),
* compile the program and upload it to the Uno.

The Uno now acts as a debug probe providing a [GDB RSP](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Remote-Protocol.html) interface. If you configured the serial line to the Uno as 115200 baud, and click on `Monitor` in the `PROJECT TASK` menu, select the `Terminal` window, and then type a minus sign into this window, you should get the response "$#00". If you type Ctrl-E, the probe should respond with "dw-link".

## Step 4: Set up the example project

Since PyAvrOCD is a custom debug solution, a number of things have to be specified in the PlatformIO configuration file `platformio.ini`, too long to present here. You can clone a project containing this file, together with a small program, from

```
https://github.com/felias-fogg/pio-attiny85-example
```

After opening a `new window`, click on `Clone Git Repository...` and type the above line into the input field. Perhaps VS Code asks you to log in to GitHub first.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pio-clone-attiny-1.png" width="90%">
</p>


The repo will be cloned, and you have to provide a destination for it.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pio-clone-2.png" width="90%">
</p>



## Step 5: Set up the hardware

You need to set up the hardware on a breadboard and use six wires to connect the ATtiny to your Uno, turned into a hardware debugger. Note that the notch or dot on the ATtiny is oriented towards the left.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/attiny85-debug-new.png" width="70%">
</p>
In reality, this could be like in the following photo.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/attiny-breadboard.jpg" width="30%">
</p>


Here is a table of all the connections so that you can check that you have made all the connections.

| ATtiny pin#  | Arduino Uno pin | component                                                    |
| ------------ | --------------- | ------------------------------------------------------------ |
| 1 (Reset)    | D8              | 10k resistor to Vcc                                          |
| 2 (D3)       |                 |                                                              |
| 3 (D4)       |                 | 220 Ω resistor to target (red) LED (+)                       |
| 4 (GND)      | GND             | red and yellow LED (-), decoupling cap 100 nF, RESET blocking cap of 10µF (-) |
| 5 (D0, MOSI) | D11             |                                                              |
| 6 (D1, MISO) | D12             |                                                              |
| 7 (D2, SCK)  | D13             |                                                              |
| 8 (Vcc)      | 5V              | 10k resistor, decoupling cap 100 nF                          |
| &nbsp;       | RESET           | RESET blocking cap of 10 µF (+)                              |
| &nbsp;       | D7              | 220 Ω to system (yellow) LED (+)                             |

The yellow LED is the *system LED*, and the red one is the *ATtiny-LED*. The system LED gives you information about the internal state of the debugger:

1. debugWIRE mode disabled (LED is off),
2. waiting for power-cycling the target (LED flashes every second for 0.1 sec),3.
3. debugWIRE mode enabled (LED is on),
4. ISP programming (LED is blinking slowly),
5. error state, i.e., not possible to connect to target or internal error (LED blinks furiously every 0.1 sec).

## Step 6: Debug the program

If you have not activated the `debug` environment, now is the time to do it.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pio-debug-attiny-1.png" width="90%">
</p>

And then we are ready to go into business seriously. First, click the debug symbol (bug in front of the triangle) in the left side bar, which will bring up the debug panes on the left side. Then, click the green triangle at the top.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pio-debug-attiny-2.png" width="90%">
</p>

This will start the debugging process and open the `TERMINAL` window below the editor window. Click on the `DEBUG CONSOLE` label, so that this console will be opened. There, you will probably see that you should power cycle the target.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pio-debug-attiny-3.png" width="90%">
</p>

After having done that, the ATtiny is in debugWIRE mode, the executable will be loaded, and after that, execution is started. As required, execution will stop in the setup function, which is signified by the yellow triangle and the highlighted line (A). The most crucial control panel (B) is now the one shown on the right side at the top. It enables you (from left to right) to

- *continuing/suspending* execution,
- *stepping-over*, i.e., making a step to the beginning of the following source line in the same function,
- *stepping-in*, that is, making a step to the following source line (entering perhaps a new function),
- *stepping-out*, that is, executing the current function until it returns to the calling function,
- *resetting* the MCU, and
- *terminating* the debugging session.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pio-debug-attiny-4.png" width="90%">
</p>
From here on, I believe, you know your way around. Otherwise, consult, e.g., the [debugging section of another quickstart guide](quick_atmega1284_pio.md#step-5-debug-the-program).

## Step 7: Start over or terminate the debugging session

If you have found the bug you were hunting, you can now leave the editor (red square), edit the program, and start again at step 6. Note that you always have to restart the debugger before any changes you made to the program are effective. In fact, changing the source text while you are debugging is not a good idea, because the correspondence between the compiled code and the source code will be lost.

Instead of starting a new edit/compile/debug cycle, you may want to call it a day and end debugging. In this case, you may wish to switch the MCU back into normal mode, in which ordinary SPI programming is possible. This can be accomplished by typing the command `monitor debugwire disable` into the input line of the `DEBUG CONSOLE` window (1) just before terminating the debugger (2).

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pio-debug-attiny-5.png" width="90%">
</p>

## Potential Problems

There is always the chance that something goes south, either debugging does not start at all, or something funny happens while debugging. If so, it is a good idea to have a look at the output in the `DEBUG CONSOLE`. Messages with the prefix [CRITICAL] often tell what went wrong. It may also be a good idea to consult the [Troubleshooting](https://felias-fogg.github.io/PyAvrOCD/troubleshooting/) and the [Limitations](https://felias-fogg.github.io/PyAvrOCD/limitations/) section of the PyAvrOCD manual.
