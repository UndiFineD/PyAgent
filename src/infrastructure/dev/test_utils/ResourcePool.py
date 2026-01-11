#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from .ResourceHandle import ResourceHandle

from typing import Dict, Optional, Union
import threading
import time

class ResourcePool:
    """Manages resource allocation for tests."""

    def __init__(self, max_resources: int = 10) -> None:
        """Initialize resource pool."""
        self.max_resources = max_resources
        self.available = max_resources
        self.lock = threading.Lock()
        self._allocations: Dict[str, int] = {}

    def acquire(self, count: Union[int, str] = 1, timeout: float = 10.0) -> Optional[ResourceHandle]:
        """Acquire a resource.

        Compatibility:
        - Tests call `acquire("test_name", timeout=...)` and expect a handle or None.
        - Legacy code may call `acquire(count)`.
        """
        if isinstance(count, str):
            name = count
            start = time.time()
            while time.time() - start < timeout:
                with self.lock:
                    if self.available >= 1:
                        self.available -= 1
                        self._allocations[name] = self._allocations.get(name, 0) + 1
                        return ResourceHandle(name=name)
                threading.Event().wait(0.01)
            return None

        with self.lock:
            if self.available >= int(count):
                self.available -= int(count)
                return ResourceHandle(name=f"count:{int(count)}")
            return None

    def release(self, handle: Union[int, ResourceHandle] = 1) -> None:
        """Release resources."""
        with self.lock:
            if isinstance(handle, ResourceHandle):
                self.available = min(self.available + 1, self.max_resources)
                self._allocations[handle.name] = max(0, self._allocations.get(handle.name, 0) - 1)
                return
            self.available = min(self.available + int(handle), self.max_resources)

    def wait_available(self, count: int = 1, timeout: float = 10.0) -> bool:
        """Wait for resources to be available."""
        import time as time_module
        start = time_module.time()
        while time_module.time() - start < timeout:
            if self.acquire(count) is not None:
                return True
            time_module.sleep(0.1)
        return False
