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

class CircuitBreaker:
    """Circuit breaker pattern for failing backends.

    Tracks failures per backend and temporarily disables them if they exceed
    a failure threshold. Prevents cascading failures and wasted retries.

    States:
    - CLOSED: Normal operation, requests go through
    - OPEN: Too many failures, requests rejected immediately
    - HALF_OPEN: Recovery attempt, one request allowed

    Example:
        breaker=CircuitBreaker(failure_threshold=3, recovery_timeout=60)
        if breaker.is_open():
            print("Backend is currently unavailable")
        else:
            try:
                result=call_backend()
                breaker.record_success()
            except Exception:
                breaker.record_failure()
    """

    def __init__(
        self,
        name: str = "default",
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            name: Name for this breaker (e.g., 'github-models', 'copilot').
            failure_threshold: Number of failures before opening circuit.
            recovery_timeout: Seconds to wait before attempting recovery.
        """
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = "CLOSED"  # CLOSED, OPEN, or HALF_OPEN

    def is_open(self) -> bool:
        """Check if circuit is open (backend should be skipped)."""
        if self.state == "CLOSED":
            return False
        if self.state == "OPEN":
            # Check if recovery timeout has elapsed
            if self.last_failure_time is None:
                return True
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = "HALF_OPEN"
                logging.info(f"Circuit breaker '{self.name}' attempting recovery (HALF_OPEN)")
                return False
            return True
        # HALF_OPEN
        return False

    def record_success(self) -> None:
        """Record a successful request."""
        self.failure_count = 0
        self.success_count += 1
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            logging.info(f"Circuit breaker '{self.name}' recovered (CLOSED)")

    def record_failure(self) -> None:
        """Record a failed request."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logging.warning(
                f"Circuit breaker '{self.name}' opened after {self.failure_count} failures"
            )
