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
Simple telemetry collector used by tests.

"""
This module provides a minimal in-process span collector. Tests only require the
class to exist and basic methods, so this is intentionally lightweight.
"""
import json
import time
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TelemetrySpan:
    name: str
    trace_id: str
    parent_id: str | None
    attributes: dict[str, Any] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    span_id: str = field(default_factory=lambda: str(uuid.uuid4()))


class SpanContext:
    def __init__(self, span: TelemetrySpan) -> None:
        self._span = span

    def set_attribute(self, key: str, value: Any) -> None:
        self._span.attributes[key] = value

    def add_event(self, name: str, payload: dict[str, Any]) -> None:
        self._span.events.append({"name": name, "payload": payload})


class TelemetryCollector:
    ""
Collect telemetry data for observability (minimal).""
def __init__(self, service_name: str = "agent") -> None:
        self.service_name = service_name
        self._spans: list[TelemetrySpan] = []
        self._current_span: TelemetrySpan | None = None

    @contextmanager
    def span(self, name: str, attributes: dict[str, Any] | None = None) -> Iterator[SpanContext]:
        parent_id = self._current_span.span_id if self._current_span else None
        trace_id = self._current_span.trace_id if self._current_span else str(uuid.uuid4())

        span = TelemetrySpan(name=name, trace_id=trace_id, parent_id=parent_id, attributes=attributes or {})
        old_current = self._current_span
        self._current_span = span
        context = SpanContext(span)
        try:
            yield context
        except Exception as e:  # pylint: disable=broad-exception-caught
            context.add_event("exception", {"message": str(e)})
            raise
        finally:
            span.end_time = time.time()
            self._spans.append(span)
            self._current_span = old_current

    def get_spans(self) -> list[TelemetrySpan]:
        return list(self._spans)

    def export_json(self) -> str:
        spans_data: list[dict[str, Any]] = []
        for span in self._spans:
            spans_data.append(
                {
                    "name": span.name,
                    "trace_id": span.trace_id,
                    "span_id": span.span_id,
                    "parent_id": span.parent_id,
                    "start_time": span.start_time,
                    "end_time": span.end_time,
                    "duration_ms": (span.end_time - span.start_time) * 1000 if span.end_time else None,
                    "attributes": span.attributes,
                    "events": span.events,
                }
            )
        return json.dumps(spans_data, indent=2)

    def clear(self) -> None:
        self._spans.clear()
