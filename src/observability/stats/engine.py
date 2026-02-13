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
Engine.py - Observability & Stats Engine

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate ObservabilityEngine(workspace_root: str | None) to collect agent telemetry.
- Call start_trace(trace_id) before an operation and end_trace(trace_id, agent, op, status, in_t, out_t, model, metadata) after to record metrics, cost and export to configured backends.
- Use StatsCore.record(metric) to register numeric metrics for rollups, queries and threshold alerts; use StatsNamespaceManager.create(name) for per-namespace objects.

WHAT IT DOES:
- Provides an ObservabilityEngine that manages trace lifecycle, spans (OTel), token-cost estimation, and metric exporting (Prometheus/OTel/custom MetricsExporter).
- Implements ObservabilityCore for pure in-memory telemetry aggregation and summary computations.
- Implements StatsCore for metric namespace management, rollup calculation, query indexing and threshold alert checking; exposes a backward-compatible namespace manager.

WHAT IT SHOULD DO BETTER:
- Persist telemetry and rollups to durable storage and support configurable batching to reduce I/O and improve resilience.
- Provide async APIs (asyncio) for non-blocking exporters and integrate transactional StateTransaction for safe FS modifications per project conventions.
- Add robust error handling and retries around exporter/network operations, stronger typing for metadata, and unit tests for cost calculations and alerting logic.

FILE CONTENT SUMMARY:
Engine.py module.
"""
# Observability and statistics engines/orchestrators.

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

from .alerting import ThresholdAlertManager
from .analysis import TokenCostEngine
from .exporters.metrics_exporter import MetricsExporter
from .exporters.otel_manager import OTelManager
from .exporters.prometheus_exporter import PrometheusExporter
from .metrics import AgentMetric, Metric
from .rollup_engine import StatsQueryEngine, StatsRollupCalculator

logger = logging.getLogger(__name__)


class ObservabilityCore:
    """Pure logic for processing agent telemetry data."""

    def __init__(self) -> None:
        self.metrics_history: list[AgentMetric] = []

    def process_metric(self, metric: AgentMetric) -> None:
        self.metrics_history.append(metric)

    def summarize_performance() -> dict[str, Any]:
        if not self.metrics_history:
            return {"count": 0, "avg_duration": 0, "total_cost": 0}

        total_d = sum(m.duration_ms for m in self.metrics_history)
        total_c = sum(m.estimated_cost for m in self.metrics_history)
        count = len(self.metrics_history)
        return {
            "total_count": count,
            "avg_duration_ms": total_d / count,
            "total_cost_usd": round(total_c, 6),
        }


class ObservabilityEngine:
    """Provides telemetry and performance tracking for the agent fleet."""

    def __init__(self, workspace_root: str | None = None) -> None:
        self.workspace_root = Path(workspace_root or ".")
        self.telemetry_file = self.workspace_root / ".agent_telemetry.json"
        self.core = ObservabilityCore()
        self.cost_engine = TokenCostEngine()
        self.prometheus = PrometheusExporter()
        self.otel = OTelManager()

        self.metrics_exporter = MetricsExporter()
        self._start_times: dict[str, float] = {}
        self._otel_spans: dict[str, str] = {}

    def start_trace(self, trace_id: str) -> None:
        self._start_times[trace_id] = time.time()
        self._otel_spans[trace_id] = self.otel.start_span(trace_id)

    def end_trace(
        self,
        trace_id: str,
        agent: str,
        op: str,
        status: str = "success",
        in_t: int = 0,
        out_t: int = 0,
        model: str = "unknown",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if trace_id not in self._start_times:
            return
        duration = (time.time() - self._start_times.pop(trace_id)) * 1000

        span_id = self._otel_spans.pop(trace_id, None)
        if span_id:
            self.otel.end_span(span_id, status=status, attributes=metadata)

        cost = self.cost_engine.calculate_cost(model, in_t, out_t)
        metric = AgentMetric(
            agent_name=agent,
            operation=op,
            duration_ms=duration,
            status=status,
            input_tokens=in_t,
            output_tokens=out_t,
            estimated_cost=cost,
            model=model,
            metadata=metadata or {},
        )

        self.core.process_metric(metric)
        self.metrics_exporter.record_agent_call(agent, duration, status == "success")


class StatsCore:
    """Core logic for statistics processing."""

    def __init__(self) -> None:
        self.namespaces: dict[str, list[Metric]] = {}
        self.rollup = StatsRollupCalculator()
        self.query = StatsQueryEngine()
        self.alerts = ThresholdAlertManager()

    def record(self, metric: Metric) -> None:
        ns = metric.namespace
        if ns not in self.namespaces:
            self.namespaces[ns] = []
        self.namespaces[ns].append(metric)
        self.rollup.add_point(metric.name, time.time(), metric.value)
        self.query.add_metric(metric.name, metric)
        self.alerts.check(metric.name, metric.value)


class StatsNamespaceManager:
    """Manages multiple namespaces (backward compat)."""

    def __init__(self) -> None:
        self.namespaces: dict[str, Any] = {}

    def create(self, name: str) -> Any:
        from .observability_core import StatsNamespace

        ns = StatsNamespace(name)
        self.namespaces[name] = ns
        return ns
"""
# Observability and statistics engines/orchestrators.

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

from .alerting import ThresholdAlertManager
from .analysis import TokenCostEngine
from .exporters.metrics_exporter import MetricsExporter
from .exporters.otel_manager import OTelManager
from .exporters.prometheus_exporter import PrometheusExporter
from .metrics import AgentMetric, Metric
from .rollup_engine import StatsQueryEngine, StatsRollupCalculator

logger = logging.getLogger(__name__)


class ObservabilityCore:
    """Pure logic for processing agent telemetry data."""

    def __init__(self) -> None:
        self.metrics_history: list[AgentMetric] = []

    def process_metric(self, metric: AgentMetric) -> None:
        self.metrics_history.append(metric)

    def summarize_performance(self) -> dict[str, Any]:
        if not self.metrics_history:
            return {"count": 0, "avg_duration": 0, "total_cost": 0}

        total_d = sum(m.duration_ms for m in self.metrics_history)
        total_c = sum(m.estimated_cost for m in self.metrics_history)
        count = len(self.metrics_history)
        return {
            "total_count": count,
            "avg_duration_ms": total_d / count,
            "total_cost_usd": round(total_c, 6),
        }


class ObservabilityEngine:
    """Provides telemetry and performance tracking for the agent fleet."""

    def __init__(self, workspace_root: str | None = None) -> None:
        self.workspace_root = Path(workspace_root or ".")
        self.telemetry_file = self.workspace_root / ".agent_telemetry.json"
        self.core = ObservabilityCore()
        self.cost_engine = TokenCostEngine()
        self.prometheus = PrometheusExporter()
        self.otel = OTelManager()

        self.metrics_exporter = MetricsExporter()
        self._start_times: dict[str, float] = {}
        self._otel_spans: dict[str, str] = {}

    def start_trace(self, trace_id: str) -> None:
        self._start_times[trace_id] = time.time()
        self._otel_spans[trace_id] = self.otel.start_span(trace_id)

    def end_trace(
        self,
        trace_id: str,
        agent: str,
        op: str,
        status: str = "success",
        in_t: int = 0,
        out_t: int = 0,
        model: str = "unknown",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if trace_id not in self._start_times:
            return
        duration = (time.time() - self._start_times.pop(trace_id)) * 1000

        span_id = self._otel_spans.pop(trace_id, None)
        if span_id:
            self.otel.end_span(span_id, status=status, attributes=metadata)

        cost = self.cost_engine.calculate_cost(model, in_t, out_t)
        metric = AgentMetric(
            agent_name=agent,
            operation=op,
            duration_ms=duration,
            status=status,
            input_tokens=in_t,
            output_tokens=out_t,
            estimated_cost=cost,
            model=model,
            metadata=metadata or {},
        )

        self.core.process_metric(metric)
        self.metrics_exporter.record_agent_call(agent, duration, status == "success")


class StatsCore:
    """Core logic for statistics processing."""

    def __init__(self) -> None:
        self.namespaces: dict[str, list[Metric]] = {}
        self.rollup = StatsRollupCalculator()
        self.query = StatsQueryEngine()
        self.alerts = ThresholdAlertManager()

    def record(self, metric: Metric) -> None:
        ns = metric.namespace
        if ns not in self.namespaces:
            self.namespaces[ns] = []
        self.namespaces[ns].append(metric)
        self.rollup.add_point(metric.name, time.time(), metric.value)
        self.query.add_metric(metric.name, metric)
        self.alerts.check(metric.name, metric.value)


class StatsNamespaceManager:
    """Manages multiple namespaces (backward compat)."""

    def __init__(self) -> None:
        self.namespaces: dict[str, Any] = {}

    def create(self, name: str) -> Any:
        from .observability_core import StatsNamespace

        ns = StatsNamespace(name)
        self.namespaces[name] = ns
        return ns
