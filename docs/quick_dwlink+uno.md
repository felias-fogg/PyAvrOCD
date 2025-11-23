# Quickstart guide: dw-link & Arduino UNO R3

This quickstart guide shows how to try out embedded debugging as offered by the Arduino IDE 2 without requiring you to invest in a debug probe. It explains

- how to turn an Arduino UNO R3 into a [debugWIRE](https://debugwire.de/) debug probe using the [dw-link](https://github.com/felias-fogg/dw-link/) firmware,
- how to set up the [Arduino IDE 2](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing/) so that you can use its debugging feature,  and
- how to use this combo in order to do embedded debugging on another Arduino UNO R3 (or Pro Mini or other ATmega 328P board).

This means that you need two UNO boards to try out debugging. In addition, you need:

- a pushbutton,
- 6 jumper wires (male-male),
- a 10 µF electrolyte capacitor (optionally), and
- an LED with a 200 Ω resistor soldered to one leg (optionally).

## Step 1: Turning an UNO into a debug probe

Download the [latest release of dw-link](https://github.com/felias-fogg/dw-link/releases/latest) from GitHub. Then uncompress the archive and start the Arduino IDE 2. Open the sketch `dw-link-X.Y.Z/dw-link/dw-link.ino` and upload it to the UNO that you want to use as the debug probe.

From now on, you can use this board as a debug probe. In order to make it easier to use, plug the (optional) electrolyte capacitor into the RESET and GND header (the negative pin goes into GND). This will make sure that the board does not go into RESET when the debug probe is started. In addition, put the LED with the soldered-on resistor into the header 6 and 7, 6 being used as GND. The LED tells you the internal state of the debug probe:

1. debugWIRE mode disabled (LED is off),
2. waiting for power-cycling the target (LED flashes every second for 0.1 sec)
3. debugWIRE mode enabled (LED is on),
4. ISP programming (LED is blinking slowly),
5. error state, i.e., not possible to connect to target or internal error (LED blinks furiously every 0.1 sec).

The completed board setup may then look as follows.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/dw-link.png" width="50%">
</p>

## Step 2: Extend the list of boards manager URLs

You first have to extend the list of `Additional boards manager URLs`. Start the `Preferences` dialog, which you find, depending on your operating system,  either in the `Arduino IDE` or the `File` menu.

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

## Step 3: Install the debug-enabled Arduino AVR Boards core

Now you need to activate the `boards manager` by clicking on the board symbol in the left side bar (1). After the boards manager pane has been opened, type "Debug" into the search line (2). After that, all cores with the word "Debug" in their description are displayed. Scroll down until you see one with the title "Arduino AVR Boards (Debug enabled)". This is a fork of the official Arduino AVR core, containing all the changes to make debugging possible. Install this core by clicking on `Install` (3). For the expert: You can also employ [MiniCore](https://github.com/MCUdude/MiniCore), which has support for the 328P and built-in debug support.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/IDE-boardmanager-Arduino.png" width="80%"></p>

Loading the core and all the necessary tools might take a while.

!!! info "Linux systems"
    After installing the first debug-enabled core, users of Linux systems will need to add `udev` rules (see [this note for Linux users](install-link.md#a-note-for-linux-users))

## Step 4: Prepare the target board for debugging

If you are going to debug an Arduino with an ATmega328P or similar, you have to alter the board physically in most cases before debugging is possible. The reason is a capacitor that is connected to the RESET line of the MCU, which is responsible for issuing a RESET when a connection to the board is established. On an original UNO board, you need to cut a solder bridge labeled `RESET EN`.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/cutconn.jpg" width="60%">
</p>
On other boards, [similar modifications are most likely necessary](https://debugwire.de/board-modifications/).

!!! Warning
    Not disconnecting the capacitor (or other loads) from the RESET line of the MCU may lead to the situation that debugWIRE mode is activated on a MCU, but it is impossible to communicate with the MCU. In particular, one cannot leave debugWIRE mode anymore.

In addition to these physical modifications, we also want to add a pushbutton, with one pin going into digital header slot 2 of the board. The other pin needs to be connected to GND. In my case, I use the header slot 4, which then has to be an output, which is `LOW`.

## Step 5: Connect the target board with the debug probe

Connecting the target and debug probe boards is not entirely straightforward. You have to connect all ISP connections, except for the RESET line. This goes into the header slot 8 on the debug probe. A Fritzing sketch looks as follows.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/Uno-debug-new.png" width="70%">
</p>

The USB connector must be plugged into the hardware debugger. In reality, this could look like the following.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/uno+dwlink.JPG" width="60%">
</p>

## Step 6: Select the board type

After having set up the hardware, you have to select the right board. First, click on `Select Board` in the top bar and choose `Select other board and port ...`.



<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/select-board.png" width="20%"></p>

Then type "Uno" in the search field (1), select the right board (2), and finally click the `OK` button. We do not care much about the serial port. However, we might as well select the serial that is connected with our debug probe.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/select-other.png" width="50%"></p>



## Step 7: Edit and compile a sketch

Let us choose a simple sketch that is a little bit more challenging than the `Blink` example. The `Debounce` example will do. Let us load it and modify it for our needs.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/debounce-example.png" width="80%"></p>

This sketch will toggle the LED state (on pin 13) when a button is pressed. The program logic contains a basic form of debouncing so that noise induced by the button contact opening and closing is ignored. The button in this sketch is supposed to be at digital input line 2. As mentioned above, the GND pin shall be the header slot 4. For this reason, we replace the empty line 32 in the `Debounce.ino` sketch with the following line

```C++
const int buttonGND = 4;  // the number of the pushbutton GND pin
```

Further, we need to replace  line 45 with

```C++
   pinMode(buttonPin, INPUT_PULLUP);
```

 and the empty line 47 with

```C++
   pinMode(buttonGND, OUTPUT);
```

Before compiling and uploading the sketch, you should set the `Optimize for Debugging` flag in the `Sketch` menu. This flag will make sure that the produced machine code resembles the program flow in the source code in order to make debugging easier.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/optimize-for-debug.png" width="30%"></p>

Now it is time to compile the sketch. Click the `Verify` button (a check mark symbol) in the top bar, which will compile the sketch. Loading the compiled code will then be done when the debugger is started.

## Step 8: Start debugging

Now it is time to start debugging by clicking the `Debug` button (bug in front of a triangle) in the top row.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-uno-0.png" width="80%"></p>

Then the IDE tries to discover a debug probe. If it finds one, it will connect and check whether the target is already in the debugWIRE mode. If this is not the case, the IDE requests a power cycle, i.e., disconnecting power from the target board and then reconnecting power. The debug probe dw-link will start to flash eveery second.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-uno-0a.png" width="80%"></p>

Power-cycling is something you have to do manually by removing the jumper cable and reinserting it. Sometimes, this does not work out according to plan, and an error message is issued. Usually, at a second attempt, it works out with the MCU already being in debugWIRE mode.

## Step 9: Debug the sketch

If the debugger has successfully started and the binary has been loaded into flash, execution will begin. It will always stop in the first line of the `main` function in `main.cpp`, which is an Arduino internal function. The line where execution has been stopped is marked yellow (perhaps with an additional yellow triangle) (A). Since this line is in a file different from the user sketch, it is loaded into the editor, and the loaded files are all shown in the top bar of the editor (B). The central debugging control is located in the debugging pane at the top (C). The buttons have the following meanings, from left to right:

- *Reset*ting the device
- *Continue* execution or *pause*
- *Step over*: execute one source line
- *Step into*: execute stepping into the function, if in this line one is called
- *Step out*: finish the current function and stop after the line where it was called
- *Restart*: Same as Reset
- *Stop*: Terminate debugging

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-uno-1.png" width="80%"></p>

Pressing the `Continue` button in the situation depicted in the picture above would start execution. However, before we do this, let us set a breakpoint. For this purpose, we first select the original sketch file `Debounce.ino` at the top row of the editor pane.

This will bring up the sketch file. Scroll down to line 75 and set a breakpoint by clicking to the left of the line number (1). A red dot will mark the breakpoint. Now press the `Continue` button (2).

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-uno-2.png" width="80%"></p>

Sketch execution will be immediately stopped in line 75. Now we want to examine the values of some of the variables. If you hover with the mouse over a variable, its value will be shown. If we want to always track the value of the variable, we can use the watch window. Move with the mouse to the right part of the `WATCH` bar. Then a plus sign will appear. Clicking on it allows you to enter "watch" expressions.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-uno-2a.png" width="80%"></p>

If we add `buttonState` and `ledState` to the `WATCH` pane, we see that they are both currently 1. If we now click the `Continue` button, `ledState` variable will be toggled (i.e., the LED will go dark) and the sketch will run and wait for a change of the button state.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-uno-3.png" width="80%"></p>

Pressing the button changes the level and will stop again in line 75, as shown below. The value of both variables is now 0. From here on, you can explore the debugger on your own. Hovering the mouse over symbols and names will bring up a short explanation. In this tutorial, we will now stop and press the exit symbol (red square).

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-uno-4.png" width="80%"></p>

## Step 10: Start over or terminate the debugging session

You now can edit the sketch and start again at step 4. Note that you always have to recompile and restart the debugger before any changes you made to sketch are effective. In fact, changing the source text while you are debugging is not a good idea, because the correspondence between the compiled code and rthe source code will be lost.

Instead of starting a new edit/compile/debug cycle, you can call it day and end debugging. In this case, you perhaps will switch the MCU back from debugWIRE mode to normal mode, in which SPI programming is possible. In order to achieve that, type `monitor debugwire disable` into the prompt line of the `Debug Console` before ending the debug session.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-uno-5.png" width="80%"></p>

If you scroll down in the `Debug Console`, you will see that the command was successful. Now you can definitely leave the debugger.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-uno-6.png" width="80%"></p>

It may also be a good idea to disable the `Optimize for Debugging` flag in the `Sketch` menu, because not doing so will result in larger codes next time you compile a sketch.

If you want to restore your UNO to its original state, you also need to burn the bootloader again. For this purpose choose the serial line connected to dw-link.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/choose-serial-uno.png" width="50%"></p>



Select as the programmer `Arduino as ISP`.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/choose-programmer-uno.png" width="40%"></p>

The select the Burn Bootloader entry in the tools menu.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/choose-burn-bootloader.png" width="25%"></p>

The debug probe should then be able to handle the rest.

As a final measure you may want to restore the solder bridge `RESET EN` or reinsert a removed capacitor. If possible, you can also try to fit onto the board some pins that can be shortened with a jumper.

## Potential problems

There is always the chance that something goes south, either debugging does not start at all or something funny happens while debugging. If so, it is a good idea to have a look at the output of the `gdb-server` console. Messages with the prefix \[CRITICAL] often tell what went wrong. It may also be a good idea to consult the [Troubleshooting](troubleshooting.md) and the [Limitations](limitations.md) section of the [PyAvrOCD manual](https://felias-fogg.github.io/PyAvrOCD/).

