#!/usr/bin/env python3
"""Existence test for observability module."""

from src.core import observability


def test_observability_import_and_validate() -> None:
    """Test that observability module can be imported and validate function runs."""
    # simply import and call validate to ensure module loads
    observability.validate()
    assert True
