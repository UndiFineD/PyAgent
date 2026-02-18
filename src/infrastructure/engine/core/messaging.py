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
# See the License for the specific language governing permissions and
# limitations under the License.


"""IPC and background process support for the engine core."""


import queue
from typing import Any, Optional

from .base import Executor, Scheduler
from .engine import EngineCore


class EngineCoreProc(EngineCore):
    """ZMQ-wrapper for running EngineCore in a background process."""
    
    def __init__(
        self,
        scheduler: Optional[Scheduler] = None,
        executor: Optional[Executor] = None,
        log_stats: bool = True,
        engine_index: int = 0,
    ) -> None:
        """Initialize the engine core process."""
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
        # Main engine loop for background process
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
