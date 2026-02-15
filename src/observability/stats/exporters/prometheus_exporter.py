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
Prometheus Exporter - Formats fleet telemetry into Prometheus/OpenMetrics metrics

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate PrometheusExporter and call record_metric(name, value, labels) as telemetry is produced.
- Expose generate_scrape_response() on an HTTP GET /metrics endpoint for Prometheus to scrape.
- Use get_grafana_info() to seed Grafana provisioning or documentation.

WHAT IT DOES:
- Provides a minimal in-process registry (dict) mapping metric_name{labels} -> float.
- Serializes metrics into a simple text/plain Prometheus scrape response prefixed with "pyagent_".
- Supplies static Grafana integration metadata to help dashboard provisioning.

WHAT IT SHOULD DO BETTER:
- Sanitize and validate metric names and label keys/values to follow Prometheus naming and
  escaping rules.
- Support metric types (counter/gauge/histogram/summary), HELP/TYPE lines, and richer metric
  families (histograms, exemplars).
- Be concurrency-safe (locks/async primitives), optionally integrate with the official
  prometheus_client package, and add unit tests and metrics TTL/expiration.

FILE CONTENT SUMMARY:
Exporter for fleet metrics in Prometheus/OpenMetrics format.
Enables real-time dashboards in Grafana and ELK stack.
"""

from __future__ import annotations

from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class PrometheusExporter:
    """Formats fleet telemetry into Prometheus-compatible metrics."""

    def __init__(self) -> None:
        self.metrics_registry: dict[str, float] = {}

    def record_metric(self, name: str, value: float, labels: dict[str, str] | None = None) -> str:
        """Records a metric with optional labels."""
        label_str = ""
        if labels:
            label_str = "{" + ",".join([f'{k}="{v}"' for k, v in labels.items()]) + "}"

        metric_key = f"{name}{label_str}"
        self.metrics_registry[metric_key] = value
        return metric_key

    def generate_scrape_response(self) -> str:
        """Generates the text response for a Prometheus scrape endpoint."""
        lines = []
        for key, value in self.metrics_registry.items():
            # Basic Prometheus format: metric_name{labels} value
            lines.append(f"pyagent_{key} {value}")

        return "\n".join(lines)

    def get_grafana_info(self) -> dict[str, Any]:
        """Returns connection details for Grafana integration."""
        return {
            "datasource_type": "Prometheus",
            "scrape_interval": "15s",
            "endpoint": "/metrics",
            "suggested_dashboard_uid": "pyagent-swarm-health-main",
            "provisioning_status": "Ready",
            "metric_prefix": "pyagent_",
        }
