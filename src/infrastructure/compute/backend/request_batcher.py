#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from .BatchRequest import BatchRequest

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
from src.classes.backend.LocalContextRecorder import LocalContextRecorder

class RequestBatcher:
    """Batches multiple requests for efficient processing.

    Collects requests and processes them together when batch
    size or timeout is reached.

    Example:
        batcher=RequestBatcher(batch_size=10, timeout_s=5.0)
        batcher.add("prompt1")
        batcher.add("prompt2")
        batch=batcher.get_batch()  # Returns when ready
    """

    def __init__(
        self,
        batch_size: int = 10,
        timeout_s: float = 5.0,
        recorder: Optional[LocalContextRecorder] = None,
    ) -> None:
        """Initialize request batcher.

        Args:
            batch_size: Requests per batch.
            timeout_s: Max wait time before processing partial batch.
            recorder: Infrastructure recorder for intelligence harvesting.
        """
        self.batch_size = batch_size
        self.timeout_s = timeout_s
        self.recorder = recorder
        self._buffer: List[str] = []
        self._lock = threading.Lock()
        self._batch_start: Optional[float] = None

    def add(self, prompt: str) -> bool:
        """Add request to current batch.

        Args:
            prompt: Request prompt.

        Returns:
            bool: True if batch is now ready.
        """
        with self._lock:
            if not self._buffer:
                self._batch_start = time.time()
            self._buffer.append(prompt)
            return len(self._buffer) >= self.batch_size

    def is_ready(self) -> bool:
        """Check if batch is ready for processing."""
        with self._lock:
            if len(self._buffer) >= self.batch_size:
                return True
            if self._batch_start and (time.time() - self._batch_start) >= self.timeout_s:
                return bool(self._buffer)
            return False

    def get_batch(self) -> Optional[BatchRequest]:
        """Get current batch and reset buffer.

        Returns:
            Optional[BatchRequest]: Current batch or None if empty.
        """
        with self._lock:
            if not self._buffer:
                return None
            
            if self.recorder:
                self.recorder.record_lesson("batch_created", {"size": len(self._buffer)})
                
            batch = BatchRequest(requests=self._buffer.copy())
            self._buffer.clear()
            self._batch_start = None
            return batch

    def pending_count(self) -> int:
        """Get number of pending requests."""
        with self._lock:
            return len(self._buffer)
