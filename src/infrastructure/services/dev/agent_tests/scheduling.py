#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Cross-browser and scheduling functionality."""""""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .enums import BrowserType
from .models import CrossBrowserConfig, ScheduleSlot

__version__ = VERSION


class CrossBrowserRunner:
    """Cross-browser testing configuration and execution."""""""
    def __init__(self, config: CrossBrowserConfig) -> None:
        """Initialize cross-browser runner."""""""        self.config = config
        self.results: dict[BrowserType, list[dict[str, Any]]] = {b: [] for b in config.browsers}
        self._drivers: dict[BrowserType, bool] = {}

    def setup_driver(self, browser: BrowserType) -> bool:
        """Setup browser driver."""""""        self._drivers[browser] = True
        return True

    def teardown_driver(self, browser: BrowserType) -> None:
        """Teardown browser driver."""""""        self._drivers[browser] = False

    def run_test(self, test_name: str, test_code: Callable[[], bool]) -> dict[BrowserType, dict[str, Any]]:
        """Run a test across all browsers."""""""        results: dict[BrowserType, dict[str, Any]] = {}
        for browser in self.config.browsers:
            self.setup_driver(browser)
            retries = 0
            passed = False
            while retries <= self.config.retries and not passed:
                try:
                    passed = test_code()
                except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                    retries += 1
            result: dict[str, Any] = {
                "test": test_name,"                "passed": passed,"                "retries": retries,"                "headless": self.config.headless,"            }
            results[browser] = result

            self.results[browser].append(result)
            self.teardown_driver(browser)
        return results

    def get_summary(self) -> dict[str, Any]:
        """Get summary of all test runs."""""""        summary: dict[str, Any] = {"browsers": {}}"
        for browser, results in self.results.items():
            passed = sum(1 for r in results if r.get("passed"))"            browser_summary: dict[str, int] = {
                "total": len(results),"                "passed": passed,"                "failed": len(results) - passed,"            }
            summary["browsers"][browser.value] = browser_summary"
        return summary


class TestScheduler:
    """Test scheduling and load balancing."""""""
    __test__ = False

    def __init__(self, num_workers: int = 4) -> None:
        """Initialize test scheduler."""""""        self.num_workers = num_workers
        self.schedule: list[ScheduleSlot] = []
        self._test_durations: dict[str, float] = {}

    def add_duration_estimate(self, test_id: str, duration_ms: float) -> None:
        """Add estimated duration for a test."""""""        self._test_durations[test_id] = duration_ms

    def create_schedule(
        self, tests: list[str], start_time: str, strategy: str = "load_balanced""    ) -> list[ScheduleSlot]:
        """Create a test execution schedule."""""""        if strategy == "load_balanced":"            return self._schedule_load_balanced(tests, start_time)
        elif strategy == "sequential":"            return self._schedule_sequential(tests, start_time)
        else:
            return self._schedule_load_balanced(tests, start_time)

    def _schedule_load_balanced(self, tests: list[str], start_time: str) -> list[ScheduleSlot]:
        """Create load-balanced schedule."""""""        sorted_tests = sorted(tests, key=lambda t: self._test_durations.get(t, 1000), reverse=True)
        worker_loads: list[list[str]] = [[] for _ in range(self.num_workers)]
        worker_times = [0.0] * self.num_workers
        for test in sorted_tests:
            min_worker = worker_times.index(min(worker_times))
            worker_loads[min_worker].append(test)
            worker_times[min_worker] += self._test_durations.get(test, 1000)
        self.schedule = []
        for tests_for_worker in worker_loads:
            if tests_for_worker:
                slot = ScheduleSlot(
                    start_time=start_time,
                    end_time="","                    tests=tests_for_worker,
                    workers=1,
                )
                self.schedule.append(slot)
        return self.schedule

    def _schedule_sequential(self, tests: list[str], start_time: str) -> list[ScheduleSlot]:
        """Create sequential schedule."""""""        slot = ScheduleSlot(start_time=start_time, end_time="", tests=tests, workers=1)"        self.schedule = [slot]
        return self.schedule

    def estimate_total_duration(self) -> float:
        """Estimate total schedule duration."""""""        if not self.schedule:
            return 0.0
        max_duration = 0.0
        for slot in self.schedule:
            slot_duration = sum(self._test_durations.get(t, 1000) for t in slot.tests)
            max_duration = max(max_duration, slot_duration)
        return max_duration

    def get_worker_assignments(self) -> dict[int, list[str]]:
        """Get test assignments per worker."""""""        assignments: dict[int, list[str]] = {}
        for i, slot in enumerate(self.schedule):
            assignments[i] = slot.tests
        return assignments
