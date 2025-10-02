# ATDF files

These are hardware description files for all relevant AVR MCUs. You can get them from https://packs.download.microchip.com.

They are used to generate the internal description files in `pyavrocd/deviceinfo/devices` and the svd files in `pyavrocd/svd`.

If I find "mistakes", I generate patch files that could be used to patch
later versions.

The patches can all be applied in one go by
```
cat *.patch | patch -b -f
```
