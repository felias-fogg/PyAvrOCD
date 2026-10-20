# Supported Simulator

In addition to debug probes, PyAvrOCD also supports the simulation tool [`simavr`](https://github.com/buserror/simavr) by providing a pass-through service. If you use the **Arduino IDE 2**, then the way to start the simulator is as follows:

1. Verify/compile your sketch.
2. Choose `Simulator (simavr)` as the `Programmer` in the `Tools` menu.
3. Click on the Debugger icon at the top of the window.

If you use the VSCode extension **Arduino Maker Workshop**, it works the same. In **PlatformIO**, you can select `simavr` as a debugging tool in the `platformio.ini` configuration file.

An alternative way to start `simavr` is to provide a path argument to the `--start` option that has as its last part `simavr`. If you use another IDE other than the ones mentioned above, you can trigger that by putting the file `pyavrocd.options` into the project folder containing the two lines

```text
--start
/path/to/simavr-executable
```

Note that the [list of chips supported by `simavr`](supported-mcus.md) is much smaller than the one supported by PyAvrOCD. Further, the means of interaction are severely limited. However, the simulator solution may sometimes be the more preferable option.

If you are adventurous, try out a few other things with `simavr`. It is possible to pass arguments to `simavr` using the option `--xarg` or `-x`. Note that each string must be passed separately as an argument, as in the example below. Use the `<option>=<value>` notation to pass options such as `--add-trace` in order to avoid the interpretation of these options as PyAvrOCD options.

For instance, you can trace the changes of a particular memory location, e.g., PORTB on an ATmega328P, where the built-in LED is usually controlled.  Add the following lines in the file `pyavrocd.options`:

```text
--xarg=--add-trace
--xarg='LED=trace@0x0025/0xff'
```

After terminating the debug session (and waiting some time), a [VCD](https://en.wikipedia.org/wiki/Value_change_dump) trace will show up in the project folder. This can be visualized, for instance, with [gtkwave](https://gtkwave.sourceforge.net) or [pulseview](https://sigrok.org/wiki/Downloads). It is also possible to provide VCD files as input. This is all sketched in a [simavr usage note](https://htmlpreview.github.io/?https://raw.githubusercontent.com/buserror/simavr/refs/heads/master/doc/Intro.html#using).

