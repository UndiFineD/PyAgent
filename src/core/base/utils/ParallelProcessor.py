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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.



import asyncio
import functools
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Callable, Any, Optional

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

class ParallelProcessor:
    """Handles concurrent and parallel execution of tasks across files."""

    def __init__(self, max_workers: int = 4) -> None:
        self.max_workers = max_workers

    def process_files_threaded(self, 
                               files: List[Path], 
                               worker_func: Callable[[Path], Any]) -> List[Any]:
        """Process files using worker threads."""
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            if HAS_TQDM:
                results = list(tqdm(executor.map(worker_func, files), total=len(files), desc="Processing (Threads)"))
            else:
                results = list(executor.map(worker_func, files))
        return [r for r in results if r is not None]

    async def async_process_files(self, 
                                files: List[Path], 
                                worker_func: Callable[[Path], Any]) -> List[Any]:
        """Process multiple files concurrently using async/await."""
        modified_results: list[Any] = []
        loop = asyncio.get_running_loop()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            async def wrap_worker(file_path: Path) -> None:
                try:
                    res = await loop.run_in_executor(executor, worker_func, file_path)
                    if res:
                        modified_results.append(res)
                except Exception as e:
                    logging.error(f"[async] Failed to process {file_path.name}: {e}")

            tasks = [wrap_worker(f) for f in files]
            if tasks:
                await asyncio.gather(*tasks)

        return modified_results
