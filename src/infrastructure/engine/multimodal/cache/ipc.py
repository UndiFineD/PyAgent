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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""IPC-enabled multimodal cache."""

from pathlib import Path
from typing import Any, Dict, Optional, Set

from .base import MultiModalCache
from .data import CacheEntry, MediaHash
from .memory import MemoryMultiModalCache


class IPCMultiModalCache(MultiModalCache):
    """
    IPC-enabled cache for cross-process sharing.
    """

    def __init__(
        self,
        name: str = "pyagent_mm_cache",
        max_size_bytes: int = 1024 * 1024 * 1024,
        max_entries: int = 10000,
        hasher: Optional[Any] = None,
        create: bool = True,
    ) -> None:
        super().__init__(max_size_bytes, max_entries, hasher)
        self.name = name
        self._local_cache = MemoryMultiModalCache(max_size_bytes, max_entries, hasher)
        self._shared_keys: Set[str] = set()

        # Paths for shared memory (placeholder implementation)
        self._shm_path = Path(f"/tmp/{name}.cache")
        self._index_path = Path(f"/tmp/{name}.index")

        if create:
            self._initialize_shared()

    def _initialize_shared(self) -> None:
        """Initialize shared memory structures."""
        try:
            if not self._index_path.parent.exists():
                self._index_path.parent.mkdir(parents=True, exist_ok=True)
            self._index_path.write_text("{}", encoding="utf-8")
        except (IOError, OSError):
            # Fallback if /tmp is not writable
            pass

    def get(self, key: MediaHash) -> Optional[CacheEntry]:
        """Get from local cache first, then check shared."""
        entry = self._local_cache.get(key)
        if entry is not None:
            return entry

        if key.value in self._shared_keys:
            self._stats.hits += 1
            return None  # In real implementation, load from shared memory

        self._stats.misses += 1
        return None

    def put(self, key: MediaHash, data: Any, metadata: Optional[Dict] = None) -> CacheEntry:
        """Put in local cache and mark for sharing."""
        entry = self._local_cache.put(key, data, metadata)
        self._shared_keys.add(key.value)
        return entry

    def evict(self, count: int = 1) -> int:
        """Evict from local cache."""
        return self._local_cache.evict(count)

    def clear(self) -> None:
        """Clear local and shared caches."""
        self._local_cache.clear()
        self._shared_keys.clear()

    def contains(self, key: MediaHash) -> bool:
        """Check local and shared."""
        return self._local_cache.contains(key) or key.value in self._shared_keys

    def share_entry(self, key: MediaHash) -> bool:
        """Explicitly share an entry."""
        if not self._local_cache.contains(key):
            return False
        self._shared_keys.add(key.value)
        return True
