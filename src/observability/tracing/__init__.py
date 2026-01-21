"""
OpenTelemetry Tracing Package - Phase 20
=========================================

Distributed tracing with OpenTelemetry integration.
"""

from .open_telemetry_tracer import (
    # Constants
    TRACE_HEADERS,
    SpanAttributes,
    # Availability check
    is_otel_available,
    otel_import_error_traceback,
    # Initialization
    init_tracer,
    get_span_exporter,
    get_tracer,
    # Context propagation
    extract_trace_context,
    inject_trace_context,
    extract_trace_headers,
    contains_trace_headers,
    # Span creation
    create_span,
    traced,
    timed_span,
    # Span helpers
    get_current_span_safe,
    add_span_attributes,
    add_span_event,
    record_exception,
    # Timing
    SpanTiming,
    # Logging
    log_tracing_disabled_warning,
    # Testing
    NullSpan,
    NullTracer,
    get_null_tracer,
)

__all__ = [
    "TRACE_HEADERS",
    "SpanAttributes",
    "is_otel_available",
    "otel_import_error_traceback",
    "init_tracer",
    "get_span_exporter",
    "get_tracer",
    "extract_trace_context",
    "inject_trace_context",
    "extract_trace_headers",
    "contains_trace_headers",
    "create_span",
    "traced",
    "timed_span",
    "get_current_span_safe",
    "add_span_attributes",
    "add_span_event",
    "record_exception",
    "SpanTiming",
    "log_tracing_disabled_warning",
    "NullSpan",
    "NullTracer",
    "get_null_tracer",
]
