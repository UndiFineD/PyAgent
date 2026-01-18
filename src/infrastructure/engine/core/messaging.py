# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""IPC and background process support for the engine core."""

import queue
from typing import Any, Optional
from .config import Request
from .engine import EngineCore
from .base import Scheduler, Executor


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
