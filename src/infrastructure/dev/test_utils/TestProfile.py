#!/usr/bin/env python3
class TestProfile:
    """TestProfile shim for pytest collection."""
    def __init__(self, name: str):
        """Represents a test profile for comparison."""
        self.name = name

__all__ = ["TestProfile"]
