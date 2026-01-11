#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from dataclasses import dataclass
from typing import List


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class DerivedMetric:
    """A derived metric from dependencies."""
    name: str
    dependencies: List[str]
    formula: str  # e.g., "{metric_a} / {metric_b} * 100"
    description: str = ""
