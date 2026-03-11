#!/usr/bin/env python3
"""Existence test for runtime module."""


def test_runtime_import_and_validate() -> None:
    """TDD: importing the runtime module should expose Runtime and validate()."""
    import importlib

    runtime = importlib.import_module("src.core.runtime")

    assert hasattr(runtime, "Runtime"), "Runtime class not found"
    assert callable(getattr(runtime, "validate", None)), "validate() is not callable"

    # Running validate() should be import-safe and cheap
    runtime.validate()
