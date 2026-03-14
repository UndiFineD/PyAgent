#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/observability/stats/exporters/CloudExporter.description.md

# CloudExporter

**File**: `src\observability\stats\exporters\CloudExporter.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 165  
**Complexity**: 8 (moderate)

## Overview

Auto-extracted class from agent_stats.py

## Classes (1)

### `CloudExporter`

Export stats to cloud monitoring services.

Supports exporting metrics to Datadog, Prometheus, Grafana,
and other cloud monitoring platforms.

Attributes:
    destination: The export destination.
    config: Export configuration.
    export_queue: Queued metrics for export.

**Methods** (8):
- `__init__(self, destination, api_key, endpoint)`
- `_get_default_endpoint(self)`
- `queue_metric(self, metric)`
- `export(self)`
- `_export_datadog(self)`
- `_export_prometheus(self)`
- `_export_generic(self)`
- `get_export_stats(self)`

## Dependencies

**Imports** (9):
- `ObservabilityCore.ExportDestination`
- `ObservabilityCore.Metric`
- `__future__.annotations`
- `datetime.datetime`
- `json`
- `logging`
- `os`
- `src.core.base.Version.VERSION`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/observability/stats/exporters/CloudExporter.improvements.md

# Improvements for CloudExporter

**File**: `src\observability\stats\exporters\CloudExporter.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 165 lines (medium)  
**Complexity**: 8 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CloudExporter_test.py` with pytest tests

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


r"""Auto-extracted class from agent_stats.py"""
