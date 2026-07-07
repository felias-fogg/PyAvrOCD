# Supported IDEs

The IDEs listed below are explicitly supported by PyAvrOCD. There exist extensions and/or forks of Arduino packages and PlatformIO packages that integrate PyAvrOCD into these IDEs. With a bit of effort, it should be possible to make PyAvrOCD available in other IDEs as well.

## Arduino IDE 2

[Arduino IDE 2](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing/) is probably the most straightforward option. In contrast to the deprecated Arduino IDE, debugging is supported by making use of an early version of the Visual Studio Code extension Cortex-Debug. The design principle behind Arduino IDE 2 is not to overwhelm beginners with a multitude of options and interaction elements. This comes at a cost, however. One is often constrained in what is possible. If one wants to be more flexible, then it is possible to employ **Arduino-cli**, the command-line interface to the Arduino processor, which exposes somewhat more functionality to the user.

PyAvrOCD has been integrated into Arduino IDE 2 by extending the `platform.txt`  configuration files of Arduino hardware packages. In order to configure Cortex-Debug, a number of attributes of the form `debug.cortex-debug.custom` and a few other variables had to be set in the `platform.txt` file.

## Arduino Maker Workshop

[Arduino Maker Workshop](https://marketplace.visualstudio.com/items?itemName=TheLastOutpostWorkshop.arduino-maker-workshop) is a Visual Studio Code extension that provides a very convenient interface to the Arduino CLI. It feels very similar to the Arduino IDE2 but offers more freedom. One can add the [Cortex-Debug](https://marketplace.visualstudio.com/items?itemName=marus25.cortex-debug) extension, resulting in a very smooth IDE. Because the Cortex-Debug version from the VSCode marketplace is much more recent than the one employed in the Arduino IDE 2, debugging is much better. The UI is more streamlined and assembly-level debugging is supported. 

On the negative side, there is no `Burn Bootloader` button or command yet. Further, each Arduino hardware package needs an additional small modification to generate the `launch.json` files that are needed to configure Cortex-Debug. 

The integration of PyAvrOCD in the form of generating the `launch.json` files is implemented by shell scripts and Windows batch files. These are parametrized and invoked by the hook `recipe.hooks.sketch.prebuild.1.pattern` defined in `platform.txt`.

## PlatformIO and Visual Studio Code

[PlatformIO](https://platformio.org) is a cross-platform, cross-architecture, multiple-framework tool for embedded
system development. It can be installed as an extension to Visual Studio Code, which provides a powerful IDE for embedded programming and debugging. 

The debugging UI is not Cortex-Debug. Assembly-level debugging is not possible. Further, the peripheral register display is somewhat buggy, sometimes not displaying the values of the inspected registers.

Integration of PyAvrOCD is implemented in a fork of the MCU-family-specific platform, which needs to be specified in the project configuration file `platformio.ini`. 
