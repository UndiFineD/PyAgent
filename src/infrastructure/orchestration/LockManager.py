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
import time
import logging
import threading
from pathlib import Path
from typing import Dict, Any, Optional, ContextManager
from contextlib import contextmanager

try:
    import portalocker
    HAS_PORTALOCKER = True
except ImportError:
    HAS_PORTALOCKER = False

class LockManager:
    """Phase 242: Distributed Lock Manager.
    Supports both memory-based (threading.Lock) and file-based (portalocker) locking.
    Essential for preventing race conditions in parallel agent workflows.
    """
    _instance = None
    _mem_locks: Dict[str, threading.Lock] = {}
    _global_lock = threading.Lock()

    def __new__(cls, *args, **kwargs) -> "LockManager":
        if cls._instance is None:
            cls._instance = super(LockManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, lock_dir: Optional[str] = None) -> None:
        self.lock_dir = Path(lock_dir) if lock_dir else Path("temp/locks")
        if not self.lock_dir.exists():
            self.lock_dir.mkdir(parents=True, exist_ok=True)

    def get_memory_lock(self, resource_id: str) -> threading.Lock:
        """Returns a thread-safe lock for a specific resource ID."""
        with self._global_lock:
            if resource_id not in self._mem_locks:
                self._mem_locks[resource_id] = threading.Lock()
            return self._mem_locks[resource_id]

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
