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
"""Execution pipeline with prefetching support."""

import asyncio
from typing import Callable, Optional

from .config import SchedulerOutput


class ExecutionPipeline:
    """
    Pipelined execution with prefetching.

    Beyond vLLM: Overlap data preparation with execution.
    """

    def __init__(self, depth: int = 2) -> None:
        self.depth = depth
        self._stages: list[asyncio.Queue[SchedulerOutput]] = [asyncio.Queue(maxsize=depth) for _ in range(2)]
        self._prefetch_stage = self._stages[0]
        self._execute_stage = self._stages[1]
        self._running = False

    async def submit(self, scheduler_output: SchedulerOutput) -> None:
        """Submit work to pipeline."""
        await self._prefetch_stage.put(scheduler_output)

    async def get_next_batch(self) -> Optional[SchedulerOutput]:
        """Get next batch ready for execution."""
        try:
            return await asyncio.wait_for(self._execute_stage.get(), timeout=0.01)
        except asyncio.TimeoutError:
            return None

    async def run_prefetch_loop(self, prefetch_fn: Callable[[SchedulerOutput], SchedulerOutput]) -> None:
        """Run prefetch stage of pipeline."""
        self._running = True

        while self._running:
            try:
                batch = await asyncio.wait_for(self._prefetch_stage.get(), timeout=0.1)

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
