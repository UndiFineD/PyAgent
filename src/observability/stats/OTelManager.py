#!/usr/bin/env python3
from __future__ import annotations
"""Distributed tracing for the PyAgent fleet using OpenTelemetry standards.
Allows visualization of agent chains and request propagation across nodes.
"""

import logging
import time
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class Span:
    name: str
    trace_id: str
    span_id: str
    parent_id: Optional[str] = None
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    status: str = "unset"

class OTelManager:
    """Manages OTel-compatible spans and traces for cross-fleet observability."""
    
    def __init__(self) -> None:
        self.active_spans: Dict[str, Span] = {}
        self.completed_spans: List[Span] = []

    def start_span(self, name: str, parent_id: Optional[str] = None, attributes: Optional[Dict[str, Any]] = None) -> str:
        """Starts a new tracing span and returns its ID."""
        span_id = str(uuid.uuid4())
        trace_id = parent_id if parent_id else str(uuid.uuid4()) # Simplifying trace_id propagation
        
        span = Span(
            name=name,
            trace_id=trace_id,
            span_id=span_id,
            parent_id=parent_id,
            attributes=attributes or {}
        )
        self.active_spans[span_id] = span
        logging.info(f"OTel: Started span {name} ({span_id})")
        return span_id

    def end_span(self, span_id: str, status: str = "ok", attributes: Optional[Dict[str, Any]] = None) -> None:
        """Ends a span and records its duration."""
        if span_id not in self.active_spans:
            logging.warning(f"OTel: Attempted to end non-existent span {span_id}")
            return
            
        span = self.active_spans.pop(span_id)
        span.end_time = time.time()
        span.status = status
        if attributes:
            span.attributes.update(attributes)
            
        self.completed_spans.append(span)
        duration = (span.end_time - span.start_time) * 1000
        logging.info(f"OTel: Ended span {span.name} in {duration:.2f}ms")

    def export_spans(self) -> List[Dict[str, Any]]:
        """Returns all completed spans for export to Jaeger or Honeycomb."""
        batch = [vars(s) for s in self.completed_spans]
        self.completed_spans = []
        return batch

    def get_trace_context(self, span_id: str) -> Dict[str, str]:
        """Generates headers for propagation across HTTP/RPC calls."""
        if span_id in self.active_spans:
            span = self.active_spans[span_id]
            return {
                "traceparent": f"00-{span.trace_id}-{span.span_id}-01"
            }
        return {}

if __name__ == "__main__":
    otel = OTelManager()
    root = otel.start_span("Workflow: Fix Code")
    child = otel.start_span("Agent: SecurityGuard", parent_id=root)
    import threading
    threading.Event().wait(timeout=0.1)
    otel.end_span(child, status="ok")
    otel.end_span(root, status="ok")
    print(f"Exported {len(otel.export_spans())} spans.")
