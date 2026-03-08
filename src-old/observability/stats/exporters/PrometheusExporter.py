#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/observability/stats/exporters/PrometheusExporter.description.md

# PrometheusExporter

**File**: `src\observability\stats\exporters\PrometheusExporter.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 59  
**Complexity**: 4 (simple)

## Overview

Exporter for fleet metrics in Prometheus/OpenMetrics format.
Enables real-time dashboards in Grafana and ELK stack.

## Classes (1)

### `PrometheusExporter`

Formats fleet telemetry into Prometheus-compatible metrics.

**Methods** (4):
- `__init__(self)`
- `record_metric(self, name, value, labels)`
- `generate_scrape_response(self)`
- `get_grafana_info(self)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/observability/stats/exporters/PrometheusExporter.improvements.md

# Improvements for PrometheusExporter

**File**: `src\observability\stats\exporters\PrometheusExporter.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 59 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `PrometheusExporter_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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


"""Exporter for fleet metrics in Prometheus/OpenMetrics format.
Enables real-time dashboards in Grafana and ELK stack.
"""

from src.core.base.version import VERSION
from typing import Dict, Any, Optional

__version__ = VERSION


class PrometheusExporter:
    """Formats fleet telemetry into Prometheus-compatible metrics."""

    def __init__(self) -> None:
        self.metrics_registry: dict[str, float] = {}

    def record_metric(
        self, name: str, value: float, labels: dict[str, str] | None = None
    ) -> str:
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
