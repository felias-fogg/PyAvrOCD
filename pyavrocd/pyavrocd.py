"""
debugWIRE GDBServer
"""
# pylint: disable=too-many-lines, consider-using-f-string

# args, logging
import platform
import importlib.metadata
import sys
import os
import argparse
import logging
from logging import getLogger
import textwrap
import shutil
import shlex
import subprocess

# utilities
import binascii
import time

# communication
import socket
import select
import usb

# debugger modules
import pymcuprog
from pyedbglib.protocols.avrispprotocol import AvrIspProtocolError
from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.protocols.edbgprotocol import EdbgProtocol
from pyedbglib.hidtransport.hidtransportfactory import hid_transport
from pymcuprog.backend import Backend
from pymcuprog.pymcuprog_main import  _clk_as_int # _setup_tool_connection
from pymcuprog.toolconnection import ToolUsbHidConnection, ToolSerialConnection
from pymcuprog.nvmspi import NvmAccessProviderCmsisDapSpi
from pymcuprog.utils import read_target_voltage
from pymcuprog.pymcuprog_errors import PymcuprogNotSupportedError, PymcuprogError

from pyavrocd import dwlink
from pyavrocd.livetests import LiveTests
from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.deviceinfo.devices.alldevices import dev_id, dev_name

# signal codes
NOSIG   = 0     # no signal
SIGHUP  = 1     # no connection
SIGINT  = 2     # Interrupt  - user interrupted the program (UART ISR)
SIGILL  = 4     # Illegal instruction
SIGTRAP = 5     # Trace trap  - stopped on a breakpoint
SIGABRT = 6     # Abort because of a fatal error or no breakpoint available
SIGBUS = 10     # Segmentation violation means in our case stack overflow

# special opcodes
BREAKCODE = 0x9598
SLEEPCODE = 0x9588

class EndOfSession(Exception):
    """Termination of session"""
    def __init__(self, msg=None):
        super().__init__(msg)

class FatalError(Exception):
    """Termination of session because of a fatal error"""
    def __init__(self, msg=None):
        super().__init__(msg)

class GdbHandler():
    # pylint: disable=too-many-instance-attributes
    """
    GDB handler
    Maps between incoming GDB requests and AVR debugging protocols (via pymcuprog)
    """
    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def __init__ (self, comsocket, avrdebugger, devicename,
                      no_backend_error, no_hw_dbg_error):
        self.packet_size = 8000
        self.logger = getLogger('GdbHandler')
        self.dbg = avrdebugger
        self.dw = DebugWIRE(avrdebugger, devicename)
        self.mon = MonitorCommand(no_backend_error, no_hw_dbg_error) # hw debugger connected
        self.mem = Memory(avrdebugger, self.mon)
        self.bp = BreakAndExec(1, self.mon, avrdebugger, self.mem.flash_read_word)
        self._comsocket = comsocket
        self._devicename = devicename
        self.last_sigval = 0
        self._lastmessage = ""
        self._extended_remote_mode = False
        self._vflashdone = False # set to True after vFlashDone received
        self._connection_error = None
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
        except (FatalError, PymcuprogNotSupportedError, PymcuprogError) as e:
            self.logger.critical(e)
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

    def _continue_handler(self, packet):
        """
        'c': Continue execution, either at current address or at given address
        """
        self.logger.debug("RSP packet: Continue")
        if not self.mon.is_dw_mode_active():
            self.logger.warning("Cannot start execution because not connected to OCD")
            self.send_debug_message("Enable debugWIRE first: 'monitor debugwire enable'")
            self.send_signal(SIGHUP)
            return
        if self.mem.is_flash_empty() and not self.mon.is_noload():
            self.logger.warning("Cannot start execution without prior loading of executable")
            self.send_debug_message("No program loaded")
            self.send_signal(SIGILL)
            return
        newpc = None
        if packet:
            newpc = int(packet,16)
            self.logger.debug("Set PC to 0x%X before resuming execution", newpc)
        sig = self.bp.resume_execution(newpc)
        if sig == SIGABRT:
            self.send_debug_message("Too many breakpoints set")
            self.send_signal(SIGABRT)
        if sig == SIGILL:
            self.send_debug_message("Cannot continue because of BREAK instruction")
            self.send_signal(SIGILL)

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
        if self.mon.is_dw_mode_active():
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
        if self.mon.is_dw_mode_active():
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
        if not self.mon.is_dw_mode_active():
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
        if not self.mon.is_dw_mode_active():
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
        if not self.mon.is_dw_mode_active():
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
        if not self.mon.is_dw_mode_active():
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
                if self._connection_error:
                    raise FatalError(self._connection_error)
                self.dw.cold_start(graceful=False, callback=self.send_power_cycle)
                # will only be called if there was no error in enabling debugWIRE mode:
                self.mon.set_dw_mode_active()
            elif response[0] == 'dwoff':
                self.dw.disable()
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
                response = ("", response[1].format(dev_name[self.dbg.device_info['device_id']]))
            elif 'live_tests' in response[0]:
                self._live_tests.run_tests()
        except AvrIspProtocolError as e:
            self.logger.critical("ISP programming failed: %s", e)
            self.send_reply_packet("ISP programming failed: %s" % e)
        except (FatalError, PymcuprogNotSupportedError, PymcuprogError) as e:
            self.logger.critical(e)
            self.send_reply_packet("Fatal error: %s" % e)
        else:
            self.send_reply_packet(response[1])


    def send_power_cycle(self):
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

    def _supported_handler(self, _):
        """
        'qSupported': query for features supported by the gbdserver; in our case
        packet size and memory map. Because this is also the command send after a
        connection with 'target remote' is made,
        we will try to establish a connection to the debugWIRE target.
        """
        self.logger.debug("RSP packet: qSupported query.")
        self.logger.debug("Will answer 'PacketSize=%X;qXfer:memory-map:read+'",
                              self.packet_size)
        # Try to start a debugWIRE debugging session
        # if we are already in debugWIRE mode, this will work
        # if not, one has to use the 'monitor debugwire on' command later on
        # If a fatal error is raised, we will remember that and print it again
        # when a request for enabling debugWIRE is made
        try:
            if  self.dw.warm_start(graceful=True):
                self.mon.set_dw_mode_active()
        except FatalError as e:
            self.logger.critical("Error while connecting: %s", e)
            self._connection_error = e
            self.dbg.stop_debugging()
        self.logger.debug("dw_mode_active=%d",self.mon.is_dw_mode_active())
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
        self.logger.debug("RSP packet: single-step")
        if not self.mon.is_dw_mode_active():
            self.logger.debug("Cannot single-step because not connected")
            self.send_debug_message("Enable debugWIRE first: 'monitor debugwire on'")
            self.send_signal(SIGHUP)
            return
        if self.mem.is_flash_empty() and not self.mon.is_noload():
            self.logger.debug("Cannot single-step without prior load")
            self.send_debug_message("No program loaded")
            self.send_signal(SIGILL)
            return
        newpc = None
        if packet:
            newpc = int(packet,16)
            self.logger.debug("Set PC to 0x%X before single step",newpc)
        sig = self.bp.single_step(newpc)
        if sig == SIGABRT:
            self.send_debug_message("Too many breakpoints set")
        self.send_signal(sig)

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
                sig = self.bp.range_step(int(step_range[0],16), int(step_range[1],16))
                if sig == SIGABRT:
                    self.send_debug_message("Too many breakpoints set")
                if sig == SIGILL:
                    self.send_debug_message("Cannot continue because of BREAK instruction")
                self.send_signal(sig)
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
        self.logger.info("Starting to flash ...")
        try:
            self.mem.flash_pages()
        except:
            self.logger.error("Flashing was unsuccessful")
            self.send_packet("E11")
            raise
        self.logger.info("Flash done")
        self.send_packet("OK")

    def _vflash_erase_handler(self, _):
        """
        'vFlashErase': Since we cannot and need not to erase pages,
        we only use this command to clear the cache when there was a previous
        vFlashDone command.
        """
        self.logger.debug("RSP packet: vFlashErase")
        if self.mon.is_dw_mode_active():
            self.bp.cleanup_breakpoints()
            if self._vflashdone:
                self._vflashdone = False
                self.mem.init_flash() # clear cache
            if self.mem.is_flash_empty():
                self.logger.info("Loading executable ...")
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
        data_idx = 0

        # unpack the data into binary array
        result = list(data)

        # check for escaped characters
        while data_idx < len(result):
            if result[data_idx] == 0x7d:
                result.pop(data_idx)
                result[data_idx] = result[data_idx] ^ 0x20
            data_idx += 1

        return result

    def _kill_handler(self, _):
        """
        'vKill': Kill command. Will be called, when the user requests a 'kill', but also
        when in extended-remote mode, when a 'run' is issued. In ordinary remote mode, it
        will disconnect, in extended-remote it will not, and you can restart or load a modified
        file and run that one.
        """
        self.logger.debug("RSP packet: kill process, will reset MCU")
        if self.mon.is_dw_mode_active():
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
        if not self.mon.is_dw_mode_active():
            self.logger.debug("Cannot start execution because not connected")
            self.send_debug_message("Enable debugWIRE first: 'monitor debugwire on'")
            self.send_signal(SIGHUP)
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
        data = self.unescape((packet.split(b':')[1]))
        self.logger.debug("RSP packet: X, addr=0x%s, length=%d, data=%s", addr, size, data)
        if not self.mon.is_dw_mode_active() and size > 0:
            self.logger.debug("RSP packet: Memory write, but not connected")
            self.send_packet("E01")
            return
        if len(data) != size:
            self.logger.error("Size of data packet does not fit: %s", packet)
            self.send_packet("E15")
            return
        if int(addr,16) < 0x80000: # writing to flash
            self.bp.cleanup_breakpoints() # cleanup breakpoints before load
        try:
            reply = self.mem.writemem(addr, bytearray(data))
        except:
            self.logger.error("Loading binary data was unsuccessful")
            self.send_packet("E11")
            raise
        self.send_packet(reply)

    def _remove_breakpoint_handler(self, packet):
        """
        'z': Remove a breakpoint
        """
        if not self.mon.is_dw_mode_active():
            self.send_packet("E01")
            return
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
        if not self.mon.is_dw_mode_active():
            self.send_packet("E01")
            return
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
        if not self.mon.is_dw_mode_active(): # if DW is not enabled yet, simply return
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
        self.logger.debug("<- %s", message)
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
        is in active mode.
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
    #pylint: disable=too-many-nested-blocks, too-many-branches
        """
        Analyze the incoming data stream from GDB. Allow more than one RSP record
        per packet, although this should not be necessary because each packet needs
        to be acknowledged by a '+' from us.
        """
        while data:
            if data[0] == ord('+'): # ACK
                self.logger.debug("-> +")
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
                self.logger.debug("-> -")
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
                #self.logger.debug("<- +")
                data = data[1:]
            elif data[0] == ord('$'): # start of message
                valid_data = True
                self.logger.debug('-> %s', data)
                checksum = (data.split(b"#")[1])[:2]
                packet_data = (data.split(b"$")[1]).split(b"#")[0]
                if int(checksum, 16) != sum(packet_data) % 256:
                    self.logger.warning("Checksum Wrong in packet: %s", data)
                    valid_data = False
                if not valid_data:
                    self._comsocket.sendall(b"-")
                    self.logger.debug("<- -")
                else:
                    self._comsocket.sendall(b"+")
                    self.logger.debug("<- +")
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

class Memory():
    # pylint: disable=too-many-instance-attributes
    """
    This class is responsible for access to all kinds of memory, for loading the flash memory,
    and for managing the flash cache.

    Flash cache is implemented as a growing bytearray. We start always at 0x0000 and fill empty
    spaces by 0xFF. _flashmem_start_prog points always to the first address from which we need to
    program flash memory. Neither the end of the flash cache nor _flashmem_start_prog need to be
    aligned with multi_page_size (page_size multiplied by buffers_per_flash_page).
    When programming, we will restart at a lower address or add 0xFF at the end.
    """

    def __init__(self, dbg, mon):
        self.logger = getLogger('Memory')
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
        method(iaddr, data)
        return "OK"

    def mem_area(self, addr):
        """
        This function returns a triple consisting of the real address as an int, the read,
        and the write method. If illegal address section, report and return
        (0, lambda *x: bytes(), lambda *x: False)
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
        if addr_section == "80": # ram
            return(iaddr, self.sram_masked_read, self.dbg.sram_write)
        if addr_section == "81": # eeprom
            return(iaddr, self.dbg.eeprom_read, self.dbg.eeprom_write)
        if addr_section == "00": # flash
            return(iaddr, self.flash_read, self.flash_write)
        self.logger.error("Illegal memtype in memory access operation at %s: %s",
                              addr, addr_section)
        return (0, lambda *x: bytes(), lambda *x: False)

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
        if not self.mon.is_dw_mode_active():
            self.logger.error("Cannot read from memory when DW mode is disabled")
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
        """
        startaddr = (self._flashmem_start_prog // self._multi_page_size) * self._multi_page_size
        stopaddr = ((len(self._flash) + self._multi_page_size - 1) //
                            self._multi_page_size) * self._multi_page_size
        pgaddr = startaddr
        while pgaddr < stopaddr:
            self.logger.debug("Flashing page starting at 0x%X", pgaddr)
            pagetoflash = self._flash[pgaddr:pgaddr + self._multi_page_size]
            currentpage = bytearray([])
            if self.mon.is_fastload():
                # interestingly, it is faster to read single pages than a multi-page chunk!
                for p in range(self._multi_buffer):
                    currentpage += self.dbg.flash_read(pgaddr+(p*self._flash_page_size),
                                                           self._flash_page_size)
            self.logger.debug("pagetoflash: %s", pagetoflash.hex())
            self.logger.debug("currentpage: %s", currentpage.hex())
            if currentpage[:len(pagetoflash)] == pagetoflash:
                self.logger.debug("Skip flashing page because already flashed at 0x%X", pgaddr)
            else:
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
                                                                     self._flash_page_size)
                    self.logger.debug("pagetoflash: %s", pagetoflash.hex())
                    self.logger.debug("readback: %s", readbackpage.hex())
                    if readbackpage != pagetoflash:
                        raise FatalError("Flash verification error on page 0x{:X}".format(pgaddr))
            pgaddr += self._multi_page_size
        self._flashmem_start_prog = len(self._flash)

    def memory_map(self):
        """
        Return a memory map in XML format. Include registers, IO regs, and EEPROM in SRAM area
        """
        return ('l<memory-map><memory type="ram" start="0x{0:X}" length="0x{1:X}"/>' + \
                             '<memory type="flash" start="0x{2:X}" length="0x{3:X}">' + \
                             '<property name="blocksize">0x{4:X}</property>' + \
                             '</memory></memory-map>').format(0 + 0x800000, \
                             (0x10000 + self._eeprom_start + self._eeprom_size),
                              self._flash_start, self._flash_size, self._multi_page_size)


class BreakAndExec():
    #pylint: disable=too-many-instance-attributes
    """
    This class manages breakpoints, supports flashwear minimizing execution, and
    makes interrupt-safe single stepping possible.
    """

    def __init__(self, hwbps, mon, dbg, read_flash_word):
        self.mon = mon
        self.dbg = dbg
        self.logger = getLogger('BreakAndExec')
        self._hwbps = hwbps # This number includes the implicit HWBP used by run_to
        self._read_flash_word = read_flash_word
        self._hw = [-1] + [None]*self._hwbps # note that the entries start at index 1
        self._bp = {}
        self._bpactive = 0
        self._bstamp = 0
        # more than 128 MB:
        self._bigmem = self.dbg.memory_info.memory_info_by_name('flash')['size'] > 128*1024
        self._range_start = 0
        self._range_end = 0
        self._range_word = []
        self._range_branch = []
        self._range_exit = set()
        if self._bigmem:
            raise FatalError("Cannot deal with address spaces larger than 128 MB")

    def _read_filtered_flash_word(self, address):
        """
        Instead of reading directly from flash memory, we filter out break points.
        """
        if address in self._bp:
            return self._bp[address]['opcode']
        return self._read_flash_word(address)

    def insert_breakpoint(self, address):
        """
        Generate a new breakpoint at given address, do not allocate flash or hwbp yet
        This method will be called before GDB starts executing or single-stepping.
        """
        if address % 2 != 0:
            self.logger.error("Breakpoint at odd address: 0x%X", address)
            return
        if self.mon.is_old_exec():
            self.dbg.software_breakpoint_set(address)
            return
        if address in self._bp: # bp already set, needs to be activated
            self.logger.debug("Already existing BP at 0x%X will be re-activated",address)
            if not self._bp[address]['active']:
                self._bp[address]['active'] = True
                self._bpactive += 1
                self.logger.debug("Set BP at 0x%X to active", address)
            else:
                # if already active, ignore
                self.logger.debug("There is already an active BP at 0x%X", address)
            return
        self.logger.debug("New BP at 0x%X", address)
        opcode = self._read_flash_word(address)
        secondword = self._read_flash_word(address+2)
        self._bstamp += 1
        self._bp[address] =  {'active': True, 'inflash': False,
                                  'hwbp' : None, 'opcode': opcode,
                                  'secondword' : secondword, 'timestamp' : self._bstamp }
        self.logger.debug("New BP at 0x%X: %s", address,  self._bp[address])
        self._bpactive += 1
        self.logger.debug("Now %d active BPs", self._bpactive)

    def remove_breakpoint(self, address):
        """
        Will mark a breakpoint as non-active, but it will stay in flash memory or marked as a hwbp.
        This method is called immediately after execution is stopped.
        """
        if address % 2 != 0:
            self.logger.error("Breakpoint at odd address: 0x%X", address)
            return
        if self.mon.is_old_exec():
            self.dbg.software_breakpoint_clear(address)
            return
        if not (address in self._bp) or not self._bp[address]['active']:
            self.logger.debug("BP at 0x%X was removed before", address)
            return # was already removed before
        self._bp[address]['active'] = False
        self._bpactive -= 1
        self.logger.debug("BP at 0x%X is now inactive", address)
        self.logger.debug("Only %d BPs are now active", self._bpactive)

    def update_breakpoints(self, reserved, protected_bp):
        """
        This is called directly before execution is started. It will remove
        inactive breakpoints different from protected_bp, it will assign the hardware
        breakpoints to the most recently added breakpoints, and request to set active
        breakpoints into flash, if they not there already. The reserved argument states
        how many HWBPs should be reserved for single- or range-stepping. The argument protected_bp
        is set by single and range-stepping, when we start at a place where there is a
        software breakpoint set. In this case, we do a single-step and then wait for
        GDB to re-activate the BP.
        The method will return False when at least one BP cannot be activated due
        to resource restrictions (e.g., not enough HWBPs).
        """
        # remove inactive BPs and de-allocate BPs that are now forbidden
        if not self.remove_inactive_and_deallocate_forbidden_bps(reserved, protected_bp):
            return False
        self.logger.debug("Updating breakpoints before execution")
        # all remaining BPs are active or protected
        # assign HWBPs to the most recently introduced BPs
        # take into account the possibility that hardware breakpoints are not allowed or reserved
        sortedbps = sorted(self._bp.items(), key=lambda entry: entry[1]['timestamp'], reverse=True)
        self.logger.debug("Sorted BP list: %s", sortedbps)
        for hix in range(min((self._hwbps-reserved)*(1-self.mon.is_onlyswbps()),len(sortedbps))):
            h = sortedbps[hix][0]
            hbp = sortedbps[hix][1]
            self.logger.debug("Consider BP at 0x%X", h)
            if hbp['hwbp'] or hbp['inflash']:
                self.logger.debug("BP at 0x%X is already assigned, either HWBP or SWBP", h)
                break # then all older BPs are already allocated!
            if None in self._hw: # there is still an available hwbp
                self.logger.debug("There is still a free HWBP at index: %s", self._hw.index(None))
                hbp['hwbp'] = self._hw.index(None)
                self._hw[self._hw.index(None)] = h
                if hbp['hwbp'] and hbp['hwbp'] > 1:
                    self.logger.error("Trying to set non-existent HWBP %s", hbp['hwbp'])
            else: # steal hwbp from oldest HWBP
                self.logger.debug("Trying to steal HWBP")
                stealbps = sorted(self._bp.items(), key=lambda entry: entry[1]['timestamp'])
                for s, sbp in stealbps:
                    if sbp['hwbp']:
                        self.logger.debug("BP at 0x%X is a HWBP", s)
                        if sbp['hwbp'] > 1:
                            self.logger.error("Trying to clear non-existent HWBP %s", sbp['hwbp'])
                            # self.dbg.hardware_breakpoint_clear(steal[s][1]['hwbp']-1)
                            # not yet implemented
                            return False
                        hbp['hwbp'] = sbp['hwbp']
                        self.logger.debug("Now BP at 0x%X is the HWP", h)
                        self._hw[hbp['hwbp']] = h
                        sbp['hwbp'] = None
                        break
        # now set SWBPs, if they are not already in flash
        for a, bp in self._bp.items():
            if not bp['inflash'] and not bp['hwbp']:
                if self.mon.is_onlyhwbps():
                    return False # we are not allowed to set a software breakpoint
                self.logger.debug("BP at 0x%X will now be set as a SW BP", a)
                self.dbg.software_breakpoint_set(a)
                bp['inflash'] = True
        return True

    def remove_inactive_and_deallocate_forbidden_bps(self, reserved, protected_bp):
        """
        Remove all inactive BPs and deallocate BPs that are forbidden
        (after changing BP preference). A protected SW BP is not deleted!
        These are BPs at the current PC that have been set before and
        will now be overstepped in a single-step action.
        Return False if a non-existent HWBP shall be cleared.
        """
        self.logger.debug("Deallocate forbidden BPs and remove inactive ones")
        for a, bp in list(self._bp.items()):
            if self.mon.is_onlyswbps() and bp['hwbp']: # only SWBPs allowed
                self.logger.debug("Removing HWBP at 0x%X  because only SWBPs allowed.", a)
                if bp['hwbp'] > 1: # this is a real HWBP
                    # self.dbg.hardware_breakpoint_clear(self._bp[a]['hwbp']-1)
                    # not yet implemented
                    self.logger.error("Trying to clear non-existent HWBP %s", bp['hwbp'])
                    return False
                bp['hwbp'] = None
                self._hw = [-1] + [None]*self._hwbps # entries start at 1
            if self.mon.is_onlyhwbps() and bp['inflash']: # only HWBPs allowed
                self.logger.debug("Removing SWBP at 0x%X  because only HWBPs allowed", a)
                bp['inflash'] = False
                self.dbg.software_breakpoint_clear(a)
            # deallocate HWBP
            if reserved > 0 and self._bp[a]['hwbp'] and self._bp[a]['hwbp'] <= reserved:
                if bp['hwbp'] > 1: # this is a real HWBP
                    # self.dbg.hardware_breakpoint_clear(self._bp[a]['hwbp']-1)
                    # not yet implemented
                    self.logger.error("Trying to clear non-existent HWBP %s",
                                          bp['hwbp'])
                    return False
                self._hw[bp['hwbp']] = None
                bp['hwbp'] = None
            # check for protected BP
            if a == protected_bp and bp['inflash']:
                self.logger.debug("BP at 0x%X is protected", a)
                continue
            # delete BP
            if not bp['active']: # delete inactive BP
                self.logger.debug("BP at 0x%X is not active anymore", a)
                if bp['inflash']:
                    self.logger.debug("Removed as a SWBP")
                    self.dbg.software_breakpoint_clear(a)
                if bp['hwbp']:
                    self.logger.debug("Removed as a HWBP")
                    if bp['hwbp'] > 1: # this is a real HWBP
                        # self.dbg.hardware_breakpoint_clear(self._bp[a]['hwbp']-1)
                        # not yet implemented
                        self.logger.error("Trying to clear non-existent HWBP %s",
                                              bp['hwbp'])
                        return False
                    self._hw[bp['hwbp']] = None
                self.logger.debug("BP at 0x%X will now be deleted", a)
                del self._bp[a]
        return True

    def cleanup_breakpoints(self):
        """
        Remove all breakpoints from flash and clear hardware breakpoints
        """
        self.logger.info("Deleting all breakpoints ...")
        self._hw = [-1] + [None for x in range(self._hwbps)]
        # self.dbg.hardware_breakpoint_clear_all() # not yet implemented
        self.dbg.software_breakpoint_clear_all()
        self._bp = {}
        self._bpactive = 0

    def resume_execution(self, addr):
        """
        Start execution at given addr (byte addr). If none given, use the actual PC.
        Update breakpoints in memory and the HWBP. Return SIGABRT if not enough break points.
        """
        self._range_start = None
        if not self.update_breakpoints(0, -1):
            return SIGABRT
        if addr:
            self.dbg.program_counter_write(addr>>1)
        else:
            addr = self.dbg.program_counter_read() << 1
        opcode = self._read_filtered_flash_word(addr)
        if opcode == BREAKCODE: # this should not happen at all
            self.logger.debug("Stopping execution in 'continue' because of BREAK instruction")
            return SIGILL
        if opcode == SLEEPCODE: # ignore sleep
            self.logger.debug("Ignoring sleep in 'single-step'")
            addr += 2
            self.dbg.program_counter_write(addr>>1)
        if self.mon.is_old_exec():
            self.dbg.run()
            return None
        if self._hw[1] is not None:
            self.logger.debug("Run to cursor at 0x%X starting at 0x%X", self._hw[1], addr)
            # according to docu, it is the word address, but in reality it is the byte address!
            self.dbg.run_to(self._hw[1])
        else:
            self.logger.debug("Now start executing at 0x%X without HWBP", addr)
            self.dbg.run()
        return None

    #pylint: disable=too-many-return-statements, too-many-statements, too-many-branches
    def single_step(self, addr, fresh=True):
        """
        Perform a single step. If at the current location, there is a software breakpoint,
        we simulate a two-word instruction or ask the hardware debugger to do a single step
        if it is a one-word instruction. The simulation saves two flash reprogramming operations.
        Otherwise, if mon._safe is true, it means that we will try to not end up in the
        interrupt vector table. For all straight-line instructions, we will use the hardware
        breakpoint to break after one step. If an interrupt occurs, we may break in the ISR,
        if there is a breakpoint, or we will not notice it at all. For all remaining instruction
        (except those branching on the I-bit), we clear the I-bit before and set it
        afterwards (if necessary). For those branching on the I-Bit, we will evaluate and
        then set the hardware BP.
        """
        if fresh:
            self._range_start = None
        if addr:
            self.dbg.program_counter_write(addr>>1)
        else:
            addr = self.dbg.program_counter_read() << 1
        self.logger.debug("One single step at 0x%X", addr)
        opcode = self._read_filtered_flash_word(addr)
        if opcode == SLEEPCODE: # ignore sleep
            self.logger.debug("Ignoring sleep in 'single-step'")
            addr += 2
            self.dbg.program_counter_write(addr>>1)
            return SIGTRAP
        if self.mon.is_old_exec():
            self.logger.debug("Single step in old execution mode")
            self.dbg.step()
            return SIGTRAP
        if opcode == BREAKCODE: # this should not happen!
            self.logger.error("Stopping execution in 'single-step' because of BREAK instruction")
            return SIGILL
        if not self.update_breakpoints(1, addr):
            self.logger.debug("Not enough free HW BPs: SIGABRT")
            return SIGABRT
        # If there is a SWBP at the place where we want to step,
        # use the internal single-step (which will execute the instruction offline)
        # or, if a two-word instruction, simulate the step.
        if addr in self._bp and self._bp[addr]['inflash']:
            if self.two_word_instr(self._bp[addr]['opcode']):
            # if there is a two word instruction, simulate
                self.logger.debug("Two-word instruction at SWBP: simulate")
                addr = self.sim_two_word_instr(self._bp[addr]['opcode'],
                                                self._bp[addr]['secondword'], addr)
                self.logger.debug("New PC(byte addr)=0x%X, return SIGTRAP", addr)
                self.dbg.program_counter_write(addr>>1)
                return SIGTRAP
            # one-word instructions are handled by offline execution in the OCD
            self.logger.debug("One-word instruction at SWBP: offline execution in OCD")
            self.dbg.step()
            return SIGTRAP
        # if stepping is unsafe, just use the AVR stepper
        if not self.mon.is_safe():
            self.logger.debug("Unsafe Single-stepping: use AVR stepper, return SIGTRAP")
            self.dbg.step()
            return SIGTRAP
        # now we have to do the dance using the HWBP or masking the I-bit
        opcode = self._read_filtered_flash_word(addr)
        self.logger.debug("Interrupt-safe stepping begins here")
        destination = None
        # compute destination for straight-line instructions and branches on I-Bit
        if not self.branch_instr(opcode):
            destination = addr + 2 + 2*int(self.two_word_instr(opcode))
            self.logger.debug("This is not a branch instruction. Destination=0x%X", destination)
        if self.branch_on_ibit(opcode):
            ibit = bool(self.dbg.status_register_read()[0] & 0x80)
            destination = self.compute_destination_of_ibranch(opcode, ibit, addr)
            self.logger.debug("Branching on I-Bit. Destination=0x%X", destination)
        if destination is not None:
            self.logger.debug("Run to cursor... at 0x%X, return None", destination)
            self.dbg.run_to(destination)
            return None
        # for the remaining branch instructions,
        # clear I-bit before and set it afterwards (if it was on before)
        self.logger.debug("Remaining branch instructions")
        sreg = self.dbg.status_register_read()[0]
        self.logger.debug("sreg=0x%X", sreg)
        ibit = sreg & 0x80
        sreg &= 0x7F # clear I-Bit
        self.logger.debug("New sreg=0x%X",sreg)
        self.dbg.status_register_write(bytearray([sreg]))
        self.logger.debug("Now make a step...")
        self.dbg.step()
        sreg = self.dbg.status_register_read()[0]
        self.logger.debug("New sreg=0x%X", sreg)
        sreg |= ibit
        self.logger.debug("Restored sreg=0x%X", sreg)
        self.dbg.status_register_write(bytearray([sreg]))
        self.logger.debug("Returning with SIGTRAP")
        return SIGTRAP


    def range_step(self, start, end):
        """
        range stepping: Break only if we leave the interval start-end. If there is only
        one exit point, we watch that. If it is an inside point (e.g., RET), we single-step on it.
        Otherwise, we break at each branching point and single-step this branching instruction.
        In principle this can be generalized to n exit points (n being the number of hardware BPs).
        Note that we need to return after the first step to allow GDB to set a breakpoint at the
        location where we started.
        """
        #pylint: disable=too-many-return-statements
        self.logger.debug("Range stepping from 0x%X to 0x%X", start, end)
        if not self.mon.is_range() or self.mon.is_old_exec():
            self.logger.debug("Range stepping forbidden")
            return self.single_step(None)
        if start%2 != 0 or end%2 != 0:
            self.logger.error("Range addresses in range stepping are ill-formed")
            return self.single_step(None)
        if start == end:
            self.logger.debug("Empty range: Simply single step")
            return self.single_step(None)
        new_range = self.build_range(start, end)
        reservehwbps = len(self._range_exit)
        if reservehwbps > self._hwbps or self.mon.is_onlyhwbps():
            reservehwbps = 1
        addr = self.dbg.program_counter_read() << 1
        if not self.update_breakpoints(reservehwbps, addr):
            return SIGABRT
        if addr < start or addr >= end: # starting outside of range, should not happen!
            self.logger.error("PC 0x%X outside of range boundary", addr)
            return self.single_step(None)
        if (addr in self._range_exit or # starting at possible exit point inside range
            self._read_filtered_flash_word(addr) in { BREAKCODE, SLEEPCODE } or # special opcode
            addr in self._bp or # a SWBP at this point
            new_range): # or it is a new range
            return self.single_step(None, fresh=False) # reduce to one step!
        if len(self._range_exit) == reservehwbps: # we can cover all exit points!
            # if more HWBPs, one could use them here!
            # #MOREHWBPS
            self.dbg.run_to(list(self._range_exit)[0]) # this covers only 1 exit point!
            return None
        if addr in self._range_branch: # if branch point, single-step
            return self.single_step(None, fresh=False)
        for b in self._range_branch:   # otherwise search for next branch point and stop there
            if addr < b:
                self.dbg.run_to(b)
                return None
        return self.single_step(None, fresh=False)

    def build_range(self, start, end):
        #pylint: disable=too-many-branches
        """
        Collect all instructions in the range and analyze them. Find all points, where
        an instruction possibly leaves the range. This includes the first instruction
        after the range, provided it is reachable. These points are remembered in
        self._range_exit. If the number of exits is less than or equal to the number of
        hardware BPs, then one can check for all them. In case of dW this number is one.
        However, this is enough for handling _delay_ms(_). In all other cases, we stop at all
        branching instructions, memorized in self._range_branch, and single-step them.
        Return False, if the range is already established.
        """
        if start == self._range_start and end == self._range_end:
            return False # previously analyzed
        self._range_word = []
        self._range_exit = set()
        self._range_branch = []
        self._range_start = start
        self._range_end = end
        for a in range(start, end+2, 2):
            self._range_word += [ self._read_filtered_flash_word(a) ]
        i = 0
        while i < len(self._range_word) - 1:
            dest = []
            opcode = self._range_word[i]
            secondword = self._range_word[i+1]
            if self.branch_instr(opcode):
                self._range_branch += [ start + (i * 2) ]
            if self.two_word_instr(opcode):
                if self.branch_instr(opcode): # JMP and CALL
                    dest = [ secondword << 1 ]
                else: # STS and LDS
                    dest = [ start + (i + 2) * 2 ]
            else:
                if not self.branch_instr(opcode): # straight-line ops
                    dest = [start + (i + 1) * 2]
                elif self.skip_operation(opcode): # CPSE, SBIC, SBIS, SBRC, SBRS
                    dest = [start + (i + 1) * 2,
                               start + (i + 2 + self.two_word_instr(secondword)) * 2]
                elif self.cond_branch_operation(opcode): # BRBS, BRBC
                    dest = [start + (i + 1) * 2,
                                self.compute_possible_destination_of_branch(opcode,
                                                                                start + (i * 2)) ]
                elif self.relative_branch_operation(opcode): # RJMP, RCALL
                    dest = [ self.compute_destination_of_relative_branch(opcode, start + (i * 2)) ]
                else: # IJMP, EIJMP, RET, ICALL, RETI, EICALL
                    dest = [ -1 ]
            self.logger.debug("Dest at 0x%X: %s", start + i*2, [hex(x) for x in dest])
            if -1 in dest:
                self._range_exit.add(start + (i * 2))
            else:
                self._range_exit = self._range_exit.union([ a for a in dest
                                                                if a < start or a >= end ])
            i += 1 + self.two_word_instr(opcode)
        self._range_branch += [ end ]
        self.logger.debug("Exit points: %s", {hex(x) for x in self._range_exit})
        self.logger.debug("Branch points: %s", [hex(x) for x in self._range_branch])
        return True

    @staticmethod
    def branch_instr(opcode):
        """
        Returns True iff it is a branch instruction
        """
        #pylint: disable=too-many-boolean-expressions)
        if (((opcode & 0xFC00) == 0x1000) or # CPSE
            ((opcode & 0xFFEF) == 0x9409) or # IJMP / EIJMP
            ((opcode & 0xFFEE) == 0x9508) or # RET, ICALL, RETI, EICALL
            ((opcode & 0xFE0C) == 0x940C) or # CALL, JMP
            ((opcode & 0xFD00) == 0x9900) or # SBIC, SBIS
            ((opcode & 0xE000) == 0xC000) or # RJMP, RCALL
            ((opcode & 0xF800) == 0xF000) or # BRBS, BRBC
            ((opcode & 0xFC08) == 0xFC00)): # SBRC, SBRS
            return True
        return False

    @staticmethod
    def relative_branch_operation(opcode):
        """
        Returns True iff it is a branch instruction with relative addressing mode
        """
        if (opcode & 0xE000) == 0xC000: # RJMP, RCALL
            return True
        return False

    @staticmethod
    def compute_destination_of_relative_branch(opcode, addr):
        """
        Computes branch destination for instructions with relative addressing mode
        """
        rdist = opcode & 0x0FFF
        tsc = rdist - int((rdist << 1) & 2**12)
        return addr + 2 + (tsc*2)

    @staticmethod
    def skip_operation(opcode):
        """
        Returns True iff instruction is a skip instruction
        """
        if (opcode & 0xFC00) == 0x1000: # CPSE
            return True
        if (opcode & 0xFD00) == 0x9900: # SBIC, SBIS
            return True
        if (opcode & 0xFC08) == 0xFC00: # SBRC, SBRS
            return True
        return False

    @staticmethod
    def cond_branch_operation(opcode):
        """
        Returns True iff instruction is a conditional branch instruction
        """
        if (opcode & 0xF800) == 0xF000: # BRBS, BRBC
            return True
        return False

    @staticmethod
    def branch_on_ibit(opcode):
        """
        Returns True iff instruction is a conditional branch instruction on the I-bit
        """
        return (opcode & 0xF807) == 0xF007 # BRID, BRIE

    @staticmethod
    def compute_possible_destination_of_branch(opcode, addr):
        """
        Computes branch destination address for conditional branch instructions
        """
        rdist = (opcode >> 3) & 0x007F
        tsc = rdist - int((rdist << 1) & 2**7) # compute twos complement
        return addr + 2 + (tsc*2)


    @staticmethod
    def compute_destination_of_ibranch(opcode, ibit, addr):
        """
        Interprets BRIE/BRID instructions and computes the target instruction.
        This is used to simulate the execution of these two instructions.
        """
        branch = ibit ^ bool(opcode & 0x0400 != 0)
        if not branch:
            return addr + 2
        return BreakAndExec.compute_possible_destination_of_branch(opcode, addr)

    @staticmethod
    def two_word_instr(opcode):
        """
        Returns True iff instruction is a two-word instruction
        """
        return(((opcode & ~0x01F0) == 0x9000) or # lds
               ((opcode & ~0x01F0) == 0x9200) or # sts
               ((opcode & 0x0FE0E) == 0x940C) or # jmp
               ((opcode & 0x0FE0E) == 0x940E))   # call

    def sim_two_word_instr(self, opcode, secondword, addr):
        """
        Simulate a two-word instruction with opcode and 2nd word secondword.
        Update all registers (except PC) and return the (byte-) address
        where execution will continue.
        """
        if (opcode & ~0x1F0) == 0x9000: # lds
            register = (opcode & 0x1F0) >> 4
            val = self.dbg.sram_read(secondword, 1)
            self.dbg.sram_write(register, val)
            self.logger.debug("Simulating lds")
            addr += 4
        elif (opcode & ~0x1F0) == 0x9200: # sts
            register = (opcode & 0x1F0) >> 4
            val = self.dbg.sram_read(register, 1)
            self.dbg.sram_write(secondword, val)
            self.logger.debug("Simulating sts")
            addr += 4
        elif (opcode & 0x0FE0E) == 0x940C: # jmp
            # since debugWIRE works only on MCUs with a flash address space <= 64 kwords
            # we do not need to use the bits from the opcode. Just put in a reminder: #BIGMEM
            addr = secondword << 1 ## now byte address
            self.logger.debug("Simulating jmp 0x%X", addr << 1)
        elif (opcode & 0x0FE0E) == 0x940E: # call
            returnaddr = (addr + 4) >> 1 # now word address
            self.logger.debug("Simulating call to 0x%X", secondword << 1)
            sp = int.from_bytes(self.dbg.stack_pointer_read(),byteorder='little')
            self.logger.debug("Current stack pointer: 0x%X", sp)
            # since debugWIRE works only on MCUs with a flash address space <= 64 kwords
            # we only need to decrement the SP by 2. Just put in a reminder: #BIGMEM
            sp -= 2
            self.logger.debug("New stack pointer: 0x%X", sp)
            self.dbg.stack_pointer_write(sp.to_bytes(2,byteorder='little'))
            self.dbg.sram_write(sp+1, returnaddr.to_bytes(2,byteorder='big'))
            # since debugWIRE works only on MCUs with a flash address space <= 64 kwords
            # we do not need to use the bits from the opcode. Just put in a reminder: #BIGMEM
            addr = secondword << 1
        return addr


class MonitorCommand():
    #pylint: disable=too-many-instance-attributes
    """
    This class implements all the monitor commands
    It manages state variables, gives responses and selects
    the right action. The return value of the dispatch method is
    a pair consisting of an action identifier and the string to be displayed.
    """
    def __init__(self, no_backend_error, no_hw_dbg_error):
        self._no_backend_error = no_backend_error
        self._no_hw_dbg_error = no_hw_dbg_error
        self._dw_mode_active = False
        self._dw_activated_once = False
        self._noload = False # when true, one may start execution even without a previous load
        self._onlyhwbps = False
        self._onlyswbps = False
        self._fastload = True
        self._cache = True
        self._safe = True
        self._verify = True
        self._timersfreeze = True
        self._noxml = False
        self._power = True
        self._old_exec = False
        self._range = True

        self.moncmds = {
            'breakpoints'  : self._mon_breakpoints,
            'caching'      : self._mon_cache,
            'debugwire'    : self._mon_debugwire,
            'help'         : self._mon_help,
            'info'         : self._mon_info,
            'load'         : self._mon_load,
            'onlyloaded'   : self._mon_noload,
            'reset'        : self._mon_reset,
            'rangestepping': self._mon_range_stepping,
            'singlestep'   : self._mon_singlestep,
            'timers'       : self._mon_timers,
            'verify'       : self._mon_flash_verify,
            'version'      : self._mon_version,
            'NoXML'        : self._mon_no_xml,
            'OldExecution' : self._mon_old_execution,
            'Target'       : self._mon_target,
            'LiveTests'    : self._mon_live_tests,
            }

    def set_default_state(self):
        """
        Set state variables to default values.
        """
        self._noload = False
        self._onlyhwbps = False
        self._onlyswbps = False
        self._fastload = True
        self._cache = True
        self._safe = True
        self._verify = True
        self._timersfreeze = True
        self._noxml = False
        self._power = True
        self._old_exec = False
        self._range = True


    def is_onlyhwbps(self):
        """
        Returns True iff only hardware breakpoints are used
        """
        return self._onlyhwbps

    def is_onlyswbps(self):
        """
        Returns True iff only software brrakpoints are used
        """
        return self._onlyswbps

    def is_cache(self):
        """
        Returns True iff the loaded binary is cached and used as a cache
        """
        return self._cache

    def is_dw_mode_active(self):
        """
        Returns True is dw mode is activated
        """
        return self._dw_mode_active

    def set_dw_mode_active(self):
        """
        Sets the dw activated mode to True and remembers that dw has been
        activated once
        """
        self._dw_mode_active = True
        self._dw_activated_once = True

    def is_fastload(self):
        """
        Returns True iff read-before-write is enabled for the load function
        """
        return self._fastload

    def is_noload(self):
        """
        Returns True iff execution without a previous load command is allowed
        """
        return self._noload

    def is_range(self):
        """
        Returns True iff range-stepping is permitted.
        """
        return self._range

    def is_safe(self):
        """
        Returns True iff interrupt-safe single-stepping is enabled
        """
        return self._safe

    def is_timersfreeze(self):
        """
        Returns True iff timers will freeze when execution is stopped.
        """
        return self._timersfreeze

    def is_verify(self):
        """
        Returns True iff we verify flashing after load.
        """
        return self._verify

    def is_old_exec(self):
        """
        Returns True iff the traditional Exec style is used.
        """
        return self._old_exec

    def is_noxml(self):
        """
        Returns True iff GDB is supposed to not accept XML queries
        """
        return self._noxml

    def is_power(self):
        """
        Return True iff target is powered.
        """
        return self._power

    def dispatch(self, tokens):
        """
        Dispatch according to tokens. First element is
        the monitor command.
        """
        if not tokens:
            return self._mon_help([])
        if len(tokens) == 1:
            tokens += [""]
        handler = self._mon_unknown
        for cmd in self.moncmds.items():
            if cmd[0].startswith(tokens[0]):
                if handler == self._mon_unknown:
                    handler = cmd[1]
                else:
                    handler = self._mon_ambigious
        # For these internal monitor commands, we require that
        # they are fully spelled out so that they are not
        # invoked by a mistyped abbreviation
        if handler == self._mon_no_xml and tokens[0] != "NoXML": # pylint: disable=comparison-with-callable
            handler = self._mon_unknown
        if handler == self._mon_target and tokens[0] != "Target": # pylint: disable=comparison-with-callable
            handler = self._mon_unknown
        if handler == self._mon_old_execution and tokens[0] != "OldExecution": # pylint: disable=comparison-with-callable
            handler = self._mon_unknown
        return handler(tokens[1:])

    def _mon_unknown(self, _):
        return("", "Unknown 'monitor' command")

    def _mon_ambigious(self, _):
        return("", "Ambiguous 'monitor' command string")

    # pylint: disable=too-many-return-statements
    def _mon_breakpoints(self, tokens):
        if not tokens[0]:
            if self._onlyhwbps and self._onlyswbps:
                return("", "Internal confusion: No breakpoints are allowed")
            if self._onlyswbps:
                return("", "Only software breakpoints")
            if self._onlyhwbps:
                return("", "Only hardware breakpoints")
            return("", "All breakpoints are allowed")
        if 'all'.startswith(tokens[0]):
            self._onlyhwbps = False
            self._onlyswbps = False
            return("", "All breakpoints are allowed")
        if 'hardware'.startswith(tokens[0]):
            self._onlyhwbps = True
            self._onlyswbps = False
            return("", "Only hardware breakpoints")
        if 'software'.startswith(tokens[0]):
            self._onlyhwbps = False
            self._onlyswbps = True
            return("", "Only software breakpoints")
        return self._mon_unknown(tokens[0])

    def _mon_cache(self, tokens):
        if (("enable".startswith(tokens[0]) and tokens[0] != "") or
                (tokens[0] == "" and self._cache is True)):
            self._cache = True
            return("", "Flash memory will be cached")
        if (("disable".startswith(tokens[0]) and tokens[0] != "") or
                (tokens[0] == "" and self._cache is False)):
            self._cache = False
            return("", "Flash memory will not be cached")
        return self._mon_unknown(tokens[0])

    # pylint: disable=too-many-return-statements, too-many-branches
    def _mon_debugwire(self, tokens):
        if self._no_backend_error:
            if platform.system() == 'Linux':
                return("", "Could not connect via USB.\nPlease install libusb: " +
                           "'sudo apt install libusb-1.0.-0'")
            if platform.system() == "Darwin":
                return("", "Could not connect via USB.\nPlease install libusb: " +
                           "'brew install libusb'")
            return("", "Could not connect via USB. Should not have happened!")
        if self._no_hw_dbg_error:
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                path_to_prog, _ = os.path.split((sys._MEIPASS)[:-1]) #pylint: disable=protected-access
                path_to_prog +=  '/pyavrocd'
            else:
                path_to_prog = 'pyavrocd'
            return("", "No hardware debugger discovered.\n" +
                       "Debugging cannot be activated." +
                       ((("\nPerhaps you need to install the udev rules first:\n" +
                             "'sudo %s --install-udev-rules'\n" +
                             "and then unplug and replug the debugger.") %
                         path_to_prog)\
                        if platform.system() == 'Linux' else ""))
        if tokens[0] =="":
            if self._dw_mode_active:
                return("", "debugWIRE is enabled")
            return("", "debugWIRE is disabled")
        if "enable".startswith(tokens[0]):
            if not self._dw_mode_active:
                if self._dw_activated_once:
                    return("", "Cannot reactivate debugWIRE\n" +
                               "You have to exit and restart the debugger")
                # we set the state variable to active in the calling module
                return("dwon", "debugWIRE is enabled")
            return("reset", "debugWIRE is enabled")
        if "disable".startswith(tokens[0]):
            if self._dw_mode_active:
                self._dw_mode_active = False
                return("dwoff", "debugWIRE is disabled")
            return("", "debugWIRE is disabled")
        return self._mon_unknown(tokens[0])

    def _mon_flash_verify(self, tokens):
        if (("enable".startswith(tokens[0]) and tokens[0] != "") or
                (tokens[0] == "" and self._verify is True)):
            self._verify = True
            return("", "Verifying flash after load")
        if (("disable".startswith(tokens[0]) and tokens[0] != "") or
                (tokens[0] == "" and self._verify is False)):
            self._verify = False
            return("", "Load operations are not verified")
        return self._mon_unknown(tokens[0])

    def _mon_help(self, _):
        return("", """monitor help                       - this help text
monitor version                    - print version
monitor info                       - print info about target and debugger
monitor debugwire [enable|disable] - activate/deactivate debugWIRE mode
monitor reset                      - reset MCU
monitor onlyloaded [enable|disable]
                                   - execute only with loaded executable
monitor load [readbeforewrite|writeonly]
                                   - optimize loading by first reading flash
monitor verify [enable|disable]    - verify that loading was successful
monitor caching [on|off]           - use loaded executable as cache
monitor timers [freeze|run]        - freeze/run timers when stopped
monitor breakpoints [all|software|hardware]
                                   - allow breakpoints of a certain kind
monitor singlestep [safe|interruptible]
                                   - single stepping mode
monitor rangestepping [enable|disable]
                                   - allow range stepping
The first option is always the default one
If no parameter is specified, the current setting is returned""")

    def _mon_info(self, _):
        return ('info', """pyavrocd Version:     """ +
                    importlib.metadata.version("pyavrocd") + """
Target:                   {}
DebugWIRE:                """ + ("enabled" if self._dw_mode_active else "disabled") + """

Breakpoints:              """ + ("all types"
                                     if (not self._onlyhwbps and not self._onlyswbps) else
                                     ("only hardware bps"
                                          if self._onlyhwbps else "only software bps")) + """
Execute only when loaded: """ + ("enabled" if not self._noload else "disabled") + """
Load mode:                """ + ("read before write" if self._fastload else "write only") + """
Verify after load:        """ + ("enabled" if self._verify else "disabled") + """
Caching loaded binary:    """ + ("enabled" if self._cache else "disabled") + """
Timers:                   """ + ("frozen when stopped"
                                     if self._timersfreeze else "run when stopped") + """
Range-stepping:           """ + ("enabled" if self._range else "disabled") + """
Single-stepping:          """ + ("safe" if self._safe else "interruptible"))


    def _mon_load(self,tokens):
        if (("readbeforewrite".startswith(tokens[0])  and tokens[0] != "") or
            (tokens[0] == "" and self._fastload is True)):
            self._fastload = True
            return("", "Reading before writing when loading")
        if (("writeonly".startswith(tokens[0])  and tokens[0] != "") or
                (tokens[0] == "" and self._fastload is False)):
            self._fastload = False
            return("", "No reading before writing when loading")
        return self._mon_unknown(tokens[0])

    def _mon_noload(self, tokens):
        if (("enable".startswith(tokens[0])  and tokens[0] != "") or
                (tokens[0] == "" and self._noload is False)):
            self._noload = False
            return("",  "Execution is only possible after a previous load command")
        if (("disable".startswith(tokens[0])  and tokens[0] != "")  or
                (tokens[0] == "" and self._noload is True)):
            self._noload = True
            return("", "Execution is always possible")
        return self._mon_unknown(tokens[0])

    def _mon_range_stepping(self, tokens):
        if (("enable".startswith(tokens[0])  and tokens[0] != "") or
                (tokens[0] == "" and self._range is True)):
            self._range = True
            return("",  "Range stepping is enabled")
        if (("disable".startswith(tokens[0])  and tokens[0] != "")  or
                  (tokens[0] == "" and self._range is False)):
            self._range = False
            return("", "Range stepping is disabled")
        return self._mon_unknown(tokens[0])

    def _mon_reset(self, _):
        if self._dw_mode_active:
            return("reset", "MCU has been reset")
        return("","Enable debugWIRE first")

    def _mon_singlestep(self, tokens):
        if (("safe".startswith(tokens[0]) and tokens[0] != "") or
                (tokens[0] == "" and self._safe is True)):
            self._safe = True
            return("", "Single-stepping is interrupt-safe")
        if (("interruptible".startswith(tokens[0]) and tokens[0] != "")  or
                (tokens[0] == "" and self._safe is False)):
            self._safe = False
            return("", "Single-stepping is interruptible")
        return self._mon_unknown(tokens[0])

    def _mon_timers(self, tokens):
        if (("freeze".startswith(tokens[0]) and tokens[0] != "") or
                (tokens[0] == "" and self._timersfreeze is True)):
            self._timersfreeze = True
            return(0, "Timers are frozen when execution is stopped")
        if (("run".startswith(tokens[0])  and tokens[0] != "") or
                (tokens[0] == "" and self._timersfreeze is False)):
            self._timersfreeze = False
            return(1, "Timers will run when execution is stopped")
        return self._mon_unknown(tokens[0])

    def _mon_version(self, _):
        return("", "pyavrocd version {}".format(importlib.metadata.version("pyavrocd")))

    # The following commands are for internal purposes
    def _mon_no_xml(self, _):
        self._noxml = True
        return("", "XML disabled")

    def _mon_old_execution(self, _):
        self._old_exec = True
        return("", "Old execution mode")

    def _mon_target(self, tokens):
        if ("on".startswith(tokens[0]) and len(tokens[0]) > 1):
            self._power = True
            res = ("power on", "Target power on")
        elif ("off".startswith(tokens[0]) and len(tokens[0]) > 1):
            self._power = False
            res = ("power off", "Target power off")
        elif ("query".startswith(tokens[0]) and len(tokens[0]) > 1):
            res = ("power query", "Target query")
        elif tokens[0] == "":
            if self._power is True:
                res = ("", "Target power is on")
            else:
                res = ("", "Target power is off")
        else:
            return self._mon_unknown(tokens[0])
        return res

    def _mon_live_tests(self, _):
        if self._dw_mode_active:
            return("live_tests", "Tests done")
        return("", "Enable debugWIRE first")

class DebugWIRE():
    """
    This class takes care of attaching to and detaching from a debugWIRE target, which is a bit
    complicated. The target is either in ISP or debugWIRE mode and the transition from ISP to
    debugWIRE involves power-cycling the target, which one would not like to do every time
    connecting to the target. Further, if one does this transition, it is necessary to restart
    the debugging tool by a housekeeping end_session/start_session sequence.
    """
    def __init__(self, dbg, devicename):
        self.dbg = dbg
        self.spidevice = None
        self._devicename = devicename
        self.logger = getLogger('DebugWIRE')

    def warm_start(self, graceful=True):
        """
        Try to establish a connection to the debugWIRE OCD. If not possible
        (because we are still in ISP mode) and graceful=True, the function returns false,
        otherwise true. If not graceful, an exception is thrown when we are
        unsuccessul in establishing the connection.
        """
        if graceful:
            self.logger.info("debugWIRE warm start")
        try:
            self.dbg.setup_session(self._devicename)
            idbytes = self.dbg.device.read_device_id()
            sig = (0x1E<<16) + (idbytes[1]<<8) + idbytes[0]
            self.logger.debug("Device signature by debugWIRE: %X", sig)
            self.dbg.start_debugging()
            self.dbg.reset()
        except FatalError:
            raise
        except Exception as e: # pylint: disable=broad-exception-caught
            if graceful:
                self.logger.debug("Graceful exception: %s",e)
                self.logger.info("Warm start was unsuccessful")
                return False  # we will try to connect later
            raise
        # Check device signature
        self.logger.debug("Device signature expected: %X", self.dbg.device_info['device_id'])
        if sig != self.dbg.device_info['device_id']:
            # Some funny special cases of chips pretending to be someone else
            # when in debugWIRE mode
            if (
                # pretends to be a 88P, but is 88
                (not (sig == 0x1E930F and self.dbg.device_info['device_id'] == 0x1E930A)) and
                # pretends to be a 168P, but is 168
                (not (sig == 0x1E940B and self.dbg.device_info['device_id'] == 0x1E9406)) and
                # pretends to be a 328P, but is 328
                (not (sig == 0x1E950F and self.dbg.device_info['device_id'] == 0x1E9514))):
                raise FatalError("Wrong MCU: '{}', expected: '{}'".\
                                     format(dev_name[sig],
                                            dev_name[self.dbg.device_info['device_id']]))
        # read out program counter and check whether it contains stuck to 1 bits
        pc = self.dbg.program_counter_read()
        self.logger.debug("PC(word)=%X",pc)
        if pc << 1 > self.dbg.memory_info.memory_info_by_name('flash')['size']:
            raise FatalError("Program counter of MCU has stuck-at-1-bits")
        # disable running timers while stopped
        self.dbg.device.avr.protocol.set_byte(Avr8Protocol.AVR8_CTXT_OPTIONS,
                                                  Avr8Protocol.AVR8_OPT_RUN_TIMERS,
                                                  0)
        return True

    def cold_start(self, graceful=False, callback=None, allow_erase=True):
        """
        On the assumption that we are in ISP mode, first DWEN is programmed,
        then a power-cycle is performed and finally, we enter debugWIRE mode.
        If graceful is True, we allow for a failed attempt to connect to
        the ISP core assuming that we are already in debugWIRE mode. If
        callback is Null or returns False, we wait for a manual power cycle.
        Otherwise, we assume that the callback function does the job.
        """
        self.logger.info("debugWIRE cold start")
        try:
            self.enable(erase_if_locked=allow_erase)
            self.power_cycle(callback=callback)
        except (PymcuprogError, FatalError):
            raise
        except Exception as e: # pylint: disable=broad-exception-caught
            self.logger.debug("Graceful exception: %s",e)
            if not graceful:
                raise
        # end current tool session and start a new one
        self.logger.info("Restarting the debug tool before entering debugWIRE mode")
        self.dbg.housekeeper.end_session()
        self.dbg.housekeeper.start_session()
        # now start the debugWIRE session
        return self.warm_start(graceful=False)


    def power_cycle(self, callback=None):
        """
        Ask user for power-cycle and wait for voltage to come up again.
        If callback is callable, we try that first. It might magically
        perform a power cycle.
        """
        wait_start = time.monotonic()
        last_message = 0
        magic = False
        if callback:
            magic = callback()
        if magic: # callback has done all the work
            return
        self.logger.info("Restarting the debug tool before power-cycling")
        self.dbg.housekeeper.end_session() # might be necessary after an unsuccessful power-cycle
        self.dbg.housekeeper.start_session()
        while time.monotonic() - wait_start < 150:
            if time.monotonic() - last_message > 20:
                self.logger.warning("*** Please power-cycle the target system ***")
                last_message = time.monotonic()
            if read_target_voltage(self.dbg.housekeeper) < 0.5:
                wait_start = time.monotonic()
                self.logger.debug("Power-cycle recognized")
                while  read_target_voltage(self.dbg.housekeeper) < 1.5 and \
                  time.monotonic() - wait_start < 20:
                    time.sleep(0.1)
                if read_target_voltage(self.dbg.housekeeper) < 1.5:
                    raise FatalError("Timed out waiting for repowering target")
                time.sleep(1) # wait for debugWIRE system to be ready to accept connections
                return
            time.sleep(0.1)
        raise FatalError("Timed out waiting for power-cycle")

    def disable(self):
        """
        Disables debugWIRE and unprograms the DWEN fusebit. After this call,
        there is no connection to the target anymore. For this reason all critical things
        needs to be done before, such as cleaning up breakpoints.
        """
        # stop core
        self.dbg.device.avr.protocol.stop()
        # clear all breakpoints
        self.dbg.software_breakpoint_clear_all()
        # disable DW
        self.logger.info("Leaving debugWIRE mode")
        self.dbg.device.avr.protocol.debugwire_disable()
        # detach from OCD
        self.dbg.device.avr.protocol.detach()
        # De-activate physical interface
        self.dbg.device.avr.deactivate_physical()
        # it seems necessary to reset the debug tool again
        self.logger.info("Restarting the debug tool before unprogramming the DWEN fuse")
        self.dbg.housekeeper.end_session()
        self.dbg.housekeeper.start_session()
        # now open an ISP programming session again
        self.logger.info("Reconnecting in ISP mode")
        self.spidevice = NvmAccessProviderCmsisDapSpi(self.dbg.transport, self.dbg.device_info)
        self.spidevice.isp.enter_progmode()
        fuses = self.spidevice.read(self.dbg.memory_info.memory_info_by_name('fuses'), 0, 3)
        self.logger.debug("Fuses read: %X %X %X",fuses[0], fuses[1], fuses[2])
        fuses[1] |= self.dbg.device_info['dwen_mask']
        self.logger.debug("New high fuse: 0x%X", fuses[1])
        self.logger.info("Unprogramming DWEN fuse")
        self.spidevice.write(self.dbg.memory_info.memory_info_by_name('fuses'), 1,
                                         fuses[1:2])
        fuses = self.spidevice.read(self.dbg.memory_info.memory_info_by_name('fuses'), 0, 3)
        fuses = self.spidevice.read(self.dbg.memory_info.memory_info_by_name('fuses'), 0, 3)
        self.logger.debug("Fuses read after DWEN disable: %X %X %X",fuses[0], fuses[1], fuses[2])
        self.spidevice.isp.leave_progmode()

    def enable(self, erase_if_locked=True):
        """
        Enables debugWIRE mode by programming the DWEN fuse bit. If the chip is locked,
        it will be erased. Also the BOOTRST fusebit is disabled.
        Since the implementation of ISP programming is somewhat funny, a few stop/start
        sequences and double reads are necessary.
        """
        if read_target_voltage(self.dbg.housekeeper) < 1.5:
            raise FatalError("Target is not powered")
        self.logger.info("Try to connect using ISP")
        self.spidevice = NvmAccessProviderCmsisDapSpi(self.dbg.transport, self.dbg.device_info)
        device_id = int.from_bytes(self.spidevice.read_device_id(),byteorder='little')
        if self.dbg.device_info['device_id'] != device_id:
            raise FatalError("Wrong MCU: '{}', expected: '{}'".format(
                dev_name[device_id],
                dev_name[self.dbg.device_info['device_id']]))
        fuses = self.spidevice.read(self.dbg.memory_info.\
                                        memory_info_by_name('fuses'), 0, 3)
        self.logger.debug("Fuses read: %X %X %X",fuses[0], fuses[1], fuses[2])
        lockbits = self.spidevice.read(self.dbg.memory_info.\
                                           memory_info_by_name('lockbits'), 0, 1)
        self.logger.debug("Lockbits read: %X", lockbits[0])
        if lockbits[0] != 0xFF and erase_if_locked:
            self.logger.info("MCU is locked. Will be erased.")
            self.spidevice.erase()
            lockbits = self.spidevice.read(self.dbg.memory_info.\
                                               memory_info_by_name('lockbits'), 0, 1)
            self.logger.debug("Lockbits after erase: %X", lockbits[0])
        if 'bootrst_fuse' in self.dbg.device_info:
            # unprogramm bit 0 in high or extended fuse
            self.logger.info("BOOTRST fuse will be unprogrammed.")
            bfuse = self.dbg.device_info['bootrst_fuse']
            fuses[bfuse] |= 0x01
            self.spidevice.write(self.dbg.memory_info.memory_info_by_name('fuses'),
                                     bfuse, fuses[bfuse:bfuse+1])
        # program the DWEN bit
        # leaving and re-entering programming mode is necessary, otherwise write has no effect
        self.logger.info("Reentering programming mode")
        self.spidevice.isp.leave_progmode()
        self.spidevice.isp.enter_progmode()
        fuses[1] &= (0xFF & ~(self.dbg.device_info['dwen_mask']))
        self.logger.debug("New high fuse: 0x%X", fuses[1])
        self.logger.info("Programming DWEN fuse")
        self.spidevice.write(self.dbg.memory_info.memory_info_by_name('fuses'), 1, fuses[1:2])
        # needs to be done twice!
        fuses = self.spidevice.read(self.dbg.memory_info.memory_info_by_name('fuses'), 0, 3)
        fuses = self.spidevice.read(self.dbg.memory_info.memory_info_by_name('fuses'), 0, 3)
        self.logger.debug("Fuses read again: %X %X %X",fuses[0], fuses[1], fuses[2])
        self.spidevice.isp.leave_progmode()
        # in order to start a debugWIRE session, a power-cycle is now necessary, but
        # this has to be taken care of by the calling process

# pylint: disable=too-many-instance-attributes
class AvrGdbRspServer():
    """
    This is the GDB RSP server, setting up the connection to the GDB, reading
    and responding, and terminating. The important part is calling the handle_data
    method of the handler.
    """
    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def __init__(self, avrdebugger, devicename, port,
                     no_backend_error, no_hw_dbg_error):
        self.avrdebugger = avrdebugger
        self.devicename = devicename
        self.port = port
        self.no_backend_error = no_backend_error
        self.no_hw_dbg_error = no_hw_dbg_error
        self.logger = getLogger("AvrGdbRspServer")
        self.connection = None
        self.gdb_socket = None
        self.handler = None
        self.address = None

    def serve(self):
        """
        Serve away ...
        """
        self.gdb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.info("Listening on port %s for gdb connection", self.port)
        # make sure that this message can be seen
        if self.logger.getEffectiveLevel() not in {logging.DEBUG, logging.INFO}:
            print("Listening on port {} for gdb connection".format(self.port))
        self.gdb_socket.bind(("127.0.0.1", self.port))
        self.gdb_socket.listen()
        self.connection, self.address = self.gdb_socket.accept()
        self.connection.setblocking(0)
        self.logger.info('Connection from %s', self.address)
        self.handler = GdbHandler(self.connection, self.avrdebugger, self.devicename,
                                      self.no_backend_error, self.no_hw_dbg_error)
        while True:
            ready = select.select([self.connection], [], [], 0.5)
            if ready[0]:
                data = self.connection.recv(8192)
                if len(data) > 0:
                    # self.logger.debug("Received over TCP/IP: %s",data)
                    self.handler.handle_data(data)
            self.handler.poll_events()


    def __del__(self):
        try:
            if self.handler:
                self.handler.bp.cleanup_breakpoints()
            if self.avrdebugger and self.avrdebugger.device:
                self.avrdebugger.stop_debugging()
        except Exception as e: #pylint: disable=broad-exception-caught
            self.logger.info("Graceful exception during stopping: %s",e)
        finally:
            # sleep 0.5 seconds before closing in order to allow the client to close first
            time.sleep(0.5)
            self.logger.info("Closing socket")
            if self.gdb_socket:
                self.gdb_socket.close()
            self.logger.info("Closing connection")
            if self.connection:
                self.connection.close()



def _setup_tool_connection(args, logger):
    """
    Copied from pymcuprog_main and modified so that no messages printed on the console
    """
    toolconnection = None

    # Parse the requested tool from the CLI
    if args.tool == "uart":
        baudrate = _clk_as_int(args)
        # Embedded GPIO/UART tool (eg: raspberry pi) => no USB connection
        toolconnection = ToolSerialConnection(serialport=args.uart,
                                                  baudrate=baudrate, timeout=args.uart_timeout)
    else:
        usb_serial = args.serialnumber
        product = args.tool
        if usb_serial and product:
            logger.info("Connecting to {0:s} ({1:s})'".format(product, usb_serial))
        else:
            if usb_serial:
                logger.info("Connecting to any tool with USB serial number '{0:s}'".\
                                format(usb_serial))
            elif product:
                logger.info("Connecting to any {0:s}".format(product))
            else:
                logger.info("Connecting to anything possible")
        toolconnection = ToolUsbHidConnection(serialnumber=usb_serial, tool_name=product)

    return toolconnection


# pylint: disable=too-many-statements, too-many-branches, too-many-return-statements, too-many-locals
def main():
    """
    Configures the CLI and parses the arguments
    """
    no_backend_error = False # will become true when libusb is not found
    no_hw_dbg_error = False # will become true, when no HW debugger is found

    udev_rules= '''# JTAGICE3
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2140", MODE="0666"
# Atmel-ICE
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2141", MODE="0666"
# Power Debugger
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2144", MODE="0666"
# EDBG - debugger on Xplained Pro
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2111", MODE="0666"
# EDBG - debugger on Xplained Pro (MSD mode)
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2169", MODE="0666"
# mEDBG - debugger on Xplained Mini
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2145", MODE="0666"
# PKOB nano (nEDBG) - debugger on Curiosity Nano
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2175", MODE="0666"
# PKOB nano (nEDBG) in DFU mode - bootloader of debugger on Curiosity Nano
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2fc0", MODE="0666"
# MPLAB PICkit 4 In-Circuit Debugger
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2177", MODE="0666"
# MPLAB Snap In-Circuit Debugger
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2180", MODE="0666"'''

    parser = argparse.ArgumentParser(usage="%(prog)s [options]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\n\
    GDB server for AVR MCUs
            '''))

    parser.add_argument("-c", "--command",
                            action='append',
                            dest='cmd',
                            type=str,
                            help="command to set gdb port")

    parser.add_argument("-d", "--device",
                            dest='dev',
                            type=str,
                            help="device to debug")

    parser.add_argument('-g', '--gede',  action="store_true",
                            help='start gede')

    parser.add_argument('-p', '--port',  type=int, default=2000, dest='port',
                            help='local port on machine (default 2000)')

    parser.add_argument('-s', '--start',  dest='prg',
                            help='start specified program or "noop"')

    parser.add_argument("-t", "--tool",
                            type=str, choices=['atmelice', 'edbg', 'jtagice3', 'medbg', 'nedbg',
                                                   'pickit4', 'powerdebugger', 'snap', 'dwlink'],
                            help="tool to connect to")

    parser.add_argument("-u", "--usbsn",
                            type=str,
                            dest='serialnumber',
                            help="USB serial number of the unit to use")

    parser.add_argument("-v", "--verbose",
                            default="info", choices=['debug', 'info',
                                                         'warning', 'error', 'critical'],
                            help="Logging verbosity level")

    parser.add_argument("-V", "--version",
                            help="Print pyavrocd version number and exit",
                            action="store_true")

    if platform.system() == 'Linux':
        parser.add_argument("--install-udev-rules",
                                help="Install udev rules for Microchip hardware " +
                                "debuggers under /etc/udev/rules.d/",
                                action="store_true")

    # Parse args
    args, unknown = parser.parse_known_args()

    if args.cmd:
        args.cmd = args.cmd
        portcmd = [c for c in args.cmd if 'gdb_port' in c]
        if portcmd:
            cmd = portcmd[0]
            args.port = int(cmd[cmd.index('gdb_port')+len('gdb_port'):])

    # set up logging
    if args.verbose:
        args.verbose = args.verbose.strip()
    if args.verbose.upper() in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
        form = "[%(levelname)s] %(message)s"
    else:
        form = "[%(levelname)s] %(name)s: %(message)s"
    logging.basicConfig(stream=sys.stderr,level=args.verbose.upper(), format = form)
    logger = getLogger()

    if args.verbose.upper() == "DEBUG":
        getLogger('pyedbglib').setLevel(logging.INFO)
    if args.verbose.upper() != "DEBUG":
        # suppress messages from hidtransport
        getLogger('pyedbglib.hidtransport.hidtransportbase').setLevel(logging.ERROR)
        # suppress spurious error messages from pyedbglib
        getLogger('pyedbglib.protocols').setLevel(logging.CRITICAL)
        # suppress errors of not connecting: It is intended!
        getLogger('pymcuprog.nvm').setLevel(logging.CRITICAL)
        # we do not want to see the "read flash" messages
        getLogger('pymcuprog.avr8target').setLevel(logging.ERROR)

    if unknown:
        logger.warning("Unknown options: %s", ' '.join(unknown))

    if args.version:
        print("pyavrocd version {}".format(importlib.metadata.version("pyavrocd")))
        return 0

    if args.dev:
        args.dev = args.dev.strip()
    if args.dev and args.dev == "?":
        print("Supported devices:")
        for d in sorted(dev_id):
            print(d)
        return 0

    if hasattr(args, 'install_udev_rules') and args.install_udev_rules:
        logger.info("Will try to install udev rules")
        try:
            with open("/etc/udev/rules.d/99-edbg-debuggers.rules", "w", encoding='utf-8') as f:
                f.write(udev_rules)
        except Exception as e: #pylint: disable=broad-exception-caught
            logger.critical("Could not install the udev rules: %s", e)
            return 1
        logger.info("Udev rules have been successfully installed")
        return 0

    device = args.dev

    if not device:
        print("Please specify target MCU with -d option")
        return 1

    if device.lower() not in dev_id:
        logger.critical("Device '%s' is not supported by pyavrocd", device)
        return 1

    if args.tool:
        args.tool = args.tool.strip()
    if args.tool == "dwlink":
        dwlink.main(args) # if we return, then there is no HW debugger
        no_hw_dbg_error = True
        logger.critical("No hardware debugger discovered")
    else:
        # Use pymcuprog backend for initial connection here
        backend = Backend()
        toolconnection = _setup_tool_connection(args, logger)

        try:
            backend.connect_to_tool(toolconnection)
        except usb.core.NoBackendError as e:
            no_backend_error = True
            logger.critical("Could not connect to hardware debugger: %s", e)
            if platform.system() == 'Darwin':
                logger.critical("Install libusb: 'brew install libusb'")
                logger.critical("Maybe consult: " +
                                "https://github.com/greatscottgadgets/cynthion/issues/136")
            elif platform.system() == 'Linux':
                logger.critical("Install libusb: 'sudo apt install libusb-1.0-0'")
            else:
                logger.critical("This error should not happen!")
        except pymcuprog.pymcuprog_errors.PymcuprogToolConnectionError as e:
            dwlink.main(args)
            no_hw_dbg_error = True
        finally:
            backend.disconnect_from_tool()

        transport = hid_transport()
        if len(transport.devices) > 1:
            logger.critical("Too many hardware debuggers connected")
        if len(transport.devices) == 0 and no_hw_dbg_error:
            logger.critical("No hardware debugger discovered")
        if not no_backend_error and not no_hw_dbg_error:
            transport.connect(serial_number=toolconnection.serialnumber,
                                product=toolconnection.tool_name)
            logger.info("Connected to %s", transport.hid_device.get_product_string())
        elif platform.system() == 'Linux' and no_hw_dbg_error and len(transport.devices) == 0:
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                path_to_prog, _ = os.path.split((sys._MEIPASS)[:-1]) #pylint: disable=protected-access
                path_to_prog +=  '/pyavrocd'
            else:
                path_to_prog = 'pyavrocd'
            logger.critical(("Perhaps you need to install the udev rules first:\n"
                             "'sudo %s --install-udev-rules'\n" +
                             "and then unplug and replug the debugger."), path_to_prog)

    if no_hw_dbg_error or no_backend_error:
        return 1

    logger.info("Starting GDB server")
    avrdebugger = XAvrDebugger(transport, device)
    server = AvrGdbRspServer(avrdebugger, device, args.port, no_backend_error, no_hw_dbg_error)

    if args.gede:
        args.prg = "gede"
    if args.prg and args.prg != "noop":
        args.prg = args.prg.strip()
        logger.info("Starting %s", args.prg)
        cmd = shlex.split(args.prg)
        cmd[0] = shutil.which(cmd[0])
        subprocess.Popen(cmd) # pylint: disable=consider-using-with

    try:
        server.serve()
    except (EndOfSession, SystemExit):
        logger.info("End of session")
        return 0
    except KeyboardInterrupt:
        logger.info("Terminated by Ctrl-C")
        return 1
    except (ValueError, Exception) as e:
        if logger.getEffectiveLevel() != logging.DEBUG:
            logger.critical("Fatal Error: %s",e)
            return 1
        raise
    return 0

if __name__ == "__main__":
    sys.exit(main())
