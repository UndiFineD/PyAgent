#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from .UsageRecord import UsageRecord

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

class SystemAnalytics:
    """Collects and reports backend usage analytics.

    Tracks usage patterns, performance metrics, and costs.

    Example:
        analytics=SystemAnalytics()
        analytics.record_usage("github-models", tokens=500, latency_ms=150)

        report=analytics.generate_report()
        print(report["total_tokens"])
    """

    def __init__(self, retention_hours: int = 24) -> None:
        """Initialize backend analytics.

        Args:
            retention_hours: Hours to retain records.
        """
        self.retention_hours = retention_hours
        self._records: List[UsageRecord] = []
        self._lock = threading.Lock()

    def record_usage(
        self,
        backend: str,
        tokens: int = 0,
        latency_ms: int = 0,
        success: bool = True,
        cost_estimate: float = 0.0,
    ) -> UsageRecord:
        """Record a usage event.

        Args:
            backend: Backend used.
            tokens: Tokens consumed.
            latency_ms: Request latency.
            success: Whether successful.
            cost_estimate: Estimated cost.

        Returns:
            UsageRecord: The recorded usage.
        """
        record = UsageRecord(
            timestamp=time.time(),
            backend=backend,
            tokens_used=tokens,
            latency_ms=latency_ms,
            success=success,
            cost_estimate=cost_estimate,
        )

        with self._lock:
            self._records.append(record)
            self._cleanup_old_records()

        return record

    def _cleanup_old_records(self) -> None:
        """Remove records older than retention period."""
        cutoff = time.time() - (self.retention_hours * 3600)
        self._records = [r for r in self._records if r.timestamp >= cutoff]

    def generate_report(self, backend: Optional[str] = None) -> Dict[str, Any]:
        """Generate usage report.

        Args:
            backend: Filter by backend (optional).

        Returns:
            Dict[str, Any]: Usage report.
        """
        with self._lock:
            records = self._records.copy()

        if backend:
            records = [r for r in records if r.backend == backend]

        if not records:
            return {
                "total_requests": 0,
                "total_tokens": 0,
                "total_cost": 0.0,
                "success_rate": 0.0,
                "avg_latency_ms": 0.0,
            }

        total_requests = len(records)
        total_tokens = sum(r.tokens_used for r in records)
        total_cost = sum(r.cost_estimate for r in records)
        successes = sum(1 for r in records if r.success)
        success_rate = successes / total_requests if total_requests > 0 else 0.0
        avg_latency = sum(r.latency_ms for r in records) / total_requests

        return {
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "success_rate": success_rate,
            "avg_latency_ms": avg_latency,
            "by_backend": self._group_by_backend(records),
        }

    def _group_by_backend(self, records: List[UsageRecord]) -> Dict[str, Dict[str, Any]]:
        """Group records by backend."""
        by_backend: Dict[str, List[UsageRecord]] = {}
        for r in records:
            if r.backend not in by_backend:
                by_backend[r.backend] = []
            by_backend[r.backend].append(r)

        return {
            backend: {
                "requests": len(recs),
                "tokens": sum(r.tokens_used for r in recs),
                "avg_latency_ms": sum(r.latency_ms for r in recs) / len(recs) if recs else 0,
            }
            for backend, recs in by_backend.items()
        }
