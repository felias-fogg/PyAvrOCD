# No Display of Static Variable

In order to reproduce the error that static variables are not shown, do the following.



1. Create folder `static` and copy the attached Arduino program as `static.ino` into it.

2. Install **VS Code**.

3. Download and install **arduino-cli** somewhere in your PATH:

     ```
     https://arduino.github.io/arduino-cli/dev/installation/
     ```

4. Open VS Code and install the extension **Arduino Maker Workshop**: https://marketplace.visualstudio.com/items?itemName=TheLastOutpostWorkshop.arduino-maker-workshop

5. Install **Cortex-Debug**.

6. Install the **Microsoft C/C++ Extension Pack.**

7. Click on Arduino symbol in left side bar.

8. Choose `Boards Manager`, click on `Add URL` paste in the following URL and select

     ```
     https://mcudude.github.io/MiniCore/package_MCUdude_MiniCore_index.json
     ```

9. Click on `Not Installed`, type 'mini' into the search field and choose the `download` button to `install latest MiniCore`.

10. On the home window, click `Open Folder`, select the `static` folder from above.

11. Click again on the Arduino symbol and choose  `Maker Workshop Home`, and `Select your Board`

11. Choose MiniCore and then `Select a Board`: `ATmega328`
12. Now select the `Home` icon again and activate the two boxes `Use programmer for upload` and `Optimize compile output for debugging ...`
13. Select `Simulator (simavr)` as the programmer (this will choose the simulator as the target).
14. Click on `Compile` .
15. Click on `Generate Cortex-Debug Configuration` and `Start Generated Cortex-Debug` in succession.
16. This will start Cortex-Debug and by that the GDB server, the simulator, and GDB. Program execution will be stopped in `main`.
17. Open static.ino, set a breakpoint in the `loop` function, and continue execution.
18. There is no variable listed under the static category, although `ontime` and `_vary` should be shown here.
19. You can make global variables visible when recompiling the program with `LTO disabled` (set under board options).