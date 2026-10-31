
## Quickstart: dw-link & ATtiny85

This quickstart guide demonstrates how to set up a PlatformIO project for debugging on an ATtiny85 without requiring you to invest in a commercial debug probe. Instead, we will build our own debug probe.

 It explains

- how to install the PyAvrOCD GDB server,

- how to turn an Arduino UNO R3 into a [debugWIRE](https://en.wikipedia.org/wiki/DebugWIRE) debug probe using the [dw-link](https://felias-fogg.github.io/dw-link/) firmware,
- how to set up the breadboard with the ATtiny85 on it, and
- how to use PlatformIO for debugging a program on the ATtiny.



### Required hardware

* Arduino Uno (will become the *debug probe*)
* USB cable
* ATtiny85 as the *target*
* In order to connect the debug probe to the target, you need:
     * a breadboard together with
     * 11 Jumper wires (male-to-male)
     * 2 LEDs
     * 3 Resistors (10 kΩ, 220Ω, 220Ω)
     * 2 Capacitors (100 nF, 10 µF)

### Step 1: Set up a project with the right platform

Setup a PlatformIO project and instead of using `atmelavr` as the `platform`, specify the `plarform-atmelavr` fork by felias-fogg in your `platformio.ini` configuration file:

```
[platformio]
default_envs = debug

[env:attiny85]
platform = https://github.com/felias-fogg/platform-atmelavr.git ; important!
framework = arduino
board = ATtiny85
board_build.mcu = attiny85
board_build.f_cpu = 800000L

[env:debug]
extends = env:attiny85
build_type = debug
debug_tool = pyavrocd

[env:release]
extends = env:attiny85
build_type = release
build_flags =
  -DNDEBUG
upload_protocol = jtag2isp
upload_port = SERIALPORT            ; Define your serial port here or use VSC command
upload_speed = 19200
```

You find this example also in the following repo:

```bash
https://github.com/felias-fogg/pio-attiny85-example
```

### Step 2: Turn an UNO into a debug probe

First, connect the UNO to your computer using the USB cable. Make sure that you have the permission to access the serial interface (under Linux).

The simplest way to install the firmware is to download or clone the dw-link repository, open the root folder of the repo as a PlatformIO project, and then compile and upload the dw-link Arduino sketch. The Uno now acts as a debug probe.


### Step 3: Set up the hardware

You need to set up the hardware on a breadboard and use six wires to connect the ATtiny to your Uno, turned into a hardware debugger. Note that the notch or dot on the ATtiny is oriented towards the left. 



<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/attiny85-debug-new.png" width="70%">
</p>
The yellow system LED and the electrolyte cap between RESET and GND are optional but very versatile. The LED gives information about the internal state of the debug probe, and the cap prohibits a RESET when the host opens the serial line to the board.

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

The red LED is the *ATtiny-LED* and the yellow one is the *system LED*. The latter gives you information about the internal state of the debugger:

1. debugWIRE mode disabled (LED is off),
2. waiting for power-cycling the target (LED flashes every second for 0.1 sec),3.
3. debugWIRE mode enabled (LED is on),
4. ISP programming (LED is blinking slowly),
5. error state, i.e., not possible to connect to target or internal error (LED blinks furiously every 0.1 sec).

### Step 4: Debug the program

If you have not activated the `debug` environment, now is the time to do it. However, since the debug environment is the default one, it should already be active.

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
After having done that, the ATtiny is in debugWIRE mode, the executable will be loaded, and execution is started. The MCU will remain in debugWIRE mode even when debugging is stopped. You have to exit debugWIRE mode explicitly (see below).

After starting the debugger, program execution will stop in the first line of the internal `main` function, which is signified by the yellow triangle and the highlighted line. How you debug is sketched in the [section on debugging](debugging.md).

### Step 5: Start over or terminate the debugging session

If you have found the bug you were hunting, you can now leave the debugger(red square), edit the program, and start again at step 6. Note that you always have to restart the debugger before any changes you made to the program are effective. In fact, changing the source text while you are debugging is not a good idea, because the correspondence between the compiled code and the source code will be lost.

Instead of starting a new edit/compile/debug cycle, you may want to call it a day and end debugging. In this case, you may wish to switch the MCU back into normal mode, in which ordinary SPI programming is possible. This can be accomplished by typing the command `monitor debugwire disable` into the input line of the `DEBUG CONSOLE` window (1) just before terminating the debugger (2).

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pio-debug-attiny-5.png" width="90%">
</p>
Alternatively, you can also use the `Disable debugWIRE`  project task under the `Platform` heading to disable debugWIRE mode.

### Potential Problems

There is always the chance that something goes south, either debugging does not start at all, or something funny happens while debugging. If so, it is a good idea to have a look at the output in the `DEBUG CONSOLE`. Messages with the prefix [CRITICAL] often tell what went wrong. It may also be a good idea to consult the [Troubleshooting](troubleshooting.md) and the [Limitations](limitations.md) sections.
