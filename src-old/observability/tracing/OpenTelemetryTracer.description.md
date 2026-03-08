# OpenTelemetryTracer

**File**: `src\observability\tracing\OpenTelemetryTracer.py`  
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
