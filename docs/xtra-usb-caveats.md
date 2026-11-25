# Debugging sketches that use the MCU's own USB

Boards like the Arduino Leonardo or the Micro have no separate USB chip: the ATmega32U4 itself is the USB device, and the sketch -- with the help of the Arduino core -- provides the USB function, be it a serial port (CDC), a keyboard or mouse (HID), or something like a debug probe. Such sketches can be debugged, and stops in `loop()` are usually harmless. There are a few places, however, where one has to be careful.

What follows is derived from the USB specification and the ATmega32U4 datasheet. The basic behaviour -- stops in `loop()` work, a breakpoint at the beginning of `setup()` lets the USB enumeration fail -- has been observed on a Leonardo; the rest has not been tested systematically.

## Why a stopped MCU usually does no harm

The USB controller of the ATmega32U4 does much of its work in hardware, independently of the CPU. When the host sends data to an endpoint whose buffer the firmware has not emptied, or asks for data the firmware has not provided yet, the controller answers with *NAK* ("not ready yet"). For the *bulk* and *interrupt* endpoints, which carry the data of CDC and HID, this is a perfectly normal state: the host keeps asking for as long as it takes and does not drop the device. Start-of-frame packets and the electrical presence on the bus are handled by the hardware as well.

What the firmware has to answer itself are *control transfers* on endpoint 0. The hardware only acknowledges the receipt of the request; the answer has to come from the code, and the host waits only a few seconds (about 5 s on common operating systems). This is where all of the problems below come from.

## Caveats for all USB sketches

- **No breakpoints during enumeration.** The Arduino core attaches the device to the bus in `main()`, before `setup()` is called, and from then on the host enumerates it with a series of control transfers (descriptors, address, configuration). A breakpoint at the beginning of `setup()` stops the CPU in exactly this phase, the requests time out, and the host reports the device as failed. If a breakpoint early in `setup()` is needed, delay the program for a second or two first, or accept that USB will not be available in this debug session.
- **The bootloader is erased.** When debugging over JTAG, PyAvrOCD erases the chip before loading (the default *erase before load*) and, with `-m bootrst`, unprograms BOOTRST. This removes the USB bootloader (Caterina on the Leonardo). Uploading over USB is then no longer possible until the bootloader has been burned again.
- **A0 to A3 are the JTAG pins.** On the ATmega32U4, PF4 to PF7 serve as TCK, TMS, TDO and TDI. While debugging over JTAG, they cannot be used as analog inputs or digital I/O.
- **No 1200 bps reset while stopped.** The "touch at 1200 bps", which makes the board enter its bootloader, is handled by the firmware. This does not matter while debugging, since the program is loaded over JTAG anyway.

## Caveats for the serial port (CDC)

- **Sending data while stopped is safe.** Characters sent from the serial monitor over an already open connection are bulk transfers. The MCU's USB hardware answers NAK, the host's driver keeps the data and tries again, and once the program runs again, the characters arrive. Only a program on the host that gives up writing after a timeout of its own may report an error during a long stop.
- **Opening, closing and reconfiguring the port fails while stopped.** Opening or closing the serial monitor and changing the baud rate are control transfers (SET_LINE_CODING, SET_CONTROL_LINE_STATE), which the sketch has to answer. While the MCU is stopped, they time out: the port cannot be opened, or the operating system reports an error. So open the serial monitor before stopping, and leave it alone while the program is stopped.

## Caveats for keyboards, mice and other HID devices

- **Stuck keys and buttons.** This is the one that can do real damage. If the sketch has sent a "key down" report and the CPU stops before the "key up" report, the host considers the key to be held down -- and its auto-repeat types the key over and over into whatever window has the focus, quite possibly the editor of the IDE. The same holds for a pressed mouse button, which the host takes for a drag. So do not stop the program between `Keyboard.press()` and `Keyboard.release()` (or between `Mouse.press()` and `Mouse.release()`), and do not set breakpoints there. `Keyboard.write()` sends both reports in direct succession and is less exposed.
- **Keyboard LEDs.** The operating system sets the Caps, Num and Scroll Lock LEDs on all keyboards, often by a control transfer (SET_REPORT). Pressing Caps Lock on the real keyboard while the Leonardo is stopped makes this request time out; depending on the operating system, this ends in an error message or, in the worst case, in the host resetting the device.
- **HID reports themselves are harmless.** HID data travels over interrupt endpoints, which the host polls; a stopped MCU just answers that there is no new report, and the device stays present.
- **A host program waiting for an answer.** If the sketch implements a device that a program on the host talks to -- for example, a debug probe firmware such as mEDBG, which speaks CMSIS-DAP over HID -- that program sends a command and waits for the answer, which does not come while the MCU is stopped. Whether that is harmless depends on the host program: avrdude gives up after its timeout, whereas a program that reads without a timeout simply waits until the MCU runs again.

A sketch that combines CDC and HID -- the Arduino core does that by default when the Keyboard or Mouse library is used -- is subject to all of the above.
