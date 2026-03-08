# HashRegistry

**File**: `src\core\base\utils\HashRegistry.py`  
**Type**: Python Module  
**Summary**: 2 classes, 13 functions, 13 imports  
**Lines**: 334  
**Complexity**: 17 (moderate)

## Overview

HashRegistry - Unified hashing utilities with multiple backends.

Inspired by vLLM's hashing.py patterns for flexible hash function selection.

Supports:
- SHA-256 (cryptographic, FIPS-compliant)
- MD5 (fast, non-cryptographic)  
- xxHash (fastest, non-cryptographic)
- FNV-1a (Rust-native fast hash)
- Safe hash (auto-selects based on environment)

Phase 17: vLLM Pattern Integration (P2)

## Classes (2)

### `HashAlgorithm`

**Inherits from**: Enum

Available hash algorithms.

### `ContentHasher`

Configurable content hasher for cache keys.

Example:
    >>> hasher = ContentHasher(algorithm='xxhash64', prefix='cache')
    >>> key = hasher.hash("some content")
    >>> print(key)  # cache:a1b2c3d4e5f6g7h8

**Methods** (4):
- `__init__(self, algorithm, prefix, truncate)`
- `hash(self, data)`
- `hash_dict(self, data)`
- `hash_file(self, filepath, chunk_size)`

## Functions (13)

### `_is_fips_mode()`

Check if running in FIPS-compliant mode.

### `is_fips_mode()`

Cached check for FIPS mode.

### `hash_sha256(data)`

SHA-256 hash (64 hex characters).

Cryptographically secure, FIPS-compliant.

### `hash_sha1(data)`

SHA-1 hash (40 hex characters).

Not recommended for security, but faster than SHA-256.

### `hash_md5(data)`

MD5 hash (32 hex characters).

Fast, not cryptographically secure.
May not work in FIPS mode.

### `hash_xxhash64(data)`

xxHash64 hash (16 hex characters).

Very fast, non-cryptographic.
Falls back to FNV-1a if xxhash not installed.

### `hash_xxhash128(data)`

xxHash128 hash (32 hex characters).

Very fast, non-cryptographic, larger output.
Falls back to SHA-1 if xxhash not installed.

### `_fnv1a_hash(data)`

FNV-1a 64-bit hash implementation.

### `hash_fnv1a(data)`

FNV-1a 64-bit hash (16 hex characters).

Fast, non-cryptographic, pure Python/Rust.

### `safe_hash(data)`

Safe hash that works in any environment.

- Uses MD5 in normal mode (fast)
- Falls back to SHA-256 in FIPS mode (compliant)

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `enum.Enum`
- `enum.auto`
- `functools.lru_cache`
- `hashlib`
- `json`
- `os`
- `rust_core`
- `typing.Any`
- `typing.Callable`
- `typing.Union`
- `xxhash`

---
*Auto-generated documentation*
