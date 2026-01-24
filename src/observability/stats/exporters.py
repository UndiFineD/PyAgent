#!/usr/bin/env python3

"""
Exporters.py module.
"""
# Copyright 2026 PyAgent Authors
# Consolidated exporters for Prometheus, OTel, and Cloud Monitoring.

from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from .analysis import TracingCore
from .metrics import Metric
from .observability_core import ExportDestination

logger = logging.getLogger(__name__)


@dataclass
class Span:
    """A tracing span for OTel."""

    name: str
    trace_id: str
    span_id: str
    parent_id: str | None = None

    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    status: str = "unset"


class PrometheusExporter:
    """Formats fleet telemetry into Prometheus-compatible metrics."""

    def __init__(self) -> None:
        self.metrics_registry: dict[str, float] = {}

    def record_metric(self, name: str, value: float, labels: dict[str, str] | None = None) -> None:
        label_str = ""
        if labels:
            label_str = "{" + ",".join([f'{k}="{v}"' for k, v in labels.items()]) + "}"
        self.metrics_registry[f"{name}{label_str}"] = value

    def generate_scrape_response(self) -> str:
        return "\n".join([f"pyagent_{k} {v}" for k, v in self.metrics_registry.items()])


class OTelManager:
    """Manages OTel-compatible spans and traces."""

    def __init__(self) -> None:
        self.active_spans: dict[str, Span] = {}
        self.completed_spans: list[Span] = []

        self.core = TracingCore()

    def start_span(
        self,
        name: str,
        parent_id: str | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> str:
        span_id = str(uuid.uuid4())
        trace_id = parent_id if parent_id else str(uuid.uuid4())

        span = Span(
            name=name,
            trace_id=trace_id,
            span_id=span_id,
            parent_id=parent_id,
            attributes=attributes or {},
        )

        self.active_spans[span_id] = span
        return span_id

    def end_span(
        self,
        span_id: str,
        status: str = "ok",
        network_latency_sec: float = 0.0,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        span = self.active_spans.pop(span_id, None)
        if not span:
            return

        span.end_time = time.time()
        span.status = status
        if attributes:
            span.attributes.update(attributes)

        total_latency = span.end_time - span.start_time
        breakdown = self.core.calculate_latency_breakdown(total_latency, network_latency_sec)
        span.attributes.update(breakdown)

        self.completed_spans.append(span)

    def export_spans(self) -> list[dict[str, Any]]:
        batch = [vars(s) for s in self.completed_spans]

        self.completed_spans = []
        return batch


class CloudExporter:
    """Export stats to cloud monitoring services."""

    def __init__(self, destination: ExportDestination, api_key: str = "", endpoint: str = "") -> None:
        self.destination = destination
        self.api_key = api_key
        self.endpoint = endpoint or self._get_default_endpoint()

        self.export_queue: list[Metric] = []

    def _get_default_endpoint(self) -> str:
        defaults = {
            ExportDestination.DATADOG: "https://api.datadoghq.com/v1/series",
            ExportDestination.PROMETHEUS: "http://localhost:9090/api/v1/write",
            ExportDestination.GRAFANA: "http://localhost:3000/api/datasources",
        }
        return defaults.get(self.destination, "")

    def queue_metric(self, metric: Metric) -> None:
        self.export_queue.append(metric)

    def export(self) -> int:
        if not self.export_queue:
            return 0
        count = len(self.export_queue)
        self.export_queue.clear()
        return count


class MetricsExporter:
    """Consolidates fleet telemetry for external monitoring."""

    def __init__(self) -> None:
        self.prometheus = PrometheusExporter()

    def record_agent_call(self, agent: str, duration: float, success: bool) -> None:
        labels = {"agent": agent, "status": "success" if success else "failure"}
        self.prometheus.record_metric("agent_call_duration_ms", duration, labels)
        self.prometheus.record_metric("agent_calls_total", 1.0, labels)

    def get_prometheus_payload(self) -> str:
        return self.prometheus.generate_scrape_response()


class StatsExporter:
    """Exports stats in various formats."""

    def __init__(self, format: str = "json") -> None:
        self.format = format

    def export(self, metrics: dict[str, Any], format: str | None = None) -> str:
        f = format or self.format
        return json.dumps(metrics) if f == "json" else ""
