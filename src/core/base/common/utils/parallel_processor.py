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


"""Manager for parallel execution.
(Facade for src.core.base.common.execution_core)
"""


from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import Any, Callable, List

try:
    from tqdm import tqdm

    HAS_TQDM = True
except Exception:
    HAS_TQDM = False

from src.core.base.common.execution_core import ExecutionCore


class ParallelProcessor:
    """Facade for parallel execution utilities.

    Uses ExecutionCore for underlying orchestration. This class provides a small
    compatibility layer so tests can exercise threaded and async execution.
    """

    def __init__(self, max_workers: int = 4) -> None:
        self.max_workers = max_workers
        self._execution_core = ExecutionCore(max_workers=max_workers)

    def process_files_threaded(self, files: List[Path], worker_func: Callable[[Path], Any]) -> List[Any]:
        """Process files using worker threads and return non-None results."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            if HAS_TQDM:
                results = list(tqdm(executor.map(worker_func, files), total=len(files), desc="Processing (Threads)"))
            else:
                results = list(executor.map(worker_func, files))
        return [r for r in results if r is not None]

    async def async_process_files(self, files: List[Path], worker_func: Callable[[Path], Any]) -> List[Any]:
        """Process files using ExecutionCore's async API."""

        def _wrapped_task(file_path: Path) -> Any:
            try:
                return worker_func(file_path)
            except Exception as exc:  # pylint: disable=broad-exception-caught
                logging.error("[ParallelProcessor] Failed to process %s: %s", file_path.name, str(exc))
                return None

        tasks = [partial(_wrapped_task, f) for f in files]

        try:
            results = await self._execution_core.execute_parallel(tasks)
            return [r for r in results if r is not None]
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logging.error("[ParallelProcessor] Async batch processing failed: %s", str(exc))
            return []
