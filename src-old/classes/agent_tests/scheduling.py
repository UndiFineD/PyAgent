#!/usr/bin/env python3
try:
    from src.infrastructure.services.dev.agent_tests.scheduling import *  # type: ignore
except Exception:

    def CrossBrowserRunner(*a, **k):
        raise RuntimeError("scheduling not available")

    def TestScheduler(*a, **k):
        raise RuntimeError("scheduling not available")


__all__ = ["CrossBrowserRunner", "TestScheduler"]
