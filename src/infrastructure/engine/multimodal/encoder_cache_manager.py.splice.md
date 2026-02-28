# Splice: src/infrastructure/engine/multimodal/encoder_cache_manager.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- CacheTier
- EvictionPolicy
- CacheConfig
- CacheEntry
- CacheStats
- EncoderCacheManager
- MultiTierEncoderCache

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
