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

"""
Manager for file locking.
(Facade for src.core.base.common.lock_core)
"""

from __future__ import annotations

from typing import Optional

from src.core.base.common.lock_core import LockCore


class FileLockManager:
    """
    Manager for coordinating file-system level locks.
    Delegates to LockCore for the underlying synchronization logic.
    """

    def __init__(self, core: Optional[LockCore] = None):
        self._core = core or LockCore()

    def acquire(self, lock_id: str, timeout: float = 10.0) -> bool:
        """Acquire a file lock."""
        return self._core.acquire_lock(lock_id, timeout)

    def release(self, lock_id: str) -> None:
        """Release a file lock."""
        self._core.release_lock(lock_id)

    def is_locked(self, lock_id: str) -> bool:
        """Check if a file is locked."""
        return self._core.is_locked(lock_id)
