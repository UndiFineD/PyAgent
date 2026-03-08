#!/usr/bin/env python3
try:
    from src.infrastructure.services.dev.agent_tests.optimization import *  # type: ignore
except Exception:

    def TestSuiteOptimizer(*a, **k):
        raise RuntimeError("optimization not available")

    class CoverageGapAnalyzer:
        def __init__(self, *a, **k):
            raise RuntimeError("optimization not available")


__all__ = ["TestSuiteOptimizer", "CoverageGapAnalyzer"]
