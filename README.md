#  PyAvrOCD

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?logo=opensourceinitiative&logoColor=white)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/pyavrocd?logo=pypi&logoColor=white)](https://pypi.org/project/pyavrocd/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/pyavrocd?logo=pypi&period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=pypi+downloads)](https://pepy.tech/projects/pyavrocd)
[![PyPI Python Version](https://img.shields.io/pypi/pyversions/pyavrocd?logo=python&logoColor=white)](https://pypi.org/project/pyavrocd/)
![Static Badge](https://img.shields.io/badge/%3A%20my%5Bpy%5D-checked-blue?logo=python&logoColor=white)
![Pylint badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/felias-fogg/c0d539e3ad0d10252d2aab8ad325246a/raw/pylint.json)
![Pytest badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/felias-fogg/c0d539e3ad0d10252d2aab8ad325246a/raw/pytest.json)
![Coverage badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/felias-fogg/c0d539e3ad0d10252d2aab8ad325246a/raw/pycoverage.json&maxAge=30)
[![Release workflow](https://github.com/felias-fogg/PyAvrOCD/actions/workflows/release.yml/badge.svg)](https://github.com/felias-fogg/PyAvrOCD/actions/workflows/release.yml)
[![Commits since latest](https://img.shields.io/github/commits-since/felias-fogg/PyAvrOCD/latest?include_prereleases&logo=github)](https://github.com/felias-fogg/PyAvrOCD/commits/main)
[![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-raw/felias-fogg/PyAvrOCD?color=blue&logo=github)](https://github.com/felias-fogg/PyAvrOCD/issues?q=is%3Aissue%20state%3Aopen)
[![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-closed-raw/felias-fogg/PyAvrOCD?color=blue&logo=github)](https://github.com/felias-fogg/PyAvrOCD/issues?q=is%3Aissue%20state%3Aclosed)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/felias-fogg/PyAvrOCD/total?style=flat&label=github%20downloads&color=blue&logo=github)
![Hit Counter](https://visitor-badge.laobi.icu/badge?page_id=felias-fogg_PyAvrOCD)

<p align="center">
  <a href="https://felias-fogg.github.io/PyAvrOCD/index.html"><img src="https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/logo-small.png" width="15%"></a>
</p>


PyAvrOCD is a GDB server for 8-bit AVR MCUs (see [list of supported MCUs](https://felias-fogg.github.io/PyAvrOCD/supported-mcus/) and [supported boards](https://felias-fogg.github.io/PyAvrOCD/supported-boards/)),  communicating with Microchip's EDBG-based debug probes, e.g., [MPLAB Snap](https://www.microchip.com/en-us/development-tool/pg164100). So, is it simply [another open-source GDB server for AVR MCUs](https://arduino-craft-corner.de/index.php/2026/02/10/pyavrocd-1-0-0-released/#what-are-alternatives-to-pyavrocd)? No! It is a *cross-platform* AVR GDB server that can easily be packaged with the [Arduino IDE 2](https://www.arduino.cc/en/software/) and [PlatformIO](https://platformio.org). Additionally, PyAvrOCD excels in [minimizing flash wear](https://arduino-craft-corner.de/index.php/2025/05/05/stop-and-go/) and [protects single-stepping against interrupts](https://arduino-craft-corner.de/index.php/2025/03/19/interrupted-and-very-long-single-steps/).

Interested in giving PyAvrOCD a try? You are welcome to [install](https://pyavrocd.io/install/) it. Want to learn more about it? [Read the docs](https://pyavrocd.io). Any feedback, be it bug reports, crazy ideas, or praise, is welcome.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide2-6.png" width="70%">
</p>

## What has been done so far, and what to expect in the future

Meanwhile, PyAvrOCD covers all debugWIRE, JTAG (Megas), and UPDI MCUs. I am unsure whether it makes sense to extend its coverage to Xmegas.

I made some leeway into integrating PyAvrOCD more tightly with *PlatformIO* and with the *Arduino Maker Workshop* VSCode extension. <s>There is the idea of basing everything on more recent versions of the GCC toolchain because it will probably solve a number of problems on the debugging front</s>. My attempt at using the GCC 15.1 toolchain was abruptly stopped when I discovered that the compiler produces buggy debug information concerning local variables, whereas the old compiler works without a flaw at that point. I guess more research and/or debugging is necessary before GCC 15.1 is a viable solution.

 Finally, I am committed to fixing some of the more obvious bugs in the AVR part of the GDB debugger.

