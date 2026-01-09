#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from typing import Callable, Optional
import time
import threading

class RetryHelper:
    """Simple retry helper for flaky operations."""

    def __init__(self, max_retries: int = 3, delay_seconds: float = 0.0) -> None:
        self.max_retries = int(max_retries)
        self.delay_seconds = float(delay_seconds)

    def retry(self, fn: Callable[[], T]) -> T:
        last_exc: Optional[BaseException] = None
        for attempt in range(self.max_retries):
            try:
                return fn()
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if attempt == self.max_retries - 1:
                    raise
                if self.delay_seconds > 0:
                    threading.Event().wait(self.delay_seconds)
        if last_exc is not None:
            raise last_exc
        raise RuntimeError("RetryHelper failed without exception")
