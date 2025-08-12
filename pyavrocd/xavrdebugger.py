"""
Python AVR MCU debugger
"""

from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.protocols.edbgprotocol import EdbgProtocol
from pyedbglib.util import binary

from pymcuprog.avrdebugger import AvrDebugger
from pymcuprog.deviceinfo import deviceinfo
from pymcuprog.nvmupdi import NvmAccessProviderCmsisDapUpdi
from pymcuprog.pymcuprog_errors import PymcuprogToolConfigurationError,\
     PymcuprogNotSupportedError

from pyavrocd.xnvmdebugwire import XNvmAccessProviderCmsisDapDebugwire
from pyavrocd.xnvmmegaavrjtag import XNvmAccessProviderCmsisDapMegaAvrJtag

class XAvrDebugger(AvrDebugger):
    """
    AVR debugger wrapper

    :param transport: transport object to communicate through
    :type transport: object(hid_transport)
    :param use_events_for_run_stop_state: True to use HID event channel, False to polling
    :type use_events_for_run_stop_state: boolean
    """
    def __init__(self, transport, device, iface, use_events_for_run_stop_state=True):
        self.device = device
        self.iface = iface
        _dummy = use_events_for_run_stop_state
        self.debugger_stopped = False
        if transport.hid_device is not None:
            super().__init__(transport)
        # Gather device info
        # moved here so that we have mem + device info even before dw has been started
        try:
            self.device_info = deviceinfo.getdeviceinfo("pyavrocd.deviceinfo.devices." + device)
        except ImportError:
            raise PymcuprogNotSupportedError("No device info for device: {}".format(device)) #pylint: disable=raise-missing-from
        if iface not in self.device_info['interface'].lower():
            raise PymcuprogToolConfigurationError("Incompatible debugging interface")

        # Memory info for the device
        self.memory_info = deviceinfo.DeviceMemoryInfo(self.device_info)
        # ISP interface in order to program DWEN fuse
        self.spidevice = None
        if transport and transport.hid_device is not None:
            self.edbg_protocol = EdbgProtocol(transport) # necessary to access target power control

    def setup_session(self, device, frequency=900000, options=""):
        """
        Sets up the device for a debug session

        :param device: name of the device to debug
        :param frequency: UPDI clock frequency in Hz
        :type frequency: int
        :param options: dictionary of options for starting the session
        :type options: dict
        """
        self.logger.info("Setting up %s for debugging", device)


        # Start a session
        if self.iface == "updi":
            self.device = NvmAccessProviderCmsisDapUpdi(self.transport, self.device_info, frequency, options)
            # Default setup for NVM Access Provider is prog session - override with debug info
            self.device.avr.setup_debug_session(interface=Avr8Protocol.AVR8_PHY_INTF_PDI_1W,
                                                khz=frequency // 1000,
                                                use_hv=Avr8Protocol.UPDI_HV_NONE)
        elif self.iface == "debugwire":
            # This starts a debugWIRE session. All the complexities of programming and
            # disabling the DWEN fuse bit and power-cycling is delegated to the calling
            # program
            self.device = XNvmAccessProviderCmsisDapDebugwire(self.transport, self.device_info)
            self.device.avr.setup_debug_session()
        elif self.iface == "jtag":
            self.device = XNvmAccessProviderCmsisDapMegaAvrJtag(self.transport, self.device_info)
            self.device.avr.setup_prog_session()
            self.logger.debug("Enabled prog (not debug) session")
            self.device.avr.protocol.enter_progmode()
            ocdenbyte = self.read_fuse(1,1) # needs generalization
            self.logger.debug("Read fuse byte containing OCDEN: 0x%x", ocdenbyte)
            ocdenbyte &= ~0x80 # needs generalization
            self.logger.debug("New fuse byte containing OCDEN: 0x%x", ocdenbyte)
            self.write_fuse(1, bytearray([ocdenbyte]))
            self.logger.debug("Enabled OCD fuse")
            self.device.avr.protocol.leave_progmode()
            #self.device.avr.setup_debug_session()


    def start_debugging(self, flash_data=None):
        """
        Start the debug session

        :param flash_data: flash data content to program in before debugging
        :type flash data: list of bytes
        """
        self.logger.info("Starting debug session")
        self.device.start()
        if self.iface == 'jtag':
            self.attach(do_break=True)
            self.logger.info("Attached to OCD")
        if self.iface == 'debugwire':
            self.attach(do_break=True)
            self.logger.info("Attached to OCD")
        if self.iface == "updi":
            # The UPDI device is now in prog mode
            device_id = self.device.read_device_id()
            self.logger.debug("Device ID read: %X", binary.unpack_le24(device_id))
            # If the user wants content on the AVR, put it there now
            if flash_data:
                if not isinstance(flash_data, list):
                    raise PymcuprogNotSupportedError("Content can only be provided as a list of binary values")
                # First chip-erase
                self.logger.info("Erasing target")
                self.device.erase()
                # Then program
                self.logger.info("Programming target")
                self.device.write(self.memory_info.memory_info_by_name('flash'), 0, flash_data)
                # Flush events before starting
                self.flush_events()
                self.logger.info("Leaving prog mode (with auto-attach)")
                self.device.avr.protocol.leave_progmode()
                self._wait_for_break()

    # Cleanup code for detaching target
    def stop_debugging(self, graceful=True):
        """
        Stop the debug session and clean up in a safe way
        """
        if self.debugger_stopped:
            return
        self.logger.info("Terminating debugging session ...")
        try:
            # Halt the core
            self.device.avr.protocol.stop()
            self.logger.info("AVR core stopped")
            # Remove all software breakpoints
            self.device.avr.protocol.software_breakpoint_clear_all()
            self.logger.info("All software breakpoints removed")
            # Remove all hardware  breakpoints
            self.device.avr.breakpoint_clear()
            self.logger.info("All hardware breakpoints removed")
        except Exception as e:
            if not graceful:
                self.logger.info("Error during stopping core and removing BPs: %s", e)
        try:
            # Detach from the OCD
            self.device.avr.protocol.detach()
            self.logger.info("Detached from OCD")
        except Exception as e:
            if not graceful:
                self.logger.info("Error during detaching from OCD: %s", e)
        try:
            # De-activate UPDI physical interface
            self.device.avr.deactivate_physical()
            self.logger.info("Physical interface deactivated")
        except Exception as e:
            if not graceful:
                self.logger.info("Error during deactivating interface: %s", e)
        try:
            # Sign off device
            if self.use_events_for_run_stop_state:
                self.housekeeper.end_session()
                self.logger.info("Housekeeping session stopped")
        except Exception as e:
            if not graceful:
                self.logger.info("Error during termination of housekeeping session: %s", e)
        self.debugger_stopped = True
        self.logger.info("... terminating debugging session done")


    def stack_pointer_write(self, data):
        """
        Writes the stack pointer

        :param data: 2 bytes representing stackpointer in little endian
        :type: bytearray
        """
        self.logger.debug("Writing stack pointer")
        self.device.avr.stack_pointer_write(data)

    def status_register_read(self):
        """
        Reads the status register from the AVR

        :return: 8-bit SREG value
        :rytpe: one byte
        """
        self.logger.debug("Reading status register")
        return self.device.avr.statreg_read()

    def status_register_write(self, data):
        """
        Writes new value to status register
        :param data: SREG
        :type: one byte
        """

        self.logger.debug("Write status register: %s", data)
        self.device.avr.statreg_write(data)

    def register_file_read(self):
        """
        Reads out the AVR register file (R0::R31)

        :return: 32 bytes of register file content as bytearray
        :rtype: bytearray
        """
        self.logger.debug("Reading register file")
        return self.device.avr.regfile_read()

    def register_file_write(self, regs):
        """
        Writes the AVR register file (R0::R31)

        :param data: 32 byte register file content as bytearray
        :raises ValueError: if 32 bytes are not given
        """
        self.logger.debug("Writing register file")
        self.device.avr.regfile_write(regs)

    def reset(self):
        """
        Reset the AVR core.
        The PC will point to the first instruction to be executed.
        """
        self.logger.info("MCU reset")
        self.device.avr.protocol.reset()
        self._wait_for_break()

    def read_fuse(self, addr, size):
        """
        Read fuses (does not work with debugWIRE and in JTAG only when programming mode)
        """
        return self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_FUSES, addr, size)

    def write_fuse(self, addr, data):
        """
        Write fuses (does not work with debugWIRE and in JTAG only in programming mode)
        """
        return self.device.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, addr, data)

    def read_lock(self, addr, size):
        """
        Read lock bits (does not work with debugWIRE and in JTAG only when programming mode)
        """
        return self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, addr, size)

    def write_lock(self, addr, data):
        """
        Write lock bits (does not work with debugWIRE and in JTAG only in programming mode)
        """
        return self.device.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_LOCKBITS, addr, data)

    def read_sig(self, addr, size):
        """
        Read signature in a liberal way, i.e., throwing no errors
        """
        resp = self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_SIGNATURE, 0, 3)
        if size+addr > 3:
            resp += [0xFF]*(addr+size)
        return bytearray(resp[addr:addr+size])

    def read_usig(self, addr, size):
        """
        Read contents of user signature (does not work with debugWIRE)
        """
        return self.device.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_USER_SIGNATURE, addr, size)

    def write_usig(self, addr, data):
        """
        Write user signature
        """
        return self.device.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_USER_SIGNATURE, addr, data)
