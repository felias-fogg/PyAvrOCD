#  PyAvrOCD

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?logo=opensourceinitiative&logoColor=white)](https://opensource.org/licenses/MIT) [![PyPI version](https://img.shields.io/pypi/v/pyavrocd?logo=pypi&logoColor=white)](https://pypi.org/project/pyavrocd/)
[![PyPI Python Version](https://img.shields.io/pypi/pyversions/pyavrocd?logo=python&logoColor=white)](https://pypi.org/project/pyavrocd/) ![Pylint badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/felias-fogg/c0d539e3ad0d10252d2aab8ad325246a/raw/pylint.json) ![Pytest badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/felias-fogg/c0d539e3ad0d10252d2aab8ad325246a/raw/pytest.json) ![Coverage badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/felias-fogg/c0d539e3ad0d10252d2aab8ad325246a/raw/pycov.json&maxAge=30) [![Commits since latest](https://img.shields.io/github/commits-since/felias-fogg/PyAvrOCD/latest?include_prereleases&logo=github)](https://github.com/felias-fogg/PyAvrOCD/commits/main) ![Hit Counter](https://visitor-badge.laobi.icu/badge?page_id=felias-fogg_PyAvrOCD) [![PyPI Downloads](https://static.pepy.tech/personalized-badge/pyavrocd?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/pyavrocd)

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/logo-small.png" width="15%">
</p>



PyAvrOCD is a GDB server for 8-bit AVR MCUs (see [list of supported MCUs](https://felias-fogg.github.io/PyAvrOCD/supported-mcus/) and [supported boards](https://felias-fogg.github.io/PyAvrOCD/supported-boards/)). It can communicate with Microchip hardware debuggers such as MPLAB Snap and with the DIY debugger dw-link (see [list of supported hardware debuggers](https://felias-fogg.github.io/PyAvrOCD/supported-debuggers/)).

So, why another open-source GDB server for AVR MCUs? The main intention is to provide a *platform-agnostic* AVR GDB server. In other words, it is ***the missing AVR debugging solution*** for [PlatformIO](https://platformio.org) and the [Arduino IDE 2](https://www.arduino.cc/en/software/). And it excels in [minimizing flash wear](https://arduino-craft-corner.de/index.php/2025/05/05/stop-and-go/) and [protects single-stepping against interrupts](https://arduino-craft-corner.de/index.php/2025/03/19/interrupted-and-very-long-single-steps/).

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide2-6.png" width="70%">
</p>


When you want to install PyAvrOCD, <!-- you can [install it as part of an Arduino core](https://felias-fogg.github.io/PyAvrOCD/install-link/#arduino-ide-2), so that it can be used in the Arduino IDE 2. -->you can [download binaries](https://felias-fogg.github.io/PyAvrOCD/install-link/#downloading-binaries), you can install PyAvrOCD using [PyPI](https://felias-fogg.github.io/PyAvrOCD/install-link/#pypi), or you can, of course, [clone or download the GitHub repo](https://felias-fogg.github.io/PyAvrOCD/install-link/#github).

[Read the docs](https://felias-fogg.github.io/PyAvrOCD/index.html) for more information.


## What has been done so far, and what to expect in the future

When moving from dw-gdbserver to PyAvrOCD, support for JTAG Mega chips has been added. This was more work than anticipated. And the current release is not yet fit for serious work. A number of JTAG MCUs still need to be tested, and more unit and integration tests are called for.  If you would nevertheless like to give it a try, you are welcome. Any feedback, be it bug reports, crazy ideas, or praise, is welcome.

The next step after the v1.0.0 release of PyAvrOCD will be to incorporate it into the respective Arduino cores, so that easy debugging in the Arduino IDE 2 will become possible. Until then, you need to live with the debugWIRE-only GDB server [dw-gdbserver](https://github.com/felias-fogg/dw-gdbserver), which is part of MiniCore and my fork of ATTinyCore, if you would like to debug inside the Arduino IDE 2.

After the integration into the Arduino IDE2, UPDI MCUs will follow next. I am unsure about Xmegas.
