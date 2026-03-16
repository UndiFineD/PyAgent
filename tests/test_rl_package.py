#!/usr/bin/env python3
"""Test that all RL packages can be imported."""


def test_rl_package_import() -> None:
    """Test that the rl package can be imported."""
    import rl  # noqa: F401

    assert hasattr(rl, "__name__")
