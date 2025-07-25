# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = []
hiddenimports += collect_submodules('pyavrocd.deviceinfo')
hiddenimports += collect_submodules('pyavrocd.deviceinfo.devices')


a = Analysis(
    ['pyavrocd/pyavrocd.py'],
    pathex=['pyavrocd/deviceinfo/devices/', 'pyavrocd/deviceinfo'],
    binaries=[
        ('/usr/local/Cellar/libusb/1.0.28/lib/libusb-1.0.0.dylib','.'),
        ('/usr/local/Cellar/libusb/1.0.28/lib/libusb-1.0.a', '.'),
        ('/usr/local/Cellar/libusb/1.0.28/lib/libusb-1.0.dylib', '.')],
    datas=[],
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
