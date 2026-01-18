"""
AsyncModelRunner: Async model execution with future-based outputs.

vLLM Pattern: GPUModelRunner from v1/worker/gpu_model_runner.py
- AsyncGPUPoolingModelRunnerOutput for non-blocking outputs
- execute_model() with scheduler_output
- _model_forward() helper

Beyond vLLM:
- Pipelined async with overlap (prefetch next batch while executing)
- Output future pooling to reduce allocation overhead
- Execution state machine for clean cancellation
"""

from __future__ import annotations
import asyncio
import logging
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Generic, Optional, TypeVar, Dict, List
import queue

logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


class RunnerState(Enum):
    """Model runner execution state."""
    IDLE = auto()        # Ready to accept work
    EXECUTING = auto()   # Currently running model forward
    WAITING = auto()     # Waiting for inputs
    CANCELLING = auto()  # Cancellation in progress
    SHUTDOWN = auto()    # Shutting down


@dataclass
class ModelInput:
    """Input for model execution."""
    request_id: str
    input_ids: list[int] = field(default_factory=list)
    attention_mask: list[int] = field(default_factory=list)
    position_ids: list[int] = field(default_factory=list)
    block_tables: list[list[int]] = field(default_factory=list)
    context_lens: list[int] = field(default_factory=list)
    num_prefill_tokens: int = 0
    num_decode_tokens: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelOutput:
    """Output from model execution."""
    request_id: str
    output_ids: list[int] = field(default_factory=list)
    logprobs: Optional[list[float]] = None
    hidden_states: Optional[list[float]] = None
    finished: bool = False
    error: Optional[str] = None
    latency_ms: float = 0.0
    tokens_generated: int = 0
    timestamp: float = field(default_factory=time.time)


@dataclass 
class SchedulerOutput:
    """Output from scheduler for model runner."""
    request_ids: list[str] = field(default_factory=list)
    inputs: list[ModelInput] = field(default_factory=list)
    num_prefill: int = 0
    num_decode: int = 0
    total_tokens: int = 0
    block_tables: dict[str, list[int]] = field(default_factory=dict)


class AsyncGPUPoolingModelRunnerOutput(Generic[T]):
    """
    Pooled async output container.
    
    vLLM Pattern: AsyncGPUPoolingModelRunnerOutput
    
    Reduces allocation overhead by reusing output objects.
    """
    
    def __init__(self, pool_size: int = 100):
        self._pool: queue.Queue[T] = queue.Queue(maxsize=pool_size)
        self._factory: Optional[Callable[[], T]] = None
        self._allocated = 0
        self._reused = 0
        self._lock = threading.Lock()
    
    def set_factory(self, factory: Callable[[], T]) -> None:
        """Set factory for creating new output objects."""
        self._factory = factory
    
    def acquire(self) -> Optional[T]:
        """Acquire output object from pool."""
        try:
            obj = self._pool.get_nowait()
            with self._lock:
                self._reused += 1
            return obj
        except queue.Empty:
            if self._factory:
                with self._lock:
                    self._allocated += 1
                return self._factory()
            return None
    
    def release(self, obj: T) -> None:
        """Return output object to pool."""
        try:
            self._pool.put_nowait(obj)
        except queue.Full:
            pass  # Pool is full, object will be GC'd
    
    def get_stats(self) -> dict[str, int]:
        """Get pool statistics."""
        with self._lock:
            return {
                "pool_size": self._pool.qsize(),
                "allocated": self._allocated,
                "reused": self._reused,
                "reuse_ratio": self._reused / max(1, self._allocated + self._reused),
            }


class ExecutionPipeline:
    """
    Pipelined execution with prefetching.
    
    Beyond vLLM: Overlap data preparation with execution.
    """
    
    def __init__(self, depth: int = 2):
        self.depth = depth
        self._stages: list[asyncio.Queue[SchedulerOutput]] = [
            asyncio.Queue(maxsize=depth) for _ in range(2)
        ]
        self._prefetch_stage = self._stages[0]
        self._execute_stage = self._stages[1]
        self._running = False
    
    async def submit(self, scheduler_output: SchedulerOutput) -> None:
        """Submit work to pipeline."""
        await self._prefetch_stage.put(scheduler_output)
    
    async def get_next_batch(self) -> Optional[SchedulerOutput]:
        """Get next batch ready for execution."""
        try:
            return await asyncio.wait_for(
                self._execute_stage.get(),
                timeout=0.01
            )
        except asyncio.TimeoutError:
            return None
    
    async def run_prefetch_loop(
        self,
        prefetch_fn: Callable[[SchedulerOutput], SchedulerOutput]
    ) -> None:
        """Run prefetch stage of pipeline."""
        self._running = True
        
        while self._running:
            try:
                batch = await asyncio.wait_for(
                    self._prefetch_stage.get(),
                    timeout=0.1
                )
                
                # Prefetch (e.g., copy to GPU, prepare tensors)
                prefetched = prefetch_fn(batch)
                
                await self._execute_stage.put(prefetched)
                
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break
    
    def stop(self) -> None:
        """Stop pipeline."""
        self._running = False


class AsyncModelRunner:
    """
    Async model execution runner.
    
    vLLM Pattern: GPUModelRunner from gpu_model_runner.py
    
    Beyond vLLM:
    - Pipelined async with overlap
    - Output future pooling
    - Clean cancellation via state machine
    """
    
    def __init__(
        self,
        model_forward_fn: Optional[Callable[[ModelInput], ModelOutput]] = None,
        num_workers: int = 1,
        enable_pipeline: bool = True
    ):
        self._model_forward_fn = model_forward_fn
        self._state = RunnerState.IDLE
        
        # Output pool
        self._output_pool: AsyncGPUPoolingModelRunnerOutput[ModelOutput] = \
            AsyncGPUPoolingModelRunnerOutput(pool_size=100)
        self._output_pool.set_factory(lambda: ModelOutput(request_id=""))
        
        # Execution pipeline
        self._enable_pipeline = enable_pipeline
        self._pipeline: Optional[ExecutionPipeline] = None
        if enable_pipeline:
            self._pipeline = ExecutionPipeline(depth=2)
        
        # Pending futures
        self._pending_futures: dict[str, asyncio.Future[ModelOutput]] = {}
        
        # Thread pool for sync execution
        self._executor = ThreadPoolExecutor(max_workers=num_workers)
        
        # Metrics
        self._total_executions = 0
        self._total_tokens = 0
        self._total_latency_ms = 0.0
        
        self._lock = threading.RLock()
        
        logger.info(f"AsyncModelRunner initialized (pipeline={enable_pipeline})")
    
    def set_model_forward(self, fn: Callable[[ModelInput], ModelOutput]) -> None:
        """Set the model forward function."""
        self._model_forward_fn = fn
    
    async def execute_model_async(
        self,
        scheduler_output: SchedulerOutput
    ) -> list[ModelOutput]:
        """
        Execute model on scheduled batch (async).
        
        vLLM Pattern: execute_model() with scheduler_output
        """
        with self._lock:
            if self._state == RunnerState.SHUTDOWN:
                raise RuntimeError("Runner is shutdown")
            self._state = RunnerState.EXECUTING
        
        try:
            outputs = []
            
            for model_input in scheduler_output.inputs:
                output = await self._execute_single_async(model_input)
                outputs.append(output)
            
            with self._lock:
                self._total_executions += 1
                self._total_tokens += scheduler_output.total_tokens
            
            return outputs
            
        finally:
            with self._lock:
                if self._state != RunnerState.SHUTDOWN:
                    self._state = RunnerState.IDLE
    
    async def _execute_single_async(self, model_input: ModelInput) -> ModelOutput:
        """Execute single model input asynchronously."""
        request_id = model_input.request_id
        
        # Create future
        loop = asyncio.get_event_loop()
        future: asyncio.Future[ModelOutput] = loop.create_future()
        self._pending_futures[request_id] = future
        
        try:
            # Run in thread pool
            output = await loop.run_in_executor(
                self._executor,
                self._model_forward,
                model_input
            )
            
            if not future.done():
                future.set_result(output)
            
            return output
            
        except Exception as e:
            error_output = self._output_pool.acquire()
            if error_output:
                error_output.request_id = request_id
                error_output.error = str(e)
            else:
                error_output = ModelOutput(request_id=request_id, error=str(e))
            
            if not future.done():
                future.set_result(error_output)
            
            return error_output
            
        finally:
            self._pending_futures.pop(request_id, None)
    
    def _model_forward(self, model_input: ModelInput) -> ModelOutput:
        """
        Execute model forward pass.
        
        vLLM Pattern: _model_forward() helper
        """
        start_time = time.perf_counter()
        
        if self._model_forward_fn is not None:
            output = self._model_forward_fn(model_input)
        else:
            # Mock execution for testing
            output = self._output_pool.acquire()
            if output is None:
                output = ModelOutput(request_id=model_input.request_id)
            
            output.request_id = model_input.request_id
            output.output_ids = [1001, 1002, 1003]  # Mock tokens
            output.finished = True
            output.error = None
        
        latency_ms = (time.perf_counter() - start_time) * 1000
        output.latency_ms = latency_ms
        output.tokens_generated = len(output.output_ids)
        
        with self._lock:
            self._total_latency_ms += latency_ms
        
        return output
    
    def execute_model_sync(
        self,
        scheduler_output: SchedulerOutput
    ) -> list[ModelOutput]:
        """Execute model synchronously."""
        outputs = []
        
        for model_input in scheduler_output.inputs:
            output = self._model_forward(model_input)
            outputs.append(output)
        
        with self._lock:
            self._total_executions += 1
            self._total_tokens += scheduler_output.total_tokens
        
        return outputs
    
    async def get_output_async(
        self,
        request_id: str,
        timeout_ms: Optional[int] = None
    ) -> Optional[ModelOutput]:
        """Get output for request (async)."""
        if request_id not in self._pending_futures:
            return None
        
        timeout = (timeout_ms or 30000) / 1000.0
        
        try:
            return await asyncio.wait_for(
                self._pending_futures[request_id],
                timeout=timeout
            )
        except asyncio.TimeoutError:
            return None
    
    def cancel_request(self, request_id: str) -> bool:
        """Cancel pending request."""
        if request_id not in self._pending_futures:
            return False
        
        future = self._pending_futures.pop(request_id)
        if not future.done():
            future.cancel()
        
        return True
    
    def cancel_all(self) -> int:
        """Cancel all pending requests."""
        with self._lock:
            self._state = RunnerState.CANCELLING
        
        cancelled = 0
        for request_id in list(self._pending_futures.keys()):
            if self.cancel_request(request_id):
                cancelled += 1
        
        with self._lock:
            self._state = RunnerState.IDLE
        
        return cancelled
    
    def return_output(self, output: ModelOutput) -> None:
        """Return output to pool for reuse."""
        self._output_pool.release(output)
    
    def shutdown(self) -> None:
        """Shutdown runner."""
        with self._lock:
            self._state = RunnerState.SHUTDOWN
        
        self.cancel_all()
        
        if self._pipeline:
            self._pipeline.stop()
        
        self._executor.shutdown(wait=False)
        
        logger.info("AsyncModelRunner shutdown")
    
    def get_metrics(self) -> dict[str, Any]:
        """Get runner metrics."""
        with self._lock:
            avg_latency = (
                self._total_latency_ms / self._total_executions
                if self._total_executions > 0 else 0.0
            )
            
            return {
                "state": self._state.name,
                "total_executions": self._total_executions,
                "total_tokens": self._total_tokens,
                "total_latency_ms": self._total_latency_ms,
                "avg_latency_ms": avg_latency,
                "pending_requests": len(self._pending_futures),
                "output_pool": self._output_pool.get_stats(),
            }
    
    @property
    def state(self) -> RunnerState:
        """Get current state."""
        return self._state
    
    @property
    def is_idle(self) -> bool:
        """Check if runner is idle."""
        return self._state == RunnerState.IDLE


class BatchedAsyncRunner:
    """
    Batched async runner with automatic batching.
    
    Beyond vLLM: Automatic micro-batching for efficiency.
    """
    
    def __init__(
        self,
        runner: AsyncModelRunner,
        max_batch_size: int = 32,
        batch_timeout_ms: float = 5.0
    ):
        self._runner = runner
        self._max_batch_size = max_batch_size
        self._batch_timeout_ms = batch_timeout_ms
        
        self._pending_inputs: list[ModelInput] = []
        self._pending_futures: list[asyncio.Future[ModelOutput]] = []
        
        self._batch_task: Optional[asyncio.Task] = None
        self._running = False
        self._lock = asyncio.Lock()
    
    async def submit(self, model_input: ModelInput) -> asyncio.Future[ModelOutput]:
        """Submit input for batched execution."""
        loop = asyncio.get_event_loop()
        future: asyncio.Future[ModelOutput] = loop.create_future()
        
        async with self._lock:
            self._pending_inputs.append(model_input)
            self._pending_futures.append(future)
            
            # Flush if batch is full
            if len(self._pending_inputs) >= self._max_batch_size:
                await self._flush_batch()
        
        return future
    
    async def _flush_batch(self) -> None:
        """Execute pending batch."""
        if not self._pending_inputs:
            return
        
        inputs = self._pending_inputs
        futures = self._pending_futures
        
        self._pending_inputs = []
        self._pending_futures = []
        
        scheduler_output = SchedulerOutput(
            request_ids=[inp.request_id for inp in inputs],
            inputs=inputs,
            total_tokens=sum(len(inp.input_ids) for inp in inputs)
        )
        
        try:
            outputs = await self._runner.execute_model_async(scheduler_output)
            
            for future, output in zip(futures, outputs):
                if not future.done():
                    future.set_result(output)
                    
        except Exception as e:
            for future in futures:
                if not future.done():
                    error_output = ModelOutput(
                        request_id="error",
                        error=str(e)
                    )
                    future.set_result(error_output)
    
    async def run_batch_loop(self) -> None:
        """Run batching loop with timeout-based flushing."""
        self._running = True
        
        while self._running:
            try:
                await asyncio.sleep(self._batch_timeout_ms / 1000.0)
                
                async with self._lock:
                    if self._pending_inputs:
                        await self._flush_batch()
                        
            except asyncio.CancelledError:
                break
    
    def start(self) -> None:
        """Start batching loop."""
        loop = asyncio.get_event_loop()
        self._batch_task = loop.create_task(self.run_batch_loop())
    
    async def stop(self) -> None:
        """Stop batching loop."""
        self._running = False
        
        if self._batch_task:
            self._batch_task.cancel()
            try:
                await self._batch_task
            except asyncio.CancelledError:
                pass
        
        # Flush any remaining
        async with self._lock:
            await self._flush_batch()


# Convenience exports
__all__ = [
    "RunnerState",
    "ModelInput",
    "ModelOutput",
    "SchedulerOutput",
    "AsyncGPUPoolingModelRunnerOutput",
    "ExecutionPipeline",
    "AsyncModelRunner",
    "BatchedAsyncRunner",
]
