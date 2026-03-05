#!/usr/bin/env python3
"""TestAssertion shim for pytest collection."""


class TestAssertion:
    """Represents the result of a test assertion."""

    def __init__(self, name: str, passed: bool = True, details: str | None = None):
        """Initializes a test assertion result."""
        self.name = name
        self.passed = passed
        self.details = details

    def __bool__(self):
        """Returns True if the assertion passed, False otherwise."""
        return bool(self.passed)


__all__ = ["TestAssertion"]
