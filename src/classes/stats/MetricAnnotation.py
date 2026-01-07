#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass

@dataclass
class MetricAnnotation:
    """Annotation or comment on a metric."""
    metric_name: str
    timestamp: str
    text: str
    author: str = ""
    annotation_type: str = "info"  # info, warning, milestone
