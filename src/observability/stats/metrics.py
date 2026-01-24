#!/usr/bin/env python3

"""
Metrics.py module.
"""
# Copyright 2026 PyAgent Authors
# Core data structures for metrics and telemetry.

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class MetricType(Enum):
    """Types of metrics."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class Metric:
    """A single metric."""

    name: str
    value: float

    metric_type: MetricType
    timestamp: str = ""
    namespace: str = "default"
    tags: dict[str, str] = field(default_factory=dict)

    # Compatibility: some tests treat history entries as (timestamp, value) tuples.

    def __iter__(self) -> Any:
        yield self.timestamp
        yield self.value

    def __getitem__(self, index: int) -> Any:
        return (self.timestamp, self.value)[index]


@dataclass
class AgentMetric:
    """Telemetry data for a single agent operation."""

    agent_name: str

    operation: str
    duration_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    status: str = "success"
    token_count: int = 0

    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost: float = 0.0
    model: str = "unknown"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MetricSnapshot:
    """A snapshot of metrics at a point in time."""

    name: str

    id: str
    timestamp: str

    metrics: dict[str, float]

    tags: dict[str, str] = field(default_factory=dict)


class AggregationType(Enum):
    """Types of metric aggregation for rollups."""

    SUM = "sum"
    AVG = "average"
    MIN = "minimum"

    MAX = "maximum"
    COUNT = "count"
    P50 = "percentile_50"
    P95 = "percentile_95"
    P99 = "percentile_99"


class AggregationResult(dict[str, Any]):
    """Compatibility class that behaves like both a dict and a float."""

    def __init__(self, value: float = 0.0, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.value = value

    def __float__(self) -> float:
        return float(self.value)


@dataclass
class MetricNamespace:
    """Namespace for organizing metrics."""

    name: str
    description: str = ""
    parent: str | None = None
    tags: dict[str, str] = field(default_factory=dict)

    retention_days: int = 30


@dataclass
class MetricAnnotation:
    """Annotation or comment on a metric."""

    metric_name: str
    timestamp: str
    text: str
    author: str = ""
    annotation_type: str = "info"  # info, warning, milestone


@dataclass
class MetricCorrelation:
    """Correlation between two metrics."""

    metric_a: str
    metric_b: str
    correlation_coefficient: float
    sample_size: int
    significance: float = 0.0


@dataclass
class MetricSubscription:
    """Subscription for metric change notifications."""

    id: str

    metric_pattern: str  # glob pattern like "cpu.*"
    callback_url: str = ""
    notify_on: list[str] = field(default_factory=lambda: ["threshold", "anomaly"])
    min_interval_seconds: int = 60


@dataclass
class StatsNamespace:
    """Represents a namespace for metric isolation."""

    name: str
    metrics: dict[str, list[Metric]] = field(default_factory=dict)
    metric_values: dict[str, float] = field(default_factory=dict)

    def add_metric(self, metric: Metric) -> None:
        if metric.name not in self.metrics:
            self.metrics[metric.name] = []
        self.metrics[metric.name].append(metric)

    def set_metric(self, name: str, value: float) -> None:
        self.metric_values[name] = value

    def get_metric(self, name: str) -> float | None:
        return self.metric_values.get(name)


@dataclass
class StatsSnapshot:
    """A persisted snapshot for StatsSnapshotManager."""

    name: str
    data: dict[str, Any]
    timestamp: str


@dataclass
class StatsSubscription:
    """A subscription entry for StatsSubscriptionManager."""

    id: str
    subscriber_id: str
    metric_pattern: str
    delivery_method: str
    created_at: str


@dataclass
class DerivedMetric:
    """Definition for a metric calculated from other metrics."""

    name: str
    dependencies: list[str]
    formula: str
    description: str = ""


@dataclass
class RetentionPolicy:
    """Policy for data retention."""

    name: str = ""
    retention_days: int = 0
    resolution: str = "1m"
    metric_name: str | None = None
    namespace: str = ""
    max_age_days: int = 0
    max_points: int = 0
    compression_after_days: int = 7


@dataclass
class ABComparisonResult:
    metrics_compared: int
    differences: dict[str, float] = field(default_factory=dict)


@dataclass
class ABSignificanceResult:
    p_value: float
    is_significant: bool
    effect_size: float = 0.0
