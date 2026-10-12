# ATDF files

These are hardware description files for all relevant AVR MCUs. You can get them from https://packs.download.microchip.com.

They are used to generate the internal description files in `pyavrocd/deviceinfo/devices` and the svd files in `pyavrocd/svd`.

`LICENSE.microchip` is the license file that comes inside the packs themselves,
copied here unchanged. It is identical in every pack, and it is what the
Apache-2.0 notices in `LICENSE`, `extras/atdf/LICENSE` and `svd/LICENSE` rest
on: the ATDF files carry no copyright header of their own, so without this file
the claim could not be checked by anybody.

If I find "mistakes", I generate patch files that could be used to patch
later versions.

The patches can all be applied in one go by
```
cat *.patch | patch -b -f
```
