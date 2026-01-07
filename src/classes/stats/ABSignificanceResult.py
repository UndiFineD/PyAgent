#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass

@dataclass
class ABSignificanceResult:
    """Result of A/B statistical significance calculation."""

    p_value: float
    is_significant: bool
    effect_size: float = 0.0
