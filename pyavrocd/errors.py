"""
Some common errors
"""

class FatalError(Exception):
    """Termination of session because of a fatal error"""
    def __init__(self, msg : str | None = None) -> None:
        super().__init__(msg)

class EndOfSession(Exception):
    """Termination of session"""
    def __init__(self, msg : str | None = None) -> None:
        super().__init__(msg)

class TerminationRequest(BaseException):
    """Termination requested by SIGTERM; derived from BaseException, like KeyboardInterrupt,
    so that 'except Exception' clauses do not swallow it"""
    def __init__(self, msg : str | None = None) -> None:
        super().__init__(msg)
