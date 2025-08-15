"""
megaAVR JTAG NVM implementation - extended
"""

from logging import getLogger

from pyedbglib.protocols.jtagice3protocol import Jtagice3ResponseError
from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.util import binary

from pymcuprog.nvmmegaavrjtag import NvmAccessProviderCmsisDapMegaAvrJtag
from pymcuprog.nvm import NvmAccessProviderCmsisDapAvr
from pymcuprog.pymcuprog_errors import PymcuprogError

from pymcuprog.deviceinfo.deviceinfokeys import DeviceMemoryInfoKeys
from pymcuprog.deviceinfo.memorynames import MemoryNames

from pymcuprog import utils

from pyavrocd.xavr8target import XMegaAvrJtagTarget
from pyavrocd.errors import FatalError

# pylint: disable=consider-using-f-string
class XNvmAccessProviderCmsisDapMegaAvrJtag(NvmAccessProviderCmsisDapMegaAvrJtag):
    """
    NVM Access the JTAG way
    """
    #pylint: disable=non-parent-init-called, super-init-not-called
    #we want to set up the debug session much later
    def __init__(self, transport, device_info):
        self.logger_local = getLogger('pyavrocd.nvmjtag')
        NvmAccessProviderCmsisDapAvr.__init__(self, device_info)
        self.avr = XMegaAvrJtagTarget(transport)
        self.logger_local.debug("Setting up device info ...")
        self.avr.setup_config(device_info)
        self.logger_local.debug("... setup done")

    #pylint: enable=non-parent-init-called, super-init-not-called
    def __del__(self):
        pass

    def start(self, user_interaction_callback=None):
        """
        Start (activate) session for JTAG targets

        """
        # pylint: disable=unused-argument
        self.logger_local.info("megaAVR-JTAG-specific initialiser")

        try:
            resp = self.avr.activate_physical()
            self.logger_local.info("Physical interface activated")
        except Jtagice3ResponseError as error:
            # The debugger could be out of sync with the target, retry
            if error.code == Avr8Protocol.AVR8_FAILURE_INVALID_PHYSICAL_STATE:
                self.logger_local.info("Physical state out of sync.  Retrying.")
                self.avr.deactivate_physical()
                self.logger_local.info("Physical interface deactivated")
                resp = self.avr.activate_physical()
                self.logger_local.info("Physical interface activated")
            else:
                raise

        self.logger_local.info("JTAG ID read: %02X%02X%02X%02X", resp[3], resp[2], resp[1], resp[0])
        if resp[0] != 0x3F:
            raise FatalError("Non-Atmel/Microchip JTAG device detected!")

    def stop(self):
        """
        Stop (deactivate) session for JTAG targets
        """
        self.logger_local.info("JTAG-specific de-initialiser")
        self.avr.deactivate_physical()
        self.logger_local.info("Physical interface deactivated")

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
        :return: array of bytes read
        """

        memtype_string = memory_info[DeviceMemoryInfoKeys.NAME]
        memtype = self.avr.memtype_read_from_string(memtype_string)
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
            # if we read chunks that are not page sized or not page aligned, then use SPM as memtype
            if offset%memory_info[DeviceMemoryInfoKeys.PAGE_SIZE] != 0 or \
              numbytes != memory_info[DeviceMemoryInfoKeys.PAGE_SIZE] or \
              not prog_mode:
                memtype = Avr8Protocol.AVR8_MEMTYPE_SPM

        self.logger_local.debug("Reading from %s (memtype=0x%x) at %X %d bytes",
                                    memory_info['name'], memtype, offset, numbytes)

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
        self.logger_local.debug("Reading with memtype=0x%x from %s", memtype, memtype_string)
        if memtype == 0:
            msg = "Unsupported memory type: {}".format(memtype_string)
            self.logger_local.error(msg)
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

        self.logger_local.info("Writing %d bytes of data in chunks of %d bytes to %s...",
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

    def erase_page(self,pageaddr):
        """
        Erase one page (in debug mode only)
        """
        resp = self.avr.protocol.jtagice3_command_response(
            bytearray([Avr8Protocol.CMD_AVR8_PAGE_ERASE, Avr8Protocol.CMD_VERSION0]) + binary.pack_le32(pageaddr))
        return self.avr.protocol.check_response(resp)
