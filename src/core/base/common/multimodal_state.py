#!/usr/bin/env python3
"""Multimodal stream state helpers (parser-safe minimal impl)."""
from __future__ import annotations

from typing import Optional


class StreamState:
        """Keeps a small buffer of partial stream content between parse calls."""

        def __init__(self) -> None:
                self.buffer: str = ""

        def reset(self) -> None:
                self.buffer = ""
