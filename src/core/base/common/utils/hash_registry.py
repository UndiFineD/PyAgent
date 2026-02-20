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


"""Hash utilities (simplified for tests).

Provides a small, dependency-free set of hashing helpers used by tests.
"""

from __future__ import annotations

import hashlib
import json
import os
from functools import lru_cache
from typing import Callable, Optional, Union
from enum import Enum

Data = Union[str, bytes]


class HashAlgorithm(Enum):
    SHA256 = "sha256"
    SHA1 = "sha1"
    MD5 = "md5"
    FNV1A = "fnv1a"
    SAFE = "safe"
    XXHASH64 = "xxhash64"
    XXHASH128 = "xxhash128"


def _to_bytes(data: Data) -> bytes:
    return data.encode("utf-8") if isinstance(data, str) else data


def hash_sha256(data: Data) -> str:
    return hashlib.sha256(_to_bytes(data)).hexdigest()


def hash_sha1(data: Data) -> str:
    return hashlib.sha1(_to_bytes(data)).hexdigest()


def hash_md5(data: Data) -> str:
    return hashlib.md5(_to_bytes(data)).hexdigest()


def _fnv1a_hash(data: bytes) -> str:
    # 64-bit FNV-1a implementation (simple, deterministic)
    h = 0xCBF29CE484222325
    for b in data:
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return f"{h:016x}"


def hash_fnv1a(data: Data) -> str:
    return _fnv1a_hash(_to_bytes(data))


@lru_cache(maxsize=1)
def is_fips_mode() -> bool:
    val = os.environ.get("FIPS_MODE", "").lower()
    return val in ("1", "true", "yes")


def safe_hash(data: Data) -> str:
    return hash_sha256(data) if is_fips_mode() else hash_md5(data)


_MAP: dict[str, Callable[[Data], str]] = {
    "sha256": hash_sha256,
    "sha1": hash_sha1,
    "md5": hash_md5,
    "fnv1a": hash_fnv1a,
    "safe": safe_hash,
}


def get_hash_fn_by_name(name: str) -> Callable[[Data], str]:
    fn = _MAP.get(name.lower())
    if fn is None:
        raise ValueError(f"Unknown hash algorithm: {name}")
    return fn


def get_hash_fn(alg: HashAlgorithm | str) -> Callable[[Data], str]:
    if isinstance(alg, HashAlgorithm):
        name = alg.value
    else:
        name = str(alg)
    return get_hash_fn_by_name(name)


def hash_xxhash64(data: Data) -> str:
    try:
        import xxhash

        return xxhash.xxh64(_to_bytes(data)).hexdigest()
    except Exception:
        # Fallback to fnv1a for tests if xxhash not available
        return hash_fnv1a(data)


def hash_xxhash128(data: Data) -> str:
    try:
        import xxhash

        return xxhash.xxh128(_to_bytes(data)).hexdigest()
    except Exception:
        # Fallback: combine two sha256 halves
        h = hashlib.sha256(_to_bytes(data)).hexdigest()
        return h[:32]


def hash_with(data: Data, algorithm: str = "safe") -> str:
    return get_hash_fn_by_name(algorithm)(data)


class ContentHasher:
    """Small helper to compute hashes for data, dicts and files.

    Parameters:
    - algorithm: name of the algorithm in _MAP
    - prefix: optional string prefix to prepend like "cache"
    - truncate: optional int to truncate the hex digest
    """

    def __init__(self, algorithm: str = "safe", prefix: Optional[str] = None, truncate: Optional[int] = None) -> None:
        self._fn = get_hash_fn_by_name(algorithm)
        self._prefix = prefix
        self._truncate = truncate

    def hash(self, data: Data) -> str:
        result = self._fn(data)
        if self._truncate:
            result = result[: self._truncate]
        if self._prefix:
            return f"{self._prefix}:{result}"
        return result

    def hash_dict(self, data: dict) -> str:
        serialized = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return self.hash(serialized)

    def hash_file(self, filepath: str, chunk_size: int = 8192) -> str:
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                h.update(chunk)
        result = h.hexdigest()
        if self._truncate:
            result = result[: self._truncate]
        if self._prefix:
            return f"{self._prefix}:{result}"
        return result


# Convenience instances
default_hasher = ContentHasher(algorithm="safe")
fast_hasher = ContentHasher(algorithm="fnv1a")


__all__ = [
    "hash_sha256",
    "hash_sha1",
    "hash_md5",
    "hash_fnv1a",
    "safe_hash",
    "get_hash_fn_by_name",
    "get_hash_fn",
    "HashAlgorithm",
    "hash_xxhash64",
    "hash_xxhash128",
    "hash_with",
    "ContentHasher",
    "is_fips_mode",
    "default_hasher",
    "fast_hasher",
]
