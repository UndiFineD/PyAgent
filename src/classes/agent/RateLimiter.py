#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from .RateLimitConfig import RateLimitConfig

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

class RateLimiter:
    """Rate limiter for API calls using token bucket algorithm.

    Manages API call rate to prevent throttling and ensure fair usage.
    Supports multiple strategies and configurable limits.

    Attributes:
        config: Rate limiting configuration.
        tokens: Current number of available tokens.
        last_refill: Timestamp of last token refill.
    """

    def __init__(self, config: Optional[RateLimitConfig] = None) -> None:
        """Initialize the rate limiter.

        Args:
            config: Rate limiting configuration. Uses defaults if not provided.
        """
        self.config = config or RateLimitConfig()
        self.tokens = float(self.config.burst_size)
        self.last_refill = time.time()
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._request_timestamps: List[float] = []

    def _refill_tokens(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        refill_amount = elapsed * self.config.requests_per_second
        self.tokens = min(float(self.config.burst_size), self.tokens + refill_amount)
        self.last_refill = now

    def acquire(self, timeout: Optional[float] = None) -> bool:
        """Acquire a token for making an API call.

        Blocks until a token is available or timeout expires.

        Args:
            timeout: Maximum time to wait for a token. None=wait forever.

        Returns:
            bool: True if token acquired, False if timeout.
        """
        start_time = time.time()

        with self._condition:
            while True:
                self._refill_tokens()

                if self.tokens >= 1.0:
                    self.tokens -= 1.0
                    self._request_timestamps.append(time.time())
                    # Clean old timestamps
                    cutoff = time.time() - 60
                    self._request_timestamps = [
                        t for t in self._request_timestamps if t > cutoff
                    ]
                    return True

                # Calculate wait time for at least 1 token
                wait_time = (1.0 - self.tokens) / self.config.requests_per_second

                # Check timeout
                elapsed = time.time() - start_time
                if timeout is not None:
                    if elapsed >= timeout:
                        return False
                    wait_time = min(wait_time, timeout - elapsed)

                # Wait before retry using condition, avoiding blocking sleep
                self._condition.wait(timeout=max(wait_time, 0.01))

    def get_stats(self) -> Dict[str, Any]:
        """Get rate limiter statistics.

        Returns:
            Dict with current tokens, request count, etc.
        """
        with self._lock:
            return {
                "tokens_available": self.tokens,
                "requests_last_minute": len(self._request_timestamps),
                "requests_per_second": self.config.requests_per_second,
                "burst_size": self.config.burst_size,
            }
