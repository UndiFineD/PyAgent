"""
EngineCore - Central engine orchestration loop.

Inspired by vLLM's v1/engine/core.py - implements the main execution loop
for scheduling, executing, and processing model outputs.
"""

from __future__ import annotations

import time
import threading
import queue
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, Iterator, List, Optional, Set, Tuple
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class RequestStatus(Enum):
    """Status of a request in the engine."""
    WAITING = auto()
    RUNNING = auto()
    FINISHED = auto()
    ABORTED = auto()
    PREEMPTED = auto()
    WAITING_FOR_REMOTE = auto()


class FinishReason(Enum):
    """Reason why a request finished."""
    STOP = auto()
    LENGTH = auto()
    ABORT = auto()
    ERROR = auto()
    EOS = auto()


@dataclass
class Request:
    """A request to be processed by the engine."""
    request_id: str
    prompt_token_ids: List[int]
    sampling_params: Optional[Dict[str, Any]] = None
    arrival_time: float = field(default_factory=time.time)
    status: RequestStatus = RequestStatus.WAITING
    num_tokens: int = 0
    num_computed_tokens: int = 0
    output_token_ids: List[int] = field(default_factory=list)
    finish_reason: Optional[FinishReason] = None
    client_index: int = 0
    lora_request: Optional[Any] = None
    cache_salt: Optional[str] = None
    trace_headers: Optional[Dict[str, str]] = None
    
    def __post_init__(self):
        self.num_tokens = len(self.prompt_token_ids)
    
    def get_finished_reason(self) -> Optional[FinishReason]:
        """Get the reason why this request finished."""
        return self.finish_reason
    
    def is_finished(self) -> bool:
        """Check if request is finished."""
        return self.status in (RequestStatus.FINISHED, RequestStatus.ABORTED)


@dataclass
class SchedulerOutput:
    """Output from the scheduler containing batch info."""
    scheduled_requests: List[Request] = field(default_factory=list)
    num_scheduled_tokens: Dict[str, int] = field(default_factory=dict)
    total_num_scheduled_tokens: int = 0
    num_prefill_tokens: int = 0
    num_decode_tokens: int = 0
    preempted_requests: List[Request] = field(default_factory=list)
    
    def is_empty(self) -> bool:
        """Check if no requests were scheduled."""
        return self.total_num_scheduled_tokens == 0


@dataclass
class ModelRunnerOutput:
    """Output from the model runner."""
    req_ids: List[str] = field(default_factory=list)
    req_id_to_index: Dict[str, int] = field(default_factory=dict)
    sampled_token_ids: List[List[int]] = field(default_factory=list)
    logprobs: Optional[List[Any]] = None
    prompt_logprobs_dict: Dict[str, Any] = field(default_factory=dict)
    pooler_output: List[Any] = field(default_factory=list)
    
    @classmethod
    def empty(cls) -> "ModelRunnerOutput":
        """Create an empty output."""
        return cls()


@dataclass
class EngineCoreOutput:
    """Output for a single request."""
    request_id: str
    new_token_ids: List[int] = field(default_factory=list)
    finish_reason: Optional[FinishReason] = None
    new_logprobs: Optional[List[Any]] = None
    pooling_output: Optional[Any] = None
    stop_reason: Optional[str] = None


@dataclass
class EngineCoreOutputs:
    """Batch of outputs from the engine core."""
    outputs: List[EngineCoreOutput] = field(default_factory=list)
    scheduler_stats: Optional[Dict[str, Any]] = None
    timestamp: float = field(default_factory=time.time)
    finished_requests: Optional[Set[str]] = None


class Scheduler(ABC):
    """Abstract scheduler interface."""
    
    def __init__(self):
        self.waiting: List[Request] = []
        self.running: List[Request] = []
        self.requests: Dict[str, Request] = {}
        self.finished_req_ids: Set[str] = set()
    
    @abstractmethod
    def schedule(self) -> SchedulerOutput:
        """Schedule requests for execution."""
        raise NotImplementedError
    
    def add_request(self, request: Request) -> None:
        """Add a request to the scheduler."""
        self.waiting.append(request)
        self.requests[request.request_id] = request
    
    def abort_requests(self, request_ids: List[str]) -> None:
        """Abort requests by ID."""
        for req_id in request_ids:
            if req_id in self.requests:
                request = self.requests[req_id]
                request.status = RequestStatus.ABORTED
                request.finish_reason = FinishReason.ABORT
                # Remove from waiting/running
                self.waiting = [r for r in self.waiting if r.request_id != req_id]
                self.running = [r for r in self.running if r.request_id != req_id]
                self.finished_req_ids.add(req_id)
    
    def finish_requests(self, request_ids: Set[str], reason: FinishReason) -> None:
        """Mark requests as finished."""
        for req_id in request_ids:
            if req_id in self.requests:
                request = self.requests[req_id]
                request.status = RequestStatus.FINISHED
                request.finish_reason = reason
                self.running = [r for r in self.running if r.request_id != req_id]
                self.finished_req_ids.add(req_id)
    
    def has_requests(self) -> bool:
        """Check if there are unfinished requests."""
        return len(self.waiting) > 0 or len(self.running) > 0
    
    def has_unfinished_requests(self) -> bool:
        """Alias for has_requests."""
        return self.has_requests()
    
    def has_finished_requests(self) -> bool:
        """Check if there are finished requests to report."""
        return len(self.finished_req_ids) > 0
    
    def get_num_unfinished_requests(self) -> int:
        """Get count of unfinished requests."""
        return len(self.waiting) + len(self.running)
    
    def update_from_output(
        self,
        scheduler_output: SchedulerOutput,
        model_output: ModelRunnerOutput,
    ) -> Dict[int, EngineCoreOutputs]:
        """Update scheduler state from model output."""
        outputs_by_client: Dict[int, List[EngineCoreOutput]] = {}
        
        for i, req_id in enumerate(model_output.req_ids):
            if req_id not in self.requests:
                continue
            
            request = self.requests[req_id]
            tokens = model_output.sampled_token_ids[i] if i < len(model_output.sampled_token_ids) else []
            
            # Update request state
            request.output_token_ids.extend(tokens)
            request.num_tokens += len(tokens)
            
            # Create output
            output = EngineCoreOutput(
                request_id=req_id,
                new_token_ids=tokens,
                finish_reason=request.finish_reason,
            )
            
            client_idx = request.client_index
            if client_idx not in outputs_by_client:
                outputs_by_client[client_idx] = []
            outputs_by_client[client_idx].append(output)
        
        # Package outputs
        result = {}
        for client_idx, outputs in outputs_by_client.items():
            result[client_idx] = EngineCoreOutputs(outputs=outputs)
        
        return result


class SimpleScheduler(Scheduler):
    """Simple FCFS scheduler implementation."""
    
    def __init__(self, max_batch_size: int = 32, max_tokens: int = 4096):
        super().__init__()
        self.max_batch_size = max_batch_size
        self.max_tokens = max_tokens
    
    def schedule(self) -> SchedulerOutput:
        """Schedule waiting requests for execution."""
        output = SchedulerOutput()
        
        # Move waiting to running up to batch size
        total_tokens = sum(r.num_tokens - r.num_computed_tokens for r in self.running)
        
        while self.waiting and len(self.running) < self.max_batch_size:
            request = self.waiting[0]
            tokens_needed = request.num_tokens - request.num_computed_tokens
            
            if total_tokens + tokens_needed > self.max_tokens:
                break
            
            self.waiting.pop(0)
            request.status = RequestStatus.RUNNING
            self.running.append(request)
            total_tokens += tokens_needed
        
        # Build output
        for request in self.running:
            output.scheduled_requests.append(request)
            tokens = request.num_tokens - request.num_computed_tokens
            output.num_scheduled_tokens[request.request_id] = tokens
            output.total_num_scheduled_tokens += tokens
            
            if request.num_computed_tokens == 0:
                output.num_prefill_tokens += tokens
            else:
                output.num_decode_tokens += tokens
        
        return output


class Executor(ABC):
    """Abstract executor for running model inference."""
    
    @abstractmethod
    def execute_model(
        self,
        scheduler_output: SchedulerOutput,
    ) -> ModelRunnerOutput:
        """Execute model on scheduled batch."""
        raise NotImplementedError
    
    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the executor."""
        raise NotImplementedError


class MockExecutor(Executor):
    """Mock executor for testing."""
    
    def __init__(self, tokens_per_step: int = 1):
        self.tokens_per_step = tokens_per_step
    
    def execute_model(
        self,
        scheduler_output: SchedulerOutput,
    ) -> ModelRunnerOutput:
        """Generate mock tokens."""
        output = ModelRunnerOutput()
        
        for request in scheduler_output.scheduled_requests:
            output.req_ids.append(request.request_id)
            output.req_id_to_index[request.request_id] = len(output.req_ids) - 1
            # Generate mock tokens
            output.sampled_token_ids.append([1000] * self.tokens_per_step)
        
        return output
    
    def shutdown(self) -> None:
        """No-op shutdown."""
        pass


class EngineCore:
    """
    Central engine orchestration loop.
    
    Manages the lifecycle of requests through scheduling, execution,
    and output processing.
    """
    
    def __init__(
        self,
        scheduler: Optional[Scheduler] = None,
        executor: Optional[Executor] = None,
        log_stats: bool = True,
    ):
        self.scheduler = scheduler or SimpleScheduler()
        self.executor = executor or MockExecutor()
        self.log_stats = log_stats
        
        # Batch queue for concurrent batch support
        self.batch_queue: List[Tuple[Any, SchedulerOutput, Any]] = []
        
        # Abort queue for async aborts
        self._abort_queue: queue.Queue = queue.Queue()
        
        # Statistics
        self._total_steps = 0
        self._total_requests = 0
    
    def add_request(self, request: Request, request_wave: int = 0) -> None:
        """Add a request to be processed."""
        self.scheduler.add_request(request)
        self._total_requests += 1
    
    def preprocess_add_request(self, request: Request) -> Tuple[Request, int]:
        """Preprocess a request before adding (for compatibility)."""
        return (request, 0)
    
    def abort_requests(self, request_ids: List[str]) -> None:
        """Abort requests by ID."""
        self.scheduler.abort_requests(request_ids)
    
    def _process_aborts_queue(self) -> None:
        """Process any pending aborts."""
        while not self._abort_queue.empty():
            try:
                request_ids = self._abort_queue.get_nowait()
                self.abort_requests(request_ids)
            except queue.Empty:
                break
    
    @contextmanager
    def log_error_detail(self, scheduler_output: SchedulerOutput):
        """Context manager for detailed error logging."""
        try:
            yield
        except Exception as e:
            logger.error(
                "Error during model execution. "
                f"Scheduled {len(scheduler_output.scheduled_requests)} requests, "
                f"Total tokens: {scheduler_output.total_num_scheduled_tokens}. "
                f"Error: {e}"
            )
            raise
    
    @contextmanager
    def log_iteration_details(self, scheduler_output: SchedulerOutput):
        """Context manager for iteration logging."""
        start_time = time.time()
        yield
        if self.log_stats:
            elapsed = time.time() - start_time
            logger.debug(
                f"Step {self._total_steps}: "
                f"{len(scheduler_output.scheduled_requests)} requests, "
                f"{scheduler_output.total_num_scheduled_tokens} tokens, "
                f"{elapsed*1000:.2f}ms"
            )
    
    def step(self) -> Tuple[Dict[int, EngineCoreOutputs], bool]:
        """
        Execute one step of the engine loop.
        
        Returns:
            Tuple of (outputs by client index, whether model was executed)
        """
        # Check for any requests
        if not self.scheduler.has_requests():
            return {}, False
        
        # Schedule batch
        scheduler_output = self.scheduler.schedule()
        
        if scheduler_output.is_empty():
            return {}, False
        
        # Execute model
        with self.log_error_detail(scheduler_output):
            with self.log_iteration_details(scheduler_output):
                model_output = self.executor.execute_model(scheduler_output)
        
        # Process aborts that happened during execution
        self._process_aborts_queue()
        
        # Update scheduler and get outputs
        outputs = self.scheduler.update_from_output(scheduler_output, model_output)
        
        self._total_steps += 1
        
        return outputs, True
    
    def step_fn(self) -> Tuple[Dict[int, EngineCoreOutputs], bool]:
        """Alias for step() for compatibility."""
        return self.step()
    
    def step_with_batch_queue(
        self,
    ) -> Tuple[Optional[Dict[int, EngineCoreOutputs]], bool]:
        """
        Step with batch queue support for concurrent batches.
        
        Returns:
            Tuple of (outputs or None, whether to continue)
        """
        # Schedule new batch if we can
        if self.scheduler.has_requests():
            scheduler_output = self.scheduler.schedule()
            if not scheduler_output.is_empty():
                # Execute and queue result
                model_output = self.executor.execute_model(scheduler_output)
                self.batch_queue.append((model_output, scheduler_output, None))
        
        # Process completed batches
        if self.batch_queue:
            model_output, scheduler_output, _ = self.batch_queue.pop(0)
            outputs = self.scheduler.update_from_output(scheduler_output, model_output)
            return outputs, True
        
        return None, False
    
    def post_step(self, model_executed: bool = True) -> None:
        """Post-step hook for cleanup."""
        pass
    
    def shutdown(self) -> None:
        """Shutdown the engine."""
        self.executor.shutdown()
    
    def profile(self, is_start: bool = True) -> None:
        """Start or stop profiling."""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics."""
        return {
            "total_steps": self._total_steps,
            "total_requests": self._total_requests,
            "waiting_requests": len(self.scheduler.waiting),
            "running_requests": len(self.scheduler.running),
        }


class EngineCoreProc(EngineCore):
    """
    ZMQ-wrapper for running EngineCore in a background process.
    """
    
    def __init__(
        self,
        scheduler: Optional[Scheduler] = None,
        executor: Optional[Executor] = None,
        log_stats: bool = True,
        engine_index: int = 0,
    ):
        super().__init__(scheduler, executor, log_stats)
        self.engine_index = engine_index
        self.engines_running = False
        
        # Queues for IPC
        self.input_queue: queue.Queue = queue.Queue()
        self.output_queue: queue.Queue = queue.Queue()
    
    def _process_engine_step(self) -> bool:
        """Process one engine step and queue outputs."""
        outputs, model_executed = self.step()
        
        for client_idx, engine_outputs in outputs.items():
            self.output_queue.put_nowait((client_idx, engine_outputs))
        
        self.post_step(model_executed)
        return model_executed
    
    def run_loop(self) -> None:
        """Main engine loop for background process."""
        self.engines_running = True
        
        try:
            while self.engines_running:
                # Process input requests
                try:
                    request_type, request_data = self.input_queue.get(timeout=0.1)
                    self._handle_request(request_type, request_data)
                except queue.Empty:
                    pass
                
                # Step if we have work
                if self.scheduler.has_requests():
                    self._process_engine_step()
        finally:
            self.engines_running = False
    
    def _handle_request(self, request_type: str, request_data: Any) -> None:
        """Handle incoming request."""
        if request_type == "add":
            self.add_request(request_data)
        elif request_type == "abort":
            self.abort_requests(request_data)
        elif request_type == "shutdown":
            self.engines_running = False


# Utility functions
def create_engine_core(
    max_batch_size: int = 32,
    max_tokens: int = 4096,
    log_stats: bool = True,
) -> EngineCore:
    """Create an EngineCore with default settings."""
    scheduler = SimpleScheduler(max_batch_size=max_batch_size, max_tokens=max_tokens)
    executor = MockExecutor()
    return EngineCore(scheduler=scheduler, executor=executor, log_stats=log_stats)


__all__ = [
    "RequestStatus",
    "FinishReason",
    "Request",
    "SchedulerOutput",
    "ModelRunnerOutput",
    "EngineCoreOutput",
    "EngineCoreOutputs",
    "Scheduler",
    "SimpleScheduler",
    "Executor",
    "MockExecutor",
    "EngineCore",
    "EngineCoreProc",
    "create_engine_core",
]
