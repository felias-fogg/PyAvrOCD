# Supported IDEs

There are some IDEs that are explicitly supported by PyAvrOCD. With a bit of effort, it is possible to make PyAvrOCD available in other IDEs as well.

## IDEs supported by board or platform  packages

There exist extensions and/or forks of Arduino packages and PlatformIO packages that integrate PyAvrOCD into the following three IDEs.

### Arduino IDE 2

[Arduino IDE 2](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing/) is probably the most straightforward option. In contrast to the deprecated Arduino IDE, debugging is supported by making use of an early version of the Visual Studio Code extension Cortex-Debug. The design principle behind Arduino IDE 2 is not to overwhelm beginners with a multitude of options and interaction elements. This comes at a cost, however. One is often constrained in what is possible. If one wants to be more flexible, then it is possible to employ **Arduino-cli**, the command-line interface to the Arduino processor, which exposes somewhat more functionality to the user.

PyAvrOCD has been integrated into Arduino IDE 2 by extending the `platform.txt`  configuration files of Arduino hardware packages. In order to configure Cortex-Debug, a number of attributes of the form `debug.cortex-debug.custom` and a few other attributes had to be set in the `platform.txt` file.

### Arduino Maker Workshop

[Arduino Maker Workshop](https://marketplace.visualstudio.com/items?itemName=TheLastOutpostWorkshop.arduino-maker-workshop) is a Visual Studio Code extension that provides a very convenient interface to the Arduino CLI. It feels very similar to the Arduino IDE2 but offers everything VSC has, e.g., AI support. One can add the [Cortex-Debug](https://marketplace.visualstudio.com/items?itemName=marus25.cortex-debug) extension, resulting in a very smooth IDE. Because the Cortex-Debug version from the VSCode marketplace is much more recent than the one employed in the Arduino IDE 2, debugging is much better. The UI is more streamlined, and assembly-level debugging is supported.

The integration is implemented the same way as with Arduino IDE 2, i.e., via `platform.txt`.

### PlatformIO and Visual Studio Code

[PlatformIO](https://platformio.org) is a cross-platform, cross-architecture, multiple-framework tool for embedded
system development. It can be installed as an extension to [Visual Studio Code](https://code.visualstudio.com), providing you with a powerful IDE for embedded programming and debugging.

The debugging UI is not Cortex-Debug. Assembly code can be displayed, but assembly-level debugging is not possible. Further, the peripheral register display is somewhat buggy, sometimes not displaying the values of the inspected registers.

Integration of PyAvrOCD is implemented in a fork of the MCU-family-specific platform, which needs to be specified in the project configuration file `platformio.ini`.

### PlatformIO and CLion

The IDE [CLion](https://www.jetbrains.com/clion/)[^*] by JetBrains is compatible with PlatformIO as well.  After the installation of PlatformIO inside CLion, everything works out of the box. In particular, the display of peripheral registers and assembly-level debugging work like a charm.

## IDEs compatible with PyAvrOCD

There exists a number of IDEs and/or frameworks that can (probably) be convinced to cooperate with PyAvrOCD.  However, a bit of manual work is necessary.

### Eclipse

It should be possible to develop and debug Software for AVR chips using Eclipse/CDT. And I found a recent, very detailed description of how to configure Eclipse: [**Programming AVRs with Eclipse**](https://androidexperto.com/programming-avrs-with-eclipse/). I have not tested it and would be interested to hear back from you if you are successful in teaching Eclipse how to use PyAvrOCD.



[^*]: In 2025, NetBrains started to offer a free license for non-commercial use of CLion. Additionally, there is also a free educational license.

