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

import pytest
from core.base.common.utils.hash_registry import HashAlgorithm, ContentHasher, is_fips_mode, hash_sha256, hash_sha1, hash_md5, hash_xxhash64, hash_xxhash128, hash_fnv1a, safe_hash, get_hash_fn, get_hash_fn_by_name, hash_with


def test_hashalgorithm_basic():
    assert HashAlgorithm is not None


def test_contenthasher_basic():
    assert ContentHasher is not None


def test_is_fips_mode_basic():
    assert callable(is_fips_mode)


def test_hash_sha256_basic():
    assert callable(hash_sha256)


def test_hash_sha1_basic():
    assert callable(hash_sha1)


def test_hash_md5_basic():
    assert callable(hash_md5)


def test_hash_xxhash64_basic():
    assert callable(hash_xxhash64)


def test_hash_xxhash128_basic():
    assert callable(hash_xxhash128)


def test_hash_fnv1a_basic():
    assert callable(hash_fnv1a)


def test_safe_hash_basic():
    assert callable(safe_hash)


def test_get_hash_fn_basic():
    assert callable(get_hash_fn)


def test_get_hash_fn_by_name_basic():
    assert callable(get_hash_fn_by_name)


def test_hash_with_basic():
    assert callable(hash_with)
