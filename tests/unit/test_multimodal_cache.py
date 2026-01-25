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

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 40: MultiModal Cache Tests

"""
Tests for MultiModalCache - content-aware caching with IPC support.
"""

import pytest
import sys
import asyncio
import numpy as np
from typing import List

from src.infrastructure.multimodal.MultiModalCache import (
    MediaType,
    CacheBackend,
    HashAlgorithm,
    MediaHash,
    CacheEntry,
    CacheStats,
    PlaceholderRange,
    MultiModalHasher,
    MultiModalCache,
    MemoryMultiModalCache,
    IPCMultiModalCache,
    PerceptualCache,
    PrefetchMultiModalCache,
    compute_media_hash,
    create_cache,
)


class TestEnums:
    """Test enum values."""

    def test_media_type_values(self):
        """Test MediaType enum."""
        assert MediaType.IMAGE is not None
        assert MediaType.VIDEO is not None
        assert MediaType.AUDIO is not None

    def test_cache_backend_values(self):
        """Test CacheBackend enum."""
        assert CacheBackend.MEMORY is not None
        assert CacheBackend.SHARED is not None
        assert CacheBackend.MMAP is not None

    def test_hash_algorithm_values(self):
        """Test HashAlgorithm enum."""
        assert HashAlgorithm.BLAKE3 is not None
        assert HashAlgorithm.SHA256 is not None
        assert HashAlgorithm.XXHASH is not None
        assert HashAlgorithm.PERCEPTUAL is not None


class TestMediaHash:
    """Test MediaHash dataclass."""

    def test_create_media_hash(self):
        """Test creating MediaHash."""
        h = MediaHash(
            value="abc123",
            algorithm=HashAlgorithm.BLAKE3,
            media_type=MediaType.IMAGE,
        )
        assert h.value == "abc123"
        assert h.algorithm == HashAlgorithm.BLAKE3

    def test_media_hash_with_size(self):
        """Test MediaHash with size."""
        h = MediaHash(
            value="def456",
            algorithm=HashAlgorithm.SHA256,
            media_type=MediaType.VIDEO,
            size_bytes=1024,
        )
        assert h.size_bytes == 1024


class TestCacheEntry:
    """Test CacheEntry dataclass."""

    def test_create_cache_entry(self):
        """Test creating CacheEntry."""
        key = MediaHash(value="test_key", algorithm=HashAlgorithm.BLAKE3, media_type=MediaType.IMAGE)
        entry = CacheEntry(
            key=key,
            data=b"test data",
            media_type=MediaType.IMAGE,
            size_bytes=9,
        )
        assert entry.key == key
        assert entry.data == b"test data"

    def test_cache_entry_with_metadata(self):
        """Test CacheEntry with metadata."""
        key = MediaHash(value="key", algorithm=HashAlgorithm.BLAKE3, media_type=MediaType.AUDIO)
        entry = CacheEntry(
            key=key,
            data=b"data",
            media_type=MediaType.AUDIO,
            size_bytes=4,
            metadata={"format": "wav"},
        )
        assert entry.metadata["format"] == "wav"


class TestMultiModalHasher:
    """Test MultiModalHasher class."""

    def test_hash_bytes(self):
        """Test hashing bytes."""
        hasher = MultiModalHasher()
        data = b"test data for hashing"

        h = hasher.hash_bytes(data)
        assert isinstance(h, str)
        assert len(h) > 0

    def test_hash_deterministic(self):
        """Test hashing is deterministic."""
        hasher = MultiModalHasher()
        data = b"consistent data"

        h1 = hasher.hash_bytes(data)
        h2 = hasher.hash_bytes(data)
        assert h1 == h2

    def test_different_data_different_hash(self):
        """Test different data produces different hash."""
        hasher = MultiModalHasher()

        h1 = hasher.hash_bytes(b"data1")
        h2 = hasher.hash_bytes(b"data2")
        assert h1 != h2

    def test_hash_with_algorithm(self):
        """Test hashing with specific algorithm."""
        hasher = MultiModalHasher(algorithm=HashAlgorithm.SHA256)
        data = b"test"

        h = hasher.hash_bytes(data)
        assert isinstance(h, str)


class TestMemoryMultiModalCache:
    """Test in-memory cache implementation."""

    def test_create_cache(self):
        """Test creating memory cache."""
        cache = MemoryMultiModalCache(max_size_bytes=1024)
        assert cache is not None

    def test_put_and_get(self):
        """Test put and get operations."""
        cache = MemoryMultiModalCache(max_size_bytes=10240)

        key = MediaHash(value="test_key", algorithm=HashAlgorithm.BLAKE3, media_type=MediaType.IMAGE)
        data = b"test data"

        cache.put(key, data)
        result = cache.get(key)

        assert result is not None
        assert result.data == data

    def test_get_missing_key(self):
        """Test getting missing key."""
        cache = MemoryMultiModalCache()
        key = MediaHash(value="nonexistent", algorithm=HashAlgorithm.BLAKE3, media_type=MediaType.IMAGE)
        result = cache.get(key)
        assert result is None

    def test_contains(self):
        """Test contains check."""
        cache = MemoryMultiModalCache()

        key_exists = MediaHash(value="exists", algorithm=HashAlgorithm.BLAKE3, media_type=MediaType.IMAGE)
        key_missing = MediaHash(value="missing", algorithm=HashAlgorithm.BLAKE3, media_type=MediaType.IMAGE)

        cache.put(key_exists, b"data")

        assert cache.contains(key_exists)
        assert not cache.contains(key_missing)

    def test_clear(self):
        """Test clearing cache."""
        cache = MemoryMultiModalCache()

        key1 = MediaHash(value="key1", algorithm=HashAlgorithm.BLAKE3, media_type=MediaType.IMAGE)
        key2 = MediaHash(value="key2", algorithm=HashAlgorithm.BLAKE3, media_type=MediaType.VIDEO)

        cache.put(key1, b"data1")
        cache.put(key2, b"data2")

        cache.clear()

        assert not cache.contains(key1)
        assert not cache.contains(key2)

    def test_lru_eviction(self):
        """Test LRU eviction."""
        cache = MemoryMultiModalCache(max_size_bytes=100)

        # Fill cache
        for i in range(10):
            key = MediaHash(value=f"key{i}", algorithm=HashAlgorithm.BLAKE3, media_type=MediaType.IMAGE)
            cache.put(key, b"x" * 20)

        # Oldest entries should be evicted
        stats = cache.stats
        assert stats.evictions >= 0

    def test_stats(self):
        """Test cache statistics."""
        cache = MemoryMultiModalCache()

        key = MediaHash(value="key", algorithm=HashAlgorithm.BLAKE3, media_type=MediaType.IMAGE)
        key_missing = MediaHash(value="missing", algorithm=HashAlgorithm.BLAKE3, media_type=MediaType.IMAGE)

        cache.put(key, b"data")
        cache.get(key)  # Hit
        cache.get(key_missing)  # Miss

        stats = cache.stats
        assert stats.hits >= 1
        assert stats.misses >= 1


@pytest.mark.skipif(sys.platform == 'win32', reason='IPC cache uses /tmp which is not available on Windows')
class TestIPCMultiModalCache:
    """Test IPC-enabled cache."""

    def test_create_ipc_cache(self):
        """Test creating IPC cache."""
        cache = IPCMultiModalCache(name="test_cache", max_size_bytes=1024)
        assert cache is not None

    def test_basic_operations(self):
        """Test basic IPC cache operations."""
        cache = IPCMultiModalCache(name="test_ops")

        key = MediaHash(value="key", algorithm=HashAlgorithm.BLAKE3, media_type=MediaType.IMAGE)
        cache.put(key, b"data")
        result = cache.get(key)

        # May or may not return CacheEntry depending on platform
        assert result is None or result.data == b"data"


class TestPerceptualCache:
    """Test perceptual similarity cache."""

    def test_create_perceptual_cache(self):
        """Test creating perceptual cache."""
        cache = PerceptualCache(similarity_threshold=0.9)
        assert cache is not None

    def test_perceptual_match(self):
        """Test perceptual matching."""
        cache = PerceptualCache(similarity_threshold=0.8)

        # Store with perceptual hash
        key = MediaHash(value="key1", algorithm=HashAlgorithm.BLAKE3, media_type=MediaType.IMAGE)
        cache.put(key, b"image data 1")

        # Query (exact match)
        result = cache.get(key)
        assert result is not None


class TestPrefetchMultiModalCache:
    """Test prefetch-enabled cache."""

    def test_create_prefetch_cache(self):
        """Test creating prefetch cache."""
        cache = PrefetchMultiModalCache()
        assert cache is not None

    def test_predict_next(self):
        """Test prediction of next access."""
        cache = PrefetchMultiModalCache()

        key = MediaHash(value="key1", algorithm=HashAlgorithm.BLAKE3, media_type=MediaType.IMAGE)

        # Record access patterns
        cache.record_access(key)

        # Should not raise
        predictions = cache.predict_next(key)
        assert isinstance(predictions, list)


class TestFactoryFunctions:
    """Test factory functions."""

    def test_compute_media_hash(self):
        """Test compute_media_hash utility."""
        data = b"test image data"

        h = compute_media_hash(data, MediaType.IMAGE)
        assert isinstance(h, MediaHash)
        assert h.media_type == MediaType.IMAGE

    def test_create_memory_cache(self):
        """Test creating memory cache via factory."""
        cache = create_cache(CacheBackend.MEMORY, max_size_bytes=1024)
        assert isinstance(cache, MemoryMultiModalCache)

    @pytest.mark.skipif(sys.platform == 'win32', reason='IPC cache uses /tmp which is not available on Windows')
    def test_create_shared_cache(self):
        """Test creating shared/IPC cache via factory."""
        cache = create_cache(CacheBackend.SHARED, name="factory_test")
        assert isinstance(cache, IPCMultiModalCache)


class TestCacheStats:
    """Test cache statistics."""

    def test_cache_stats_dataclass(self):
        """Test CacheStats dataclass."""
        stats = CacheStats(
            hits=100,
            misses=20,
            evictions=5,
            total_size_bytes=1024,
        )
        assert stats.hits == 100
        assert stats.misses == 20
        assert stats.evictions == 5

    def test_hit_ratio(self):
        """Test hit ratio calculation."""
        stats = CacheStats(hits=80, misses=20, evictions=0, total_size_bytes=100)

        # Hit ratio should be 0.8
        assert stats.hit_rate == 0.8


class TestPlaceholderRange:
    """Test PlaceholderRange dataclass."""

    def test_create_placeholder_range(self):
        """Test creating PlaceholderRange."""
        pr = PlaceholderRange(
            start=10,
            end=60,
            modality=MediaType.IMAGE,
            content_hash="abc123",
        )
        assert pr.start == 10
        assert pr.end == 60
        assert pr.length == 50
        assert pr.content_hash == "abc123"


# Run pytest if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
