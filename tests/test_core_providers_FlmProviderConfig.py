#!/usr/bin/env python3
"""Presence test for FLM provider config module."""

from src.core.providers import FlmProviderConfig


def test_module_imports_and_validate() -> None:
    """Test that FlmProviderConfig can be imported and validate function runs."""
    FlmProviderConfig.validate()
    assert True
