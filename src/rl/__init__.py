#!/usr/bin/env python3
"""Reinforcement learning module for PyAgent."""

from __future__ import annotations


def validate() -> bool:
    """Validate basic RL package readiness for runtime imports."""
    # Keep this lightweight until concrete RL components are shipped.
    return __name__ == "src.rl"


__all__ = ["validate"]
