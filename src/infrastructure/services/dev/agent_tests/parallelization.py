#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""ParallelizationStrategy for test distribution."""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ParallelizationStrategy:
    """Strategy for parallel test execution."""

    def __init__(self, strategy_type: str = "round_robin", workers: int = 1) -> None:
        """Initialize strategy."""
        self.strategy_type = strategy_type
        self.workers = int(workers)

    def distribute(
        self, tests: list[str], workers: int | None = None
    ) -> dict[int, list[str]]:
        """Distribute tests across workers."""
        worker_count = int(workers) if workers is not None else self.workers
        worker_count = max(worker_count, 1)
        result: dict[int, list[str]] = {i: [] for i in range(worker_count)}
        if self.strategy_type == "round_robin":
            for i, test in enumerate(tests):
                result[i % worker_count].append(test)
            return result

        for test in sorted(tests, key=len, reverse=True):
            min_idx = min(result.keys(), key=lambda idx: len(result[idx]))
            result[min_idx].append(test)
        return result

    def distribute_balanced(self, tests: dict[str, float]) -> dict[int, list[str]]:
        """Distribute tests while attempting to balance total duration."""
        worker_count = max(self.workers, 1)
        assignments: dict[int, list[str]] = {i: [] for i in range(worker_count)}
        loads: dict[int, float] = {i: 0.0 for i in range(worker_count)}
        for test_name, duration in sorted(
            tests.items(), key=lambda kv: kv[1], reverse=True
        ):
            target = min(loads.keys(), key=lambda idx: loads[idx])
            assignments[target].append(test_name)
            loads[target] += float(duration)
        return assignments
