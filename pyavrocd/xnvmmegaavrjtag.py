"""
megaAVR JTAG NVM implementation - extended
"""

from logging import getLogger

from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.util import binary

from pymcuprog.nvmmegaavrjtag import NvmAccessProviderCmsisDapMegaAvrJtag
from pymcuprog.nvm import NvmAccessProviderCmsisDapAvr
from pymcuprog.pymcuprog_errors import PymcuprogError

from pymcuprog.deviceinfo.deviceinfokeys import DeviceMemoryInfoKeys
from pymcuprog.deviceinfo.memorynames import MemoryNames

from pymcuprog import utils

from pyavrocd.xavr8target import XMegaAvrJtagTarget

# pylint: disable=consider-using-f-string
class XNvmAccessProviderCmsisDapMegaAvrJtag(NvmAccessProviderCmsisDapMegaAvrJtag):
    """
    NVM Access the JTAG way
    """
    #pylint: disable=non-parent-init-called, super-init-not-called
    #we want to set up the debug session much later
    def __init__(self, transport, device_info, manage=None):
        self.manage = [] if manage is None else manage
        self.logger_local = getLogger('pyavrocd.nvmjtag')
        NvmAccessProviderCmsisDapAvr.__init__(self, device_info)
        self.avr = XMegaAvrJtagTarget(transport)

    #pylint: enable=non-parent-init-called, super-init-not-called
    def __del__(self):
        pass

    # pylint: disable=arguments-differ
    # reason for the difference in arguments:
    # read and write are declared as staticmethod in the base class,
    # which is an oversight, I believe
    def read(self, memory_info, offset, numbytes, prog_mode=False):
        """
        Read the memory in chunks

        :param memory_info: dictionary for the memory as provided by the DeviceMemoryInfo class
        :param offset: relative offset in the memory type
        :param numbytes: number of bytes to read
        :param prog_mode: True iff in programming mode
        :return: array of bytes read
        """

        memtype_string = memory_info[DeviceMemoryInfoKeys.NAME]
        memtype = self.avr.memtype_read_from_string(memtype_string)
        if memtype_string == MemoryNames.EEPROM:
            if prog_mode:
                memtype = Avr8Protocol.AVR8_MEMTYPE_EEPROM_PAGE
        self.logger_local.debug("Reading with memtype=0x%x", memtype)
        if memtype == 0:
            msg = "Unsupported memory type: {}".format(memtype_string)
            self.logger_local.error(msg)
            raise PymcuprogError(msg)

        if not memtype_string == MemoryNames.FLASH:
            # Flash is offset by the debugger config
            try:
                offset += memory_info[DeviceMemoryInfoKeys.ADDRESS]
            except TypeError:
                pass
        else:
            # if we are not in prog_mode, then use SPM as memtype, otherwise FLASH_PAGE
            if not prog_mode:
                memtype = Avr8Protocol.AVR8_MEMTYPE_SPM

        self.logger_local.debug("Reading from %s (memtype=0x%x) at %X %d bytes",
                                    memory_info['name'], memtype, offset, numbytes)

        data = self.avr.read_memory_section(memtype, offset, numbytes, numbytes)
        return data

    def write(self, memory_info, offset, data, prog_mode=False):
        """
        Write the memory with data

        :param memory_info: dictionary for the memory as provided by the DeviceMemoryInfo class
        :param offset: relative offset within the memory type
        :param data: the data to program
        """
        if len(data) == 0:
            return
        memtype_string = memory_info[DeviceMemoryInfoKeys.NAME]
        memtype = self.avr.memtype_read_from_string(memtype_string)
        if memtype_string == MemoryNames.EEPROM:
            if prog_mode:
                memtype = Avr8Protocol.AVR8_MEMTYPE_EEPROM_PAGE
        self.logger_local.debug("Writing to memtype=0x%x from %s", memtype, memtype_string)
        if memtype == 0:
            msg = "Unsupported memory type: {}".format(memtype_string)
            self.logger_local.error(msg)
            raise PymcuprogError(msg)

        if prog_mode:
            # For prog_mode, page alignment is necessary
            data_to_write, address = utils.pagealign(data,
                                                     offset,
                                                     memory_info[DeviceMemoryInfoKeys.PAGE_SIZE],
                                                     memory_info[DeviceMemoryInfoKeys.WRITE_SIZE])
        else:
            data_to_write = data
            address = offset

        if memtype_string != MemoryNames.FLASH:
            # Flash is offset by the debugger config
            address += memory_info[DeviceMemoryInfoKeys.ADDRESS]

        allow_blank_skip = False
        if memtype_string in MemoryNames.FLASH:
            memtype = Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE
            allow_blank_skip = True

        if memtype in (Avr8Protocol.AVR8_MEMTYPE_EEPROM_PAGE, Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE):
            # For Flash and EEPROM pages we have to write exactly one page
            write_chunk_size = memory_info[DeviceMemoryInfoKeys.PAGE_SIZE]
            data_to_write = utils.pad_to_size(data_to_write, write_chunk_size, 0xFF)
            first_chunk_size = write_chunk_size - address%write_chunk_size
        else:
            write_chunk_size = len(data_to_write)
            # changed computation of first_chunk_size for SRAM:
            first_chunk_size = write_chunk_size

        self.logger_local.debug("Writing %d bytes of data in chunks of %d bytes to %s...",
                         len(data_to_write),
                         write_chunk_size,
                         memory_info[DeviceMemoryInfoKeys.NAME])

        self.avr.write_memory_section(memtype,
                                      address,
                                      data_to_write[:first_chunk_size],
                                      write_chunk_size,
                                      allow_blank_skip=allow_blank_skip)
        address += first_chunk_size
        if len(data_to_write) > first_chunk_size:
            self.avr.write_memory_section(memtype,
                                          address,
                                          data_to_write[first_chunk_size:],
                                          write_chunk_size,
                                          allow_blank_skip=allow_blank_skip)

    def erase_page(self, pageaddr, prog_mode):
        """
        Erase one page (in debug mode only)
        """
        if prog_mode:
            self.avr.switch_to_debmode()
        self.avr.protocol.jtagice3_command_response(
            bytearray([Avr8Protocol.CMD_AVR8_PAGE_ERASE, Avr8Protocol.CMD_VERSION0]) + binary.pack_le32(pageaddr))
        if prog_mode:
            self.avr.switch_to_progmode()
        #self.avr.protocol.check_response(resp)
        return True

    def erase_chip(self, prog_mode):
        """
        Erasing entire chip. Save EEPROM by, potentially, reprogramming EESAVE fuse
        """
        eesave_fuse_byte = None
        eesave_mask = self.device_info.get('eesave_mask')
        eesave_base = self.device_info.get('eesave_base')
        if not prog_mode:
            self.avr.switch_to_progmode()
        if eesave_base and eesave_mask and 'eesave' in self.manage:
            eesave_fuse_byte = self.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_FUSES,
                                                        eesave_base, 1)
            if  eesave_fuse_byte[0] & eesave_mask: # needs to be temporarily programmed
                self.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, eesave_base,
                                          bytearray([eesave_fuse_byte[0] & ~eesave_mask & 0xFF]))
                self.logger_local.debug("Programmed EESAVE fuse temporarily")
            else:
                eesave_fuse_byte = None
        else:
            self.logger_local.error("EESAVE fuse data unknown. EEPROM will be deleted")
        self.avr.erase(Avr8Protocol.ERASE_CHIP, 0)
        self.logger_local.info("Flash memory erased")
        if eesave_fuse_byte: # needs to be restored
            self.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, eesave_base, eesave_fuse_byte)
            self.logger_local.debug("EESAVE fuse restored")
        if not prog_mode:
            self.avr.switch_to_debmode()
        return True
