#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from .AggregationType import AggregationType

from typing import Dict, List, Tuple

class StatsRollupCalculator:
    """Calculates metric rollups."""
    def __init__(self) -> None:
        self.rollups: Dict[str, List[float]] = {}
        self._points: Dict[str, List[Tuple[float, float]]] = {}

    def add_point(self, metric: str, timestamp: float, value: float) -> None:
        """Add a data point for rollup calculation."""
        if metric not in self._points:
            self._points[metric] = []
        self._points[metric].append((float(timestamp), float(value)))

    def rollup(self, metric: str, interval: str = "1h") -> List[float]:
        """Compute rollups for a metric at the given interval.

        Interval format examples: '1h', '1d', '15m'.
        Returns a list of aggregated values per time bucket (average).
        """
        points = self._points.get(metric, [])
        if not points:
            return []

        unit = interval[-1]
        try:
            amount = int(interval[:-1])
        except Exception:
            amount = 1

        if unit == "m":
            bucket = 60 * amount
        elif unit == "h":
            bucket = 3600 * amount
        elif unit == "d":
            bucket = 86400 * amount
        else:
            bucket = 3600 * amount

        buckets: Dict[int, List[float]] = {}
        for ts, val in points:
            key = int(ts) // int(bucket)
            buckets.setdefault(key, []).append(float(val))

        results: List[float] = []
        for key in sorted(buckets.keys()):
            vals = buckets[key]
            results.append(sum(vals) / len(vals))

        self.rollups[metric] = results
        return results

    def calculate_rollup(self, metrics: List[float], aggregation_type: AggregationType) -> float:
        """Calculate rollup with specified aggregation."""
        if not metrics:
            return 0.0
        if aggregation_type == AggregationType.SUM:
            return sum(metrics)
        elif aggregation_type == AggregationType.AVG:
            return sum(metrics) / len(metrics)
        elif aggregation_type == AggregationType.MIN:
            return min(metrics)
        elif aggregation_type == AggregationType.MAX:
            return max(metrics)
        elif aggregation_type == AggregationType.COUNT:
            return float(len(metrics))
        return 0.0
