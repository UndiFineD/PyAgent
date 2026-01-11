#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from dataclasses import dataclass


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class ABSignificanceResult:
    """Result of A/B statistical significance calculation."""

    p_value: float
    is_significant: bool
    effect_size: float = 0.0
