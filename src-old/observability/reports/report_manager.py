#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""Minimal ReportManager stub to satisfy imports during tests.

This module provides a lightweight placeholder implementation so the
observability.reports package can be imported during pytest collection.
The real implementation may live elsewhere; the stub keeps test
collection progressing while other import-time issues are resolved.
"""

from __future__ import annotations
from pathlib import Path
from typing import Any


class ReportManager:
    """Simple placeholder for the real ReportManager.

    Methods are intentionally minimal; expand if tests require more.
    """

    def __init__(self, storage: Any = None) -> None:
        self.storage = storage

    def register(self, name: str, obj: Any) -> None:
        """Register a report or helper (no-op stub)."""
        return None

    def get(self, name: str) -> Any:
        """Return a registered item or None."""
        return None

    def list_reports(self) -> list[str]:
        """Return an empty list in the stub."""
        return []


__all__ = ["ReportManager"]
