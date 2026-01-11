#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from enum import Enum


































from src.core.base.version import VERSION
__version__ = VERSION

class ExportDestination(Enum):
    """Cloud monitoring export destinations."""
    DATADOG = "datadog"
    PROMETHEUS = "prometheus"
    GRAFANA = "grafana"
    CLOUDWATCH = "cloudwatch"
    STACKDRIVER = "stackdriver"
