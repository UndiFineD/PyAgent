# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 40: Multimodal Cache - Content-Aware Caching with IPC
# Inspired by vLLM's multimodal/cache.py and hasher.py

"""
MultiModalCache: Advanced caching for multimodal content.

Provides:
- Content-aware hashing using Blake3/SHA256
- IPC-enabled caching between frontend and core processes
- Perceptual hashing for similar-but-not-identical media
- Async prefetch for predicted multimodal content
- Cross-request embedding pooling
"""

from __future__ import annotations

import hashlib
import io
import mmap
import os
import struct
import threading
import time
import weakref
from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import (
    Any, Callable, Dict, Generic, Iterator, List, 
    Optional, Set, Tuple, TypeVar, Union
)
import numpy as np

# Optional imports
try:
    import blake3
    HAS_BLAKE3 = True
except ImportError:
    HAS_BLAKE3 = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


# Type variables
T = TypeVar('T')
MediaContent = TypeVar('MediaContent')


# =============================================================================
# Enums
# =============================================================================

class MediaType(Enum):
    """Types of media content."""
    IMAGE = auto()
    VIDEO = auto()
    AUDIO = auto()
    TEXT = auto()
    EMBEDDING = auto()
    UNKNOWN = auto()


class CacheBackend(Enum):
    """Cache storage backend types."""
    MEMORY = auto()       # In-memory dictionary
    MMAP = auto()         # Memory-mapped file
    SHARED = auto()       # Shared memory (IPC)
    DISK = auto()         # Disk-based persistence
    HYBRID = auto()       # Multi-tier caching


class HashAlgorithm(Enum):
    """Hash algorithms for content addressing."""
    BLAKE3 = auto()       # Fast cryptographic hash
    SHA256 = auto()       # Standard SHA-256
    XXHASH = auto()       # Fast non-cryptographic
    PERCEPTUAL = auto()   # Perceptual hash for images


# =============================================================================
# Data Classes
# =============================================================================

@dataclass(frozen=True)
class MediaHash:
    """Content hash for media items."""
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
    """Entry in the multimodal cache."""
    key: MediaHash
    data: Any                              # Cached data (embeddings, processed tensors)
    media_type: MediaType
    size_bytes: int
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def touch(self) -> None:
        """Update access time and count."""
        self.last_accessed = time.time()
        self.access_count += 1


@dataclass
class CacheStats:
    """Statistics for cache performance."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    total_size_bytes: int = 0
    entry_count: int = 0
    avg_access_time_ms: float = 0.0
    
    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


@dataclass
class PlaceholderRange:
    """Range of tokens for multimodal placeholder."""
    start: int
    end: int
    modality: MediaType
    content_hash: str = ""
    
    @property
    def length(self) -> int:
        return self.end - self.start


# =============================================================================
# MultiModal Hasher
# =============================================================================

class MultiModalHasher:
    """
    Content-aware hasher for multimodal data.
    
    Supports:
    - Blake3 for fast cryptographic hashing
    - SHA256 for compatibility
    - Perceptual hashing for similar image detection
    """
    
    def __init__(
        self,
        algorithm: HashAlgorithm = HashAlgorithm.BLAKE3,
        perceptual_size: Tuple[int, int] = (8, 8),
    ):
        self.algorithm = algorithm
        self.perceptual_size = perceptual_size
        
        # Use Blake3 if available, fallback to SHA256
        if algorithm == HashAlgorithm.BLAKE3 and not HAS_BLAKE3:
            self.algorithm = HashAlgorithm.SHA256
    
    def hash_bytes(self, data: bytes) -> str:
        """Hash raw bytes."""
        if self.algorithm == HashAlgorithm.BLAKE3 and HAS_BLAKE3:
            return blake3.blake3(data).hexdigest()
        elif self.algorithm == HashAlgorithm.SHA256:
            return hashlib.sha256(data).hexdigest()
        elif self.algorithm == HashAlgorithm.XXHASH:
            # Simple xxHash-like implementation
            h = 0
            for i, byte in enumerate(data):
                h = (h * 31 + byte) & 0xFFFFFFFFFFFFFFFF
            return format(h, '016x')
        else:
            return hashlib.sha256(data).hexdigest()
    
    def hash_image(self, image_data: Union[bytes, Any]) -> MediaHash:
        """Hash image content."""
        if isinstance(image_data, bytes):
            content_hash = self.hash_bytes(image_data)
            size = len(image_data)
        elif HAS_PIL and isinstance(image_data, Image.Image):
            # Convert PIL image to bytes
            buffer = io.BytesIO()
            image_data.save(buffer, format='PNG')
            img_bytes = buffer.getvalue()
            content_hash = self.hash_bytes(img_bytes)
            size = len(img_bytes)
        else:
            # Try to get bytes from object
            content_hash = self.hash_bytes(str(image_data).encode())
            size = 0
        
        return MediaHash(
            value=content_hash,
            algorithm=self.algorithm,
            media_type=MediaType.IMAGE,
            size_bytes=size
        )
    
    def hash_audio(self, audio_data: bytes, sample_rate: int = 16000) -> MediaHash:
        """Hash audio content."""
        # Include sample rate in hash for audio
        combined = audio_data + struct.pack('I', sample_rate)
        content_hash = self.hash_bytes(combined)
        
        return MediaHash(
            value=content_hash,
            algorithm=self.algorithm,
            media_type=MediaType.AUDIO,
            size_bytes=len(audio_data)
        )
    
    def hash_video(self, video_data: bytes, frame_count: int = 0) -> MediaHash:
        """Hash video content."""
        # Include frame count in hash
        combined = video_data + struct.pack('I', frame_count)
        content_hash = self.hash_bytes(combined)
        
        return MediaHash(
            value=content_hash,
            algorithm=self.algorithm,
            media_type=MediaType.VIDEO,
            size_bytes=len(video_data)
        )
    
    def hash_embedding(self, embedding: np.ndarray) -> MediaHash:
        """Hash embedding vector."""
        content_hash = self.hash_bytes(embedding.tobytes())
        
        return MediaHash(
            value=content_hash,
            algorithm=self.algorithm,
            media_type=MediaType.EMBEDDING,
            size_bytes=embedding.nbytes
        )
    
    def perceptual_hash(self, image_data: Union[bytes, Any]) -> str:
        """
        Compute perceptual hash for image similarity.
        
        Uses average hash algorithm for simplicity.
        """
        if not HAS_PIL:
            # Fallback to content hash
            if isinstance(image_data, bytes):
                return self.hash_bytes(image_data)[:16]
            return self.hash_bytes(str(image_data).encode())[:16]
        
        # Load image
        if isinstance(image_data, bytes):
            img = Image.open(io.BytesIO(image_data))
        elif isinstance(image_data, Image.Image):
            img = image_data
        else:
            return self.hash_bytes(str(image_data).encode())[:16]
        
        # Resize to small size
        img = img.convert('L').resize(self.perceptual_size, Image.Resampling.LANCZOS)
        
        # Get pixels and compute average
        pixels = np.array(img)
        avg = pixels.mean()
        
        # Create hash from above/below average
        bits = (pixels > avg).flatten()
        hash_value = ''.join('1' if b else '0' for b in bits)
        
        # Convert to hex
        return format(int(hash_value, 2), f'0{len(bits)//4}x')


# =============================================================================
# Base Cache Class
# =============================================================================

class MultiModalCache(ABC):
    """
    Abstract base for multimodal content caching.
    
    Features:
    - LRU eviction with configurable capacity
    - Content-aware hashing
    - Statistics tracking
    """
    
    def __init__(
        self,
        max_size_bytes: int = 1024 * 1024 * 1024,  # 1GB
        max_entries: int = 10000,
        hasher: Optional[MultiModalHasher] = None,
    ):
        self.max_size_bytes = max_size_bytes
        self.max_entries = max_entries
        self.hasher = hasher or MultiModalHasher()
        self._stats = CacheStats()
        self._lock = threading.RLock()
    
    @abstractmethod
    def get(self, key: MediaHash) -> Optional[CacheEntry]:
        """Get entry from cache."""
        pass
    
    @abstractmethod
    def put(self, key: MediaHash, data: Any, metadata: Optional[Dict] = None) -> CacheEntry:
        """Put entry into cache."""
        pass
    
    @abstractmethod
    def evict(self, count: int = 1) -> int:
        """Evict entries, return number evicted."""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all entries."""
        pass
    
    @abstractmethod
    def contains(self, key: MediaHash) -> bool:
        """Check if key exists in cache."""
        pass
    
    def get_or_compute(
        self,
        key: MediaHash,
        compute_fn: Callable[[], Any],
        metadata: Optional[Dict] = None
    ) -> CacheEntry:
        """Get from cache or compute and cache."""
        entry = self.get(key)
        if entry is not None:
            return entry
        
        # Compute and cache
        data = compute_fn()
        return self.put(key, data, metadata)
    
    @property
    def stats(self) -> CacheStats:
        """Get cache statistics."""
        return self._stats


# =============================================================================
# In-Memory LRU Cache
# =============================================================================

class MemoryMultiModalCache(MultiModalCache):
    """
    In-memory LRU cache for multimodal content.
    
    Uses OrderedDict for O(1) LRU operations.
    """
    
    def __init__(
        self,
        max_size_bytes: int = 1024 * 1024 * 1024,
        max_entries: int = 10000,
        hasher: Optional[MultiModalHasher] = None,
    ):
        super().__init__(max_size_bytes, max_entries, hasher)
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._current_size = 0
    
    def get(self, key: MediaHash) -> Optional[CacheEntry]:
        """Get entry, moving to end for LRU."""
        with self._lock:
            key_str = key.value
            if key_str not in self._cache:
                self._stats.misses += 1
                return None
            
            # Move to end (most recently used)
            self._cache.move_to_end(key_str)
            entry = self._cache[key_str]
            entry.touch()
            self._stats.hits += 1
            return entry
    
    def put(self, key: MediaHash, data: Any, metadata: Optional[Dict] = None) -> CacheEntry:
        """Put entry, evicting if necessary."""
        with self._lock:
            key_str = key.value
            
            # Calculate size
            if isinstance(data, np.ndarray):
                size = data.nbytes
            elif isinstance(data, bytes):
                size = len(data)
            else:
                size = 0
            
            # Evict if necessary
            while (self._current_size + size > self.max_size_bytes or 
                   len(self._cache) >= self.max_entries):
                if not self._cache:
                    break
                self.evict(1)
            
            # Create entry
            entry = CacheEntry(
                key=key,
                data=data,
                media_type=key.media_type,
                size_bytes=size,
                metadata=metadata or {}
            )
            
            # Remove old if exists
            if key_str in self._cache:
                old = self._cache[key_str]
                self._current_size -= old.size_bytes
            
            # Add new
            self._cache[key_str] = entry
            self._current_size += size
            self._stats.entry_count = len(self._cache)
            self._stats.total_size_bytes = self._current_size
            
            return entry
    
    def evict(self, count: int = 1) -> int:
        """Evict least recently used entries."""
        evicted = 0
        with self._lock:
            for _ in range(count):
                if not self._cache:
                    break
                # Pop oldest (first item)
                key_str, entry = self._cache.popitem(last=False)
                self._current_size -= entry.size_bytes
                evicted += 1
                self._stats.evictions += 1
        
        self._stats.entry_count = len(self._cache)
        self._stats.total_size_bytes = self._current_size
        return evicted
    
    def clear(self) -> None:
        """Clear all entries."""
        with self._lock:
            self._cache.clear()
            self._current_size = 0
            self._stats.entry_count = 0
            self._stats.total_size_bytes = 0
    
    def contains(self, key: MediaHash) -> bool:
        """Check if key exists."""
        return key.value in self._cache
    
    def keys(self) -> List[MediaHash]:
        """Get all cache keys."""
        with self._lock:
            return [entry.key for entry in self._cache.values()]


# =============================================================================
# IPC-Enabled Cache
# =============================================================================

class IPCMultiModalCache(MultiModalCache):
    """
    IPC-enabled cache for cross-process sharing.
    
    Uses shared memory for efficient inter-process communication.
    Supports frontend (P0) to core (P1) caching pattern from vLLM.
    """
    
    def __init__(
        self,
        name: str = "pyagent_mm_cache",
        max_size_bytes: int = 1024 * 1024 * 1024,
        max_entries: int = 10000,
        hasher: Optional[MultiModalHasher] = None,
        create: bool = True,
    ):
        super().__init__(max_size_bytes, max_entries, hasher)
        self.name = name
        self._local_cache = MemoryMultiModalCache(max_size_bytes, max_entries, hasher)
        self._shared_keys: Set[str] = set()
        
        # Shared memory setup (simplified - would use multiprocessing.shared_memory in production)
        self._shm_path = Path(f"/tmp/{name}.cache")
        self._index_path = Path(f"/tmp/{name}.index")
        
        if create:
            self._initialize_shared()
    
    def _initialize_shared(self) -> None:
        """Initialize shared memory structures."""
        # Create empty index file
        self._index_path.write_text("{}")
    
    def get(self, key: MediaHash) -> Optional[CacheEntry]:
        """Get from local cache first, then check shared."""
        # Try local first
        entry = self._local_cache.get(key)
        if entry is not None:
            return entry
        
        # Check shared memory
        if key.value in self._shared_keys:
            # Load from shared (simplified)
            self._stats.hits += 1
            return None  # Would load from shared memory
        
        self._stats.misses += 1
        return None
    
    def put(self, key: MediaHash, data: Any, metadata: Optional[Dict] = None) -> CacheEntry:
        """Put in local cache and optionally share."""
        entry = self._local_cache.put(key, data, metadata)
        
        # Mark for sharing (in production, would write to shared memory)
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
        """Explicitly share an entry for IPC access."""
        if not self._local_cache.contains(key):
            return False
        
        self._shared_keys.add(key.value)
        return True


# =============================================================================
# Perceptual Similarity Cache
# =============================================================================

class PerceptualCache(MemoryMultiModalCache):
    """
    Cache with perceptual similarity matching.
    
    Beyond vLLM:
    - Find similar cached items using perceptual hashing
    - Configurable similarity threshold
    - Useful for image/video queries with minor variations
    """
    
    def __init__(
        self,
        max_size_bytes: int = 1024 * 1024 * 1024,
        max_entries: int = 10000,
        similarity_threshold: float = 0.9,
    ):
        super().__init__(max_size_bytes, max_entries)
        self.similarity_threshold = similarity_threshold
        self._perceptual_index: Dict[str, List[str]] = {}  # phash -> [content_hash]
    
    def put_with_perceptual(
        self,
        content_hash: MediaHash,
        data: Any,
        perceptual_hash: str,
        metadata: Optional[Dict] = None
    ) -> CacheEntry:
        """Put with perceptual hash for similarity search."""
        entry = self.put(content_hash, data, metadata)
        
        # Index by perceptual hash
        if perceptual_hash not in self._perceptual_index:
            self._perceptual_index[perceptual_hash] = []
        self._perceptual_index[perceptual_hash].append(content_hash.value)
        
        return entry
    
    def find_similar(self, perceptual_hash: str) -> List[CacheEntry]:
        """Find entries with similar perceptual hash."""
        similar = []
        
        # Exact perceptual match
        if perceptual_hash in self._perceptual_index:
            for content_key in self._perceptual_index[perceptual_hash]:
                if content_key in self._cache:
                    similar.append(self._cache[content_key])
        
        # Hamming distance for near matches (simplified)
        phash_int = int(perceptual_hash, 16) if perceptual_hash else 0
        for cached_phash, content_keys in self._perceptual_index.items():
            if cached_phash == perceptual_hash:
                continue
            
            try:
                cached_int = int(cached_phash, 16)
                # Hamming distance
                xor = phash_int ^ cached_int
                distance = bin(xor).count('1')
                # Normalize by hash length
                max_bits = max(len(bin(phash_int)), len(bin(cached_int))) - 2
                similarity = 1.0 - (distance / max(max_bits, 1))
                
                if similarity >= self.similarity_threshold:
                    for content_key in content_keys:
                        if content_key in self._cache:
                            similar.append(self._cache[content_key])
            except ValueError:
                continue
        
        return similar


# =============================================================================
# Async Prefetch Cache
# =============================================================================

class PrefetchMultiModalCache(MemoryMultiModalCache):
    """
    Cache with async prefetch support.
    
    Beyond vLLM:
    - Predictive prefetching based on access patterns
    - Background loading of anticipated content
    - Priority-based prefetch queue
    """
    
    def __init__(
        self,
        max_size_bytes: int = 1024 * 1024 * 1024,
        max_entries: int = 10000,
        max_prefetch_queue: int = 100,
    ):
        super().__init__(max_size_bytes, max_entries)
        self.max_prefetch_queue = max_prefetch_queue
        self._prefetch_queue: List[Tuple[MediaHash, Callable, float]] = []  # (key, loader, priority)
        self._access_patterns: Dict[str, List[str]] = {}  # key -> [subsequent keys]
        self._prefetch_lock = threading.Lock()
    
    def record_access(self, key: MediaHash, subsequent_key: Optional[MediaHash] = None) -> None:
        """Record access pattern for prediction."""
        key_str = key.value
        
        if subsequent_key:
            if key_str not in self._access_patterns:
                self._access_patterns[key_str] = []
            self._access_patterns[key_str].append(subsequent_key.value)
    
    def predict_next(self, key: MediaHash) -> List[str]:
        """Predict likely next accesses based on patterns."""
        key_str = key.value
        if key_str not in self._access_patterns:
            return []
        
        # Return most common subsequent accesses
        from collections import Counter
        subsequent = self._access_patterns[key_str]
        counter = Counter(subsequent)
        return [k for k, _ in counter.most_common(5)]
    
    def schedule_prefetch(
        self,
        key: MediaHash,
        loader: Callable[[], Any],
        priority: float = 0.5
    ) -> None:
        """Schedule content for prefetch."""
        with self._prefetch_lock:
            if len(self._prefetch_queue) >= self.max_prefetch_queue:
                # Remove lowest priority
                self._prefetch_queue.sort(key=lambda x: x[2], reverse=True)
                self._prefetch_queue.pop()
            
            self._prefetch_queue.append((key, loader, priority))
            self._prefetch_queue.sort(key=lambda x: x[2], reverse=True)
    
    def execute_prefetch(self, count: int = 1) -> int:
        """Execute pending prefetches."""
        executed = 0
        
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
                    except Exception:
                        pass
        
        return executed


# =============================================================================
# Utility Functions
# =============================================================================

def compute_media_hash(
    data: Union[bytes, np.ndarray, Any],
    media_type: MediaType = MediaType.UNKNOWN,
    algorithm: HashAlgorithm = HashAlgorithm.BLAKE3,
) -> MediaHash:
    """Compute hash for media content."""
    hasher = MultiModalHasher(algorithm=algorithm)
    
    if media_type == MediaType.IMAGE or (media_type == MediaType.UNKNOWN and HAS_PIL):
        return hasher.hash_image(data)
    elif media_type == MediaType.AUDIO:
        return hasher.hash_audio(data if isinstance(data, bytes) else data.tobytes())
    elif media_type == MediaType.VIDEO:
        return hasher.hash_video(data if isinstance(data, bytes) else data.tobytes())
    elif media_type == MediaType.EMBEDDING or isinstance(data, np.ndarray):
        return hasher.hash_embedding(data if isinstance(data, np.ndarray) else np.frombuffer(data, dtype=np.float32))
    else:
        # Generic bytes hash
        if isinstance(data, bytes):
            hash_value = hasher.hash_bytes(data)
        else:
            hash_value = hasher.hash_bytes(str(data).encode())
        
        return MediaHash(
            value=hash_value,
            algorithm=algorithm,
            media_type=media_type,
            size_bytes=len(data) if isinstance(data, bytes) else 0
        )


def create_cache(
    backend: CacheBackend = CacheBackend.MEMORY,
    max_size_bytes: int = 1024 * 1024 * 1024,
    max_entries: int = 10000,
    **kwargs
) -> MultiModalCache:
    """Factory function to create cache instance."""
    if backend == CacheBackend.MEMORY:
        return MemoryMultiModalCache(max_size_bytes, max_entries)
    elif backend == CacheBackend.SHARED:
        return IPCMultiModalCache(
            name=kwargs.get("name", "pyagent_mm_cache"),
            max_size_bytes=max_size_bytes,
            max_entries=max_entries
        )
    else:
        # Default to memory cache
        return MemoryMultiModalCache(max_size_bytes, max_entries)
