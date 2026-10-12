#!/bin/bash
#
# Proves that the three programs we ship can debug together, the way the
# Arduino IDE arranges them: avr-gdb talks to PyAvrOCD, and PyAvrOCD starts
# simavr as the target. That is what the simavr entry in the cores'
# programmers.txt sets up ('-s <path>/bin/simavr'), so it is what should be
# tested -- the IDE never talks to simavr directly.
#
# What this covers that a floor measurement cannot: whether avr-gdb starts at
# all on this platform (it is linked against the system ncurses), whether it
# was built with usable DWARF support, whether simavr finds its bundled libelf
# through the RPATH, whether PyAvrOCD's launcher path works and prints the line
# the IDE waits for, and whether the firmware can be written into the simulated
# flash over the remote protocol -- PyAvrOCD starts simavr without a firmware,
# so gdb has to 'load' it.
#
# Usage:
#   extras/gdb-simavr-test.sh <folder> [port] [--direct]
#   extras/gdb-simavr-test.sh extras/binaries/x86_64-linux-gnu
#
# <folder> is a triple folder holding pyavrocd, avr-gdb and bin/simavr -- the
# arrangement packer.sh produces and the user receives. With --direct, PyAvrOCD
# is left out and gdb talks to simavr's own stub; useful where there is no
# pyavrocd binary to hand.

set -eu

DIR=${1:?usage: gdb-simavr-test.sh <folder> [port] [--direct]}
PORT=${2:-2000}
MODE=${3:-}
HERE=$(cd "$(dirname "$0")" && pwd)
DIR=$(cd "$DIR" && pwd)

GDB=$DIR/avr-gdb
[ -f "$GDB" ] || GDB=$DIR/avr-gdb.exe
# Deliberately without the .exe: PyAvrOCD only recognises simavr when the
# basename is exactly 'simavr', and shutil.which adds the extension on Windows.
SIM_ARG=$DIR/bin/simavr
SIM=$SIM_ARG
[ -f "$SIM" ] || SIM=$SIM_ARG.exe
SERVER=$DIR/pyavrocd
[ -f "$SERVER" ] || SERVER=$DIR/pyavrocd.exe
FW=$HERE/ci/smoke-atmega328p.elf
SRC=$HERE/ci/smoke.c

for f in "$GDB" "$SIM" "$FW" "$SRC"; do
    [ -f "$f" ] || { echo "not there: $f" >&2; exit 1; }
done
if [ "$MODE" != "--direct" ] && [ ! -f "$SERVER" ]; then
    echo "not there: $SERVER (use --direct to test without PyAvrOCD)" >&2
    exit 1
fi

# The breakpoint goes on the line after the loop, and the line number is read
# from the source instead of written down here: a line number kept in two
# places is a line number that will disagree with itself.
LINE=$(grep -n 'DDRB |= _BV' "$SRC" | head -1 | cut -d: -f1)
[ -n "$LINE" ] || { echo "cannot find the DDRB line in $SRC" >&2; exit 1; }

WORK=$(mktemp -d)
PID=
cleanup() {
    if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then kill "$PID" 2>/dev/null || true; fi
    rm -rf "$WORK"
}
trap cleanup EXIT

echo "avr-gdb : $GDB"
echo "simavr  : $SIM"
echo "firmware: $FW, breakpoint at smoke.c:$LINE, port $PORT"

if [ "$MODE" = "--direct" ]; then
    echo "mode    : gdb against simavr's own stub"
    "$SIM" -m atmega328p -f 16000000 -g "$PORT" "$FW" > "$WORK/server.log" 2>&1 &
    PID=$!
    LOAD=""
else
    echo "mode    : gdb -> PyAvrOCD -> simavr (what the IDE does)"
    echo "server  : $SERVER"
    # -s makes PyAvrOCD start simavr with '-g <port> -f <F_CPU> -m <device>'
    # and wait for it. No firmware is passed, hence the 'load' below.
    "$SERVER" -s "$SIM_ARG" -d atmega328p -F 16000000 -p "$PORT" \
        > "$WORK/server.log" 2>&1 &
    PID=$!
    LOAD="load"
fi

# Waiting is left to gdb, which retries a refused connection until its
# connect-timeout expires. Reading the log would be unreliable: simavr
# announces its port with a plain printf that stays in the block buffer, and
# probing the port is worse, since the stub listens with a backlog of one and
# would take the probe for its client.
sleep 0.5
kill -0 "$PID" 2>/dev/null || {
    echo "the server did not start:" >&2; cat "$WORK/server.log" >&2; exit 1; }

cat > "$WORK/gdb.cmds" <<CMDS
set confirm off
set pagination off
set height 0
set tcp auto-retry on
set tcp connect-timeout 30
directory $HERE/ci
target remote 127.0.0.1:$PORT
$LOAD
break smoke.c:$LINE
continue
info line
print sum
kill
quit
CMDS

set +e
"$GDB" -batch -x "$WORK/gdb.cmds" "$FW" > "$WORK/gdb.log" 2>&1
GDBST=$?
set -e
echo "--- gdb ---"
cat "$WORK/gdb.log"
echo "--- server ---"
cat "$WORK/server.log"

fail() { echo "FAILED: $*" >&2; exit 1; }

if [ "$MODE" != "--direct" ]; then
    grep -q 'Simavr starts' "$WORK/server.log" \
        || fail "PyAvrOCD did not start simavr -- with -s it only does so when the \
basename is exactly 'simavr', so an argument ending in .exe silently misses it"
    grep -q 'Listening on port' "$WORK/server.log" \
        || fail "PyAvrOCD did not print the line the IDE waits for \
(overrideGDBServerStartedRegex)"
    grep -q 'Transfer rate' "$WORK/gdb.log" \
        || fail "'load' did not transfer anything -- the firmware never reached the \
simulated flash, so FlashErase/FlashWrite over the remote protocol is suspect"
fi

# Three assertions, each for a different part of the chain.
grep -q 'Breakpoint 1, main' "$WORK/gdb.log" \
    || fail "the breakpoint on smoke.c:$LINE was never reached -- symbols, line \
table or the remote protocol"
grep -q 'Line .* of "smoke.c"' "$WORK/gdb.log" \
    || fail "gdb does not place the stop in smoke.c -- no usable line table, \
which is what a build without DWARF support looks like"
grep -qE '^\$1 = 55$' "$WORK/gdb.log" \
    || fail "'print sum' did not yield 55 -- the local variable could not be \
located in SRAM or not read over the remote protocol"

# Everything ends by itself: gdb's 'kill' sends the k packet, simavr sets
# cpu_Done and terminates, and PyAvrOCD returns once its child is gone.
set +e
wait "$PID"; SRVST=$?
set -e
PID=
[ "$SRVST" = 0 ] || fail "the server exited with status $SRVST"
[ "$GDBST" = 0 ] || fail "avr-gdb exited with status $GDBST"

echo "OK: avr-gdb, PyAvrOCD and simavr debugged the firmware together"
