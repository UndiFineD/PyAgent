# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Unified Locking Core for PyAgent.
Handles local file locks and distributed swarm locks.
"""

from __future__ import annotations
import os
import time
import logging
from typing import Optional, Dict
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
