#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Rollup engine.py module.
"""
# Rollup, query, and correlation analyzer engine.
# Phase 16: Rust acceleration for aggregation and percentile calculations

from __future__ import annotations

import contextlib
import logging
import math
from datetime import datetime
from typing import Any

from .metrics import AggregationType, Metric
from .metrics_core import CorrelationCore, StatsRollupCore
from .observability_core import RollupConfig

logger: logging.Logger = logging.getLogger(__name__)

# Phase 16: Rust acceleration imports
try:
    import rust_core

    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False
    logging.debug("rust_core not available, using Python fallback for RollupEngine")


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
        points: list[tuple[float, float]] = self._points.get(metric, [])
        if not points:
            return []

        unit: str = interval[-1]
        amount = 1
        with contextlib.suppress(Exception):
            amount = int(interval[:-1])

        if unit == "m":
            bucket: int = 60 * amount
        elif unit == "h":
            bucket: int = 3600 * amount
        elif unit == "d":
            bucket: int = 86400 * amount
        else:
            bucket: int = 3600 * amount

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

    def calculate_rollup(self, metrics: list[float], aggregation_type: AggregationType) -> float:
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

    def add_value(self, metric_name: str, value: float, timestamp: datetime | None = None) -> None:
        ts: datetime = timestamp or datetime.now()
        if metric_name not in self._raw_data:
            self._raw_data[metric_name] = []
        self._raw_data[metric_name].append((ts, value))

    def compute_rollup(self, name: str) -> list[dict[str, Any]]:
        config: RollupConfig | None = self.configs.get(name)
        if not config:
            return []
        all_values: list[float] = []
        for metric in config.source_metrics:
            values = self._raw_data.get(metric, [])
            all_values.extend(v for _, v in values)
        if not all_values:
            return []

        result = self._try_rust_aggregation(config, all_values)
        if result is None:
            result = self._python_aggregation(config, all_values)

        rollup_entry: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "value": result,
            "sample_count": len(all_values),
            "aggregation": config.aggregation.value,
        }
        self.rollups[name].append(rollup_entry)
        if not config.keep_raw:
            self._clear_raw_data(config)
        return self.rollups[name]

    def _try_rust_aggregation(self, config: RollupConfig, all_values: list[float]) -> float | None:
        if not _RUST_AVAILABLE:
            return None
        with contextlib.suppress(Exception):
            if config.aggregation == AggregationType.SUM and hasattr(rust_core, "calculate_sum_rust"):
                return rust_core.calculate_sum_rust(all_values)
            elif config.aggregation == AggregationType.AVG and hasattr(rust_core, "calculate_avg_rust"):
                return rust_core.calculate_avg_rust(all_values)
            elif config.aggregation == AggregationType.MIN and hasattr(rust_core, "calculate_min_rust"):
                return rust_core.calculate_min_rust(all_values)
            elif config.aggregation == AggregationType.MAX and hasattr(rust_core, "calculate_max_rust"):
                return rust_core.calculate_max_rust(all_values)
            elif config.aggregation == AggregationType.P50 and hasattr(rust_core, "calculate_median_rust"):
                return rust_core.calculate_median_rust(all_values)
            elif config.aggregation == AggregationType.P95 and hasattr(rust_core, "calculate_p95_rust"):
                return rust_core.calculate_p95_rust(all_values)
            elif config.aggregation == AggregationType.P99 and hasattr(rust_core, "calculate_p99_rust"):
                return rust_core.calculate_p99_rust(all_values)
        return None

    def _python_aggregation(self, config: RollupConfig, all_values: list[float]) -> float:
        agg = config.aggregation
        if agg == AggregationType.SUM:
            return sum(all_values)
        elif agg == AggregationType.AVG:
            return sum(all_values) / len(all_values)
        elif agg == AggregationType.MIN:
            return min(all_values)
        elif agg == AggregationType.MAX:
            return max(all_values)
        elif agg == AggregationType.COUNT:
            return float(len(all_values))
        elif agg in (AggregationType.P50, AggregationType.P95, AggregationType.P99):
            return self._percentile_aggregation(agg, all_values)
        else:
            return sum(all_values) / len(all_values)

    def _percentile_aggregation(self, agg: AggregationType, all_values: list[float]) -> float:
        sorted_vals = sorted(all_values)
        if agg == AggregationType.P50:
            return sorted_vals[len(sorted_vals) // 2]
        elif agg == AggregationType.P95:
            return sorted_vals[int(len(sorted_vals) * 0.95)]
        elif agg == AggregationType.P99:
            return sorted_vals[int(len(sorted_vals) * 0.99)]
        return sorted_vals[len(sorted_vals) // 2]

    def _clear_raw_data(self, config: RollupConfig) -> None:
        for metric in config.source_metrics:
            self._raw_data[metric] = []

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
        start_time: str | None = None,  # noqa: ARG002
        end_time: str | None = None,  # noqa: ARG002
        start: float | None = None,
        end: float | None = None,
        aggregation: str = "",
    ) -> Any:
        rows: list[dict[str, Any]] = list(self._rows.get(metric_name, []))
        if rows:
            if start is not None or end is not None:
                start_v: float = float(start) if start is not None else float("-inf")
                end_v: float = float(end) if end is not None else float("inf")
                rows = [r for r in rows if start_v <= float(r.get("timestamp", 0.0)) <= end_v]

            if aggregation:
                values: list[float] = []
                for r in rows:
                    with contextlib.suppress(Exception):
                        values.append(float(r.get("value")))
                if not values:
                    agg_value = 0.0
                else:
                    agg: str = aggregation.lower()
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
        self.correlations: list[Any] = []  # Use Any for MetricCorrelation to avoid circular import if needed
        self._metric_history: dict[str, list[float]] = {}
        self.core = CorrelationCore()

    def record_value(self, metric_name: str, value: float) -> None:
        if metric_name not in self._metric_history:
            self._metric_history[metric_name] = []
        self._metric_history[metric_name].append(value)

    def compute_correlation(self, metric_a: str, metric_b: str) -> Any:
        values_a: list[float] = self._metric_history.get(metric_a, [])
        values_b: list[float] = self._metric_history.get(metric_b, [])
        n: int = min(len(values_a), len(values_b))
        if n < 3:
            return None
        values_a: list[float] = values_a[-n:]
        values_b: list[float] = values_b[-n:]

        # Rust optimization
        try:
            import rust_core as rc

            correlation = rc.calculate_pearson_correlation(values_a, values_b)
        except (ImportError, AttributeError):
            # Pearson correlation fallback
            mean_a: float = sum(values_a) / n
            mean_b: float = sum(values_b) / n
            numerator: float | int = sum((values_a[i] - mean_a) * (values_b[i] - mean_b) for i in range(n))
            denom_a: float = math.sqrt(sum((x - mean_a) ** 2 for x in values_a))
            denom_b: float = math.sqrt(sum((x - mean_b) ** 2 for x in values_b))
            if denom_a == 0 or denom_b == 0:
                return None
            correlation: float = numerator / (denom_a * denom_b)

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

        keys: list[str] = list(self._metric_history.keys())

        # Rust-accelerated O(N²) pairwise correlation
        with contextlib.suppress(ImportError, Exception):
            from rust_core import \
                find_strong_correlations_rust  # pylint: disable=no-name-in-module

            metric_values: list[list[float]] = [self._metric_history[k] for k in keys]
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

        # Python fallback: Re-compute pairwise for all history (O(N^2) naive)
        strong = []
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                corr = self.compute_correlation(keys[i], keys[j])
                if corr and abs(corr.correlation_coefficient) >= threshold:
                    strong.append(corr)
        return strong
