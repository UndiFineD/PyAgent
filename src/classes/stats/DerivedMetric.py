#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

@dataclass
class DerivedMetric:
    """A derived metric from dependencies."""
    name: str
    dependencies: List[str]
    formula: str  # e.g., "{metric_a} / {metric_b} * 100"
    description: str = ""
