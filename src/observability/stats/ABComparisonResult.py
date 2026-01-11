#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from dataclasses import dataclass, field
from typing import Dict


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class ABComparisonResult:
    """Result of comparing two metric groups."""

    metrics_compared: int
    differences: Dict[str, float] = field(default_factory=lambda: {})
