#!/usr/bin/env python3
"""Python-level tests for rust_core SharedMemory wrapper."""

import pytest

try:
    import rust_core
except ImportError:
    pytest.skip("rust_core not available - Rust extension not compiled", allow_module_level=True)

if not hasattr(rust_core, "SharedMemory"):
    pytest.skip("rust_core.SharedMemory not available - Rust extension not compiled", allow_module_level=True)
SharedMemory = rust_core.SharedMemory  # type: ignore[attr-defined]


def test_shared_memory_python_basics() -> None:
    """Test basic put/get and master key rotation behavior of SharedMemory."""
    # construct with 32-byte master key
    mem = SharedMemory(bytes([1] * 32))
    assert mem.get(b"foo") is None
    mem.put(b"foo", b"bar")
    assert mem.get(b"foo") == b"bar"
    # rotate key and ensure old entry still verifies
    mem.rotate_master_key(bytes([2] * 32))
    assert mem.get(b"foo") == b"bar"


def test_verify_hmac_wrong_tag() -> None:
    """Test that verify_hmac returns False for an incorrect tag."""
    mem = SharedMemory(bytes([1] * 32))
    mem.put(b"a", b"b")
    # bogus tag should fail
    assert not mem.verify_hmac(b"a", b"b", bytes([0] * 32))
