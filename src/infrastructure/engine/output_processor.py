"""
OutputProcessor - Request output management and state tracking.

Inspired by vLLM's v1/engine/output_processor.py - manages per-request state,
detokenization, and output batching.
"""

from __future__ import annotations

import asyncio
import time
import contextlib
from abc import ABC
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, Iterator, List, Optional, Set, Tuple
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types of request events."""
    QUEUED = auto()
    STARTED = auto()
    PREEMPTED = auto()
    RESUMED = auto()
    FINISHED = auto()
    ABORTED = auto()


@dataclass
class RequestEvent:
    """An event in request lifecycle."""
    event_type: EventType
    timestamp: float = field(default_factory=time.time)
    details: Optional[Dict[str, Any]] = None


@dataclass
class LoRARequest:
    """LoRA adapter request information."""
    lora_id: int
    lora_name: str
    lora_path: Optional[str] = None


@dataclass
class ParentRequest:
    """Parent request for multi-turn conversations."""
    request_id: str
    child_request_ids: List[str] = field(default_factory=list)


@dataclass
class SamplingParams:
    """Parameters for token sampling."""
    max_tokens: int = 256
    temperature: float = 1.0
    top_p: float = 1.0
    top_k: int = -1
    skip_special_tokens: bool = True
    spaces_between_special_tokens: bool = True
    stop: Optional[List[str]] = None
    include_stop_str_in_output: bool = False


@dataclass
class EngineCoreRequest:
    """Request to be processed by engine core."""
    request_id: str
    external_req_id: Optional[str] = None
    prompt_token_ids: Optional[List[int]] = None
    prompt_embeds: Optional[Any] = None
    mm_features: Optional[Any] = None
    eos_token_id: Optional[int] = None
    arrival_time: float = field(default_factory=time.time)
    lora_request: Optional[LoRARequest] = None
    cache_salt: Optional[str] = None
    data_parallel_rank: Optional[int] = None
    sampling_params: Optional[SamplingParams] = None
    pooling_params: Optional[Any] = None


@dataclass
class EngineCoreOutput:
    """Output from engine core for a single request."""
    request_id: str
    new_token_ids: List[int] = field(default_factory=list)
    finish_reason: Optional[str] = None
    new_logprobs: Optional[List[Any]] = None
    new_prompt_logprobs_tensors: Optional[Any] = None
    pooling_output: Optional[Any] = None
    stop_reason: Optional[str] = None
    events: List[RequestEvent] = field(default_factory=list)


@dataclass
class EngineCoreOutputs:
    """Batch of outputs from engine core."""
    outputs: List[EngineCoreOutput] = field(default_factory=list)
    scheduler_stats: Optional[Any] = None
    timestamp: float = field(default_factory=time.time)


@dataclass
class RequestOutput:
    """Final output for a request (to be returned to client)."""
    request_id: str
    prompt: Optional[str] = None
    prompt_token_ids: Optional[List[int]] = None
    outputs: List[Dict[str, Any]] = field(default_factory=list)
    finished: bool = False
    metrics: Optional[Dict[str, Any]] = None


@dataclass
class OutputProcessorOutput:
    """Output from OutputProcessor.process_outputs()."""
    request_outputs: List[RequestOutput] = field(default_factory=list)
    finished_request_ids: Set[str] = field(default_factory=set)


class RequestOutputCollector:
    """Queue for collecting request outputs."""

    def __init__(self):
        self._queue: asyncio.Queue = asyncio.Queue()

    def put(self, output: RequestOutput) -> None:
        """Put output into queue (non-async)."""
        try:
            self._queue.put_nowait(output)
        except asyncio.QueueFull:
            logger.warning(f"Output queue full for request {output.request_id}")

    async def get(self) -> RequestOutput:
        """Get output from queue."""
        return await self._queue.get()

    def empty(self) -> bool:
        """Check if queue is empty."""
        return self._queue.empty()


class RequestState:
    """
    Per-request state tracking.

    Manages detokenization state, output accumulation, and streaming.
    """

    def __init__(
        self,
        request_id: str,
        prompt: Optional[str],
        prompt_token_ids: Optional[List[int]],
        sampling_params: Optional[SamplingParams],
        arrival_time: float,
        queue: Optional[RequestOutputCollector] = None,
        log_stats: bool = False,
        stream_interval: int = 1,
    ):
        self.request_id = request_id
        self.prompt = prompt
        self.prompt_token_ids = prompt_token_ids or []
        self.sampling_params = sampling_params
        self.arrival_time = arrival_time
        self.queue = queue
        self.log_stats = log_stats
        self.stream_interval = stream_interval

        # Output state
        self.output_token_ids: List[int] = []
        self.output_text: str = ""
        self.finished: bool = False
        self.finish_reason: Optional[str] = None

        # Streaming state
        self._output_count: int = 0
        self._last_output_index: int = 0

        # Events
        self.events: List[RequestEvent] = []

        # Statistics
        self.first_token_time: Optional[float] = None
        self.last_token_time: Optional[float] = None
        self.num_output_tokens: int = 0

    @classmethod
    def from_new_request(
        cls,
        tokenizer: Any,
        request: EngineCoreRequest,
        prompt: Optional[str],
        parent_req: Optional[ParentRequest] = None,
        request_index: int = 0,
        queue: Optional[RequestOutputCollector] = None,
        log_stats: bool = False,
        stream_interval: int = 1,
    ) -> "RequestState":
        """Create RequestState from a new request."""
        return cls(
            request_id=request.request_id,
            prompt=prompt,
            prompt_token_ids=request.prompt_token_ids,
            sampling_params=request.sampling_params,
            arrival_time=request.arrival_time,
            queue=queue,
            log_stats=log_stats,
            stream_interval=stream_interval,
        )

    def add_event(self, event_type: EventType, details: Optional[Dict[str, Any]] = None) -> None:
        """Add an event to the request."""
        self.events.append(RequestEvent(event_type=event_type, details=details))

    def update(
        self,
        new_token_ids: List[int],
        new_text: str = "",
        finish_reason: Optional[str] = None,
    ) -> None:
        """Update state with new output."""
        now = time.time()

        if new_token_ids:
            if self.first_token_time is None:
                self.first_token_time = now
            self.last_token_time = now

            self.output_token_ids.extend(new_token_ids)
            self.num_output_tokens += len(new_token_ids)

        self.output_text += new_text

        if finish_reason is not None:
            self.finished = True
            self.finish_reason = finish_reason
            self.add_event(EventType.FINISHED, {"reason": finish_reason})

    def should_emit_output(self) -> bool:
        """Check if we should emit output based on stream interval."""
        self._output_count += 1
        if self.finished:
            return True
        return self._output_count % self.stream_interval == 0

    def get_output(self, delta: bool = False) -> RequestOutput:
        """Get current output."""
        if delta:
            # Return only new tokens since last output
            token_ids = self.output_token_ids[self._last_output_index:]
            self._last_output_index = len(self.output_token_ids)
        else:
            token_ids = self.output_token_ids.copy()

        return RequestOutput(
            request_id=self.request_id,
            prompt=self.prompt,
            prompt_token_ids=self.prompt_token_ids,
            outputs=[{
                "token_ids": token_ids,
                "text": self.output_text,
                "finish_reason": self.finish_reason,
            }],
            finished=self.finished,
            metrics=self._get_metrics() if self.log_stats else None,
        )

    def _get_metrics(self) -> Dict[str, Any]:
        """Get request metrics."""
        metrics = {
            "num_prompt_tokens": len(self.prompt_token_ids),
            "num_output_tokens": self.num_output_tokens,
            "arrival_time": self.arrival_time,
        }
        if self.first_token_time:
            metrics["time_to_first_token"] = self.first_token_time - self.arrival_time
        if self.last_token_time and self.first_token_time:
            metrics["generation_time"] = self.last_token_time - self.first_token_time
        return metrics


class LoRARequestStates:
    """Track LoRA request states."""

    def __init__(self, log_stats: bool = False):
        self.log_stats = log_stats
        self.active_loras: Dict[int, Set[str]] = defaultdict(set)
        self.lora_stats: Dict[int, Dict[str, Any]] = {}

    def add_request(self, request_id: str, lora_request: Optional[LoRARequest]) -> None:
        """Track a new request with LoRA."""
        if lora_request:
            self.active_loras[lora_request.lora_id].add(request_id)

    def remove_request(self, request_id: str, lora_request: Optional[LoRARequest]) -> None:
        """Remove request from LoRA tracking."""
        if lora_request and lora_request.lora_id in self.active_loras:
            self.active_loras[lora_request.lora_id].discard(request_id)
            if not self.active_loras[lora_request.lora_id]:
                del self.active_loras[lora_request.lora_id]

    def get_active_lora_ids(self) -> Set[int]:
        """Get currently active LoRA IDs."""
        return set(self.active_loras.keys())


class OutputProcessor:
    """
    Process EngineCoreOutputs into RequestOutputs.

    Manages per-request state, detokenization, and output streaming.
    """

    def __init__(
        self,
        tokenizer: Any = None,
        log_stats: bool = False,
        stream_interval: int = 1,
    ):
        self.tokenizer = tokenizer
        self.log_stats = log_stats
        self.stream_interval = stream_interval

        # Request states
        self.request_states: Dict[str, RequestState] = {}
        self.parent_requests: Dict[str, ParentRequest] = {}
        self.external_req_ids: Dict[str, List[str]] = defaultdict(list)

        # LoRA tracking
        self.lora_states = LoRARequestStates(log_stats)

        # Async support
        self._requests_drained = asyncio.Event()
        self._requests_drained.set()

    def get_num_unfinished_requests(self) -> int:
        """Get count of unfinished requests."""
        return len(self.request_states)

    def has_unfinished_requests(self) -> bool:
        """Check if there are unfinished requests."""
        return bool(self.request_states)

    async def wait_for_requests_to_drain(self) -> None:
        """Wait for all requests to complete."""
        if not self.request_states:
            return
        await self._requests_drained.wait()

    def propagate_error(self, e: Exception) -> None:
        """Propagate error to all request queues."""
        for request_id, state in self.request_states.items():
            if state.queue is not None:
                state.queue.put(e)  # type: ignore

    def add_request(
        self,
        request: EngineCoreRequest,
        prompt: Optional[str],
        parent_req: Optional[ParentRequest] = None,
        request_index: int = 0,
        queue: Optional[RequestOutputCollector] = None,
    ) -> None:
        """Add a new request to track."""
        request_id = request.request_id

        if request_id in self.request_states:
            raise ValueError(f"Request id {request_id} already running.")

        state = RequestState.from_new_request(
            tokenizer=self.tokenizer,
            request=request,
            prompt=prompt,
            parent_req=parent_req,
            request_index=request_index,
            queue=queue,
            log_stats=self.log_stats,
            stream_interval=self.stream_interval,
        )

        if self._requests_drained.is_set():
            self._requests_drained.clear()

        self.request_states[request_id] = state

        if parent_req:
            self.parent_requests[parent_req.request_id] = parent_req

        # Track external ID mapping
        if request.external_req_id:
            self.external_req_ids[request.external_req_id].append(request_id)

        # Track LoRA
        if request.lora_request:
            self.lora_states.add_request(request_id, request.lora_request)

        # Add queued event
        state.add_event(EventType.QUEUED)

    def abort_requests(
        self,
        request_ids: List[str],
        internal: bool = False,
    ) -> List[str]:
        """Abort requests and return list of aborted IDs."""
        aborted = []

        for request_id in request_ids:
            if request_id in self.request_states:
                state = self.request_states[request_id]
                state.add_event(EventType.ABORTED)
                state.finished = True
                state.finish_reason = "abort"

                # Emit final output
                if state.queue is not None:
                    state.queue.put(state.get_output())

                del self.request_states[request_id]
                aborted.append(request_id)

        # Check if all drained
        if not self.request_states:
            self._requests_drained.set()

        return aborted

    def process_outputs(
        self,
        engine_core_outputs: List[EngineCoreOutput],
        engine_core_timestamp: Optional[float] = None,
        iteration_stats: Optional[Any] = None,
    ) -> OutputProcessorOutput:
        """
        Process EngineCoreOutputs into RequestOutputs.

        This is the main processing loop that:
        1) Updates request states with new tokens
        2) Detokenizes if needed
        3) Creates and emits RequestOutput objects
        """
        result = OutputProcessorOutput()

        for output in engine_core_outputs:
            request_id = output.request_id

            if request_id not in self.request_states:
                logger.warning(f"Unknown request {request_id} in output")
                continue

            state = self.request_states[request_id]

            # Update state with new tokens
            # Note: In real impl, we'd detokenize here
            new_text = ""
            if self.tokenizer and output.new_token_ids:
                with contextlib.suppress(Exception):
                    new_text = self.tokenizer.decode(
                        output.new_token_ids,
                        skip_special_tokens=True,
                    )

            state.update(
                new_token_ids=output.new_token_ids,
                new_text=new_text,
                finish_reason=output.finish_reason,
            )

            # Emit output if needed
            if state.should_emit_output() or state.finished:
                request_output = state.get_output(delta=True)
                result.request_outputs.append(request_output)

                # Send to queue if present
                if state.queue is not None:
                    state.queue.put(request_output)

            # Handle finished requests
            if state.finished:
                result.finished_request_ids.add(request_id)
                del self.request_states[request_id]

        # Check if all drained
        if not self.request_states:
            self._requests_drained.set()

        return result

    def get_request_state(self, request_id: str) -> Optional[RequestState]:
        """Get state for a request."""
        return self.request_states.get(request_id)


class IterationStats:
    """Statistics for a single iteration."""

    def __init__(self):
        self.num_prompt_tokens: int = 0
        self.num_generation_tokens: int = 0
        self.num_requests: int = 0
        self.time_in_scheduler_ms: float = 0.0
        self.time_in_model_ms: float = 0.0
        self.time_in_output_proc_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "num_prompt_tokens": self.num_prompt_tokens,
            "num_generation_tokens": self.num_generation_tokens,
            "num_requests": self.num_requests,
            "time_in_scheduler_ms": self.time_in_scheduler_ms,
            "time_in_model_ms": self.time_in_model_ms,
            "time_in_output_proc_ms": self.time_in_output_proc_ms,
        }


__all__ = [
    "EventType",
    "RequestEvent",
    "LoRARequest",
    "ParentRequest",
    "SamplingParams",
    "EngineCoreRequest",
    "EngineCoreOutput",
    "EngineCoreOutputs",
    "RequestOutput",
    "OutputProcessorOutput",
    "RequestOutputCollector",
    "RequestState",
    "LoRARequestStates",
    "OutputProcessor",
    "IterationStats",
]
