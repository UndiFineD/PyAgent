#!/usr/bin/env python3
try:
    from src.infrastructure.services.dev.agent_tests.testing_utils import *  # type: ignore
except Exception:
    # Minimal fallbacks
    class VisualRegressionTester:
        def __init__(self, *a, **k):
            raise RuntimeError("testing_utils not available")

    class ContractTestRunner:
        def __init__(self, *a, **k):
            raise RuntimeError("testing_utils not available")

    class ResultAggregator:
        def __init__(self, *a, **k):
            raise RuntimeError("testing_utils not available")

    class TestMetricsCollector:
        def __init__(self, *a, **k):
            raise RuntimeError("testing_utils not available")


__all__ = [
    "VisualRegressionTester",
    "ContractTestRunner",
    "ResultAggregator",
    "TestMetricsCollector",
]
