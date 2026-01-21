# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Request and metrics data structures for scheduling."""

from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any, Optional
from .config import RequestPriority, RequestState, PreemptionReason


@dataclass
class RequestMetrics:
    """Metrics for a single request."""
    created_at: float = 0.0
    first_scheduled_at: float = 0.0
    completed_at: float = 0.0
    preemption_count: int = 0
    total_preemption_time: float = 0.0
    tokens_processed: int = 0
    chunks_executed: int = 0

    @property
    def latency_ms(self) -> float:
        """Total latency in milliseconds."""
        if self.completed_at > 0:
            return (self.completed_at - self.created_at) * 1000
        return 0.0

    @property
    def queue_time_ms(self) -> float:
        """Time spent waiting in queue."""
        if self.first_scheduled_at > 0:
            return (self.first_scheduled_at - self.created_at) * 1000
        return 0.0


@dataclass
class ScheduledRequest:
    """A request scheduled for inference."""
    request_id: str
    prompt: str
    priority: RequestPriority = RequestPriority.NORMAL
    state: RequestState = RequestState.WAITING
    deadline: Optional[float] = None
    max_tokens: int = 256

    # Scheduling metadata
    arrival_time: float = field(default_factory=time.time)
    prompt_tokens: int = 0
    generated_tokens: int = 0
    metrics: RequestMetrics = field(default_factory=RequestMetrics)

    # Preemption state
    preempted_at: float = 0.0
    preemption_reason: Optional[PreemptionReason] = None
    saved_state: Optional[Any] = None  # KV cache state, etc.

    # Internal
    _sequence: int = field(default=0, repr=False)

    def __post_init__(self) -> None:
        """Initialize metrics."""
        self.metrics.created_at = self.arrival_time

    @property
    def total_tokens(self) -> int:
        """Total tokens (prompt + generated)."""
        return self.prompt_tokens + self.generated_tokens

    @property
    def remaining_tokens(self) -> int:
        """Tokens remaining to generate."""
        return max(0, self.max_tokens - self.generated_tokens)

    @property
    def is_preemptible(self) -> bool:
        """Whether request can be preempted."""
        return (
            self.state == RequestState.RUNNING and
            self.priority != RequestPriority.CRITICAL
        )

    def preempt(self, reason: PreemptionReason, state: Optional[Any] = None) -> None:
        """Preempt this request."""
        self.state = RequestState.PREEMPTED
        self.preempted_at = time.time()
        self.preemption_reason = reason
        self.saved_state = state
        self.metrics.preemption_count += 1

    def resume(self) -> Optional[Any]:
        """Resume a preempted request."""
        if self.state == RequestState.PREEMPTED:
            preemption_duration = time.time() - self.preempted_at
            self.metrics.total_preemption_time += preemption_duration
            self.state = RequestState.WAITING
            return self.saved_state
        return None
