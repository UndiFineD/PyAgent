#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/observability/stats/exporters/ResourceMonitor.description.md

# ResourceMonitor

**File**: `src\observability\stats\exporters\ResourceMonitor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 80  
**Complexity**: 4 (simple)

## Overview

Engine for monitoring system resources (CPU, Memory, Disk).

## Classes (1)

### `ResourceMonitor`

Monitors local system load to inform agent execution strategies.

**Methods** (4):
- `__init__(self, workspace_root)`
- `get_current_stats(self)`
- `save_stats(self)`
- `get_execution_recommendation(self)`

## Dependencies

**Imports** (9):
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `platform`
- `psutil`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/observability/stats/exporters/ResourceMonitor.improvements.md

# Improvements for ResourceMonitor

**File**: `src\observability\stats\exporters\ResourceMonitor.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 80 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ResourceMonitor_test.py` with pytest tests

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

"""Engine for monitoring system resources (CPU, Memory, Disk)."""

import json
import logging
import platform
from pathlib import Path
from typing import Any, Dict

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


class ResourceMonitor:
    """Monitors local system load to inform agent execution strategies."""

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.stats_file = self.workspace_root / ".system_stats.json"

    def get_current_stats(self) -> Dict[str, Any]:
        """Collects current CPU, Memory, and Disk metrics."""
        stats = {
            "platform": platform.platform(),
            "cpu_usage_pct": 0,
            "memory_usage_pct": 0,
            "disk_free_gb": 0,
            "status": "UNAVAILABLE",
        }

        if not HAS_PSUTIL:
            return stats

        try:
            stats["cpu_usage_pct"] = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            stats["memory_usage_pct"] = mem.percent

            disk = psutil.disk_usage(str(self.workspace_root))
            stats["disk_free_gb"] = round(disk.free / (1024**3), 2)

            # Simple threshold logic
            if stats["cpu_usage_pct"] > 90 or stats["memory_usage_pct"] > 90:
                stats["status"] = "CRITICAL"
            elif stats["cpu_usage_pct"] > 70 or stats["memory_usage_pct"] > 70:
                stats["status"] = "WARNING"
            else:
                stats["status"] = "HEALTHY"

        except Exception as e:
            logging.error(f"Failed to gather resource stats: {e}")
            stats["status"] = "ERROR"

        return stats

    def save_stats(self) -> str:
        """Saves current stats to disk."""
        stats = self.get_current_stats()
        try:
            self.stats_file.write_text(json.dumps(stats, indent=2))
        except Exception as e:
            logging.error(f"Failed to save system stats: {e}")

    def get_execution_recommendation(self) -> str:
        """Suggests whether to run heavy tasks."""
        stats = self.get_current_stats()
        if stats["status"] == "CRITICAL":
            return "PAUSE: System load is too high. Defer heavy indexing or LLM calls."
        elif stats["status"] == "WARNING":
            return "CAUTION: Elevated load. Run tasks sequentially rather than in parallel."
        return "PROCEED: System resources are sufficient."


if __name__ == "__main__":
    mon = ResourceMonitor("c:/DEV/PyAgent")
    print(json.dumps(mon.get_current_stats(), indent=2))
    print(f"Recommendation: {mon.get_execution_recommendation()}")
