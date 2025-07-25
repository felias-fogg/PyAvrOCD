# Restoring a target to its original state after debugging

If, after debugging, you want to restore a target board to its original state, two things have to be done:

1. You need to undo the physical changes you have made to the board. This may be to restore a solder bridge (or solder a header in its place). Alternatively, you may need to solder a capacitor again or reconnect a reset circuit. My advice is not to do that, but mark the board instead for **debug use** only.  In this case, you can also ignore step 2. 

2. You may need to reflash the bootloader and likely need to set the correct fuses. 

   - In the Arduino IDE, you can do this by using the `Burn Bootloader` command in the `Tools` menu. This will set the correct fuses and reinstall the bootloader.
   - Note that when using MiniCore to debug an Arduino Uno, this means that the *urboot* bootloader is installed. In other words, you then need to use MiniCore whenever programming the UNO board (instead of the standard Arduino Uno board).

   If you want to restore the board to its exact state before debugging, you must download the bootloader and record the fuses before starting the debugging process. Then you can easily restore the original state.



------

[<small><i>Back to pyavrocd README</i></small>](https://github.com/felias-fogg/pyavrocd/blob/main/README.md)

