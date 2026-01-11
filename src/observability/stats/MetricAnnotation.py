#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from dataclasses import dataclass


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class MetricAnnotation:
    """Annotation or comment on a metric."""
    metric_name: str
    timestamp: str
    text: str
    author: str = ""
    annotation_type: str = "info"  # info, warning, milestone
