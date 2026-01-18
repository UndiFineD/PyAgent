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


"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .RequestContext import RequestContext
from .RequestPriority import RequestPriority
from typing import Dict, List, Optional
import logging
import threading
import time
import uuid

__version__ = VERSION

class RequestTracer:
    """Traces requests with correlation IDs.

    Provides distributed tracing capabilities for debugging
    and monitoring request flow.

    Example:
        tracer=RequestTracer()
        context=tracer.start_trace("my-request")
        # Do work
        tracer.end_trace(context.request_id, success=True)
    """

    def __init__(self) -> None:
        """Initialize request tracer."""
        self._traces: dict[str, RequestContext] = {}
        self._lock = threading.Lock()

    def start_trace(
        self,
        description: str,
        correlation_id: str | None = None,
        priority: RequestPriority = RequestPriority.NORMAL,
    ) -> RequestContext:
        """Start a new trace.

        Args:
            description: Trace description.
            correlation_id: Optional correlation ID for linking traces.
            priority: Request priority.

        Returns:
            RequestContext: Context for this trace.
        """
        context = RequestContext(
            correlation_id=correlation_id or str(uuid.uuid4()),
            priority=priority,
            metadata={"description": description},
        )

        with self._lock:
            self._traces[context.request_id] = context

        logging.debug(f"Started trace {context.request_id} (correlation: {context.correlation_id})")
        return context

    def end_trace(
        self,
        request_id: str,
        success: bool,
        response_size: int = 0,
    ) -> float | None:
        """End a trace and return duration.

        Args:
            request_id: Request ID to end.
            success: Whether request succeeded.
            response_size: Size of response.

        Returns:
            Optional[float]: Duration in seconds, or None if not found.
        """
        with self._lock:
            context = self._traces.pop(request_id, None)
        if not context:
            return None

        duration = time.time() - context.created_at
        logging.debug(
            f"Ended trace {request_id}: success={success}, "
            f"duration={duration:.3f}s, size={response_size}"
        )
        return duration

    def get_active_traces(self) -> list[RequestContext]:
        """Get all active traces."""
        with self._lock:
            return list(self._traces.values())