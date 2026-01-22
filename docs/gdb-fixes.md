# GDB Fixes

Getting avr-gdb compiled on macOS:

1. Downloaded the sources, e.g., from https://ftpmirror.gnu.org/gnu/gdb/gdb-17.1.tar.xz
2. Extract archive
3. `cd` into the folder
4. `mkdir build`
5. `cd build`
6. `export CFLAGS="-g -O2 -Wno-error"`
7. `export CXXFLAGS="-g -O2 -Wno-error"`
8. `../configure --prefix=/usr/local --with-system-zlib --without-python --target=avr --with-gmp=/opt/homebrew/Cellar/gmp/6.3.0 --with-mpfr=/opt/homebrew/Cellar/mpfr/4.2.2 --with-lzma=/opt/homebrew/Cellar/xz/5.8.1 --disable-binutiles --without-guile`
9. `make -j$(proc)`
10. You find gdb under `./gdb/gdb`



### Problems solvable in avr-tdep.c

##### Backtrace problem when a function has local variables that are on the stack

```diff
-- avr-tdep.c~	2025-12-20 03:53:21
+++ avr-tdep.c	2026-01-16 17:25:54
@@ -829,7 +829,9 @@
 	  vpc += 2;
 	  insn = extract_unsigned_integer (&prologue[vpc], 2, byte_order);
 	  vpc += 2;
-	  locals_size += ((insn & 0xf) | ((insn & 0xf00) >> 4)) << 8;
+	  /* Here we need to check for "sbc r29, r1" as well! */
+	  if (insn != 0x09d1)
+	    locals_size += ((insn & 0xf) | ((insn & 0xf00) >> 4)) << 8;
 	}
       else
 	return pc_beg + vpc;
```



##### Masking out the unused PC bit when retrieving return addresses from the stack

```diff
--- avr-tdep.c~	2025-12-20 03:53:21
+++ avr-tdep.c	2026-01-17 17:13:27
@@ -38,6 +38,7 @@
 #include "objfiles.h"
 #include <algorithm>
 #include "gdbarch.h"
+#include "memattr.h"

 /* AVR Background:

@@ -240,12 +241,28 @@
   return builtin_type (gdbarch)->builtin_uint8;
 }

+/* Apply a mask to mask out unused bits in the program counter.
+   This needs to be done for ATmega16, ATmega64, ATmega329, and ATmega3250.
+   It works only when the memory map is supplied by the remote server, though.
+   In other words, older servers or GDB compiled without expat will have a problem. */
+
+static CORE_ADDR avr_pc_mask(void)
+{
+  static CORE_ADDR pcmask = 0;
+  if (pcmask == 0) {
+    struct mem_region *m = lookup_mem_region(0);
+    pcmask = m->hi-1;
+  }
+  return pcmask;
+}
+
+
 /* Instruction address checks and conversions.  */

 static CORE_ADDR
 avr_make_iaddr (CORE_ADDR x)
 {
-  return ((x) | AVR_IMEM_START);
+  return ((x & avr_pc_mask()) | AVR_IMEM_START);
 }

 /* FIXME: TRoth: Really need to use a larger mask for instructions.  Some

```



