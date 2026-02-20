#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# ruff: noqa: F401
# flake8: noqa

"""Lazy-loading entry point for observability.tracing.from __future__ import annotationsfrom typing import Any, TYPE_CHECKING
try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION

try:
    from .core.lazy_loader import ModuleLazyLoader
except ImportError:
    from src.core.lazy_loader import ModuleLazyLoader


if TYPE_CHECKING:
    # ruff: noqa: F401
    from .open_telemetry_tracer import (
        NullSpan, NullTracer, SpanAttributes, SpanTiming, TRACE_HEADERS,
        add_span_attributes, add_span_event, contains_trace_headers,
        create_span, extract_trace_context, extract_trace_headers,
        get_current_span_safe, get_null_tracer, get_span_exporter,
        get_tracer, init_tracer, inject_trace_context, is_otel_available,
        log_tracing_disabled_warning, otel_import_error_traceback,
        record_exception, timed_span, traced
    )

_LAZY_REGISTRY = {
    "NullSpan": ("src.observability.tracing.open_telemetry_tracer", "NullSpan"),"    "NullTracer": ("src.observability.tracing.open_telemetry_tracer", "NullTracer"),"    "SpanAttributes": ("src.observability.tracing.open_telemetry_tracer", "SpanAttributes"),"    "SpanTiming": ("src.observability.tracing.open_telemetry_tracer", "SpanTiming"),"    "TRACE_HEADERS": ("src.observability.tracing.open_telemetry_tracer", "TRACE_HEADERS"),"    "add_span_attributes": ("src.observability.tracing.open_telemetry_tracer", "add_span_attributes"),"    "add_span_event": ("src.observability.tracing.open_telemetry_tracer", "add_span_event"),"    "contains_trace_headers": ("src.observability.tracing.open_telemetry_tracer", "contains_trace_headers"),"    "create_span": ("src.observability.tracing.open_telemetry_tracer", "create_span"),"    "extract_trace_context": ("src.observability.tracing.open_telemetry_tracer", "extract_trace_context"),"    "extract_trace_headers": ("src.observability.tracing.open_telemetry_tracer", "extract_trace_headers"),"    "get_current_span_safe": ("src.observability.tracing.open_telemetry_tracer", "get_current_span_safe"),"    "get_null_tracer": ("src.observability.tracing.open_telemetry_tracer", "get_null_tracer"),"    "get_span_exporter": ("src.observability.tracing.open_telemetry_tracer", "get_span_exporter"),"    "get_tracer": ("src.observability.tracing.open_telemetry_tracer", "get_tracer"),"    "init_tracer": ("src.observability.tracing.open_telemetry_tracer", "init_tracer"),"    "inject_trace_context": ("src.observability.tracing.open_telemetry_tracer", "inject_trace_context"),"    "is_otel_available": ("src.observability.tracing.open_telemetry_tracer", "is_otel_available"),"    "log_tracing_disabled_warning": ("src.observability.tracing.open_telemetry_tracer", "log_tracing_disabled_warning"),"    "otel_import_error_traceback": ("src.observability.tracing.open_telemetry_tracer", "otel_import_error_traceback"),"    "record_exception": ("src.observability.tracing.open_telemetry_tracer", "record_exception"),"    "timed_span": ("src.observability.tracing.open_telemetry_tracer", "timed_span"),"    "traced": ("src.observability.tracing.open_telemetry_tracer", "traced"),"}

_loader = ModuleLazyLoader(_LAZY_REGISTRY)

def __getattr__(name: str) -> Any:
    return _loader.load(name)

__all__ = ["VERSION"] + list(_LAZY_REGISTRY.keys())"

"""
