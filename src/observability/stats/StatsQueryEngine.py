#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from .Metric import Metric

from typing import Any, Dict, List, Optional


































from src.core.base.version import VERSION
__version__ = VERSION

class StatsQueryEngine:
    """Queries metrics with time range and aggregation."""
    def __init__(self) -> None:
        self.metrics: Dict[str, List[Metric]] = {}
        # Lightweight query store used by tests.
        self._rows: Dict[str, List[Dict[str, Any]]] = {}

    def insert(self, metric: str, timestamp: float, value: Any) -> None:
        """Insert a datapoint for querying."""
        if metric not in self._rows:
            self._rows[metric] = []
        self._rows[metric].append({"timestamp": float(timestamp), "value": value})

    def query(
        self,
        metric_name: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        start: Optional[float] = None,
        end: Optional[float] = None,
        aggregation: str = "",
    ) -> Any:
        """Query metrics within time range and/or aggregate.

        Compatibility:
        - Tests call `query(metric, start=..., end=...)` returning a list of dict rows.
        - Tests call `query(metric, aggregation='avg')` returning a dict with `value`.
        """
        # Prefer the test store when present.
        rows = list(self._rows.get(metric_name, []))
        if rows:
            if start is not None or end is not None:
                start_v = float(start) if start is not None else float("-inf")
                end_v = float(end) if end is not None else float("inf")
                rows = [r for r in rows if start_v <= float(r.get("timestamp", 0.0)) <= end_v]

            if aggregation:
                values: List[float] = []
                for r in rows:
                    try:
                        values.append(float(r.get("value")))
                    except Exception:
                        continue
                if not values:
                    agg_value = 0.0
                else:
                    agg = aggregation.lower()
                    if agg == "sum":
                        agg_value = float(sum(values))
                    elif agg in ("avg", "mean"):
                        agg_value = float(sum(values) / len(values))
                    elif agg == "min":
                        agg_value = float(min(values))
                    elif agg == "max":
                        agg_value = float(max(values))
                    else:
                        agg_value = float(sum(values) / len(values))
                return {"metric": metric_name, "aggregation": aggregation, "value": agg_value}

            return rows

        # Fallback to legacy Metric store.
        if metric_name not in self.metrics:
            return []
        return self.metrics[metric_name]

    def add_metric(self, name: str, metric: Metric) -> None:
        """Add metric to query engine."""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(metric)
