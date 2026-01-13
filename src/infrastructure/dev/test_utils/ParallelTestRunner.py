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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .ParallelTestResult import ParallelTestResult
from typing import Any, Dict, List
from collections.abc import Callable
import time

__version__ = VERSION

class ParallelTestRunner:
    """Helper for parallel test execution.

    Manages parallel execution of tests with worker pools.

    Example:
        runner=ParallelTestRunner(workers=4)
        runner.add_test("test1", test_func1)
        runner.add_test("test2", test_func2)
        results=runner.run_all()
    """

    def __init__(self, workers: int = 4) -> None:
        """Initialize runner.

        Args:
            workers: Number of worker threads.
        """
        self.workers = workers
        self._tests: dict[str, Callable[[], None]] = {}
        self._results: list[ParallelTestResult] = []
        self.success_count = 0
        self.failure_count = 0

    def add_test(self, name: str, test_fn: Callable[[], None]) -> None:
        """Add test to run.

        Args:
            name: Test name.
            test_fn: Test function.
        """
        self._tests[name] = test_fn

    def run(self, test_functions: list[Callable[[], Any]], fail_fast: bool = True) -> list[Any]:
        """Run tests in parallel.

        Args:
            test_functions: List of test functions to run.
            fail_fast: Stop on first failure.

        Returns:
            List of results from test functions.
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed
        self.success_count = 0
        self.failure_count = 0
        results: list[Any] = []
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = {executor.submit(test_fn): i for i, test_fn in enumerate(test_functions)}
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    self.success_count += 1
                except Exception:
                    self.failure_count += 1
                    if fail_fast:
                        executor.shutdown(wait=False)
                        raise
                    results.append(None)
        return results

    def _run_test(
        self,
        name: str,
        test_fn: Callable[[], None],
        worker_id: int,
    ) -> ParallelTestResult:
        """Run a single test."""
        start = time.time()
        try:
            test_fn()
            return ParallelTestResult(
                test_name=name,
                passed=True,
                duration_ms=(time.time() - start) * 1000,
                worker_id=worker_id,
            )
        except Exception as e:
            return ParallelTestResult(
                test_name=name,
                passed=False,
                duration_ms=(time.time() - start) * 1000,
                error=str(e),
                worker_id=worker_id,
            )

    def run_all(self) -> list[ParallelTestResult]:
        """Run all tests in parallel.

        Returns:
            List of test results.
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed, Future

        self._results = []

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures: dict[Future[ParallelTestResult], str] = {}
            for i, (name, test_fn) in enumerate(self._tests.items()):
                worker_id = i % self.workers
                future = executor.submit(self._run_test, name, test_fn, worker_id)
                futures[future] = name

            for future in as_completed(futures):
                result: ParallelTestResult = future.result()
                self._results.append(result)

        return self._results

    def get_summary(self) -> dict[str, Any]:
        """Get summary of parallel test execution."""
        total = len(self._results)
        passed = sum(1 for r in self._results if r.passed)
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "total_duration_ms": sum(r.duration_ms for r in self._results),
        }