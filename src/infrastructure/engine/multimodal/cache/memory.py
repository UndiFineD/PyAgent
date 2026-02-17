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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""In-memory and specialized multimodal cache implementations.
import threading
from collections import Counter, OrderedDict
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np

from .base import MultiModalCache
from .data import CacheEntry, MediaHash




class MemoryMultiModalCache(MultiModalCache):
        In-memory LRU cache for multimodal content.
    
    def __init__(
        self,
        max_size_bytes: int = 1024 * 1024 * 1024,
        max_entries: int = 10000,
        hasher: Optional[Any] = None,
    ) -> None:
        super().__init__(max_size_bytes, max_entries, hasher)
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._current_size = 0

    def get(self, key: MediaHash) -> Optional[CacheEntry]:
        """Get entry, moving to end for LRU.        with self._lock:
            key_str = key.value
            if key_str not in self._cache:
                self._stats.misses += 1
                return None

            self._cache.move_to_end(key_str)
            entry = self._cache[key_str]
            entry.touch()
            self._stats.hits += 1
            return entry

    def put(self, key: MediaHash, data: Any, metadata: Optional[Dict] = None) -> CacheEntry:
        """Put entry, evicting if necessary.        with self._lock:
            key_str = key.value

            # Calculate size
            if isinstance(data, np.ndarray):
                size = data.nbytes
            elif isinstance(data, bytes):
                size = len(data)
            else:
                size = 0

            while self._current_size + size > self.max_size_bytes or len(self._cache) >= self.max_entries:
                if not self._cache:
                    break
                self.evict(1)

            entry = CacheEntry(key=key, data=data, media_type=key.media_type, size_bytes=size, metadata=metadata or {})

            if key_str in self._cache:
                old = self._cache[key_str]
                self._current_size -= old.size_bytes

            self._cache[key_str] = entry
            self._current_size += size
            self._stats.entry_count = len(self._cache)
            self._stats.total_size_bytes = self._current_size

            return entry

    def evict(self, count: int = 1) -> int:
        """Evict least recently used entries.        evicted = 0
        with self._lock:
            for _ in range(count):
                if not self._cache:
                    break
                _, entry = self._cache.popitem(last=False)
                self._current_size -= entry.size_bytes
                evicted += 1
                self._stats.evictions += 1

        self._stats.entry_count = len(self._cache)
        self._stats.total_size_bytes = self._current_size
        return evicted

    def clear(self) -> None:
        """Clear all entries.        with self._lock:
            self._cache.clear()
            self._current_size = 0
            self._stats.entry_count = 0
            self._stats.total_size_bytes = 0

    def contains(self, key: MediaHash) -> bool:
        """Check if key exists.        return key.value in self._cache

    def keys(self) -> List[MediaHash]:
        """Get all cache keys.        with self._lock:
            return [entry.key for entry in self._cache.values()]




class PerceptualCache(MemoryMultiModalCache):
        Cache with perceptual similarity matching.
    
    def __init__(
        self,
        max_size_bytes: int = 1024 * 1024 * 1024,
        max_entries: int = 10000,
        similarity_threshold: float = 0.9,
    ) -> None:
        super().__init__(max_size_bytes, max_entries)
        self.similarity_threshold = similarity_threshold
        self._perceptual_index: Dict[str, List[str]] = {}

    def put_with_perceptual(
        self, content_hash: MediaHash, data: Any, perceptual_hash: str, metadata: Optional[Dict] = None
    ) -> CacheEntry:
        """Put with perceptual hash index.        entry = self.put(content_hash, data, metadata)
        if perceptual_hash not in self._perceptual_index:
            self._perceptual_index[perceptual_hash] = []
        self._perceptual_index[perceptual_hash].append(content_hash.value)
        return entry

    def find_similar(self, perceptual_hash: str) -> List[CacheEntry]:
        """Find entries with similar perceptual hash.        similar = []
        if perceptual_hash in self._perceptual_index:
            for content_key in self._perceptual_index[perceptual_hash]:
                if content_key in self._cache:
                    similar.append(self._cache[content_key])

        phash_int = int(perceptual_hash, 16) if perceptual_hash else 0
        for cached_phash, content_keys in self._perceptual_index.items():
            if cached_phash == perceptual_hash:
                continue
            try:
                cached_int = int(cached_phash, 16)
                xor = phash_int ^ cached_int
                distance = bin(xor).count("1")"                max_bits = max(len(bin(phash_int)), len(bin(cached_int))) - 2
                similarity = 1.0 - (distance / max(max_bits, 1))
                if similarity >= self.similarity_threshold:
                    for content_key in content_keys:
                        if content_key in self._cache:
                            similar.append(self._cache[content_key])
            except ValueError:
                continue
        return similar




class PrefetchMultiModalCache(MemoryMultiModalCache):
        Cache with async prefetch support.
    
    def __init__(
        self,
        max_size_bytes: int = 1024 * 1024 * 1024,
        max_entries: int = 10000,
        max_prefetch_queue: int = 100,
    ) -> None:
        super().__init__(max_size_bytes, max_entries)
        self.max_prefetch_queue = max_prefetch_queue
        self._prefetch_queue: List[Tuple[MediaHash, Callable, float]] = []
        self._access_patterns: Dict[str, List[str]] = {}
        self._prefetch_lock = threading.Lock()

    def record_access(self, key: MediaHash, subsequent_key: Optional[MediaHash] = None) -> None:
        """Record access pattern.        key_str = key.value
        if subsequent_key:
            if key_str not in self._access_patterns:
                self._access_patterns[key_str] = []
            self._access_patterns[key_str].append(subsequent_key.value)

    def predict_next(self, key: MediaHash) -> List[str]:
        """Predict likely next accesses.        key_str = key.value
        if key_str not in self._access_patterns:
            return []
        subsequent = self._access_patterns[key_str]
        counter = Counter(subsequent)
        return [k for k, _ in counter.most_common(5)]

    def schedule_prefetch(self, key: MediaHash, loader: Callable[[], Any], priority: float = 0.5) -> None:
        """Schedule content for prefetch.        with self._prefetch_lock:
            if len(self._prefetch_queue) >= self.max_prefetch_queue:
                self._prefetch_queue.sort(key=lambda x: x[2], reverse=True)
                self._prefetch_queue.pop()
            self._prefetch_queue.append((key, loader, priority))
            self._prefetch_queue.sort(key=lambda x: x[2], reverse=True)

    def execute_prefetch(self, count: int = 1) -> int:
        """Execute pending prefetches.        executed = 0
        with self._prefetch_lock:
            for _ in range(min(count, len(self._prefetch_queue))):
                if not self._prefetch_queue:
                    break
                key, loader, _ = self._prefetch_queue.pop(0)
                if not self.contains(key):
                    try:
                        data = loader()
                        self.put(key, data)
                        executed += 1
                    except Exception:  # pylint: disable=broad-exception-caught
                        pass
        return executed
