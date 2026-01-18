"""AdvancedRequestScheduler - Priority scheduling with preemption for LLM inference.

This module implements vLLM-style request scheduling with priority queues,
preemption support, and token budget management for efficient GPU utilization.

Inspired by vLLM v1/core/sched/scheduler.py, but extends with:
- Deadline-aware EDF (Earliest Deadline First) scheduling
- Fine-grained preemption with state preservation
- Multi-tier priority with starvation prevention
- Dynamic token budget based on memory pressure

Example:
    >>> scheduler = AdvancedRequestScheduler(max_tokens=4096)
    >>> req = scheduler.add_request(prompt="Hello", priority=RequestPriority.HIGH)
    >>> batch = scheduler.schedule()  # Get next batch to execute
    >>> scheduler.complete_request(req.request_id)
"""

from __future__ import annotations

import heapq
import threading
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Optional, Iterator
from collections import deque
import uuid

# Try to import Rust accelerations
try:
    from src.core.rust_bridge import get_bridge
    _bridge = get_bridge()
    HAS_RUST = hasattr(_bridge, 'priority_heap_ops_rust')
except Exception:
    HAS_RUST = False
    _bridge = None


class RequestPriority(Enum):
    """Priority levels for inference requests."""
    CRITICAL = 0    # System-critical (must execute immediately)
    HIGH = 1        # User-facing, latency-sensitive
    NORMAL = 2      # Standard priority
    LOW = 3         # Background processing
    BACKGROUND = 4  # Batch jobs, can be heavily preempted


class RequestState(Enum):
    """State of an inference request."""
    WAITING = auto()           # In queue, not yet scheduled
    RUNNING = auto()           # Currently executing
    PREEMPTED = auto()         # Paused to make room for higher priority
    WAITING_KV_CACHE = auto()  # Waiting for remote KV cache
    COMPLETED = auto()         # Finished successfully
    ABORTED = auto()           # Cancelled by user
    FAILED = auto()            # Error during execution


class PreemptionReason(Enum):
    """Reason for request preemption."""
    HIGHER_PRIORITY = auto()   # Higher priority request arrived
    MEMORY_PRESSURE = auto()   # Need to free GPU memory
    TIMEOUT = auto()           # Exceeded time limit
    TOKEN_BUDGET = auto()      # Token budget exhausted
    DEADLINE = auto()          # Deadline approaching for other requests


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
    """A request scheduled for inference.
    
    Attributes:
        request_id: Unique identifier
        prompt: Input prompt text or tokens
        priority: Request priority
        state: Current state
        deadline: Optional deadline (Unix timestamp)
    """
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
        """Resume a preempted request.
        
        Returns:
            Saved state for resumption
        """
        if self.state == RequestState.PREEMPTED:
            preemption_duration = time.time() - self.preempted_at
            self.metrics.total_preemption_time += preemption_duration
            self.state = RequestState.WAITING
            return self.saved_state
        return None


class PriorityRequestQueue:
    """Heap-based priority queue for inference requests.
    
    Orders requests by (priority, deadline, arrival_time) for fair scheduling.
    Supports efficient insertion, extraction, and preemption lookup.
    """
    
    def __init__(self, enable_starvation_prevention: bool = True):
        """Initialize priority queue.
        
        Args:
            enable_starvation_prevention: Whether to age priorities
        """
        self.enable_starvation_prevention = enable_starvation_prevention
        self._heap: list[tuple[float, float, float, int, ScheduledRequest]] = []
        self._sequence = 0
        self._lock = threading.Lock()
        self._request_map: dict[str, ScheduledRequest] = {}
        
        # Starvation prevention
        self._age_interval = 1.0  # seconds
        self._max_age = 10.0      # seconds before priority boost
        self._last_age_time = time.time()
    
    def _get_priority_score(self, request: ScheduledRequest) -> float:
        """Calculate priority score for heap ordering.
        
        Lower score = higher priority in min-heap.
        """
        base_priority = request.priority.value
        
        # Factor in deadline (EDF component)
        if request.deadline is not None:
            time_to_deadline = request.deadline - time.time()
            if time_to_deadline < 0:
                return -1000  # Overdue - highest priority
            # Blend priority with deadline urgency
            deadline_factor = 1.0 / max(time_to_deadline, 0.001)
            return base_priority - min(deadline_factor * 10, 2.0)
        
        return float(base_priority)
    
    def push(self, request: ScheduledRequest) -> None:
        """Add request to queue."""
        with self._lock:
            self._sequence += 1
            request._sequence = self._sequence
            
            # Tuple: (priority_score, deadline or inf, arrival_time, sequence, request)
            priority_score = self._get_priority_score(request)
            deadline = request.deadline if request.deadline else float('inf')
            
            entry = (
                priority_score,
                deadline,
                request.arrival_time,
                self._sequence,
                request,
            )
            heapq.heappush(self._heap, entry)
            self._request_map[request.request_id] = request
    
    def pop(self) -> Optional[ScheduledRequest]:
        """Remove and return highest priority request."""
        with self._lock:
            self._maybe_age_priorities()
            
            while self._heap:
                entry = heapq.heappop(self._heap)
                request = entry[4]
                
                # Skip if request was removed
                if request.request_id not in self._request_map:
                    continue
                
                # Skip if request state changed
                if request.state not in (RequestState.WAITING, RequestState.PREEMPTED):
                    continue
                
                del self._request_map[request.request_id]
                return request
            
            return None
    
    def peek(self) -> Optional[ScheduledRequest]:
        """Return highest priority request without removing."""
        with self._lock:
            for entry in self._heap:
                request = entry[4]
                if request.request_id in self._request_map:
                    if request.state in (RequestState.WAITING, RequestState.PREEMPTED):
                        return request
            return None
    
    def remove(self, request_id: str) -> Optional[ScheduledRequest]:
        """Remove request by ID (lazy removal)."""
        with self._lock:
            if request_id in self._request_map:
                request = self._request_map.pop(request_id)
                return request
            return None
    
    def _maybe_age_priorities(self) -> None:
        """Apply priority aging to prevent starvation."""
        if not self.enable_starvation_prevention:
            return
        
        now = time.time()
        if now - self._last_age_time < self._age_interval:
            return
        
        self._last_age_time = now
        
        # Rebuild heap with aged priorities
        new_heap: list[tuple[float, float, float, int, ScheduledRequest]] = []
        
        for entry in self._heap:
            request = entry[4]
            if request.request_id not in self._request_map:
                continue
            
            # Calculate age-based priority boost
            age = now - request.arrival_time
            if age > self._max_age:
                # Boost priority by up to 1 level
                boost = min((age - self._max_age) / self._max_age, 1.0)
                new_priority = self._get_priority_score(request) - boost
            else:
                new_priority = entry[0]
            
            new_heap.append((
                new_priority,
                entry[1],
                entry[2],
                entry[3],
                request,
            ))
        
        heapq.heapify(new_heap)
        self._heap = new_heap
    
    def __len__(self) -> int:
        """Number of requests in queue."""
        with self._lock:
            return len(self._request_map)
    
    def __bool__(self) -> bool:
        """Whether queue has requests."""
        return len(self) > 0


@dataclass
class SchedulerConfig:
    """Configuration for the request scheduler."""
    max_running_requests: int = 32
    max_tokens_per_batch: int = 4096
    max_prompt_tokens: int = 2048
    preemption_enabled: bool = True
    preemption_mode: str = "swap"  # "swap" or "recompute"
    chunked_prefill_enabled: bool = True
    chunk_token_threshold: int = 512
    starvation_prevention: bool = True
    deadline_scheduling: bool = True


class AdvancedRequestScheduler:
    """Advanced request scheduler with priority and preemption.
    
    This scheduler manages inference requests with support for:
    - Priority-based scheduling with multiple levels
    - Request preemption for latency-sensitive workloads
    - Token budget management for efficient batching
    - Deadline-aware scheduling (EDF option)
    - Chunked prefill for long prompts
    
    Attributes:
        config: Scheduler configuration
        running: Currently executing requests
        waiting: Priority queue of waiting requests
    """
    
    def __init__(self, config: Optional[SchedulerConfig] = None):
        """Initialize scheduler.
        
        Args:
            config: Scheduler configuration
        """
        self.config = config or SchedulerConfig()
        
        # Request queues
        self.waiting = PriorityRequestQueue(
            enable_starvation_prevention=self.config.starvation_prevention
        )
        self.running: dict[str, ScheduledRequest] = {}
        self.preempted: dict[str, ScheduledRequest] = {}
        self.completed: dict[str, ScheduledRequest] = {}
        
        # Token tracking
        self._running_tokens = 0
        self._lock = threading.Lock()
        self._sequence = 0
        
        # Statistics
        self._total_scheduled = 0
        self._total_completed = 0
        self._total_preemptions = 0
    
    def add_request(
        self,
        prompt: str,
        priority: RequestPriority = RequestPriority.NORMAL,
        max_tokens: int = 256,
        deadline: Optional[float] = None,
        request_id: Optional[str] = None,
        prompt_tokens: Optional[int] = None,
    ) -> ScheduledRequest:
        """Add a new request to the scheduler.
        
        Args:
            prompt: Input prompt
            priority: Request priority
            max_tokens: Maximum tokens to generate
            deadline: Optional deadline timestamp
            request_id: Optional custom ID
            prompt_tokens: Pre-computed prompt token count
            
        Returns:
            ScheduledRequest instance
        """
        if request_id is None:
            request_id = str(uuid.uuid4())[:8]
        
        # Estimate prompt tokens if not provided
        if prompt_tokens is None:
            # Simple estimate: ~4 chars per token
            prompt_tokens = len(prompt) // 4
        
        request = ScheduledRequest(
            request_id=request_id,
            prompt=prompt,
            priority=priority,
            state=RequestState.WAITING,
            deadline=deadline,
            max_tokens=max_tokens,
            prompt_tokens=prompt_tokens,
        )
        
        with self._lock:
            self._sequence += 1
            request._sequence = self._sequence
        
        self.waiting.push(request)
        return request
    
    def schedule(self) -> list[ScheduledRequest]:
        """Select requests for the next execution batch.
        
        This is the main scheduling function that:
        1. Considers preempted requests first
        2. Fills remaining capacity from waiting queue
        3. Respects token budget constraints
        4. May preempt running requests for higher priority
        
        Returns:
            List of requests to execute
        """
        with self._lock:
            batch: list[ScheduledRequest] = []
            token_budget = self.config.max_tokens_per_batch - self._running_tokens
            
            # First, try to resume preempted requests
            preempted_ids = list(self.preempted.keys())
            for req_id in preempted_ids:
                if len(batch) >= self.config.max_running_requests - len(self.running):
                    break
                
                request = self.preempted[req_id]
                if request.total_tokens <= token_budget:
                    request.resume()
                    request.state = RequestState.RUNNING
                    del self.preempted[req_id]
                    self.running[req_id] = request
                    batch.append(request)
                    token_budget -= request.total_tokens
            
            # Then, schedule waiting requests
            # Track initial running count to avoid double-counting batch items
            initial_running = len(self.running)
            while len(batch) + initial_running < self.config.max_running_requests:
                if token_budget <= 0:
                    break
                
                request = self.waiting.pop()
                if request is None:
                    break
                
                # Check if we need to preempt for this request
                if request.total_tokens > token_budget:
                    if self._should_preempt(request, token_budget):
                        freed = self._preempt_for_request(request)
                        token_budget += freed
                    else:
                        # Put back and try next
                        self.waiting.push(request)
                        continue
                
                # Schedule the request
                request.state = RequestState.RUNNING
                if request.metrics.first_scheduled_at == 0:
                    request.metrics.first_scheduled_at = time.time()
                
                self.running[request.request_id] = request
                batch.append(request)
                token_budget -= request.total_tokens
                self._total_scheduled += 1
                self._running_tokens += request.total_tokens
            
            return batch
    
    def _should_preempt(
        self,
        incoming: ScheduledRequest,
        available_budget: int,
    ) -> bool:
        """Decide whether to preempt running requests.
        
        Args:
            incoming: Incoming high-priority request
            available_budget: Currently available token budget
            
        Returns:
            True if preemption should occur
        """
        if not self.config.preemption_enabled:
            return False
        
        # Only preempt for higher priority requests
        if incoming.priority.value >= RequestPriority.NORMAL.value:
            return False
        
        # Check if preemption would free enough budget
        preemptible = [
            r for r in self.running.values()
            if r.is_preemptible and r.priority.value > incoming.priority.value
        ]
        
        if not preemptible:
            return False
        
        # Sort by priority (lower priority first for preemption)
        preemptible.sort(key=lambda r: -r.priority.value)
        
        freed = 0
        needed = incoming.total_tokens - available_budget
        
        for request in preemptible:
            freed += request.total_tokens
            if freed >= needed:
                return True
        
        return False
    
    def _preempt_for_request(self, incoming: ScheduledRequest) -> int:
        """Preempt running requests to make room.
        
        Args:
            incoming: Request that needs resources
            
        Returns:
            Total tokens freed
        """
        preemptible = [
            r for r in self.running.values()
            if r.is_preemptible and r.priority.value > incoming.priority.value
        ]
        
        preemptible.sort(key=lambda r: -r.priority.value)
        
        freed = 0
        needed = incoming.total_tokens - (
            self.config.max_tokens_per_batch - self._running_tokens
        )
        
        for request in preemptible:
            if freed >= needed:
                break
            
            self._preempt_request(
                request.request_id,
                PreemptionReason.HIGHER_PRIORITY,
            )
            freed += request.total_tokens
            self._total_preemptions += 1
        
        return freed
    
    def _preempt_request(
        self,
        request_id: str,
        reason: PreemptionReason,
        saved_state: Optional[Any] = None,
    ) -> bool:
        """Preempt a specific request.
        
        Args:
            request_id: Request to preempt
            reason: Reason for preemption
            saved_state: State to save for resumption
            
        Returns:
            True if preemption succeeded
        """
        if request_id not in self.running:
            return False
        
        request = self.running.pop(request_id)
        request.preempt(reason, saved_state)
        self.preempted[request_id] = request
        self._running_tokens -= request.total_tokens
        
        return True
    
    def preempt_request(
        self,
        request_id: str,
        reason: PreemptionReason = PreemptionReason.MEMORY_PRESSURE,
        saved_state: Optional[Any] = None,
    ) -> bool:
        """Public API for preempting a request."""
        with self._lock:
            return self._preempt_request(request_id, reason, saved_state)
    
    def resume_request(self, request_id: str) -> bool:
        """Resume a preempted request.
        
        Args:
            request_id: Request to resume
            
        Returns:
            True if resumption succeeded
        """
        with self._lock:
            if request_id not in self.preempted:
                return False
            
            request = self.preempted.pop(request_id)
            request.resume()
            self.waiting.push(request)
            return True
    
    def complete_request(
        self,
        request_id: str,
        generated_tokens: int = 0,
    ) -> bool:
        """Mark a request as completed.
        
        Args:
            request_id: Request to complete
            generated_tokens: Tokens generated
            
        Returns:
            True if completion succeeded
        """
        with self._lock:
            if request_id not in self.running:
                return False
            
            request = self.running.pop(request_id)
            request.state = RequestState.COMPLETED
            request.generated_tokens = generated_tokens
            request.metrics.completed_at = time.time()
            
            self.completed[request_id] = request
            self._running_tokens -= request.total_tokens
            self._total_completed += 1
            
            return True
    
    def abort_request(self, request_id: str) -> bool:
        """Abort a request.
        
        Args:
            request_id: Request to abort
            
        Returns:
            True if abort succeeded
        """
        with self._lock:
            # Check running
            if request_id in self.running:
                request = self.running.pop(request_id)
                request.state = RequestState.ABORTED
                self._running_tokens -= request.total_tokens
                return True
            
            # Check preempted
            if request_id in self.preempted:
                request = self.preempted.pop(request_id)
                request.state = RequestState.ABORTED
                return True
            
            # Check waiting
            request = self.waiting.remove(request_id)
            if request is not None:
                request.state = RequestState.ABORTED
                return True
            
            return False
    
    def get_request(self, request_id: str) -> Optional[ScheduledRequest]:
        """Get request by ID."""
        with self._lock:
            if request_id in self.running:
                return self.running[request_id]
            if request_id in self.preempted:
                return self.preempted[request_id]
            if request_id in self.completed:
                return self.completed[request_id]
        return None
    
    @property
    def stats(self) -> dict[str, Any]:
        """Get scheduler statistics."""
        with self._lock:
            return {
                "waiting": len(self.waiting),
                "running": len(self.running),
                "preempted": len(self.preempted),
                "completed": len(self.completed),
                "running_tokens": self._running_tokens,
                "total_scheduled": self._total_scheduled,
                "total_completed": self._total_completed,
                "total_preemptions": self._total_preemptions,
                "token_budget_used": self._running_tokens / self.config.max_tokens_per_batch,
            }
    
    def clear_completed(self, older_than: float = 0) -> int:
        """Clear completed requests older than threshold.
        
        Args:
            older_than: Age threshold in seconds (0 = all)
            
        Returns:
            Number of requests cleared
        """
        with self._lock:
            if older_than <= 0:
                count = len(self.completed)
                self.completed.clear()
                return count
            
            cutoff = time.time() - older_than
            to_remove = [
                rid for rid, req in self.completed.items()
                if req.metrics.completed_at < cutoff
            ]
            
            for rid in to_remove:
                del self.completed[rid]
            
            return len(to_remove)


# Convenience functions
def create_scheduler(
    max_tokens: int = 4096,
    max_requests: int = 32,
    preemption: bool = True,
) -> AdvancedRequestScheduler:
    """Create a scheduler with common settings."""
    config = SchedulerConfig(
        max_running_requests=max_requests,
        max_tokens_per_batch=max_tokens,
        preemption_enabled=preemption,
    )
    return AdvancedRequestScheduler(config)


def priority_from_string(s: str) -> RequestPriority:
    """Convert string to RequestPriority."""
    mapping = {
        "critical": RequestPriority.CRITICAL,
        "high": RequestPriority.HIGH,
        "normal": RequestPriority.NORMAL,
        "low": RequestPriority.LOW,
        "background": RequestPriority.BACKGROUND,
    }
    return mapping.get(s.lower(), RequestPriority.NORMAL)
