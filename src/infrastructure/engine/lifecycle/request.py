# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Request object implementation."""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from .enums import RequestStatus, FinishReason, RequestEventType, is_valid_transition
from .event import RequestEvent


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

    def should_stop(self, max_model_len: Optional[int] = None) -> bool:
        """Check if the request should stop generating."""
        if self.is_finished():
            return True

        if self.num_output_tokens >= self.max_tokens:
            return True

        if max_model_len is not None and self.num_tokens >= max_model_len:
            return True

        if self.output_token_ids and self.stop_token_ids:
            if self.output_token_ids[-1] in self.stop_token_ids:
                return True

        if self.output_token_ids and self.eos_token_id is not None:
            if self.output_token_ids[-1] == self.eos_token_id:
                return True

        return False
