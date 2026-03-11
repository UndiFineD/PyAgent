#!/usr/bin/env python3
"""Test that all speculation packages can be imported."""


def test_speculation_package_import() -> None:
    """Test that the speculation package can be imported."""
    import speculation  # noqa: F401
    assert hasattr(speculation, "__name__")
