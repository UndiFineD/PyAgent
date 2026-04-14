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
"""Tests for backend.tracing — OpenTelemetry span instrumentation."""

from __future__ import annotations

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from backend.tracing import _TRACER_NAME, setup_tracing


def test_setup_tracing_returns_tracer():
    exporter = InMemorySpanExporter()
    t = setup_tracing(exporter)
    assert t is not None


def test_span_name_recorded():
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    t = provider.get_tracer(_TRACER_NAME)
    with t.start_as_current_span("my-span"):
        pass
    spans = exporter.get_finished_spans()
    assert len(spans) == 1
    assert spans[0].name == "my-span"


def test_tracer_instrumentation_scope():
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    t = provider.get_tracer(_TRACER_NAME)
    with t.start_as_current_span("scope-check"):
        pass
    spans = exporter.get_finished_spans()
    assert spans[0].instrumentation_scope.name == _TRACER_NAME


def test_tracing_module_singleton_exists():
    from backend import tracing

    assert hasattr(tracing, "tracer")
    assert hasattr(tracing, "setup_tracing")
    assert hasattr(tracing, "_TRACER_NAME")


def test_tracer_name_constant():
    assert _TRACER_NAME == "pyagent.backend"
