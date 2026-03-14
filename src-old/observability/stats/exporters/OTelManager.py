#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/observability/stats/exporters/OTelManager.description.md

# OTelManager

**File**: `src\observability\stats\exporters\OTelManager.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 13 imports  
**Lines**: 161  
**Complexity**: 5 (moderate)

## Overview

Distributed tracing for the PyAgent fleet using OpenTelemetry standards.
Allows visualization of agent chains and request propagation across nodes.

## Classes (2)

### `Span`

Class Span implementation.

### `OTelManager`

Manages OTel-compatible spans and traces for cross-fleet observability.
Integrated with TracingCore for latency analysis and OTel formatting.

**Methods** (5):
- `__init__(self)`
- `start_span(self, name, parent_id, attributes)`
- `end_span(self, span_id, status, network_latency_sec, attributes)`
- `export_spans(self)`
- `get_trace_context(self, span_id)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `logging`
- `opentelemetry.sdk.resources.Resource`
- `opentelemetry.sdk.trace.TracerProvider`
- `opentelemetry.trace`
- `src.core.base.Version.VERSION`
- `src.observability.stats.core.TracingCore.TracingCore`
- `threading`
- `time`
- `typing.Any`
- `uuid`

---
*Auto-generated documentation*
## Source: src-old/observability/stats/exporters/OTelManager.improvements.md

# Improvements for OTelManager

**File**: `src\observability\stats\exporters\OTelManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 161 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: Span

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `OTelManager_test.py` with pytest tests

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


"""Distributed tracing for the PyAgent fleet using OpenTelemetry standards.
Allows visualization of agent chains and request propagation across nodes.
"""

import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from src.core.base.Version import VERSION
from src.observability.stats.core.TracingCore import TracingCore

# Phase 307: Official OpenTelemetry SDK integration
try:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider

    # Initialize Global Tracer
    resource = Resource(attributes={"service.name": "pyagent-fleet"})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)
    HAS_OTEL = True
except ImportError:
    HAS_OTEL = False

__version__ = VERSION


@dataclass
class Span:
    name: str
    trace_id: str
    span_id: str
    parent_id: str | None = None

    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    status: str = "unset"


class OTelManager:
    """
    """
