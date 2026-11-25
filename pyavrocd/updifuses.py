"""
The UPDI fuses PyAvrOCD may set because the program dictates them (-m bootend, -m oscfreq).

The policy: PyAvrOCD only writes a fuse whose value follows from the program and that cannot lock
the debugger out. BOOTEND/BOOTSIZE says where the application -- and with it the vector table --
starts, and OSCCFG chooses between the 16 MHz and the 20 MHz oscillator. UPDI runs on its own
clock, so neither can take the debugger's access away. Reset and UPDI pin configuration, BOD
level, lock bits and the CRC source are never written.

The functions here only compute what the fuse should be. Reading and writing is done by the
session (AvrSession._manage_updi_fuses).
"""
from typing import Any

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

# The prescaler of the main clock on tinyAVR 0/1/2, megaAVR 0 and the AVR Ex/Lx parts
# (CLKCTRL.MCLKCTRLB: off, 2, 4, 8, 16, 32, 64, 6, 10, 12, 24, 48)
PRESCALERS : tuple[int, ...] = (1, 2, 4, 6, 8, 10, 12, 16, 24, 32, 48, 64)

def reachable(base_mhz : int, f_cpu : int) -> bool:
    """Whether f_cpu (Hz) is the oscillator of base_mhz divided by one of the prescalers"""
    return any(base_mhz * 1_000_000 == f_cpu * p for p in PRESCALERS)

def oscillator_for(f_cpu : int) -> int | None:
    """
    16 or 20 (MHz), if f_cpu can be derived from only one of the two oscillators; None if it can
    be derived from both (2 MHz) or from neither (tuned or overclocked oscillator, external clock)
    """
    from16 = reachable(16, f_cpu)
    from20 = reachable(20, f_cpu)
    if from16 == from20:
        return None
    return 16 if from16 else 20

def oscfreq_value(fuse : int, f_cpu : int, device_info : dict[str, Any]) -> int | None:
    """
    The new value of the fuse byte that holds the oscillator choice, or None if it is to be left
    as it is. Only the bits of the field change, so OSCLOCK and the like stay what they were.
    """
    base = oscillator_for(f_cpu)
    if base is None or 'oscfreq_mask' not in device_info:
        return None
    mask : int = device_info['oscfreq_mask']
    value : int = device_info['oscfreq_16mhz' if base == 16 else 'oscfreq_20mhz']
    return (fuse & ~mask & 0xFF) | (value & mask)

def vector_table_address(elf_file : str) -> int | None:
    """
    Where the program's vector table is: the symbol __vectors from the C runtime, or the start of
    the .text section if there is no symbol table. None if the file cannot be read.
    """
    try:
        with open(elf_file, 'rb') as f:
            elf = ELFFile(f)
            symtab = elf.get_section_by_name('.symtab')
            if isinstance(symtab, SymbolTableSection):
                for sym in symtab.get_symbol_by_name('__vectors') or []:
                    return int(sym['st_value'])
            text = elf.get_section_by_name('.text')
            if text is not None:
                return int(text['sh_addr'])
    except Exception: # pylint: disable=broad-exception-caught # then the fuse is left alone
        return None
    return None

def bootend_value(vectors : int, device_info : dict[str, Any]) -> int | None:
    """
    The BOOTEND/BOOTSIZE value that makes the application, and with it the vector table, start at
    'vectors'. None if the device has no such fuse or the address is not a multiple of its unit.
    """
    unit : int | None = device_info.get('bootend_unit')
    if not unit or 'bootend_base' not in device_info or vectors % unit != 0:
        return None
    value = vectors // unit
    return value if value <= 0xFF else None
