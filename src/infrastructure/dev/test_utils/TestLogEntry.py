#!/usr/bin/env python3
class TestLogEntry:
    """TestLogEntry shim for pytest collection."""

    def __init__(self, level: str, message: str):
        """Represents a test log entry for comparison."""
        self.level = level
        self.message = message


__all__ = ["TestLogEntry"]
