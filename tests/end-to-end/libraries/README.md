# Libraries

Libraries the test sketches include, kept here so that a test compiles the same
on every machine. `rune2e.py` passes this directory to `arduino-cli compile` with
`--libraries`; without it the compilation would silently depend on what sits in
the sketchbook of whoever runs the tests, which is how `flash` came to fail on a
second machine and nowhere else.

- `progmem_far` (MIT, Bernhard Nebel) — used by the `flashed` sketch. Shipped
  with MightyCore and MegaCore, but not with megaTinyCore or DxCore. Copied here
  from MightyCore; update it from there when it changes.
- `Vcc` 2.3.2 (Bernhard Nebel) — used by the `measure` sketch. From
  https://github.com/felias-fogg/Vcc; update it from there when it changes.
