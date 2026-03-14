#!/usr/bin/env python3
from __future__ import annotations

from src.core.base.shell import ShellExecutor  # type: ignore

__all__ = ["ShellExecutor"]

r"""Compatibility shim to expose `ShellExecutor` at
`src.core.base.ShellExecutor` (capitalized module name).

Some modules import the capitalized module path; re-export the
implementation from `src.core.base.shell` to satisfy those imports
without changing existing code.
"""
