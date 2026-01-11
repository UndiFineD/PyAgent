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
from src.core.base.CircuitBreaker import CircuitBreaker as CircuitBreakerImpl

class CircuitBreaker:
    """Circuit breaker pattern for failing backends.

    Tracks failures per backend and temporarily disables them if they exceed
    a failure threshold. Prevents cascading failures and wasted retries.
    Shell for CircuitBreakerImpl.

    States:
    - CLOSED: Normal operation, requests go through
    - OPEN: Too many failures, requests rejected immediately
    - HALF_OPEN: Recovery attempt, one request allowed
    """

    def __init__(
        self,
        name: str = "default",
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
    ) -> None:
        """Initialize circuit breaker."""
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = "CLOSED"  # CLOSED, OPEN, or HALF_OPEN
        self.impl = CircuitBreakerImpl(name=name, failure_threshold=failure_threshold, recovery_timeout=recovery_timeout)

    def is_open(self) -> bool:
        return self.impl.state == "OPEN"

    def call(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        return self.impl.call(func, *args, **kwargs)

    def on_success(self) -> None:
        self.impl.on_success()
        self.state = self.impl.state
        self.failure_count = self.impl.failure_count

    def on_failure(self) -> None:
        self.impl.on_failure()
        self.state = self.impl.state
        self.failure_count = self.impl.failure_count
        self.last_failure_time = self.impl.last_failure_time
