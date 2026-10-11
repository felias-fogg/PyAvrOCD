#!/bin/bash
#
# Proves that the two programs we ship can actually work together: avr-gdb
# attaches to simavr's GDB stub, reads the firmware's DWARF information and
# stops where the source says it should.
#
# This is the question no floor measurement can answer. The release workflows
# of avr-gdb and simavr establish that both binaries start on an old enough
# system and that simavr can load an ELF file; whether avr-gdb was built with
# working DWARF support and whether the two speak the same remote protocol only
# shows in a session.
#
# Usage:
#   extras/gdb-simavr-test.sh <folder> [port]
#   extras/gdb-simavr-test.sh extras/binaries/x86_64-linux-gnu
#
# The folder is one of the triple folders *after* packer.sh has run, because
# that is when avr-gdb sits beside bin/simavr -- the same arrangement the user
# gets. Only a folder for the architecture this machine runs, of course.

set -eu

DIR=${1:?usage: gdb-simavr-test.sh <folder with avr-gdb and bin/simavr> [port]}
PORT=${2:-1234}
HERE=$(cd "$(dirname "$0")" && pwd)
DIR=$(cd "$DIR" && pwd)

GDB=$DIR/avr-gdb
SIM=$DIR/bin/simavr
[ -f "$GDB" ] || GDB=$DIR/avr-gdb.exe
[ -f "$SIM" ] || SIM=$DIR/bin/simavr.exe
FW=$HERE/ci/smoke-atmega328p.elf
SRC=$HERE/ci/smoke.c

for f in "$GDB" "$SIM" "$FW" "$SRC"; do
    [ -f "$f" ] || { echo "not there: $f" >&2; exit 1; }
done

# The breakpoint goes on the line after the loop, and the line number is read
# from the source instead of written down here: a line number kept in two
# places is a line number that will disagree with itself.
LINE=$(grep -n 'DDRB |= _BV' "$SRC" | head -1 | cut -d: -f1)
[ -n "$LINE" ] || { echo "cannot find the DDRB line in $SRC" >&2; exit 1; }

WORK=$(mktemp -d)
SIMPID=
cleanup() {
    if [ -n "$SIMPID" ] && kill -0 "$SIMPID" 2>/dev/null; then
        kill "$SIMPID" 2>/dev/null || true
    fi
    rm -rf "$WORK"
}
trap cleanup EXIT

echo "avr-gdb: $GDB"
echo "simavr : $SIM"
echo "firmware: $FW, breakpoint at smoke.c:$LINE, port $PORT"

# -g makes simavr listen and wait: the core stays stopped until gdb says go.
"$SIM" -m atmega328p -f 16000000 -g "$PORT" "$FW" > "$WORK/simavr.log" 2>&1 &
SIMPID=$!

# Waiting for the stub is left to gdb, which retries a refused connection until
# its connect-timeout expires. The two obvious alternatives do not work here:
# simavr announces its port with a plain printf, which stays in the block buffer
# because the process then blocks in accept() before the buffer is flushed; and
# probing the port is worse than useless, since the stub listens with a backlog
# of one and would take the probe for its client.
sleep 0.3
kill -0 "$SIMPID" 2>/dev/null || {
    echo "simavr did not start:" >&2; cat "$WORK/simavr.log" >&2; exit 1; }

cat > "$WORK/gdb.cmds" <<CMDS
set confirm off
set pagination off
set height 0
set tcp auto-retry on
set tcp connect-timeout 30
directory $HERE/ci
target remote 127.0.0.1:$PORT
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
echo "--- simavr ---"
cat "$WORK/simavr.log"

fail() { echo "FAILED: $*" >&2; exit 1; }

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

# simavr ends itself: gdb's 'kill' sends the k packet, which sets cpu_Done.
set +e
wait "$SIMPID"; SIMST=$?
set -e
SIMPID=
[ "$SIMST" = 0 ] || fail "simavr exited with status $SIMST"
[ "$GDBST" = 0 ] || fail "avr-gdb exited with status $GDBST"

echo "OK: avr-gdb and simavr debugged the firmware together"
