#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from .AggregationType import AggregationType
from .RollupConfig import RollupConfig

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

class StatsRollup:
    """Aggregate metrics into rollup views.

    Provides rollup capabilities for aggregating metrics
    over time intervals.

    Attributes:
        configs: Rollup configurations.
        rollups: Computed rollup data.
    """

    def __init__(self) -> None:
        """Initialize stats rollup."""
        self.configs: Dict[str, RollupConfig] = {}
        self.rollups: Dict[str, List[Dict[str, Any]]] = {}
        self._raw_data: Dict[str, List[Tuple[datetime, float]]] = {}

    def configure_rollup(
        self,
        name: str,
        source_metrics: List[str],
        aggregation: AggregationType,
        interval_minutes: int = 60,
        keep_raw: bool = True
    ) -> RollupConfig:
        """Configure a rollup.

        Args:
            name: Name for the rollup.
            source_metrics: Source metric names.
            aggregation: Aggregation type to use.
            interval_minutes: Rollup interval in minutes.
            keep_raw: Whether to keep raw data.

        Returns:
            The rollup configuration.
        """
        config = RollupConfig(
            name=name,
            source_metrics=source_metrics,
            aggregation=aggregation,
            interval_minutes=interval_minutes,
            keep_raw=keep_raw
        )
        self.configs[name] = config
        self.rollups[name] = []
        return config

    def add_value(
        self,
        metric_name: str,
        value: float,
        timestamp: Optional[datetime] = None
    ) -> None:
        """Add a value for rollup processing.

        Args:
            metric_name: The metric name.
            value: The value to add.
            timestamp: Optional timestamp (default: now).
        """
        ts = timestamp or datetime.now()
        if metric_name not in self._raw_data:
            self._raw_data[metric_name] = []
        self._raw_data[metric_name].append((ts, value))

    def compute_rollup(self, name: str) -> List[Dict[str, Any]]:
        """Compute rollup for a configuration.

        Args:
            name: The rollup name.

        Returns:
            List of rollup values.
        """
        config = self.configs.get(name)
        if not config:
            return []
        # Collect all values for source metrics
        all_values: List[float] = []
        for metric in config.source_metrics:
            values = self._raw_data.get(metric, [])
            all_values.extend(v for _, v in values)
        if not all_values:
            return []
        # Apply aggregation
        if config.aggregation == AggregationType.SUM:
            result = sum(all_values)
        elif config.aggregation == AggregationType.AVG:
            result = sum(all_values) / len(all_values)
        elif config.aggregation == AggregationType.MIN:
            result = min(all_values)
        elif config.aggregation == AggregationType.MAX:
            result = max(all_values)
        elif config.aggregation == AggregationType.COUNT:
            result = float(len(all_values))
        elif config.aggregation == AggregationType.P50:
            sorted_vals = sorted(all_values)
            result = sorted_vals[len(sorted_vals) // 2]
        elif config.aggregation == AggregationType.P95:
            sorted_vals = sorted(all_values)
            result = sorted_vals[int(len(sorted_vals) * 0.95)]
        elif config.aggregation == AggregationType.P99:
            sorted_vals = sorted(all_values)
            result = sorted_vals[int(len(sorted_vals) * 0.99)]
        else:
            result = sum(all_values) / len(all_values)
        rollup_entry: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "value": result,
            "sample_count": len(all_values),
            "aggregation": config.aggregation.value
        }
        self.rollups[name].append(rollup_entry)
        # Clear raw data if not keeping
        if not config.keep_raw:
            for metric in config.source_metrics:
                self._raw_data[metric] = []
        return self.rollups[name]

    def get_rollup_history(self, name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get rollup history.

        Args:
            name: The rollup name.
            limit: Maximum entries to return.

        Returns:
            List of rollup entries.
        """
        return self.rollups.get(name, [])[-limit:]
