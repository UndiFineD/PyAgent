#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from .QueuedRequest import QueuedRequest
from .RequestPriority import RequestPriority

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from queue import PriorityQueue
from typing import Any, Callable, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import os
import re
import subprocess
import threading
import time
import uuid

# Infrastructure
from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder

class RequestQueue:
    """Priority queue for backend requests.

    Manages request ordering by priority and timestamp.
    Thread - safe for concurrent access.

    Example:
        queue=RequestQueue()
        queue.enqueue("prompt", RequestPriority.HIGH)
        request=queue.dequeue()
    """

    def __init__(self, max_size: int = 1000, recorder: Optional[LocalContextRecorder] = None) -> None:
        """Initialize request queue.

        Args:
            max_size: Maximum queue size.
            recorder: Infrastructure recorder for intelligence harvesting.
        """
        self._queue: PriorityQueue[QueuedRequest] = PriorityQueue(maxsize=max_size)
        self.recorder = recorder
        self._lock = threading.Lock()
        self._pending: Dict[str, QueuedRequest] = {}

    def enqueue(
        self,
        prompt: str,
        priority: RequestPriority = RequestPriority.NORMAL,
        callback: Optional[Callable[[str], None]] = None,
    ) -> str:
        """Add request to queue.

        Args:
            prompt: The prompt to queue.
            priority: Request priority level.
            callback: Optional callback when processed.

        Returns:
            str: Request ID for tracking.
        """
        request_id = str(uuid.uuid4())
        request = QueuedRequest(
            priority=priority.value,
            timestamp=time.time(),
            request_id=request_id,
            prompt=prompt,
            callback=callback,
        )

        with self._lock:
            self._queue.put(request)
            self._pending[request_id] = request
            
        if self.recorder:
            self.recorder.record_lesson("request_queued", {"id": request_id, "priority": priority.name})
            
        logging.debug(f"Queued request {request_id} with priority {priority.name}")
        return request_id

    def dequeue(self, timeout: Optional[float] = None) -> Optional[QueuedRequest]:
        """Get next request from queue.

        Args:
            timeout: Maximum wait time in seconds.

        Returns:
            Optional[QueuedRequest]: Next request or None if empty / timeout.
        """
        try:
            request = self._queue.get(timeout=timeout)
            with self._lock:
                self._pending.pop(request.request_id, None)
            return request
        except Exception:
            return None

    def size(self) -> int:
        """Get current queue size."""
        return self._queue.qsize()

    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self._queue.empty()

    def get_pending(self, request_id: str) -> Optional[QueuedRequest]:
        """Get pending request by ID."""
        with self._lock:
            return self._pending.get(request_id)
