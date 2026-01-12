#!/usr/bin/env python3
<<<<<<< HEAD
=======
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

>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))

"""Exporter for fleet metrics in Prometheus/OpenMetrics format.
Enables real-time dashboards in Grafana and ELK stack.
"""

<<<<<<< HEAD
import logging
from typing import Dict, List, Any, Optional

class PrometheusExporter:
    """Formats fleet telemetry into Prometheus-compatible metrics."""
    
    def __init__(self) -> None:
        self.metrics_registry: Dict[str, float] = {}

    def record_metric(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> str:
=======
from __future__ import annotations

from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class PrometheusExporter:
    """Formats fleet telemetry into Prometheus-compatible metrics."""

    def __init__(self) -> None:
        self.metrics_registry: dict[str, float] = {}

    def record_metric(self, name: str, value: float, labels: dict[str, str] | None = None) -> str:
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))
        """Records a metric with optional labels."""
        label_str = ""
        if labels:
            label_str = "{" + ",".join([f'{k}="{v}"' for k, v in labels.items()]) + "}"
<<<<<<< HEAD
        
        metric_key = f"{name}{label_str}"
        self.metrics_registry[metric_key] = value
=======

        metric_key = f"{name}{label_str}"
        self.metrics_registry[metric_key] = value
        return metric_key
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))

    def generate_scrape_response(self) -> str:
        """Generates the text response for a Prometheus scrape endpoint."""
        lines = []
        for key, value in self.metrics_registry.items():
            # Basic Prometheus format: metric_name{labels} value
            lines.append(f"pyagent_{key} {value}")
<<<<<<< HEAD
        
        return "\n".join(lines)

    def get_grafana_info(self) -> str:
        """Returns info for Grafana integration."""
        return "Prometheus Exporter: Active on /metrics. Grafana Dashboard ID: 12345 (Simulated)"
=======

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
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))
