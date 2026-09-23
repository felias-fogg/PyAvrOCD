# Diagnostic scripts

These scripts are not part of the test suite. They contain no assertions: every step
runs and the log file shows what the target actually did. They were written to track
down the 16-bit write anomaly of the AVR8X ADC (see `docs/UPDI-notes.md`).

Run them from the `end-to-end` directory, so that the includes and the sketch paths
resolve:

    ./rune2e.py -s diagnose/ioregdiag.yml        -d <updi device>   -t ioreg-diag
    ./rune2e.py -s diagnose/ioregdiagclassic.yml -d <classic device> -t ioreg-diag-classic
    ./rune2e.py -s diagnose/ioregdiagcpu.yml     -d <updi device>   -t ioreg-diag-cpu

| script | what it answers |
|---|---|
| `ioregdiag.yml` | Which 16-bit registers survive a debugger write, and in which byte order? Hard-wired addresses are those of ADC0.WINLT/WINHT, identical on the tinyAVR 1-series and the megaAVR 0-series. |
| `ioregdiagclassic.yml` | The same for classic AVRs, with TC1.OCR1A, EEPROM.EEAR and USART0.UBRR0, and ADC.ADC as a read-only control. Byte addresses are those of an ATmega328P. |
| `ioregdiagcpu.yml` | Does the anomaly also hit code executed by the CPU? Loads the sketch `sketches/adcwin`, which writes ADC0.WINHT and TCB0.CCMP in three variants and reads them back. |

`draft/winht_repro.py` and `draft/temp_probe.py` do the same without GDB, using pymcuprog
alone; `temp_probe.py` also watches the peripheral's TEMP register.
