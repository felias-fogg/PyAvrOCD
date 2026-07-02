"""
GDB Server module
"""
from typing import Any

# args, logging
import logging
import signal
import platform
from logging import getLogger
import argparse

# utilities
import time

# communication
import socket
import select

# debugger modules

from pyavrocd.handler import GdbHandler, RECEIVE_BUFFER
from pyavrocd.errors import  EndOfSession
from pyavrocd.xavrdebugger import XAvrDebugger

class RspServer():
    """
    This is the GDB RSP server, setting up the connection to the GDB debugger, reading
    and responding, and terminating. The important part is calling the handle_data
    method of the handler.
    """

    def __init__(self, avrdebugger : XAvrDebugger,
                     devicename : str,
                     args : argparse.Namespace,
                     toolname : str) -> None:
        self.avrdebugger : XAvrDebugger = avrdebugger
        self.devicename : str = devicename
        self.port : int = args.port
        self.toolname : str = toolname
        self._terminate : bool = False
        self.logger : logging.Logger = getLogger("pyavrocd.rspserver")
        self.args : argparse.Namespace = args
        self.connection : socket.socket | None = None
        self.gdb_socket : socket.socket | None = None
        self.address : int | None = None
        self.handler : GdbHandler | None = None

    def _signal_server(self, _signo : int ,_frame : Any) -> None:
        self.logger.info("System requested termination using SIGTERM signal")
        self._terminate = True

    def serve(self) -> int:
        """
        Serve away ...
        """
        signal.signal(signal.SIGTERM, self._signal_server)
        self.gdb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.info("Listening on port %s for gdb connection", self.port)
        # make sure that this message can be seen
        if self.logger.getEffectiveLevel() not in {logging.DEBUG, logging.INFO}:
            print("Listening on port {} for gdb connection".format(self.port))
        self.gdb_socket.bind(("127.0.0.1", self.port))
        try:
            self.gdb_socket.listen()
            self.gdb_socket.settimeout(0.5) # necessary in order to allow for Ctrl-C under Windows
            while self.connection is None:
                try:
                    self.connection, self.address = self.gdb_socket.accept()
                except socket.timeout:
                    pass
            self.connection.setblocking(False)
            self.logger.info('Connection from %s', self.address)
            self.handler = GdbHandler(self.connection, self.avrdebugger, self.devicename, self.args, self.toolname)
            while not self._terminate:
                ready = select.select([self.connection], [], [], 0.2)
                if ready[0]:
                    data : bytes = self.connection.recv(RECEIVE_BUFFER)
                    if len(data) > 0:
                        self.handler.handle_data(data)
                    else:
                        self._terminate = True
                        self.logger.info("Connection closed by GDB")
                else:
                    self.handler.handle_data(None)
                self.handler.poll_events()
            return 0 # termination because of dropped connection or SIGTERM signal
        except EndOfSession: # raised by 'detach' command
            self.logger.info("End of session")
            return 0
        except KeyboardInterrupt: # caused by user interrupt
            self.logger.info("Terminated by Ctrl-C")
            return 1
        except Exception as e:
            self.logger.critical("Forced exit: %s", e)
            return 1
        finally:
            self.logger.info("Leaving GDB server")
            if self.avrdebugger and self.avrdebugger.device:
                leave : bool = self.avrdebugger.get_iface() != 'debugwire'
                if self.handler is not None and \
                    self.handler.mon is not None:
                    leave = self.handler.mon.is_leaveonexit()
                if self.handler is None or self.handler.mon is None or \
                    self.handler.mon.is_debugger_active():
                    self.avrdebugger.stop_debugging(leave=leave, graceful=True)
            # sleep 1 second before closing in order to allow the client to close first
            if platform.system() != "Windows":
                time.sleep(1) # under Windows, a system exception is raised
            if self.connection:
                self.connection.close()
                self.logger.info("Connection closed")
            if self.gdb_socket:
                self.gdb_socket.close()
                self.logger.info("Socket closed")
            self.logger.info("GDB server terminated")

