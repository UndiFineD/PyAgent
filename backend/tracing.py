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
"""OpenTelemetry tracing setup for the PyAgent FastAPI backend."""
from __future__ import annotations

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SpanExporter

_TRACER_NAME = "pyagent.backend"


def setup_tracing(exporter: SpanExporter | None = None) -> trace.Tracer:
    """Configure a TracerProvider and return a named tracer.

    Args:
        exporter: Optional span exporter. Defaults to ConsoleSpanExporter.
                  Pass an InMemorySpanExporter + SimpleSpanProcessor in tests.

    Returns:
        A :class:`opentelemetry.trace.Tracer` scoped to ``pyagent.backend``.

    """
    provider = TracerProvider()
    span_exporter: SpanExporter = exporter if exporter is not None else ConsoleSpanExporter()
    provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(provider)
    return trace.get_tracer(_TRACER_NAME)


tracer: trace.Tracer = setup_tracing()
