#!/usr/bin/env python3
"""Presence test for FLM chat adapter module."""

from src.core.providers import FlmChatAdapter


def test_module_imports_and_validate() -> None:
    """Test that FlmChatAdapter can be imported and validate function runs."""
    # ensure validate symbol exists and can be called
    FlmChatAdapter.validate()
    assert True
