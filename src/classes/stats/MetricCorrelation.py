#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass

@dataclass
class MetricCorrelation:
    """Correlation between two metrics."""
    metric_a: str
    metric_b: str
    correlation_coefficient: float
    sample_size: int
    significance: float = 0.0
