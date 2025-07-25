# How to Generate a New Version

1. Inside `dw-gdbserver`:
   1. Bump version number in pyproject.toml
   2. poetry install
   3. git commit -a -m ... (this calls pre-commit!)
   4. git push
   5. poetry build (for PyPi)
   6. poetry publish (also for PyPi)
2. For each macOS, Linux-Arm, Windows, macOS-Parallels, Linux-on-PC,
   1. run local: `newversion.sh`
   1. This will populate the directories in felias-fogg.github.io:
      - `felias-fogg.github.io/binaries/`
3. Create packages and assets:
   1. Change into `felias-fogg.github.io/dw-tools`
   2. Run ./packer.sh, which will populate the folders:
      - The `dw-tools` folder itself with tools packages
      - The `assets` folder with binary tars of dw-gdbserver
   3. git add \<new tool packages\> in `dw-tools`
   4. git commit ...
   5. git push
4. Create new dw-gdbserver release:
   1. Goto GitHub repo dw-gdbserver
   2. Create new release
   3. Include as assets the new binaries from `felias-fogg.github.io/assets`
5. Change into XCore
   1. Change version number for `DWTOOLS_VERSION` in Add_dw-tools-release.sh
   2. Change `DWTOOLSVERSION` number in `Boads_manager_release.sh`
   3. create PR