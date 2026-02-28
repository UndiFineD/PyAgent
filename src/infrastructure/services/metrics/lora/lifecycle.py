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

# SPDX-License-Identifier: Apache-2.0
"""
LoRA Request Lifecycle - Detailed tracking of per-request events and timing.
"""

from __future__ import annotations

import threading
import time
from typing import Any, Dict, List, Optional, Tuple

from src.infrastructure.services.metrics.lora.types import RequestStatus


class RequestLifecycle:
    """
    Enhanced request lifecycle tracking.
    """

    def __init__(
        self,
        request_id: str,
        prompt_tokens: int = 0,
        max_tokens: int = 0,
        lora_adapter: Optional[str] = None,
    ):
        self.request_id = request_id
        self.prompt_tokens = prompt_tokens
        self.max_tokens = max_tokens
        self.lora_adapter = lora_adapter

        self._status = RequestStatus.WAITING
        self._events: List[Tuple[float, str, Any]] = []
        self._state_times: Dict[RequestStatus, float] = {}
        self._created_time = time.time()
        self._first_token_time: Optional[float] = None
        self._finish_time: Optional[float] = None
        self._tokens_generated = 0
        self._preemption_count = 0
        self._lock = threading.Lock()

        self._record_event(
            "created",
            {
                "prompt_tokens": prompt_tokens,
                "max_tokens": max_tokens,
                "lora_adapter": lora_adapter,
            },
        )

    def _record_event(self, event_type: str, data: Any = None) -> None:
        """Record an event."""
        self._events.append((time.time(), event_type, data))

    @property
    def status(self) -> RequestStatus:
        """Get current status."""
        with self._lock:
            return self._status

    def transition_to(self, new_status: RequestStatus) -> None:
        """Transition to a new status."""
        with self._lock:
            now = time.time()
            old_status = self._status

            # Record time spent in old status
            if old_status in self._state_times:
                self._state_times[old_status] = now - self._state_times.get(f"_start_{old_status}", self._created_time)

            self._status = new_status
            self._state_times[f"_start_{new_status}"] = now

            if new_status == RequestStatus.PREEMPTED:
                self._preemption_count += 1

            self._record_event(
                "state_transition",
                {
                    "from": old_status.name,
                    "to": new_status.name,
                },
            )

    def record_token(self) -> None:
        """Record a generated token."""
        with self._lock:
            now = time.time()
            self._tokens_generated += 1

            if self._first_token_time is None:
                self._first_token_time = now
                self._record_event("first_token", {"time": now})

    def finish(self, reason: str = "stopped") -> None:
        """Mark request as finished."""
        with self._lock:
            self._finish_time = time.time()

            if reason == "stopped":
                new_status = RequestStatus.FINISHED_STOPPED
            elif reason == "length":
                new_status = RequestStatus.FINISHED_LENGTH_CAPPED
            elif reason == "aborted":
                new_status = RequestStatus.FINISHED_ABORTED
            else:
                new_status = RequestStatus.FINISHED_STOPPED

            self._status = new_status
            self._record_event(
                "finished",
                {
                    "reason": reason,
                    "tokens_generated": self._tokens_generated,
                },
            )

    @property
    def time_to_first_token(self) -> Optional[float]:
        """Get TTFT in seconds."""
        with self._lock:
            if self._first_token_time:
                return self._first_token_time - self._created_time
            return None

    @property
    def total_latency(self) -> Optional[float]:
        """Get total latency in seconds."""
        with self._lock:
            if self._finish_time:
                return self._finish_time - self._created_time
            return None

    @property
    def tokens_generated(self) -> int:
        """Get tokens generated."""
        with self._lock:
            return self._tokens_generated

    @property
    def inter_token_latency(self) -> Optional[float]:
        """Get average inter-token latency."""
        with self._lock:
            if self._tokens_generated <= 1 or not self._finish_time:
                return None
            if not self._first_token_time:
                return None
            decode_time = self._finish_time - self._first_token_time
            return decode_time / (self._tokens_generated - 1)

    @property
    def throughput(self) -> Optional[float]:
        """Get tokens per second."""
        latency = self.total_latency
        if latency and latency > 0:
            return self._tokens_generated / latency
        return None

    def get_events(self) -> List[Tuple[float, str, Any]]:
        """Get all events."""
        with self._lock:
            return list(self._events)

    def get_timing_breakdown(self) -> Dict[str, float]:
        """Get timing breakdown by state."""
        with self._lock:
            result = {}
            for status in RequestStatus:
                if status in self._state_times:
                    result[status.name] = self._state_times[status]

            if self._first_token_time:
                result["time_to_first_token"] = self._first_token_time - self._created_time
            if self._finish_time:
                result["total_latency"] = self._finish_time - self._created_time

            return result


class RequestLifecycleManager:
    """Manager for request lifecycles."""

    def __init__(self, max_completed: int = 1000):
        self._active: Dict[str, RequestLifecycle] = {}
        self._completed: List[RequestLifecycle] = []
        self._max_completed = max_completed
        self._lock = threading.Lock()

    def create(
        self,
        request_id: str,
        prompt_tokens: int = 0,
        max_tokens: int = 0,
        lora_adapter: Optional[str] = None,
    ) -> RequestLifecycle:
        """Create a new request lifecycle."""
        lifecycle = RequestLifecycle(
            request_id=request_id,
            prompt_tokens=prompt_tokens,
            max_tokens=max_tokens,
            lora_adapter=lora_adapter,
        )
        with self._lock:
            self._active[request_id] = lifecycle
        return lifecycle

    def get(self, request_id: str) -> Optional[RequestLifecycle]:
        """Get a request lifecycle."""
        with self._lock:
            return self._active.get(request_id)

    def finish(self, request_id: str, reason: str = "stopped") -> None:
        """Finish a request."""
        with self._lock:
            if request_id in self._active:
                lifecycle = self._active.pop(request_id)
                lifecycle.finish(reason)
                self._completed.append(lifecycle)
                if len(self._completed) > self._max_completed:
                    self._completed.pop(0)

    def get_active_count(self) -> int:
        """Get number of active requests."""
        with self._lock:
            return len(self._active)

    def get_completed_count(self) -> int:
        """Get number of completed requests."""
        with self._lock:
            return len(self._completed)

    def get_aggregate_stats(self) -> Dict[str, float]:
        """Get aggregate statistics from completed requests."""
        with self._lock:
            if not self._completed:
                return {}

            ttft_values = [r.time_to_first_token for r in self._completed if r.time_to_first_token is not None]
            itl_values = [r.inter_token_latency for r in self._completed if r.inter_token_latency is not None]
            latency_values = [r.total_latency for r in self._completed if r.total_latency is not None]
            throughput_values = [r.throughput for r in self._completed if r.throughput is not None]

            stats = {}
            if ttft_values:
                stats["avg_ttft"] = sum(ttft_values) / len(ttft_values)
                sorted_ttft = sorted(ttft_values)
                stats["p50_ttft"] = sorted_ttft[len(ttft_values) // 2]
                stats["p99_ttft"] = sorted_ttft[int(len(ttft_values) * 0.99)]
            if itl_values:
                stats["avg_itl"] = sum(itl_values) / len(itl_values)
            if latency_values:
                stats["avg_latency"] = sum(latency_values) / len(latency_values)
            if throughput_values:
                stats["avg_throughput"] = sum(throughput_values) / len(throughput_values)

            return stats
