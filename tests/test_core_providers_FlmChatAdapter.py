#!/usr/bin/env python3
"""Presence test for FLM chat adapter module."""

import pytest

# importing FlmChatAdapter may transitively import openai/pydantic and
# trigger a SystemError if the pydantic-core version mismatch exists.
try:
    from src.core.providers import FlmChatAdapter
except SystemError as e:
    pytest.skip(f"Skipping FlmChatAdapter tests due to import error: {e}", allow_module_level=True)


def test_module_imports_and_validate() -> None:
    """Test that FlmChatAdapter can be imported and validate function runs."""
    # ensure validate symbol exists and can be called
    FlmChatAdapter.validate()
    assert True
