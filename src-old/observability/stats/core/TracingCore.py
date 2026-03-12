"""
LLM_CONTEXT_START

## Source: src-old/observability/stats/core/TracingCore.description.md

# TracingCore

**File**: `src\observability\stats\core\TracingCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 39  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for TracingCore.

## Classes (1)

### `TracingCore`

TracingCore handles the logic for distributed tracing and latency breakdown.
It prepares trace data for OpenTelemetry (OTel) exporters.

**Methods** (3):
- `create_span_context(self, trace_id, span_id)`
- `calculate_latency_breakdown(self, total_time, network_time)`
- `format_otel_log(self, name, attributes)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `time`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
## Source: src-old/observability/stats/core/TracingCore.improvements.md

# Improvements for TracingCore

**File**: `src\observability\stats\core\TracingCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 39 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TracingCore_test.py` with pytest tests

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

from __future__ import annotations

from typing import Dict, Any
import time


class TracingCore:
    """
    TracingCore handles the logic for distributed tracing and latency breakdown.
    It prepares trace data for OpenTelemetry (OTel) exporters.
    """

    def create_span_context(self, trace_id: str, span_id: str) -> dict[str, str]:
        """Creates a standardized context for distributed tracing."""
        return {"trace_id": trace_id, "span_id": span_id, "version": "OTel-1.1"}

    def calculate_latency_breakdown(
        self, total_time: float, network_time: float
    ) -> dict[str, float]:
        """
        Calculates agent thinking time vs network latency.
        """
        thinking_time = total_time - network_time
        return {
            "total_latency_ms": total_time * 1000,
            "network_latency_ms": network_time * 1000,
            "agent_thinking_ms": thinking_time * 1000,
            "think_ratio": thinking_time / total_time if total_time > 0 else 0,
        }

    def format_otel_log(self, name: str, attributes: dict[str, Any]) -> dict[str, Any]:
        """Formats a single telemetry event for OTel ingestion."""
        return {
            "timestamp": time.time_ns(),
            "name": name,
            "attributes": attributes,
            "kind": "INTERNAL",
        }
