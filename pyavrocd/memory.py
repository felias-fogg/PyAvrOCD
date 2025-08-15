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
    If the attribute lazy is set, then flashing is done leaving the bytes not fitting in a page
    unprogrammed. One can finalize loading when calling flash_pages with the lazy attribute set to False.
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
        self.lazy_loading = False
        self.programming_mode = False

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
        response = method(iaddr, data)
        self.logger.debug("Result of writing: %s", response)
        if response is None:
            return "OK"
        return "E13"

    def mem_area(self, addr):
        """
        This function returns a triple consisting of the real address as an int, the read,
        and the write method. If illegal address section, report and return
        (0, lambda *x: bytes(), lambda *x: 'E13')
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
        if addr_section == "00": # flash
            if self.dbg.iface == "debugwire" or self.programming_mode:
                return(iaddr, self.flash_read, self.flash_write)
            return(iaddr, self.flash_read, lambda *x: 'E13')
        if addr_section == "80": # ram
            if not self.programming_mode:
                return(iaddr, self.sram_masked_read, self.dbg.sram_write)
        if addr_section == "81": # eeprom
            return(iaddr, self.dbg.eeprom_read, self.dbg.eeprom_write)
        if addr_section == "82": # fuse
            if self.programming_mode and self.dbg.iface in ['jtag', 'updi']:
                return(iaddr, self.fuse_read, self.fuse_write)
        if addr_section == "83": #  lock
            if (self.programming_mode and self.dbg.iface == 'jtag') or self.dbg.iface == 'updi':
                return(iaddr, self.lock_read, self.lock_write)
        if addr_section == "84": # signature
            if (self.programming_mode and self.dbg.iface in ['jtag', 'updi']) \
              or self.dbg.iface == 'debugwire':
                return(iaddr, self.sig_read, lambda *x: 'E13')
        if addr_section == "85":  # user signature
            if self.dbg.iface in ['jtag', 'updi']:
                return(iaddr, self.usig_read, self.usig_write)
        self.logger.error("Illegal memtype in memory access operation at %s: %s",
                              addr, addr_section)
        return (0, lambda *x: bytes(), lambda *x: 'E13')

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
            self.logger.error("Cannot read from memory when OCD is disabled")
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

    #pylint: disable=useless-return
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
        return None

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
        If mon.is_fast_load() is true (read before write), the we will read a page before it is written.
        If it is nothing new, we skip. Otherwise, when "jtag", we check whether the page is blank.
        If not, the we need to erase this page by temporarily leaving progmode.
        This out of the way, we program.
        Optionally, after writing, we check whether we were successful.
        """
        startaddr = (self._flashmem_start_prog // self._multi_page_size) * self._multi_page_size
        if self.lazy_loading:
            roundup = 0
        else:
            roundup = self._multi_page_size - 1
        stopaddr = ((len(self._flash) + roundup) // self._multi_page_size) * self._multi_page_size
        pgaddr = startaddr
        give_info = stopaddr-startaddr > 2048
        proged = 0
        next_mile_stone = 2000
        self.logger.info("Flashing at 0x%X, length: %u ...", pgaddr, stopaddr-startaddr)
        while pgaddr < stopaddr:
            self.logger.debug("Flashing page starting at 0x%X", pgaddr)
            pagetoflash = self._flash[pgaddr:pgaddr + self._multi_page_size]
            currentpage = bytearray([])
            if self.mon.is_fastload():
                # interestingly, it is faster to read single pages than a multi-page chunk!
                for p in range(self._multi_buffer):
                    currentpage += self.dbg.flash_read(pgaddr+(p*self._flash_page_size),
                                                           self._flash_page_size, prog_mode=True)
            self.logger.debug("pagetoflash: %s", pagetoflash.hex())
            self.logger.debug("currentpage: %s", currentpage.hex())
            if currentpage[:len(pagetoflash)] == pagetoflash:
                self.logger.debug("Skip flashing page because already flashed at 0x%X", pgaddr)
            else:
                if self.dbg.iface == 'jtag':
                    if self.mon.is_fastload() and not self.dbg.device.avr.is_blank(currentpage):
                        self.logger.debug("Erasing page at 0x%x in debug mode", pgaddr)
                        if self.programming_mode:
                            self.dbg.device.avr.protocol.leave_progmode()
                        self.dbg.device.erase_page(pgaddr)
                        if self.programming_mode:
                            self.dbg.device.avr.protocol.enter_progmode()
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
                                                                     self._flash_page_size,
                                                                      prog_mode=True)
                    self.logger.debug("pagetoflash: %s", pagetoflash.hex())
                    self.logger.debug("readback: %s", readbackpage.hex())
                    if readbackpage != pagetoflash:
                        raise FatalError("Flash verification error on page 0x{:X}".format(pgaddr))
            pgaddr += self._multi_page_size
            proged += self._multi_page_size
            if give_info and proged >= next_mile_stone:
                next_mile_stone += 2000
                self.logger.info("%d bytes flashed", proged)
        if self.lazy_loading:
            self._flashmem_start_prog = pgaddr
        else:
            self._flashmem_start_prog = len(self._flash)
        self.logger.info("... flashing done")

    def memory_map(self):
        """
        Return a memory map in XML format. Include registers, IO regs, and EEPROM in SRAM area
        """
        return ('l<memory-map><memory type="ram" start="0x{0:X}" length="0x{1:X}"/>' + \
                             '<memory type="flash" start="0x{2:X}" length="0x{3:X}">' + \
                             '<property name="blocksize">0x{4:X}</property>' + \
                             '</memory></memory-map>').format(0 + 0x800000, \
                              # (0x10000 + self._eeprom_start + self._eeprom_size),
                              0x890000, # is needed to read the other memory areas as well
                              self._flash_start, self._flash_size, self._multi_page_size)

    def fuse_read(self, addr, size):
        """
        Read fuses (does not work with debugWIRE)
        """
        try:
            resp = self.dbg.read_fuse(addr, size)
        except Exception as e:
            self.logger.error("Error reading fuses: %s", e)
            return bytearray([0xFF]*size)
        return bytearray(resp)

    def fuse_write(self, addr, data):
        """
        Write fuses (does not work with debugWIRE)
        """
        try:
            self.dbg.write_fuse(self, addr, data)
        except Exception as e:
            self.logger.error("Error writing fuses: %s", e)
            return 'E13'
        return None

    def lock_read(self, addr, size):
        """
        Read lock bits (does not work with debugWIRE)
        """
        try:
            resp = self.dbg.read_lock(addr, size)
        except Exception as e:
            self.logger.error("Error reading lockbits: %s", e)
            return bytearray([0xFF]*size)
        return bytearray(resp)

    def lock_write(self, addr, data):
        """
        Write lock bits (does not work with debugWIRE)
        """
        try:
            self.dbg.write_lock(addr, data)
        except Exception as e:
            self.logger.error("Error writing lockbits: %s", e)
            return 'E13'
        return None

    def sig_read(self, addr, size):
        """
        Read signature in a liberal way, i.e., throwing no errors
        """
        try:
            resp = self.dbg.read_sig(addr, size)
        except Exception as e:
            self.logger.error("Error reading the signature: %s", e)
            return bytearray([0xFF]*size)
        return bytearray(resp)

    def usig_read(self, addr, size):
        """
        Read contents of user signature (does not work with debugWIRE)
        """
        try:
            resp = self.dbg.read_usig(addr, size)
        except Exception as e:
            self.logger.error("Error reading the user signature: %s", e)
            return bytearray([0xFF]*size)
        return bytearray(resp)

    def usig_write(self, addr, data):
        """
        Write user signature
        """
        try:
            self.dbg.write_usig(addr, data)
        except Exception as e:
            self.logger.error("Error writing the user signature: %s", e)
            return 'E13'
        return None
