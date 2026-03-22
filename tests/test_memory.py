#!/usr/bin/env python
"""Test the memory package."""
import pytest
try:
    import rust_core
except ImportError:
    pytest.skip("rust_core not available - Rust extension not compiled", allow_module_level=True)

if not hasattr(rust_core, 'SharedMemory'):
    pytest.skip("rust_core.SharedMemory not available - Rust extension not compiled", allow_module_level=True)
SharedMemory = rust_core.SharedMemory


def test_shared_memory_put_get() -> None:
    """Putting a value in SharedMemory and then getting it should return the same value."""
    mem = SharedMemory(bytes([0xAA] * 32))
    assert mem.get(b"key") is None
    mem.put(b"key", b"value")
    assert mem.get(b"key") == b"value"
    # overwrite
    mem.put(b"key", b"123")
    assert mem.get(b"key") == b"123"
