# Quickstart guide: ATmega328P Xplained Mini

This quickstart guide explains how to set up the [Arduino IDE 2](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing/) so that you can use its debugging feature on an [Atmega328P Xplained Mini](https://www.microchip.com/en-us/development-tool/atmega328p-xmini) board. This development board is ideal for making first debugging steps because it already contains an onboard debugger.  This means you do not have to bother with preparing the board for debugging, connecting the debug probe to the board, choosing a programmer/debugger, and setting the proper fuses. It is simply plug-and-play.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/xplained.png" width="35%">
</p>


In addition, this development board has an Arduino UNO R3 footprint. If you solder headers (at the right place) on the board, then it is possible to plug ordinary Uno shields into the headers. And if you need more I/O power, there is also an Xplained Mini board with the ATmega328**PB** for the same price. By the way, these boards are not overly expensive.

## Step 1: Install a new board manager URL

Assuming that you have already installed the Arduino IDE 2, you first have to extend the list of `Additional boards manager URL`s. Start the `Preferences` dialog, which you find, depending on your operating system,  either in the `Arduino IDE` or the `File` menu.

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

You close the dialog by clicking on two `OK` buttons.

## Step 2: Install a debug-enabled core

Now you need to activate the `boards manager` by clicking on the board symbol in the left side bar (1). After the boards manager pane has been opened, type "Debug" into the search line (2). After that, all cores with the word "Debug" in their description are displayed. Scroll down until you see one with the title "Atmel AVR Xplained-minis (Debug enabled)" (3). Install this core by clicking on `Install` (4).

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/IDE-boardmanager.png" width="80%"></p>

Loading the core and all the necessary tools might take a while. After this has been done, you have unleashed the power of the Arduino debugger.

## Step 3: Connect the board and select the board type in the boards manager

In our case, connecting the target board to the host consists simply of plugging the USB cable into the board. After that, you have to select the right board and serial line in the IDE. First, click on `Select Board` in the top bar and choose `Select other board and port ...`.



<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/select-board.png" width="20%"></p>

Then type "328" in the search field (1), select the right board (2), the correct port (3), and finally click the `OK` button.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/select-other.png" width="50%"></p>

## Step 4: Edit and compile sketch



## Step 5: Debug the sketch

## Step 6: Stop debugging and start over, or terminate the debugging session
