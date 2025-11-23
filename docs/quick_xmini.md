# Quickstart guide: ATmega328P Xplained Mini

This quickstart guide explains how to set up the [Arduino IDE 2](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing/) so that you can use its debugging feature on an [Atmega328P Xplained Mini](https://www.microchip.com/en-us/development-tool/atmega328p-xmini) board. This development board is ideal for making a first experience with embedded debugging because it already contains an onboard debugger.  This means you do not have to bother with preparing the board for debugging, connecting the debug probe to the board, choosing a programmer/debugger, and setting the proper fuses. It is simply plug-and-play.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/xplained.png" width="35%">
</p>


In addition, this development board has an Arduino UNO R3 footprint. If you solder headers (at the right place) on the board, then it is possible to plug ordinary Uno shields into the headers. And if you need more I/O power, there is also an Xplained Mini board with the ATmega328**PB** for the same price. By the way, these boards are not overly expensive.

## Step 1: Extend the list of boards manager URLs

Assuming that you have already installed the Arduino IDE 2, you first have to extend the list of `Additional boards manager URLs`. Start the `Preferences` dialog, which you find, depending on your operating system,  either in the `Arduino IDE` or the `File` menu.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/preferences.png" width="30%">
</p>


Now select the field with the additional board manager URLs.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/preferences-dialog.png" width="50%">
</p>


Type the following URL into a new line:

```
https://felias-fogg.github.io/package_debugging_index.json
```

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/additional-board-urls.png" width="50%">
</p>

You close the dialog by clicking on two `OK` buttons in succession.

## Step 2: Install a debug-enabled core

Now you need to activate the `boards manager` by clicking on the board symbol in the left side bar (1). After the boards manager pane has been opened, type "Debug" into the search line (2). After that, all cores with the word "Debug" in their description are displayed. Scroll down until you see one with the title "Atmel AVR Xplained-minis (Debug enabled)" (3). Install this core by clicking on `Install` (4).

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/IDE-boardmanager.png" width="80%"></p>

Loading the core and all the necessary tools might take a while.

!!! info "Linux systems"
    After installing the first debug-enabled core, users of Linux systems will need to add `udev` rules (see [this note for Linux users](install-link.md#a-note-for-linux-users))

## Step 3: Connect the board and select the board type and port in the boards manager

In our case, connecting the target board to the host consists simply of plugging the USB cable into the board. After that, you have to select the right board and serial line in the IDE. First, click on `Select Board` in the top bar and choose `Select other board and port ...`.



<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/select-board.png" width="20%"></p>

Then type "328" in the search field (1), select the right board (2), the correct port (3), and finally click the `OK` button.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/select-other.png" width="50%"></p>

The debugging icon in the top row is no longer greyed out. In other words, you have unleashed the power of the Arduino debugger at this point.

## Step 4: Edit and compile a sketch

Let us choose a simple sketch that is a little bit more challenging than the `Blink` example. The `Debounce` example will do. Let us load it and modify it for our needs.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/debounce-example.png" width="80%"></p>

This sketch will toggle the LED state (on pin 13) when a button is pressed. The program logic contains a basic form of debouncing so that noise induced by the button contact opening and closing is ignored. The button in this sketch is supposed to be at digital input line 2. The xmini, however, has such a button at digital input line 21. For this reason, we have to change line 31 of the sketch as follows:

```C++
const int buttonPin = 21;  // the number of the pushbutton pin
```

Before compiling and uploading the sketch, you should set the `Optimize for Debugging` flag in the `Sketch` menu. This flag will make sure that the produced machine code resembles the program flow in the source code in order to make debugging easier.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/optimize-for-debug.png" width="30%"></p>

Now it is time to compile the sketch. Click the `Verify` button (a check mark symbol) in the top bar, which will compile the sketch. Loading the compiled code will then be done when the debugger is started. Instead, you can click on the `Upload` button (the right arrow symbol), which will compile and upload the code. In the case of the Xmini development board, this is the preferred way because it results in an overall faster upload time.

## Step 5: Debug the sketch

Now it is time to start debugging by clicking the `Debug` button (bug in front of a triangle) in the top row.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-xmini-0.png" width="80%"></p>

This will trigger a lot of actions. First, the debug pane to the left of the sketch editor pane will be opened. Second, below the sketch editor pane, first a `gdb-server` console will appear, then the `Debug Console`. While this is happening, the sketch is loaded and execution is started.

The execution will always stop in the first line of the `main` function in `main.cpp`, which is an Arduino internal function. The line where execution has been stopped is marked yellow (perhaps with an additional yellow triangle) (A). Since this line is in a file different from the main sketch, it is loaded into the editor, and the loaded files are all shown in the top bar of the editor (B). The central debugging control is located in the debugging pane at the top (C). The buttons have the following meanings, from left to right:

- *Reset*ting the device
- *Continue* execution or *pause*
- *Step over*: execute one source line
- *Step into*: execute stepping into the function, if in this line one is called
- *Step out*: finish the current function and stop after the line where it was called
- *Restart*: Same as Reset
- *Stop*: Terminate debugging

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-xmini-1.png" width="80%"></p>

Pressing the `Continue` button in the situation depicted in the picture above would start execution. However, before we do this, let us set a breakpoint. For this purpose, we first select the original sketch file `Debounce.ino` at the top row of the editor pane.

This will bring up the sketch file. Scroll down to line 75 and set a breakpoint by clicking to the left of the line number (1). A red dot will mark the breakpoint. Now press the `Continue` button (2).

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-xmini-2.png" width="80%"></p>

Sketch execution will be immediately stopped in line 75. Now we want to examine the values of some of the variables. If you hover with the mouse over a variable, its value will be shown. If we want to always track the value of the variable, we can use the watch window. Move with the mouse to the right part of the `WATCH` bar. Then a plus sign will appear. Clicking on it allows you to enter "watch" expressions.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-xmini-2a.png" width="80%"></p>

If we add buttonState and ledState to the `WATCH` pane, we see that they are both currently 1. If we now click the `Continue` button, `ledState` variable will be toggled (i.e., the LED will go dark) and the sketch will wait for a change of the button state.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-xmini-3.png" width="80%"></p>

Pressing the button changes the level and will stop again in line 75, as shown below. The value of both variables is now 0. From here on, you can explore the debugger on your own. Hovering the mouse over symbols and names will bring up a short explanation. In this tutorial, we will now stop and press the exit symbol (red square).

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-xmini-4.png" width="80%"></p>

## Step 6: Start over or terminate the debugging session

You now can edit the sketch and start again at step 4. Note that you always have to recompile and restart the debugger before any changes you made to sketch are effective. In fact, changing the source text while yore are debugging is not a good idea, because the correspondence between the compiled code and rthe source code will be lost.

Instead of starting a new edit/compile/debug cycle, you can call it day and end debugging. In this case, it may be a good idea to disable the `Optimize for Debugging` flag in the `Sketch` menu, because not doing so will result in larger codes next time you compile a sketch.

## Potential problems

There is always the chance that something goes south, either debugging does not start at all or something funny happens while debugging. If so, it is a good idea to have a look at the output of the `gdb-server` console. Messages with the prefix \[CRITICAL] often tell what went wrong. It may also be a good idea to consult the [Troubleshooting](troubleshooting.md) and the [Limitations](limitations.md) section of the PyAvrOCD manual.

!!! danger "Warning: Do not source attached circuits through the 5V or 3V pin. Use IOREF!"
    If you have any attached circuitry, be it on a bread board or a shield, use the `IOREF` pin to power it.


    The reason for this is that the `IOREF` pin is under the switching control of the onboard debugger. So, if a power cycle is necessary to bring the MCU into debugWIRE mode, then the MCU as well as IOREF will be connected to GND and then powered again. The 5V/3V pins are not switched and deliver always power. This could lead to the situation that the MCU will be powered through its I/O pins, which is not healthy for the chip and will also prohibit that the MCU switches to debugWIRE mode.
