## Quickstart: ATmega328P Xplained Mini

The [Atmega328P Xplained Mini](https://www.microchip.com/en-us/development-tool/atmega328p-xmini) development board, which has an Arduino Uno footprint, is ideal for making a first experience with embedded debugging because it already contains an onboard debugger. It is simply plug-and-play.

### Required hardware

The only thing needed is the XPlained Mini board and a USB cable to connect it to your computer.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/xplained.png" width="35%">
</p>

### Step 1: Set up a project with the right platform

Set up a PlatformIO project, e.g., by importing arduino-blink from the example projects. Add the following to your `platformio.ini` configuration file, making the new `xmini` environment the default environment:

```python-repl
[platformio]
default_envs = xmini

[env:xmini]
platform = https://github.com/felias-fogg/platform-atmelavr.git
framework = arduino
board = xmini328p
debug_tool = pyavrocd
```

### Step 2: Debug the program

Click the debug symbol (bug in front of the triangle) in the left side bar, which will bring up the debug panes on the left side. Then, click the green triangle at the top.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pio-debug-1.png" width="90%">
</p>

This will start the compilation process, and after that, the debug server. The code will be uploaded, and execution will begin. A first temporary stop is made in the `main` function. A yellow triangle and the highlighted line signify this. How you can control program execution, and inspect and change the internal state is sketched in the [debugging section](http://localhost:8000/debugging/).

### Step 3: Start over or terminate the debugging session

If you have found the bug you were hunting, you can now leave the editor (red square), edit the program, and start again at step 5. Note that you always have to restart the debugger before any changes you made to the program are effective. In fact, changing the source text while you are debugging is not a good idea, because the correspondence between the compiled code and the source code will be lost.

Instead of starting a new edit/compile/debug cycle, you may want to call it a day and end debugging. In this case, you may wish to switch the MCU back into normal mode, in which ordinary SPI programming is possible. This can be accomplished by typing the command `monitor debugwire disable` into the input line of the `DEBUG CONSOLE` window (1) just before terminating the debugger (2).



<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/pio-debug-attiny-5.png" width="90%">
</p>

Alternatively, you can also use the `Disable debugWIRE`  project task under the `Platform` heading to disable debugWIRE mode.

### Potential Problems

There is always the chance that something goes south, either debugging does not start at all, or something funny happens while debugging. If so, it is a good idea to have a look at the output in the `DEBUG CONSOLE`. Messages with the prefix [CRITICAL] often tell what went wrong. It may also be a good idea to consult the [Troubleshooting](http://localhost:8000/troubleshooting/) and the [Limitations](http://localhost:8000/limitations/) sections of the PyAvrOCD manual.

!!! danger "Warning:  Use IOREF to source attached circuits"
    If you have any attached circuitry, be it on a breadboard or a shield, use the `IOREF` pin to power it. If this is not possible, check out the [`README` file of XminiCore for a solution](https://github.com/felias-fogg/XMiniCore?tab=readme-ov-file#powering-external-circuitry).
