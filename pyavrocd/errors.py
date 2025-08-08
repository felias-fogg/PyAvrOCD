"""
Some common errors
"""

class FatalError(Exception):
    """Termination of session because of a fatal error"""
    def __init__(self, msg=None):
        super().__init__(msg)

class EndOfSession(Exception):
    """Termination of session"""
    def __init__(self, msg=None):
        super().__init__(msg)
