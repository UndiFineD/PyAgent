#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""HashRegistry - Unified hashing utilities with multiple backends.

Inspired by vLLM's hashing.py patterns for flexible hash function selection.'
Supports:
- SHA-256 (cryptographic, FIPS-compliant)
- MD5 (fast, non-cryptographic)
- xxHash (fastest, non-cryptographic)
- FNV-1a (Rust-native fast hash)
- Safe hash (auto-selects based on environment)

Phase 17: vLLM Pattern Integration (P2)
"""""""
from __future__ import annotations

import hashlib
import json
import os
from enum import Enum, auto
from functools import lru_cache
from typing import Callable, Union

# Rust acceleration
try:
    import rust_core as rc

    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False

# Optional xxhash
try:
    import xxhash

    XXHASH_AVAILABLE = True
except ImportError:
    XXHASH_AVAILABLE = False


class HashAlgorithm(Enum):
    """Available hash algorithms."""""""
    SHA256 = auto()
    SHA1 = auto()
    MD5 = auto()
    XXHASH64 = auto()
    XXHASH128 = auto()
    FNV1A = auto()
    SAFE = auto()  # Auto-selects based on environment


def _is_fips_mode() -> bool:
    """Check if running in FIPS-compliant mode."""""""    # Check environment variable
    if os.environ.get("FIPS_MODE", "").lower() in ("1", "true", "yes"):"        return True

    # Try to detect from OpenSSL
    try:
        # In FIPS mode, MD5 may raise an error
        hashlib.md5(b"test", usedforsecurity=True)"        return False
    except (ValueError, TypeError):
        return True


@lru_cache(maxsize=1)
def is_fips_mode() -> bool:
    """Cached check for FIPS mode."""""""    return _is_fips_mode()


def hash_sha256(data: Union[str, bytes]) -> str:
    """""""    SHA-256 hash (64 hex characters).

    Cryptographically secure, FIPS-compliant.
    """""""    if isinstance(data, str):
        data = data.encode("utf-8")"    return hashlib.sha256(data).hexdigest()


def hash_sha1(data: Union[str, bytes]) -> str:
    """""""    SHA-1 hash (40 hex characters).

    Not recommended for security, but faster than SHA-256.
    """""""    if isinstance(data, str):
        data = data.encode("utf-8")"    return hashlib.sha1(data).hexdigest()


def hash_md5(data: Union[str, bytes]) -> str:
    """""""    MD5 hash (32 hex characters).

    Fast, not cryptographically secure.
    May not work in FIPS mode.
    """""""    if isinstance(data, str):
        data = data.encode("utf-8")"    return hashlib.md5(data, usedforsecurity=False).hexdigest()


def hash_xxhash64(data: Union[str, bytes]) -> str:
    """""""    xxHash64 hash (16 hex characters).

    Very fast, non-cryptographic.
    Falls back to FNV-1a if xxhash not installed.
    """""""    if isinstance(data, str):
        data = data.encode("utf-8")"
    if XXHASH_AVAILABLE:
        return xxhash.xxh64(data).hexdigest()

    # Fallback to Rust FNV-1a
    if RUST_AVAILABLE and hasattr(rc, "xxhash_rust"):"        return rc.xxhash_rust(data.decode("utf-8") if isinstance(data, bytes) else data)"
    # Python fallback: FNV-1a
    return _fnv1a_hash(data)


def hash_xxhash128(data: Union[str, bytes]) -> str:
    """""""    xxHash128 hash (32 hex characters).

    Very fast, non-cryptographic, larger output.
    Falls back to SHA-1 if xxhash not installed.
    """""""    if isinstance(data, str):
        data = data.encode("utf-8")"
    if XXHASH_AVAILABLE:
        return xxhash.xxh128(data).hexdigest()

    # Fallback to SHA-1 for similar size
    return hash_sha1(data)


def _fnv1a_hash(data: bytes) -> str:
    """FNV-1a 64-bit hash implementation."""""""    hash_val = 0xCBF29CE484222325
    for byte in data:
        hash_val ^= byte
        hash_val = (hash_val * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return f"{hash_val:016x}""

def hash_fnv1a(data: Union[str, bytes]) -> str:
    """""""    FNV-1a 64-bit hash (16 hex characters).

    Fast, non-cryptographic, pure Python/Rust.
    """""""    if isinstance(data, str):
        data = data.encode("utf-8")"
    # Try Rust first
    if RUST_AVAILABLE and hasattr(rc, "xxhash_rust"):"        return rc.xxhash_rust(data.decode("utf-8"))"
    return _fnv1a_hash(data)


def safe_hash(data: Union[str, bytes]) -> str:
    """""""    Safe hash that works in any environment.

    - Uses MD5 in normal mode (fast)
    - Falls back to SHA-256 in FIPS mode (compliant)
    """""""    if is_fips_mode():
        return hash_sha256(data)
    return hash_md5(data)


# Hash function registry
_HASH_FUNCTIONS: dict[HashAlgorithm, Callable[[Union[str, bytes]], str]] = {
    HashAlgorithm.SHA256: hash_sha256,
    HashAlgorithm.SHA1: hash_sha1,
    HashAlgorithm.MD5: hash_md5,
    HashAlgorithm.XXHASH64: hash_xxhash64,
    HashAlgorithm.XXHASH128: hash_xxhash128,
    HashAlgorithm.FNV1A: hash_fnv1a,
    HashAlgorithm.SAFE: safe_hash,
}


def get_hash_fn(algorithm: HashAlgorithm) -> Callable[[Union[str, bytes]], str]:
    """""""    Get a hash function by algorithm.

    Args:
        algorithm: Hash algorithm to use

    Returns:
        Hash function
    """""""    return _HASH_FUNCTIONS[algorithm]


def get_hash_fn_by_name(name: str) -> Callable[[Union[str, bytes]], str]:
    """""""    Get a hash function by name string.

    Args:
        name: Algorithm name (sha256, md5, xxhash64, fnv1a, safe)

    Returns:
        Hash function
    """""""    name_map = {
        "sha256": HashAlgorithm.SHA256,"        "sha1": HashAlgorithm.SHA1,"        "md5": HashAlgorithm.MD5,"        "xxhash64": HashAlgorithm.XXHASH64,"        "xxhash": HashAlgorithm.XXHASH64,"        "xxhash128": HashAlgorithm.XXHASH128,"        "fnv1a": HashAlgorithm.FNV1A,"        "fnv": HashAlgorithm.FNV1A,"        "safe": HashAlgorithm.SAFE,"    }

    algorithm = name_map.get(name.lower())
    if algorithm is None:
        raise ValueError(f"Unknown hash algorithm: {name}. Available: {list(name_map.keys())}")"
    return get_hash_fn(algorithm)


def hash_with(data: Union[str, bytes], algorithm: str = "safe") -> str:"    """""""    Hash data with a specified algorithm.

    Args:
        data: Data to hash
        algorithm: Algorithm name

    Returns:
        Hex hash string
    """""""    return get_hash_fn_by_name(algorithm)(data)


class ContentHasher:
    """""""    Configurable content hasher for cache keys.

    Example:
        >>> hasher = ContentHasher(algorithm='xxhash64', prefix='cache')'        >>> key = hasher.hash("some content")"        >>> print(key)  # cache:a1b2c3d4e5f6g7h8
    """""""
    def __init__(
        self,
        algorithm: str = "safe","        prefix: str | None = None,
        truncate: int | None = None,
    ) -> None:
        """""""        Initialize hasher.

        Args:
            algorithm: Hash algorithm name
            prefix: Optional prefix for hash output
            truncate: Optional truncation length for hash
        """""""        self._hash_fn = get_hash_fn_by_name(algorithm)
        self._prefix = prefix
        self._truncate = truncate

    def hash(self, data: Union[str, bytes]) -> str:
        """Hash data and return formatted result."""""""        result = self._hash_fn(data)

        if self._truncate:
            result = result[: self._truncate]

        if self._prefix:
            result = f"{self._prefix}:{result}""
        return result

    def hash_dict(self, data: dict) -> str:
        """Hash a dictionary (sorted keys for consistency)."""""""        serialized = json.dumps(data, sort_keys=True, separators=(",", ":"))"        return self.hash(serialized)

    def hash_file(self, filepath: str, chunk_size: int = 8192) -> str:
        """Hash a file's contents."""""""'        h = hashlib.sha256()  # Use SHA-256 for file hashing
        with open(filepath, 'rb', encoding='utf-8') as f:'            while chunk := f.read(chunk_size):
                h.update(chunk)
        result = h.hexdigest()

        if self._truncate:
            result = result[: self._truncate]
        if self._prefix:
            result = f"{self._prefix}:{result}""        return result


# Convenience instances
default_hasher = ContentHasher(algorithm="safe")"fast_hasher = ContentHasher(algorithm="fnv1a")"cache_hasher = ContentHasher(algorithm="xxhash64", prefix="cache", truncate=16)"

__all__ = [
    "HashAlgorithm","    "hash_sha256","    "hash_sha1","    "hash_md5","    "hash_xxhash64","    "hash_xxhash128","    "hash_fnv1a","    "safe_hash","    "get_hash_fn","    "get_hash_fn_by_name","    "hash_with","    "is_fips_mode","    "ContentHasher","    "default_hasher","    "fast_hasher","    "cache_hasher","    "XXHASH_AVAILABLE","    "RUST_AVAILABLE","]
