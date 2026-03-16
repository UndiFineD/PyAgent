#!/usr/bin/env python
"""Test the memory package."""


def test_memory_package_import() -> None:
    """Test that the memory package can be imported."""
    import memory  # noqa: F401

    assert hasattr(memory, "__name__")
