from __future__ import annotations


"""
UI package for userspace interface components.

This module intentionally keeps a minimal, import-safe surface so tests
can import the `userspace.interface.ui` package even when deeper modules
may be under repair. It exposes a lightweight `__all__` and `__version__`.
"""
from typing import List

try:
    from src.core.base.lifecycle.version import VERSION
except Exception:
    VERSION = "0.0.0"

__version__ = VERSION

__all__: List[str] = []
