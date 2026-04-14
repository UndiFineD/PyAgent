#!/usr/bin/env python3
"""Package-level speculation API surface checks without direct import syntax."""

from __future__ import annotations

import importlib


def test_speculation_package_exports_slice1_api() -> None:
    """Verify speculation package exposes the expected Slice 1 API symbols."""
    module = importlib.import_module("speculation")

    assert module.__name__ == "speculation"
    assert hasattr(module, "select_candidate")
    assert hasattr(module, "validate")
    assert set(module.__all__) == {"select_candidate", "validate"}
