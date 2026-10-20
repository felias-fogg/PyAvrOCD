# Stress tests

Tests against real debug probes that are neither unit tests nor end-to-end tests:
they need hardware but no target, and they are meant to be run many times in a row.
pytest does not collect them.

## sigstress.py: signals during probe transactions

`pyavrocd/termination.py` defers SIGTERM and SIGINT while a transaction with the
probe is under way. This script checks that it works. It sends housekeeping GETs,
padded to three fragments, in a loop and lets a timer interrupt them at a random
moment between 5 and 30 ms; afterwards it checks that a GET still gets its own answer
and that no response is left pending. Under Unix the signal is SIGTERM, under
Windows SIGINT, raised from the timer thread as a console Ctrl-C would be.

```
python tests/stress/sigstress.py list                         # attached probes
python tests/stress/sigstress.py <serial> guarded 100         # with the guard
python tests/stress/sigstress.py <serial> unguarded 100       # without, for comparison
python tests/stress/sigstress.py <serial> noop 100            # handler that does nothing
python tests/stress/sigstress_all.py [rounds] [timeout]       # both modes, all probes
```

`unguarded` has to fail, otherwise the test proves nothing. On EDBG and Atmel-ICE it
hangs in a blocking HID read instead; Ctrl-C does not help then, and the probe has to
be replugged afterwards. `sigstress_all.py` kills a run that hangs after the timeout
(120 s by default).

`noop` shows a second effect: under macOS, a signal that arrives while hidapi is
inside a C call makes that call fail, even with a handler that does nothing. This is
why the guard also blocks the signals with `pthread_sigmask` where the OS has it.

## Results, 2026-10-20

100 rounds each.

| Probe     | Firmware   | macOS, SIGTERM: unguarded / guarded | Windows, SIGINT: unguarded / guarded |
|-----------|------------|-------------------------------------|--------------------------------------|
| SNAP      | 1.11 b20   | error / 100 ok                      | error / 100 ok                       |
| PICkit4   | 1.15 b20   | error / 100 ok                      | error / 100 ok                       |
| nEDBG     | 1.31 b39   | error / 100 ok                      | error / 100 ok                       |
| mEDBG     | 1.22 b134  | error / 100 ok                      | error / 100 ok                       |
| EDBG      | 3.37 b438  | hangs / 100 ok                      | hangs / 100 ok                       |
| Atmel-ICE | 1.45 b7    | hangs / 100 ok                      | hangs, then unresponsive / 100 ok    |

## Why: what the probes do with a transaction cut short

Measured with housekeeping and AVR8 configuration commands, no target attached:

- **Response never fetched, then the next command:** SNAP, PICkit4, nEDBG and mEDBG
  drop the next command and hand out the old response in its place (the mEDBG appends
  the bytes of the dropped command to it). Atmel-ICE and EDBG discard the old response
  and execute the next command.
- **Command cut between its fragments, then the next command:** all of them take the
  next command as the missing tail of the interrupted one, whatever fragment number it
  carries, execute that, and drop the next command.
- pyedbglib notices neither: `Jtagice3Command.validate_response`, which would compare
  sequence numbers, is never called.
