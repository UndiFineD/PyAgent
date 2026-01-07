#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from .Metric import Metric

from typing import Dict, List, Optional

class StatsNamespace:
    """Represents a namespace for metric isolation."""
    def __init__(self, name: str) -> None:
        self.name = name
        self.metrics: Dict[str, List[Metric]] = {}
        self.metric_values: Dict[str, float] = {}  # Direct metric values for set_metric/get_metric

    def add_metric(self, metric: Metric) -> None:
        """Add a metric to namespace."""
        if metric.name not in self.metrics:
            self.metrics[metric.name] = []
        self.metrics[metric.name].append(metric)

    def set_metric(self, name: str, value: float) -> None:
        """Set a metric value."""
        self.metric_values[name] = value

    def get_metric(self, name: str) -> Optional[float]:
        """Get a metric value."""
        return self.metric_values.get(name)

    def get_metrics(self) -> Dict[str, List[Metric]]:
        """Get all metrics in namespace."""
        return self.metrics
