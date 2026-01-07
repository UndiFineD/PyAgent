#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from typing import Any, Dict
import os

class EnvironmentIsolator:
    """Context manager that restores environment variables on exit."""

    def __init__(self) -> None:
        self._original: Dict[str, str] = {}

    def __enter__(self) -> "EnvironmentIsolator":
        self._original = dict(os.environ)
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        os.environ.clear()
        os.environ.update(self._original)

    def set_env(self, key: str, value: str) -> None:
        os.environ[str(key)] = str(value)
