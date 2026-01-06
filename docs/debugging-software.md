# Installing & configuring the debugging software

The GDB server PyAvrOCD provides an interface to the debug probe on one side. The other side can be an IDE, a debug GUI, or the GDB debugger. Installation of the software is usually straightforward when you follow the instructions on the respective webpages, where you can download the software. In addition, we will also cover the [installation of a software simulator](#a-software-simulator-simavr).

## Arduino IDE 2

[Arduino IDE 2](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing/) is probably the most straightforward option. After having installed it, you can extend the IDE's capabilities by [adding third-party platforms](https://support.arduino.cc/hc/en-us/articles/360016466340-Add-third-party-platforms-to-the-Boards-Manager-in-Arduino-IDE). This is done by adding [additional Board Manager URLs](https://support.arduino.cc/hc/en-us/articles/360016466340-Add-third-party-platforms-to-the-Boards-Manager-in-Arduino-IDE) in the preferences dialog, installing a platform, and selecting a board in the Board Manager. For example, you can add the following `Board Manager URL` :

```
https://downloads.pyavrocd.io/package_debug_enabled_index.json
```

After that, you can install one of the platforms referred to in the index file, e.g., `ATTinyCore (Debug enabled)`, which is a fork of Spence Konde's  `ATTinyCore` platform. And this is all! Now, you can press the debug button and start debugging. Well, before you can do that, you must probably [modify the target board](board-preparation.md), and you need to [connect the debug probe to the target board](connect-to-target.md).

The set of available cores is covered in the [section on Arduino cores](supporting-cores.md).

## PlatformIO and Visual Studio Code

[PlatformIO](https://platformio.org) is a cross-platform, cross-architecture, multiple framework professional tool for embedded systems engineers. Installed as an extension to the popular Visual Studio Code, it provides a powerful IDE for embedded programming and debugging. Using the `platformio.ini` file, integrating an external debugging framework is very easy. If you want to debug a program on an ATmega328P, the `platformio.ini` file could look as follows. A more elaborate example can be found at [https://github.com/felias-fogg/pio-atmega1284p-example](https://github.com/felias-fogg/pio-atmega1284p-example).

```ini
[platformio]
default_envs = debug

[env:atmega328p]
platform = atmelavr
framework = arduino
board = ATmega328P
board_build.mcu = atmega328p
board_build.f_cpu = 16000000L
board_hardware.oscillator = external
build_unflags = -flto              ;; this makes sure we can watch the global vars

[env:debug]
extends = env:atmega328p          ;; <--- substitute the right board here
build_type = debug
debug_tool = custom
debug_server = /path/to/pyavrocd  ;; <-- specify path to gdbserver
    --port=3333
    --device=${this.board_build.mcu}
    --manage=all
debug_init_cmds =
    define pio_reset_halt_target
         monitor reset
    end
    define pio_reset_run_target
         monitor reset
         disconnect
    end
    target remote $DEBUG_PORT
    monitor debugwire enable
    $LOAD_CMDS
    $INIT_BREAK
debug_build_flags =
    -Og
    -ggdb3
    -DDEBUG
debug_svd_path = /path/to/svd-file ;; <-- specify path to SVD file
```

Note that debugging in the IDE can only start when the debug environment is made the current environment.

Recently, PyAvrOCD has been extended to [deal with *System View Description* files](https://arduino-craft-corner.de/index.php/2025/08/01/system-view-descriptions-of-avr-mcus/), which enable the IDE to view and manipulate I/O registers in a very comfortable way. In order to use this feature, you need to copy the right SVD file from the [SVD folder of the GitHub repo](https://github.com/felias-fogg/PyAvrOCD/tree/main/svd) to the PlatformIO project folder, or you can also access it in the `pyavrocd-util` folder, which is stored alongside `pyavrocd`. The SVD files are all stored in the directory `pyavrocd-util/svd`.

I noticed that the avr-gdb debugger in the PlatformIO toolchain is quite dated and does not start (e.g., under Ubuntu 24.04 and macOS 15.5). Simply replace it with a more recent version from your system or use the version shipped with the PyAvrOCD binary. The location where PlatformIO stores its copy of avr-gdb is `~/.platformio/packages/toolchain-atmelavr/`, where the tilde symbol signifies the home directory of the user.

## Other IDEs

There are a few other possible options for IDEs. The most crucial point is that remote debugging and the specification of alternative debuggers are supported. I believe it should be possible to integrate PyAvrOCD into  [**CLion**](https://www.jetbrains.com/clion/) and [**Eclipse**](https://eclipseide.org/projects/). How to integrate an AVR-GDB server into CLion is, for example, described [here](https://bloom.oscillate.io/docs/clion-debugging-setup). Integration into [**Visual Studio Code**](https://code.visualstudio.com) and **[Eclipse Theia](https://theia-ide.org)** should be straightforward because one could make use of the Visual Studio Code extension [cortex-debug](https://github.com/Marus/cortex-debug) that is also used in the Arduino IDE 2.

If you have a clear description of how to integrate PyAvrOCD in an IDE, I'd be happy to add it here.

## A debug GUI: Gede

[Gede](https://github.com/jhn98032/gede) is a lean and clean GUI for GDB. It can be built and run on almost all Linux distros, FreeBSD, and macOS. You need an AVR-GDB client with a version of 10.2 or higher. If you have installed Gede somewhere in your PATH, PyAvrOCD will start Gede in the background if you specify the option `--start gede` when invoking PyAvrOCD. Configuring Gede is done when you [start the GUI](debugging.md#debugging-using-gede).

## CLI debugging

The most basic option is simply to install avr-gdb, the GDB debugger for AVR chips. You can use the version shipped with the PyAvrOCD binaries or the version already installed on your system. If avr-gdb is not installed, use your preferred package manager on Linux, Homebrew on macOS, or download a version from Zak's [avr-gcc-build](https://github.com/ZakKemble/avr-gcc-build) repository. This is particularly useful when you want to run debugging software on a 32-bit system.

It is not necessary to configure anything when you use avr-gdb. However, I find it very helpful to have the following commands in the global initialization file `.gdbinit`, which has to be stored in the user directory:

```gdb
define hook-quit
    set confirm off
end
set history save on
set history size 10000
set history filename ~/.gdb_history
set logging overwrite 1
```

## A software simulator: simavr

The software simulator `simavr` is included in the Arduino IDE 2 tools and in the binary package. If you have installed PyAvrOCD differently, you need to install the simulator first. While the package managers under macOS and Linux offer the stable version 1.7, this release unfortunately does not play well with PyAvrOCD. You can either download a binary from the latest [Github Actions CI](https://github.com/buserror/simavr/actions) or you can build it from source.

If you want or need to build simavr from source, clone or download the [simavr GitHub repo](https://github.com/buserror/simavr) and make sure that you have avr-gcc, avr-libc, libelf-dev, and freeglut installed (using your preferred package managers). Then call `make`, perhaps with the DESTDIR argument:

```bash
make install DESTDIR=~/.local/
```

This works under macOS and Linux. The instructions in the repo provided for Windows appear to be outdated. For the Mac, one could alternatively build from source by using the following commands:

```
brew tap osx-cross/avr
brew install --HEAD simavr
```

