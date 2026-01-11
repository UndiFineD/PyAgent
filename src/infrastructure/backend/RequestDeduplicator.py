#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

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

class RequestDeduplicator:
    """Deduplicates concurrent requests with identical prompts.

    Prevents redundant API calls when multiple threads / processes
    send the same request simultaneously.

    Example:
        dedup=RequestDeduplicator()
        if dedup.is_duplicate("prompt"):
            result=dedup.wait_for_result("prompt")
        else:
            result=call_api("prompt")
            dedup.store_result("prompt", result)
    """

    def __init__(self, ttl_seconds: float = 60.0, recorder: Optional[LocalContextRecorder] = None) -> None:
        """Initialize deduplicator.

        Args:
            ttl_seconds: Time - to - live for pending requests.
            recorder: Interaction recorder for logic harvesting.
        """
        self.ttl_seconds = ttl_seconds
        self.recorder = recorder
        self._pending: Dict[str, float] = {}  # hash -> start_time
        self._results: Dict[str, str] = {}
        self._lock = threading.Lock()
        self._events: Dict[str, threading.Event] = {}

    def _get_key(self, prompt: str) -> str:
        """Generate deduplication key for prompt."""
        return hashlib.sha256(prompt.encode()).hexdigest()[:16]

    def is_duplicate(self, prompt: str) -> bool:
        """Check if request is a duplicate of a pending request.

        Args:
            prompt: Request prompt.

        Returns:
            bool: True if duplicate request is in progress.
        """
        key = self._get_key(prompt)
        now = time.time()

        with self._lock:
            # Clean expired entries
            expired = [k for k, t in self._pending.items() if now - t > self.ttl_seconds]
            for k in expired:
                self._pending.pop(k, None)
                self._events.pop(k, None)
                self._results.pop(k, None)

            if key in self._pending:
                if self.recorder:
                    self.recorder.record_lesson("duplicate_detected", {"hash": key})
                return True

            # Mark as pending
            self._pending[key] = now
            self._events[key] = threading.Event()
            return False

    def wait_for_result(self, prompt: str, timeout: float = 60.0) -> Optional[str]:
        """Wait for result of duplicate request.

        Args:
            prompt: Request prompt.
            timeout: Maximum wait time.

        Returns:
            Optional[str]: Result or None if timeout.
        """
        key = self._get_key(prompt)

        with self._lock:
            event = self._events.get(key)

        if event:
            event.wait(timeout=timeout)

        with self._lock:
            return self._results.get(key)

    def store_result(self, prompt: str, result: str) -> None:
        """Store result and notify waiters.

        Args:
            prompt: Request prompt.
            result: Request result.
        """
        key = self._get_key(prompt)

        with self._lock:
            self._results[key] = result
            self._pending.pop(key, None)
            event = self._events.get(key)
            if event:
                event.set()
