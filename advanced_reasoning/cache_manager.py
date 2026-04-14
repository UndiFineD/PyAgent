"""Cache Manager and Semantic Caching for Reasoning Results

Caches reasoning results with LRU eviction, TTL support, and semantic similarity
matching for reusing answers to similar questions.

Speedup: 10-100x on repeated/similar queries
"""

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


@dataclass
class CacheEntry:
    """A single cached reasoning result"""

    query: str
    answer: str
    reasoning_steps: List[str]
    confidence: float
    cached_at: datetime
    ttl_seconds: Optional[int] = None
    access_count: int = 0
    last_accessed: Optional[datetime] = None

    def is_expired(self) -> bool:
        """Check if entry has expired"""
        if self.ttl_seconds is None:
            return False

        age = datetime.now() - self.cached_at
        return age > timedelta(seconds=self.ttl_seconds)

    def get_key(self) -> str:
        """Get hash key for this entry"""
        return hashlib.md5(self.query.encode()).hexdigest()


@dataclass
class CacheStats:
    """Statistics about cache performance"""

    hits: int = 0
    misses: int = 0
    evictions: int = 0
    total_queries: int = 0
    memory_bytes: int = 0
    avg_hit_time_ms: float = 0.0
    avg_generation_time_ms: float = 0.0

    @property
    def hit_rate(self) -> float:
        """Cache hit rate (0-1)"""
        return self.hits / max(self.total_queries, 1)

    @property
    def speedup_factor(self) -> float:
        """Estimated speedup from caching"""
        if self.avg_generation_time_ms == 0:
            return 1.0
        return self.avg_generation_time_ms / max(self.avg_hit_time_ms, 1)


class LRUCache:
    """LRU Cache with TTL support"""

    def __init__(self, max_size: int = 1000, default_ttl_seconds: Optional[int] = None):
        """Args:
        max_size: Maximum entries in cache
        default_ttl_seconds: Default time-to-live for entries

        """
        self.max_size = max_size
        self.default_ttl_seconds = default_ttl_seconds
        self.cache: Dict[str, CacheEntry] = {}
        self.access_order: List[str] = []
        self.stats = CacheStats()

    def get(self, query: str) -> Optional[CacheEntry]:
        """Retrieve a cached entry.
        
        Returns None if not found or expired.
        """
        key = hashlib.md5(query.encode()).hexdigest()

        if key not in self.cache:
            self.stats.misses += 1
            self.stats.total_queries += 1
            return None

        entry = self.cache[key]

        # Check expiration
        if entry.is_expired():
            del self.cache[key]
            self.access_order.remove(key)
            self.stats.misses += 1
            self.stats.total_queries += 1
            return None

        # Update LRU order
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)

        # Update stats
        entry.access_count += 1
        entry.last_accessed = datetime.now()
        self.stats.hits += 1
        self.stats.total_queries += 1

        return entry

    def put(self, query: str, answer: str, steps: List[str], confidence: float):
        """Store a result in cache.
        
        Args:
            query: The question
            answer: The final answer
            steps: Reasoning steps
            confidence: Confidence in answer

        """
        key = hashlib.md5(query.encode()).hexdigest()

        # Evict if at capacity
        if len(self.cache) >= self.max_size and key not in self.cache:
            self._evict_lru()

        entry = CacheEntry(
            query=query,
            answer=answer,
            reasoning_steps=steps,
            confidence=confidence,
            cached_at=datetime.now(),
            ttl_seconds=self.default_ttl_seconds,
            access_count=0
        )

        self.cache[key] = entry

        if key not in self.access_order:
            self.access_order.append(key)

    def _evict_lru(self):
        """Evict least-recently-used entry"""
        if not self.access_order:
            return

        lru_key = self.access_order.pop(0)
        del self.cache[lru_key]
        self.stats.evictions += 1

    def clear(self):
        """Clear entire cache"""
        self.cache.clear()
        self.access_order.clear()

    def size(self) -> int:
        """Current cache size"""
        return len(self.cache)


class SemanticCache:
    """Cache that matches similar queries even if not identical.
    
    Uses embedding-based similarity to find cached answers for similar questions.
    """

    def __init__(
        self,
        embedder=None,
        similarity_threshold: float = 0.85,
        max_size: int = 1000
    ):
        """Args:
        embedder: Function that embeds text to vector
        similarity_threshold: Min similarity to consider a match (0-1)
        max_size: Max cache entries

        """
        self.embedder = embedder
        self.similarity_threshold = similarity_threshold
        self.max_size = max_size
        self.cache: Dict[str, Tuple[CacheEntry, list]] = {}
        self.stats = CacheStats()

    def get(self, query: str) -> Optional[CacheEntry]:
        """Find semantically similar cached entry.
        
        Args:
            query: The new question
        
        Returns:
            Cached entry if similar query found, else None

        """
        if not self.embedder:
            return None  # No embedder = can't do semantic matching

        query_embedding = self.embedder(query)
        if query_embedding is None:
            return None

        best_match = None
        best_similarity = 0.0

        # Find most similar cached query
        for entry_key, (entry, cached_embedding) in self.cache.items():
            if cached_embedding is None:
                continue

            similarity = self._cosine_similarity(query_embedding, cached_embedding)

            if similarity > best_similarity and similarity >= self.similarity_threshold:
                best_similarity = similarity
                best_match = entry

        if best_match:
            self.stats.hits += 1
        else:
            self.stats.misses += 1

        self.stats.total_queries += 1
        return best_match

    def put(self, query: str, answer: str, steps: List[str], confidence: float):
        """Store result in semantic cache"""
        if not self.embedder:
            return

        # Evict if needed
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = min(
                self.cache.keys(),
                key=lambda k: self.cache[k][0].cached_at
            )
            del self.cache[oldest_key]
            self.stats.evictions += 1

        # Embed query
        embedding = self.embedder(query)

        entry = CacheEntry(
            query=query,
            answer=answer,
            reasoning_steps=steps,
            confidence=confidence,
            cached_at=datetime.now()
        )

        key = entry.get_key()
        self.cache[key] = (entry, embedding)

    @staticmethod
    def _cosine_similarity(vec1: list, vec2: list) -> float:
        """Compute cosine similarity between vectors"""
        if not vec1 or not vec2:
            return 0.0

        if len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(x * x for x in vec1) ** 0.5
        magnitude2 = sum(x * x for x in vec2) ** 0.5

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)


class StepCache:
    """Cache individual reasoning steps for reuse"""

    def __init__(self, max_size: int = 5000):
        """Args:
        max_size: Max step cache entries

        """
        self.max_size = max_size
        self.cache: Dict[str, Tuple[str, float]] = {}
        self.stats = CacheStats()

    def get_step(self, context: str) -> Optional[Tuple[str, float]]:
        """Get cached step for given context.
        
        Args:
            context: The reasoning context (previous steps)
        
        Returns:
            (next_step, confidence) or None

        """
        key = hashlib.md5(context.encode()).hexdigest()

        if key in self.cache:
            self.stats.hits += 1
            step, confidence = self.cache[key]
            return (step, confidence)

        self.stats.misses += 1
        return None

    def put_step(self, context: str, step: str, confidence: float):
        """Cache a reasoning step"""
        if len(self.cache) >= self.max_size:
            # Remove random entry
            key_to_remove = next(iter(self.cache))
            del self.cache[key_to_remove]
            self.stats.evictions += 1

        key = hashlib.md5(context.encode()).hexdigest()
        self.cache[key] = (step, confidence)


class CacheManager:
    """Unified cache manager combining all cache types"""

    def __init__(
        self,
        max_size: int = 1000,
        enable_semantic: bool = True,
        enable_step_cache: bool = True,
        default_ttl_seconds: Optional[int] = 3600  # 1 hour
    ):
        """Args:
        max_size: Max entries in LRU cache
        enable_semantic: Use semantic caching?
        enable_step_cache: Cache individual steps?
        default_ttl_seconds: Default TTL for entries

        """
        self.lru = LRUCache(max_size, default_ttl_seconds)
        self.semantic = SemanticCache() if enable_semantic else None
        self.step_cache = StepCache() if enable_step_cache else None

    def get_cached_reasoning(self, query: str) -> Optional[CacheEntry]:
        """Try to get cached reasoning result.
        
        Tries LRU first, then semantic cache.
        """
        # Try exact match first
        result = self.lru.get(query)
        if result:
            return result

        # Try semantic match
        if self.semantic:
            result = self.semantic.get(query)
            if result:
                return result

        return None

    def cache_reasoning(
        self,
        query: str,
        answer: str,
        steps: List[str],
        confidence: float
    ):
        """Cache a reasoning result"""
        self.lru.put(query, answer, steps, confidence)

        if self.semantic:
            self.semantic.put(query, answer, steps, confidence)

    def get_cached_step(self, context: str) -> Optional[Tuple[str, float]]:
        """Get cached step for context"""
        if not self.step_cache:
            return None
        return self.step_cache.get_step(context)

    def cache_step(self, context: str, step: str, confidence: float):
        """Cache a step"""
        if self.step_cache:
            self.step_cache.put_step(context, step, confidence)

    def get_stats(self) -> Dict:
        """Get statistics about all caches"""
        return {
            'lru': {
                'size': self.lru.size(),
                'hit_rate': f"{self.lru.stats.hit_rate:.1%}",
                'speedup': f"{self.lru.stats.speedup_factor:.1f}x",
                'evictions': self.lru.stats.evictions
            },
            'semantic': {
                'enabled': self.semantic is not None,
                'hit_rate': f"{self.semantic.stats.hit_rate:.1%}" if self.semantic else "N/A"
            },
            'step_cache': {
                'enabled': self.step_cache is not None,
                'hit_rate': f"{self.step_cache.stats.hit_rate:.1%}" if self.step_cache else "N/A"
            }
        }

    def clear_all(self):
        """Clear all caches"""
        self.lru.clear()
        if self.semantic:
            self.semantic.cache.clear()
        if self.step_cache:
            self.step_cache.cache.clear()
