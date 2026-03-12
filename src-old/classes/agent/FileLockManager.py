#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/classes/agent/FileLockManager.description.md

# FileLockManager

**File**: `src\\classes\agent\\FileLockManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 133  
**Complexity**: 4 (simple)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `FileLockManager`

Manages file locks to prevent concurrent modifications.

Provides advisory file locking to coordinate access between
multiple agent instances or processes.

Attributes:
    locks: Dict of active file locks.
    lock_timeout: Default lock timeout in seconds.

**Methods** (4):
- `__init__(self, lock_timeout)`
- `acquire_lock(self, file_path, lock_type, timeout)`
- `release_lock(self, file_path)`
- `_cleanup_expired_locks(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.models.LockType`
- `src.core.base.utils.FileLock.FileLock`
- `src.core.base.version.VERSION`
- `threading`
- `time`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/agent/FileLockManager.improvements.md

# Improvements for FileLockManager

**File**: `src\\classes\agent\\FileLockManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 133 lines (medium)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `FileLockManager_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END

"""

from __future__ import annotations

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


"""Auto-extracted class from agent.py"""

import logging
import os
import threading
import time
from pathlib import Path

from src.core.base.models import LockType
from src.core.base.utils.FileLock import FileLock
from src.core.base.version import VERSION

__version__ = VERSION


class FileLockManager:
    """Manages file locks to prevent concurrent modifications.

    Provides advisory file locking to coordinate access between
    multiple agent instances or processes.

    Attributes:
        locks: Dict of active file locks.
        lock_timeout: Default lock timeout in seconds.

    """

    def __init__(self, lock_timeout: float = 300.0) -> None:
        """Initialize the lock manager.

        Args:
            lock_timeout: Default lock timeout in seconds.

        """
        self.locks: dict[str, FileLock] = {}
        self.lock_timeout = lock_timeout
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._owner_id = f"{os.getpid()}_{threading.current_thread().ident}"

    def acquire_lock(
        self,
        file_path: Path,
        lock_type: LockType = LockType.EXCLUSIVE,
        timeout: float | None = None,
    ) -> FileLock | None:
        """Acquire a lock on a file.

        Args:
            file_path: Path to file to lock.
            lock_type: Type of lock to acquire.
            timeout: Timeout for acquiring lock.

        Returns:
            FileLock if acquired, None if timeout.

        """
        path_str = str(file_path.resolve())
        timeout = timeout or self.lock_timeout
        start_time = time.time()

        with self._condition:
            while True:
                # Check for expired locks
                self._cleanup_expired_locks()

                # Check if already locked
                existing_lock = self.locks.get(path_str)
                if existing_lock is None:
                    # Acquire new lock
                    lock = FileLock(
                        file_path=file_path,
                        lock_type=lock_type,
                        owner=self._owner_id,
                        acquired_at=time.time(),
                        expires_at=time.time() + self.lock_timeout,
                    )
                    self.locks[path_str] = lock
                    logging.debug(f"Acquired {lock_type.name} lock on {file_path}")
                    return lock
                elif (
                    existing_lock.lock_type == LockType.SHARED
                    and lock_type == LockType.SHARED
                ):
                    # Shared locks can coexist
                    return existing_lock

                # Check timeout
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    logging.warning(f"Timeout acquiring lock on {file_path}")
                    return None

                # Wait for condition signal instead of blocking sleep
                self._condition.wait(timeout=min(0.1, timeout - elapsed))

    def release_lock(self, file_path: Path) -> bool:
        """Release a lock on a file.

        Args:
            file_path: Path to file to unlock.

        Returns:
            bool: True if lock released, False if not owner.

        """
        path_str = str(file_path.resolve())

        with self._condition:
            lock = self.locks.get(path_str)
            if lock and lock.owner == self._owner_id:
                del self.locks[path_str]
                logging.debug(f"Released lock on {file_path}")
                self._condition.notify_all()
                return True
            return False

    def _cleanup_expired_locks(self) -> None:
        """Remove expired locks."""
        now = time.time()
        expired = [
            path
            for path, lock in self.locks.items()
            if lock.expires_at and lock.expires_at < now
        ]
        for path in expired:
            logging.debug(f"Cleaning up expired lock on {path}")
            del self.locks[path]
