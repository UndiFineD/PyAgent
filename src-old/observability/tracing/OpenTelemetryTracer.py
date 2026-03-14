#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/observability/tracing/OpenTelemetryTracer.description.md

# OpenTelemetryTracer

**File**: `src\\observability\tracing\\OpenTelemetryTracer.py`  
**Type**: Python Module  
**Summary**: 4 classes, 17 functions, 34 imports  
**Lines**: 605  
**Complexity**: 30 (complex)

## Overview

OpenTelemetry Tracing Module - Phase 20: Production Infrastructure
===================================================================

Distributed tracing with OpenTelemetry integration.
Inspired by vLLM's tracing.py pattern.

Features:
- SpanAttributes: Standard attribute names for LLM operations
- Trace context extraction and propagation
- OTLP exporter support (gRPC and HTTP)
- Graceful fallback when OpenTelemetry is not installed
- Span context managers and decorators
- Custom span processors

Author: PyAgent Phase 20

## Classes (4)

### `SpanAttributes`

Standard span attribute names for LLM and AI operations.

Based on OpenTelemetry semantic conventions for GenAI.

### `SpanTiming`

Helper for tracking timing within a span.

**Methods** (4):
- `checkpoint(self, name)`
- `elapsed(self)`
- `to_attributes(self, prefix)`
- `apply_to_span(self, span, prefix)`

### `NullSpan`

A no-op span for testing or when tracing is disabled.

**Methods** (7):
- `set_attribute(self, key, value)`
- `add_event(self, name, attributes)`
- `record_exception(self, exception, escaped)`
- `set_status(self, status)`
- `is_recording(self)`
- `__enter__(self)`
- `__exit__(self)`

### `NullTracer`

A no-op tracer for testing or when tracing is disabled.

**Methods** (2):
- `start_as_current_span(self, name)`
- `start_span(self, name)`

## Functions (17)

### `is_otel_available()`

Check if OpenTelemetry is available.

### `init_tracer(instrumenting_module_name, otlp_traces_endpoint)`

Initialize an OpenTelemetry tracer.

Args:
    instrumenting_module_name: Name of the module being instrumented.
    otlp_traces_endpoint: OTLP endpoint URL for trace export.
    use_batch_processor: If True, use batch span processor (recommended).

Returns:
    Tracer instance or None if OpenTelemetry is not available.

Raises:
    ValueError: If OpenTelemetry is not available.

### `get_span_exporter(endpoint)`

Get a span exporter based on the configured protocol.

Supports both gRPC and HTTP protocols.

### `get_tracer(name)`

Get a tracer from the current provider.

Returns None if OpenTelemetry is not available.

### `extract_trace_context(headers)`

Extract trace context from HTTP headers.

Args:
    headers: HTTP headers containing trace context.

Returns:
    OpenTelemetry context or None.

### `inject_trace_context(headers)`

Inject current trace context into headers.

Args:
    headers: Dictionary to inject trace context into.

Returns:
    Headers with trace context added.

### `extract_trace_headers(headers)`

Extract only trace-related headers from a headers mapping.

### `contains_trace_headers(headers)`

Check if headers contain trace context.

### `create_span(name, tracer)`

Context manager for creating a span.

Args:
    name: Span name.
    tracer: Tracer to use (uses global if not provided).
    kind: Span kind (CLIENT, SERVER, PRODUCER, CONSUMER, INTERNAL).
    attributes: Initial span attributes.
    context: Parent context.
    record_exception: If True, record exceptions on the span.
    set_status_on_exception: If True, set error status on exception.

Yields:
    Span instance or None if tracing is not available.

Example:
    >>> with create_span("process_request", attributes={"user_id": 123}) as span:
    ...     if span:
    ...         span.set_attribute("status", "processing")
    ...     result = do_work()

### `traced(name)`

Decorator to trace a function.

Args:
    name: Span name (defaults to function name).
    tracer: Tracer to use.
    kind: Span kind.
    attributes: Static span attributes.
    record_exception: If True, record exceptions.

Example:
    >>> @traced("process_data", attributes={"service": "processor"})
    ... def process_data(data: str) -> str:
    ...     return data.upper()

## Dependencies

**Imports** (34):
- `__future__.annotations`
- `collections.abc.Mapping`
- `contextlib.contextmanager`
- `dataclasses.dataclass`
- `dataclasses.field`
- `functools`
- `logging`
- `opentelemetry.context.context.Context`
- `opentelemetry.exporter.otlp.proto.grpc.trace_exporter.OTLPSpanExporter`
- `opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter`
- `opentelemetry.sdk.environment_variables.OTEL_EXPORTER_OTLP_TRACES_PROTOCOL`
- `opentelemetry.sdk.trace.TracerProvider`
- `opentelemetry.sdk.trace.export.BatchSpanProcessor`
- `opentelemetry.sdk.trace.export.SimpleSpanProcessor`
- `opentelemetry.sdk.trace.export.SpanExporter`
- ... and 19 more

---
*Auto-generated documentation*
## Source: src-old/observability/tracing/OpenTelemetryTracer.improvements.md

# Improvements for OpenTelemetryTracer

**File**: `src\\observability\tracing\\OpenTelemetryTracer.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 605 lines (large)  
**Complexity**: 30 score (complex)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `OpenTelemetryTracer_test.py` with pytest tests

### Code Organization
- [TIP] **4 classes in one file** - Consider splitting into separate modules

### File Complexity
- [!] **Large file** (605 lines) - Consider refactoring

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


"""
OpenTelemetry Tracing Module - Phase 20: Production Infrastructure
===================================================================

Distributed tracing with OpenTelemetry integration.
Inspired by vLLM's tracing.py pattern.

Features:
- SpanAttributes: Standard attribute names for LLM operations
- Trace context extraction and propagation
- OTLP exporter support (gRPC and HTTP)
- Graceful fallback when OpenTelemetry is not installed
- Span context managers and decorators
- Custom span processors

Author: PyAgent Phase 20
"""


import functools
import logging
import os
import time
from collections.abc import Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generator,
    ParamSpec,
    TypeVar,
)

logger = logging.getLogger(__name__)

# Standard trace headers
TRACE_HEADERS = ["traceparent", "tracestate"]

# Track if OpenTelemetry is available
OTEL_IMPORT_ERROR_TRACEBACK: str | None = None
# Type stubs for when otel is not available (runtime)
if not TYPE_CHECKING:
    Context = Any
    Tracer = Any
    Span = Any
    SpanKind = Any
    get_current_span = None

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import (
        BatchSpanProcessor,
        SimpleSpanProcessor,
        SpanExporter,
    )
    from opentelemetry.trace import (
        SpanKind,
        Status,
        StatusCode,
        get_current_span,
        get_tracer_provider,
        set_tracer_provider,
    )

    if not TYPE_CHECKING:
        from opentelemetry.context.context import Context
        from opentelemetry.trace import Span, Tracer

    _IS_OTEL_IMPORTED = True
except ImportError:
    import traceback

    OTEL_IMPORT_ERROR_TRACEBACK = traceback.format_exc()
    Status = None
    StatusCode = None
    TracerProvider = None  # type: ignore[assignment]
    BatchSpanProcessor = None  # type: ignore[assignment]
    SimpleSpanProcessor = None  # type: ignore[assignment]
    SpanExporter = None  # type: ignore[assignment]
    set_tracer_provider = None  # type: ignore[assignment]
    get_tracer_provider = None  # type: ignore[assignment]
    get_current_span = None  # type: ignore[assignment]
    _IS_OTEL_IMPORTED = False


P = ParamSpec("P")
T = TypeVar("T")


# ============================================================================
# Span Attributes (Standard names for LLM operations)
# ============================================================================


class SpanAttributes:
    """
    """
