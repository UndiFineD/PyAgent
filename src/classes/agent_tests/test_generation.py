#!/usr/bin/env python3
try:
    from src.infrastructure.services.dev.agent_tests.test_generation import *  # type: ignore
except Exception:

    def TestGenerator(*a, **k):
        raise RuntimeError("test_generation not available")

    def TestCaseMinimizer(*a, **k):
        raise RuntimeError("test_generation not available")

    def TestDocGenerator(*a, **k):
        raise RuntimeError("test_generation not available")


__all__ = ["TestGenerator", "TestCaseMinimizer", "TestDocGenerator"]
