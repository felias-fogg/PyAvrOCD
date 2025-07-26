# Debugging software

There are several possible options for debugging software.

## CLI debugging

The most basic option is simply to install avr-gdb, the GDB debugger for AVR chips. You can use the version shipped with the pyavrocd binaries or the version already installed on your system. If avr-gdb is not installed, use your preferred package manager on Linux, Homebrew on macOS, or download a version from Zak's [avr-gcc-build](https://github.com/ZakKemble/avr-gcc-build) repository. This is particularly useful when you want to run debugging software on a 32-bit system.

If you are not a fan of a command-line interface, then an integrated development environment (IDE) or a simple graphical user interface (GUI) for avr-gdb is called for.

## Arduino IDE 2

[Arduino IDE 2](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing/) is probably the most straightforward option. After installing it, you can extend the IDE's capabilities by [adding third-party platforms](https://support.arduino.cc/hc/en-us/articles/360016466340-Add-third-party-platforms-to-the-Boards-Manager-in-Arduino-IDE). This is done by adding [additional Board Manager URLs](https://support.arduino.cc/hc/en-us/articles/360016466340-Add-third-party-platforms-to-the-Boards-Manager-in-Arduino-IDE) in the preferences dialog and selecting a board in the Board Manager. For example, adding the following three Board Manager URLs enables debugging of almost all debugWIRE MCUs.

```
https://felias-fogg.github.io/ATTinyCore/package_drazzy.com_ATTinyCore_index.json
https://mcudude.github.io/MicroCore/package_MCUdude_MicroCore_index.json
https://mcudude.github.io/MiniCore/package_MCUdude_MiniCore_index.json
```

After that, you must install the respective cores, which enable you to debug almost all classic AVR chips that use the debugWIRE interface. And this is all! Now, you can press the debug button and start debugging.

Linux users may need to add a few udev rules. When you first start the Arduino IDE debugger and the hardware debuggers are not recognized, a hint appears in the gdb-server window on how to set the udev rules. You simply need to execute pyavrocd once as root using the command-line option `--install-udev-rules`. Instead, you can create a udev-rules file along the lines described in the [README file of pyedbglib](https://github.com/microchip-pic-avr-tools/pyedbglib/blob/main/README.md).

## PlatformIO and Visual Studio Code

[PlatformIO](https://platformio.org) is a cross-platform, cross-architecture, multiple framework professional tool for embedded systems engineers. Installed as an extension to the popular Visual Studio Code, it provides a powerful IDE for embedded programming and debugging. Using the `platformio.ini` file, integrating an external debugging framework is very easy. If you want to debug a program on an ATmega328P, the `platformio.ini` file could look as follows (see also the `example` folder)

```
[platformio]
default_envs = debug

[env:atmega328p]
platform = atmelavr
framework = arduino
board = ATmega328P
board_build.f_cpu = 16000000L
board_hardware.oscillator = external

[env:debug]
extends = env:atmega328p          ;; <--- substitute the right board here
build_type = debug
debug_tool = custom
debug_server = /path/to/pyavrocd  ;; <-- specify path to gdbserver
    --port=3333
    --device=${env:debug.board}
debug_init_cmds =
    define pio_reset_halt_target
         monitor reset
    end
    define pio_reset_run_target
         monitor reset
	       continue
    end
    target remote $DEBUG_PORT
    monitor debugwire enable
    $LOAD_CMDS
    $INIT_BREAK
debug_build_flags =
    -Og
    -ggdb3
```

Note that the debug environment should be the default one. It should be the first if no default environment has been declared.

I further noticed that the avr-gdb debugger in the PlatformIO toolchain is quite dated and does not start (e.g., under Ubuntu 24.04 and macOS 15.5). Simply replace it with a more recent version from your system or use the version shipped with the pyavrocd binary . The location where PlatformIO stores its copy of avr-gdb is `~/.platformio/packages/toolchain-atmelavr/` , where the tilde symbol signifies the home directory of the user.

## Gede

[Gede](https://github.com/jhn98032/gede) is a lean and clean GUI for GDB. It can be built and run on almost all Linux distros, FreeBSD, and macOS. You need an avr-gdb client with a version of 10.2 or higher. If you have installed Gede somewhere in your PATH, you can start it by specifying the option `--gede` or `-g` when starting pyavrocd.

## Other options

There are a few other possible options. The most crucial point is that remote debugging and the specification of alternative debuggers are supported. I believe it should be possible to integrate pyavrocd into **Visual Studio Code**, **CLion**, and **Eclipse**. How to integrate a GDB server into CLion is, for example, described [here](https://bloom.oscillate.io/docs/clion-debugging-setup).

If you have a clear description of how to integrate pyavrocd in an IDE, I'd be happy to add it here.

------

[<small><i>Back to pyavrocd README</i></small>](https://github.com/felias-fogg/pyavrocd/blob/main/README.md)

