#!/usr/bin/env python3
"""Presence test for FLM provider config module."""

from src.core.providers import FlmProviderConfig


def test_module_imports_and_validate() -> None:
    FlmProviderConfig.validate()
    assert True
