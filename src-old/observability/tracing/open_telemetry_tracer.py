#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/observability/tracing/open_telemetry_tracer.description.md

# Description: src/observability/tracing/open_telemetry_tracer.py

Module overview:
- Implements OpenTelemetry integration and fallback behavior when OTEL packages are not installed.
- Defines standardized `SpanAttributes` names for GenAI operations and various helpers to create, inject, extract, and manage spans.
- Provides context managers (`create_span`), decorators (`traced`), tracer initialization (`init_tracer`), and utilities for exporters.

Primary classes and APIs:
- `SpanAttributes` (class): constant names for span attributes.
- `is_otel_available()`, `init_tracer()`, `get_span_exporter()`, `create_span()`, `traced()` and propagation helpers.

Behavioral notes:
- Attempts to import OpenTelemetry at module import and records traceback if unavailable.
- Gracefully yields None spans or no-op behaviors when OTEL is not installed.
## Source: src-old/observability/tracing/open_telemetry_tracer.improvements.md

# Improvements: src/observability/tracing/open_telemetry_tracer.py

Potential improvements:
- Add unit tests for `create_span`, `traced`, and propagation helpers that run in both OTEL-available and OTEL-missing environments (use monkeypatch to simulate availability).
- Split into smaller modules (`attributes`, `tracer`, `propagation`, `decorators`) for maintainability and faster import times.
- Document expected shapes for attributes dictionaries and context objects.
- Provide clear fallbacks and no-op tracers so instrumentation code can assume a tracer is always present.
- Add integration tests that validate exporters using a local OTLP collector (or a mock) to ensure export paths work.
- Consider improving performance by lazy-importing heavy OTEL packages only when `init_tracer` is invoked.
- Add type hints and mypy-friendly stubs for OpenTelemetry types to improve developer experience.

LLM_CONTEXT_END
"""
from __future__ import annotations


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
OpenTelemetry Tracing Module - Phase 20: Production Infrastructure
===================================================================

Distributed tracing with OpenTelemetry integration for PyAgent.
This module provides:
- Standardized span attribute names for LLM operations
- Trace context extraction and propagation utilities
- OTLP exporter support (gRPC and HTTP)
- Graceful fallback when OpenTelemetry is not installed
- Span context managers and decorators
- Custom span processors

This module is required for Phase 315 documentation parity.

Author: PyAgent Phase 20
"""


import functools
import logging
import os
import time
from collections.abc import Callable, Generator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, ParamSpec, TypeVar

logger = logging.getLogger(__name__)

# Standard trace headers
TRACE_HEADERS: list[str] = ["traceparent", "tracestate"]

# Track if OpenTelemetry and Rust core are available
_is_otel_imported = False
HAS_RUST = False
otel_import_error_traceback: str | None = None


try:
    from opentelemetry import trace  # pylint: disable=unused-import
    from opentelemetry.context.context import Context
    from opentelemetry.sdk.environment_variables import OTEL_EXPORTER_OTLP_TRACES_PROTOCOL
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor, SpanExporter
    from opentelemetry.trace import (
        Span,
        SpanKind,
        Status,
        StatusCode,
        Tracer,
        get_current_span,
        get_tracer_provider,
        set_tracer_provider,
    )
    from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

    _is_otel_imported = True
except ImportError:
    import traceback
    otel_import_error_traceback = traceback.format_exc()

try:
    import rust_core as rc  # type: ignore
    HAS_RUST = True
except ImportError:
    rc = None # type: ignore


P = ParamSpec("P")
T = TypeVar("T")


# ============================================================================
# Span Attributes (Standard names for LLM operations)
# ============================================================================
class SpanAttributes:
    """
    """
