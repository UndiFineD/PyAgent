"""Minimal shim for test utilities used during collection.

Provides a lightweight `AgentAssertions` class so import-time checks succeed.
Full test behavior isn't implemented — this is only to unblock collection.
"""

class AgentAssertions:
    """Placeholder assertion helpers used in tests."""

    @staticmethod
    def assert_true(expr, msg=None):
        if not expr:
            raise AssertionError(msg or "Assertion failed")

    @staticmethod
    def assert_false(expr, msg=None):
        if expr:
            raise AssertionError(msg or "Assertion failed")
