#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/stats/MetricsExporter.description.md

# MetricsExporter

**File**: `src\classes\stats\MetricsExporter.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 45  
**Complexity**: 5 (moderate)

## Overview

Exporter for high-level fleet metrics.
Sends telemetry to specialized backends like Prometheus, InfluxDB, or Grafana Cloud.

## Classes (1)

### `MetricsExporter`

Consolidates all fleet telemetry and exposes it for external monitoring.

**Methods** (5):
- `__init__(self)`
- `record_agent_call(self, agent_name, duration_ms, success)`
- `record_resource_usage(self, cpu_percent, mem_mb)`
- `get_prometheus_payload(self)`
- `export_to_grafana(self)`

## Dependencies

**Imports** (7):
- `logging`
- `src.classes.stats.PrometheusExporter.PrometheusExporter`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/stats/MetricsExporter.improvements.md

# Improvements for MetricsExporter

**File**: `src\classes\stats\MetricsExporter.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 45 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MetricsExporter_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""Exporter for high-level fleet metrics.
Sends telemetry to specialized backends like Prometheus, InfluxDB, or Grafana Cloud.
"""

import logging
import time
from typing import Dict, List, Any, Optional
from src.classes.stats.PrometheusExporter import PrometheusExporter


class MetricsExporter:
    """Consolidates all fleet telemetry and exposes it for external monitoring."""

    def __init__(self) -> None:
        self.prometheus = PrometheusExporter()
        self.last_export_time = time.time()

    def record_agent_call(
        self, agent_name: str, duration_ms: float, success: bool
    ) -> str:
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
        logging.info(
            f"MetricsExporter: Pushing batch to Grafana... ({len(payload)} bytes)"
        )
        self.last_export_time = time.time()
        return "Export successful."


if __name__ == "__main__":
    exporter = MetricsExporter()
    exporter.record_agent_call("CoderAgent", 1500.0, True)
    exporter.record_resource_usage(12.5, 256.0)
    print(exporter.get_prometheus_payload())
