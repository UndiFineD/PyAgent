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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from ..observability_core import ExportDestination
from ..observability_core import Metric
from datetime import datetime
from typing import Any, Dict, List, Optional
import json
import logging

__version__ = VERSION

class CloudExporter:
    """Export stats to cloud monitoring services.

    Supports exporting metrics to Datadog, Prometheus, Grafana,
    and other cloud monitoring platforms.

    Attributes:
        destination: The export destination.
        config: Export configuration.
        export_queue: Queued metrics for export.
    """

    def __init__(
        self,
        destination: ExportDestination,
        api_key: str = "",
        endpoint: str = ""
    ) -> None:
        """Initialize cloud exporter.

        Args:
            destination: The target cloud platform.
            api_key: API key for authentication.
            endpoint: Custom endpoint URL.
        """
        self.destination = destination
        self.api_key = api_key
        self.endpoint = endpoint or self._get_default_endpoint()
        self.export_queue: list[Metric] = []
        self._export_count = 0
        self._last_export: datetime | None = None

    def _get_default_endpoint(self) -> str:
        """Get default endpoint for destination.

        Returns:
            Default endpoint URL.
        """
        defaults = {
            ExportDestination.DATADOG: "https://api.datadoghq.com / v1 / series",
            ExportDestination.PROMETHEUS: "http://localhost:9090 / api / v1 / write",
            ExportDestination.GRAFANA: "http://localhost:3000 / api / datasources",
            ExportDestination.CLOUDWATCH: "cloudwatch.amazonaws.com",
            ExportDestination.STACKDRIVER: "monitoring.googleapis.com"
        }
        return defaults.get(self.destination, "")

    def queue_metric(self, metric: Metric) -> None:
        """Add metric to export queue.

        Args:
            metric: The metric to queue.
        """
        self.export_queue.append(metric)

    def export(self) -> int:
        """Export all queued metrics.

        Returns:
            Number of metrics exported.
        """
        if not self.export_queue:
            return 0
        count = len(self.export_queue)
        # Format metrics for destination
        if self.destination == ExportDestination.DATADOG:
            self._export_datadog()
        elif self.destination == ExportDestination.PROMETHEUS:
            self._export_prometheus()
        else:
            self._export_generic()
        self._export_count += count
        self._last_export = datetime.now()
        self.export_queue.clear()
        return count

    def _export_datadog(self) -> None:
        """Export in Datadog format."""
        payload: dict[str, list[dict[str, Any]]] = {
            "series": [{
                "metric": m.name,
                "points": [[int(datetime.now().timestamp()), m.value]],
                "type": m.metric_type.value,
                "tags": [f"{k}:{v}" for k, v in m.tags.items()]
            } for m in self.export_queue]
        }
        logging.debug(f"Datadog export: {json.dumps(payload)}")

    def _export_prometheus(self) -> None:
        """Export in Prometheus format (OpenMetrics)."""
        metrics_file = "data/metrics/prometheus.metrics"
        try:
            import os
            os.makedirs("data/metrics", exist_ok=True)
            
            lines = []
            for m in self.export_queue:
                # Track specialized metrics as requested in Phase 290
                # Success Rate (Counter/Gauge)
                # Latency (Histogram/Summary)
                # Token Burn Rate (Gauge)
                
                tags = ",".join(f'{k}="{v}"' for k, v in m.tags.items())
                tag_str = f"{{{tags}}}" if tags else ""
                lines.append(f"{m.name}{tag_str} {m.value}")
            
            with open(metrics_file, "a") as f:
                f.write("\n".join(lines) + "\n")
            
            logging.info(f"Prometheus export: Appended {len(lines)} metrics to {metrics_file}")
        except Exception as e:
            logging.error(f"Prometheus export failed: {e}")

    def _export_generic(self) -> None:
        """Generic export format."""
        data: list[dict[str, Any]] = [{
            "name": m.name,
            "value": m.value,
            "timestamp": m.timestamp,
            "tags": m.tags
        } for m in self.export_queue]
        logging.debug(f"Generic export: {json.dumps(data)}")

    def get_export_stats(self) -> dict[str, Any]:
        """Get export statistics.

        Returns:
            Export statistics.
        """
        return {
            "destination": self.destination.value,
            "total_exported": self._export_count,
            "last_export": self._last_export.isoformat() if self._last_export else None,
            "queue_size": len(self.export_queue)
        }