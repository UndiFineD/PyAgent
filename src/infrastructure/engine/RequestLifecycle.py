# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Request lifecycle management for inference engines.

This module implements request state tracking and lifecycle management,
inspired by vLLM's v1/request.py architecture.

Key Components:
    - RequestStatus: Enum for request states (WAITING, RUNNING, FINISHED_*)
    - FinishReason: Why a request completed (STOP, LENGTH, ABORT, ERROR)
    - Request: Core request representation with status tracking
    - RequestEvent: Timestamped state transitions
    - RequestQueue: Waiting/running queue management
    - RequestTracker: Lifecycle tracking with timing metrics

Example:
    >>> from src.infrastructure.engine import Request, RequestStatus, FinishReason
    >>> 
    >>> # Create a new request
    >>> request = Request(
    ...     request_id="req-001",
    ...     prompt="What is the capital of France?",
    ...     max_tokens=100,
    ... )
    >>> assert request.status == RequestStatus.WAITING
    >>> 
    >>> # Transition to running
    >>> request.start_running()
    >>> assert request.status == RequestStatus.RUNNING
    >>> 
    >>> # Finish with stop reason
    >>> request.finish(FinishReason.STOP, stop_reason="</s>")
    >>> assert request.is_finished()
    >>> assert request.get_finished_reason() == FinishReason.STOP
"""

from __future__ import annotations

import enum
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union

# Try to import Rust accelerations
try:
    from rust_core import request_status_transition_rust
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


# ==============================================================================
# Finish Reason Enum
# ==============================================================================

# These are possible values of RequestOutput.finish_reason,
# so form part of the external API (matches vLLM).
FINISH_REASON_STRINGS = ("stop", "length", "abort", "error")


class FinishReason(enum.IntEnum):
    """
    Reason a request finished - stop, length, abort, or error.

    Int rather than Str for more compact serialization.

    Attributes:
        STOP: A stop string or token was emitted
        LENGTH: max_tokens was consumed, or max_model_len was reached
        ABORT: Aborted by client
        ERROR: Retryable request-level internal error (e.g., KV load failure)
    """

    STOP = 0
    LENGTH = 1
    ABORT = 2
    ERROR = 3

    def __str__(self) -> str:
        """Return string representation for API responses."""
        return FINISH_REASON_STRINGS[self.value]

    def __repr__(self) -> str:
        return f"FinishReason.{self.name}"


# ==============================================================================
# Request Status Enum
# ==============================================================================

class RequestStatus(enum.IntEnum):
    """
    Status of a request in the engine.

    States before PREEMPTED are considered "active" (not finished).
    States after PREEMPTED are considered "finished".
    """

    # Active states
    WAITING = enum.auto()                 # In waiting queue
    WAITING_FOR_FSM = enum.auto()         # Waiting for FSM compilation
    WAITING_FOR_REMOTE_KVS = enum.auto()  # Waiting for remote KV cache
    RUNNING = enum.auto()                 # Currently being processed
    PREEMPTED = enum.auto()               # Preempted, will be rescheduled

    # Finished states (anything after PREEMPTED)
    FINISHED_STOPPED = enum.auto()        # Completed with stop token/string
    FINISHED_LENGTH_CAPPED = enum.auto()  # Hit max_tokens or max_model_len
    FINISHED_ABORTED = enum.auto()        # Aborted by client
    FINISHED_IGNORED = enum.auto()        # Ignored (prompt too long)
    FINISHED_ERROR = enum.auto()          # Internal error

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def is_finished(status: "RequestStatus") -> bool:
        """Check if a status represents a finished request."""
        return status > RequestStatus.PREEMPTED

    @staticmethod
    def is_waiting(status: "RequestStatus") -> bool:
        """Check if a status represents a waiting request."""
        return status in (
            RequestStatus.WAITING,
            RequestStatus.WAITING_FOR_FSM,
            RequestStatus.WAITING_FOR_REMOTE_KVS,
        )

    @staticmethod
    def get_finished_reason(status: "RequestStatus") -> Optional[FinishReason]:
        """Get the finish reason for a finished status."""
        return _FINISHED_REASON_MAP.get(status)


# Mapping of finished statuses to their finish reasons
# NOTE: Ignored requests are those whose prompt lengths are longer than
# the model's length cap. The stop reason is "length" as in OpenAI API.
_FINISHED_REASON_MAP = {
    RequestStatus.FINISHED_STOPPED: FinishReason.STOP,
    RequestStatus.FINISHED_LENGTH_CAPPED: FinishReason.LENGTH,
    RequestStatus.FINISHED_ABORTED: FinishReason.ABORT,
    RequestStatus.FINISHED_IGNORED: FinishReason.LENGTH,
    RequestStatus.FINISHED_ERROR: FinishReason.ERROR,
}

# Valid state transitions
_VALID_TRANSITIONS: Dict[RequestStatus, Set[RequestStatus]] = {
    RequestStatus.WAITING: {
        RequestStatus.WAITING_FOR_FSM,
        RequestStatus.WAITING_FOR_REMOTE_KVS,
        RequestStatus.RUNNING,
        RequestStatus.FINISHED_ABORTED,
        RequestStatus.FINISHED_IGNORED,
    },
    RequestStatus.WAITING_FOR_FSM: {
        RequestStatus.WAITING,
        RequestStatus.RUNNING,
        RequestStatus.FINISHED_ABORTED,
    },
    RequestStatus.WAITING_FOR_REMOTE_KVS: {
        RequestStatus.WAITING,
        RequestStatus.RUNNING,
        RequestStatus.FINISHED_ABORTED,
        RequestStatus.FINISHED_ERROR,
    },
    RequestStatus.RUNNING: {
        RequestStatus.PREEMPTED,
        RequestStatus.FINISHED_STOPPED,
        RequestStatus.FINISHED_LENGTH_CAPPED,
        RequestStatus.FINISHED_ABORTED,
        RequestStatus.FINISHED_ERROR,
    },
    RequestStatus.PREEMPTED: {
        RequestStatus.WAITING,
        RequestStatus.RUNNING,
        RequestStatus.FINISHED_ABORTED,
    },
}


def is_valid_transition(from_status: RequestStatus, to_status: RequestStatus) -> bool:
    """Check if a state transition is valid."""
    # Note: Rust function uses simplified 0-based values, Python has extended states
    # Fall back to Python implementation for full compatibility
    valid_targets = _VALID_TRANSITIONS.get(from_status, set())
    return to_status in valid_targets


# ==============================================================================
# Request Event
# ==============================================================================

class RequestEventType(enum.Enum):
    """Types of request lifecycle events."""
    CREATED = "created"
    QUEUED = "queued"
    SCHEDULED = "scheduled"
    FIRST_TOKEN = "first_token"
    PREEMPTED = "preempted"
    RESUMED = "resumed"
    FINISHED = "finished"
    ABORTED = "aborted"
    ERROR = "error"


@dataclass
class RequestEvent:
    """
    A timestamped event in the request lifecycle.

    Attributes:
        event_type: Type of the event
        timestamp: Unix timestamp when the event occurred
        details: Optional additional information about the event
    """
    event_type: RequestEventType
    timestamp: float = field(default_factory=time.time)
    details: Optional[Dict[str, Any]] = None

    @classmethod
    def new_event(
        cls,
        event_type: RequestEventType,
        timestamp: Optional[float] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> "RequestEvent":
        """Factory method to create a new event."""
        return cls(
            event_type=event_type,
            timestamp=timestamp if timestamp is not None else time.time(),
            details=details,
        )


# ==============================================================================
# Request
# ==============================================================================

@dataclass
class Request:
    """
    Core request representation with lifecycle tracking.

    This class tracks the full lifecycle of an inference request from
    creation through completion, including state transitions and timing.

    Attributes:
        request_id: Unique identifier for this request
        prompt: The input prompt (text or token IDs)
        max_tokens: Maximum number of tokens to generate
        status: Current status of the request
        arrival_time: When the request was created
        events: List of lifecycle events
        output_token_ids: Generated token IDs
        stop_reason: Why the request stopped (if finished)
        finish_reason: High-level finish reason enum
        
    Example:
        >>> request = Request("req-001", "Hello", max_tokens=50)
        >>> request.start_running()
        >>> request.add_output_token(1234)
        >>> request.finish(FinishReason.STOP)
    """
    request_id: str
    prompt: Union[str, List[int]]
    max_tokens: int = 100
    
    # Optional parameters
    temperature: float = 1.0
    top_p: float = 1.0
    top_k: int = -1
    stop_strings: Optional[List[str]] = None
    stop_token_ids: Optional[List[int]] = None
    eos_token_id: Optional[int] = None
    
    # State tracking
    status: RequestStatus = field(default=RequestStatus.WAITING)
    arrival_time: float = field(default_factory=time.time)
    events: List[RequestEvent] = field(default_factory=list)
    
    # Output tracking
    output_token_ids: List[int] = field(default_factory=list)
    prompt_token_ids: Optional[List[int]] = None
    
    # Finish state
    stop_reason: Optional[Union[int, str]] = None
    finish_reason: Optional[FinishReason] = None
    
    # Timing (set during lifecycle)
    first_scheduled_time: Optional[float] = None
    first_token_time: Optional[float] = None
    finished_time: Optional[float] = None
    
    # Metadata
    lora_request: Optional[Any] = None
    kv_transfer_params: Optional[Dict[str, Any]] = None
    priority: int = 0
    
    def __post_init__(self):
        """Record creation event."""
        self._record_event(RequestEventType.CREATED)

    def _record_event(
        self,
        event_type: RequestEventType,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record a lifecycle event."""
        self.events.append(RequestEvent.new_event(event_type, details=details))

    def _transition_to(self, new_status: RequestStatus) -> None:
        """Transition to a new status with validation."""
        if not is_valid_transition(self.status, new_status):
            raise ValueError(
                f"Invalid status transition: {self.status} -> {new_status}"
            )
        self.status = new_status

    # -------------------------------------------------------------------------
    # Status Properties
    # -------------------------------------------------------------------------

    def is_finished(self) -> bool:
        """Check if the request is finished."""
        return RequestStatus.is_finished(self.status)

    def is_waiting(self) -> bool:
        """Check if the request is waiting."""
        return RequestStatus.is_waiting(self.status)

    def is_running(self) -> bool:
        """Check if the request is currently running."""
        return self.status == RequestStatus.RUNNING

    def get_finished_reason(self) -> Optional[FinishReason]:
        """Get the finish reason if finished."""
        return self.finish_reason or RequestStatus.get_finished_reason(self.status)

    # -------------------------------------------------------------------------
    # Computed Properties
    # -------------------------------------------------------------------------

    @property
    def num_output_tokens(self) -> int:
        """Number of output tokens generated so far."""
        return len(self.output_token_ids)

    @property
    def num_prompt_tokens(self) -> int:
        """Number of prompt tokens."""
        if self.prompt_token_ids is not None:
            return len(self.prompt_token_ids)
        if isinstance(self.prompt, list):
            return len(self.prompt)
        # Estimate for string prompts (rough approximation)
        return len(self.prompt.split()) * 4 // 3

    @property
    def num_tokens(self) -> int:
        """Total number of tokens (prompt + output)."""
        return self.num_prompt_tokens + self.num_output_tokens

    @property
    def time_in_queue(self) -> Optional[float]:
        """Time spent waiting in queue."""
        if self.first_scheduled_time is None:
            return None
        return self.first_scheduled_time - self.arrival_time

    @property
    def time_to_first_token(self) -> Optional[float]:
        """Time from scheduling to first token."""
        if self.first_token_time is None or self.first_scheduled_time is None:
            return None
        return self.first_token_time - self.first_scheduled_time

    @property
    def total_time(self) -> Optional[float]:
        """Total time from arrival to completion."""
        if self.finished_time is None:
            return None
        return self.finished_time - self.arrival_time

    # -------------------------------------------------------------------------
    # Lifecycle Methods
    # -------------------------------------------------------------------------

    def start_running(self) -> None:
        """Transition to RUNNING state."""
        now = time.time()
        self._transition_to(RequestStatus.RUNNING)
        if self.first_scheduled_time is None:
            self.first_scheduled_time = now
        self._record_event(RequestEventType.SCHEDULED)

    def add_output_token(self, token_id: int) -> None:
        """Add a generated token to the output."""
        if not self.is_running():
            raise RuntimeError(
                f"Cannot add token to request in state {self.status}"
            )
        was_empty = len(self.output_token_ids) == 0
        self.output_token_ids.append(token_id)
        if was_empty:
            self.first_token_time = time.time()
            self._record_event(RequestEventType.FIRST_TOKEN)

    def preempt(self) -> None:
        """Preempt the request (move back to waiting)."""
        self._transition_to(RequestStatus.PREEMPTED)
        self._record_event(RequestEventType.PREEMPTED)

    def resume(self) -> None:
        """Resume a preempted request."""
        if self.status != RequestStatus.PREEMPTED:
            raise ValueError("Can only resume preempted requests")
        self.status = RequestStatus.WAITING
        self._record_event(RequestEventType.RESUMED)

    def finish(
        self,
        reason: FinishReason,
        stop_reason: Optional[Union[int, str]] = None,
    ) -> None:
        """Finish the request with a reason."""
        # Determine the finish status based on reason
        status_map = {
            FinishReason.STOP: RequestStatus.FINISHED_STOPPED,
            FinishReason.LENGTH: RequestStatus.FINISHED_LENGTH_CAPPED,
            FinishReason.ABORT: RequestStatus.FINISHED_ABORTED,
            FinishReason.ERROR: RequestStatus.FINISHED_ERROR,
        }
        new_status = status_map.get(reason, RequestStatus.FINISHED_STOPPED)
        
        self._transition_to(new_status)
        self.finish_reason = reason
        self.stop_reason = stop_reason
        self.finished_time = time.time()
        self._record_event(
            RequestEventType.FINISHED,
            {"reason": str(reason), "stop_reason": stop_reason},
        )

    def abort(self) -> None:
        """Abort the request."""
        # Can abort from any non-finished state
        if not self.is_finished():
            self.status = RequestStatus.FINISHED_ABORTED
            self.finish_reason = FinishReason.ABORT
            self.finished_time = time.time()
            self._record_event(RequestEventType.ABORTED)

    def error(self, error_msg: Optional[str] = None) -> None:
        """Mark the request as errored."""
        if not self.is_finished():
            self.status = RequestStatus.FINISHED_ERROR
            self.finish_reason = FinishReason.ERROR
            self.finished_time = time.time()
            self._record_event(RequestEventType.ERROR, {"message": error_msg})

    # -------------------------------------------------------------------------
    # Check Methods
    # -------------------------------------------------------------------------

    def should_stop(self, max_model_len: Optional[int] = None) -> bool:
        """Check if the request should stop generating."""
        if self.is_finished():
            return True

        # Check max tokens
        if self.num_output_tokens >= self.max_tokens:
            return True

        # Check max model length
        if max_model_len is not None and self.num_tokens >= max_model_len:
            return True

        # Check last token against stop tokens
        if self.output_token_ids and self.stop_token_ids:
            if self.output_token_ids[-1] in self.stop_token_ids:
                return True

        # Check EOS token
        if self.output_token_ids and self.eos_token_id is not None:
            if self.output_token_ids[-1] == self.eos_token_id:
                return True

        return False


# ==============================================================================
# Request Queue
# ==============================================================================

class RequestQueue:
    """
    Thread-safe queue for managing waiting and running requests.

    This class manages the lifecycle of requests as they move between
    waiting, running, and finished states.

    Attributes:
        waiting: Deque of waiting request IDs
        running: Set of running request IDs
        requests: Dict mapping request_id to Request
        finished: Set of finished request IDs (recent)
    """

    def __init__(self, max_finished_history: int = 1000):
        """
        Initialize the request queue.

        Args:
            max_finished_history: Maximum number of finished requests to track
        """
        self._lock = threading.RLock()
        self._waiting: deque = deque()
        self._running: Set[str] = set()
        self._requests: Dict[str, Request] = {}
        self._finished: deque = deque(maxlen=max_finished_history)

    def add_request(self, request: Request) -> None:
        """Add a new request to the waiting queue."""
        with self._lock:
            if request.request_id in self._requests:
                raise ValueError(f"Request {request.request_id} already exists")
            self._requests[request.request_id] = request
            self._waiting.append(request.request_id)
            request._record_event(RequestEventType.QUEUED)

    def get_request(self, request_id: str) -> Optional[Request]:
        """Get a request by ID."""
        with self._lock:
            return self._requests.get(request_id)

    def schedule_next(self, n: int = 1) -> List[Request]:
        """
        Schedule the next n waiting requests.

        Returns:
            List of requests that were scheduled
        """
        scheduled = []
        with self._lock:
            while len(scheduled) < n and self._waiting:
                request_id = self._waiting.popleft()
                request = self._requests.get(request_id)
                if request and not request.is_finished():
                    request.start_running()
                    self._running.add(request_id)
                    scheduled.append(request)
        return scheduled

    def finish_request(
        self,
        request_id: str,
        reason: FinishReason,
        stop_reason: Optional[Union[int, str]] = None,
    ) -> Optional[Request]:
        """Mark a request as finished."""
        with self._lock:
            request = self._requests.get(request_id)
            if request is None:
                return None
            
            request.finish(reason, stop_reason)
            self._running.discard(request_id)
            self._finished.append(request_id)
            return request

    def abort_request(self, request_id: str) -> Optional[Request]:
        """Abort a request."""
        with self._lock:
            request = self._requests.get(request_id)
            if request is None:
                return None
            
            request.abort()
            self._waiting = deque(
                rid for rid in self._waiting if rid != request_id
            )
            self._running.discard(request_id)
            self._finished.append(request_id)
            return request

    def abort_requests(
        self,
        request_ids: Union[str, Iterable[str]],
    ) -> List[Request]:
        """Abort multiple requests."""
        if isinstance(request_ids, str):
            request_ids = [request_ids]
        
        aborted = []
        for request_id in request_ids:
            request = self.abort_request(request_id)
            if request:
                aborted.append(request)
        return aborted

    def preempt_request(self, request_id: str) -> Optional[Request]:
        """Preempt a running request back to waiting."""
        with self._lock:
            request = self._requests.get(request_id)
            if request is None or not request.is_running():
                return None
            
            request.preempt()
            self._running.discard(request_id)
            self._waiting.appendleft(request_id)  # Add to front
            return request

    def get_num_waiting(self) -> int:
        """Get the number of waiting requests."""
        with self._lock:
            return len(self._waiting)

    def get_num_running(self) -> int:
        """Get the number of running requests."""
        with self._lock:
            return len(self._running)

    def get_num_unfinished(self) -> int:
        """Get total number of unfinished requests."""
        return self.get_num_waiting() + self.get_num_running()

    def has_unfinished_requests(self) -> bool:
        """Check if there are any unfinished requests."""
        return self.get_num_unfinished() > 0

    def get_waiting_requests(self) -> List[Request]:
        """Get all waiting requests (ordered)."""
        with self._lock:
            return [
                self._requests[rid]
                for rid in self._waiting
                if rid in self._requests
            ]

    def get_running_requests(self) -> List[Request]:
        """Get all running requests."""
        with self._lock:
            return [
                self._requests[rid]
                for rid in self._running
                if rid in self._requests
            ]

    def cleanup_finished(self, older_than_seconds: float = 3600.0) -> int:
        """
        Remove finished requests older than the threshold.

        Returns:
            Number of requests removed
        """
        cutoff = time.time() - older_than_seconds
        removed = 0
        with self._lock:
            to_remove = []
            for request_id in self._finished:
                request = self._requests.get(request_id)
                if request and request.finished_time and request.finished_time < cutoff:
                    to_remove.append(request_id)
            
            for request_id in to_remove:
                del self._requests[request_id]
                removed += 1
        return removed


# ==============================================================================
# Request Tracker
# ==============================================================================

@dataclass
class RequestTracker:
    """
    Comprehensive tracking for request lifecycle metrics.

    This class aggregates statistics across all requests for
    monitoring and optimization.
    """
    
    # Counters
    total_requests: int = 0
    completed_requests: int = 0
    aborted_requests: int = 0
    error_requests: int = 0
    
    # Timing aggregates (in seconds)
    total_queue_time: float = 0.0
    total_ttft: float = 0.0  # Time to first token
    total_completion_time: float = 0.0
    
    # Token counts
    total_prompt_tokens: int = 0
    total_output_tokens: int = 0
    
    # For computing averages
    _queue_times: List[float] = field(default_factory=list)
    _ttfts: List[float] = field(default_factory=list)
    _completion_times: List[float] = field(default_factory=list)

    def record_request(self, request: Request) -> None:
        """Record metrics from a finished request."""
        if not request.is_finished():
            return
        
        self.total_requests += 1
        
        # Categorize by finish reason
        if request.finish_reason == FinishReason.ABORT:
            self.aborted_requests += 1
        elif request.finish_reason == FinishReason.ERROR:
            self.error_requests += 1
        else:
            self.completed_requests += 1
        
        # Record tokens
        self.total_prompt_tokens += request.num_prompt_tokens
        self.total_output_tokens += request.num_output_tokens
        
        # Record timing
        if request.time_in_queue is not None:
            self.total_queue_time += request.time_in_queue
            self._queue_times.append(request.time_in_queue)
        
        if request.time_to_first_token is not None:
            self.total_ttft += request.time_to_first_token
            self._ttfts.append(request.time_to_first_token)
        
        if request.total_time is not None:
            self.total_completion_time += request.total_time
            self._completion_times.append(request.total_time)

    @property
    def avg_queue_time(self) -> Optional[float]:
        """Average time spent in queue."""
        if not self._queue_times:
            return None
        return sum(self._queue_times) / len(self._queue_times)

    @property
    def avg_ttft(self) -> Optional[float]:
        """Average time to first token."""
        if not self._ttfts:
            return None
        return sum(self._ttfts) / len(self._ttfts)

    @property
    def avg_completion_time(self) -> Optional[float]:
        """Average total completion time."""
        if not self._completion_times:
            return None
        return sum(self._completion_times) / len(self._completion_times)

    @property
    def avg_tokens_per_request(self) -> float:
        """Average output tokens per completed request."""
        if self.completed_requests == 0:
            return 0.0
        return self.total_output_tokens / self.completed_requests

    @property
    def throughput(self) -> Optional[float]:
        """Tokens per second (based on total completion time)."""
        if self.total_completion_time == 0:
            return None
        return self.total_output_tokens / self.total_completion_time

    def reset(self) -> None:
        """Reset all counters."""
        self.total_requests = 0
        self.completed_requests = 0
        self.aborted_requests = 0
        self.error_requests = 0
        self.total_queue_time = 0.0
        self.total_ttft = 0.0
        self.total_completion_time = 0.0
        self.total_prompt_tokens = 0
        self.total_output_tokens = 0
        self._queue_times.clear()
        self._ttfts.clear()
        self._completion_times.clear()

    def as_dict(self) -> Dict[str, Any]:
        """Export metrics as a dictionary."""
        return {
            "total_requests": self.total_requests,
            "completed_requests": self.completed_requests,
            "aborted_requests": self.aborted_requests,
            "error_requests": self.error_requests,
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_output_tokens": self.total_output_tokens,
            "avg_queue_time": self.avg_queue_time,
            "avg_ttft": self.avg_ttft,
            "avg_completion_time": self.avg_completion_time,
            "avg_tokens_per_request": self.avg_tokens_per_request,
            "throughput": self.throughput,
        }
