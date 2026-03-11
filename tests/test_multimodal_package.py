#!/usr/bin/env python3
"""Test that all multimodal package components can be imported."""


def test_multimodal_package_import() -> None:
    """Test that the multimodal package can be imported."""
    import multimodal  # noqa: F401
    assert hasattr(multimodal, "__name__")
