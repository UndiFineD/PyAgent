#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/observability/stats/exporters/ObservabilityCore.description.md

# ObservabilityCore

**File**: `src\observability\stats\exporters\ObservabilityCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 9 imports  
**Lines**: 68  
**Complexity**: 4 (simple)

## Overview

ObservabilityCore logic for metric aggregation and auditing.
Pure logic for summarizing agent performance and costs.

## Classes (2)

### `AgentMetric`

Class AgentMetric implementation.

### `ObservabilityCore`

Pure logic for processing agent telemetry data.

**Methods** (4):
- `__init__(self)`
- `process_metric(self, metric)`
- `summarize_performance(self)`
- `filter_by_time(self, start_iso, end_iso)`

## Dependencies

**Imports** (9):
- `dataclasses.asdict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `json`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/observability/stats/exporters/ObservabilityCore.improvements.md

# Improvements for ObservabilityCore

**File**: `src\observability\stats\exporters\ObservabilityCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 68 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: AgentMetric

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ObservabilityCore_test.py` with pytest tests

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

"""
ObservabilityCore logic for metric aggregation and auditing.
Pure logic for summarizing agent performance and costs.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class AgentMetric:
    agent_name: str
    operation: str
    duration_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "success"
    token_count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost: float = 0.0
    model: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)


class ObservabilityCore:
    """Pure logic for processing agent telemetry data."""

    def __init__(self) -> None:
        self.metrics_history: List[AgentMetric] = []

    def process_metric(self, metric: AgentMetric):
        """Standardizes a metric entry."""
        self.metrics_history.append(metric)

    def summarize_performance(self) -> Dict[str, Any]:
        """Calculates aggregate stats from history."""
        if not self.metrics_history:
            return {"count": 0, "avg_duration": 0, "total_cost": 0}

        total_duration = sum(m.duration_ms for m in self.metrics_history)
        total_cost = sum(m.estimated_cost for m in self.metrics_history)
        count = len(self.metrics_history)

        # Breakdown by agent
        by_agent = {}
        for m in self.metrics_history:
            if m.agent_name not in by_agent:
                by_agent[m.agent_name] = {
                    "count": 0,
                    "total_cost": 0,
                    "avg_duration": 0,
                }
            stats = by_agent[m.agent_name]
            stats["count"] += 1
            stats["total_cost"] += m.estimated_cost

        return {
            "total_count": count,
            "avg_duration_ms": total_duration / count,
            "total_cost_usd": round(total_cost, 6),
            "agents": by_agent,
        }

    def filter_by_time(self, start_iso: str, end_iso: str) -> List[AgentMetric]:
        """Filters metrics within a time range."""
        results = []
        for m in self.metrics_history:
            if start_iso <= m.timestamp <= end_iso:
                results.append(m)
        return results
