#!/usr/bin/env python3
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

"""
OpenTelemetry Tracing Package - Phase 20
=========================================

Distributed tracing with OpenTelemetry integration.
"""

from .open_telemetry_tracer import (  # noqa: F401
    # Constants; Availability check; Initialization; Context propagation;
    # Span creation; Span helpers; Timing; Logging; Testing
    TRACE_HEADERS, NullSpan, NullTracer, SpanAttributes, SpanTiming,
    add_span_attributes, add_span_event, contains_trace_headers, create_span,
    extract_trace_context, extract_trace_headers, get_current_span_safe,
    get_null_tracer, get_span_exporter, get_tracer, init_tracer,
    inject_trace_context, is_otel_available, log_tracing_disabled_warning,
    otel_import_error_traceback, record_exception, timed_span, traced)

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
