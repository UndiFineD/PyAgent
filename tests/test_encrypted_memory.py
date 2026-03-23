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
"""Tests for the Rust-backed MemoryBlockRegistry (ChaCha20-Poly1305 + X25519 ECDH).

prj0000027 — encrypted memory blocks.
"""
import pytest

try:
    from rust_core import MemoryBlockRegistry  # type: ignore[import]
    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not _RUST_AVAILABLE,
    reason="rust_core not built — run `maturin develop` first",
)


@pytest.fixture()
def registry():
    """Return a fresh MemoryBlockRegistry."""
    return MemoryBlockRegistry()


def test_create_block_returns_uuid_string(registry):
    """create_block must return a non-empty UUID string."""
    block_id = registry.create_block()
    assert isinstance(block_id, str)
    assert len(block_id) == 36  # standard UUID format: 8-4-4-4-12


def test_put_returns_slab_index(registry):
    """put must return the slab index (0 for the first slab)."""
    block_id = registry.create_block()
    idx = registry.put(block_id, b"hello world")
    assert idx == 0


def test_multiple_puts_increment_slab_index(registry):
    """Each put in the same block increments the slab index."""
    block_id = registry.create_block()
    idx0 = registry.put(block_id, b"first")
    idx1 = registry.put(block_id, b"second")
    idx2 = registry.put(block_id, b"third")
    assert idx0 == 0
    assert idx1 == 1
    assert idx2 == 2


def test_encrypt_decrypt_roundtrip(registry):
    """Data stored with put must be faithfully recovered by get."""
    block_id = registry.create_block()
    payload = b"PyAgent encrypted memory test payload"
    idx = registry.put(block_id, payload)
    recovered = registry.get(block_id, idx)
    assert recovered == payload


def test_roundtrip_binary_payload(registry):
    """Roundtrip must preserve arbitrary binary data."""
    block_id = registry.create_block()
    binary = bytes(range(256))
    idx = registry.put(block_id, binary)
    assert registry.get(block_id, idx) == binary


def test_slab_count(registry):
    """slab_count must return the correct number of stored slabs."""
    block_id = registry.create_block()
    assert registry.slab_count(block_id) == 0
    registry.put(block_id, b"a")
    assert registry.slab_count(block_id) == 1
    registry.put(block_id, b"b")
    assert registry.slab_count(block_id) == 2


def test_purge_wipes_slabs(registry):
    """purge must remove all slabs from a block."""
    block_id = registry.create_block()
    registry.put(block_id, b"sensitive")
    registry.put(block_id, b"data")
    registry.purge(block_id)
    assert registry.slab_count(block_id) == 0


def test_remove_block(registry):
    """remove_block must remove the block from the registry."""
    block_id = registry.create_block()
    registry.put(block_id, b"ephemeral")
    registry.remove_block(block_id)
    # After removal, any access to the block should raise an error.
    with pytest.raises(Exception):
        registry.get(block_id, 0)


def test_different_blocks_are_independent(registry):
    """Two blocks in the same registry must be independently encrypted."""
    b1 = registry.create_block()
    b2 = registry.create_block()
    idx1 = registry.put(b1, b"block-one-data")
    idx2 = registry.put(b2, b"block-two-data")
    assert registry.get(b1, idx1) == b"block-one-data"
    assert registry.get(b2, idx2) == b"block-two-data"


def test_separate_registries_cannot_share_blocks():
    """A block created in one registry must not be readable from another."""
    reg_a = MemoryBlockRegistry()
    reg_b = MemoryBlockRegistry()
    block_id = reg_a.create_block()
    reg_a.put(block_id, b"secret")
    # reg_b does not know this block_id → should raise
    with pytest.raises(Exception):
        reg_b.get(block_id, 0)


def test_get_invalid_slab_index_raises(registry):
    """get must raise when the slab index is out of bounds."""
    block_id = registry.create_block()
    registry.put(block_id, b"only one slab")
    with pytest.raises(Exception):
        registry.get(block_id, 99)


def test_empty_payload_roundtrip(registry):
    """Encrypting an empty byte string must succeed and round-trip."""
    block_id = registry.create_block()
    idx = registry.put(block_id, b"")
    assert registry.get(block_id, idx) == b""
