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


"""Auto-extracted class from agent.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from src.core.base.models import SpanContext, TelemetrySpan
from contextlib import contextmanager
from typing import List, Optional, Dict, Any
from collections.abc import Iterator
import json
import time
import uuid

__version__ = VERSION

class TelemetryCollector:
    """Collect telemetry data for observability.

    Provides OpenTelemetry - compatible span collection.

    Example:
        collector=TelemetryCollector()

        with collector.span("process_file") as span:
            span.set_attribute("file", "test.py")
            # ... process file ...

        spans=collector.get_spans()
    """

    def __init__(self, service_name: str = "agent") -> None:
        """Initialize collector.

        Args:
            service_name: Service name for tracing.
        """
        self.service_name = service_name
        self._spans: list[TelemetrySpan] = []
        self._current_span: TelemetrySpan | None = None

    @contextmanager
    def span(self, name: str, attributes: dict[str, Any] | None = None) -> Iterator[SpanContext]:
        """Create a telemetry span.

        Args:
            name: Span name.
            attributes: Initial attributes.

        Yields:
            SpanContext for adding attributes and events.
        """
        parent_id = self._current_span.span_id if self._current_span else None
        trace_id = self._current_span.trace_id if self._current_span else str(uuid.uuid4())

        span = TelemetrySpan(
            name=name,
            trace_id=trace_id,
            parent_id=parent_id,
            attributes=attributes or {},
        )

        old_current = self._current_span
        self._current_span = span

        context = SpanContext(span)

        try:
            yield context
        except Exception as e:
            context.add_event("exception", {"message": str(e)})
            raise
        finally:
            span.end_time = time.time()
            self._spans.append(span)
            self._current_span = old_current

    def get_spans(self) -> list[TelemetrySpan]:
        """Get all collected spans."""
        return list(self._spans)

    def export_json(self) -> str:
        """Export spans as JSON.

        Returns:
            JSON string of spans.
        """
        spans_data: list[dict[str, Any]] = []
        for span in self._spans:
            spans_data.append({
                "name": span.name,
                "trace_id": span.trace_id,
                "span_id": span.span_id,
                "parent_id": span.parent_id,
                "start_time": span.start_time,
                "end_time": span.end_time,
                "duration_ms": (span.end_time - span.start_time) * 1000 if span.end_time else None,
                "attributes": span.attributes,
                "events": span.events,
            })
        return json.dumps(spans_data, indent=2)

    def clear(self) -> None:
        """Clear all spans."""
        self._spans.clear()