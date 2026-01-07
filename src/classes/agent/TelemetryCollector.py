#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from .SpanContext import SpanContext
from .TelemetrySpan import TelemetrySpan

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from types import TracebackType
from typing import List, Set, Optional, Dict, Any, Callable, Iterable, TypeVar, cast, Final
import argparse
import asyncio
import difflib
import fnmatch
import functools
import hashlib
import importlib.util
import json
import logging
import os
import signal
import subprocess
import sys
import threading
import time
import uuid

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
        self._spans: List[TelemetrySpan] = []
        self._current_span: Optional[TelemetrySpan] = None

    @contextmanager
    def span(self, name: str, attributes: Optional[Dict[str, Any]] = None):
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

    def get_spans(self) -> List[TelemetrySpan]:
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
