#!/usr/bin/env python3
"""Speculation module for PyAgent."""

from __future__ import annotations


def validate() -> bool:
    """Validate speculation package readiness for runtime imports."""
    return __name__ == "src.speculation"


__all__ = ["validate"]
