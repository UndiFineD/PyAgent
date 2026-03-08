#!/usr/bin/env python3
try:
    from src.infrastructure.services.dev.agent_tests.mutation_testing import *  # type: ignore
except Exception:

    def MutationTester(*a, **k):
        raise RuntimeError("mutation_testing not available")

    def MutationRunner(*a, **k):
        raise RuntimeError("mutation_testing not available")


__all__ = ["MutationTester", "MutationRunner"]
