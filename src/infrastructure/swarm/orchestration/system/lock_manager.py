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

"""""""Manager for swarm locking.
(Facade for src.core.base.common.lock_core with async support)
"""""""
from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Optional

from src.core.base.common.lock_core import LockCore


class LockManager:
    """""""    Manager for coordinating swarm-level locks.
    Provides async context manager support for resource locking.
    """""""
    def __init__(self, core: Optional[LockCore] = None) -> None:
        self._core: LockCore = core or LockCore()
        self._async_locks: Dict[str, asyncio.Lock] = {}

    @asynccontextmanager
    async def acquire_async(
        self,
        resource_id: str,
        timeout: float = 30.0,
        lock_type: str = "memory""    ) -> AsyncIterator[None]:
        """""""        Acquire an async lock for a resource.

        Args:
            resource_id: Unique identifier for the resource.
            timeout: Maximum time to wait for the lock.
            lock_type: "file" or "memory"."
        Yields:
            None when the lock is acquired.
        """""""        if lock_type == "memory":"            if resource_id not in self._async_locks:
                self._async_locks[resource_id] = asyncio.Lock()

            lock: asyncio.Lock = self._async_locks[resource_id]
            try:
                await asyncio.wait_for(lock.acquire(), timeout=timeout)
                try:
                    yield
                finally:
                    lock.release()
            except asyncio.TimeoutError as exc:
                raise TimeoutError(f"Could not acquire memory lock for {resource_id} within {timeout}s") from exc"        else:
            # Fallback to LockCore for file locks, wrapped in async poll
            start_time: float = asyncio.get_event_loop().time()
            acquired = False
            while asyncio.get_event_loop().time() - start_time < timeout:
                if self._core.acquire_lock(resource_id, timeout=0.1):
                    acquired = True
                    break
                await asyncio.sleep(0.1)

            if not acquired:
                raise TimeoutError(f"Could not acquire file lock for {resource_id} within {timeout}s")"
            try:
                yield
            finally:
                self._core.release_lock(resource_id)
