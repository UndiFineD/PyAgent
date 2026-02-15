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
Metrics Exporter - Consolidate and expose fleet telemetry

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate: exporter = MetricsExporter()
- Record agent call: exporter.record_agent_call("AgentName", duration_ms, success_bool)
- Record resource usage: exporter.record_resource_usage(cpu_percent, mem_mb)
- Get scrape payload: payload = exporter.get_prometheus_payload()
- Push simulation: exporter.export_to_grafana()

WHAT IT DOES:
- Centralizes fleet telemetry and forwards metrics to a Prometheus-compatible
  exporter implementation (PrometheusExporter).
- Provides simple helpers for recording agent execution timing/counts and
  process resource usage, and for producing a Prometheus scrape payload or
  simulating a push to Grafana Cloud.
- Tracks last export timestamp for basic batching/observability.

WHAT IT SHOULD DO BETTER:
- Add explicit return types and error handling; current record_* methods
  return None though annotated as str in signatures and should return
  consistent status or be typed None.
- Make exporters pluggable via configuration (backend selection, auth,
  endpoints) and support async/non-blocking exports with retries, backoff,
  and rate limiting.
- Improve label normalization, histogram buckets for durations,
  sampling/aggregation strategy, thread-safety for concurrent metric updates,
  and unit/integration tests for backend behavior; add telemetry tests and
  metrics naming constants.

FILE CONTENT SUMMARY:
Exporter for high-level fleet metrics.
Sends telemetry to specialized backends like Prometheus, InfluxDB, or Grafana Cloud.
"""

from __future__ import annotations

import logging
import time

from src.core.base.lifecycle.version import VERSION

from .prometheus_exporter import PrometheusExporter

__version__ = VERSION


class MetricsExporter:
    """Consolidates all fleet telemetry and exposes it for external monitoring."""

    def __init__(self) -> None:
        self.prometheus = PrometheusExporter()
        self.last_export_time = time.time()

    def record_agent_call(self, agent_name: str, duration_ms: float, success: bool) -> str:
        """Records a single agent execution event."""
        labels = {"agent": agent_name, "status": "success" if success else "failure"}

        self.prometheus.record_metric("agent_call_duration_ms", duration_ms, labels)
        self.prometheus.record_metric("agent_calls_total", 1.0, labels)

    def record_resource_usage(self, cpu_percent: float, mem_mb: float) -> str:
        """Records system resource usage for the fleet process."""
        self.prometheus.record_metric("fleet_cpu_percent", cpu_percent)
        self.prometheus.record_metric("fleet_memory_mb", mem_mb)

    def get_prometheus_payload(self) -> str:
        """Returns the payload for a Prometheus scrape."""
        return self.prometheus.generate_scrape_response()

    def export_to_grafana(self) -> str:
        """Simulates pushing metrics to a Grafana Cloud API."""

        payload = self.get_prometheus_payload()
        logging.info(f"MetricsExporter: Pushing batch to Grafana... ({len(payload)} bytes)")
        self.last_export_time = time.time()
        return "Export successful."


if __name__ == "__main__":
    exporter = MetricsExporter()
    exporter.record_agent_call("CoderAgent", 1500.0, True)
    exporter.record_resource_usage(12.5, 256.0)
    print(exporter.get_prometheus_payload())
