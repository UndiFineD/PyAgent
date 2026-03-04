#!/usr/bin/env python3
"""Shim for agent_tests.models expected under src.classes.agent_tests."""
try:
    from importlib import import_module

    _mod = import_module("src.infrastructure.services.dev.agent_tests.models")
    for _name in dir(_mod):
        if _name.startswith("__") and _name.endswith("__"):
            continue
        globals()[_name] = getattr(_mod, _name)
    __all__ = [n for n in dir(_mod) if not (n.startswith("__") and n.endswith("__"))]
except Exception:
    # Minimal dataclass placeholders for tests when infra module isn't available.
    from dataclasses import dataclass

    @dataclass
    class TestCase:
        id: str = ""

    @dataclass
    class TestRun:
        id: str = ""

    __all__ = ["TestCase", "TestRun"]
