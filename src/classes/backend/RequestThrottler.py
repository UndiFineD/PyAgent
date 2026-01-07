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

class RequestThrottler:
    """Throttles requests to prevent overloading backends.

    Implements token bucket algorithm for rate limiting.

    Example:
        throttler=RequestThrottler(requests_per_second=10)
        if throttler.allow_request("github-models"):
            make_request()
        else:
            wait_or_queue()
    """

    def __init__(
        self,
        requests_per_second: float = 10.0,
        burst_size: int = 20,
    ) -> None:
        """Initialize request throttler.

        Args:
            requests_per_second: Sustained request rate.
            burst_size: Maximum burst size.
        """
        self.requests_per_second = requests_per_second
        self.burst_size = burst_size
        self._buckets: Dict[str, float] = {}  # backend -> tokens
        self._last_update: Dict[str, float] = {}
        self._lock = threading.Lock()

    def allow_request(self, backend: str) -> bool:
        """Check if request is allowed.

        Args:
            backend: Backend identifier.

        Returns:
            bool: True if request is allowed.
        """
        with self._lock:
            now = time.time()

            # Initialize bucket if needed
            if backend not in self._buckets:
                self._buckets[backend] = float(self.burst_size)
                self._last_update[backend] = now

            # Replenish tokens
            elapsed = now - self._last_update[backend]
            self._buckets[backend] = min(
                self.burst_size,
                self._buckets[backend] + elapsed * self.requests_per_second
            )
            self._last_update[backend] = now

            # Check if token available
            if self._buckets[backend] >= 1.0:
                self._buckets[backend] -= 1.0
                return True

            return False

    def wait_for_token(self, backend: str, timeout: float = 10.0) -> bool:
        """Wait for a token to become available.

        Args:
            backend: Backend identifier.
            timeout: Maximum wait time.

        Returns:
            bool: True if token acquired.
        """
        start = time.time()

        while time.time() - start < timeout:
            if self.allow_request(backend):
                return True
            time.sleep(0.1)

        return False

    def get_status(self, backend: str) -> Dict[str, Any]:
        """Get throttle status for backend.

        Args:
            backend: Backend identifier.

        Returns:
            Dict: Throttle status.
        """
        with self._lock:
            tokens = self._buckets.get(backend, self.burst_size)
            return {
                "available_tokens": tokens,
                "max_tokens": self.burst_size,
                "requests_per_second": self.requests_per_second,
            }
