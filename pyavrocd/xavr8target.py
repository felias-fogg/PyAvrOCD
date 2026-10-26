"""
Device Specific Classes which use AVR8Protocol implementation
"""
from typing import Any

import logging

from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.util import binary
from pyedbglib.hidtransport.hidtransportbase import HidTransportBase

from pymcuprog.deviceinfo import deviceinfo
from pymcuprog.deviceinfo.memorynames import MemoryNames
from pymcuprog.deviceinfo.deviceinfokeys import DeviceInfoKeysAvr, DeviceMemoryInfoKeys, DeviceInfoKeys

from pymcuprog.avr8target import TinyXAvrTarget, TinyAvrTarget,\
     MegaAvrJtagTarget, XmegaAvrTarget, AvrDevice


class XTinyXAvrTarget(TinyXAvrTarget):
    """
    Class handling sessions with TinyX (UPDI) AVR targets using the AVR8 generic protocol
    """
    def __init__(self, transport : HidTransportBase, device_info :  dict[ str, Any ] | None = None) -> None:
        if device_info is None:
            device_info = {}
        super().__init__(transport)
        self.logger_loc : logging.Logger = logging.getLogger('pyavrocd.tinyxtarget')
        self._fusebase : int = device_info.get('fuses_address_byte', 0)
        self._lockbase : int = device_info.get('lockbits_address_byte', 0)
        self._sigbase : int =  device_info.get('signatures_address_byte', 0)
        self._usbase : int =   device_info.get('user_row_address_byte', 0)
        self._nvmcbase : int = device_info.get('nvmctrl_base', 0)
        self._syscbase : int = device_info.get('syscfg_base', 0)

    def memory_read(self, memory_name : int, start_address : int, numbytes : int) -> bytearray:
        """
        Read device memory
        """
        data : bytearray = self.protocol.memory_read(memory_name,
                                self._addr_transform(memory_name, start_address), numbytes)
        self.logger_loc.debug("Read %d bytes on transformed addr 0x%X", numbytes,
                                  self._addr_transform(memory_name, start_address))
        return data

    def memory_write(self, memory_name : int, start_address : int , data : bytes) -> bytearray | None:
        """
        Write device memory
        """
        self.logger_loc.debug("Writing %d bytes to transformed address 0x%X", len(data),
                                  self._addr_transform(memory_name, start_address))
        return self.protocol.memory_write(memory_name, self._addr_transform(memory_name, start_address), data)

    def _addr_transform(self, memory_name : int, start_address : int) -> int:
        """
        Transforms start_address
        """
        if memory_name == Avr8Protocol.AVR8_MEMTYPE_FUSES:
            return start_address + self._fusebase
        if memory_name == Avr8Protocol.AVR8_MEMTYPE_LOCKBITS:
            return start_address + self._lockbase
        if memory_name == Avr8Protocol.AVR8_MEMTYPE_SIGNATURE:
            return start_address + self._sigbase
        if memory_name == Avr8Protocol.AVR8_MEMTYPE_USER_SIGNATURE:
            return start_address + self._usbase
        return start_address


    # The next two methods are needed because different targets access the registers
    # in different ways: TinyX and XMega have a regfile mem type, the others have to access
    # the registers as part of their SRAM address space.
    def regfile_read(self) -> bytearray:
        """
        Reads out the AVR register file (R0::R31)

        :return: 32 bytes of register file content as bytearray
        """
        self.logger_loc.debug("Reading register file")
        return self.protocol.regfile_read()

    def regfile_write(self, regs : bytes) -> None:
        """
        Writes the AVR register file (R0::R31)

        :param data: 32 byte register file content as bytearray
        :raises ValueError: if 32 bytes are not given
        """
        self.logger_loc.debug("Writing register file")
        self.protocol.regfile_write(regs)

    def statreg_read(self) -> bytearray:
        """
        Reads out SREG (for this type of MCU not at 0x5F, but at 0x3F)

        :return: 1 byte of status register
        """
        return self.protocol.memory_read(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x3F, 1)


    def statreg_write(self, data : bytes) -> bytearray:
        """
        Writes byte to SREG
        :param: 1 byte of data

        """
        return self.protocol.memory_write(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x3F, data)

    def stack_pointer_write(self, data : bytes) -> None:
        """
        Writes the stack pointer
        """
        self.protocol.memory_write(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x3D, data)

    def stack_pointer_read(self) -> bytearray:
        """
        Reads the stack pointer

        :returns: Stack pointer
        :rtype: bytearray
        """
        return self.protocol.memory_read(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x3D, 0x02)

    def hardware_breakpoint_set(self, num : int, address : int) -> bytes | None:
        """
        Sets one hardware breakpoint <num>

        :param num: number of breakpoint: can only be 1
        :param address: Address to break at
        :type address: int
        """
        if num < 1 or num > 1:
            self.logger.error("Tried to set hardware breakpoint %d at 0x%X on UPDI target",
                                num, address)
            return None
        return self.breakpoint_set(address)


    def hardware_breakpoint_clear(self, num : int) -> bytes | None:
        """
        Clears the hardware breakpoint <num>
        """
        if num < 1 or num > 1:
            self.logger.error("Tried to clear hardware breakpoint %d on UPDI target",
                                num)
            return None
        return self.breakpoint_clear()

    def attach(self) -> None:
        """
        Attach (in the beginning)

        """
        self.protocol.attach()

    def reactivate(self) -> None:
        """
        Reactivate physical: Necessary to set the right timer mode
        """
        self.protocol.detach()
        self.deactivate_physical()
        self.activate_physical()
        self.protocol.attach()
        self.logger_loc.info("Physical interface re-activated")

    def switch_to_progmode(self) -> None:
        """
        Simply detach and enter prog mode
        """
        self.logger_loc.debug("Detaching...")
        self.protocol.detach()
        self.logger_loc.debug("Entering progmode...")
        self.protocol.enter_progmode()
        self.logger_loc.debug("Switched to progmode")

    def switch_to_debmode(self) -> None:
        """
        Simply leave prog mode and attach again
        """
        self.logger_loc.debug("Leaving progmode...")
        self.protocol.leave_progmode()
        self.logger_loc.debug("Trying to attach...")
        self.protocol.attach()
        self.logger_loc.debug("Switched to debug mode")


    #pylint: disable=arguments-differ
    def setup_debug_session(self, kbps : int | None = None,
                            **kwargs : Any) -> None:
        """
        Sets up a debug session for a tinyX AVR device

        :param kbps: Communication speed in kbps
        :param timers_run: whether timers should run while execution is suspended
        """
        _dummy = kwargs
        self.logger_loc.info("Setting up debug session for UPDI target")
        if kbps is not None:
            self.protocol.set_le16(Avr8Protocol.AVR8_CTXT_PHYSICAL, Avr8Protocol.AVR8_PHY_XM_PDI_CLK, kbps)
            self.logger_loc.info("UPDI communication speed limit: %d kbps", kbps)
        self.protocol.set_byte(Avr8Protocol.AVR8_CTXT_OPTIONS,
                                   Avr8Protocol.AVR8_OPT_HV_UPDI_ENABLE,
                                   0)
        self.logger_loc.debug("UPDI HV programming disabled")
        #self.protocol.set_byte(Avr8Protocol.AVR8_CTXT_OPTIONS,
        #                           Avr8Protocol.AVR8_OPT_RUN_TIMERS,
        #                           timers_run)
        #self.logger_loc.debug("Configured timers as running: %d", timers_run)
        self.protocol.set_variant(Avr8Protocol.AVR8_VARIANT_TINYX)
        self.logger_loc.debug("Set variant: UPDI target")
        self.protocol.set_function(Avr8Protocol.AVR8_FUNC_DEBUGGING)
        self.logger_loc.debug("Set function: debugging")
        self.protocol.set_interface(Avr8Protocol.AVR8_PHY_INTF_PDI_1W)
        self.logger_loc.debug("Set interface: PDI 1 wire (UPDI)")

    def setup_config(self, device_info  : dict[str, Any ]) -> None:
        """
        Sets up the device config for a tinyX AVR device

        :param device_info: Target device information as returned by deviceinfo.deviceinfo.getdeviceinfo
        :type device_info: dict
        """
        if device_info is None:
            device_info = {}

        # Parse the device info for memory descriptions
        device_memory_info = deviceinfo.DeviceMemoryInfo(device_info)

        flash_info : dict = device_memory_info.memory_info_by_name(MemoryNames.FLASH)
        eeprom_info : dict = device_memory_info.memory_info_by_name(MemoryNames.EEPROM)
        # Extract settings
        fl_base : int = flash_info[DeviceMemoryInfoKeys.ADDRESS]
        fl_page_size : int = flash_info[DeviceMemoryInfoKeys.PAGE_SIZE]
        fl_size : int = flash_info[DeviceMemoryInfoKeys.SIZE]
        ee_base : int = eeprom_info[DeviceMemoryInfoKeys.ADDRESS]
        ee_page_size : int = eeprom_info[DeviceMemoryInfoKeys.PAGE_SIZE]
        ee_size : int = eeprom_info[DeviceMemoryInfoKeys.SIZE]
        nvmctrl_addr : int = device_info.get(DeviceInfoKeysAvr.NVMCTRL_BASE, 0)
        ocd_addr : int = device_info.get(DeviceInfoKeysAvr.OCD_BASE, 0)
        user_row_base : int = device_memory_info.memory_info_by_name(MemoryNames.USER_ROW)[DeviceMemoryInfoKeys.ADDRESS]
        user_row_size : int = device_memory_info.memory_info_by_name(MemoryNames.USER_ROW)[DeviceMemoryInfoKeys.SIZE]
        sig_row_base : int = device_memory_info.\
          memory_info_by_name(MemoryNames.SIGNATURES)[DeviceMemoryInfoKeys.ADDRESS]
        fuses_base : int = device_memory_info.memory_info_by_name(MemoryNames.FUSES)[DeviceMemoryInfoKeys.ADDRESS]
        fuse_size : int = device_memory_info.memory_info_by_name(MemoryNames.FUSES)[DeviceMemoryInfoKeys.SIZE]
        lock_base : int = device_memory_info.memory_info_by_name(MemoryNames.LOCKBITS)[DeviceMemoryInfoKeys.ADDRESS]
        device_id : int = device_info.get(DeviceInfoKeys.DEVICE_ID, 0)
        hv_implementation : bool = device_info.get(DeviceInfoKeysAvr.HV_IMPLEMENTATION, 0)

        # Setup device structure and write to tool
        # TINYX_PROG_BASE (2@0x00)
        devdata : bytearray = bytearray([fl_base & 0xff, (fl_base >> 8) & 0xff])
        # TINYX_FLASH_PAGE_BYTES (1@0x02)
        devdata += bytearray([fl_page_size & 0xff])
        # TINYX_EEPROM_PAGE_BYTES  (1@0x03)
        devdata += bytearray([ee_page_size])
        # TINYX_NVMCTRL_MODULE_ADDRESS (2@0x04)
        devdata += bytearray([nvmctrl_addr & 0xff, (nvmctrl_addr >> 8) & 0xff])
        # TINYX_OCD_MODULE_ADDRESS (2@0x06)
        devdata += bytearray([ocd_addr & 0xff, (ocd_addr >> 8) & 0xff])

        # Pad to get to TINYX_FLASH_BYTES
        devdata += bytearray([0x00]*(0x12-len(devdata)))

        # TINYX_FLASH_BYTES (4@0x12)
        devdata += bytearray([fl_size & 0xFF, (fl_size >> 8) & 0xFF, (fl_size >> 16) & 0xFF, (fl_size >> 24) & 0xFF])
        # TINYX_EEPROM_BYTES (2@0x16)
        devdata += bytearray([ee_size & 0xff, (ee_size >> 8) & 0xff])
        # TINYX_USER_SIG_BYTES_BYTES (2@0x18)
        devdata += bytearray([user_row_size & 0xff, (user_row_size >> 8) & 0xff])
        # TINYX_FUSE_BYTES (1@0x1A)
        devdata += bytearray([fuse_size & 0xff])

        # Pad to get to TINYX_EEPROM_BASE
        devdata += bytearray([0x00]*(0x20-len(devdata)))

        # TINYX_EEPROM_BASE (2@0x20)
        devdata += bytearray([ee_base & 0xFF, (ee_base >> 8) & 0xFF])
        # TINYX_USER_ROW_BASE (2@0x22)
        devdata += bytearray([user_row_base & 0xFF, (user_row_base >> 8) & 0xFF])
        #TINYX_SIGROW_BASE (2@0x24)
        devdata += bytearray([sig_row_base & 0xFF, (sig_row_base >> 8) & 0xFF])
        #TINYX_FUSES_BASE (2@0x26)
        devdata += bytearray([fuses_base & 0xFF, (fuses_base >> 8) & 0xFF])
        # TINYX_LOCK_BASE (2@0x28)
        devdata += bytearray([lock_base & 0xFF, (lock_base >> 8) & 0xFF])
        # TINYX_DEVICE_ID (2@0x2A)
        devdata += bytearray([device_id & 0xFF, (device_id >> 8) & 0xFF])
        # TINYX_PROG_BASE_MSB (1@0x2C)
        devdata += bytearray([(fl_base >> 16) & 0xFF])
        # TINYX_FLASH_PAGE_BYTES_MSB (1@0x2D)
        devdata += bytearray([(fl_page_size >> 8) & 0xFF])
        # TINYX_ADDRESS_SIZE (1@0x2E)
        if device_info.get(DeviceInfoKeysAvr.ADDRESS_SIZE, '16-bit') == '24-bit':
            # Use 24-bit addressing mode
            devdata += bytearray([0x01])
        else:
            # Default is 16-bit addressing mode
            devdata += bytearray([0x00])
        # TINYX_HV_IMPLEMENTATION (1@0x2F)
        devdata += bytearray([hv_implementation & 0xFF])

        self.protocol.write_device_data(devdata)



def tiny_device_data(device_info : dict[str, Any]) -> bytearray:
    """
    The 31 bytes of device data for a debugWIRE target, as the EDBG probes get them
    (XTinyAvrTarget.setup_config) and as the JTAGICE mkII and dw-link get them in section 0x02
    of the device context (jtag2.make_device_context)
    """
    # Parse the device info for memory descriptions
    device_memory_info : deviceinfo.DeviceMemoryInfo = deviceinfo.DeviceMemoryInfo(device_info)

    flash_info : dict = device_memory_info.memory_info_by_name(MemoryNames.FLASH)
    eeprom_info : dict = device_memory_info.memory_info_by_name(MemoryNames.EEPROM)
    sram_info : dict = device_memory_info.memory_info_by_name(MemoryNames.INTERNAL_SRAM)
    # Extract settings
    fl_page_size : int = flash_info[DeviceMemoryInfoKeys.PAGE_SIZE]
    fl_size : int = flash_info[DeviceMemoryInfoKeys.SIZE]
    fl_base : int = flash_info[DeviceMemoryInfoKeys.ADDRESS]
    sram_base : int = sram_info[DeviceMemoryInfoKeys.ADDRESS]
    ee_page_size : int = eeprom_info[DeviceMemoryInfoKeys.PAGE_SIZE]
    ee_size : int = eeprom_info[DeviceMemoryInfoKeys.SIZE]
    ocd_addr : int = device_info.get(DeviceInfoKeysAvr.OCD_BASE,0)
    ocd_rev : int = device_info.get('ocd_rev',0)
    pagebuffers_per_flash_block : int = device_info.get('buffers_per_flash_page',1)
    eear_size : int = device_info.get('eear_size',0)
    eearh_addr : int = device_info.get('eear_base',0) + eear_size - 1
    eearl_addr : int = device_info.get('eear_base',0)
    eecr_addr : int = device_info.get('eecr_base',0)
    eedr_addr : int = device_info.get('eedr_base',0)
    spmcsr_addr : int = device_info.get('spmcsr_base',0)
    osccal_addr : int = device_info.get('osccal_base',0)

    # Setup device structure and write to tool
    # TINY_FLASH_PAGE_BYTES (2@0x00)
    devdata : bytearray = bytearray([fl_page_size & 0xff, 0])
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
    return devdata


class XTinyAvrTarget(TinyAvrTarget):
    """
    Implements Tiny AVR (debugWIRE) functionality of the AVR8 protocol
    """

    def __init__(self, transport : HidTransportBase, **kwargs : Any) -> None:
        _dummy = kwargs
        super().__init__(transport)
        self.logger_loc = logging.getLogger('pyavrocd.tinytarget')

        # next lines are copied from TinyXAvrTarget
        if transport.device.product_string.lower().startswith('edbg'):
            # This is a workaround for FW3G-158 which has not been fixed for EDBG (fixed in common,
            # but no new EDBG firmware has/will be built)
            self.max_read_chunk_size = 256

    def setup_debug_session(self, timers_run : bool = True, **kwargs : Any) -> None:
        """
        Sets up a debugging session on an Tiny AVR (debugwire)
        """
        _dummy = kwargs
        self.logger_loc.info("Setting up debug session for debugWIRE target")
        self.protocol.set_byte(Avr8Protocol.AVR8_CTXT_OPTIONS,
                                              Avr8Protocol.AVR8_OPT_RUN_TIMERS,
                                              timers_run)
        self.protocol.set_variant(Avr8Protocol.AVR8_VARIANT_TINYOCD)
        self.protocol.set_function(Avr8Protocol.AVR8_FUNC_DEBUGGING)
        self.protocol.set_interface(Avr8Protocol.AVR8_PHY_INTF_DW)


    #pylint: disable=arguments-differ
    def memtype_read_from_string(self, memtype_string : str) -> int:
        """
        Maps from a string to an AVR memtype taking into account the constraints for
        memory in the NVM mode for reading.
        """
        memtype : int = AvrDevice.memtype_read_from_string(memtype_string)
        if memtype == Avr8Protocol.AVR8_MEMTYPE_CALIBRATION_SIGNATURE:
            memtype = Avr8Protocol.AVR8_MEMTYPE_SIGNATURE
        return memtype

    def memtype_write_from_string(self, memtype_string : str) -> int:
        """
        Maps from a string to an avr8 memtype for writes

        :param memtype_string: Friendly name of memory
        :type memtype_string: str
        :returns: Memory type identifier as defined in the protocol
        :rtype: int
        """
        return self.memtype_read_from_string(memtype_string)

    def switch_to_progmode(self) -> None:
        """
        In general, we would switch to programming mode. However, for debugWIRE,
        prog mode or deb mode do not make a difference.
        """
        #self.protocol.enter_progmode()

    def switch_to_debmode(self) -> None:
        """
        In general, we would switch to debugging mode. However, for debugWIRE,
        prog mode or deb mode do not make a difference.
        """
        #self.protocol.leave_progmode()

    def attach(self) -> None:
        """
        For debugWIRE, we will attach to the OCD just once.
        """
        self.protocol.attach()

    def reactivate(self) -> None:
        """
        For debugWIRE, reactivating is nothing
        """

    def setup_config(self, device_info : dict[str, Any ]) -> None:
        """
        Sets up the device config for a tiny AVR device

        :param device_info: Target device information as returned
                            by deviceinfo.deviceinfo.getdeviceinfo
        :type device_info: dict
        """
        devdata : bytearray = tiny_device_data(device_info)
        self.logger_loc.debug("Write all device data: %s",
                              [devdata.hex()[i:i+2] for i in range(0, len(devdata.hex()), 2)])
        self.protocol.write_device_data(devdata)


    def statreg_read(self) -> bytearray:
        """
        Reads out SREG

        :return: 1 byte of status register
        """
        return self.protocol.memory_read(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5F, 1)


    def statreg_write(self, data : bytes) -> bytearray:
        """
        Writes byte to SREG
        :param: 1 byte of data

        """
        return self.protocol.memory_write(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5F, data)


    def regfile_read(self) -> bytearray:
        """
        Reads out the AVR register file (R0::R31)

        :return: 32 bytes of register file content as bytearray
        """
        return self.protocol.memory_read(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0, 32)

    def regfile_write(self, regs : bytes) -> bytearray:
        """
        Writes the AVR register file (R0::R31)

        :param data: 32 byte register file content as bytearray
        :raises ValueError: if 32 bytes are not given
        """
        return self.protocol.memory_write(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0, regs)

    def stack_pointer_read(self) -> bytearray:
        """
        Reads the stack pointer

        :returns: Stack pointer
        :rtype: bytearray
        """
        return self.protocol.memory_read(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5D, 0x02)

    def stack_pointer_write(self, data : bytes) -> bytearray:
        """
        Writes the stack pointer

        :param data: 2 byte as bytearray
        :raises ValueError: if 2 bytes are not given
        """
        return self.protocol.memory_write(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5D, data)

    def hardware_breakpoint_set(self, num : int, address : int) -> None:
        """
        Sets one hardware breakpoint <num>

        :param num: number of breakpoint 1-3
        :param address: Address to break at
        :type address: int
        """
        self.logger.error("Tried to set hardware breakpoint %d at 0x%X on debugWIRE target",
                              num, address)


    def hardware_breakpoint_clear(self, num : int) -> None:
        """
        Clears the hardware breakpoint <num>
        """
        self.logger.error("Tried to clear hardware breakpoint %d on debugWIRE target",
                              num)


    def breakpoint_clear(self) -> None:
        """
        Is needed in stop_debugging - should not be there!
        """
        return None


class XMegaAvrJtagTarget(MegaAvrJtagTarget):
    """
    Implements Mega AVR (JTAG) functionality of the AVR8 protocol
    """

    def __init__(self, transport  : HidTransportBase, **kwargs : Any) -> None:
        _dummy = kwargs
        super().__init__(transport)
        self.logger_loc : logging.Logger = logging.getLogger('pyavrocd.megatarget')

    #pylint: disable=arguments-differ
    def memtype_read_from_string(self, memtype_string : str) -> int:
        """
        Maps from a string to an AVR memtype taking into account the constraints for
        memory in the NVM mode for reading.
        """
        memtype : int = AvrDevice.memtype_read_from_string(memtype_string)
        if memtype == Avr8Protocol.AVR8_MEMTYPE_CALIBRATION_SIGNATURE:
            memtype = Avr8Protocol.AVR8_MEMTYPE_SIGNATURE
        return memtype

    def memtype_write_from_string(self, memtype_string : str) -> int:
        """
        Maps from a string to an AVR memtype taking into account the constraints for
        memory in the NVM mode for writing.
        """
        return self.memtype_read_from_string(memtype_string)

    def switch_to_progmode(self) -> None:
        """
        Simply detach and enter prog mode
        """
        self.logger_loc.debug("Detaching...")
        self.protocol.detach()
#        self.logger_loc.debug("Deactivating physical...")
#        self.deactivate_physical()
#        self.logger_loc.debug("Activating physical...")
#        self.activate_physical()
        self.logger_loc.debug("Entering progmode...")
        self.protocol.enter_progmode()
        self.logger_loc.debug("Switched to progmode")

    def switch_to_debmode(self) -> None:
        """
        Simply leave prog mode and attach again
        """
        self.logger_loc.debug("Leaving progmode...")
        self.protocol.leave_progmode()
#        self.logger_loc.debug("Deactivating physical...")
#        self.deactivate_physical()
#        self.logger_loc.debug("Activating physical...")
#        self.activate_physical()
        self.logger_loc.debug("Trying to attach...")
        self.protocol.attach()
        self.logger_loc.debug("Switched to debug mode")

    def attach(self) -> None:
        """
        Attach (in the beginning)

        """
        self.protocol.attach()

    def reactivate(self) -> None:
        """
        Reactivate physical: Necessary to set the right timer mode
        """
        self.protocol.detach()
        self.deactivate_physical()
        self.activate_physical()
        self.protocol.attach()
        self.logger_loc.info("Physical interface re-activated")

    def setup_debug_session(self, clkprg : int = 200,
                                clkdeb : int = 1000,
                                timers_run : bool = True,
                                **kwargs : Any) -> None:
        """
        Sets up a programming session on an Mega AVR (JTAG)
        """
        _dummy = kwargs
        self.logger_loc.info("Setting up debug session for JTAG target")
        self.protocol.set_le16(Avr8Protocol.AVR8_CTXT_PHYSICAL, Avr8Protocol.AVR8_PHY_MEGA_DBG_CLK, clkdeb)
        self.logger_loc.info("Debugging JTAG frequency: %d kHz", clkdeb)
        self.protocol.set_le32(Avr8Protocol.AVR8_CTXT_PHYSICAL, Avr8Protocol.AVR8_PHY_JTAG_DAISY, 0)
        self.logger_loc.debug("JTAG daisy chain configuration set up")
        self.protocol.set_byte(Avr8Protocol.AVR8_CTXT_OPTIONS,
                                              Avr8Protocol.AVR8_OPT_RUN_TIMERS,
                                              timers_run)
        self.logger_loc.info("Configured timers as running: %d", timers_run)
        self.protocol.set_variant(Avr8Protocol.AVR8_VARIANT_MEGAOCD)
        self.logger_loc.debug("Set Variant: megaJTAG")
        self.protocol.set_function(Avr8Protocol.AVR8_FUNC_DEBUGGING)
        self.logger_loc.debug("Set Function: Debugging")
        self.protocol.set_interface(Avr8Protocol.AVR8_PHY_INTF_JTAG)
        self.logger_loc.debug("Set Interface: JTAG")
        self.protocol.set_le16(Avr8Protocol.AVR8_CTXT_PHYSICAL, Avr8Protocol.AVR8_PHY_MEGA_PRG_CLK, clkprg)
        self.logger_loc.info("Programming JTAG frequency: %d kHz", clkprg)


    # setup_config is done in the super class
    # However, it seems to be wrong. Instead of IO register addresses RAM addresses
    # are used. I guess the version below is the correct one!
    def setup_config(self, device_info : dict[str, Any ]) -> None:
        """
        Sets up the device config for a tiny AVR device

        :param device_info: Target device information as returned
                            by deviceinfo.deviceinfo.getdeviceinfo
        :type device_info: dict
        """

        # Parse the device info for memory descriptions
        device_memory_info = deviceinfo.DeviceMemoryInfo(device_info)

        flash_info : dict = device_memory_info.memory_info_by_name(MemoryNames.FLASH)
        eeprom_info : dict = device_memory_info.memory_info_by_name(MemoryNames.EEPROM)
        sram_info : dict = device_memory_info.memory_info_by_name(MemoryNames.INTERNAL_SRAM)
        # Extract settings
        fl_page_size : int = flash_info[DeviceMemoryInfoKeys.PAGE_SIZE]
        fl_size : int = flash_info[DeviceMemoryInfoKeys.SIZE]
        fl_base : int = flash_info[DeviceMemoryInfoKeys.ADDRESS]
        sram_base : int = sram_info[DeviceMemoryInfoKeys.ADDRESS]
        ee_page_size : int = eeprom_info[DeviceMemoryInfoKeys.PAGE_SIZE]
        ee_size : int = eeprom_info[DeviceMemoryInfoKeys.SIZE]
        ocd_addr : int = device_info.get(DeviceInfoKeysAvr.OCD_BASE,0)
        ocd_rev : int = device_info.get('ocd_rev',0)
        pagebuffers_per_flash_block : int = device_info.get('buffers_per_flash_page',1)
        eear_size : int = device_info.get('eear_size',0)
        eearh_addr : int = device_info.get('eear_base',0) + eear_size - 1
        eearl_addr : int = device_info.get('eear_base',0)
        eecr_addr : int = device_info.get('eecr_base',0)
        eedr_addr : int = device_info.get('eedr_base',0)
        spmcsr_addr : int = device_info.get('spmcsr_base',0)
        osccal_addr : int = device_info.get('osccal_base',0)

        # Setup device structure and write to tool

        # TMEGA_FLASH_PAGE_BYTES (2@0x00)
        devdata : bytearray = bytearray([fl_page_size & 0xff, (fl_page_size >> 8) & 0xff])

        # TMEGA_FLASH_BYTES (4@0x02)
        devdata += bytearray([fl_size & 0xFF, (fl_size >> 8) & 0xFF,
                                  (fl_size >> 16) & 0xFF, (fl_size >> 24) & 0xFF])

        # TMEGA_FLASH_BASE (4@0x06)
        devdata += bytearray([fl_base & 0xFF, (fl_base >> 8) & 0xFF,
                                  (fl_base >> 16) & 0xFF, (fl_base >> 24) & 0xFF])

        # TMEGA_BOOT_BASE (4@0x0A)
        boot_base = fl_size - fl_page_size # as is done for MegaAvr
        devdata += bytearray([boot_base & 0xFF, (boot_base >> 8) & 0xFF,
                                  (boot_base >> 16) & 0xFF, (boot_base >> 24) & 0xFF])

        # TMEGA_SRAM_BASE (2@0x0E)
        devdata += bytearray([sram_base & 0xff, (sram_base >> 8) & 0xff])

        # TMEGA_EEPROM_BYTES (2@0x10)
        devdata += bytearray([ee_size & 0xff, (ee_size >> 8) & 0xff])

        # TMEGA_EEPROM_PAGE_BYTES (1@0x12)
        devdata += bytearray([ee_page_size])

        # TMEGA_OCD_REVISION (1@0x13)
        devdata += bytearray([ocd_rev])

        # TMEGA_PAGEBUFFERS_PER_FLASH_BLOCK
        devdata += bytearray([pagebuffers_per_flash_block])

        # 3 byte gap (3@0x15)
        devdata += bytearray([0, 0, 0])

        # TMEGA_OCD_MODULE_ADDRESS (1@0x18)
        devdata += bytearray([ocd_addr & 0xff])

        # TMEGA_EEARH_BASE (1@0x19)
        devdata += bytearray([eearh_addr & 0xFF])

        # TMEGA_EEARL_BASE (1@0x1A)
        devdata += bytearray([eearl_addr & 0xFF])

        # TMEGA_EECR_BASE (1@0x1B)
        devdata += bytearray([eecr_addr & 0xFF])

        # TMEGA_EEDR_BASE (1@0x1C)
        devdata += bytearray([eedr_addr & 0xFF])

        # TMEGA_SPMCSR_BASE (1@0x1D)
        devdata += bytearray([spmcsr_addr & 0xFF])

        # TMEGA_OSCCAL_BASE (1@0x1E)
        devdata += bytearray([osccal_addr & 0xFF])

        self.logger_loc.debug("Write all device data: %s",
                              [devdata.hex()[i:i+2] for i in range(0, len(devdata.hex()), 2)])
        self.protocol.write_device_data(devdata)



    def regfile_read(self) -> bytearray:
        """
        Reads out the AVR register file (R0::R31)

        :return: 32 bytes of register file content as bytearray
        """
        return self.protocol.memory_read(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0, 32)

    def regfile_write(self, regs : bytes) -> bytes:
        """
        Writes the AVR register file (R0::R31)

        :param data: 32 byte register file content as bytearray
        :raises ValueError: if 32 bytes are not given
        """
        return self.protocol.memory_write(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0, regs)

    def statreg_read(self) -> bytearray:
        """
        Reads out SREG

        :return: 1 byte of status register
        """
        return self.protocol.memory_read(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5F, 1)


    def statreg_write(self, data : bytes) -> bytes:
        """
        Writes byte to SREG
        :param: 1 byte of data

        """
        return self.protocol.memory_write(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5F, data)

    def stack_pointer_read(self) -> bytearray:
        """
        Reads the stack pointer

        :returns: Stack pointer
        :rtype: bytearray
        """
        return self.protocol.memory_read(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5D, 0x02)

    def stack_pointer_write(self, data : bytes) -> bytes:
        """
        Writes the stack pointer

        :param data: 2 byte as bytearray
        :raises ValueError: if 2 bytes are not given
        """
        return self.protocol.memory_write(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x5D, data)

    def hardware_breakpoint_set(self, num : int, address : int) -> bytes | None:
        """
        Sets one hardware breakpoint <num>

        :param num: number of breakpoint 1-3
        :param address: Address to break at
        :type address: int
        """
        if num < 1 or num > 3:
            self.logger.error("Tried to set hardware breakpoint %d at 0x%X on JTAG target",
                                num, address)
            return None
        resp = self.protocol.jtagice3_command_response(
            bytearray([Avr8Protocol.CMD_AVR8_HW_BREAK_SET, Avr8Protocol.CMD_VERSION0, 1, num]) +
            binary.pack_le32(address) +
            bytearray([3]))
        return self.protocol.check_response(resp)


    def hardware_breakpoint_clear(self, num : int) -> bytes | None:
        """
        Clears the hardware breakpoint <num>
        """
        if num < 1 or num > 3:
            self.logger.error("Tried to clear hardware breakpoint %d on JTAG target",
                                num)
            return None
        resp = self.protocol.jtagice3_command_response(
            bytearray([Avr8Protocol.CMD_AVR8_HW_BREAK_CLEAR, Avr8Protocol.CMD_VERSION0, num]))
        return self.protocol.check_response(resp)

    def breakpoint_clear(self) -> None:
        """
        Is needed in stop_debugging and will clear all hardware breakpoints
        """
        for hwbp in range(1,4):
            self.hardware_breakpoint_clear(hwbp)


class XXmegaAvrTarget(XmegaAvrTarget):
    """
    Implements XMEGA (PDI) functionality of the AVR8 protocol
    """

    def __init__(self, transport : HidTransportBase, **kwargs : Any) -> None:
        _dummy = kwargs
        super().__init__(transport)
        self.logger_loc : logging.Logger = logging.getLogger('pyavrocd.xmegatarget')


    def setup_debug_session(self) -> None:
        """
        Sets up a debugging session on an XMEGA AVR
        """
        self.protocol.set_variant(Avr8Protocol.AVR8_VARIANT_XMEGA)
        self.protocol.set_function(Avr8Protocol.AVR8_FUNC_DEBUGGING)
        self.protocol.set_interface(Avr8Protocol.AVR8_PHY_INTF_PDI)

    # The next two methods are needed because different targets access the registers
    # in different ways: TinyX and XMega have a regfile mem type, the others have to access
    # the registers as part of their SRAM address space.
    def regfile_read(self) -> bytearray:
        """
        Reads out the AVR register file (R0::R31)

        :return: 32 bytes of register file content as bytearray
        """
        self.logger_loc.debug("Reading register file")
        return self.protocol.regfile_read()

    def regfile_write(self, regs : bytes) -> bytearray:
        """
        Writes the AVR register file (R0::R31)

        :param data: 32 byte register file content as bytearray
        :raises ValueError: if 32 bytes are not given
        """
        self.logger_loc.debug("Writing register file")
        return self.protocol.regfile_write(regs)
