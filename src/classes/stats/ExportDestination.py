#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from enum import Enum

class ExportDestination(Enum):
    """Cloud monitoring export destinations."""
    DATADOG = "datadog"
    PROMETHEUS = "prometheus"
    GRAFANA = "grafana"
    CLOUDWATCH = "cloudwatch"
    STACKDRIVER = "stackdriver"
