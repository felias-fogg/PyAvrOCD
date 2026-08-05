## Deployment tests

What tests to run before a new release is published?

- 1. Before producing binaries, running tests on **Mac**:

     - dw-link + ATtiny85:
       - [x] Run e2e tests
       - [x] Upload blink with avrdude
       - [x] Erase
     - SNAP + ATtiny2313:
       - [x] e2e
       - [x] Upload blink
       - [x] Erase
     - SNAP + Mega128 (Olimex, 12V!!!):
       - [x] e2e
     - Atmel-ICE + UNO: e2e
       - [x] e2e
       - [x] Upload Blink
       - [x] Erase
     - Atmel-ICE + ATmega16
       - [x] e2e
     - ATmega324PB XPlained Pro
       - [x] e2e
     - UNO Wifi Rev2
       - [x] e2e
     - Curiosity 3217
       - [x] e2e
     - Curiosity AVR128DA48
       - [x] e2e
- 2. Before producing binaries, test on platforms (pulling from GitHub and installing avr-gdb) on **Raspi/Trixie** (Poetry got stuck, use PyPi)
     - dw-link + ATtiny861
          - [x] Erase
          - [x] Upload Blink
          - [x] e2e
     - Curiosity AVR128DA48
          - [x] e2e
- [ ] 3. After generating new release candidate and generating pre-screen downloads
     - **Mac**

          - Arduino IDE 2 + PlatformIO
             - XMini328P
                - [x] Upload Blink
                - [x] Debug vblink
             - ATtiny85
                - [x] Upload Blink
                - [x] Debug blink
     - **Prodesk/Windows**

          - Arduino IDE 2 + PlatformIO
             - dw-link + ATtiny85
                - [x] Upload Blink
                - [x] Debug vblink
            - Atmel-ICE + ATmega328P
                - [x] Upload Blink
                - [x] Debug vblink
     - **Prodesk/Linux**

          - Arduino IDE 2 + PlatformIO
              - Atmel-ICE + ATmega328P
                - [ ] Upload Blink
                - [ ] Debug vblink
              -  dw-link + ATtiny85
                - [ ] Upload Blink
                - [ ] Debug blink