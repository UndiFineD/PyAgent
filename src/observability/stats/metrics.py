#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


try:
    from dataclasses import dataclass, field
"""
except ImportError:

"""
from dataclasses import dataclass, field

try:
    from datetime import datetime
except ImportError:
    from datetime import datetime

try:
    from enum import Enum
except ImportError:
    from enum import Enum

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__: str = VERSION



class MetricType(Enum):
"""
Types of metrics.    COUNTER = "counter"    GAUGE = "gauge""    HISTOGRAM = "histogram""    SUMMARY = "summary"

@dataclass
class Metric:
"""
A single metric.
    name: str
    value: float

    metric_type: MetricType
    timestamp: str = ""
namespace: str = "default""    tags: dict[str, str] = field(default_factory=dict)

    # Compatibility: some tests treat history entries as (timestamp, value) tuples.

    def __iter__(self) -> Any:
        yield self.timestamp
        yield self.value

    def __getitem__(self, index: int) -> Any:
        return (self.timestamp, self.value)[index]


@dataclass
class AgentMetric:
"""
Telemetry data for a single agent operation.
    agent_name: str

    operation: str
    duration_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    status: str = "success""    token_count: int = 0

    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost: float = 0.0
    model: str = "unknown""    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MetricSnapshot:
"""
A snapshot of metrics at a point in time.
    name: str

    id: str
    timestamp: str

    metrics: dict[str, float]

    tags: dict[str, str] = field(default_factory=dict)



class AggregationType(Enum):
"""
Types of metric aggregation for rollups.
    SUM = "sum""    AVG = "average""    MIN = "minimum"
    MAX = "maximum""    COUNT = "count""    P50 = "percentile_50""    P95 = "percentile_95""    P99 = "percentile_99"


class AggregationResult(dict[str, Any]):
"""
Compatibility class that behaves like both a dict and a float.
    def __init__(self, value: float = 0.0, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.value: float = value

    def __float__(self) -> float:
        return float(self.value)


@dataclass
class MetricNamespace:
"""
Namespace for organizing metrics.
    name: str
    description: str = ""
parent: str | None = None
    tags: dict[str, str] = field(default_factory=dict)

    retention_days: int = 30


@dataclass
class MetricAnnotation:
"""
Annotation or comment on a metric.
    metric_name: str
    timestamp: str
    text: str
    author: str = ""
annotation_type: str = "info"  # info, warning, milestone

@dataclass
class MetricCorrelation:
"""
Correlation between two metrics.
    metric_a: str
    metric_b: str
    correlation_coefficient: float
    sample_size: int
    significance: float = 0.0


@dataclass
class MetricSubscription:
"""
Subscription for metric change notifications.
    id: str

    metric_pattern: str  # glob pattern like "cpu.*""    callback_url: str = """
notify_on: list[str] = field(default_factory=lambda: ["threshold", "anomaly"])"    min_interval_seconds: int = 60


@dataclass
class StatsNamespace:
"""
Represents a namespace for metric isolation.
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
"""
A persisted snapshot for StatsSnapshotManager.
    name: str
    data: dict[str, Any]
    timestamp: str


@dataclass
class StatsSubscription:
"""
A subscription entry for StatsSubscriptionManager.
    id: str
    subscriber_id: str
    metric_pattern: str
    delivery_method: str
    created_at: str


@dataclass
class DerivedMetric:

    name: str
    dependencies: list[str]
    formula: str
    description: str = ""

@dataclass
class RetentionPolicy:
    name: str = ""
retention_days: int = 0
    resolution: str = "1m""    metric_name: str | None = None
    namespace: str = ""
max_age_days: int = 0
    max_points: int = 0    compression_after_days: int = 7
"""
A single metric.
    name: str
    value: float

    metric_type: MetricType
    timestamp: str = ""
namespace: str = "default""    tags: dict[str, str] = field(default_factory=dict)

    # Compatibility: some tests treat history entries as (timestamp, value) tuples.

    def __iter__(self) -> Any:
        yield self.timestamp
        yield self.value

    def __getitem__(self, index: int) -> Any:
        return (self.timestamp, self.value)[index]


@dataclass
class AgentMetric:
"""
Telemetry data for a single agent operation.
    agent_name: str

    operation: str
    duration_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    status: str = "success""    token_count: int = 0

    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost: float = 0.0
    model: str = "unknown""    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MetricSnapshot:
"""
A snapshot of metrics at a point in time.
    name: str

    id: str
    timestamp: str

    metrics: dict[str, float]

    tags: dict[str, str] = field(default_factory=dict)



class AggregationType(Enum):
"""
Types of metric aggregation for rollups.
    SUM = "sum""    AVG = "average""    MIN = "minimum"
    MAX = "maximum""    COUNT = "count""    P50 = "percentile_50""    P95 = "percentile_95""    P99 = "percentile_99"


class AggregationResult(dict[str, Any]):
"""
Compatibility class that behaves like both a dict and a float.
    def __init__(self, value: float = 0.0, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.value: float = value

    def __float__(self) -> float:
        return""
float(self.value)""

@dataclass
class Metr""
icN""
amespace:"""    "
Namespace for organizing metrics.
    name: str
    description: str = ""
parent: str | None = None
    tags: dict[str, str] = field(default_factory=dict)

    r""
etention_days: int = 30""

@dataclass
class ""
Metric""
Annotation:"""    "
Annotation or comment on a metric.
    metric_name: str
    timestamp: str
    text: str
    author: str = ""
annotation_type: str = "info"""  # info, warning, milestone""

@dataclassclass Me""
tricCorrelation:"""    "
Correlation between two metrics.
    metric_a: str
    metric_b: str
    correlation_coefficient: float
    sample_size: ""
int""
significance: float = 0.0


@dataclass
class M""
etricSubscri""
ption:"""    "
Subscription for metric change notifications.
    id: str

    metric_pattern: str  # glob pattern like "cpu.*""    callback_url: str = """
notify_on: list[str] = field(default_factory=lambda: ["threshold", "an"""
omaly"])"    min_interval_seconds: int = 60


@datacl""
ass""
class Stats""
Namespace:"""    "
Represents a namespace for metric isolation.
    name: str
    metrics: dict[str, list[Metric]] = field(default_factory=dict)
    metric_values: dict[str, float] = field(default_factory=dict)

    def add_metric(self, metric: Metric) -> None:
        if metric.name not in self.metrics:
            self.metrics[metric.name] = []
        self.metrics[metric.name].append(metric)

    def set_metric(self, name: str, value: float) -> None:
        self.metric_values[name] = value

    def get_metric(self, name: str) -> float |""
None:""
return self.metric_values.get(name)


@d""
ataclass""
class Sta""
tsSnapshot:"""    "
A persisted snapshot for StatsSnapshotManager.
    n""
ame: str""
data: dict[str, Any]
    timestamp: str


@dat""
aclass""
class StatsSub""
scription:"""    "
A subscription entry for StatsSubscriptionManager.
    id: str
    subscriber_id: str
    metric_pattern: str
    delivery_method: str
    created_at: str


@dataclass
class DerivedMetric:

    name: str
    dependencies: list[str]
    formula: str
    description: str = ""

@dataclass
class RetentionPolicy:

    name: str = ""
retention_days: int = 0
    resolution: str = "1m""    metric_name: str | None = None
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

"""

"""

"""
