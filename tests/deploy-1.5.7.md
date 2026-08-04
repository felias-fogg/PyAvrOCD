## Deployment tests

What tests to run before a new release is published?

- [ ] 1. Before producing binaries, running tests on Mac:

     - dw-link + ATtiny85:
   - [x] Erase
     - [x] Upload blink with avrdude
     - [x] Run e2e tests
     - SNAP + ATtiny2313:
   - [x] Erase
     - [x] Upload blink
   - [x] e2e
     - SNAP + Mega128 (Olimex, 12V!!!):
     - [x] e2e
     - Atmel-ICE + UNO: e2e
   - [x] Erase
     - [x] Upload Blink
   - [x] e2e
     - Atmel-ICE + ATmega16
   - [x] e2e
     
   - ATmega324PB XPlained Pro
          - [x] e2e
     - UNO Wifi Rev2
     - [x] e2e
   - Curiosity 3227
     - [ ] e2e

     Curiosity AVR128DA48

     - [x] e2e

- [ ] 2. Before producing binaries, test on platforms (pulling from GitHub and installing avr-gdb)

     - Mac/Windows under Parallels

     - [ ] dw-link + ATtiny861
          - [ ] Erase
          - [ ] Upload Blink
          - [ ] run e2e?
     - [ ] Curiosity ATmega4809
          - [ ] e2e?

     - Raspi/Trixie

     - [ ] dw-link + ATtiny861
          - [ ] Erase
          - [ ] Upload Blink
          - [ ] e2e
     - [ ] Curiosity AVR128DB48

     - Prodesk/Linux

     - [ ] dw-link + ATtiny861
          - [ ] Erase
          - [ ] Upload Blink
          - [ ] e2e
     - [ ] XNano416
          - [ ] e2e

- [ ] 3. After generating new release candidate and generating pre-screen downloads

     - Mac

     - [ ] Arduino IDE 2 + PlatformIO
          - [ ] dw-link + ATtiny1634
               - [ ] Upload Blink
               - [ ] Debug vblink
          - [ ] XMini328
               - [ ] Upload Blink
               - [ ] Debug vblink
          - [ ] Atmel-ICE + ATmega2560
               - [ ] Debug vblink
          - [ ] UNO Wifi Rev2
               - [ ] Debug vblink
          - [ ] Curiosity AVR128DB48
               - [ ] Debug vblink

     - Prodesk/Windows

     - [ ] Arduino IDE 2 + PlatformIO
          - [ ] dw-link + ATtiny1634
          - [ ] Curiosity AVR128DB48

     - Prodesk/Linux

     - [ ] Arduino IDE 2 + PlatformIO
          - [ ] dw-link + ATtiny1634
          - [ ] Curiosity AVR128DB48