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

# pylint: disable=line-too-long, consider-using-f-string
class XAvrDebugger(AvrDebugger):
    """
    AVR debugger wrapper

    :param transport: transport object to communicate through
    :type transport: object(hid_transport)
    :param use_events_for_run_stop_state: True to use HID event channel, False to polling
    :type use_events_for_run_stop_state: boolean
    """
    def __init__(self, transport, device, use_events_for_run_stop_state=True):
        if transport.hid_device is not None:
            super().__init__(transport)
        # Gather device info
        # moved here so that we have mem + device info even before dw has been started
        try:
            self.device_info = deviceinfo.getdeviceinfo("pyavrocd.deviceinfo.devices." + device)
        except ImportError:
            raise PymcuprogNotSupportedError("No device info for device: {}".format(device)) #pylint: disable=raise-missing-from
        if self.device_info['interface'].upper() !="UPDI" and \
           'DEBUGWIRE' not in self.device_info['interface'].upper():
            raise PymcuprogToolConfigurationError("pymcuprog debug wrapper only supports UPDI and debugWIRE devices")

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
        if self.device_info['interface'].upper() == "UPDI":
            self.device = NvmAccessProviderCmsisDapUpdi(self.transport, self.device_info, frequency, options)
            # Default setup for NVM Access Provider is prog session - override with debug info
            self.device.avr.setup_debug_session(interface=Avr8Protocol.AVR8_PHY_INTF_PDI_1W,
                                                khz=frequency // 1000,
                                                use_hv=Avr8Protocol.UPDI_HV_NONE)
        elif "DEBUGWIRE" in self.device_info['interface'].upper():
            # This starts a debugWIRE session. All the complexities of programming and
            # disabling the DWEN fuse bit and power-cycling is delegated to the calling
            # program
            self.device = XNvmAccessProviderCmsisDapDebugwire(self.transport, self.device_info)
            self.device.avr.setup_debug_session()

    # pylint: disable=line-too-long
    def start_debugging(self, flash_data=None):
        """
        Start the debug session

        :param flash_data: flash data content to program in before debugging
        :type flash data: list of bytes
        """
        self.logger.info("Starting debug session")
        self.device.start()
        if "DEBUGWIRE" in self.device_info['interface'].upper():
            self.attach(do_break=True)
        if self.device_info['interface'].upper() == "UPDI":
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
