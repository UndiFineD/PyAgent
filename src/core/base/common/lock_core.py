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
Unified Locking Core for PyAgent.
Handles local file locks and distributed swarm locks.
"""

import time
from typing import Dict

from .base_core import BaseCore


class LockCore(BaseCore):
    """
    Standard implementation for resource locking.
    Supports both file-based advisory locks and in-memory swarm locks.
    """

    def __init__(self):
        super().__init__()
        self.active_locks: Dict[str, float] = {}

    def acquire_lock(self, lock_id: str, timeout: float = 10.0) -> bool:
        """Acquire a lock by ID."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if lock_id not in self.active_locks:
                self.active_locks[lock_id] = time.time()
                return True
            time.sleep(0.1)
        return False

    def release_lock(self, lock_id: str) -> None:
        """Release a held lock."""
        self.active_locks.pop(lock_id, None)

    def is_locked(self, lock_id: str) -> bool:
        """Check if a resource is currently locked."""
        return lock_id in self.active_locks
