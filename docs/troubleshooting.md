# Troubleshooting

## No debug probe recognized

- No compatible tool discovered
- Too many connected tools

## Debugging does not start:

- Error message: Apple cannot check ...
     - Use `xattr -d com.apple.quarantine FILE`

- Address already in use
- ISP programming failed
- Wrong MCU: ...
- Stuck-at-1-bit
- Debugging is impossible, because lockbits/OCDEN/DWEN cannot be programmed
- Target is not powered

## Problems while debugging

- debugging/loading is slow
- Does not stop at a line with a set breakpoint, but later
- variable cannot be accessed
- analogwrite (PWM) does not appear to work when execution is stopped
- single step leads to jump to interrupt dispatch table
- Cannot run/continue
     - SIGSYS - breakpoints
     - SIGABRT - Fatal error before
	 - SIGILL - BREAK instructions
	 - SIGBUS - stackpointer too low
	 - SIGSEGV - executable not yet flashed#

