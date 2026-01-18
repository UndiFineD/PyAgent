#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Unified logic for metric calculation, processing, and management.

from __future__ import annotations
import json
import logging
import time
from dataclasses import asdict
from typing import Any
from pathlib import Path
from .ObservabilityCore import (
    AgentMetric,
    ObservabilityCore,
)

# Import pure calculation cores
from .MetricsCore import (
    TokenCostCore,
    ModelFallbackCore,
)

try:
    import psutil
except ImportError:

    psutil = None
from .exporters import PrometheusExporter, OTelManager, MetricsExporter

try:
    from src.observability.reports.GrafanaGenerator import (
        GrafanaDashboardGenerator as GrafanaGenerator,
    )
except ImportError:
    GrafanaGenerator = None
from src.core.base.Version import VERSION

__version__ = VERSION

logger = logging.getLogger(__name__)


class ObservabilityEngine:
    """Provides telemetry and performance tracking for the agent fleet."""

    def __init__(self, workspace_root: str = None, fleet: Any = None) -> None:
        if fleet and hasattr(fleet, "workspace_root"):
            self.workspace_root = Path(fleet.workspace_root)
        elif workspace_root:
            self.workspace_root = Path(workspace_root)
        else:
            self.workspace_root = Path(".")

        self.telemetry_file = self.workspace_root / ".agent_telemetry.json"
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

    def log_event(
        self, agent_id: str, event_type: str, data: Any, level: str = "INFO"
    ) -> None:
        """Logs a system event in a structured format for ELK.

        Args:
            agent_id: The ID of the agent generating the event.
            event_type: The category of event (e.g., 'task_complete', 'error').
            data: Payload of the event.
            level: Severity level (INFO, WARNING, ERROR, CRITICAL).
        """
        # Noise Reduction: Only store significant events in the persistent log buffer.
        # Metrics are still recorded for everything.
        important_types = [
            "agent_failure",
            "security_alert",
            "workflow_error",
            "system_crash",
        ]
        important_levels = ["ERROR", "WARNING", "CRITICAL"]

        should_log = level in important_levels or event_type in important_types

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
        self.prometheus.record_metric(
            "agent_events_total", 1.0, {"agent": agent_id, "type": event_type}
        )
        self.metrics_exporter.record_agent_call(agent_id, 0.0, True)

    def export_to_elk(self) -> str:
        """Simulates exporting log buffer to ELK stack."""
        count = len(self.log_buffer)
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
        if GrafanaGenerator:
            generator = GrafanaGenerator(self.workspace_root / "deploy" / "grafana")
            if shard_name:
                return generator.generate_shard_obs(shard_name)
            return generator.generate_fleet_summary()
        return "Error: GrafanaGenerator not available."

    def start_trace(self, trace_id: str) -> None:
        """Start timing an operation."""
        self._start_times[trace_id] = time.time()
        # Also start OTel span and store its UUID
        span_id = self.otel.start_span(trace_id)
        self._otel_spans[trace_id] = span_id

    def end_trace(
        self,
        trace_id: str,
        agent_name: str,
        operation: str,
        status: str = "success",
        input_tokens: int = 0,
        output_tokens: int = 0,
        model: str = "unknown",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """End timing and record metric with cost estimation."""
        if trace_id not in self._start_times:
            logging.warning(f"No start trace found for {trace_id}")
            return

        duration = (time.time() - self._start_times.pop(trace_id)) * 1000

        # End OTel span using the stored span_id
        otel_span_id = self._otel_spans.pop(trace_id, None)
        if otel_span_id:
            self.otel.end_span(otel_span_id, status=status, attributes=metadata)

        # Calculate cost
        cost = self.cost_engine.calculate_cost(model, input_tokens, output_tokens)

        metric = AgentMetric(
            agent_name=agent_name,
            operation=operation,
            duration_ms=duration,
            status=status,
            token_count=input_tokens + output_tokens,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=cost,
            model=model,
            metadata=metadata or {},
        )

        self.core.process_metric(metric)
        self.metrics.append(metric)  # Redundant but kept for display

        # External exporters
        self.prometheus.record_metric(
            "agent_duration_ms", duration, {"agent": agent_name, "op": operation}
        )
        self.metrics_exporter.record_agent_call(
            agent_name, duration, status == "success"
        )

        if len(self.metrics) > 1000:
            self.save()
            self.metrics = self.metrics[-500:]  # Prune memory

    def get_reliability_weights(self, agent_names: list[str]) -> list[float]:
        """Exposes core reliability logic for consensus protocols."""
        return self.core.calculate_reliability_scores(agent_names)

    def trace_workflow(self, workflow_name: str, duration: float) -> None:
        """Records a workflow trace for OpenTelemetry visualization."""
        self.prometheus.record_metric(
            "workflow_duration_seconds", duration, {"workflow": workflow_name}
        )
        self.log_event(
            "system",
            "workflow_trace",
            {"workflow": workflow_name, "duration": duration},
        )

    def get_summary(self) -> dict[str, Any]:
        """Returns a summary of performance and cost metrics."""
        if not self.metrics:
            return {"status": "No data"}

        total_latency = 0.0
        success_count = 0
        agents = {}

        for m in self.metrics:
            total_latency += m.duration_ms
            if m.status == "success":
                success_count += 1

            if m.agent_name not in agents:
                agents[m.agent_name] = {"calls": 0, "latency": 0.0, "cost": 0.0}

            a = agents[m.agent_name]
            a["calls"] += 1
            a["latency"] += m.duration_ms
            a["cost"] += m.estimated_cost

        count = len(self.metrics)
        summary = {
            "total_calls": count,
            "avg_latency_ms": round(total_latency / count, 2),
            "success_rate": round(success_count / count * 100, 2),
            "total_tokens": sum(m.token_count for m in self.metrics),
            "total_cost_usd": round(sum(m.estimated_cost for m in self.metrics), 6),
            "agents": {},
        }

        for name, data in agents.items():
            summary["agents"][name] = {
                "calls": data["calls"],
                "avg_latency": round(data["latency"] / data["calls"], 2),
                "total_cost": round(data["cost"], 6)
            }

        return summary

    def save(self) -> None:
        """Persist telemetry to disk."""
        try:
            data = [asdict(m) for m in self.metrics]
            self.telemetry_file.write_text(json.dumps(data, indent=2))
        except Exception as e:
            logging.error(f"Failed to save telemetry: {e}")

    def load(self) -> None:
        """Load telemetry from disk."""
        if self.telemetry_file.exists():
            try:
                data = json.loads(self.telemetry_file.read_text())

                self.metrics = [AgentMetric(**m) for m in data]
            except Exception as e:
                logging.error(f"Failed to load telemetry: {e}")
                self.metrics = []




class TokenCostEngine:
    def __init__(self):
        self.core = TokenCostCore()
    def calculate_cost(self, model, input_tokens=0, output_tokens=0):
        res = self.core.calculate_cost(input_tokens, output_tokens, model)
        return res.total_cost

class ModelFallbackEngine:
    def __init__(self, cost_engine=None):
        self.cost_engine = cost_engine
        self.core = ModelFallbackCore()
    def get_fallback_model(self, current_model):
        return self.core.determine_next_model(current_model)
