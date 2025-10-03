"""
GDB Server module
"""
# args, logging
import logging
import signal
from logging import getLogger


# utilities
import time

# communication
import socket
import select

# debugger modules

from pyavrocd.handler import GdbHandler, RECEIVE_BUFFER
from pyavrocd.errors import  EndOfSession

class RspServer():
    """
    This is the GDB RSP server, setting up the connection to the GDB debugger, reading
    and responding, and terminating. The important part is calling the handle_data
    method of the handler.
    """
    def __init__(self, avrdebugger, devicename, args):
        self.avrdebugger = avrdebugger
        self.devicename = devicename
        self.port = args.port
        self.logger = getLogger("pyavrocd.rspserver")
        self.connection = None
        self.gdb_socket = None
        self.handler = None
        self.address = None
        self.args = args
        self._terminate = False

    def _signal_server(self,_signo,_frame):
        self.logger.info("System requested termination using SIGTERM signal")
        self._terminate = True

    def serve(self):
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
            self.connection, self.address = self.gdb_socket.accept()
            self.connection.setblocking(0)
            self.logger.info('Connection from %s', self.address)
            self.handler = GdbHandler(self.connection, self.avrdebugger, self.devicename, self.args)
            while not self._terminate:
                ready = select.select([self.connection], [], [], 0.5)
                if ready[0]:
                    data = self.connection.recv(RECEIVE_BUFFER)
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
        finally:
            self.logger.info("Leaving GDB server")
            if self.avrdebugger and self.avrdebugger.device:
                if self.avrdebugger.get_iface() == "debugwire" and \
                  self.handler.mon.is_debugger_active() and \
                  self.handler.mon.is_leaveonexit():
                    self.avrdebugger.dw_disable()
                self.avrdebugger.stop_debugging(graceful=False)
                self.avrdebugger = None


    def __del__(self):
        try:
            self.logger.info("Terminating GDB server ...")
            if self.avrdebugger and self.avrdebugger.device:
                self.avrdebugger.stop_debugging(graceful=True)
        except Exception as e:
            if self.logger.getEffectiveLevel() == logging.DEBUG:
                self.logger.debug("Graceful exception during stopping: %s",e)
                # raise
            else:
                pass
        finally:
            # sleep 0.5 seconds before closing in order to allow the client to close first
            time.sleep(0.5)
            if self.connection:
                self.connection.close()
                self.logger.info("Connection closed")
            if self.gdb_socket:
                self.gdb_socket.close()
                self.logger.info("Socket closed")
            self.logger.info("... GDB server terminated")

