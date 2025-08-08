"""
Discover dw-link and then redirect data from a TCP/IP connection to the serial port and vice versa.
Further, send the device name in specially designed RSP record and wait for Ack
Based on Chris Liechti's tcp_serial_redirect script
"""
# pylint: disable=consider-using-f-string
import os
import sys
import shutil
import shlex
import subprocess
import time
import socket
import serial
import serial.threaded
from serial import SerialException
import serial.tools.list_ports

class DetachException(Exception):
    """Termination of session because of a detach command"""
    def __init__(self, msg=None):
        super().__init__(msg)

class SerialToNet(serial.threaded.Protocol):
    """serial->socket"""

    def __init__(self, logging):
        self.logging = logging
        self.socket = None
        self.last = b""

    def __call__(self):
        return self

    def data_received(self, data):
        """
        Deal with data received from the serial line: send to socket and maybe log to console.
        """
        if self.socket is not None:
            self.socket.sendall(data)
            self.last += data
            if self.last:
                if self.last[-1] == ord('+') or (len(self.last) > 2 and self.last[-3] == ord('#')):
                    if len(self.last) > 2 and self.last[1] == ord('O') and self.last[2] != ord('K'):
                        message = self.convert_gdb_message()
                    else:
                        message = ""
                    if self.logging:
                        sys.stderr.write("[DEBUG] recv: {}\n".format(self.last))
                        if message:
                            sys.stderr.write("[DEBUG] dw-link: {}".format(message))
                        sys.stdout.flush()
                    if len(message) > 2 and message[:3] == '***':
                        sys.stderr.write("[WARNING] {}".format(message))
                        sys.stderr.flush()
                    self.last = b""

    def convert_gdb_message(self):
        """
        converts hex string into an UTF-8 text message
        """
        bs = self.last[2:self.last.find(b'#')]
        hv = bs.decode('utf-8')
        bv = bytes.fromhex(hv)
        return bv.decode('utf-8')

    def connection_lost(self, exc):
        """
        What to do when the connection is lost: Complain when caused by an exception,
        otherwise tell the serial connection is closed.
        """
        if exc:
            sys.stderr.write('[ERROR] ' +  repr(exc) + '\n\r')
            sys.stderr.write('[INFO] Serial connection lost, will exit\n\r')
            time.sleep(0.2)
        else:
            sys.stderr.write('[INFO] Serial connection closed\n\r')
            os._exit(0)

def discover(args):
    """
    Discovers the dw-link adapter, if present
    """
    for delay in (0.2, 2):
        for s in serial.tools.list_ports.comports(True):
            if args.verbose == "debug":
                sys.stdout.write("[DEBUG] Device: {}\n".format(s.device))
                sys.stdout.flush()
            if s.device in ["/dev/cu.Bluetooth-Incoming-Port", "/dev/cu.debug-console"]:
                continue
            if args.verbose == "debug":
                sys.stdout.write("[DEBUG] Check:{}\n".format(s.device))
                sys.stdout.flush()
            try:
                for sp in (115200, ):
                    with serial.Serial(s.device, sp, timeout=0.1,
                                           write_timeout=0.1, exclusive=True) as ser:
                        time.sleep(delay)
                        ser.write(b'\x05') # send ENQ
                        resp = ser.read(7) # under Linux, the first response might be empty
                        if resp != b'dw-link':
                            time.sleep(0.2)
                            ser.write(b'\x05') # try again sending ENQ
                            resp = ser.read(7) # now it should be the right response!
                        # if we get this response, it must be an dw-link adapter
                        if resp == b'dw-link':
                            # send type of MCU in a special RSP packet
                            message = ('=' + args.dev).encode('ascii')
                            checksum = sum(message)&0xFF
                            ser.write(b'$' + message + b'#' + (b'%02X' % checksum))
                            return (sp, s.device)
            except SerialException:
                pass
            except Exception as e: # pylint: disable=broad-exception-caught
                sys.stderr.write('[ERROR] ' + repr(e) + '\n\r')
    return (None, None)

def main(args, intf):
    """
    Main function providing an serial-to-IP bridge for the dw-link hardware debugger
    """
    #pylint: disable=too-many-statements, too-many-branches, too-many-nested-blocks
    # discover adapter
    speed, device = discover(args)
    if speed is None or device is None:
        return # return to dw-gdbserver main, which will handle this problem

    # check whether interface is OK
    if intf != "debugwire":
        sys.stderr.write('[CRITICAL] dw-link can only debug debugWIRE targets\n')
        sys.exit(1)

    # connect to serial port
    ser = serial.serial_for_url(device, do_not_open=True)
    ser.baudrate = speed
    ser.bytesize = 8
    ser.parity = 'N'
    ser.stopbits = 1
    ser.rtscts = False
    ser.xonxoff = False
    ser.exclusive = True

    try:
        ser.open()
    except serial.SerialException as e:
        sys.stderr.write('[CRITICAL] Could not open serial port {}: {}\n'.format(device, e))
        sys.exit(2)

    try:
        ser_to_net = SerialToNet(args.verbose == 'debug')
        serial_worker = serial.threaded.ReaderThread(ser, ser_to_net)
        serial_worker.start()

        if args.gede:
            args.prg = "gede"

        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            srv.bind(('', args.port))
            srv.listen(1)
        except OSError as error:
            sys.stderr.write("OSError: " + error.strerror +"\n\r")
            sys.exit(3)

        subprc = None
        if args.prg and args.prg != "noop":
            cmd = shlex.split(args.prg)
            cmd[0] = shutil.which(cmd[0])
            subprc = subprocess.Popen(cmd) #pylint: disable=consider-using-with

        sys.stderr.write("[INFO] Connected to dw-link debugger\r\n")
        sys.stderr.write("[INFO] Listening on port {} for gdb connection\n\r".format(args.port))
        sys.stderr.flush()

        client_socket, addr = srv.accept()
        sys.stderr.write('[INFO] Connected by {}\n'.format(addr))
        # More quickly detect bad clients who quit without closing the
        # connection: After 1 second of idle, start sending TCP keep-alive
        # packets every 1 second. If 3 consecutive keep-alive packets
        # fail, assume the client is gone and close the connection.
        try:
            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)
            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 1)
            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        except AttributeError:
            pass
        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        try:
            ser_to_net.socket = client_socket
            # enter network <-> serial loop
            while True:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    ser.write(data)                 # get a bunch of bytes and send them
                    if b'$D#44' in data:
                        raise DetachException
                    if args.verbose == "debug":
                        sys.stderr.write("[DEBUG] sent: {}\n".format(data))
                        sys.stderr.flush()
                except socket.error as msg:
                    sys.stderr.write('[ERROR] {}\n\r'.format(msg))
                    # probably got disconnected
                    break
        except Exception as msg: # pylint: disable=broad-exception-caught
            sys.stderr.write('[ERROR] {}\n\r'.format(msg))
        finally:
            ser_to_net.socket = None
            sys.stderr.write('[INFO] Disconnected\n\r')
            ser.write(b'$D#44') # send detach command to dw-link debugger
            client_socket.close()
    except KeyboardInterrupt:
        os._exit(1)
    except Exception: # pylint: disable=broad-exception-caught
        pass

    if subprc:
        subprc.kill()
    try:
        serial_worker.stop()
    except Exception:  # pylint: disable=broad-exception-caught
        pass
