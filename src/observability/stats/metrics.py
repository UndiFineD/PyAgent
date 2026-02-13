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
Metrics - Core metric types and telemetry structures

Brief Summary
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Import the module and create Metric, AgentMetric, MetricSnapshot, StatsNamespace, or other dataclasses to record and pass telemetry.
- Use StatsNamespace.add_metric() to accumulate time-series Metric entries and set_metric()/get_metric() for current values.
- Use AggregationResult and AggregationType for compatibility with rollups and percentile/summary results; use MetricSubscription/StatsSubscription to register notification interests.

WHAT IT DOES:
- Defines enums and lightweight dataclasses representing metrics, telemetry events, snapshots, namespaces, annotations, correlations, subscriptions, derived metrics, retention policies, and simple in-memory stats containers.
- Provides small compatibility conveniences (Metric supports tuple-like iteration and indexing; AggregationResult behaves like a dict with a float value).
- Offers a minimal in-memory StatsNamespace for collecting lists of Metric objects per name and simple metric value storage.

WHAT IT SHOULD DO BETTER:
- Add serialization helpers (to_dict/from_dict), validation, and strict unit tests for all dataclasses (especially for timestamps and tag types).
- Provide timezone-aware timestamps, consistent ISO formatting, and optional typed timestamps (datetime) rather than plain strings.
- Implement thread/process-safety for StatsNamespace (locks or concurrent structures) and efficient retention/eviction per MetricNamespace.retention_days.
- Add aggregation/rollup functions (count, percentiles, histograms) and integration points for persistence/export (StateTransaction-compatible snapshotting, persistence adapters).
- Provide clear API for subscriptions (webhook signing, retry/backoff, delivery guarantees) and metrics ingestion (batching, rate limiting) and document expected semantics for MetricType vs. aggregation behavior.
- Consider richer metadata typing (TypedDict), explicit provenance (CascadeContext), and benchmarking for large-scale metric workloads (rust-backed heavy lifting).

FILE CONTENT SUMMARY:
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
Metrics.py module.
"""
# Core data structures for metrics and telemetry.

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__: str = VERSION


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
        self.value: float = value

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
    """Policy for dat
"""
# Core data structures for metrics and telemetry.

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__: str = VERSION


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
        self.value: float = value

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
