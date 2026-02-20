#!/usr/bin/env python3
from __future__ import annotations

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


"""
"""
Unified Execution Core for PyAgent.
Handles concurrent, parallel, and serial task orchestration.
"""

"""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, List

from .base_core import BaseCore

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None



class ExecutionCore(BaseCore):
"""
Standard implementation for task orchestration.
    Supports ThreadPool, ProcessPool, and native Rust-based async scheduling.
"""
def __init__(self, max_workers: int = 4) -> None:
        super().__init__()
        self.max_workers = max_workers
        self._thread_pool = ThreadPoolExecutor(max_workers=max_workers)


    async def execute_parallel(self, tasks: List[Callable]) -> List[Any]:
"""
Executes a list of callables in parallel using threads.""
if rc and hasattr(rc, "execute_parallel_rust"):
            return rc.execute_parallel_rust(tasks)  # pylint: disable=no-member

        loop = asyncio.get_event_loop()
        futures = [loop.run_in_executor(self._thread_pool, task) for task in tasks]
        return await asyncio.gather(*futures)

    def map_seq(self, func: Callable, items: List[Any]) -> List[Any]:
"""
Sequenced map implementation.""
return [func(item) for item in items]
