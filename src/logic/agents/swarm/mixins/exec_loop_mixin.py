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

"""Execution loop logic for OrchestratorAgent."""

from __future__ import annotations
import logging
import asyncio

class ExecLoopMixin:
    """Mixin for parallel execution strategies and main run loops."""

    def run_with_parallel_execution(self) -> None:
        """Run the main agent loop with parallel execution strategy."""
        if not hasattr(self, "find_code_files"):
            return

        code_files = self.find_code_files()
        logging.info(f"Found {len(code_files)} code files to process")

        loop_count = getattr(self, "loop", 1)
        for loop_iteration in range(1, loop_count + 1):
            logging.info(
                f"Starting loop iteration {loop_iteration}/{loop_count}"
            )

            if getattr(self, "enable_multiprocessing", False):
                logging.info("Using multiprocessing for parallel execution")
                if hasattr(self, "process_files_multiprocessing"):
                    self.process_files_multiprocessing(code_files)
            elif getattr(self, "enable_async", False):
                logging.info("Using async for concurrent execution")
                if hasattr(self, "async_process_files"):
                    asyncio.run(self.async_process_files(code_files))
            else:
                logging.info("Using threaded execution")
                if hasattr(self, "process_files_threaded"):
                    self.process_files_threaded(code_files)

            logging.info(
                f"Completed loop iteration {loop_iteration}/{loop_count}"
            )

        if hasattr(self, "run_stats_update"):
            self.run_stats_update(code_files)

        if hasattr(self, "execute_callbacks"):
            self.execute_callbacks("agent_complete", getattr(self, "metrics", {}))
        if hasattr(self, "send_webhook_notification"):
            self.send_webhook_notification("agent_complete", getattr(self, "metrics", {}))

    def run(self) -> None:
        """Run the main agent loop."""
        if not hasattr(self, "logger"):
            from src.observability.structured_logger import StructuredLogger
            self.logger = StructuredLogger(agent_id=self.__class__.__name__)

        self.logger.info("Entering agent.run()")
        if getattr(self, "enable_async", False) or getattr(self, "enable_multiprocessing", False):
            self.run_with_parallel_execution()
        else:
            if not hasattr(self, "find_code_files"):
                return
            code_files = self.find_code_files()
            self.logger.info(
                f"Found {len(code_files)} code files to process", count=len(code_files)
            )
            loop_count = getattr(self, "loop", 1)
            for loop_iteration in range(1, loop_count + 1):
                logging.info(
                    f"Starting loop iteration {loop_iteration}/{loop_count}"
                )
                for code_file in code_files:
                    if hasattr(self, "process_file"):
                        self.process_file(code_file)
                logging.info(
                    f"Completed loop iteration {loop_iteration}/{loop_count}"
                )
            logging.info("Final stats:")
            if hasattr(self, "run_stats_update"):
                self.run_stats_update(code_files)

            if hasattr(self, "execute_callbacks"):
                self.execute_callbacks("agent_complete", getattr(self, "metrics", {}))
            if hasattr(self, "send_webhook_notification"):
                self.send_webhook_notification("agent_complete", getattr(self, "metrics", {}))
