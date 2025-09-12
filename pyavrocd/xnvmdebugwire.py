"""
DebugWIRE NVM implementation - extended
"""

from logging import getLogger

from pyedbglib.protocols.jtagice3protocol import Jtagice3ResponseError
from pyedbglib.protocols.avr8protocol import Avr8Protocol

from pymcuprog.nvmdebugwire import NvmAccessProviderCmsisDapDebugwire
from pymcuprog.nvm import NvmAccessProviderCmsisDapAvr
from pymcuprog.pymcuprog_errors import PymcuprogError

from pymcuprog.deviceinfo.deviceinfokeys import DeviceMemoryInfoKeys
from pymcuprog.deviceinfo.memorynames import MemoryNames

from pymcuprog import utils

from pyavrocd.xavr8target import XTinyAvrTarget

class XNvmAccessProviderCmsisDapDebugwire(NvmAccessProviderCmsisDapDebugwire):
    """
    NVM Access the DW way
    """
    #pylint: disable=non-parent-init-called, super-init-not-called
    #we want to set up the debug session much later
    def __init__(self, transport, device_info, **kwargs):
        _dummy = kwargs
        self.logger_local = getLogger('pyavrocd.nvmdw')
        NvmAccessProviderCmsisDapAvr.__init__(self, device_info)
        self.avr = XTinyAvrTarget(transport)

    def __del__(self):
        pass

    def start(self, user_interaction_callback=None):
        """
        Start (activate) session for debugWIRE targets

        """
        self.logger_local.info("debugWIRE-specific initialiser")

        _dummy = user_interaction_callback
        try:
            self.avr.activate_physical()
            self.logger_local.info("Physical interface activated")
        except Jtagice3ResponseError as error:
            # The debugger could be out of sync with the target, retry
            if error.code == Avr8Protocol.AVR8_FAILURE_INVALID_PHYSICAL_STATE:
                self.logger_local.info("Physical state out of sync.  Retrying.")
                self.avr.deactivate_physical()
                self.logger_local.info("Physical interface deactivated")
                self.avr.activate_physical()
                self.logger_local.info("Physical interface activated")
            else:
                raise

    def stop(self):
        """
        Stop (deactivate) session for debugWIRE targets
        """
        self.logger_local.info("debugWIRE-specific de-initialiser")
        self.avr.deactivate_physical()
        self.logger_local.info("Physical interface deactivated")

    # pylint: disable=arguments-differ
    # reason for the difference: read and write are declared as staticmethod in the base class,
    # which is an oversight, I believe
    def read(self, memory_info, offset, numbytes, prog_mode=False):
        """
        Read the memory in chunks

        :param memory_info: dictionary for the memory as provided by the DeviceMemoryInfo class
        :param offset: relative offset in the memory type
        :param numbytes: number of bytes to read
        :return: array of bytes read
        """
        _dummy = prog_mode # not relevant for debugWIRE
        memtype_string = memory_info[DeviceMemoryInfoKeys.NAME]
        memtype = self.avr.memtype_read_from_string(memtype_string)
        if memtype == 0:
            msg = "Unsupported memory type: {}".format(memtype_string)
            self.logger.error(msg)
            raise PymcuprogError(msg)

        if not memtype_string == MemoryNames.FLASH:
            # Flash is offset by the debugger config
            try:
                offset += memory_info[DeviceMemoryInfoKeys.ADDRESS]
            except TypeError:
                pass
        else:
            # if we read chunks that are not page sized or not page aligned, then use SPM as memtype
            if offset%memory_info[DeviceMemoryInfoKeys.PAGE_SIZE] != 0 or \
              numbytes != memory_info[DeviceMemoryInfoKeys.PAGE_SIZE]:
                memtype = Avr8Protocol.AVR8_MEMTYPE_SPM

        self.logger.debug("Reading from %s at %X %d bytes", memory_info['name'], offset, numbytes)

        data = self.avr.read_memory_section(memtype, offset, numbytes, numbytes)
        return data

    def write(self, memory_info, offset, data):
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
        if memtype == 0:
            msg = "Unsupported memory type: {}".format(memtype_string)
            self.logger.error(msg)
            raise PymcuprogError(msg)

        if memtype_string != MemoryNames.EEPROM:
            # For debugWIRE parts single byte access is enabled for
            # EEPROM so no need to align to page boundaries
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
            allow_blank_skip = True

        if memtype_string in (MemoryNames.FLASH, MemoryNames.EEPROM):
            # For Flash we have to write exactly one page but for EEPROM we
            # could write less than one page, but not more.
            write_chunk_size = memory_info[DeviceMemoryInfoKeys.PAGE_SIZE]
            if memtype_string != MemoryNames.EEPROM:
                data_to_write = utils.pad_to_size(data_to_write, write_chunk_size, 0xFF)
            first_chunk_size = write_chunk_size - address%write_chunk_size
        else:
            write_chunk_size = len(data_to_write)
            # changed computation of first_chunk_size for SRAM:
            first_chunk_size = write_chunk_size

        self.logger.info("Writing %d bytes of data in chunks of %d bytes to %s...",
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

    def erase_page(self, addr, prog_mode):
        """
        In debugWIRE, we cannot erase single pages. But we also do not need to because this takes
        place while flash programming.
        """
        _dummy1 = addr
        _dummy2 = prog_mode
        return False

    def erase_chip(self, prog_mode):
        """
        Erasing entire chip is impossible in debugWIRE.
        """
        _dummy = prog_mode
        return False
