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

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Exporter for fleet metrics in Prometheus/OpenMetrics format.
Enables real-time dashboards in Grafana and ELK stack.
"""



import logging
from typing import Dict, List, Any, Optional



































class PrometheusExporter:
    """Formats fleet telemetry into Prometheus-compatible metrics."""
    
    def __init__(self) -> None:
        self.metrics_registry: Dict[str, float] = {}

    def record_metric(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> str:
        """Records a metric with optional labels."""
        label_str = ""
        if labels:
            label_str = "{" + ",".join([f'{k}="{v}"' for k, v in labels.items()]) + "}"
        
        metric_key = f"{name}{label_str}"
        self.metrics_registry[metric_key] = value

    def generate_scrape_response(self) -> str:
        """Generates the text response for a Prometheus scrape endpoint."""
        lines = []
        for key, value in self.metrics_registry.items():
            # Basic Prometheus format: metric_name{labels} value
            lines.append(f"pyagent_{key} {value}")
        
        return "\n".join(lines)

    def get_grafana_info(self) -> Dict[str, Any]:
        """Returns connection details for Grafana integration."""
        return {
            "datasource_type": "Prometheus",
            "scrape_interval": "15s",
            "endpoint": "/metrics",
            "suggested_dashboard_uid": "pyagent-swarm-health-main",
            "provisioning_status": "Ready",
            "metric_prefix": "pyagent_"
        }
