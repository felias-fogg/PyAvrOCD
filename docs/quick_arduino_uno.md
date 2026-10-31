## Quickstart: dw-link & Arduino UNO

This quickstart guide shows how to try out embedded debugging as offered by the Arduino IDE 2 without requiring you to invest in a debug probe. It will turn an Arduino Uno into a debug probe.

### Required hardware

- Two Arduino UNO R3 (or similar),
- one USB cable (for the connection to the host),
- 6 jumper wires (male-male),
- a 10 µF electrolyte capacitor (optionally), and
- an LED with a 200 Ω resistor soldered to one leg (optionally).

### Step 1: Turning an UNO into a debug probe

The simplest way to flash the hardware debugger firmware onto an Arduino UNO is to install the library **dw-link** with the library manager, and then upload the example sketch *dw-link* (`File` -> `Examples` -> `dw-link` -> `dw-link`). Alternatively, you can download or clone the [dw-link repository](https://github.com/felias-fogg/dw-link) and then compile and upload the dw-link sketch from the examples folder.

From now on, you can use this board as a debug probe. In order to make it easier to use, plug the (optional) electrolyte capacitor into the RESET and GND header (the negative pin goes into GND). This will make sure that the board does not go into RESET when the host contacts the debug probe. In addition, put the LED with the soldered-on resistor into the header 6 and 7, 6 being used as GND. The LED tells you the internal state of the debug probe:

1. debugWIRE mode disabled (LED is off),
2. waiting for power-cycling the target (LED flashes every second for 0.1 sec)
3. debugWIRE mode enabled (LED is on),
4. ISP programming (LED is blinking slowly, 0.5 sec on, 0.5 sec off),
5. error state, i.e., not possible to connect to target or internal error (LED blinks furiously every 0.1 sec).

The completed board setup may then look as follows.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/dw-link.png" width="50%">
</p>

### Step 2: Install the debug-enabled MiniCore

Since the stock Arduino AVR Boards package does not support debugging, we need to shop elsewhere. For this reason, you need to add a new *boards manager URL* in the `Preferences` dialog so that `MiniCore` can be installed:

```
https://mcudude.github.io/MiniCore/package_MCUdude_MiniCore_index.json
```

{!details-boards-manager-url.md!}

Next you have to install the `MiniCore`. Activate the `Boards Manager`, select `MiniCore`, and click on `Install`.

{!details-install-package.md!}

### Step 3: Prepare the target board for debugging

On an original UNO board, you need to cut a solder bridge labeled `RESET EN` in order to disconnect the auto-RESET enabling capacitor.

<details>
<summary><b>Picture showing the cut</b></summary>
<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/cutconn.jpg" width="60%">
</p>
</details>
<p></p>

On other boards, [similar modifications are most likely necessary](board-preparation.md#preparing-a-debugwire-target).

!!! Warning
    Not disconnecting the capacitor (or other loads) from the RESET line of the MCU may lead to the situation that debugWIRE mode is activated on the MCU, but it is impossible to communicate with the MCU. In particular, one cannot leave debugWIRE mode anymore.


### Step 4: Connect the target board with the debug probe

You have to connect all SPI programming pins except for the RESET line. This goes into the header slot 8 on the debug probe. A Fritzing sketch looks as follows.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/Uno-debug-new.png" width="70%">
</p>

The USB connector must be plugged into the hardware debugger.

### Step 5: Load sketch and select board

Load a sketch, e.g., the `Blink` sketch, and select the right board: `Tools -> Board -> MiniCore -> ATmega328`.

### Step 6: Compile the sketch

Activate `Optimize for Debugging` in the `Sketch` menu. This only needs to be done once. Then click on the `Verify` button (leftmost button) in the top bar. This will compile the sketch.

### Step 7: Start debugging

Now it is time to start debugging by clicking the `Debug` button (bug in front of a triangle) in the top bar. If the target MCU is not already in debugWIRE mode, the debugger will request 'power cycling'.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-uno-0a.png" width="90%"></p>

Power cycling means to remove the Vcc jumper cable and after a few seconds to reinsert it. After a while, the `DEBUG` pane should open.

### Step 8: Debug the sketch

You can now start and stop execution, inspect variables, set breakpoints, and the like (see section on [debugging](debugging.md)). Clicking on the red square in the top bar of the DEBUG pane will terminate the current debugging episode.

### Step 9: Start over or terminate the debugging session

After leaving the debugger, you can edit the sketch and start again at step 6. Note that you always have to recompile and restart the debugger before any changes you made to the sketch are effective.

Instead of starting a new edit/compile/debug cycle, you may want to end debugging. In this case, you should switch the MCU back from debugWIRE mode to normal mode, in which SPI programming is possible. In order to achieve that, type `monitor debugwire disable` into the prompt line of the `Debug Console` before ending the last debug episode.
It may also be a good idea to disable the `Optimize for Debugging` flag in the `Sketch` menu.

If you want to restore your Uno to the original state, consult the section on "[Restoring the target](restore-original-state.md)."

### Potential problems

If the status LED of dw-link starts to blink furiously, then the hardware debugger has hit an unrecoverable error. Typing `monitor info` into the input field of the GDB debugger can then help you find out about the error number, which is decoded in the [Troubleshooting](troubleshooting.md#internal-and-fatal-dw-link-errors) section.
It may also be a good idea to consult the [Limitations](limitations.md) section.

