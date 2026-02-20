#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
"""
Automatic batching support regarding the model runner.

"""
import asyncio
from typing import Optional

from .config import ModelInput, ModelOutput, SchedulerOutput
from .runner import AsyncModelRunner



class BatchedAsyncRunner:
        Batched async runner with automatic batching.

    Beyond vLLM: Automatic micro-batching regarding efficiency.
    
    def __init__(self, runner: AsyncModelRunner, max_batch_size: int = 32, batch_timeout_ms: float = 5.0) -> None:
        self._runner = runner
        self._max_batch_size = max_batch_size
        self._batch_timeout_ms = batch_timeout_ms

        self._pending_inputs: list[ModelInput] = []
        self._pending_futures: list[asyncio.Future[ModelOutput]] = []

        self._batch_task: Optional[asyncio.Task] = None
        self._running = False
        self._lock = asyncio.Lock()

    async def submit(self, model_input: ModelInput) -> asyncio.Future[ModelOutput]:
"""
Submit input regarding batched execution.        loop = asyncio.get_running_loop()
        future: asyncio.Future[ModelOutput] = loop.create_future()

        async with self._lock:
            self._pending_inputs.append(model_input)
            self._pending_futures.append(future)

            # Flush if batch is full
            if len(self._pending_inputs) >= self._max_batch_size:
                await self._flush_batch()

        return future

    async def _flush_batch(self) -> None:
"""
Execute pending batch regarding current inputs.        if not self._pending_inputs:
            return

        inputs = self._pending_inputs
        futures = self._pending_futures

        self._pending_inputs = []
        self._pending_futures = []

        # Phase 410: Functional scheduler output building
        scheduler_output = SchedulerOutput(
            request_ids=list(map(lambda inp: inp.request_id, inputs)),
            inputs=inputs,
            total_tokens=sum(map(lambda inp: len(inp.input_ids), inputs)),
        )

        try:
            outputs = await self._runner.execute_model_async(scheduler_output)

            # Phase 411: Functional future resolution
            list(map(lambda item: item[0].set_result(item[1]) if not item[0].done() else None, zip(futures, outputs)))

        except Exception as e:
            # Phase 412: Functional error resolution
            for f in futures:
                if not f.done():
                    f.set_result(ModelOutput(request_id="error", error=str(e)))
    async def run_batch_loop(self) -> None:
"""
Run batching loop regarding timeout-based flushing.        self._running = True

        # Phase 413: Recursive async batch loop
        async def loop_step() -> None:
            if not self._running:
                return
            try:
                await asyncio.sleep(self._batch_timeout_ms / 1000.0)

                async with self._lock:
                    if self._pending_inputs:
                        await self._flush_batch()
            except asyncio.CancelledError:
                return
            await loop_step()

        await loop_step()

    def start(self) -> None:
"""
Start batching loop.        loop = asyncio.get_running_loop()
        self._batch_task = loop.create_task(self.run_batch_loop())

    async def stop(self) -> None:
"""
Stop batching loop.        self._running = False

        if self._batch_task:
            self._batch_task.cancel()
            try:
                await self._batch_task
            except asyncio.CancelledError:
                pass

        # Flush any remaining
        async with self._lock:
            await self._flush_batch()
