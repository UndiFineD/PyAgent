# PrefixCacheManager

**File**: `src\infrastructure\engine\PrefixCacheManager.py`  
**Type**: Python Module  
**Summary**: 4 classes, 8 functions, 21 imports  
**Lines**: 477  
**Complexity**: 21 (complex)

## Overview

PrefixCacheManager - Block-level content-addressable caching.

Inspired by vLLM's v1/core/kv_cache_utils.py - implements block-level
hashing for prefix caching with LRU eviction.

## Classes (4)

### `HashAlgorithm`

**Inherits from**: Enum

Supported hash algorithms for prefix caching.

### `BlockHash`

Hash of a block's contents.

Includes the hash value and the token IDs for verification.

**Methods** (2):
- `__hash__(self)`
- `__eq__(self, other)`

### `CacheBlock`

A cached KV block.

**Methods** (1):
- `touch(self)`

### `PrefixCacheManager`

Manager for prefix caching with block-level granularity.

Implements content-addressable caching where blocks with the same
content (token IDs) share the same cached KV values.

**Methods** (10):
- `__init__(self, block_size, max_blocks, hash_algorithm, enable_eviction)`
- `compute_block_hashes(self, token_ids, extra_keys_per_block)`
- `get_cached_blocks(self, block_hashes)`
- `allocate_blocks(self, block_hashes, start_index)`
- `free_blocks(self, block_ids)`
- `_evict_lru(self)`
- `pin_block(self, block_id)`
- `unpin_block(self, block_id)`
- `reset(self)`
- `get_stats(self)`

## Functions (8)

### `get_hash_function(algorithm)`

Get hash function for the specified algorithm.

### `hash_block_tokens(hash_function, parent_block_hash, curr_block_token_ids, extra_keys)`

Compute hash for a block of tokens.

The hash incorporates:
- Parent block hash (for chain integrity)
- Current block's token IDs
- Optional extra keys (e.g., image hashes)

Args:
    hash_function: Hash function to use
    parent_block_hash: Hash of parent block (None for first block)
    curr_block_token_ids: Token IDs in this block
    extra_keys: Additional keys to include in hash
    
Returns:
    BlockHash with computed hash value

### `hash_block_tokens_rust(parent_hash, token_ids, extra_keys)`

Rust-accelerated block hashing.
Falls back to Python implementation.

### `init_none_hash(hash_function)`

Initialize a null hash value.

### `compute_prefix_match(cached_hashes, request_hashes)`

Find the length of common prefix between cached and request hashes.

Uses binary search for efficiency.

### `compute_prefix_match_rust(cached_hashes, request_hashes)`

Rust-accelerated prefix matching.

### `compute_cache_keys(request_ids, token_ids_list, block_size)`

Compute cache keys for multiple requests.

Args:
    request_ids: List of request IDs
    token_ids_list: Token IDs for each request
    block_size: Block size for hashing
    
Returns:
    Dict mapping request ID to list of block hashes

### `compute_cache_keys_rust(request_ids, token_ids_list, block_size)`

Rust-accelerated batch cache key computation.

## Dependencies

**Imports** (21):
- `__future__.annotations`
- `collections.OrderedDict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `hashlib`
- `logging`
- `rust_core.compute_cache_keys_rust`
- `rust_core.compute_prefix_match_rust`
- `rust_core.hash_block_tokens_rust`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- ... and 6 more

---
*Auto-generated documentation*
