# Potential Speedup for Rangestepping

While the current implementation of range stepping does already cover a lot of ground, there is still the problem that when one "steps over" a line, one will necessarily stop for each procedure call. The reason is that we leave the range. GDB will then set a BP at the return address inside the range, continue execution, and after returning back into the range, another range-stepping action is called.

It would be much faster not to stop after the call, of course. And this is what a "step over" command is meant to do.  However, there is only one rangestepping command that does not distinguish between stepping over and stepping into.

What we see in the stream of GDB commands is the following:

``` 
$vCont;r<START>,<END>:1  ;; range stepping required
T05 ... PC out of range  ;; stopped in a function
$m 80...                 ;; looking into prog
$m 00...                 ;; looking into stack
$m 00...                 ;; looking somewhere else
$Z1,<addr>,2             ;; set breakpoint inside range (return address)
$vCont;c                 ;; finish function and stop after return
T05 ... PC at <addr>     ;; break after return
$m 00...
$z1,<addr>               ;; remove temp breakpoint
$vCont;r<START>,<END>:1  ;; continue with range stepping
```

At the point where `$vCont;c` is requested, the range stepping scaffold is deleted, and the temporary hardware BPs are deallocated. When the second `$vCont;r<START>,<END>:1` command is received, the range stepping scaffold is set up again, and range stepping is continued.

In case of a "step into" command, the sequence looks different.

```
$vCont;r<START>,<END>:1  ;; range stepping required
T05 ... PC out of range  ;; stopped in a function
$m 80...                 ;; looking into prog
$m 00...                 ;; looking into stack
$m 00...                 ;; looking somewhere else
$Z1,<func>,2             ;; set breakpoint outside range (start of function address)
$vCont;c                 ;; finish function and stop after return
T05 ... PC at <func>     ;; stop inside function
$z1,<func>,2             ;; remove temp BP
$m 00 ...
```

This means that if the first kind of sequence is observed, then one could remember that if the next time, range-stepping is requested for the same range, we could ignore all `call`, `rcall`, and `icall` instructions.

Basically, it means that if we simply ignore `m` (and perhaps `x`) records, then the following sequence should trigger the `call-ignore` mode:

1. `$vCont;r<range>`
2. `$Z1,<addr>` with `<addr>` inside `<range>`
3. `$vCont;c`
4. `$z1,<addr>`
5. `$vCont;r<range>` with same range

If the range stepping method is called now, it can ignore all `call` instructions as potential branch points and as instructions to jump outside the range.  If any other record is received, the `call-ignore` mode needs to be disabled.

Will that be enough to distinguish it from simply leaving the range, setting a breakpoint in the range, and then stopping again in the range? Yes. When execution is stopped, GDB will also use `$qfThreadInfo` and `$qsThreadInfo` records. So, the above sequence seems to be distinctive.

This method has been implemented in version 1.2.1.