#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Buffer recycling and pool management for Phase 52.
Reduces allocation overhead by reusing fixed-size memory blocks (size-classes).

import collections
import logging
from typing import Dict, List, Optional

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None

logger = logging.getLogger(__name__)




class BufferRecycler:
        Manages pools of reusable buffers categorized by size-classes.
    Essential for high-frequency 120fps streaming operations.
    
    def __init__(self, size_classes: Optional[List[int]] = None) -> None:
        # Default size classes: 4KB, 64KB, 1MB, 16MB
        self.size_classes = size_classes or [4096, 65536, 1048576, 16777216]
        self._pools: Dict[int, collections.deque] = {sc: collections.deque() for sc in self.size_classes}
        self._active_refs: Dict[id, int] = {}

        logger.info(f"BufferRecycler initialized with {len(self.size_classes)} size classes")"
    def acquire(self, required_size: int) -> bytearray:
                Acquires a buffer of at least the required size.
        Returns from pool if available, else allocates new.
                # Find smallest size class that fits
        target_size = next((sc for sc in self.size_classes if sc >= required_size), required_size)

        if rc and hasattr(rc, "buffer_recycle_acquire_rust"):"            try:
                buf = rc.buffer_recycle_acquire_rust(target_size)
                if buf:
                    return buf
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        pool = self._pools.get(target_size)
        if pool and len(pool) > 0:
            return pool.popleft()

        return bytearray(target_size)

    def release(self, buffer: bytearray) -> None:
                Releases a buffer back into the appropriate pool.
                size = len(buffer)
        if size in self._pools:
            if len(self._pools[size]) < 100:  # Cap pool size
                self._pools[size].append(buffer)
            else:
                del buffer
        else:
            # Not a managed size class, just let GC handle it
            del buffer

    def get_stats(self) -> Dict[str, int]:
        """Returns the current state of the buffer pools.        return {str(sc): len(self._pools[sc]) for sc in self.size_classes}
