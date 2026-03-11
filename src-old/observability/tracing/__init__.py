#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/observability/tracing/__init__.description.md

# Description: src/observability/tracing/__init__.py

Module purpose:
- Provides a lazy-loading entry point for the `observability.tracing` subpackage.
- Exposes a registry of names that are loaded on-demand from `open_telemetry_tracer` through `ModuleLazyLoader`.

Behavioral notes:
- Uses `ModuleLazyLoader` to avoid importing heavy OpenTelemetry packages at import time.
- Defines `__getattr__` to forward attribute access to the lazy loader.

Public symbols (lazy):
- `NullSpan`, `NullTracer`, `SpanAttributes`, `SpanTiming`, `TRACE_HEADERS`, and many helper functions like `create_span`, `traced`, `init_tracer`, etc. (all lazily loaded)
## Source: src-old/observability/tracing/__init__.improvements.md

# Improvements: src/observability/tracing/__init__.py

Suggested improvements (automatically generated):
- Add unit tests covering core behavior and edge cases.
- Break large modules into smaller, testable components.
- Avoid heavy imports at module import time; import lazily where appropriate.
- Add type hints and explicit return types for public functions.
- Add logging and better error handling for file and IO operations.
- Consider dependency injection for filesystem and environment interactions.

LLM_CONTEXT_END
"""

"""Lazy-loading entry point for observability.tracing."""
from __future__ import annotations

from typing import Any

try:
    from src.interface.lazy_loader import ModuleLazyLoader
except ImportError:
    # Fallback for when lazy_loader is not available
    class ModuleLazyLoader:
        """Simple fallback lazy loader that raises an error
        if used without the actual implementation.
        """

        def __init__(self, registry):
            """Initialize with a registry of module paths and attributes."""
            self.registry = registry

        def load(self, name: str):
            """Load the specified attribute from the registered module."""
            if name not in self.registry:
                raise AttributeError(f"module has no attribute '{name}'")
            module_path, attr_name = self.registry[name]
            mod = __import__(module_path, fromlist=[attr_name])
            return getattr(mod, attr_name)

from .open_telemetry_tracer import (
    TRACE_HEADERS,
    NullSpan,
    NullTracer,
    SpanAttributes,
    SpanTiming,
    add_span_attributes,
    add_span_event,
    contains_trace_headers,
    create_span,
    extract_trace_context,
    extract_trace_headers,
    get_current_span_safe,
    get_null_tracer,
    get_span_exporter,
    get_tracer,
    init_tracer,
    inject_trace_context,
    is_otel_available,
    log_tracing_disabled_warning,
    otel_import_error_traceback,
    record_exception,
    timed_span,
    traced,
)

_LAZY_REGISTRY = {
    "NullSpan": ("src.observability.tracing.open_telemetry_tracer", "NullSpan"),
    "NullTracer": ("src.observability.tracing.open_telemetry_tracer", "NullTracer"),
    "SpanAttributes": (
        "src.observability.tracing.open_telemetry_tracer",
        "SpanAttributes",
    ),
    "SpanTiming": ("src.observability.tracing.open_telemetry_tracer", "SpanTiming"),
    "TRACE_HEADERS": (
        "src.observability.tracing.open_telemetry_tracer",
        "TRACE_HEADERS",
    ),
    "add_span_attributes": (
        "src.observability.tracing.open_telemetry_tracer",
        "add_span_attributes",
    ),
    "add_span_event": (
        "src.observability.tracing.open_telemetry_tracer",
        "add_span_event",
    ),
    "contains_trace_headers": (
        "src.observability.tracing.open_telemetry_tracer",
        "contains_trace_headers",
    ),
    "create_span": ("src.observability.tracing.open_telemetry_tracer", "create_span"),
    "extract_trace_context": (
        "src.observability.tracing.open_telemetry_tracer",
        "extract_trace_context",
    ),
    "extract_trace_headers": (
        "src.observability.tracing.open_telemetry_tracer",
        "extract_trace_headers",
    ),
    "get_current_span_safe": (
        "src.observability.tracing.open_telemetry_tracer",
        "get_current_span_safe",
    ),
    "get_null_tracer": (
        "src.observability.tracing.open_telemetry_tracer",
        "get_null_tracer",
    ),
    "get_span_exporter": (
        "src.observability.tracing.open_telemetry_tracer",
        "get_span_exporter",
    ),
    "get_tracer": ("src.observability.tracing.open_telemetry_tracer", "get_tracer"),
    "init_tracer": ("src.observability.tracing.open_telemetry_tracer", "init_tracer"),
    "inject_trace_context": (
        "src.observability.tracing.open_telemetry_tracer",
        "inject_trace_context",
    ),
    "is_otel_available": (
        "src.observability.tracing.open_telemetry_tracer",
        "is_otel_available",
    ),
    "log_tracing_disabled_warning": (
        "src.observability.tracing.open_telemetry_tracer",
        "log_tracing_disabled_warning",
    ),
    "otel_import_error_traceback": (
        "src.observability.tracing.open_telemetry_tracer",
        "otel_import_error_traceback",
    ),
    "record_exception": (
        "src.observability.tracing.open_telemetry_tracer",
        "record_exception",
    ),
    "timed_span": ("src.observability.tracing.open_telemetry_tracer", "timed_span"),
    "traced": ("src.observability.tracing.open_telemetry_tracer", "traced"),
}

_loader = ModuleLazyLoader(_LAZY_REGISTRY)


def __getattr__(name: str) -> Any:
    return _loader.load(name)


__all__ = [
    "NullSpan",
    "NullTracer",
    "SpanAttributes",
    "SpanTiming",
    "TRACE_HEADERS",
    "add_span_attributes",
    "add_span_event",
    "contains_trace_headers",
    "create_span",
    "extract_trace_context",
    "extract_trace_headers",
    "get_current_span_safe",
    "get_null_tracer",
    "get_span_exporter",
    "get_tracer",
    "init_tracer",
    "inject_trace_context",
    "is_otel_available",
    "log_tracing_disabled_warning",
    "otel_import_error_traceback",
    "record_exception",
    "timed_span",
    "traced",
]
