#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

@dataclass
class ABComparisonResult:
    """Result of comparing two metric groups."""

    metrics_compared: int
    differences: Dict[str, float] = field(default_factory=lambda: {})
