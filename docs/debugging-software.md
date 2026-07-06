# Installing & configuring the debugging software

In addition to PyAvrOCD, you need an IDE, a debug GUI, or the stand-alone GDB client.

## Arduino IDE 2

[Arduino IDE 2](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing/) is probably the most straightforward option. After having installed
it, you can extend the IDE's capabilities by adding third-party
packages in the `Additional Board Manager URLs` field of the
`Preferences` dialog. The set of available debug-enabled Arduino packages and how
to install them is covered in the [section on Arduino packages](supporting-packages.md).

## PlatformIO and Visual Studio Code

[PlatformIO](https://platformio.org) is a cross-platform, cross-architecture, multiple-framework tool for embedded
system development. It can be installed as an extension to Visual Studio Code, which provides a powerful IDE for embedded programming and debugging. By using project-specific`platformio.ini` files, integrating PyAvrOCD is straightforward by employing a forked platform:

```
[env:...]
platform = https://github.com/felias-fogg/platform-atmelavr.git
...
```

For the modern parts, there is no supporting fork yet, but it will be added real soon.

## Other IDEs

There are a few other possible options for IDEs. I believe it should be possible to integrate PyAvrOCD into  [**CLion**](https://www.jetbrains.com/clion/) and [**Eclipse**](https://eclipseide.org/projects/). How to integrate an AVR-GDB server into CLion is, for example, described [here](https://bloom.oscillate.io/docs/clion-debugging-setup).

If you have a clear description of how to integrate PyAvrOCD in an IDE, I'd be happy to add it here.

## A debug GUI: Gede

[Gede](https://github.com/jhn98032/gede) is a lean and clean GUI for GDB. It can be built and run on almost all Linux distros, FreeBSD, and macOS. You need an AVR-GDB client with a version of 10.2 or higher. If you have installed Gede somewhere in your PATH, PyAvrOCD will start Gede in the background if you specify the option `--start gede` when invoking PyAvrOCD. Configuring Gede is done when you [start the GUI](debugging.md#debugging-using-gede).

## CLI debugging

The most basic option is simply to install avr-gdb, the GDB debugger for AVR chips. You can use the version shipped with the PyAvrOCD binaries, which contains a few important patches for AVR MCUs.

It is not necessary to configure anything when you use
avr-gdb. However, I find it very helpful to have the few commands in the global initialization file `.gdbinit`.

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

The software simulator `simavr` is included in the Arduino IDE 2 tools and in the binary package. If you have installed PyAvrOCD differently, you need to install the simulator first. You can either download a binary from the latest [Github Actions CI](https://github.com/buserror/simavr/actions), you can build it from source, or, under macOS, use Homebrew.

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
