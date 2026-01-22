<<<<<<< HEAD
<<<<<<< HEAD
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
=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""
Unified Locking Core for PyAgent.
Handles local file locks and distributed swarm locks.
"""

<<<<<<< HEAD
<<<<<<< HEAD
import time
from typing import Any, Dict

from .base_core import BaseCore

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
from __future__ import annotations
import os
import time
import logging
from typing import Optional, Dict
from src.core.base.common.base_core import BaseCore
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

class LockCore(BaseCore):
    """
    Standard implementation for resource locking.
    Supports both file-based advisory locks and in-memory swarm locks.
    """
<<<<<<< HEAD
<<<<<<< HEAD

    def __init__(self) -> None:
        super().__init__()
        self.active_locks: Dict[str, float] = {}
        self.shared_counts: Dict[str, int] = {}

    def acquire_lock(self, lock_id: str, timeout: float = 10.0, lock_type: Any = None) -> bool:
        """Acquire a lock by ID. Supports SHARED and EXCLUSIVE."""
        # Detect lock type
        is_shared = False
        if lock_type is not None:
            if hasattr(lock_type, "name"):
                is_shared = lock_type.name == "SHARED"
            else:
                is_shared = str(lock_type).upper() == "SHARED"

        start_time = time.time()
        while time.time() - start_time < timeout:
            if is_shared:
                # Shared lock can be acquired if no exclusive lock exists
                if lock_id not in self.active_locks:
                    self.shared_counts[lock_id] = self.shared_counts.get(lock_id, 0) + 1
                    return True
            else:
                # Exclusive lock can be acquired if no lock exists (shared or exclusive)
                if lock_id not in self.active_locks and self.shared_counts.get(lock_id, 0) == 0:
                    self.active_locks[lock_id] = time.time()
                    return True
            time.sleep(0.05)  # Shorter sleep for responsiveness
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    
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
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return False

    def release_lock(self, lock_id: str) -> None:
        """Release a held lock."""
<<<<<<< HEAD
<<<<<<< HEAD
        if lock_id in self.active_locks:
            self.active_locks.pop(lock_id)
        elif lock_id in self.shared_counts:
            self.shared_counts[lock_id] -= 1
            if self.shared_counts[lock_id] <= 0:
                self.shared_counts.pop(lock_id)
=======
        self.active_locks.pop(lock_id, None)
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        self.active_locks.pop(lock_id, None)
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

    def is_locked(self, lock_id: str) -> bool:
        """Check if a resource is currently locked."""
        return lock_id in self.active_locks
