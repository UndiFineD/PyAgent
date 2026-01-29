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
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Core async model runner implementation."""

import asyncio
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Optional

from .config import ModelInput, ModelOutput, RunnerState, SchedulerOutput
from .pipeline import ExecutionPipeline
from .pooling import AsyncGPUPoolingModelRunnerOutput

logger = logging.getLogger(__name__)


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
        enable_pipeline: bool = True,
    ) -> None:
        self._model_forward_fn = model_forward_fn
        self._state = RunnerState.IDLE

        # Output pool
        self._output_pool: AsyncGPUPoolingModelRunnerOutput[ModelOutput] = AsyncGPUPoolingModelRunnerOutput(
            pool_size=100
        )
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

    async def execute_model_async(self, scheduler_output: SchedulerOutput) -> List[ModelOutput]:
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
            output = await loop.run_in_executor(self._executor, self._model_forward, model_input)

            if not future.done():
                future.set_result(output)

            return output

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
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

        if self._model_forward_fn:
            output = self._model_forward_fn(model_input)
        else:
            # Mock execution for testing
            output = self._output_pool.acquire()
            if not output:
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

    def execute_model_sync(self, scheduler_output: SchedulerOutput) -> List[ModelOutput]:
        """Execute model synchronously."""
        outputs = []

        for model_input in scheduler_output.inputs:
            output = self._model_forward(model_input)
            outputs.append(output)

        with self._lock:
            self._total_executions += 1
            self._total_tokens += scheduler_output.total_tokens

        return outputs

    async def get_output_async(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[ModelOutput]:
        """Get output for request (async)."""
        if request_id not in self._pending_futures:
            return None

        timeout = (timeout_ms or 30000) / 1000.0

        try:
            return await asyncio.wait_for(self._pending_futures[request_id], timeout=timeout)
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

    def get_metrics(self) -> Dict[str, Any]:
        """Get runner metrics."""
        with self._lock:
            avg_latency = self._total_latency_ms / self._total_executions if self._total_executions else 0.0

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
