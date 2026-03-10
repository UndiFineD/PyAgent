#!/usr/bin/env python3
"""Smoke test for workflow engine module."""

from src.core.workflow import engine


def test_engine_imports_and_validate() -> None:
    engine.validate()
    assert True
