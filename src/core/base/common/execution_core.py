# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Unified Execution Core for PyAgent.
Handles concurrent, parallel, and serial task orchestration.
"""

from __future__ import annotations
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Any, List, Callable, Optional
from .base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None

class ExecutionCore(BaseCore):
    """
    Standard implementation for task orchestration.
    Supports ThreadPool, ProcessPool, and native Rust-based async scheduling.
    """
    
    def __init__(self, max_workers: int = 4):
        super().__init__()
        self.max_workers = max_workers
        self._thread_pool = ThreadPoolExecutor(max_workers=max_workers)

    async def execute_parallel(self, tasks: List[Callable]) -> List[Any]:
        """Executes a list of callables in parallel using threads."""
        if rc and hasattr(rc, "execute_parallel_rust"):
            return rc.execute_parallel_rust(tasks)
            
        loop = asyncio.get_event_loop()
        futures = [loop.run_in_executor(self._thread_pool, task) for task in tasks]
        return await asyncio.gather(*futures)

    def map_seq(self, func: Callable, items: List[Any]) -> List[Any]:
        """Sequenced map implementation."""
        return [func(item) for item in items]
