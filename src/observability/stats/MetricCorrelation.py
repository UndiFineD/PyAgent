#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from dataclasses import dataclass


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class MetricCorrelation:
    """Correlation between two metrics."""
    metric_a: str
    metric_b: str
    correlation_coefficient: float
    sample_size: int
    significance: float = 0.0
