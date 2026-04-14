#!/usr/bin/env python3
"""Setup script for test environment."""

import os


def create_test_structure(root: str) -> None:
    """Create a basic test structure under the given root."""
    base = os.path.join(root, "tests")
    for sub in ["core", "agents"]:
        os.makedirs(os.path.join(base, sub), exist_ok=True)
        # add a placeholder __init__.py and a sample test
        with open(os.path.join(base, sub, "__init__.py"), "a", encoding="utf-8"):
            pass
        with open(os.path.join(base, sub, f"test_{sub}.py"), "a", encoding="utf-8") as f:
            f.write("def test_placeholder():\n    assert True\n")
