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
Phase 45: Prometheus Metrics Registry
vLLM-inspired prometheus integration with multiprocessing support.

Beyond vLLM:
- Multi-backend support (Prometheus, StatsD, OpenTelemetry)
- Automatic metric aggregation
- Custom histogram buckets
- Metric sampling for high-frequency counters
- Rate limiting for cardinality protection
"""

from __future__ import annotations

import contextlib
import os
import tempfile
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

# Try to import rust_core for acceleration
try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False
    rust_core = None


class MetricType(Enum):
    """Types of metrics."""

    COUNTER = auto()
    GAUGE = auto()
    HISTOGRAM = auto()
    SUMMARY = auto()


class MetricsBackend(Enum):
    """Metrics backend types."""

    PROMETHEUS = auto()
    STATSD = auto()
    OPENTELEMETRY = auto()
    NULL = auto()


@dataclass(frozen=True)
class MetricSpec:
    """Specification for a metric."""

    name: str
    description: str
    metric_type: MetricType
    labels: Tuple[str, ...] = ()
    buckets: Optional[Tuple[float, ...]] = None
    namespace: str = "pyagent"
    subsystem: str = ""

    @property
    def full_name(self) -> str:
        """Get full metric name with namespace."""
        parts = [self.namespace]
        if self.subsystem:
            parts.append(self.subsystem)
        parts.append(self.name)
        return "_".join(parts)


@dataclass
class MetricValue:
    """Container for metric value with labels."""

    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class MetricCollector(ABC):
    """Abstract base for metric collectors."""

    @abstractmethod
    def increment(self, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        """Increment a counter."""
        pass

    @abstractmethod
    def set(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Set a gauge value."""
        pass

    @abstractmethod
    def observe(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Observe a value for histogram/summary."""
        pass

    @abstractmethod
    def get(self, labels: Optional[Dict[str, str]] = None) -> float:
        """Get current value."""
        pass


class Counter(MetricCollector):
    """Thread-safe counter metric."""

    def __init__(self, spec: MetricSpec):
        self.spec = spec
        self._values: Dict[Tuple[Tuple[str, str], ...], float] = {}
        self._lock = threading.Lock()

    def _label_key(self, labels: Optional[Dict[str, str]]) -> Tuple[Tuple[str, str], ...]:
        if not labels:
            return ()
        return tuple(sorted(labels.items()))

    def increment(self, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._label_key(labels)
        with self._lock:
            self._values[key] = self._values.get(key, 0.0) + value

    def set(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        # Counters don't support set, only increment
        raise NotImplementedError("Counters only support increment")

    def observe(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        # For counters, observe is same as increment
        self.increment(value, labels)

    def get(self, labels: Optional[Dict[str, str]] = None) -> float:
        key = self._label_key(labels)
        with self._lock:
            return self._values.get(key, 0.0)

    def get_all(self) -> Dict[Tuple[Tuple[str, str], ...], float]:
        """Get all label combinations and values."""
        with self._lock:
            return dict(self._values)


class Gauge(MetricCollector):
    """Thread-safe gauge metric."""

    def __init__(self, spec: MetricSpec):
        self.spec = spec
        self._values: Dict[Tuple[Tuple[str, str], ...], float] = {}
        self._lock = threading.Lock()

    def _label_key(self, labels: Optional[Dict[str, str]]) -> Tuple[Tuple[str, str], ...]:
        if not labels:
            return ()
        return tuple(sorted(labels.items()))

    def increment(self, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._label_key(labels)
        with self._lock:
            self._values[key] = self._values.get(key, 0.0) + value

    def decrement(self, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        self.increment(-value, labels)

    def set(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._label_key(labels)
        with self._lock:
            self._values[key] = value

    def observe(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        self.set(value, labels)

    def get(self, labels: Optional[Dict[str, str]] = None) -> float:
        key = self._label_key(labels)
        with self._lock:
            return self._values.get(key, 0.0)

    def get_all(self) -> Dict[Tuple[Tuple[str, str], ...], float]:
        """Get all label combinations and values."""
        with self._lock:
            return dict(self._values)


@dataclass
class HistogramBucket:
    """Single histogram bucket."""

    upper_bound: float
    count: int = 0


class Histogram(MetricCollector):
    """Thread-safe histogram metric with configurable buckets."""

    DEFAULT_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, float("inf"))

    def __init__(self, spec: MetricSpec):
        self.spec = spec
        self._buckets = spec.buckets or self.DEFAULT_BUCKETS
        self._data: Dict[Tuple[Tuple[str, str], ...], Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def _label_key(self, labels: Optional[Dict[str, str]]) -> Tuple[Tuple[str, str], ...]:
        if not labels:
            return ()
        return tuple(sorted(labels.items()))

    def _get_or_create(self, key: Tuple[Tuple[str, str], ...]) -> Dict[str, Any]:
        if key not in self._data:
            self._data[key] = {
                "buckets": {b: 0 for b in self._buckets},
                "sum": 0.0,
                "count": 0,
            }
        return self._data[key]

    def increment(self, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        raise NotImplementedError("Histograms only support observe")

    def set(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        raise NotImplementedError("Histograms only support observe")

    def observe(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._label_key(labels)
        with self._lock:
            data = self._get_or_create(key)
            data["sum"] += value
            data["count"] += 1
            for bucket in self._buckets:
                if value <= bucket:
                    data["buckets"][bucket] += 1

    def get(self, labels: Optional[Dict[str, str]] = None) -> float:
        """Get the count."""
        key = self._label_key(labels)
        with self._lock:
            if key in self._data:
                return self._data[key]["count"]
            return 0.0

    def get_sum(self, labels: Optional[Dict[str, str]] = None) -> float:
        key = self._label_key(labels)
        with self._lock:
            if key in self._data:
                return self._data[key]["sum"]
            return 0.0

    def get_buckets(self, labels: Optional[Dict[str, str]] = None) -> Dict[float, int]:
        key = self._label_key(labels)
        with self._lock:
            if key in self._data:
                return dict(self._data[key]["buckets"])
            return {b: 0 for b in self._buckets}


class Summary(MetricCollector):
    """Thread-safe summary metric with quantiles."""

    DEFAULT_QUANTILES = (0.5, 0.9, 0.95, 0.99)

    def __init__(self, spec: MetricSpec, max_age_seconds: float = 60.0, max_samples: int = 1000):
        self.spec = spec
        self._max_age = max_age_seconds
        self._max_samples = max_samples
        self._data: Dict[Tuple[Tuple[str, str], ...], List[Tuple[float, float]]] = {}
        self._lock = threading.Lock()

    def _label_key(self, labels: Optional[Dict[str, str]]) -> Tuple[Tuple[str, str], ...]:
        if not labels:
            return ()
        return tuple(sorted(labels.items()))

    def _prune(self, samples: List[Tuple[float, float]], now: float) -> List[Tuple[float, float]]:
        cutoff = now - self._max_age
        pruned = [(t, v) for t, v in samples if t > cutoff]
        if len(pruned) > self._max_samples:
            pruned = pruned[-self._max_samples :]
        return pruned

    def increment(self, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        raise NotImplementedError("Summaries only support observe")

    def set(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        raise NotImplementedError("Summaries only support observe")

    def observe(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._label_key(labels)
        now = time.time()
        with self._lock:
            if key not in self._data:
                self._data[key] = []
            samples = self._data[key]
            samples.append((now, value))
            self._data[key] = self._prune(samples, now)

    def get(self, labels: Optional[Dict[str, str]] = None) -> float:
        """Get the count."""
        key = self._label_key(labels)
        now = time.time()
        with self._lock:
            if key in self._data:
                samples = self._prune(self._data[key], now)
                self._data[key] = samples
                return len(samples)
            return 0.0

    def get_quantile(self, quantile: float, labels: Optional[Dict[str, str]] = None) -> float:
        key = self._label_key(labels)
        now = time.time()
        with self._lock:
            if key not in self._data:
                return 0.0
            samples = self._prune(self._data[key], now)
            self._data[key] = samples
            if not samples:
                return 0.0
            values = sorted(v for _, v in samples)
            idx = int(len(values) * quantile)
            return values[min(idx, len(values) - 1)]


class MetricsRegistry:
    """
    Central registry for all metrics.

    Features:
    - Thread-safe metric registration
    - Multiprocessing support
    - Multiple backend support
    - Automatic cleanup
    """

    _instance: Optional["MetricsRegistry"] = None
    _lock = threading.Lock()

    def __init__(self, backend: MetricsBackend = MetricsBackend.PROMETHEUS):
        self._backend = backend
        self._metrics: Dict[str, MetricCollector] = {}
        self._metrics_lock = threading.Lock()
        self._multiproc_dir: Optional[tempfile.TemporaryDirectory] = None
        self._initialized = False

    @classmethod
    def get_instance(cls, backend: MetricsBackend = MetricsBackend.PROMETHEUS) -> "MetricsRegistry":
        """Get singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(backend)
        return cls._instance

    def setup_multiprocess(self) -> None:
        """Set up multiprocessing directory for prometheus."""
        if self._backend != MetricsBackend.PROMETHEUS:
            return

        if "PROMETHEUS_MULTIPROC_DIR" not in os.environ:
            self._multiproc_dir = tempfile.TemporaryDirectory()
            os.environ["PROMETHEUS_MULTIPROC_DIR"] = self._multiproc_dir.name

        self._initialized = True

    def register(self, spec: MetricSpec) -> MetricCollector:
        """Register a new metric."""
        with self._metrics_lock:
            if spec.full_name in self._metrics:
                return self._metrics[spec.full_name]

            if spec.metric_type == MetricType.COUNTER:
                collector = Counter(spec)
            elif spec.metric_type == MetricType.GAUGE:
                collector = Gauge(spec)
            elif spec.metric_type == MetricType.HISTOGRAM:
                collector = Histogram(spec)
            elif spec.metric_type == MetricType.SUMMARY:
                collector = Summary(spec)
            else:
                raise ValueError(f"Unknown metric type: {spec.metric_type}")

            self._metrics[spec.full_name] = collector
            return collector

    def get(self, name: str) -> Optional[MetricCollector]:
        """Get a registered metric."""
        with self._metrics_lock:
            return self._metrics.get(name)

    def counter(
        self,
        name: str,
        description: str = "",
        labels: Tuple[str, ...] = (),
        namespace: str = "pyagent",
        subsystem: str = "",
    ) -> Counter:
        """Create or get a counter metric."""
        spec = MetricSpec(
            name=name,
            description=description,
            metric_type=MetricType.COUNTER,
            labels=labels,
            namespace=namespace,
            subsystem=subsystem,
        )
        return self.register(spec)  # type: ignore

    def gauge(
        self,
        name: str,
        description: str = "",
        labels: Tuple[str, ...] = (),
        namespace: str = "pyagent",
        subsystem: str = "",
    ) -> Gauge:
        """Create or get a gauge metric."""
        spec = MetricSpec(
            name=name,
            description=description,
            metric_type=MetricType.GAUGE,
            labels=labels,
            namespace=namespace,
            subsystem=subsystem,
        )
        return self.register(spec)  # type: ignore

    def histogram(
        self,
        name: str,
        description: str = "",
        labels: Tuple[str, ...] = (),
        buckets: Optional[Tuple[float, ...]] = None,
        namespace: str = "pyagent",
        subsystem: str = "",
    ) -> Histogram:
        """Create or get a histogram metric."""
        spec = MetricSpec(
            name=name,
            description=description,
            metric_type=MetricType.HISTOGRAM,
            labels=labels,
            buckets=buckets,
            namespace=namespace,
            subsystem=subsystem,
        )
        return self.register(spec)  # type: ignore

    def summary(
        self,
        name: str,
        description: str = "",
        labels: Tuple[str, ...] = (),
        namespace: str = "pyagent",
        subsystem: str = "",
    ) -> Summary:
        """Create or get a summary metric."""
        spec = MetricSpec(
            name=name,
            description=description,
            metric_type=MetricType.SUMMARY,
            labels=labels,
            namespace=namespace,
            subsystem=subsystem,
        )
        return self.register(spec)  # type: ignore

    def collect_all(self) -> Dict[str, Any]:
        """Collect all metric values."""
        result = {}
        with self._metrics_lock:
            for name, collector in self._metrics.items():
                if isinstance(collector, Counter):
                    result[name] = {
                        "type": "counter",
                        "values": collector.get_all(),
                    }
                elif isinstance(collector, Gauge):
                    result[name] = {
                        "type": "gauge",
                        "values": collector.get_all(),
                    }
                elif isinstance(collector, Histogram):
                    result[name] = {
                        "type": "histogram",
                        "sum": collector.get_sum(),
                        "count": collector.get(),
                        "buckets": collector.get_buckets(),
                    }
                elif isinstance(collector, Summary):
                    result[name] = {
                        "type": "summary",
                        "count": collector.get(),
                        "quantiles": {q: collector.get_quantile(q) for q in Summary.DEFAULT_QUANTILES},
                    }
        return result

    def reset(self) -> None:
        """Reset all metrics."""
        with self._metrics_lock:
            self._metrics.clear()

    def shutdown(self) -> None:
        """Shutdown and cleanup."""
        self.reset()
        if self._multiproc_dir:
            with contextlib.suppress(Exception):
                self._multiproc_dir.cleanup()
            self._multiproc_dir = None


class SampledCounter(Counter):
    """
    Counter with sampling for high-frequency operations.

    Beyond vLLM: Rate-limited counter to prevent cardinality explosion.
    """

    def __init__(self, spec: MetricSpec, sample_rate: float = 0.1):
        super().__init__(spec)
        self._sample_rate = sample_rate
        self._sample_counter = 0
        self._sample_lock = threading.Lock()

    def increment(self, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        with self._sample_lock:
            self._sample_counter += 1
            if self._sample_counter % int(1 / self._sample_rate) == 0:
                super().increment(value / self._sample_rate, labels)


class RateLimitedGauge(Gauge):
    """
    Gauge with rate limiting for updates.

    Beyond vLLM: Prevents excessive updates in hot paths.
    """

    def __init__(self, spec: MetricSpec, min_interval: float = 0.1):
        super().__init__(spec)
        self._min_interval = min_interval
        self._last_update: Dict[Tuple[Tuple[str, str], ...], float] = {}
        self._rate_lock = threading.Lock()

    def set(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._label_key(labels)
        now = time.time()

        with self._rate_lock:
            last = self._last_update.get(key, 0)
            if now - last >= self._min_interval:
                super().set(value, labels)
                self._last_update[key] = now


# Pre-defined vLLM-compatible metrics
class VLLMMetrics:
    """Collection of vLLM-compatible metrics."""

    def __init__(self, registry: Optional[MetricsRegistry] = None):
        self.registry = registry or MetricsRegistry.get_instance()

        # Request metrics
        self.num_requests_running = self.registry.gauge(
            "num_requests_running",
            "Number of requests currently being processed",
            subsystem="engine",
        )
        self.num_requests_waiting = self.registry.gauge(
            "num_requests_waiting",
            "Number of requests waiting in queue",
            subsystem="engine",
        )

        # Token metrics
        self.num_prompt_tokens = self.registry.counter(
            "num_prompt_tokens_total",
            "Total number of prompt tokens processed",
            subsystem="engine",
        )
        self.num_generation_tokens = self.registry.counter(
            "num_generation_tokens_total",
            "Total number of generation tokens produced",
            subsystem="engine",
        )

        # Latency metrics
        self.request_latency = self.registry.histogram(
            "request_latency_seconds",
            "Request end-to-end latency",
            subsystem="engine",
            buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, float("inf")),
        )
        self.time_to_first_token = self.registry.histogram(
            "time_to_first_token_seconds",
            "Time to first token latency",
            subsystem="engine",
            buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, float("inf")),
        )
        self.inter_token_latency = self.registry.histogram(
            "inter_token_latency_seconds",
            "Inter-token latency",
            subsystem="engine",
            buckets=(0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, float("inf")),
        )

        # Cache metrics
        self.cache_hit_rate = self.registry.gauge(
            "cache_hit_rate",
            "Prefix cache hit rate",
            subsystem="cache",
        )
        self.kv_cache_usage = self.registry.gauge(
            "kv_cache_usage",
            "KV cache usage fraction",
            subsystem="cache",
        )

        # GPU metrics
        self.gpu_memory_used = self.registry.gauge(
            "gpu_memory_used_bytes",
            "GPU memory used in bytes",
            labels=("device",),
            subsystem="gpu",
        )

        # Speculative decoding metrics
        self.spec_decode_acceptance_rate = self.registry.gauge(
            "spec_decode_acceptance_rate",
            "Speculative decoding acceptance rate",
            subsystem="spec_decode",
        )
        self.spec_decode_num_accepted = self.registry.counter(
            "spec_decode_num_accepted_total",
            "Total number of accepted speculative tokens",
            subsystem="spec_decode",
        )
        self.spec_decode_num_drafted = self.registry.counter(
            "spec_decode_num_drafted_total",
            "Total number of drafted speculative tokens",
            subsystem="spec_decode",
        )


# Singleton instance
_metrics: Optional[VLLMMetrics] = None


def get_metrics() -> VLLMMetrics:
    """Get the global VLLMMetrics instance."""
    global _metrics
    if _metrics is None:
        _metrics = VLLMMetrics()
    return _metrics


__all__ = [
    "MetricType",
    "MetricsBackend",
    "MetricSpec",
    "MetricValue",
    "MetricCollector",
    "Counter",
    "Gauge",
    "Histogram",
    "Summary",
    "MetricsRegistry",
    "SampledCounter",
    "RateLimitedGauge",
    "VLLMMetrics",
    "get_metrics",
]
