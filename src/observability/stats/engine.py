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
"""
    def __init__(self) -> None:"""
        self.metrics_history: list[AgentMetric] = []

    def process_metric(self, metric: AgentMetric) -> None:
        """
        Add a new AgentMetric to the metrics history.

        Args:
            metric (AgentMetric): The metric instance to add.
        """
        self.metrics_history.append(metric)

    def summarize_performance(self) -> dict[str, Any]:
        """
        Summarize the performance metrics collected so far.

        Returns:
            dict[str, Any]: A dictionary containing total count, average duration, and total cost.
        """
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
        """
        Start a trace by recording the current time and initiating an OpenTelemetry span.

        Args:
            trace_id (str): Unique identifier for the trace.
        """
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
        """
        Complete a trace by recording its duration, cost, and metrics, and exporting telemetry data.

        Args:
            trace_id (str): Unique identifier for the trace.
            agent (str): Name of the agent performing the operation.
            op (str): Operation name.
            status (str, optional): Status of the operation. Defaults to "success".
            in_t (int, optional): Number of input tokens. Defaults to 0.
            out_t (int, optional): Number of output tokens. Defaults to 0.
            model (str, optional): Model name. Defaults to "unknown".
            metadata (dict[str, Any] | None, optional): Additional metadata. Defaults to None.
        """
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
        """
        Record a metric in the appropriate namespace, update rollup, query, and alert systems.

        Args:
            metric (Metric): The metric instance to record.
        """
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
        """
        Create and register a new StatsNamespace with the given name.

        Args:
            name (str): The name of the namespace to create.

        Returns:
            Any: The created StatsNamespace instance.
        """
        from .observability_core import StatsNamespace

        ns = StatsNamespace(name)
        self.namespaces[name] = ns
        return ns
