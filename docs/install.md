# PyAvrOCD installation



!!! info "Linux"
    Under Linux, users may need to add a few `udev` rules before they can use PyAvrOCD. Download [https://pyavrocd.io/99-edbg-debuggers.rules](https://pyavrocd.io/99-edbg-debuggers.rules), edit if you want, and copy to `/etc/udev/rules.d/`.

## Arduino IDE 2 & Arduino Maker Workshop

If you want to use PyAvrOCD as part of Arduino IDE 2 or the Arduino Maker Workshop, it is sufficient to [install a debug-enabled Arduino package](supporting-packages.md) in the IDE.

## PlatformIO

When you want to use PyAvrOCD together with PlatformIO, you only have to set [the right platform](debugging-software.md#platformio-and-visual-studio-code) in your `platform.ini` configuration file. Then PyAvrOCD will be automatically downloaded and installed when needed.

## Downloading binaries

In order to use PyAvrOCD stand-alone or as part of another IDE, you need to install the PyAvrOCD package explicitly. This can be done, e.g., by downloading the binaries.

Go to the [PyAvrOCD GitHub repo](https://github.com/felias-fogg/PyAvrOCD), and download  the archive containing the binary for your architecture from the set of assets of the latest `Releases`.  This archive includes the folder `tools`.

<details>
<summary><b>How to download the binaries</b></summary>
<p></p>
<p>Click on the <code>Latest</code> button below <b>Releases</b> on the right side of the page.</p>
<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/repo.png" width="55%">
</p>
<p>
This will open the latest release page with all its assets.
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/release.png" width="55%">
</p>
<p>
Select the archive matching your architecture and download it.
Then extract the files (for Windows, I assume, you use the <code>Windows PowerShell</code>):
<pre>
<code class="language-bash hljs">tar xvzf avrocd-tools-X.Y.Z-architecture.tar.gz</code>
</pre>
</p>
</details>
<p></p>

Store its content somewhere in a folder and include this folder in your `PATH` variable.

<details>
<summary><b>How to install the binaries</b></summary>
<p></p>
<p>
Once you have downloaded the archive and uncompressed it, you need to move the files from the tools folder to its destination (e.g., <code>~/.local/bin</code>). For this purpose, first move into the <code>tools</code> folder of the uncompressed archive and:
</p>
<p>
<pre>
<code class="language-bash hljs">mkdir ~/.local
mkdir ~/.local/bin
rm -rf ~/.local/bin/pyavrocd-util
mv pyavrocd* ~/.local/bin/
mv avr-gdb*  ~/.local/bin/
mv bin/* ~/.local/bin/
mv lib ~/.local/</code>
</pre>
</p>
<p>
Now, you only need to add <code>~/.local/bin/</code> to your <code>PATH</code>
</p>
</details>
<p></p>

!!! warning "macOS"
    On a Mac, files downloaded through a browser or from an email are marked as potentially dangerous, and the system may not allow them to be executed. In this case, use the command `xattr -r -d com.apple.quarantine FOLDER` in a terminal window to remove the extended attribute `com.apple.quarantine` from all the binary executables in FOLDER. After that, you can start the executables without a hitch.

## PyPI

If you are a Pythonist, you may want to install the Python package instead of the much larger binary. I assume you already installed a recent Python version (>=3.10). Then [PyPI](https://pypi.org/project/pyavrocd/), with the help of [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/) or [pipx](https://pipx.pypa.io/), will bring PyAvrOCD to your computer.

<details>
<summary><b>How to install PyAvrOCD with pip or pipx</b></summary>
<p></p>
<p>
It is possible to install PyAvrOCD using <code>pip</code>. However, it is recommended to use <code>pipx</code> instead. <code>Pipx</code> installs packages in a way such that they are entirely isolated from the rest of your Python installation and can be invoked as an ordinary binary executable. So, if you haven't done so already, install pipx following the instructions on the <a href="https://pipx.pypa.io/latest/how-to/install-pipx.html">pipx website</a>. Then proceed as follows.
</p>
<pre>
<code class="language-bash hljs">pipx install pyavrocd
pipx ensurepath</code>
</pre>
<p>
Now you should be able to start the GDB server. The binary is stored under <code>~/.local/bin/</code>.
</details>
<p></p>

Note that the folder with [SVD](https://arduino-craft-corner.de/index.php/2025/08/01/system-view-descriptions-of-avr-mcus/) files is not part of the PyPI installation. If you want to use SVD files, they have to be downloaded separately from the [release page](https://github.com/felias-fogg/PyAvrOCD/releases/tag/v0.22.0) of the GitHub repo. The release asset is called `svd.tar.gz`.

## GitHub

Alternatively, you can download or clone the [GitHub repository](https://github.com/felias-fogg/PyAvrOCD). Additionally, you need to install a Python package manager, for instance, [Poetry](https://python-poetry.org), which can be used to install and run the package.

<details>
<summary><b>How to use Poetry</b></summary>
<p></p>
<p>
After having cloned the repo, install Poetry:
</p>
<pre>
<code class="language-bash hljs">pipx install poetry</code>
</pre>
<p>
In the PyAvrOCD project folder, you can now start executing the script as follows:
</p>
<pre>
<code class="language-bash hljs">poetry install
poetry run pyavrocd ...
</code>
</pre>
<p>
Furthermore, you can create a binary standalone package as follows:
</p>
<pre>
<code class="language-bash hljs">poetry run pyinstaller pyavrocd.spec</code>
</pre>
<p>
  As a result, under Linux, you find an executable <code>pyavrocd</code> in the directory <code>dist</code>code>. Under macOS and Windows, wou will find the executable in the directory <code>dist/pyavrocd/</code> together with the folder <code>pyavrocd-util</code>. You can move the executable (and if present <code>pyavrocd-util</code>) to a place in your <code>PATH</code>.
</p>
</details>
<p></p>

