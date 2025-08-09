"""
This module is responsible for connecting and disconnecting to and from a JTAG target.
"""
# args, logging

from logging import getLogger

class JTAG():
    """
    This class  makes sure that all the right fuses are set for a JTAG target in the end unprogrammed.
    """

    def __init__(self, dbg, devicename):
        self.dbg = dbg
        self._devicename = devicename
        self.logger = getLogger("JTAG target")

    def start(self):
        """
        This is pomnly y stup
        """
        return 0
