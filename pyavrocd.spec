# -*- mode: python ; coding: utf-8 -*-
import os
import platform
from PyInstaller.utils.hooks import collect_submodules

binlist = []
if platform.uname().system == "Darwin":
    # The release workflow builds libusb itself and points here, because
    # Homebrew's bottle is built for the runner's own macOS and would set the
    # deployment target of the whole package. Without the variable -- a local
    # build on this machine -- the Homebrew copy is used as before.
    _libusb = os.environ.get("PYAVROCD_LIBUSB_PREFIX")
    if _libusb:
        binlist = [(_libusb + '/lib/libusb-1.0.0.dylib', '.'),
                   (_libusb + '/lib/libusb-1.0.a', '.'),
                   (_libusb + '/lib/libusb-1.0.dylib', '.')]
    elif platform.uname().machine == "x86_64":
        binlist = [('/usr/local/Cellar/libusb/1.0.*/lib/libusb-1.0.0.dylib','.'),
                   ('/usr/local/Cellar/libusb/1.0.*/lib/libusb-1.0.a', '.'),
                   ('/usr/local/Cellar/libusb/1.0.*/lib/libusb-1.0.dylib', '.')]
    else: # arm64
        binlist = [('/opt/homebrew/Cellar/libusb/1.0.*/lib/libusb-1.0.0.dylib','.'),
                   ('/opt/homebrew/Cellar/libusb/1.0.*/lib/libusb-1.0.a', '.'),
                   ('/opt/homebrew/Cellar/libusb/1.0.*/lib/libusb-1.0.dylib', '.')]


# Only the device descriptions: xavrdebugger loads them by name at runtime
# (getdeviceinfo("pyavrocd.deviceinfo.devices." + devicename)), so import
# analysis cannot see them. Collecting all of pyavrocd.deviceinfo would also
# drag in the three generator scripts harvest.py, collect.py and addsvd.py,
# and through addsvd its import of svd2py -- none of which the server imports.
hiddenimports = []
hiddenimports += collect_submodules('pyavrocd.deviceinfo.devices')

# The SVD files are not read by the server -- monitor.py takes its register
# descriptions from device_info['svd'], baked into the device modules -- but
# the IDE's peripheral register view reads them from inside the package:
# debug.svd_file={debug.toolchain.path}/pyavrocd-util/svd/{build.mcu}.svd in
# the cores' platform.txt. So they ship on every platform. Linux used to be
# excluded, presumably because staticx had to pack everything into a single
# file, which left Linux users without that view.
datalist = [('./svd','svd')]

a = Analysis(
    ['pyavrocd/main.py'],
    pathex=['pyavrocd/deviceinfo/devices/', 'pyavrocd/deviceinfo'],
    binaries= binlist,
    datas=datalist,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
      pyz,
      a.scripts,
      [],
      exclude_binaries=True,
      name='pyavrocd',
      debug=False,
      bootloader_ignore_signals=False,
      strip=False,
      upx=True,
      console=True,
      disable_windowed_traceback=False,
      argv_emulation=False,
      target_arch=None,
      codesign_identity=None,
      entitlements_file=None,
      contents_directory='pyavrocd-util',
    )
coll = COLLECT(
      exe,
      a.binaries,
      a.datas,
      strip=False,
      upx=True,
      upx_exclude=[],
      name='pyavrocd',
    )

