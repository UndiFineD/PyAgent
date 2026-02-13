#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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
Observability Core - Telemetry facade and metric models

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
Import observability_core and use its dataclasses and enums (Alert, Threshold, MetricSnapshot, AggregationType, RetentionPolicy, MetricNamespace, etc.) as the canonical in-process telemetry model; use the Metric alias that proxies to src.core.base.common.telemetry_core.Metric for integration with the core telemetry plumbing. The module optionally uses rust_core for accelerated processing when available and exposes structures for alerting, retention, federation, rollups, streaming, and subscriptions.

WHAT IT DOES:
Provides typed dataclasses and enums representing alerts, thresholds, snapshots, retention policies, namespaces, annotations, correlations, subscriptions, export destinations, federation configuration, rollup and streaming configs, and agent-captured metrics. Acts as a thin facade tying these models to the existing telemetry core (Metric) and conditionally enabling rust_core acceleration. Centralizes observability domain types so other components can share a single schema.

WHAT IT SHOULD DO BETTER:
Add robust validation for timestamps, numeric bounds, and operator semantics; prefer stricter typing (from typing import TypedDict/Protocol where appropriate) and more explicit Optional usage. Expose async-friendly helpers for federation polling and streaming, unit tests for serialization/deserialization, and a stable adapter layer for switching between Python and rust implementations with feature-flagged fallbacks. Provide clear conversion helpers to/from telemetry_core.Metric and documented examples for exporters (Prometheus, CloudWatch, Datadog).

FILE CONTENT SUMMARY:
Observability core logic.
(Facade for src.core.base.common.telemetry_core)
"""

import contextlib
import json
import logging
import math
import zlib
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from src.core.base.common.telemetry_core import Metric  # pylint: disable=unused-import

# Try to import rust_core
try:
    import rust_core as rc

    HAS_RUST = True
except ImportError:
    rc = None
    HAS_RUST = False

# Additional types specific to Observability tier


class AlertSeverity(Enum):
    """Severity levels for observability alerts."""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1


@dataclass
class Alert:
    """Represents an observability alert."""
    id: str
    metric_name: str
    current_value: float
    threshold_value: float
    severity: AlertSeverity
    message: str
    timestamp: str


@dataclass
class Threshold:
    """Defines a threshold for a metric."""
    metric_name: str
    min_value: float | None = None
    max_value: float | None = None
    severity: AlertSeverity | None = None
    message: str = ""
    operator: str | None = None
    value: float | None = None


@dataclass
class RetentionPolicy:
    """Policy for data retention."""

    name: str = ""  # Changed from metric_name to name for constructor
    retention_days: int = 0
    resolution: str = "1m"
    metric_name: str | None = None
    namespace: str = ""
    max_age_days: int = 0

    max_points: int = 0
    compression_after_days: int = 7


@dataclass
class MetricSnapshot:
    """A snapshot of metrics at a point in time."""

    name: str
    id: str
    timestamp: str
    metrics: dict[str, float]
    tags: dict[str, str] = field(default_factory=lambda: {})


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


@dataclass
class MetricNamespace:
    """Namespace for organizing metrics."""

    name: str
    description: str = ""
    parent: str | None = None
    tags: dict[str, str] = field(default_factory=lambda: {})
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


class ExportDestination(Enum):
    """Cloud monitoring export destinations."""

    DATADOG = "datadog"
    PROMETHEUS = "prometheus"
    GRAFANA = "grafana"
    CLOUDWATCH = "cloudwatch"
    STACKDRIVER = "stackdriver"


@dataclass
class FederatedSource:
    """A source repository for stats federation."""

    repo_url: str
    api_endpoint: str
    auth_token: str = ""

    poll_interval_seconds: int = 300
    enabled: bool = True
    metrics: dict[str, float] = field(default_factory=dict)


class FederationMode(Enum):
    """Federation modes for multi-repo aggregation."""

    PULL = "pull"

    PUSH = "push"
    HYBRID = "hybrid"


@dataclass
class RollupConfig:
    """Configuration for metric rollups."""

    name: str
    source_metrics: list[str]
    aggregation: AggregationType
    interval_minutes: int = 60
    keep_raw: bool = True


class StreamingProtocol(Enum):
    """Protocols for real-time stats streaming."""

    WEBSOCKET = "websocket"
    SSE = "server_sent_events"
    GRPC = "grpc"
    MQTT = "mqtt"


@dataclass
class StreamingConfig:
    """Configuration for real-time stats streaming."""

    protocol: StreamingProtocol
    endpoint: str
    port: int = 8080
    buffer_size: int = 1000


@dataclass
class AgentMetric:
    """Represents a metric captured from an agent operation."""
    agent_name: str
    operation: str
    duration_ms: f
"""

import contextlib
import json
import logging
import math
import zlib
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from src.core.base.common.telemetry_core import Metric  # pylint: disable=unused-import

# Try to import rust_core
try:
    import rust_core as rc

    HAS_RUST = True
except ImportError:
    rc = None
    HAS_RUST = False

# Additional types specific to Observability tier


class AlertSeverity(Enum):
    """Severity levels for observability alerts."""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1


@dataclass
class Alert:
    """Represents an observability alert."""
    id: str
    metric_name: str
    current_value: float
    threshold_value: float
    severity: AlertSeverity
    message: str
    timestamp: str


@dataclass
class Threshold:
    """Defines a threshold for a metric."""
    metric_name: str
    min_value: float | None = None
    max_value: float | None = None
    severity: AlertSeverity | None = None
    message: str = ""
    operator: str | None = None
    value: float | None = None


@dataclass
class RetentionPolicy:
    """Policy for data retention."""

    name: str = ""  # Changed from metric_name to name for constructor
    retention_days: int = 0
    resolution: str = "1m"
    metric_name: str | None = None
    namespace: str = ""
    max_age_days: int = 0

    max_points: int = 0
    compression_after_days: int = 7


@dataclass
class MetricSnapshot:
    """A snapshot of metrics at a point in time."""

    name: str
    id: str
    timestamp: str
    metrics: dict[str, float]
    tags: dict[str, str] = field(default_factory=lambda: {})


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


@dataclass
class MetricNamespace:
    """Namespace for organizing metrics."""

    name: str
    description: str = ""
    parent: str | None = None
    tags: dict[str, str] = field(default_factory=lambda: {})
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


class ExportDestination(Enum):
    """Cloud monitoring export destinations."""

    DATADOG = "datadog"
    PROMETHEUS = "prometheus"
    GRAFANA = "grafana"
    CLOUDWATCH = "cloudwatch"
    STACKDRIVER = "stackdriver"


@dataclass
class FederatedSource:
    """A source repository for stats federation."""

    repo_url: str
    api_endpoint: str
    auth_token: str = ""

    poll_interval_seconds: int = 300
    enabled: bool = True
    metrics: dict[str, float] = field(default_factory=dict)


class FederationMode(Enum):
    """Federation modes for multi-repo aggregation."""

    PULL = "pull"

    PUSH = "push"
    HYBRID = "hybrid"


@dataclass
class RollupConfig:
    """Configuration for metric rollups."""

    name: str
    source_metrics: list[str]
    aggregation: AggregationType
    interval_minutes: int = 60
    keep_raw: bool = True


class StreamingProtocol(Enum):
    """Protocols for real-time stats streaming."""

    WEBSOCKET = "websocket"
    SSE = "server_sent_events"
    GRPC = "grpc"
    MQTT = "mqtt"


@dataclass
class StreamingConfig:
    """Configuration for real-time stats streaming."""

    protocol: StreamingProtocol
    endpoint: str
    port: int = 8080
    buffer_size: int = 1000


@dataclass
class AgentMetric:
    """Represents a metric captured from an agent operation."""
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


class ObservabilityCore:
    """Pure logic for processing agent telemetry data."""

    def __init__(self) -> None:
        self.metrics_history: list[AgentMetric] = []

    def process_metric(self, metric: AgentMetric) -> None:
        """Standardizes a metric entry."""
        self.metrics_history.append(metric)

    def summarize_performance(self) -> dict[str, Any]:
        """Calculates aggregate stats from history."""
        if not self.metrics_history:
            return {"count": 0, "avg_duration": 0, "total_cost": 0}

        total_duration: float | int = sum(m.duration_ms for m in self.metrics_history)
        total_cost: float | int = sum(m.estimated_cost for m in self.metrics_history)
        count: int = len(self.metrics_history)

        by_agent = self._breakdown_by_agent()

        return {
            "total_count": count,
            "avg_duration_ms": total_duration / count,
            "total_cost_usd": round(total_cost, 6),
            "agents": by_agent,
        }

    def _breakdown_by_agent(self) -> dict[str, dict[str, float]]:
        """Helper to break down metrics by agent."""
        by_agent: dict[str, dict[str, float]] = {}
        for m in self.metrics_history:
            if m.agent_name not in by_agent:
                by_agent[m.agent_name] = {
                    "count": 0,
                    "total_cost": 0,
                    "avg_duration": 0,
                }
            stats = by_agent[m.agent_name]
            stats["count"] += 1
            stats["total_cost"] += m.estimated_cost
        return by_agent

    def filter_by_time(self, start_iso: str, end_iso: str) -> list[AgentMetric]:
        """Filters metrics within a time range."""
        results = []
        for m in self.metrics_history:
            if start_iso <= m.timestamp <= end_iso:
                results.append(m)
        return results

    def calculate_reliability_scores(self, agent_names: list[str]) -> list[float]:
        """
        Calculates normalized reliability scores (0.0 to 1.0) for a list of agents.
        Reliability = success_count / total_attempts.
        If no history, defaults to 0.5 (neutral).
        """
        scores: list[float] = []

        # Aggregate history per agent
        stats: dict[str, dict[str, int]] = {}
        for m in self.metrics_history:
            if m.agent_name not in stats:
                stats[m.agent_name] = {"success": 0, "total": 0}
            stats[m.agent_name]["total"] += 1
            if m.status == "success":
                stats[m.agent_name]["success"] += 1

        for name in agent_names:
            if name in stats and stats[name]["total"] > 0:
                score: float = stats[name]["success"] / stats[name]["total"]
                scores.append(score)
            else:
                # Neutral default for new/unknown agents
                scores.append(0.5)

        return scores


class StatsCore:
    """Core logic for statistics processing, separated from the Agent shell."""

    @staticmethod
    def detect_anomaly(history: list[Metric], value: float, threshold_std: float = 2.0) -> tuple[bool, float]:
        """Detect if a value is anomalous using standard deviation."""
        if len(history) < 2:
            return False, 0.0

        values: list[float] = [m.value for m in history]
        mean: float = sum(values) / len(values)
        variance: float = sum((x - mean) ** 2 for x in values) / len(values)
        std: float = math.sqrt(variance) if variance > 0 else 0.001
        z_score: float = abs((value - mean) / std)
        return z_score > threshold_std, z_score

    @staticmethod
    def forecast(history: list[Metric], periods: int = 5) -> list[float]:
        """Simple linear forecasting for a metric."""
        if len(history) < 3:
            return []
        values: list[float] = [m.value for m in history]
        # Rust-accelerated linear regression
        if HAS_RUST:
            with contextlib.suppress(Exception):
                return rc.linear_forecast_rust(values, periods)  # type: ignore[attr-defined]

        n: int = len(values)
        x_mean: float = (n - 1) / 2
        y_mean: float = sum(values) / n
        numerator: float | int = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator: float | int = sum((i - x_mean) ** 2 for i in range(n))
        if denominator == 0:
            return [y_mean] * periods
        slope: float = numerator / denominator
        intercept: float = y_mean - slope * x_mean
        return [slope * (n + i) + intercept for i in range(periods)]

    @staticmethod
    def compress_metrics(metrics: list[Metric]) -> bytes:
        """Compress metric history."""
        if not metrics:
            return b""
        data: str = json.dumps([{"value": m.value, "timestamp": m.timestamp, "tags": m.tags} for m in metrics])
        return zlib.compress(data.encode("utf-8"))

    @staticmethod
    def visualize_stats(stats: dict[str, Any]) -> None:
        """Generate CLI graphs for stats visualization."""
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            logging.warning("matplotlib not available for visualization")
            return

        labels: list[str] = list(stats.keys())
        values: list[Any] = list(stats.values())
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color="skyblue")
        plt.xlabel("Metrics")
        plt.ylabel("Values")
        plt.title("Stats Visualization")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        plt.show()

    @staticmethod
    def compare_snapshots(s1: MetricSnapshot, s2: MetricSnapshot) -> dict[str, dict[str, float | int]]:
        """Compare two snapshots."""
        comparison = {}
        all_keys = set(s1.metrics.keys()) | set(s2.metrics.keys())
        for key in all_keys:
            v1 = s1.metrics.get(key, 0.0)
            v2 = s2.metrics.get(key, 0.0)
            comparison[key] = {
                "snapshot1": v1,
                "snapshot2": v2,
                "difference": v2 - v1,
                "percentage_change": ((v2 - v1) / v1 * 100) if v1 != 0 else 0,
            }
        return comparison

    @staticmethod
    def apply_retention(metrics_dict: dict[str, list[Metric]], policies: dict[str, RetentionPolicy]) -> int:
        """Apply retention policies to metrics."""
        removed = 0
        now: datetime = datetime.now()
        for key, metrics in list(metrics_dict.items()):
            namespace: str = metrics[0].namespace if metrics else "default"
            policy: RetentionPolicy | None = policies.get(key) or policies.get(namespace)
            if not policy:
                continue

            if policy.max_age_days > 0:
                cutoff: datetime = now - timedelta(days=policy.max_age_days)
                orig: int = len(metrics)
                metrics_dict[key] = [m for m in metrics if datetime.fromisoformat(m.timestamp) > cutoff]
                removed += orig - len(metrics_dict[key])

            if policy.max_points > 0 and len(metrics_dict[key]) > policy.max_points:
                removed += len(metrics_dict[key]) - policy.max_points
                metrics_dict[key] = metrics_dict[key][-policy.max_points :]
        return removed


class StatsNamespace:
    """Represents a namespace for metric isolation."""

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.metrics: dict[str, list[Metric]] = {}
        self.metric_values: dict[str, float] = {}  # Direct metric values for set_metric/get_metric

    def add_metric(self, metric: Metric) -> None:
        """Add a metric to namespace."""
        if metric.name not in self.metrics:
            self.metrics[metric.name] = []
        self.metrics[metric.name].append(metric)

    def set_metric(self, name: str, value: float) -> None:
        """Set a metric value."""
        self.metric_values[name] = value

    def get_metric(self, name: str) -> float | None:
        """Get a metric value."""
        return self.metric_values.get(name)

    def get_metrics(self) -> dict[str, list[Metric]]:
        """Get all metrics in namespace."""
        return self.metrics


class StatsNamespaceManager:
    """Manages multiple namespaces."""

    def __init__(self) -> None:
        self.namespaces: dict[str, StatsNamespace] = {}

    def create(self, name: str) -> StatsNamespace:
        """Create a new namespace."""
        ns = StatsNamespace(name)
        self.namespaces[name] = ns
        return ns

    def create_namespace(self, name: str) -> StatsNamespace:
        """Create a new namespace (backward compat)."""
        return self.create(name)

    def get_namespace(self, name: str) -> StatsNamespace | None:
        """Get a namespace."""
        return self.namespaces.get(name)


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
class ThresholdAlert:
    """A single threshold alert emitted by ThresholdAlertManager."""

    metric: str
    value: float
    severity: str
    threshold: float


@dataclass
class DerivedMetric:
    """A metric derived from other metrics via a formula."""
    name: str
    dependencies: list[str]
    formula: str
    description: str = ""
