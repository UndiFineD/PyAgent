#!/usr/bin/env python3
"""Smoke test for workflow engine module."""

from src.core.workflow import engine


def test_engine_imports_and_validate() -> None:
    """Test that the workflow engine can be imported and validate() runs."""
    engine.validate()
    assert True
