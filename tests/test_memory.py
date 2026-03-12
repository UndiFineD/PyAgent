#!/usr/bin/env python
"""Test the memory package."""
from rust_core import SharedMemory


def test_shared_memory_put_get() -> None:
    """Putting a value in SharedMemory and then getting it should return the same value."""
    mem = SharedMemory(bytes([0xAA] * 32))
    assert mem.get(b"key") is None
    mem.put(b"key", b"value")
    assert mem.get(b"key") == b"value"
    # overwrite
    mem.put(b"key", b"123")
    assert mem.get(b"key") == b"123"
