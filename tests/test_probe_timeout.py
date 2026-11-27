"""
A probe that stops answering ends the session with ProbeNotResponding instead of a read that waits forever
"""
#pylint: disable=missing-function-docstring,protected-access
import socket
import unittest
from unittest.mock import MagicMock, create_autospec, patch

from pyedbglib.hidtransport.cyhidapi import CyHidApiTransport

from pyavrocd.errors import ProbeNotResponding
from pyavrocd.handler import GdbHandler
from pyavrocd.main import options
from pyavrocd.xavrdebugger import EdbgBackend, limit_hid_reads, PROBE_NOT_RESPONDING


def hidapi_transport(replies):
    """A stand-in for pyedbglib's hidapi transport whose device answers with 'replies' ([] = timeout)"""
    transport = MagicMock(spec=CyHidApiTransport)
    transport.device = MagicMock(packet_size=64)        # instance attributes, unknown to the spec
    transport.hid_device = MagicMock()
    transport.hid_device.read.side_effect = replies
    return transport


class TestLimitHidReads(unittest.TestCase):
    """The time limit on the reads of pyedbglib's hidapi transport"""

    def test_answers_pass_through_with_the_time_limit(self):
        transport = hidapi_transport([[0x80, 0x01]])
        limit_hid_reads(transport, timeout_ms=1234)
        self.assertEqual(transport.hid_read(), bytearray([0x80, 0x01]))
        transport.hid_device.read.assert_called_once_with(64, 1234)

    def test_timeout_raises_and_then_everything_fails_at_once(self):
        transport = hidapi_transport([[]])
        write = transport.hid_write
        limit_hid_reads(transport)
        with self.assertRaisesRegex(ProbeNotResponding, PROBE_NOT_RESPONDING):
            transport.hid_read()
        with self.assertRaises(ProbeNotResponding):
            transport.hid_write(bytearray([0x81]))
        with self.assertRaises(ProbeNotResponding):
            transport.hid_read()
        write.assert_not_called()                          # the dead probe is not written to
        self.assertEqual(transport.hid_device.read.call_count, 1)   # nor waited for again

    def test_only_hidapi_transports_and_only_once(self):
        other = MagicMock()                                # e.g. a bulk transport with its own timeouts
        read = other.hid_read
        limit_hid_reads(other)
        self.assertIs(other.hid_read, read)
        transport = hidapi_transport([[1], [2]])
        limit_hid_reads(transport)
        limited = transport.hid_read
        limit_hid_reads(transport)
        self.assertIs(transport.hid_read, limited)


class TestHandlerPassesItOn(unittest.TestCase):
    """The handler does not turn ProbeNotResponding into a SIGABRT for GDB, so the server ends"""

    @patch('pyavrocd.handler.logging.getLogger', MagicMock())
    def test_dispatch_reraises(self):
        dbg = create_autospec(EdbgBackend, spec_set=False, instance=True)
        dbg.get_iface.return_value = 'updi'
        dbg.memory_info = MagicMock()                    # as in test_gdbhandler.py
        dbg.device_info = MagicMock()
        dbg.memory_info.memory_info_by_name('flash')['size'].__gt__ = lambda self, compare: False
        handler = GdbHandler(create_autospec(socket.socket, instance=True), dbg, "attiny416",
                             options(['-d', 'attiny416']), "Tool")
        handler.mem = MagicMock()
        handler.mem.lazy_loading = False
        handler.packettypes['g'] = MagicMock(side_effect=ProbeNotResponding(PROBE_NOT_RESPONDING))
        with self.assertRaises(ProbeNotResponding):
            handler.dispatch('g', b'g')


if __name__ == '__main__':
    unittest.main()
