"""
Memory module for the AVR GDB server
"""

# args, logging
from logging import getLogger

# debugger modules
from pyavrocd.errors import  FatalError

class Memory():
    """
    This class is responsible for access to all kinds of memory, for loading the flash memory,
    and for managing the flash cache.

    Flash cache is implemented as a growing bytearray. We start always at 0x0000 and fill empty
    spaces by 0xFF. _flashmem_start_prog points always to the first address from which we need to
    program flash memory. Neither the end of the flash cache nor _flashmem_start_prog need to be
    aligned with multi_page_size (page_size multiplied by buffers_per_flash_page).
    When programming, we will restart at a lower address or add 0xFF at the end.
    """

    def __init__(self, dbg, mon):
        self.logger = getLogger('pyavrocd.memory')
        self.dbg = dbg
        self.mon = mon
        self._flash = bytearray() # bytearray starting at 0x0000
        # some device info that is needed throughout
        self._flash_start = self.dbg.memory_info.memory_info_by_name('flash')['address']
        self._flash_page_size = self.dbg.memory_info.memory_info_by_name('flash')['page_size']
        self._flash_size = self.dbg.memory_info.memory_info_by_name('flash')['size']
        self._multi_buffer = self.dbg.device_info.get('buffers_per_flash_page',1)
        self._masked_registers = self.dbg.device_info.get('masked_registers',[])
        self._multi_page_size = self._multi_buffer*self._flash_page_size
        self._sram_start = self.dbg.memory_info.memory_info_by_name('internal_sram')['address']
        self._sram_size = self.dbg.memory_info.memory_info_by_name('internal_sram')['size']
        self._eeprom_start = self.dbg.memory_info.memory_info_by_name('eeprom')['address']
        self._eeprom_size = self.dbg.memory_info.memory_info_by_name('eeprom')['size']
        self._flashmem_start_prog = 0

    def init_flash(self):
        """
        Initialize flash by emptying it.
        """
        self._flash = bytearray()
        self._flashmem_start_prog = 0

    def is_flash_empty(self):
        """
        Return true if flash cache is empty.
        """
        return len(self._flash) == 0

    def flash_filled(self):
        """
        Return how many bytes have already be filled.
        """
        return len(self._flash)

    def readmem(self, addr, size):
        """
        Read a chunk of memory and return a bytestring or bytearray.
        The parameter addr and size should be hex strings.
        """
        iaddr, method, _ = self.mem_area(addr)
        isize = int(size, 16)
        return method(iaddr, isize)

    def writemem(self, addr, data):
        """
        Write a chunk of memory and return a reply string.
        The parameter addr and size should be hex strings.
        """
        iaddr, _, method = self.mem_area(addr)
        if not data:
            return "OK"
        method(iaddr, data)
        return "OK"

    def mem_area(self, addr):
        """
        This function returns a triple consisting of the real address as an int, the read,
        and the write method. If illegal address section, report and return
        (0, lambda *x: bytes(), lambda *x: False)
        """
        addr_section = "00"
        if len(addr) > 4:
            if len(addr) == 6:
                addr_section = addr[:2]
                addr = addr[2:]
            else:
                addr_section = "0" + addr[0]
                addr = addr[1:]
        iaddr = int(addr,16)
        self.logger.debug("Address section: %s",addr_section)
        if addr_section == "80": # ram
            return(iaddr, self.sram_masked_read, self.dbg.sram_write)
        if addr_section == "81": # eeprom
            return(iaddr, self.dbg.eeprom_read, self.dbg.eeprom_write)
        if addr_section == "00": # flash
            return(iaddr, self.flash_read, self.flash_write)
        self.logger.error("Illegal memtype in memory access operation at %s: %s",
                              addr, addr_section)
        return (0, lambda *x: bytes(), lambda *x: False)

    def sram_masked_read(self, addr, size):
        """
        Read a chunk from SRAM but leaving  out any masked registers. In theory,
        one could use the "Memory Read Masked" method of the AVR8 Generic protocol.
        However, there is no Python method implemented that does that for you.
        For this reason, we do it here step by step.
        """
        end = addr + size
        data = bytearray()
        for mr in sorted(self._masked_registers):
            if mr >= end or addr >= end:
                break
            if mr < addr:
                continue
            if addr < mr:
                data.extend(self.dbg.sram_read(addr, mr - addr))
            data.append(0xFF)
            addr = mr + 1
        if addr < end:
            data.extend(self.dbg.sram_read(addr, end - addr))
        return data


    def flash_read(self, addr, size):
        """
        Read flash contents from cache that had been constructed during loading the file.
        It is faster and circumvents the problem that with some debuggers only page-sized
        access is possible. If there is nothing in the cache or it is explicitly disallowed,
        fall back to reading the flash page-wise (which is the only way supported by mEDBG).
        """
        self.logger.debug("Trying to read %d bytes starting at 0x%X", size, addr)
        if not self.mon.is_debugger_active():
            self.logger.error("Cannot read from memory when DW mode is disabled")
            return bytearray([0xFF]*size)
        if self.mon.is_cache() and addr + size <= self.flash_filled():
            return self._flash[addr:addr+size]
        baseaddr = (addr // self._flash_page_size) * self._flash_page_size
        endaddr = addr + size
        pnum = ((endaddr - baseaddr) +  self._flash_page_size - 1) // self._flash_page_size
        self.logger.debug("No cache, request %d pages starting at 0x%X", pnum, baseaddr)
        response = bytearray()
        for p in range(pnum):
            response +=  self.dbg.flash_read(baseaddr + (p * self._flash_page_size),
                                                  self._flash_page_size)
        self.logger.debug("Response from page read: %s", response)
        response = response[addr-baseaddr:addr-baseaddr+size]
        return response

    def flash_read_word(self, addr):
        """
        Read one word at an even address from flash (LSB first!) and return it as a word value.
        """
        return(int.from_bytes(self.flash_read(addr, 2), byteorder='little'))

    def flash_write(self, addr, data):
        """
        This writes an arbitrary chunk of data to flash. If addr is lower than len(self._flash),
        the cache is cleared. This should do the right thing when loading is implemented with
        X-records.
        """
        if addr < len(self._flash):
            self.init_flash()
        self.store_to_cache(addr, data)
        self.flash_pages()

    def store_to_cache(self, addr, data):
        """
        Store chunks into the flash cache. Programming will take place later.
        """
        self.logger.debug("store_to_cache at %X", addr)
        if addr < len(self._flash):
            raise FatalError("Overlapping  flash areas at 0x%X" % addr)
        self._flash.extend(bytearray([0xFF]*(addr - len(self._flash) )))
        self._flash.extend(data)
        self.logger.debug("%s", self._flash)

    def flash_pages(self):
        """
        Write pages to flash memory, starting at _flashmem_start_prog up to len(self._flash)-1.
        Since programming takes place in chunks of size self._multi_page_size, beginning and end
        needs to be adjusted. At the end, we may add some 0xFFs.
        """
        startaddr = (self._flashmem_start_prog // self._multi_page_size) * self._multi_page_size
        stopaddr = ((len(self._flash) + self._multi_page_size - 1) //
                            self._multi_page_size) * self._multi_page_size
        pgaddr = startaddr
        self.logger.info("Flashing at 0x%X, length: %u ...", pgaddr, stopaddr-startaddr)
        self.dbg.device.avr.protocol.enter_progmode()
        self.logger.info("Programming mode entered")
        while pgaddr < stopaddr:
            self.logger.debug("Flashing page starting at 0x%X", pgaddr)
            pagetoflash = self._flash[pgaddr:pgaddr + self._multi_page_size]
            currentpage = bytearray([])
            if self.mon.is_fastload():
                # interestingly, it is faster to read single pages than a multi-page chunk!
                for p in range(self._multi_buffer):
                    currentpage += self.dbg.flash_read(pgaddr+(p*self._flash_page_size),
                                                           self._flash_page_size)
            self.logger.debug("pagetoflash: %s", pagetoflash.hex())
            self.logger.debug("currentpage: %s", currentpage.hex())
            if currentpage[:len(pagetoflash)] == pagetoflash:
                self.logger.debug("Skip flashing page because already flashed at 0x%X", pgaddr)
            else:
                self.logger.debug("Flashing now from 0x%X to 0x%X", pgaddr, pgaddr+len(pagetoflash))
                pagetoflash.extend(bytearray([0xFF]*(self._multi_page_size-len(pagetoflash))))
                flashmemtype = self.dbg.device.avr.memtype_write_from_string('flash')
                self.dbg.device.avr.write_memory_section(flashmemtype,
                                                            pgaddr,
                                                            pagetoflash,
                                                            self._flash_page_size,
                                                            allow_blank_skip=
                                                             self._multi_buffer == 1)
                if self.mon.is_verify():
                    readbackpage = bytearray([])
                    for p in range(self._multi_buffer):
                        readbackpage += self.dbg.flash_read(pgaddr+(p*self._flash_page_size),
                                                                     self._flash_page_size)
                    self.logger.debug("pagetoflash: %s", pagetoflash.hex())
                    self.logger.debug("readback: %s", readbackpage.hex())
                    if readbackpage != pagetoflash:
                        raise FatalError("Flash verification error on page 0x{:X}".format(pgaddr))
            pgaddr += self._multi_page_size
        self._flashmem_start_prog = len(self._flash)
        self.dbg.device.avr.protocol.leave_progmode()
        self.logger.info("Programming mode stopped")
        self.logger.info("... flashing done")

    def memory_map(self):
        """
        Return a memory map in XML format. Include registers, IO regs, and EEPROM in SRAM area
        """
        return ('l<memory-map><memory type="ram" start="0x{0:X}" length="0x{1:X}"/>' + \
                             '<memory type="flash" start="0x{2:X}" length="0x{3:X}">' + \
                             '<property name="blocksize">0x{4:X}</property>' + \
                             '</memory></memory-map>').format(0 + 0x800000, \
                             (0x10000 + self._eeprom_start + self._eeprom_size),
                              self._flash_start, self._flash_size, self._multi_page_size)

