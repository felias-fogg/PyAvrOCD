"""
Device Specific Classes which use AVR8Protocol implementation
"""
from pyedbglib.protocols.avr8protocol import Avr8Protocol

from pymcuprog.deviceinfo import deviceinfo
from pymcuprog.deviceinfo.memorynames import MemoryNames
from pymcuprog.deviceinfo.deviceinfokeys import DeviceInfoKeys,\
     DeviceInfoKeysAvr, DeviceMemoryInfoKeys

from pymcuprog.avr8target import TinyXAvrTarget, TinyAvrTarget,\
     MegaAvrJtagTarget, XmegaAvrTarget


class XTinyXAvrTarget(TinyXAvrTarget):
    """
    Class handling sessions with TinyX AVR targets using the AVR8 generic protocol
    """

    # The next two methods are needed because different targets access the registers
    # in different ways: TinyX and XMega have a regfile mem type, the others have to access
    # the registers as part of their SRAM address space.
    def register_file_read(self):
        """
        Reads out the AVR register file (R0::R31)

        :return: 32 bytes of register file content as bytearray
        """
        self.logger.debug("Reading register file")
        return self.protocol.regfile_read()

    def register_file_write(self, regs):
        """
        Writes the AVR register file (R0::R31)

        :param data: 32 byte register file content as bytearray
        :raises ValueError: if 32 bytes are not given
        """
        self.logger.debug("Writing register file")
        self.protocol.regfile_write(regs)

    def statreg_read(self):
        """
        Reads SREG

        :returns: 1 Byte of SREG
        :rtype: bytearray
        """
        return self.protocol.memory_read(Avr8Protocol.AVR8_MEMTYPE_OCD,
                                             Avr8Protocol.AVR8_MEMTYPE_OCD_SREG, 1)

    def statreg_write(self, data):
        """
        Writes SREG

        """
        self.protocol.memory_write(Avr8Protocol.AVR8_MEMTYPE_OCD,
                                       Avr8Protocol.AVR8_MEMTYPE_OCD_SREG, data)

    def stack_pointer_write(self,data):
        """
        Writes the stack pointer
        """
        self.protocol.memory_write(Avr8Protocol.AVR8_MEMTYPE_OCD, 0x18, data)


class XTinyAvrTarget(TinyAvrTarget):
    """
    Implements Tiny AVR (debugWIRE) functionality of the AVR8 protocol
    """

    def __init__(self, transport):
        super().__init__(transport)

        # next lines are copied from TinyXAvrTarget
        if transport.device.product_string.lower().startswith('edbg'):
            # This is a workaround for FW3G-158 which has not been fixed for EDBG (fixed in common,
            # but no new EDBG firmware has/will be built)
            self.max_read_chunk_size = 256

    def memtype_write_from_string(self, memtype_string):
        """
        Maps from a string to an avr8 memtype for writes

        :param memtype_string: Friendly name of memory
        :type memtype_string: str
        :returns: Memory type identifier as defined in the protocol
        :rtype: int
        """
        return self.memtype_read_from_string(memtype_string)

    #pylint: disable=too-many-locals, unused-variable
    def setup_config(self, device_info):
        """
        Sets up the device config for a tiny AVR device

        :param device_info: Target device information as returned
                            by deviceinfo.deviceinfo.getdeviceinfo
        :type device_info: dict
        """
        if device_info is None:
            device_info = {}

        # Parse the device info for memory descriptions
        device_memory_info = deviceinfo.DeviceMemoryInfo(device_info)

        flash_info = device_memory_info.memory_info_by_name(MemoryNames.FLASH)
        eeprom_info = device_memory_info.memory_info_by_name(MemoryNames.EEPROM)
        sram_info = device_memory_info.memory_info_by_name(MemoryNames.INTERNAL_SRAM)
        # Extract settings
        fl_page_size = flash_info[DeviceMemoryInfoKeys.PAGE_SIZE]
        fl_size = flash_info[DeviceMemoryInfoKeys.SIZE]
        fl_base = flash_info[DeviceMemoryInfoKeys.ADDRESS]
        sram_base = sram_info[DeviceMemoryInfoKeys.ADDRESS]
        ee_base = eeprom_info[DeviceMemoryInfoKeys.ADDRESS]
        ee_page_size = eeprom_info[DeviceMemoryInfoKeys.PAGE_SIZE]
        ee_size = eeprom_info[DeviceMemoryInfoKeys.SIZE]
        ocd_addr = device_info.get(DeviceInfoKeysAvr.OCD_BASE)
        ocd_rev = device_info.get('ocd_rev')
        pagebuffers_per_flash_block = device_info.get('buffers_per_flash_page',1)
        eear_size = device_info.get('eear_size')
        eearh_addr = device_info.get('eear_base') + eear_size - 1
        eearl_addr = device_info.get('eear_base')
        eecr_addr = device_info.get('eecr_base')
        eedr_addr = device_info.get('eedr_base')
        spmcsr_addr = device_info.get('spmcsr_base')
        osccal_addr = device_info.get('osccal_base')
        device_id = device_info.get(DeviceInfoKeys.DEVICE_ID)

        # Setup device structure and write to tool
        # TINY_FLASH_PAGE_BYTES (2@0x00)
        devdata = bytearray([fl_page_size & 0xff, 0])
        # TINY_FLASH_BYTES (4@0x02)
        devdata += bytearray([fl_size & 0xFF, (fl_size >> 8) & 0xFF,
                                  (fl_size >> 16) & 0xFF, (fl_size >> 24) & 0xFF])
        # TINY_FLASH_BASE (4@0x06)
        devdata += bytearray([fl_base & 0xFF, (fl_base >> 8) & 0xFF,
                                  (fl_base >> 16) & 0xFF, (fl_base >> 24) & 0xFF])
        # TINY_BOOT_BASE (4@0x0A)
        boot_base = fl_size - fl_page_size # as is done for MegaAvr
        devdata += bytearray([boot_base & 0xFF, (boot_base >> 8) & 0xFF,
                                  (boot_base >> 16) & 0xFF, (boot_base >> 24) & 0xFF])
        # TINY_SRAM_BASE (2@0x0E)
        devdata += bytearray([sram_base & 0xff, (sram_base >> 8) & 0xff])
        # TINY_EEPROM_BYTES (2@0x10)
        devdata += bytearray([ee_size & 0xff, (ee_size >> 8) & 0xff])
        # TINY_EEPROM_PAGE_BYTES (1@0x12)
        devdata += bytearray([ee_page_size])
        # TINY_OCD_REVISION (1@0x13)
        devdata += bytearray([ocd_rev])
        # TINY_PAGEBUFFERS_PER_FLASH_BLOCK
        devdata += bytearray([pagebuffers_per_flash_block])
        # 3 byte gap (3@0x15)
        devdata += bytearray([0, 0, 0])
        # TINY_OCD_MODULE_ADDRESS (1@0x18)
        devdata += bytearray([ocd_addr & 0xff])
        # TINY_EEARH_BASE (1@0x19)
        devdata += bytearray([eearh_addr & 0xFF])
        # TINY_EEARL_BASE (1@0x1A)
        devdata += bytearray([eearl_addr & 0xFF])
        # TINY_EECR_BASE (1@0x1B)
        devdata += bytearray([eecr_addr & 0xFF])
        # TINY_EEDR_BASE (1@0x1C)
        devdata += bytearray([eedr_addr & 0xFF])
        # TINY_SPMCSR_BASE (1@0x1D)
        devdata += bytearray([spmcsr_addr & 0xFF])
        # TINY_OSCCAL_BASE (1@0x1E)
        devdata += bytearray([osccal_addr & 0xFF])

        self.logger.debug("Write all device data: %s",
                              [devdata.hex()[i:i+2] for i in range(0, len(devdata.hex()), 2)])
        self.protocol.write_device_data(devdata)


    def statreg_read(self):
        """
        Reads out SREG

        :return: 1 byte of status register
        """
        return self.protocol.memory_read(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5F, 1)


    def statreg_write(self, data):
        """
        Writes byte to SREG
        :param: 1 byte of data

        """
        return self.protocol.memory_write(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5F, data)


    def regfile_read(self):
        """
        Reads out the AVR register file (R0::R31)

        :return: 32 bytes of register file content as bytearray
        """
        return self.protocol.memory_read(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0, 32)

    def regfile_write(self, regs):
        """
        Writes the AVR register file (R0::R31)

        :param data: 32 byte register file content as bytearray
        :raises ValueError: if 32 bytes are not given
        """
        return self.protocol.memory_write(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0, regs)

    def stack_pointer_read(self):
        """
        Reads the stack pointer

        :returns: Stack pointer
        :rtype: bytearray
        """
        return self.protocol.memory_read(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5D, 0x02)

    def stack_pointer_write(self, data):
        """
        Writes the stack pointer

        :param data: 2 byte as bytearray
        :raises ValueError: if 2 bytes are not given
        """
        return self.protocol.memory_write(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5D, data)

    def breakpoint_clear(self):
        """
        Is needed in stop_debugging - should not be there!
        """
        return 0


class XMegaAvrJtagTarget(MegaAvrJtagTarget):
    """
    Implements Mega AVR (JTAG) functionality of the AVR8 protocol
    """

    def regfile_read(self):
        """
        Reads out the AVR register file (R0::R31)

        :return: 32 bytes of register file content as bytearray
        """
        return self.protocol.memory_read(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0, 32)

    def regfile_write(self, regs):
        """
        Writes the AVR register file (R0::R31)

        :param data: 32 byte register file content as bytearray
        :raises ValueError: if 32 bytes are not given
        """
        return self.protocol.memory_write(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0, regs)

class XXmegaAvrTarget(XmegaAvrTarget):
    """
    Implements XMEGA (PDI) functionality of the AVR8 protocol
    """

    def setup_debug_session(self):
        """
        Sets up a debugging session on an XMEGA AVR
        """
        self.protocol.set_variant(Avr8Protocol.AVR8_VARIANT_XMEGA)
        self.protocol.set_function(Avr8Protocol.AVR8_FUNC_DEBUGGING)
        self.protocol.set_interface(Avr8Protocol.AVR8_PHY_INTF_PDI)

    # The next two methods are needed because different targets access the registers
    # in different ways: TinyX and XMega have a regfile mem type, the others have to access
    # the registers as part of their SRAM address space.
    def register_file_read(self):
        """
        Reads out the AVR register file (R0::R31)

        :return: 32 bytes of register file content as bytearray
        """
        self.logger.debug("Reading register file")
        return self.protocol.regfile_read()

    def register_file_write(self, regs):
        """
        Writes the AVR register file (R0::R31)

        :param data: 32 byte register file content as bytearray
        :raises ValueError: if 32 bytes are not given
        """
        self.logger.debug("Writing register file")
        return self.protocol.regfile_write(regs)
