#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/core/base/common/utils/AgentMetrics.description.md

# AgentMetrics

**File**: `src\core\base\common\utils\AgentMetrics.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 113  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for AgentMetrics.

## Classes (1)

### `AgentMetrics`

Manages execution metrics and statistics for an agent.

**Methods** (7):
- `record_file_processed(self, modified)`
- `record_agent_applied(self, agent_name)`
- `finalize(self)`
- `get_summary(self, dry_run)`
- `to_dict(self)`
- `benchmark_execution(self, files, total_time_provided)`
- `cost_analysis(self, backend, cost_per_request)`

## Dependencies

**Imports** (7):
- `dataclasses.dataclass`
- `dataclasses.field`
- `logging`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/core/base/common/utils/AgentMetrics.improvements.md

# Improvements for AgentMetrics

**File**: `src\core\base\common\utils\AgentMetrics.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 113 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AgentMetrics_test.py` with pytest tests

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

from dataclasses import dataclass, field
from typing import Dict, Any, List
import time
import logging


@dataclass
class AgentMetrics:
    """Manages execution metrics and statistics for an agent."""

    files_processed: int = 0
    files_modified: int = 0
    agents_applied: Dict[str, int] = field(default_factory=dict)
    start_time: float = field(default_factory=time.time)
    end_time: float = None

    def record_file_processed(self, modified: bool = False):
        """Record a file as processed."""
        self.files_processed += 1
        if modified:
            self.files_modified += 1

    def record_agent_applied(self, agent_name: str):
        """Record an agent application."""
        self.agents_applied[agent_name] = self.agents_applied.get(agent_name, 0) + 1

    def finalize(self):
        """Finalize metrics collection."""
        self.end_time = time.time()

    def get_summary(self, dry_run: bool = False) -> str:
        """Get a text summary of the metrics."""
        if not self.end_time:
            self.finalize()
        elapsed = self.end_time - self.start_time

        summary = f"""
=== Agent Execution Summary ===
Files processed: {self.files_processed}
Files modified:  {self.files_modified}
Execution time:  {elapsed:.2f}s
Dry-run mode:    {'Yes' if dry_run else 'No'}

Agents applied:
"""
        for agent, count in sorted(self.agents_applied.items()):
            summary += f"  - {agent}: {count} files\n"
        return summary

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to a dictionary for reporting."""
        if not self.end_time:
            self.finalize()
        elapsed = self.end_time - self.start_time
        return {
            "timestamp": time.time(),
            "start_time": self.start_time,
            "end_time": self.end_time,
            "summary": {
                "files_processed": self.files_processed,
                "files_modified": self.files_modified,
                "total_time_seconds": elapsed,
                "average_time_per_file": elapsed / max(self.files_processed, 1),
            },
            "agents_applied": self.agents_applied,
        }

    def benchmark_execution(
        self, files: List[Any], total_time_provided: float = None
    ) -> Dict[str, Any]:
        """Benchmark execution time per file and per agent."""
        if not self.end_time:
            self.finalize()

        total_time = (
            total_time_provided
            if total_time_provided is not None
            else (self.end_time - self.start_time)
        )
        files_count = len(files)
        avg_per_file = total_time / max(files_count, 1)

        benchmarks: Dict[str, Any] = {
            "total_time": total_time,
            "file_count": files_count,
            "average_per_file": avg_per_file,
            "per_file": {str(getattr(f, "name", f)): avg_per_file for f in files},
            "per_agent": dict(self.agents_applied),
        }

        logging.debug(
            f"Benchmarks: {files_count} files in {total_time:.2f}s "
            f"({avg_per_file:.2f}s / file)"
        )
        return benchmarks

    def cost_analysis(
        self, backend: str = "github-models", cost_per_request: float = 0.0001
    ) -> Dict[str, Any]:
        """Analyze API usage cost for the agent execution."""
        total_agent_runs = sum(self.agents_applied.values())

        # Estimate requests: one per file per agent type
        estimated_requests = total_agent_runs
        estimated_cost = estimated_requests * cost_per_request

        analysis: Dict[str, Any] = {
            "backend": backend,
            "files_processed": self.files_processed,
            "agents_applied": dict(self.agents_applied),
            "total_agent_runs": total_agent_runs,
            "cost_per_request": cost_per_request,
            "estimated_requests": estimated_requests,
            "total_estimated_cost": estimated_cost,
            "cost_per_file": estimated_cost / max(self.files_processed, 1),
        }

        logging.info(
            f"Cost analysis: {estimated_requests} requests, "
            f"${estimated_cost:.4f} estimated"
        )
        return analysis
