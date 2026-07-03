### Step 1: Installing an alternative platform

Setup a PlatformIO project and instead of using `atmelavr` as the platform, specify the following in your `platformio.ini` configuration file:

```
[platformio]

[env:atmega1284p]
platform = https://github.com/felias-fogg/platform-atmelavr.git
framework = arduino
board = ATmega1284P
upload_flags = -e
board_upload.require_upload_port = false
```

This will pull in:

- The new AVR-GCC 15.1 toolchain
- and PyAvrOCD.
