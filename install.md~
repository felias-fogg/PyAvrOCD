# PyAvrOCD installation & configuration



## Installation

Mac and Linux users should be aware of some idiosyncrasies.

!!! info "Linux"
    On a Linux installation, users may need to add a few `udev` rules after having installed PyAvrOCD. Download [https://pyavrocd.io/99-edbg-debuggers.rules](https://pyavrocd.io/99-edbg-debuggers.rules), edit if you want, and copy to `/etc/udev/rules.d/`.

!!! warning "macOS"
    On a Mac, files downloaded through a browser or from an email are marked as potentially dangerous, and the system may not allow them to be executed. In this case, use the command `xattr -d com.apple.quarantine FILE` in a terminal window to remove the extended attribute `com.apple.quarantine` from the binary executable FILE. After that, you can start the executable without a hitch.

### Arduino IDE 2

If you want to use PyAvrOCD as part of Arduino IDE 2, you do not need to install it explicitly. It is sufficient to [install a debug-enabled Arduino core](supporting-cores.md). Together with PyAvrOCD, you will also get the GDB client `avr-gdb` and the simulator (for some AVR chips) `simavr`.

If you want to use PyAvrOCD stand-alone or as part of another IDE, you need to install the PyAvrOCD package explicitly, as described below.

### Downloading binaries

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
After downloading the archive, extract the files (for Windows, I assume, you use the <code>Windows PowerShell</code>):
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

It might happen that the binaries are not compatible with your operating system. In this case, use one of the methods below.

### PyPI

I assume you already installed a recent Python version (>=3.10). Then [PyPI](https://pypi.org/project/pyavrocd/), with the help of [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/) or [pipx](https://pipx.pypa.io/), will bring PyAvrOCD to your computer.

<details>
<summary><b>How to install PyAvrOCD with pip or pipx</b></summary>
<p></p>
<p>
It is possible to install PyAvrOCD using <code>pip</code>. However, it is recommended to use <code>pipx</code> instead. <code>Pipx</code> installs packages in a way such that they are entirely isolated from the rest of your Python installation and can be invoked as an ordinary binary executable. So, if you haven't done so already, install pipx following the instructions on the <a href="https://pipx.pypa.io/stable/installation/">pipx website</a>. Then proceed as follows.
</p>
<pre>
<code class="language-bash hljs">pipx install pyavrocd
pipx ensurepath</code>
</pre>
<p>
After restarting the shell, you should be able to start the GDB server. The binary is stored under <code>~/.local/bin/</code>.
</details>
<p></p>

Note that the folder with [SVD](https://arduino-craft-corner.de/index.php/2025/08/01/system-view-descriptions-of-avr-mcus/) files is not part of the PyPI installation. If you want to use SVD files, they have to be downloaded separately from the [release page](https://github.com/felias-fogg/PyAvrOCD/releases/tag/v0.22.0) of the GitHub repo. The release asset is called `svd.tar.gz`.

### GitHub

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
With that, you can start executing the script inside the downloaded folder as follows:
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
  As a result, you find an executable <code>pyavrocd</code> (or <code>pyavrocd.exe</code>) in the directory <code>dist/pyavrocd/</code> together with the folder <code>pyavrocd-util</code>. You can copy those two to a place in your <code>PATH</code>.
</p>
</details>
<p></p>

## Configuration

It is not necessary to set up any configuration file before using PyAvrOCD.

However, sometimes, it may be convenient to store some [options](command-line-options.md) in a file so that you do not have to type them every time you invoke PyAvrOCD. For this purpose, the `@` notation is very helpful. If you place the string `@file.ext` on the command line, then arguments are read from `file.ext` and spliced into the command line. These arguments are read line by line.

<details>
<summary><b>Example</b></summary>
<p></p>
<p>
Let us assume, <code>file.ext</code> contains the following lines:
</p>
<pre>
<code class="language-bash hljs">--manage
eesave
--prog=3000
--to
atmelice
--veri=e</code>
</pre>
<p>
When you now invoke PyAvrOCD with <code>pyavrocd -d attiny13 -t dwlink @file.ext</code>,, then this is expanded into
</p>
<pre>
<code class="language-bash hljs">pyavrocd -d attiny13 -t dwlink --manage eesave --prog=3000 --to atmelice --veri=e</code>
</pre>
<p>
With the usual abbreviation rules, the fact that the equal sign can simply be substituted by space,  and the rule that later arguments override earlier ones, this is equivalent to
</p>
<pre>
<code class="language-bash hljs">pyavrocd --device attiny13 --manage eesave --prog-clock 3000 --tool atmelice --verify enable</code>
</pre>
</details>
<p></p>
Note that implicitly `@pyavrocd.options` is added to the end of the command line. This means that even if you cannot change the command line that invokes PyAvrOCD, because, e.g., PyAvrOCD is invoked by an IDE, you still can specify arguments that have precedence by using the configuration file `pyavrocd.options`.
