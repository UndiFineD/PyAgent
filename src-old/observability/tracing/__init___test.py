#!/usr/bin/env python3
"""Test for src.observability.tracing.__init__."""
import importlib


def test_import_src_observability_tracing___init__():
    """Test that src.observability.tracing.__init__ imports without error."""
    mod = importlib.import_module("src.observability.tracing.__init__")
    # Basic smoke tests
    assert mod is not None
