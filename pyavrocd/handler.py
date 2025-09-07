"""
This is the RSP command handler module.
"""

# args, logging
from logging import getLogger


# utilities
import binascii
import time

# communication
import select

from pyedbglib.protocols.avrispprotocol import AvrIspProtocolError
from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.protocols.edbgprotocol import EdbgProtocol
from pymcuprog.pymcuprog_errors import PymcuprogNotSupportedError, PymcuprogError

from pyavrocd.memory import Memory
from pyavrocd.breakexec import BreakAndExec, NOSIG, SIGHUP, SIGINT, SIGILL, SIGTRAP, SIGABRT
from pyavrocd.monitor import MonitorCommand
from pyavrocd.livetests import LiveTests
from pyavrocd.errors import  EndOfSession, FatalError
from pyavrocd.deviceinfo.devices.alldevices import dev_name

RECEIVE_BUFFER = 1024

class GdbHandler():
    """
    GDB handler
    Maps between incoming GDB requests and AVR debugging protocols (via pymcuprog)
    """
    def __init__ (self, comsocket, avrdebugger, devicename, args):
        self.packet_size = RECEIVE_BUFFER - 20
        self.logger = getLogger('pyavrocd.handler')
        self.rsp_logger = getLogger('pyavrocd.rsp')
        self.dbg = avrdebugger
        self.mon = MonitorCommand(self.dbg.iface, args)
        self.mem = Memory(avrdebugger, self.mon)
        self.bp = BreakAndExec(1, self.mon, avrdebugger, self.mem.flash_read_word)
        self._comsocket = comsocket
        self._devicename = devicename
        self.last_sigval = 0
        self._lastmessage = ""
        self._extended_remote_mode = False
        self._vflashdone = False # set to True after vFlashDone received
        self.critical = None
        self._live_tests = LiveTests(self)
        self.packettypes = {
            '!'           : self._extended_remote_handler,
            '?'           : self._stop_reason_handler,
            'c'           : self._continue_handler,
            'C'           : self._continue_with_signal_handler, # signal will be ignored
            'D'           : self._detach_handler,
            'g'           : self._get_register_handler,
            'G'           : self._set_register_handler,
            'H'           : self._set_thread_handler,
          # 'k'           : kill - never used because vKill is supported
            'm'           : self._get_memory_handler,
            'M'           : self._set_memory_handler,
            'p'           : self._get_one_register_handler,
            'P'           : self._set_one_register_handler,
            'qAttached'   : self._attached_handler,
            'qOffsets'    : self._offsets_handler,
            'qRcmd'       : self._monitor_cmd_handler,
            'qSupported'  : self._supported_handler,
            'qfThreadInfo': self._first_thread_info_handler,
            'qsThreadInfo': self._subsequent_thread_info_handler,
            'qXfer'       : self._memory_map_handler,
          # 'Q'           : general set commands - no relevant cases
          # 'R'           : run command - never used because vRun is supported
            's'           : self._step_handler,
            'S'           : self._step_with_signal_handler, # signal will be ignored
            'T'           : self._thread_alive_handler,
            'vCont'       : self._vcont_handler,
            'vFlashDone'  : self._vflash_done_handler,
            'vFlashErase' : self._vflash_erase_handler,
            'vFlashWrite' : self._vflash_write_handler,
            'vKill'       : self._kill_handler,
            'vRun'        : self._run_handler,
            'X'           : self._set_binary_memory_handler,
            'z'           : self._remove_breakpoint_handler,
            'Z'           : self._add_breakpoint_handler,
            }


    def dispatch(self, cmd, packet):
        """
        Dispatches command to the right handler
        """
        if cmd is None: # This is a timeout
            if self.mem.lazy_loading: # while we were loading an executable
                self._set_binary_memory_handler_finalize(None)
            return
        try:
            handler = self.packettypes[cmd]
        except (KeyError, IndexError):
            self.logger.debug("Unhandled GDB RSP packet type: %s", cmd)
            self.send_packet("")
            return
        try:
            if cmd not in {'X', 'vFlashWrite'}: # no binary data in packet
                packet = packet.decode('ascii')
            handler(packet)
        except (FatalError, PymcuprogNotSupportedError, PymcuprogError, AssertionError) as e:
            self.logger.critical(e)
            if not self.critical:
                self.critical = e
            self.send_signal(SIGABRT)

    def _extended_remote_handler(self, _):
        """
        '!': GDB tries to switch to extended remote mode and we accept
        """
        self.logger.debug("RSP packet: set extended remote")
        self._extended_remote_mode = True
        self.send_packet("OK")

    def _stop_reason_handler(self, _):
        """
        '?': Send reason for last stop: the last signal
        """
        self.logger.debug("RSP packet: ask for last stop reason")
        if not self.last_sigval:
            self.last_sigval = NOSIG
        self.send_packet("S{:02X}".format(self.last_sigval))
        self.logger.debug("Reason was %s",self.last_sigval)

    def __debugger_is_active(self):
        """
        Internal method for continue and step:
        Checks whether debugger is active and flash is loaded. If not,
        a signal is sent, a warning message is printed and False is returned
        """
        if self.critical:
            self.send_debug_message("Cannot execute after critical error:")
            self.send_debug_message(str(self.critical))
            self.send_signal(SIGABRT)
            return False
        if not self.mon.is_debugger_active():
            self.logger.warning("Cannot start execution because not connected to OCD")
            if "debugwire" == self.dbg.iface:
                self.send_debug_message("Enable debugWIRE first: 'monitor debugwire enable'")
            elif "jtag" in self.dbg.iface:
                self.send_debug_message("JTAG pins are not enabled.")
            else:
                self.send_debug_message("No connection to OCD. Enable debugging first")
            self.send_signal(SIGHUP)
            return False
        if self.mem.is_flash_empty() and not self.mon.is_noload():
            self.logger.warning("Cannot start execution without prior loading of executable")
            self.send_debug_message("No program loaded; cannot start execution")
            self.send_signal(SIGILL)
            return False
        return True

    def __send_execution_result_signal(self, sig):
        """
        Internal method for continue and step:
        Print message and send signal according the result of the execution.
        """
        if sig == SIGABRT:
            self.send_debug_message("Too many breakpoints set")
            self.logger.warning("Too many breakpoints.")
        if sig == SIGILL:
            self.send_debug_message("Cannot execute because of user supplied BREAK instruction")
            self.logger.warning("Cannot execute because of user supplied BREAK instruction")
        if sig is not None:
            self.send_signal(sig)


    def _continue_handler(self, packet):
        """
        'c': Continue execution, either at current address or at given address
        """
        self.logger.debug("RSP packet: Continue")
        if not self.__debugger_is_active():
            return
        newpc = None
        if packet:
            newpc = int(packet,16)
            self.logger.debug("Set PC to 0x%X before resuming execution", newpc)
        self.__send_execution_result_signal(self.bp.resume_execution(newpc))

    def _continue_with_signal_handler(self, packet):
        """
        'C': continue with signal, which we ignore here
        """
        self._continue_handler((packet+";").split(";")[1])

    def _detach_handler(self, _):
        """
       'D': Detach. All the real housekeeping will take place when the connection is terminated
        """
        self.logger.debug("RSP packet: Detach")
        self.send_packet("OK")
        raise EndOfSession("Session ended by client ('detach')")

    def _get_register_handler(self, _):
        """
        'g': Send the current register values R[0:31] + SREG + SP + PC to GDB
        """
        self.logger.debug("RSP packet: GDB reading registers")
        if self.mon.is_debugger_active():
            regs = self.dbg.register_file_read()
            sreg = self.dbg.status_register_read()
            sp = self.dbg.stack_pointer_read()
            # get PC as word address and make a byte address
            pc = self.dbg.program_counter_read() << 1
            reg_string = ""
            for reg in regs:
                reg_string = reg_string + format(reg, '02x')
            sreg_string = ""
            for reg in sreg:
                sreg_string = sreg_string + format(reg, '02x')
            sp_string = ""
            for reg in sp:
                sp_string = sp_string + format(reg, '02x')
            pcstring = binascii.hexlify(pc.to_bytes(4,byteorder='little')).decode('ascii')
            reg_string = reg_string + sreg_string + sp_string + pcstring
        else:
            reg_string = \
               "0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2000341200000000"
        self.send_packet(reg_string)
        self.logger.debug("Data sent: %s", reg_string)


    def _set_register_handler(self, packet):
        """
        'G': Receive new register ( R[0:31] + SREAG + SP + PC) values from GDB
        """
        self.logger.debug("RSP packet: GDB writing registers")
        self.logger.debug("Data received: %s", packet)
        if self.mon.is_debugger_active():
            newdata = binascii.unhexlify(packet)
            self.dbg.register_file_write(newdata[:32])
            self.dbg.status_register_write(newdata[32:33])
            self.dbg.stack_pointer_write(newdata[33:35])
            self.dbg.program_counter_write((int(binascii.hexlify(
                                          bytes(reversed(newdata[35:]))),16)) >> 1)
            self.logger.debug("Setting new register data from GDB: %s", packet)
        self.send_packet("OK")

    def _set_thread_handler(self, _):
        """
        'H': set thread id for next operation. Since we only have one, it is always OK
        """
        self.logger.debug("RSP packet: Set current thread")
        self.send_packet('OK')

    def _get_memory_handler(self, packet):
        """
        'm': provide GDB with memory contents
        """
        if not self.mon.is_debugger_active():
            self.logger.debug("RSP packet: memory read, but not connected")
            self.send_packet("E01")
            return
        addr = packet.split(",")[0]
        size = packet.split(",")[1]
        isize = int(size, 16)
        self.logger.debug("RSP packet: Reading memory: addr=%s, size=%d", addr, isize)
        if isize == 0:
            self.send_packet("OK")
            return
        data = self.mem.readmem(addr, size)
        if data:
            data_string = (binascii.hexlify(data)).decode('ascii')
            self.logger.debug("Data retrieved: %s", data_string)
            self.send_packet(data_string)
        else:
            self.logger.error("Cannot access memory for address 0x%s", addr)
            self.send_packet("E14")

    def _set_memory_handler(self, packet):
        """
        'M': GDB sends new data for MCU memory
        """
        if not self.mon.is_debugger_active():
            self.logger.debug("RSP packet: Memory write, but not connected")
            self.send_packet("E01")
            return
        addr = packet.split(",")[0]
        size = (packet.split(",")[1]).split(":")[0]
        data = (packet.split(",")[1]).split(":")[1]
        self.logger.debug("RSP packet: Memory write addr=%s, size=%s, data=%s", addr, size, data)
        data = binascii.unhexlify(data)
        if len(data) != int(size,16):
            self.logger.error("Size of data packet does not fit: %s", packet)
            self.send_packet("E15")
            return
        reply = self.mem.writemem(addr, data)
        self.send_packet(reply)


    def _get_one_register_handler(self, packet):
        """
        'p': read register and send to GDB
        currently only PC
        """
        if not self.mon.is_debugger_active():
            self.logger.debug("RSP packet: read register command, but not connected")
            self.send_packet("E01")
            return
        if packet == "22":
            # GDB defines PC register for AVR to be REG34(0x22)
            # and the bytes have to be given in reverse order (big endian)
            pc = self.dbg.program_counter_read() << 1
            self.logger.debug("RSP packet: read PC command: 0x%X", pc)
            pc_byte_string = binascii.hexlify((pc).to_bytes(4,byteorder='little')).decode('ascii')
            self.send_packet(pc_byte_string)
        elif packet == "21": # SP
            sp_byte_string = "%02X%02X" % tuple(self.dbg.stack_pointer_read())
            self.logger.debug("RSP packet: read SP command (little endian): 0x%s", sp_byte_string)
            self.send_packet(sp_byte_string)
        elif packet == "20": # SREG
            sreg_byte_string =  "%02X" % self.dbg.status_register_read()[0]
            self.logger.debug("RSP packet: read SREG command: 0x%s", sreg_byte_string)
            self.send_packet(sreg_byte_string)
        else:
            reg_byte_string =  (binascii.hexlify(self.dbg.sram_read(int(packet,16), 1))).\
                                   decode('ascii')
            self.logger.debug("RSP packet: read Reg%s command: 0x%s", packet, reg_byte_string)
            self.send_packet(reg_byte_string)

    def _set_one_register_handler(self, packet):
        """
        'P': set a single register with a new value given by GDB
        """
        if not self.mon.is_debugger_active():
            self.logger.debug("RSP packet: write register command, but not connected")
            self.send_packet("E01")
            return
        if packet[0:3] == "22=": # PC
            pc = int(binascii.hexlify(bytearray(reversed(binascii.unhexlify(packet[3:])))),16)
            self.logger.debug("RSP packet: write PC=0x%X", pc)
            self.dbg.program_counter_write(pc>>1) # write PC as word address
        elif packet[0:3] == "21=": # SP (already in little endian order)
            self.logger.debug("RSP packet: write SP (little endian)=%s", packet[3:])
            self.dbg.stack_pointer_write(binascii.unhexlify(packet[3:]))
        elif packet[0:3] == "20=": # SREG
            self.logger.debug("RSP packet: write SREG=%s",packet[3:])
            self.dbg.status_register_write(binascii.unhexlify(packet[3:]))
        else:
            self.logger.debug("RSP packet: write REG%d=%s",int(packet[0:2],16),packet[3:])
            self.dbg.sram_write(int(packet[0:2],16), binascii.unhexlify(packet[3:]))
        self.send_packet("OK")


    def _attached_handler(self, _):
        """
        'qAttached': whether detach or kill will be used when quitting GDB
        """
        self.logger.debug("RSP packet: attached query, will answer '1'")
        self.send_packet("1")

    def _offsets_handler(self, _):
        """
        'qOffsets': Querying offsets of the different memory areas
        """
        self.logger.debug("RSP packet: offset query, will answer 'Text=000;Data=000;Bss=000'")
        self.send_packet("Text=000;Data=000;Bss=000")

    def _monitor_cmd_handler(self, packet):
        """
        'qRcmd': Monitor commands that directly get info or set values in the gdbserver
        """
        payload = packet[1:]
        self.logger.debug("RSP packet: monitor command: %s"
                              ,binascii.unhexlify(payload).decode('ascii'))
        tokens = binascii.unhexlify(payload).decode('ascii').split()
        try:
            response = self.mon.dispatch(tokens)
            if response[0] == 'dwon':
                if self.critical:
                    raise FatalError(self.critical)
                self.dbg.prepare_debugging(callback=self.__send_power_cycle,
                                               recognition=self.__send_ready_message)
                self.dbg.start_debugging()
                # will only be called if there was no error in connecting to OCD:
                self.mon.set_debug_mode_active()
            elif response[0] == 'dwoff':
                self.dbg.dw_disable()
                self.mon.set_debug_mode_active(False)
            elif response[0] == 'reset':
                self.dbg.reset()
            elif response[0] in [0, 1]:
                self.dbg.device.avr.protocol.set_byte(Avr8Protocol.AVR8_CTXT_OPTIONS,
                                                    Avr8Protocol.AVR8_OPT_RUN_TIMERS,
                                                    response[0])
            elif 'power o' in response[0]:
                self.dbg.edbg_protocol.set_byte(EdbgProtocol.EDBG_CTXT_CONTROL,
                                                    EdbgProtocol.EDBG_CONTROL_TARGET_POWER,
                                                    'on' in response[0])
            elif 'power q' in response[0]:
                resp = self.dbg.edbg_protocol.query(EdbgProtocol.EDBG_QUERY_COMMANDS)
                self.logger.info("Commands: %s", resp)
            elif 'info' in response[0]:
                response = ("",
                            response[1].format(dev_name[self.dbg.device_info['device_id']]))
            elif 'live_tests' in response[0]:
                self._live_tests.run_tests()
        except AvrIspProtocolError:
            self.logger.critical("ISP programming failed. Wrong connection or wrong MCU?")
            self.send_reply_packet("ISP programming failed. Wrong connection or wrong MCU?")
        except (FatalError, PymcuprogNotSupportedError, PymcuprogError) as e:
            self.logger.critical(e)
            if not self.critical:
                self.critical = e
            self.send_reply_packet("Fatal error: %s" % e)
        else:
            self.send_reply_packet(response[1])


    def __send_power_cycle(self):
        """
        This is a call back function that will try to power-cycle
        automagically. If successful, it will return True.
        Otherwise, it will ask user to power-cycle and return False.
        """
        if self.dbg.transport.device.product_string.lower().startswith('medbg'):
            # mEDBG are the only ones it will work with, I believe.
            # I tried to use a try/except construction,
            # but this confuses the debugger and it is stuck
            # in an illegal state (the housekeeper does not respond)
            self.logger.info("Try automatic power-cycling")
            self.dbg.edbg_protocol.set_byte(EdbgProtocol.EDBG_CTXT_CONTROL,
                                                EdbgProtocol.EDBG_CONTROL_TARGET_POWER,
                                                0)
            time.sleep(0.5)
            self.dbg.edbg_protocol.set_byte(EdbgProtocol.EDBG_CTXT_CONTROL,
                                                EdbgProtocol.EDBG_CONTROL_TARGET_POWER,
                                                1)
            time.sleep(0.1)
            self.logger.info("Automatic power-cycling successful")
            return True
        self.send_debug_message("*** Please power-cycle the target system ***")
        return False

    def __send_ready_message(self):
        self.send_debug_message("*** Power-down recognized. Apply power again! ***")

    def _supported_handler(self, _):
        """
        'qSupported': query for features supported by the gbdserver; in our case
        packet size and memory map. Because this is also the command send after a
        connection with 'target remote' is made,
        we will try to establish a connection to the target OCD
        """
        self.logger.debug("RSP packet: qSupported query.")
        self.logger.debug("Will answer 'PacketSize=%X;qXfer:memory-map:read+'",
                              self.packet_size)
        # Try to start a debugging session. If we are unsuccessful,
        # one has to use the 'monitor debugwire on' command later on
        # If a fatal error is raised, we will remember that and print it again
        # when a request for enabling debugWIRE is made
        try:
            if self.dbg.start_debugging(warmstart=self.dbg.iface=='debugwire'):
                self.mon.set_debug_mode_active()
        except FatalError as e:
            self.logger.critical("Error while connecting to target OCD: %s", e)
            if not self.critical:
                self.critical = e
            self.dbg.stop_debugging()
        self.logger.debug("debugger_active=%d",self.mon.is_debugger_active())
        self.send_packet("PacketSize={0:X};qXfer:memory-map:read+".format(self.packet_size))

    def _first_thread_info_handler(self, _):
        """
        'qfThreadInfo': get info about active threads
        """
        self.logger.debug("RSP packet: first thread info query, will answer 'm01'")
        self.send_packet("m01")

    def _subsequent_thread_info_handler(self, _):
        """
        'qsThreadInfo': get more info about active threads
        """
        self.logger.debug("RSP packet: subsequent thread info query, will answer 'l'")
        self.send_packet("l") # the previously given thread was the last one

    def _memory_map_handler(self, packet):
        """
        'qXfer:memory-map:read' - provide info about memory map so that the vFlash commands are used
        """
        if ":memory-map:read" in packet and not self.mon.is_noxml():
            self.logger.debug("RSP packet: memory map query")
            mmap = self.mem.memory_map()
            self.send_packet(mmap)
            self.logger.debug("Memory map=%s", mmap)
        else:
            self.logger.debug("Unhandled query: qXfer%s", packet)
            self.send_packet("")

    def _step_handler(self, packet):
        """
        's': single step, perhaps starting at a different address
        """
        if not self.__debugger_is_active():
            return
        newpc = None
        if packet:
            newpc = int(packet,16)
            self.logger.debug("Set PC to 0x%X before single step",newpc)
        self.__send_execution_result_signal(self.bp.single_step(newpc))


    def _step_with_signal_handler(self, packet):
        """
        'S': single-step with signal, which we ignore here
        """
        self._step_handler((packet+";").split(";")[1])

    def _thread_alive_handler(self, _):
        """
        'T': Is thread still alive? Yes, always!
        """
        self.logger.debug("RSP packet: thread alive query, will answer 'OK'")
        self.send_packet('OK')

    def _vcont_handler(self, packet):
        """
        'vCont': eversything about execution
        """
        self.logger.debug("RSP packet: vCont")
        if packet == '?': # asks for capabilities
            self.logger.debug("Tell GDB about vCont capabilities: c, C, s, S, r")
            self.send_packet("vCont;c;C;s;S;r")
        elif packet[0] == ';':
            if packet[1] in ['c', 'C']:
                self._continue_handler("")
            elif packet[1] in ['s', 'S']:
                self._step_handler("")
            elif packet[1] == 'r':
                step_range = packet[2:].split(':')[0].split(',')
                self.__send_execution_result_signal(
                    self.bp.range_step(int(step_range[0],16), int(step_range[1],16)))
            else:
                self.send_packet("") # unknown
        else:
            self.send_packet("") # unknown


    def _vflash_done_handler(self, _):
        """
        'vFlashDone': everything is there, now we can start flashing!
        """
        self.logger.debug("RSP packet: vFlashDone")
        self._vflashdone = True
        try:
            self.dbg.device.avr.switch_to_progmode()
            self.mem.programming_mode = True
            self.logger.info("Programming mode entered")
            self.mem.flash_pages()
        except:
            self.logger.error("Flashing was unsuccessful")
            self.send_packet("E11")
            raise
        finally:
            self.dbg.device.avr.switch_to_debmode()
            self.mem.programming_mode = False
            self.logger.info("Programming mode stopped")
        self.send_packet("OK")

    def _vflash_erase_handler(self, _):
        """
        'vFlashErase': We use this command to clear the cache when there was a previous
        vFlashDone command, and erase chip if possible.
        """
        self.logger.debug("RSP packet: vFlashErase")
        if self.mon.is_debugger_active():
            self.bp.cleanup_breakpoints()
            if self.mon.is_erase_before_load():
                # if erase is not possible or desired, then it is done before flashing each page (perhaps implicitly)
                self.dbg.device.erase_chip(self.mem.programming_mode)
            if self._vflashdone:
                self._vflashdone = False
                self.mem.init_flash() # clear cache
            if self.mem.is_flash_empty():
                self.logger.info("Loading executable")
            self.send_packet("OK")
        else:
            self.send_packet("E01")

    def _vflash_write_handler(self, packet):
        """
        'vFlashWrite': chunks of the program data we need to flash
        """
        addrstr = (packet.split(b':')[1]).decode('ascii')
        data = self.unescape(packet[len(addrstr)+2:])
        addr = int(addrstr, 16)
        self.logger.debug("RSP packet: vFlashWrite starting at 0x%04X", addr)
        #insert new block in flash cache
        self.mem.store_to_cache(addr, data)
        self.send_packet("OK")

    @staticmethod
    def escape(data):
        """
        Escape binary data to be sent to Gdb.

        :param: data Bytes-like object containing raw binary.
        :return: Bytes object with the characters in '#$}*' escaped as required by Gdb.
        """
        result = []
        for c in data:
            if c in tuple(b'#$}*'):
                # Escape by prefixing with '}' and xor'ing the char with 0x20.
                result += [0x7d, c ^ 0x20]
            else:
                result.append(c)
        return bytes(result)

    @staticmethod
    def unescape(data):
        """
        De-escapes binary data from Gdb.

        :param: data Bytes-like object with possibly escaped values.
        :return: List of integers in the range 0-255, with all escaped bytes de-escaped.
        """
        result = []
        unquote = False

        for c in data:
            if unquote:
                result.append(c ^ 0x20)
                unquote = False
            elif c == 0x7d:
                unquote = True
            else:
                result.append(c)

        return result

    def _kill_handler(self, _):
        """
        'vKill': Kill command. Will be called, when the user requests a 'kill', but also
        when in extended-remote mode, when a 'run' is issued. In ordinary remote mode, it
        will disconnect, in extended-remote it will not, and you can restart or load a modified
        file and run that one.
        """
        self.logger.debug("RSP packet: kill process, will reset MCU")
        if self.mon.is_debugger_active():
            self.dbg.reset()
        self.send_packet("OK")
        if not self._extended_remote_mode:
            self.logger.debug("Terminating session ...")
            raise EndOfSession

    def _run_handler(self, _):
        """
        'vRun': reset and wait to be started from address 0
        """
        self.logger.debug("RSP packet: run")
        if not self.__debugger_is_active():
            return
        self.logger.debug("Resetting MCU and wait for start")
        self.dbg.reset()
        self.send_signal(SIGTRAP)

    def _set_binary_memory_handler(self, packet):
        """
        'X': Binary load
        """
        addr = (packet.split(b',')[0]).decode('ascii')
        size = int(((packet.split(b',')[1]).split(b':')[0]).decode('ascii'),16)
        data = self.unescape((packet.split(b':',1)[1]))
        self.logger.debug("RSP packet: X, addr=0x%s, length=%d, data=%s", addr, size, data)
        if not self.mon.is_debugger_active() and size > 0:
            self.logger.debug("RSP packet: Memory write, but not connected")
            self.send_packet("E01")
            return
        if len(data) != size:
            self.logger.error("Size of data packet %d does not fit data length %d",size,len(data))
            self.logger.error("Data: %s", data)
            self.send_packet("E15")
            return
        if int(addr,16) < 0x80000: # writing to flash
            if not self.mem.lazy_loading:
                self.logger.info("Loading executable")
                self.bp.cleanup_breakpoints() # cleanup breakpoints before load
                self.mem.lazy_loading = True
                self.dbg.device.avr.switch_to_progmode()
                self.mem.programming_mode = True
                self.logger.info("Switched to programming mode")
                if self.mon.is_erase_before_load():
                    # If erase before load is requested, we do that here
                    # otherwise it will done implicitly before each page is programmed
                    self.dbg.device.erase_chip(self.mem.programming_mode)
        try:
            reply = self.mem.writemem(addr, bytearray(data))
        except:
            self.logger.error("Loading binary data was unsuccessful")
            self.send_packet("E11")
            raise
        self.send_packet(reply)

    def _set_binary_memory_handler_finalize(self, _):
        """
        This method is called when the server function times out after 1 second
        while mem.lazy_loading = True, meaning there is an executable loaded using
        the X-records.
        """
        self.logger.debug("Finalize binary programming")
        self.mem.lazy_loading = False
        self.mem.flash_pages() # program the remaining bytes
        self.dbg.device.avr.switch_to_debmode()
        self.mem.programming_mode = False
        self.logger.info("Programming mode stopped")


    def _remove_breakpoint_handler(self, packet):
        """
        'z': Remove a breakpoint
        """
        breakpoint_type = packet[0]
        addr = packet.split(",")[1]
        self.logger.debug("RSP packet: remove BP of type %s at %s", breakpoint_type, addr)
        if breakpoint_type in {"0", "1"}:
            self.bp.remove_breakpoint(int(addr, 16))
            self.send_packet("OK")
        else:
            self.logger.debug("Breakpoint type %s not supported", breakpoint_type)
            self.send_packet("")

    def _add_breakpoint_handler(self, packet):
        """
        'Z': Set a breakpoint
        """
        breakpoint_type = packet[0]
        addr = packet.split(",")[1]
        self.logger.debug("RSP packet: set BP of type %s at %s", breakpoint_type, addr)
        if breakpoint_type in {"0", "1"}:
            self.bp.insert_breakpoint(int(addr, 16))
            self.send_packet("OK")
        else:
            self.logger.error("Breakpoint type %s not supported", breakpoint_type)
            self.send_packet("")

    def poll_events(self):
        """
        Checks the AvrDebugger for incoming events (breaks)
        """
        if not self.mon.is_debugger_active() or self.mem.programming_mode:
            # if DW is not enabled yet or we are in programming mode, simply return
            return
        pc = self.dbg.poll_event()
        if pc:
            self.logger.debug("MCU stopped execution")
            self.send_signal(SIGTRAP)

    def poll_gdb_input(self):
        """
        Checks whether input from GDB is waiting. If so while singelstepping, we might stop.
        """
        ready = select.select([self._comsocket], [], [], 0) # just look, never wait
        return bool(ready[0])

    def send_packet(self, packet_data):
        """
        Sends a GDB response packet
        """
        checksum = sum(packet_data.encode("ascii")) % 256
        message = "$" + packet_data + "#" + format(checksum, '02x')
        self.rsp_logger.debug("<- %s", message)
        self._lastmessage = packet_data
        self._comsocket.sendall(message.encode("ascii"))

    def send_reply_packet(self, mes):
        """
        Send a packet as a reply to a monitor command to be displayed in the debug console
        """
        self.send_packet(binascii.hexlify(bytearray((mes+"\n").\
                                                    encode('utf-8'))).decode("ascii").upper())

    def send_debug_message(self, mes):
        """
        Send a packet that always should be displayed in the debug console when the system
        is in 'running' mode.
        """
        self.send_packet('O' + binascii.hexlify(bytearray((mes+"\n").\
                                                    encode('utf-8'))).decode("ascii").upper())

    def send_signal(self, signal):
        """
        Sends signal to GDB
        """
        self.last_sigval = signal
        if signal: # do nothing if None or 0
            if signal in [SIGHUP, SIGILL, SIGABRT]:
                self.send_packet("S{:02X}".format(signal))
                return
            sreg = self.dbg.status_register_read()[0]
            spl, sph = self.dbg.stack_pointer_read()
            # get PC as word address and make a byte address
            pc = self.dbg.program_counter_read() << 1
            pcstring = binascii.hexlify(pc.to_bytes(4,byteorder='little')).decode('ascii')
            stoppacket = "T{:02X}20:{:02X};21:{:02X}{:02X};22:{};thread:1;".\
              format(signal, sreg, spl, sph, pcstring)
            self.send_packet(stoppacket)

    def handle_data(self, data):
        """
        Analyze the incoming data stream from GDB. Allow more than one RSP record
        per packet, although this should not be necessary because each packet needs
        to be acknowledged by a '+' from us.
        """
        if data is None: # timeout
            self.dispatch(None, None)
            return
        while data:
            if data[0] == ord('+'): # ACK
                self.rsp_logger.debug("-> +")
                data = data[1:]
                # if no ACKs/NACKs are following, delete last message
                if not data or data[0] not in b'+-':
                    self._lastmessage = None
            elif data[0] == ord('-'): # NAK, resend last message
                # remove multiple '-'
                i = 0
                while (i < len(data) and data[i] == ord('-')):
                    i += 1
                data = data[i:]
                self.rsp_logger.debug("-> -")
                if self._lastmessage:
                    self.logger.debug("Resending packet to GDB")
                    self.send_packet(self._lastmessage)
                else:
                    self.send_packet("")
            elif data[0] == 3: # CTRL-C
                self.logger.info("CTRL-C")
                self.dbg.stop()
                self.send_signal(SIGINT)
                #self._comsocket.sendall(b"+")
                #self.rsp_logger.debug("<- +")
                data = data[1:]
            elif data[0] == ord('$'): # start of message
                valid_data = True
                self.rsp_logger.debug('-> %s', data)
                checksum = (data.split(b"#")[1])[:2]
                packet_data = (data.split(b"$")[1]).split(b"#")[0]
                if int(checksum, 16) != sum(packet_data) % 256:
                    self.logger.warning("Checksum Wrong in packet: %s", data)
                    valid_data = False
                if not valid_data:
                    self._comsocket.sendall(b"-")
                    self.rsp_logger.debug("<- -")
                else:
                    self._comsocket.sendall(b"+")
                    self.rsp_logger.debug("<- +")
                    # now split into command and data (or parameters) and dispatch
                    if chr(packet_data[0]) not in {'v', 'q', 'Q'}:
                        i = 1
                    else:
                        for i in range(len(packet_data)+1):
                            if i == len(packet_data) or not chr(packet_data[i]).isalpha():
                                break
                    self.dispatch(packet_data[:i].decode('ascii'),packet_data[i:])
                data = data[(data.index(b"#")+2):]
            else: # ignore character
                data = data[1:]

