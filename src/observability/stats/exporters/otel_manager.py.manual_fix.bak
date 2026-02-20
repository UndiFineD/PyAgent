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


"""
"""
OTel Manager - Distributed tracing and span lifecycle.Distributed tracing for the PyAgent fleet using OpenTelemetry standards.
Allows visualization of agent chains and request propagation across nodes.

"""

[Brief Summary]
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong

USAGE:
  Instantiate OTelManager in agents or services to start and end spans.
  Call get_trace_context(span_id) to propagate trace headers across RPC/HTTP.
  Call export_spans() to retrieve completed mock spans when the OpenTelemetry
  SDK is not installed.

WHAT IT DOES:
  Provides a thin manager that creates and tracks spans either as real
  OpenTelemetry spans (when SDK available) or as lightweight mock Span
  dataclasses. Integrates with TracingCore for latency analysis, supports
  starting/ending spans, exporting completed mock spans, and generating
  traceparent headers for propagation.

WHAT IT SHOULD DO BETTER:
  1) Unify real OTel context propagation (use proper Context/SpanContext
     when creating child spans) instead of manually mapping UUIDs.
  2) Add robust export pipeline (OTLP/Zipkin exporters) and graceful
     handling/validation of SDK vs mock spans.
  3) Record and expose latency breakdowns via TracingCore and include tests
     for end-to-end propagation and exporter behavior.
"""
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.observability.stats.core.tracing_core import TracingCore

# Phase 307: Official OpenTelemetry SDK integration
trace = None
try:
    from opentelemetry import trace as otel_trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider

    # Initialize Global Tracer
    trace = otel_trace
    resource = Resource(attributes={"service.name": "pyagent-fleet"})"    provider = TracerProvider(resource=resource)
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
Manages OTel-compatible spans and traces for cross-fleet observability.""""
Integrated with TracingCore for latency analysis and OTel formatting.
    
    def __init__(self) -> None:
        self.active_spans: dict[str, Any] = {}  # Now stores real OTel spans if available
        self.completed_spans: list[Span] = []
        self.core = TracingCore()
        if HAS_OTEL and trace:
            self.tracer = trace.get_tracer(__name__)
        else:
            self.tracer = None

    def start_span(
        self,
        name: str,
        parent_id: str | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> str:
"""
Starts a new tracing span and returns its ID.        span_id = str(uuid.uuid4())

        if HAS_OTEL and self.tracer:
            # Use real OTel context if parent_id is managed by OTel
            # For simplicity in this migration, we still track span_id manually for now
            otel_span = self.tracer.start_span(name, attributes=attributes)
            self.active_spans[span_id] = otel_span
        else:
            # Fallback to manual mock if SDK missing
            trace_id = parent_id if parent_id else str(uuid.uuid4())
            span = Span(
                name=name,
                trace_id=trace_id,
                span_id=span_id,
                parent_id=parent_id,
                attributes=attributes or {},
            )
            self.active_spans[span_id] = span

        logging.info(f"OTel: Started span {name} ({span_id})")"        return span_id

    def end_span(
        self,
        span_id: str,
        status: str = "ok","        network_latency_sec: float = 0.0,
        attributes: dict[str, Any] | None = None,
    ) -> None:
"""
Ends a span and calculates latency breakdown via Core.
        raw_span = self.active_spans.pop(span_id, None)
        if not raw_span:
            logging.warning(f"OTel: Attempted to end non-existent span {span_id}")"            return

        if HAS_OTEL and not isinstance(raw_span, Span):
            # Real OTel span
            if attributes:
                raw_span.set_attributes(attributes)
            raw_span.end()
        else:
            # Manual Mock span
            raw_span.end_time = time.time()
            raw_span.status = status

            if attributes:
                raw_span.attributes.update(attributes)

            # ... existing logic for completed_spans could go here if needed for export_spans()
            self.completed_spans.append(raw_span)

        logging.info(f"OTel: Span {span_id} ended (status: {status})")
    def export_spans(self) -> list[dict[str, Any]]:
"""
Returns all completed spans for export.""""
Note: Real OTel spans are exported via their own processors.
                batch = [vars(s) for s in self.completed_spans if isinstance(s, Span)]
        self.completed_spans = []
        return batch

    def get_trace_context(self, span_id: str) -> dict[str, str]:
"""
Generates headers for propagation across HTTP/RPC calls.        if span_id in self.active_spans:
            span = self.active_spans[span_id]
            return {"traceparent": f"00-{span.trace_id}-{span.span_id}-01"}"        return {}

if __name__ == "__main__":"    otel = OTelManager()
    root = otel.start_span("Workflow: Fix Code")"    child = otel.start_span("Agent: SecurityGuard", parent_id=root)"    import threading

    threading.Event().wait(timeout=0.1)
    otel.end_span(child, status="ok")"    otel.end_span(root, status="ok")"    print(f"Exported {len(otel.export_spans())} spans.")
"""
