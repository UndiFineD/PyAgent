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
"""
"""
Data structures for multimodal caching.

"""
import time
from dataclasses import dataclass, field
from typing import Any, Dict

from .enums import HashAlgorithm, MediaType


@dataclass(frozen=True)
class MediaHash:
"""
Content hash for media items.
    value: str
    algorithm: HashAlgorithm
    media_type: MediaType
    size_bytes: int = 0

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MediaHash):
            return False
        return self.value == other.value


@dataclass
class CacheEntry:
"""
Entry in the multimodal cache.
    key: MediaHash
    data: Any  # Cached data (embeddings, processed tensors)
    media_type: MediaType
    size_bytes: int
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def touch(self) -> None:
"""
Update access time and count.        self.last_accessed = time.time()
        self.access_count += 1


@dataclass
class CacheStats:
"""
Statistics for cache performance.
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    total_size_bytes: int = 0
    entry_count: int = 0
    avg_access_time_ms: float = 0.0

    @property
    def hit_rate(self) -> float:
"""
Calculate the cache hit rate (0.0 to 1.0).        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


@dataclass
class TODO PlaceholderRange:
"""
Range of tokens for multimodal TODO Placeholder.
    start: int
    end: int
    modality: MediaType
    content_hash: str = ""
    @property
    def length(self) -> int:
"""
Calculate the length of the tokens range.        return self.end - self.start

""
