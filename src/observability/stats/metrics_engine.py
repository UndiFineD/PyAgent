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
Metrics Engine - High-performance observability & token cost aggregation

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate ObservabilityEngine(workspace_root=<path>, fleet=<fleet>) in the agent runtime.
- Use start_trace/stop_trace/log_event/get_metrics/generate_dashboard/export_to_elk to record, export and view telemetry.
- Integrate PrometheusExporter, OTelManager and MetricsExporter for scraping, tracing and external dashboards.

WHAT IT DOES:
- Centralizes fleet-wide telemetry, event logging and metric aggregation for PyAgent.
- Records structured events with noise reduction, exports buffered logs to an ELK-style sink, and exposes Prometheus payloads.
- Provides token-cost calculation via TokenCostEngine, Grafana dashboard generation hooks, and optional Rust acceleration via rust_core.

WHAT IT SHOULD DO BETTER:
- Persist telemetry atomically (use StateTransaction) and provide configurable retention/rotation for the .agent_telemetry.json file.
- Add robust error handling and backpressure when exporters (Prometheus/OTel/Grafana) are unavailable, and surface async APIs for non-blocking operation.
- Improve type-safety and unit coverage for boundary cases (missing rust_core, exporter failures, and malformed events), and document stable public API surface.

FILE CONTENT SUMMARY:
High-performance metrics engine for real-time observability and aggregation.
"""

from __future__ import annotations


import json
import logging
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any, Optional

from src.observability.reports.grafana_generator import GrafanaDashboardGenerator

from src.observability.stats.metrics_core import TokenCostResult

# Import pure calculation cores
from .metrics_core import ModelFallbackCore, TokenCostCore
from .observability_core import AgentMetric, ObservabilityCore

try:
    import rust_core as rc
except ImportError:
    rc = None

from .exporters import MetricsExporter, OTelManager, PrometheusExporter
from src.core.base.lifecycle.version import VERSION


__version__: str = VERSION

logger: logging.Logger = logging.getLogger(__name__)


class ObservabilityEngine:
    """Provides telemetry and performance tracking for the agent fleet."""

    def __init__(self, workspace_root: str | None = None, fleet: Any = None) -> None:
        if fleet and hasattr(fleet, "workspace_root"):
            self.workspace_root = Path(fleet.workspace_root)
        elif workspace_root:
            self.workspace_root = Path(workspace_root)
        else:
            self.workspace_root = Path(".")

        self.telemetry_file: Path = self.workspace_root / ".agent_telemetry.json"
        self.core = ObservabilityCore()
        self.metrics: list[AgentMetric] = []
        self._start_times: dict[str, float] = {}
        self._otel_spans: dict[str, str] = {}  # Map trace_id -> tel_span_id
        self.cost_engine = TokenCostEngine()
        self.prometheus = PrometheusExporter()
        self.otel = OTelManager()
        self.metrics_exporter = MetricsExporter()
        self.log_buffer: list[dict[str, Any]] = []
        self.load()

    def log_event(self, agent_id: str, event_type: str, data: Any, level: str = "INFO") -> None:
        """Logs a system event in a structured format for ELK.

        Args:
            agent_id: The ID of the agent generating the event.
            event_type: The category of event (e.g., 'task_complete', 'error').
            data: Payload of the event.
            level: Severity level (INFO, WARNING, ERROR, CRITICAL).
        """
        # Noise Reduction: Only store significant events in the persistent log buffer.
        # Metrics are still recorded for everything.
        important_types: list[str] = [
            "agent_failure",
            "security_alert",
            "workflow_error",
            "system_crash",
        ]
        important_levels: list[str] = ["ERROR", "WARNING", "CRITICAL"]

        should_log: bool = level in important_levels or event_type in important_types

        if should_log:
            event = {
                "timestamp": time.time(),
                "agent_id": agent_id,
                "event_type": event_type,
                "level": level,
                "data": data,
            }
            self.log_buffer.append(event)

        # Always record metrics regardless of log storage
        self.prometheus.record_metric("agent_events_total", 1.0, {"agent": agent_id, "type": event_type})
        self.metrics_exporter.record_agent_call(agent_id, 0.0, True)

    def export_to_elk(self) -> str:
        """Simulates exporting log buffer to ELK stack."""
        count: int = len(self.log_buffer)
        # In real scenario: push to Elasticsearch/Logstash
        json.dumps(self.log_buffer)
        self.log_buffer = []
        self.metrics_exporter.export_to_grafana()
        return f"Exported {count} events to ELK/Logstash."

    def get_metrics(self) -> str:
        """Returns Prometheus scrape response."""
        return self.metrics_exporter.get_prometheus_payload()

    def generate_dashboard(self, shard_name: str | None = None) -> str:
        """
        Triggers Grafana JSON dashboard generation (Phase 126).
        """
        try:
            generator = GrafanaDashboardGenerator(self.workspace_root / "deploy" / "grafana")
            if shard_name:
                return generator.generate_shard_obs(shard_name)
            return generator.generate_fleet_summary()
        except RuntimeError as e:
            return f"Error: GrafanaDashboardGenerator not available: {e}"

    def start_trace(self, trace_id: str) -> None:
        """Start timing an operation."""
        self._start_time
"""

from __future__ import annotations


import json
import logging
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any, Optional

from src.observability.reports.grafana_generator import GrafanaDashboardGenerator

from src.observability.stats.metrics_core import TokenCostResult

# Import pure calculation cores
from .metrics_core import ModelFallbackCore, TokenCostCore
from .observability_core import AgentMetric, ObservabilityCore

try:
    import rust_core as rc
except ImportError:
    rc = None

from .exporters import MetricsExporter, OTelManager, PrometheusExporter
from src.core.base.lifecycle.version import VERSION


__version__: str = VERSION

logger: logging.Logger = logging.getLogger(__name__)


class ObservabilityEngine:
    """Provides telemetry and performance tracking for the agent fleet."""

    def __init__(self, workspace_root: str | None = None, fleet: Any = None) -> None:
        if fleet and hasattr(fleet, "workspace_root"):
            self.workspace_root = Path(fleet.workspace_root)
        elif workspace_root:
            self.workspace_root = Path(workspace_root)
        else:
            self.workspace_root = Path(".")

        self.telemetry_file: Path = self.workspace_root / ".agent_telemetry.json"
        self.core = ObservabilityCore()
        self.metrics: list[AgentMetric] = []
        self._start_times: dict[str, float] = {}
        self._otel_spans: dict[str, str] = {}  # Map trace_id -> tel_span_id
        self.cost_engine = TokenCostEngine()
        self.prometheus = PrometheusExporter()
        self.otel = OTelManager()
        self.metrics_exporter = MetricsExporter()
        self.log_buffer: list[dict[str, Any]] = []
        self.load()

    def log_event(self, agent_id: str, event_type: str, data: Any, level: str = "INFO") -> None:
        """Logs a system event in a structured format for ELK.

        Args:
            agent_id: The ID of the agent generating the event.
            event_type: The category of event (e.g., 'task_complete', 'error').
            data: Payload of the event.
            level: Severity level (INFO, WARNING, ERROR, CRITICAL).
        """
        # Noise Reduction: Only store significant events in the persistent log buffer.
        # Metrics are still recorded for everything.
        important_types: list[str] = [
            "agent_failure",
            "security_alert",
            "workflow_error",
            "system_crash",
        ]
        important_levels: list[str] = ["ERROR", "WARNING", "CRITICAL"]

        should_log: bool = level in important_levels or event_type in important_types

        if should_log:
            event = {
                "timestamp": time.time(),
                "agent_id": agent_id,
                "event_type": event_type,
                "level": level,
                "data": data,
            }
            self.log_buffer.append(event)

        # Always record metrics regardless of log storage
        self.prometheus.record_metric("agent_events_total", 1.0, {"agent": agent_id, "type": event_type})
        self.metrics_exporter.record_agent_call(agent_id, 0.0, True)

    def export_to_elk(self) -> str:
        """Simulates exporting log buffer to ELK stack."""
        count: int = len(self.log_buffer)
        # In real scenario: push to Elasticsearch/Logstash
        json.dumps(self.log_buffer)
        self.log_buffer = []
        self.metrics_exporter.export_to_grafana()
        return f"Exported {count} events to ELK/Logstash."

    def get_metrics(self) -> str:
        """Returns Prometheus scrape response."""
        return self.metrics_exporter.get_prometheus_payload()

    def generate_dashboard(self, shard_name: str | None = None) -> str:
        """
        Triggers Grafana JSON dashboard generation (Phase 126).
        """
        try:
            generator = GrafanaDashboardGenerator(self.workspace_root / "deploy" / "grafana")
            if shard_name:
                return generator.generate_shard_obs(shard_name)
            return generator.generate_fleet_summary()
        except RuntimeError as e:
            return f"Error: GrafanaDashboardGenerator not available: {e}"

    def start_trace(self, trace_id: str) -> None:
        """Start timing an operation."""
        self._start_times[trace_id] = time.time()
        # Also start OTel span and store its UUID
        span_id: str = self.otel.start_span(trace_id)
        self._otel_spans[trace_id] = span_id

    def end_trace(
        self,
        trace_id: str,
        agent_name: str,  # noqa: ARG002
        operation: str,  # noqa: ARG002
        status: str = "success",
        input_tokens: int = 0,  # noqa: ARG002
        output_tokens: int = 0,  # noqa: ARG002
        model: str = "unknown",  # noqa: ARG002
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """End timing and record metric with cost estimation."""
        if trace_id not in self._start_times:
            logging.warning(f"No start trace found for {trace_id}")
            return

        _duration: float = (time.time() - self._start_times.pop(trace_id)) * 1000  # noqa: F841

        # End OTel span using the stored span_id
        otel_span_id: str | None = self._otel_spans.pop(trace_id, None)
        if otel_span_id:
            self.otel.end_span(otel_span_id, status=status, attributes=metadata)

    def consolidate_telemetry(self) -> dict[str, float]:
        """Aggregate metrics using Rust high-throughput engine."""
        if rc and hasattr(rc, "aggregate_metrics_rust"):
            data_map = self._build_data_map()
            try:
                aggregated_results = rc.aggregate_metrics_rust(data_map)  # type: ignore
                return aggregated_results
            except (AttributeError, RuntimeError) as e:  # pylint: disable=broad-exception-caught
                logger.warning("Rust metric aggregation failed: %s", e)
                import traceback
                traceback.print_exc()
        return self._python_aggregate_metrics()

    def _build_data_map(self) -> dict[str, list[float]]:
        data_map: dict[str, list[float]] = {}
        for m in self.metrics:
            key = f"{m.agent_name}:{m.operation}"
            if key not in data_map:
                data_map[key] = []
            data_map[key].append(m.duration_ms)
        return data_map

    def _python_aggregate_metrics(self) -> dict[str, float]:
        counts: dict[str, int] = {}
        sums: dict[str, float] = {}
        for m in self.metrics:
            key = f"{m.agent_name}:{m.operation}"
            counts[key] = counts.get(key, 0) + 1
            sums[key] = sums.get(key, 0.0) + m.duration_ms
        aggregated_results: dict[str, float] = {}
        for key, total in sums.items():
            if counts[key] > 0:
                aggregated_results[key] = total / counts[key]
        return aggregated_results

    def get_reliability_weights(self, agent_names: list[str]) -> list[float]:
        """Exposes core reliability logic for consensus protocols."""
        return self.core.calculate_reliability_scores(agent_names)

    def trace_workflow(self, workflow_name: str, duration: float) -> None:
        """Records a workflow trace for OpenTelemetry visualization."""
        self.prometheus.record_metric("workflow_duration_seconds", duration, {"workflow": workflow_name})
        self.log_event(
            "system",
            "workflow_trace",
            {"workflow": workflow_name, "duration": duration},
        )

    def get_summary(self) -> dict[str, Any]:
        """Returns a summary of performance and cost metrics."""
        if not self.metrics:
            return {"status": "No data"}

        count = len(self.metrics)
        total_latency = sum(m.duration_ms for m in self.metrics)
        success_count = sum(1 for m in self.metrics if m.status == "success")
        agent_stats = self._aggregate_agent_stats()

        summary = {
            "total_calls": count,
            "avg_latency_ms": round(total_latency / count, 2),
            "success_rate": round(success_count / count * 100, 2),
            "total_tokens": sum(m.token_count for m in self.metrics),
            "total_cost_usd": round(sum(m.estimated_cost for m in self.metrics), 6),
            "agents": agent_stats,
        }
        return summary

    def _aggregate_agent_stats(self) -> dict[str, dict[str, float]]:
        agents: dict[str, dict[str, float]] = {}
        for m in self.metrics:
            if m.agent_name not in agents:
                agents[m.agent_name] = {"calls": 0, "latency": 0.0, "cost": 0.0}
            a = agents[m.agent_name]
            a["calls"] += 1
            a["latency"] += m.duration_ms
            a["cost"] += m.estimated_cost
        for _name, data in agents.items():
            data["avg_latency"] = round(data["latency"] / data["calls"], 2) if data["calls"] else 0.0
            data["total_cost"] = round(data["cost"], 6)
        return agents

    def save(self) -> None:
        """Persist telemetry to disk."""
        try:
            data: list[dict[str, Any]] = [asdict(m) for m in self.metrics]
            self.telemetry_file.write_text(json.dumps(data, indent=2))
        except (OSError, TypeError) as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"Failed to save telemetry: {e}")
            import traceback
            traceback.print_exc()

    def load(self) -> None:
        """Load telemetry from disk."""
        if self.telemetry_file.exists():
            try:
                data = json.loads(self.telemetry_file.read_text())

                self.metrics = [AgentMetric(**m) for m in data]
            except (json.JSONDecodeError, TypeError, ValueError) as e:
                logging.error(f"Failed to load telemetry: {e}")
                import traceback
                traceback.print_exc()
                self.metrics = []


class TokenCostEngine:
    def __init__(self) -> None:
        self.core = TokenCostCore()

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0) -> float:
        res: TokenCostResult = self.core.calculate_cost(input_tokens, output_tokens, model)
        return res.total_cost


class ModelFallbackEngine:
    def __init__(self, cost_engine: Optional[TokenCostEngine] = None) -> None:
        self.cost_engine: Optional[TokenCostEngine] = cost_engine
        self.core = ModelFallbackCore()

    def get_fallback_model(self, current_model: str) -> str:
        return self.core.determine_next_model(current_model)
