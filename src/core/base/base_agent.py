#!/usr/bin/env python3
"""Compatibility shim re-exporting `BaseAgent`.

This module provides a lightweight fallback when the full lifecycle module
is not importable during large-scale repair runs.
"""

try:
    from src.core.base.lifecycle.base_agent import BaseAgent  # type: ignore
except Exception:
    try:
        from .lifecycle.base_agent import BaseAgent  # type: ignore
    except Exception:
        class BaseAgent:  # pragma: no cover - fallback stub
            def __init__(self, *args, **kwargs):
                pass


__all__ = ["BaseAgent"]
