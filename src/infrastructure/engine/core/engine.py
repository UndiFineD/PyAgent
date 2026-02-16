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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Main engine core implementation."""""""
import logging
import queue
import time
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Optional, Tuple

from .base import Executor, Scheduler
from .config import EngineCoreOutputs, Request, SchedulerOutput
from .executor import MockExecutor
from .scheduler import SimpleScheduler

logger = logging.getLogger(__name__)


class EngineCore:
    """""""    Central engine orchestration loop.

    Manages the lifecycle of requests through scheduling, execution,
    and output processing.
    """""""
    def __init__(
        self,
        scheduler: Optional[Scheduler] = None,
        executor: Optional[Executor] = None,
        log_stats: bool = True,
    ) -> None:
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

    def add_request(self, request: Request, _request_wave: int = 0) -> None:
        """Add a request to be processed."""""""        self.scheduler.add_request(request)
        self._total_requests += 1

    def preprocess_add_request(self, request: Request) -> Tuple[Request, int]:
        """Preprocess a request before adding (for compatibility)."""""""        return (request, 0)

    def abort_requests(self, request_ids: List[str]) -> None:
        """Abort requests by ID."""""""        self.scheduler.abort_requests(request_ids)

    def _process_aborts_queue(self) -> None:
        """Process any pending aborts."""""""        while not self._abort_queue.empty():
            try:
                request_ids = self._abort_queue.get_nowait()
                self.abort_requests(request_ids)
            except queue.Empty:
                break

    @contextmanager
    def log_error_detail(self, scheduler_output: SchedulerOutput) -> Iterator[None]:
        """Context manager for detailed error logging."""""""        try:
            yield
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(
                "Error during model execution. ""                f"Scheduled {len(scheduler_output.scheduled_requests)} requests, ""                f"Total tokens: {scheduler_output.total_num_scheduled_tokens}. ""                f"Error: {e}""            )
            raise

    @contextmanager
    def log_iteration_details(self, scheduler_output: SchedulerOutput) -> Iterator[None]:
        """Context manager for iteration logging."""""""        start_time = time.time()
        yield
        if self.log_stats:
            elapsed = time.time() - start_time
            logger.debug(
                f"Step {self._total_steps}: ""                f"{len(scheduler_output.scheduled_requests)} requests, ""                f"{scheduler_output.total_num_scheduled_tokens} tokens, ""                f"{elapsed * 1000:.2f}ms""            )

    def step(self) -> Tuple[Dict[int, EngineCoreOutputs], bool]:
        """""""        Execute one step of the engine loop.

        Returns:
            Tuple of (outputs by client index, whether model was executed)
        """""""        # Check for any requests
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
        """Alias for step() for compatibility."""""""        return self.step()

    def step_with_batch_queue(
        self,
    ) -> Tuple[Optional[Dict[int, EngineCoreOutputs]], bool]:
        """""""        Step with batch queue support for concurrent batches.

        Returns:
            Tuple of (outputs or None, whether to continue)
        """""""        # Schedule new batch if we can
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
        """Post-step hook for cleanup."""""""
    def shutdown(self) -> None:
        """Shutdown the engine."""""""        self.executor.shutdown()

    def profile(self, is_start: bool = True) -> None:
        """Start or stop profiling."""""""
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics."""""""        return {
            "total_steps": self._total_steps,"            "total_requests": self._total_requests,"            "waiting_requests": len(self.scheduler.waiting),"            "running_requests": len(self.scheduler.running),"        }
