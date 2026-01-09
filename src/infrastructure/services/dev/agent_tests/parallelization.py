#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors
# Licensed under the Apache License, Version 2.0 (the "License");

"""ParallelizationStrategy for test distribution."""

from typing import Dict, List, Optional


class ParallelizationStrategy:
    """Strategy for parallel test execution."""

    def __init__(self, strategy_type: str = "round_robin", workers: int = 1) -> None:
        """Initialize strategy."""
        self.strategy_type = strategy_type
        self.workers = int(workers)

    def distribute(self, tests: List[str], workers: Optional[int] = None) -> Dict[int, List[str]]:
        """Distribute tests across workers."""
        worker_count = int(workers) if workers is not None else self.workers
        worker_count = max(worker_count, 1)
        result: Dict[int, List[str]] = {i: [] for i in range(worker_count)}
        if self.strategy_type == "round_robin":
            for i, test in enumerate(tests):
                result[i % worker_count].append(test)
            return result

        for test in sorted(tests, key=len, reverse=True):
            min_idx = min(result.keys(), key=lambda idx: len(result[idx]))
            result[min_idx].append(test)
        return result

    def distribute_balanced(self, tests: Dict[str, float]) -> Dict[int, List[str]]:
        """Distribute tests while attempting to balance total duration."""
        worker_count = max(self.workers, 1)
        assignments: Dict[int, List[str]] = {i: [] for i in range(worker_count)}
        loads: Dict[int, float] = {i: 0.0 for i in range(worker_count)}
        for test_name, duration in sorted(tests.items(), key=lambda kv: kv[1], reverse=True):
            target = min(loads.keys(), key=lambda idx: loads[idx])
            assignments[target].append(test_name)
            loads[target] += float(duration)
        return assignments
