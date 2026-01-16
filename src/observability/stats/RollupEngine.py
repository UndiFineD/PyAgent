#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Rollup, query, and correlation analyzer engine.

from __future__ import annotations
import logging
import math
from datetime import datetime
from typing import Any
from .Metrics import AggregationType, Metric
from .ObservabilityCore import RollupConfig
from .MetricsCore import StatsRollupCore, CorrelationCore

logger = logging.getLogger(__name__)


class StatsRollupCalculator:
    """Calculates metric rollups using pure logic core."""

    def __init__(self) -> None:
        self.rollups: dict[str, list[float]] = {}
        self._points: dict[str, list[tuple[float, float]]] = {}
        self.core = StatsRollupCore()

    def add_point(self, metric: str, timestamp: float, value: float) -> None:
        if metric not in self._points:
            self._points[metric] = []
        self._points[metric].append((float(timestamp), float(value)))

    def rollup(self, metric: str, interval: str = "1h") -> list[float]:
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

        buckets: dict[int, list[float]] = {}
        for ts, val in points:
            key = int(ts) // int(bucket)
            buckets.setdefault(key, []).append(float(val))

        results: list[float] = []
        for key in sorted(buckets.keys()):
            vals = buckets[key]
            results.append(sum(vals) / len(vals))

        self.rollups[metric] = results
        return results

    def calculate_rollup(
        self, metrics: list[float], aggregation_type: AggregationType
    ) -> float:
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


class StatsRollup:
    """Aggregate metrics into rollup views."""

    def __init__(self) -> None:
        self.configs: dict[str, RollupConfig] = {}
        self.rollups: dict[str, list[dict[str, Any]]] = {}
        self._raw_data: dict[str, list[tuple[datetime, float]]] = {}

    def configure_rollup(
        self,
        name: str,
        source_metrics: list[str],
        aggregation: AggregationType,
        interval_minutes: int = 60,
        keep_raw: bool = True,
    ) -> RollupConfig:
        config = RollupConfig(
            name=name,
            source_metrics=source_metrics,
            aggregation=aggregation,
            interval_minutes=interval_minutes,
            keep_raw=keep_raw,
        )
        self.configs[name] = config
        self.rollups[name] = []
        return config

    def add_value(
        self, metric_name: str, value: float, timestamp: datetime | None = None
    ) -> None:
        ts = timestamp or datetime.now()
        if metric_name not in self._raw_data:
            self._raw_data[metric_name] = []
        self._raw_data[metric_name].append((ts, value))

    def compute_rollup(self, name: str) -> list[dict[str, Any]]:
        config = self.configs.get(name)

        if not config:
            return []
        all_values: list[float] = []
        for metric in config.source_metrics:
            values = self._raw_data.get(metric, [])
            all_values.extend(v for _, v in values)
        if not all_values:
            return []

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

        rollup_entry: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "value": result,
            "sample_count": len(all_values),
            "aggregation": config.aggregation.value,
        }
        self.rollups[name].append(rollup_entry)
        if not config.keep_raw:
            for metric in config.source_metrics:
                self._raw_data[metric] = []
        return self.rollups[name]

    def get_rollup_history(self, name: str, limit: int = 100) -> list[dict[str, Any]]:
        return self.rollups.get(name, [])[-limit:]


class StatsQueryEngine:
    """Queries metrics with time range and aggregation."""

    def __init__(self) -> None:
        self.metrics: dict[str, list[Metric]] = {}
        self._rows: dict[str, list[dict[str, Any]]] = {}

    def insert(self, metric: str, timestamp: float, value: Any) -> None:
        if metric not in self._rows:
            self._rows[metric] = []
        self._rows[metric].append({"timestamp": float(timestamp), "value": value})

    def query(
        self,
        metric_name: str,
        start_time: str | None = None,
        end_time: str | None = None,
        start: float | None = None,
        end: float | None = None,
        aggregation: str = "",
    ) -> Any:
        rows = list(self._rows.get(metric_name, []))
        if rows:
            if start is not None or end is not None:
                start_v = float(start) if start is not None else float("-inf")
                end_v = float(end) if end is not None else float("inf")
                rows = [
                    r
                    for r in rows
                    if start_v <= float(r.get("timestamp", 0.0)) <= end_v
                ]

            if aggregation:
                values: list[float] = []
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
                return {
                    "metric": metric_name,
                    "aggregation": aggregation,
                    "value": agg_value,
                }
            return rows

        if metric_name not in self.metrics:
            return []
        return self.metrics[metric_name]

    def add_metric(self, name: str, metric: Metric) -> None:
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(metric)


class CorrelationAnalyzer:
    """Analyze correlations between metrics."""

    def __init__(self) -> None:
        self.correlations: list[
            Any
        ] = []  # Use Any for MetricCorrelation to avoid circular import if needed
        self._metric_history: dict[str, list[float]] = {}
        self.core = CorrelationCore()

    def record_value(self, metric_name: str, value: float) -> None:
        if metric_name not in self._metric_history:
            self._metric_history[metric_name] = []
        self._metric_history[metric_name].append(value)

    def compute_correlation(self, metric_a: str, metric_b: str) -> Any:
        values_a = self._metric_history.get(metric_a, [])
        values_b = self._metric_history.get(metric_b, [])
        n = min(len(values_a), len(values_b))
        if n < 3:
            return None
        values_a = values_a[-n:]
        values_b = values_b[-n:]

        # Rust optimization
        try:
            import rust_core as rc

            correlation = rc.calculate_pearson_correlation(values_a, values_b)
        except (ImportError, AttributeError):
            # Pearson correlation fallback
            mean_a = sum(values_a) / n
            mean_b = sum(values_b) / n
            numerator = sum(
                (values_a[i] - mean_a) * (values_b[i] - mean_b) for i in range(n)
            )
            denom_a = math.sqrt(sum((x - mean_a) ** 2 for x in values_a))
            denom_b = math.sqrt(sum((x - mean_b) ** 2 for x in values_b))
            if denom_a == 0 or denom_b == 0:
                return None
            correlation = numerator / (denom_a * denom_b)

        from types import SimpleNamespace

        result = SimpleNamespace(
            metric_a=metric_a,
            metric_b=metric_b,
            correlation_coefficient=correlation,
            sample_size=n,
        )
        self.correlations.append(result)
        return result

    def find_strong_correlations(self, threshold: float = 0.8) -> list[Any]:
        """Find strong correlations."""
        from types import SimpleNamespace
        keys = list(self._metric_history.keys())
        
        # Rust-accelerated O(N²) pairwise correlation
        try:
            from rust_core import find_strong_correlations_rust
            metric_values = [self._metric_history[k] for k in keys]
            rust_results = find_strong_correlations_rust(metric_values, threshold)
            
            strong = []
            for i, j, corr in rust_results:
                result = SimpleNamespace(
                    metric_a=keys[i],
                    metric_b=keys[j],
                    correlation_coefficient=corr,
                    sample_size=min(len(metric_values[i]), len(metric_values[j])),
                )
                self.correlations.append(result)
                strong.append(result)
            return strong
        except (ImportError, Exception):
            pass  # Fall back to Python
        
        # Python fallback: Re-compute pairwise for all history (O(N^2) naive)
        strong = []
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                corr = self.compute_correlation(keys[i], keys[j])
                if corr and abs(corr.correlation_coefficient) >= threshold:
                    strong.append(corr)
        return strong
