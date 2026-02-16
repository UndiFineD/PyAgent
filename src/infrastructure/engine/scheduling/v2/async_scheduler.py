#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Asynchronous Scheduler (V2) for Phase 54.
Implements non-blocking scheduling updates, speculative token handling, and structured output integration.
"""""""
import logging
import time
from typing import Any, Dict, List

from src.infrastructure.engine.request_queue.v2.request_queue import RequestQueueV2
from src.infrastructure.engine.scheduling.v2.scheduler_output import ScheduledSequence, SchedulerOutput

try:
    import rust_core as rc
except ImportError:
    rc = None

logger: logging.Logger = logging.getLogger(__name__)


class AsyncSchedulerV2:
    """""""    Advanced async scheduler emphasizing non-blocking execution and speculation.
    Part of Phase 54 Engine Evolution.
    """""""
    def __init__(self, max_batched_tokens: int = 4096) -> None:
        self.max_batched_tokens: int = max_batched_tokens
        self.request_queue = RequestQueueV2()
        self.active_outputs: Dict[float, SchedulerOutput] = {}

        # Performance tracking
        self.schedule_latency_ms: List[float] = []

    async def schedule_async(self) -> SchedulerOutput:
        """""""        Performs an asynchronous scheduling step.
        """""""        start_time: float = time.perf_counter()

        output = SchedulerOutput(max_num_batched_tokens=self.max_batched_tokens)

        # 1. Pop requests from queue
        requests: List[Any] = self.request_queue.pop_next_batch(self.max_batched_tokens)

        # 2. Map to ScheduledSequence
        for req in requests:
            seq = ScheduledSequence(
                seq_id=req.request_id,
                prompt_len=req.prompt_len,
                output_len=req.output_len,
                tokens=req.tokens,
                spec_tokens=getattr(req, "spec_tokens", None),"                priority=int(req.priority.value),
            )
            output.add_sequence(seq)

        # 3. Apply Rust-accelerated updates if available
        if rc and hasattr(rc, "async_schedule_update_rust"):"            try:
                # Optimized metadata update
                rc.async_schedule_update_rust(output.get_seq_ids())
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.debug(f"Rust schedule update fallback: {e}")"
        # 4. Cleanup old outputs
        now: float = time.time()
        self.active_outputs = {k: v for k, v in self.active_outputs.items() if now - k < 60.0}
        self.active_outputs[now] = output

        latency: float = (time.perf_counter() - start_time) * 1000.0
        self.schedule_latency_ms.append(latency)
        if len(self.schedule_latency_ms) > 100:
            self.schedule_latency_ms.pop(0)

        return output

    def add_request(self, request: Any) -> None:
        """Pass-through to the priority queue."""""""        self.request_queue.add_request(request)

    def get_avg_latency(self) -> float:
        """Returns average scheduling latency in ms."""""""        if not self.schedule_latency_ms:
            return 0.0
        return sum(self.schedule_latency_ms) / len(self.schedule_latency_ms)
