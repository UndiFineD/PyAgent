"""
Manager for file locking.
(Facade for src.core.base.common.lock_core)
"""

<<<<<<< HEAD
"""
Manager for file locking.
(Facade for src.core.base.common.lock_core)
"""

from __future__ import annotations

from typing import Any, Dict, Optional


class LockProxy:
    """A proxy object for a held lock."""

    def __init__(self, lock_id: str, lock_type: Any) -> None:
        self.lock_id = lock_id
        self.lock_type = lock_type


class FileLockManager:
    """
    Manager for coordinating file-system level locks.
    Delegates to LockCore for the underlying synchronization logic.
    """

    def __init__(self, core: Optional[Any] = None) -> None:
        from src.core.base.common.lock_core import LockCore
        self._core = core or LockCore()
        self.lock_timeout = 300.0
        self.locks: Dict[str, LockProxy] = {}

    def acquire(self, lock_id: str, timeout: float = 10.0, lock_type: Any = None) -> bool:
        """Acquire a file lock."""
        return self._core.acquire_lock(str(lock_id), timeout, lock_type)

    def acquire_lock(self, lock_id: str, lock_type: Any = None, timeout: float = None) -> LockProxy | None:
        """Alias for acquire to match expectations of some core modules."""
        # Use default timeout if not provided
        t = timeout if timeout is not None else self.lock_timeout

        # Default lock_type to EXCLUSIVE if not provided (mocking behavior for tests)
        if lock_type is None:
            # Try to get LockType from models or similar, otherwise hardcode
            try:
                from src.core.base.common.models import LockType
                lock_type = LockType.EXCLUSIVE
            except ImportError:
                lock_type = "EXCLUSIVE"

        success = self.acquire(str(lock_id), t, lock_type)
        if success:
            proxy = LockProxy(str(lock_id), lock_type)
            self.locks[str(lock_id)] = proxy
            return proxy
        return None

    def release(self, lock_id: str) -> bool:
        """Release a file lock."""
        self._core.release_lock(str(lock_id))
        if str(lock_id) in self.locks:
            del self.locks[str(lock_id)]
        return True

    def release_lock(self, lock_id: str) -> bool:
        """Alias for release to match expectations of some core modules."""
        return self.release(lock_id)

    def is_locked(self, lock_id: str) -> bool:
        """Check if a file is locked."""
        return self._core.is_locked(lock_id)
=======
from src.core.base.common.lock_core import LockCore as FileLockManager
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
