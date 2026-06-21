## Quickstart: SNAP & ATtiny85

This quickstart guide demonstrates how to use the Arduino IDE 2 for debugging on an ATtiny85 using the MPLAB SNAP debug probe.


### Required hardware

* SNAP
* USB cable
* ATtiny85 (or any other classic ATtiny or ATmegaX8) as the *target*
* In order to set up the target, you need:
    * a breadboard together with
    * jumper wires (male-to-male)
    * 1 LED
    * 2 resistors (10 kΩ, 1kΩ)
    * 1 capacitor (100 nF)

### Step 1: Install the debug-enabled TinyCore package

Add a new *boards manager URL* in the `Preferences` dialog:

	https://mcudude.github.io/TinyCore/package_MCUdude_TinyCore_index.json
{!details-boards-manager-url.md!}

Next, you have to install the new package. Activate the `Boards Manager`, select `TinyCore`, and click on `Install`.

{!details-install-package.md!}

!!! info "Linux systems"
    After the installation, users of Linux systems will need to add `udev` rules. Download [https://pyavrocd.io/99-edbg-debuggers.rules](https://pyavrocd.io/99-edbg-debuggers.rules), edit if you want, and copy to `/etc/udev/rules.d/`.

### Step 2: Connect the target with the debug probe

You need to set up the hardware on a breadboard and use a few jumper wires to connect the ATtiny to the debug probe. Further, as is obvious from the Fritzing sketch, you need an external power supply. Note that the notch or dot on the ATtiny is oriented towards the left.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/snap+attiny85.png" width="80%">
</p>


<details>
<summary><b>Table of breadboard connections</b></summary>
<p></p>
<p>You can use this table to check whether you have made all the connections.</p>
<table>
<thead>
<tr>
<th>ATtiny pin</th>
<th>SNAP pin</th>
<th>component</th>
</tr>
</thead>
<tbody>
<tr>
<td>#1 (Reset)</td>
<td>TAUX #6</td>
<td>10 kΩ resistor to Vcc</td>
</tr>
<tr>
<td>#2 (D3)</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>#3 (D4)</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>#4 (GND)</td>
<td>GND #3</td>
<td>GND on breadboard, LED (-), decoupling cap 100 nF</td>
</tr>
<tr>
<td>#5 (D0, MOSI)</td>
<td>TTDI #7</td>
<td></td>
</tr>
<tr>
<td>#6 (D1, MISO)</td>
<td>PGD #4</td>
<td></td>
</tr>
<tr>
<td>#7 (D2, SCK)</td>
<td>PGC #5</td>
<td>1 kΩ resistor to LED (+)</td>
</tr>
<tr>
<td>#8 (Vcc)</td>
<td>TVDD #2</td>
<td>Vcc on breadboard, 10k resistor, decoupling cap 100 nF</td>
</tr>
<tr>
<td></td>
<td></td>
<td>connect LED (+) and 1 kΩ resistor</td>
</tr>
</tbody>
</table>
<!--
| ATtiny pin    | SNAP pin | component                                              |
| ------------- | -------- | ------------------------------------------------------ |
| #1 (Reset)    | TAUX #6  | 10 kΩ resistor to Vcc                                  |
| #2 (D3)       | &nbsp;   | &nbsp;                                                 |
| #3 (D4)       | &nbsp;   | &nbsp;                                                 |
| #4 (GND)      | GND #3   | GND on breadboard, LED (-), decoupling cap 100 nF      |
| #5 (D0, MOSI) | TTDI #7  |                                                        |
| #6 (D1, MISO) | PGD #4   |                                                        |
| #7 (D2, SCK)  | PGC #5   | 1 kΩ resistor to LED (+)                               |
| #8 (Vcc)      | TVDD #2  | Vcc on breadboard, 10k resistor, decoupling cap 100 nF |
|               |          | connect LED (+) and 1 kΩ resistor                      |
-->

</details>
<p></p>

### Step 3: Load sketch and select board

Load a sketch, e.g., the `Blink` sketch, and select the right board: `Tools -> Board -> TinyCore -> ATtiny85`. If this is a chip is fresh from the factory, you need to adjust for the clock frequency. Choose `1 MHz internal osc.` under `Tools -> Clock`.

### Step 4: Compile the sketch

Activate `Optimize for Debugging` in the `Sketch` menu. This only needs to be done once. Then click on the `Verify` button (checkmark symbol) in the top bar. This will compile the sketch.

### Step 5: Start debugging

Now it is time to start debugging by clicking the `Debug` button (bug in front of a triangle) in the top bar. If the target MCU is not already in debugWIRE mode, the debugger will request 'power cycling'.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-attiny-power-cycle.png " width="90%"></p>

Power cycling means to remove the Vcc jumper cable and, after a few seconds, to reinsert it. After a while, the `DEBUG` pane should open.

### Step 6: Debug the sketch

You can now start and stop execution, inspect variables, set breakpoints, and the like (see section on [debugging](debugging.md)). Clicking on the red square in the top bar of the DEBUG pane will terminate the current debugging episode.

### Step 7: Start over or terminate the debugging session

After leaving the debugger, you can edit the sketch and start again at step 4. Note that you always have to recompile and restart the debugger before any changes you made to the sketch are effective.

Instead of starting a new edit/compile/debug cycle, you may want to end debugging. In this case, you should switch the MCU back from debugWIRE mode to normal mode, in which SPI programming is possible. In order to achieve that, type `monitor debugwire disable` into the prompt line of the `Debug Console` before ending the last debug episode. It may also be a good idea to disable the `Optimize for Debugging` flag in the `Sketch` menu.


### What can go wrong?

There is always the chance that something goes south, either debugging does not start at all, or something funny happens while debugging. If so, it is a good idea to have a look at the output in the `gdb-server` console. Messages with the prefix [CRITICAL] often tell what went wrong. It may also be a good idea to consult the [Troubleshooting](troubleshooting.md) and the [Limitations](limitations.md) sections.

