#!/usr/bin/env python3
try:
    from src.infrastructure.services.dev.agent_tests.debugging import *  # type: ignore
except Exception:

    def ExecutionReplayer(*a, **k):
        raise RuntimeError("debugging not available")

    def TestProfiler(*a, **k):
        raise RuntimeError("debugging not available")

    def TestRecorder(*a, **k):
        raise RuntimeError("debugging not available")

    def TestReplayer(*a, **k):
        raise RuntimeError("debugging not available")


__all__ = ["ExecutionReplayer", "TestProfiler", "TestRecorder", "TestReplayer"]
