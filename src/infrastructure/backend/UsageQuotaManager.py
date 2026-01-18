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
from src.core.base.Version import VERSION
from .UsageQuota import UsageQuota
from typing import Any
import threading
import time

__version__ = VERSION


class UsageQuotaManager:
    """Manages usage quotas and limits.

    Tracks request counts and enforces daily / hourly limits.

    Example:
        quota=UsageQuotaManager(daily_limit=1000, hourly_limit=100)
        if quota.can_request():
            quota.record_request()
            # Make request
    """

    def __init__(
        self,
        daily_limit: int = 1000,
        hourly_limit: int = 100,
    ) -> None:
        """Initialize quota manager.

        Args:
            daily_limit: Max requests per day.
            hourly_limit: Max requests per hour.
        """
        self._quota = UsageQuota(
            daily_limit=daily_limit,
            hourly_limit=hourly_limit,
        )
        self._lock = threading.Lock()

    def _check_reset(self) -> None:
        """Check and reset counters if needed."""
        now = time.time()
        # Reset hourly
        if now - self._quota.reset_hourly_at >= 3600:
            self._quota.current_hourly = 0
            self._quota.reset_hourly_at = now
        # Reset daily
        if now - self._quota.reset_daily_at >= 86400:
            self._quota.current_daily = 0
            self._quota.reset_daily_at = now

    def can_request(self) -> bool:
        """Check if request is allowed under quota."""
        with self._lock:
            self._check_reset()
            return (
                self._quota.current_daily < self._quota.daily_limit
                and self._quota.current_hourly < self._quota.hourly_limit
            )

    def record_request(self) -> None:
        """Record a request against quota."""
        with self._lock:
            self._check_reset()
            self._quota.current_daily += 1
            self._quota.current_hourly += 1

    def get_remaining(self) -> tuple[int, int]:
        """Get remaining quota (daily, hourly)."""
        with self._lock:
            self._check_reset()
            daily_remaining = max(
                0, self._quota.daily_limit - self._quota.current_daily
            )
            hourly_remaining = max(
                0, self._quota.hourly_limit - self._quota.current_hourly
            )
            return daily_remaining, hourly_remaining

    def get_usage_report(self) -> dict[str, Any]:
        """Get usage report."""
        with self._lock:
            self._check_reset()
            return {
                "daily_used": self._quota.current_daily,
                "daily_limit": self._quota.daily_limit,
                "daily_remaining": max(
                    0, self._quota.daily_limit - self._quota.current_daily
                ),
                "hourly_used": self._quota.current_hourly,
                "hourly_limit": self._quota.hourly_limit,
                "hourly_remaining": max(
                    0, self._quota.hourly_limit - self._quota.current_hourly
                ),
            }
