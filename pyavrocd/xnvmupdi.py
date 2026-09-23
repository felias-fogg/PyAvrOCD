"""
UPDI NVM implementation - extended
"""
#Implementation is only a stub:
#pylint: disable=unused-import
from typing import Any

import logging

from pyedbglib.protocols.jtagice3protocol import Jtagice3ResponseError
from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.hidtransport.hidtransportbase import HidTransportBase
from pyedbglib.util import binary

from pymcuprog.nvmupdi import NvmAccessProviderCmsisDapUpdi
from pymcuprog.nvm import NvmAccessProviderCmsisDapAvr
from pymcuprog.pymcuprog_errors import PymcuprogError
from pymcuprog.avr8target import AvrDevice

from pymcuprog.deviceinfo.deviceinfo import DeviceMemoryInfo
from pymcuprog.deviceinfo.deviceinfokeys import DeviceMemoryInfoKeys, DeviceInfoKeysAvr
from pymcuprog.deviceinfo.memorynames import MemoryNames

from pymcuprog import utils

from pyavrocd.xavr8target import XTinyXAvrTarget

class XNvmAccessProviderCmsisDapUpdi(NvmAccessProviderCmsisDapUpdi):
    """
    NVM Access the DW way
    """
    #pylint: disable=non-parent-init-called, super-init-not-called
    #we want to set up the debug session much later
    def __init__(self, transport :  HidTransportBase,
                    device_info :  dict[ str, Any ],
                    manage : list[str] | None = None):
        self.manage : list[str] = [] if manage is None else manage
        self.logger_local : logging.Logger = logging.getLogger('pyavrocd.nvmupdi')
        NvmAccessProviderCmsisDapAvr.__init__(self, device_info)
        self.avr : AvrDevice = XTinyXAvrTarget(transport, device_info=device_info)
        self.logger_local.debug("manage=%s", self.manage)
        self.options : dict[ str, Any ] = {} # necessary for USER_ROW writing

    def read(self, memory_info : dict[ str, Any ], offset : int,
                 numbytes : int, prog_mode : bool=False) -> bytearray:
        """
        Read the memory in chunks

        :param memory_info: dictionary for the memory as provided by the DeviceMemoryInfo class
        :param offset: relative offset in the memory type
        :param numbytes: number of bytes to read
        :param prog_mode: True iff in programming mode
        :return: array of bytes read

        The super class will handle it (we simply remove the prog_mode parameter)
        """
        _dummy = prog_mode
        return super().read(memory_info, offset, numbytes)


    def write(self, memory_info : dict[ str, Any ], offset : int,
                  data : bytes, prog_mode : bool=False) -> None:
        """
        Write the memory with data

        :param memory_info: dictionary for the memory as provided by the DeviceMemoryInfo class
        :param offset: relative offset within the memory type
        :param data: the data to program

        The super class will handle it
        """
        _dummy = prog_mode
        #super().write(memory_info, offset, data)

######################################################################################################
        #Here we have the real routine because of the USER_ROW pagealing bug.
        memtype_string = memory_info[DeviceMemoryInfoKeys.NAME]
        memtype = self.avr.memtype_write_from_string(memtype_string)
        if memtype == 0:
            msg = "Unsupported memory type: {}".format(memtype_string)
            self.logger.error(msg)
            raise PymcuprogError(msg)

        if memtype_string not in [MemoryNames.EEPROM, MemoryNames.USER_ROW]:
            # For UPDI parts single byte access is enabled for EEPROM so no need to align to page boundaries
            # Same for USER_ROW!
            self.logger.debug("Aligning!")
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

        user_row_write_locked_device = (memtype_string == MemoryNames.USER_ROW) and \
            ('user-row-locked-device' in self.options and self.options['user-row-locked-device'])

        if memtype_string in (MemoryNames.FLASH, MemoryNames.EEPROM, MemoryNames.FUSES, MemoryNames.LOCKBITS) or \
            user_row_write_locked_device:
            # For Flash we have to write exactly one page but for EEPROM we could write less than one page,
            # but not more.  For fuses and lockbits only one byte at a time can be written.
            # For user row on a locked device exactly one page must be written
            write_chunk_size = memory_info[DeviceMemoryInfoKeys.PAGE_SIZE]
            if memtype_string != MemoryNames.EEPROM:
                data_to_write = utils.pad_to_size(data_to_write, write_chunk_size, 0xFF)
        else:
            write_chunk_size = len(data_to_write)

        self.logger.debug("Writing %d bytes of data in chunks of %d bytes to %s...",
                         len(data_to_write),
                         write_chunk_size,
                         memory_info[DeviceMemoryInfoKeys.NAME])

        first_chunk_size = write_chunk_size - address%write_chunk_size
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
######################################################################################################


    def erase_page(self, pageaddr : int, memory_info: dict[ str, Any ], prog_mode : bool) -> bool:
        """
        Erase one page: We do not need this function for UPDI targets!
        """
        _dummy0 = pageaddr
        _dummy1 = memory_info
        _dummy2 = prog_mode
        return False

    def erase_chip(self, prog_mode : bool) -> bool :
        """
        Erasing entire chip. If EESAVE is managed, preserve EEPROM.

        On AVR8X, EESAVE (SYSCFG0) is active high (1 = EEPROM is retained), and a fuse value
        only takes effect after a reset. So, if EESAVE is not set, we set it temporarily,
        reset the MCU, erase the chip, write back the original value, and reset again.
        Lockbits will never be set when this function is called since this is handled
        in _manage_fuses.
        """
        eesave_mask = self.device_info.get('eesave_mask')
        eesave_base = self.device_info.get('eesave_base')
        self.logger_local.debug("Erase Chip: Manage:=%s, Mask=%s, Base=%s", self.manage,
                                    eesave_mask, eesave_base)
        if not prog_mode:
            self.avr.switch_to_progmode()
        original_fuse_byte = None
        if 'eesave' in self.manage:
            if eesave_base is not None and eesave_mask:
                fuse_byte = self.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_FUSES, eesave_base, 1)
                if not fuse_byte[0] & eesave_mask: # EEPROM would be erased
                    self.logger_local.info("EESAVE will be temporarily set")
                    self.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, eesave_base,
                                            bytearray([fuse_byte[0] | eesave_mask]))
                    self._reload_fuses()
                    original_fuse_byte = fuse_byte
                    self.logger_local.debug("EESAVE temporarily set and activated")
            else:
                self.logger_local.error("EESAVE fuse data unknown. EEPROM will be deleted")
        self.avr.erase(Avr8Protocol.ERASE_CHIP, 0)
        self.logger_local.info("Flash memory erased")
        if original_fuse_byte is not None: # needs to be restored
            self.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, eesave_base,
                                      bytearray(original_fuse_byte))
            self._reload_fuses()
            self.logger_local.info("EESAVE fuse restored")
        if not prog_mode:
            self.avr.switch_to_debmode()
        return True

    def _reload_fuses(self) -> None:
        """
        AVR8X fuses take effect only after a reset. Leaving the programming mode
        resets the MCU, so leaving and re-entering it activates the new fuse values.
        (To be verified on hardware by the e2e test 'eesave'.)
        """
        self.avr.leave_progmode()
        self.avr.enter_progmode()

    def read_device_id(self) -> bytearray:
        """
        Read the device info

        :returns: Device ID raw bytes (little endian)
        """
        device_memory_info = DeviceMemoryInfo(self.device_info)
        signatures_info = device_memory_info.memory_info_by_name(MemoryNames.SIGNATURES)
        signatures_address = signatures_info[DeviceMemoryInfoKeys.ADDRESS]
        sig = self.avr.memory_read(self.avr.memtype_read_from_string("raw"),
                                   signatures_address,
                                   3)
        device_id_read = binary.unpack_be24(sig)

        self.logger.info("Device ID: '%06X'", device_id_read)

        revision = self.avr.memory_read(self.avr.memtype_read_from_string("raw"),
                                        self.device_info.get(DeviceInfoKeysAvr.SYSCFG_BASE) + 1, 1)
        self.logger.debug("Device revision: 0x%02x", revision[0])
        self.logger.info("Device revision: '%x.%x'", revision[0] >> 4, revision[0] & 0x0F)

        # Return the raw signature bytes, but swap the endianness as target sends ID as Big endian
        return bytearray([sig[2], sig[1], sig[0]])

