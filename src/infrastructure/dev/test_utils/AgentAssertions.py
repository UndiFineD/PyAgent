"""Compatibility shim for AgentAssertions in dev test utilities."""


class AgentAssertions:
    """Minimal placeholder for assertion helpers used during test collection."""

    @staticmethod
    def assert_true(expr, msg=None):
        if not expr:
            raise AssertionError(msg or "Assertion failed")

    @staticmethod
    def assert_false(expr, msg=None):
        if expr:
            raise AssertionError(msg or "Assertion failed")
