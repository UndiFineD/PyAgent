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
import os
import logging
import threading
import asyncio
from pathlib import Path
from typing import Dict, Optional, ContextManager, Any
from contextlib import contextmanager, asynccontextmanager

try:
    import portalocker
    HAS_PORTALOCKER = True
except ImportError:
    HAS_PORTALOCKER = False

class LockManager:
    """Phase 242/152: Distributed & Async-Ready Lock Manager.
    Supports memory-based (threading.Lock/asyncio.Lock) and file-based (portalocker) locking.
    """
    _instance = None
    _mem_locks: dict[str, threading.Lock] = {}
    _async_mem_locks: dict[str, asyncio.Lock] = {}
    _global_lock = threading.Lock()

    def __new__(cls, *args, **kwargs) -> LockManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, lock_dir: str | None = None) -> None:
        self.lock_dir = Path(lock_dir) if lock_dir else Path("temp/locks")
        if not self.lock_dir.exists():
            self.lock_dir.mkdir(parents=True, exist_ok=True)

    def get_memory_lock(self, resource_id: str) -> threading.Lock:
        """Returns a thread-safe lock for a specific resource ID."""
        with self._global_lock:
            if resource_id not in self._mem_locks:
                self._mem_locks[resource_id] = threading.Lock()
            return self._mem_locks[resource_id]

    def get_async_memory_lock(self, resource_id: str) -> asyncio.Lock:
        """Phase 152: Returns an asyncio-safe lock."""
        if resource_id not in self._async_mem_locks:
            self._async_mem_locks[resource_id] = asyncio.Lock()
        return self._async_mem_locks[resource_id]

    @asynccontextmanager
    async def acquire_async(self, resource_id: str, lock_type: str = "memory", timeout: float = 10.0):
        """Phase 152: Async-native lock acquisition."""
        if lock_type == "file":
            # File locks are blocking, offload to executor
            loop = asyncio.get_running_loop()
            try:
                await loop.run_in_executor(None, lambda: self._sync_file_lock_acquire(resource_id, timeout))
                yield
            finally:
                await loop.run_in_executor(None, lambda: self._sync_file_lock_release(resource_id))
        else:
            lock = self.get_async_memory_lock(resource_id)
            try:
                await asyncio.wait_for(lock.acquire(), timeout=timeout)
                yield
            finally:
                lock.release()

    def _sync_file_lock_acquire(self, resource_path: str, timeout: float):
        lock_file = self.lock_dir / f"{os.path.basename(resource_path)}.lock"
        if HAS_PORTALOCKER:
            lock_obj = portalocker.Lock(str(lock_file), timeout=timeout)
            lock_obj.acquire()
            # Store lock object for release - this is simplistic, 
            # in a real system we'd need a better way to track these per-task
            if not hasattr(self, '_active_file_locks'):
                self._active_file_locks = {}
            self._active_file_locks[resource_path] = lock_obj
        else:
            self.get_memory_lock(resource_path).acquire()

    def _sync_file_lock_release(self, resource_path: str):
        if HAS_PORTALOCKER and hasattr(self, '_active_file_locks'):
            lock_obj = self._active_file_locks.get(resource_path)
            if lock_obj:
                lock_obj.release()
                del self._active_file_locks[resource_path]
        else:
            self.get_memory_lock(resource_path).release()

    @contextmanager
    def file_lock(self, resource_path: str, timeout: float = 10.0) -> ContextManager[None]:
        """A cross-process file lock using portalocker."""
        lock_file = self.lock_dir / f"{os.path.basename(resource_path)}.lock"
        
        if not HAS_PORTALOCKER:
            logging.warning("portalocker not installed. Falling back to memory-only lock for file.")
            with self.get_memory_lock(resource_path):
                yield
            return

        try:
            with portalocker.Lock(str(lock_file), timeout=timeout):
                yield
        except portalocker.exceptions.LockException:
            logging.error(f"Could not acquire lock for {resource_path} within {timeout}s")
            raise TimeoutError(f"Lock acquisition timeout for {resource_path}")
        finally:
            if lock_file.exists():
                try:
                    # We don't necessarily delete it to avoid race conditions on deletion itself,
                    # but we could. Portalocker handles the handle cleanup.
                    pass
                except Exception:
                    pass

    @contextmanager
    def acquire(self, resource_id: str, lock_type: str = "memory", timeout: float = 10.0):
        """Generic lock acquisition helper."""
        if lock_type == "file":
            with self.file_lock(resource_id, timeout):
                yield
        else:
            lock = self.get_memory_lock(resource_id)
            acquired = lock.acquire(timeout=timeout)
            if not acquired:
                raise TimeoutError(f"Memory lock timeout for {resource_id}")
            try:
                yield
            finally:
                lock.release()