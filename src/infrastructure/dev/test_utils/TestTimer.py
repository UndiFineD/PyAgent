import time


class TestTimer:
    """A simple timer utility for measuring elapsed time in tests."""

    # def __init__(self):
    #    self._start = None

    def start(self):
        """Start the timer by recording the current time."""
        self._start = time.time()

    def elapsed(self):
        """Return the elapsed time in seconds since start() was called."""
        return (time.time() - self._start) if self._start else 0


__all__ = ["TestTimer"]
