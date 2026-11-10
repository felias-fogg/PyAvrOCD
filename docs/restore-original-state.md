# Restoring a target to its original state after debugging

If, after debugging, you want to restore a target board to its original state, a few things have to be done:

1. If your target is a debugWIRE MCU, then you need to disable debugWIRE mode. This can be done by entering the debugger and then issuing the `monitor debugwire disable` command.
2. You need to undo the physical changes you have made to the board. This may be to restore a solder bridge (or solder a header in its place). Alternatively, you may need to solder a capacitor again or reconnect a reset circuit. My advice is not to do that, but mark the board instead for *debug use* only.  In this case, you can ignore step 3.
3. You may need to reflash the *bootloader*, if initially present, and likely need to set the correct *fuses*.
      - To restore the board to its exact original state before debugging, you must get hold of the bootloader and record the fuses before initiating the debugging process. Then you can easily restore the original state using a programmer.
      - In the Arduino IDE, you can do this by using the `Burn Bootloader` command in the `Tools` menu. This will set the correct fuses and reinstall the bootloader (if needed). Note that if you want only to set the fuses without installing a bootloader, you still have to use the `Burn Bootloader` command.

!!! info "Use dw-link as a programmer"
    You can use dw-link as a programmer. Select as the `Port` in the `Tools` menu the serial connection to dw-link and choose `dw-link` as the `Programmer`. Now you can upload programs and burn bootloaders and fuses.

!!! warning "Burning the bootloader using the Arduino AVR Boards package"
    If you have debugged a board using, e.g., `MiniCore`, and now want to restore an Uno R3 board to its previous state under the`Arduino AVR Boards` package as an `Arduino Uno`, you may encounter problems when using one of the Microchip debug probes. Use a cheap USBasp programmer or something similar instead for burning the boot loader. Alternatively, you may consider staying with MiniCore and employing [Urboot](https://github.com/stefanrueger/urboot) as the bootloader.

!!! warning "Burning the bootloader when there are many user-selectable options"
    If you have debugged a target for which the `Tools` menu offers many different options, make sure that all relevant options have the correct value before you use the `Burn Bootloader` command. In particular, make sure that the right `Clock` value is selected! Otherwise, it can happen that you need to apply an external clock to reanimate your chip.

