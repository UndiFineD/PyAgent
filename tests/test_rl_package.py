#!/usr/bin/env python3
"""Package-level RL API surface checks without direct `import rl` syntax."""

from __future__ import annotations

import importlib


def test_rl_package_exports_slice1_api() -> None:
    """Verify RL package exposes the expected Slice 1 API symbols."""
    module = importlib.import_module("rl")

    assert module.__name__ == "rl"
    assert hasattr(module, "discounted_return")
    assert hasattr(module, "validate")
    assert set(module.__all__) == {"discounted_return", "validate"}
