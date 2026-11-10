# Installing & configuring the debugging software

In addition to PyAvrOCD, you need an IDE, a debug GUI, or the stand-alone GDB client.

## Arduino IDE 2

After having installed [Arduino IDE 2](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing/), you can extend the IDE's capabilities by adding third-party packages in the `Additional Board Manager URLs` field of the `Preferences` dialog. The set of available debug-enabled Arduino packages and how to install them is covered in the [section on Arduino packages](supporting-packages.md).

## Arduino Maker Workshop

First, [Visual Studio Code](https://code.visualstudio.com) has to be installed. In addition to the Visual Studio Code extension [Arduino Maker Workshop](https://marketplace.visualstudio.com/items?itemName=TheLastOutpostWorkshop.arduino-maker-workshop), one needs to add the [Cortex-Debug](https://marketplace.visualstudio.com/items?itemName=marus25.cortex-debug) extension. In order to debug a particular MCU, install the right board packages from the [Arduino packages list](supporting-packages.md).

## PlatformIO and Visual Studio Code

You need to install [Visual Studio Code](https://code.visualstudio.com) and the Visual Studio Code extension [PlatformIO](https://platformio.org). By using project-specific `platformio.ini` files, integrating PyAvrOCD is straightforward. You simply need to  specify the debug-enabled platform for the Atmel AVR family:

```
[env:...]
platform = https://github.com/felias-fogg/platform-atmelavr.git
...
```

This debug-enabled platform fork has already the right `debug_server` command with all the right parameters and contains the `debug_init_cmds` setting up a GDB session with PyAvrOCD. If you want to change something in these settings, you should check the original settings in `~/.platformio/platforms/atmelavr/platform.py`.

A complete platformio.ini file for an ATtiny85 project when using the [dw-link debug probe](https://github.com/felias-fogg/dw-link) could look las follows:

```
[platformio]
default_envs = debug

[env:attiny85]
platform = https://github.com/felias-fogg/platform-atmelavr.git
framework = arduino
board = ATtiny85
board_build.mcu = attiny85
board_build.f_cpu = 800000L

[env:debug]
extends = env:attiny85
build_type = debug
debug_tool = pyavrocd

[env:release]
extends = env:attiny85
build_type = release
build_flags =
  -DNDEBUG
upload_protocol = jtag2isp          ; protocol for dw-link
upload_port = SERIALPORT            ; Define your serial port here or use VSC command
upload_speed = 19200
```

The following repos provide example projects with `platformio.ini` files for different MCUs and debug probes:

```
https://github.com/felias-fogg/pio-attiny85-example
https://github.com/felias-fogg/pio-atmega328p-example
https://github.com/felias-fogg/pio-atmega1284p-example
```

For the modern parts, i.e., UPDI targets, there is no supporting fork yet, but it will be added real soon.

## PlatformIO and CLion

Similar to Visual Studio Code, you can install a PlatfromIO plugin that exposes the most important PlatformIO commands in CLion. After you have installed CLion, follow the instructions of the [CLion documentation](https://www.jetbrains.com/help/clion/platformio.html) for installing PlatformIO. Then you can use the way described above in order to use the debug-enabled fork of the platform package.

## A debug GUI: Gede

[Gede](https://github.com/jhn98032/gede) is a lean and clean GUI for GDB. It can be built from source and run on almost all Linux distros, FreeBSD, and macOS. You need an AVR-GDB client with a version of 10.2 or higher. A better choice is the client shipped together with PyAvrOCD. If you have installed Gede somewhere in your PATH, PyAvrOCD will start Gede in the background if you specify the option `--start gede` when invoking PyAvrOCD. Configuring Gede is done when you [start the GUI](debugging.md#debugging-using-gede).

## CLI debugging

The most basic option is simply to install avr-gdb, the GDB debugger for AVR chips. You can use the version shipped with the PyAvrOCD binaries, which contains a few important patches for AVR MCUs.

It is not necessary to configure anything when you use avr-gdb. However, I find it very helpful to have a few commands in the global initialization file `.gdbinit`.

<details>
<summary><b>A .gdbinit example</b></summary>
<pre>
<code class="language-text hljs">define hook-quit
    set confirm off
end
set history save on
set history size 10000
set history filename ~/.gdb_history
set logging overwrite 1</code>
</pre>
</details>
<p></p>

## A software simulator: simavr

The software simulator `simavr` is included in the Arduino IDE 2 tools and in the binary package. If you have installed PyAvrOCD differently, you need to install the simulator separately. You can either download a binary from the latest [GitHub Actions CI](https://github.com/buserror/simavr/actions), you can build it from source, or, under macOS, use Homebrew.

<details>
<summary><b>How to build simavr from source</b></summary>
<p></p>
<p>
If you want or need to build simavr from source, clone or download the
<a href="https://github.com/buserror/simavr">simavr GitHub repo</a> and make sure that you have avr-gcc, avr-libc, libelf-dev, and freeglut installed (using your preferred package managers). Then call <code>make</code>, perhaps with the DESTDIR argument:
</p>
<pre>
<code class="language-bash hljs">make install DESTDIR=~/.local/</code>
</pre>
</details>



<p></p>
