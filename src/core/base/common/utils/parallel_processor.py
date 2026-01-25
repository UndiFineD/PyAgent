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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Manager for parallel execution.
(Facade for src.core.base.common.execution_core)
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import Any, Callable

try:
    from tqdm import tqdm

    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

from src.core.base.common.execution_core import ExecutionCore


class ParallelProcessor:
    """
    Facade for parallel execution utilities.
    Uses ExecutionCore for underlying orchestration.
    """

    def __init__(self, max_workers: int = 4) -> None:
        """
        Initialize the ParallelProcessor.

        Args:
            max_workers: Maximum number of worker threads.
        """
        self.max_workers = max_workers
        self._execution_core = ExecutionCore(max_workers=max_workers)

    def process_files_threaded(self, files: list[Path], worker_func: Callable[[Path], Any]) -> list[Any]:
        """
        Process files using worker threads.

        Args:
            files: List of file paths to process.
            worker_func: Function to apply to each file.

        Returns:
            List of results from worker_func.
        """
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            if HAS_TQDM:
                results = list(
                    tqdm(
                        executor.map(worker_func, files),
                        total=len(files),
                        desc="Processing (Threads)",
                    )
                )
            else:
                results = list(executor.map(worker_func, files))
        return [r for r in results if r is not None]

    async def async_process_files(self, files: list[Path], worker_func: Callable[[Path], Any]) -> list[Any]:
        """
        Process multiple files concurrently using async/await.

        Args:
            files: List of file paths to process.
            worker_func: Function to apply to each file.

        Returns:
            List of results from worker_func.
        """

        def _wrapped_task(file_path: Path) -> Any:
            """Inner wrapper to handle single file execution and errors."""
            try:
                return worker_func(file_path)
            except Exception as exc:  # pylint: disable=broad-exception-caught, unused-variable
                logging.error("[ParallelProcessor] Failed to process %s: %s", file_path.name, str(exc))
                return None

        # Prepare tasks for ExecutionCore
        tasks = [partial(_wrapped_task, f) for f in files]

        try:
            # ExecutionCore handles the pooled thread execution
            results = await self._execution_core.execute_parallel(tasks)
            return [r for r in results if r is not None]
        except Exception as exc:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error("[ParallelProcessor] Async batch processing failed: %s", str(exc))
            return []
