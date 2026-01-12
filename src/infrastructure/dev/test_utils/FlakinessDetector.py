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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_test_utils.py"""




from .FlakinessReport import FlakinessReport

from typing import Callable, Dict, List, Optional

class FlakinessDetector:
    """Detects flaky tests through repeated execution.

    Runs tests multiple times to identify intermittent failures.

    Example:
        detector=FlakinessDetector()
        report=detector.analyze(test_fn, runs=10)
        if report.flakiness_score > 0.1:
            print(f"Test is flaky: {report.flakiness_score}")
    """

    def __init__(self, default_runs: int = 5) -> None:
        """Initialize detector.

        Args:
            default_runs: Default number of test runs.
        """
        self.default_runs = default_runs
        self._history: Dict[str, List[FlakinessReport]] = {}

    def analyze(
        self,
        test_fn: Callable[[], None],
        runs: Optional[int] = None,
        test_name: Optional[str] = None,
    ) -> FlakinessReport:
        """Analyze test for flakiness.

        Args:
            test_fn: Test function to analyze.
            runs: Number of runs.
            test_name: Test name for reporting.

        Returns:
            FlakinessReport with analysis results.
        """
        runs = runs or self.default_runs
        test_name = test_name or test_fn.__name__

        passes = 0
        failures = 0
        failure_messages: List[str] = []

        for _ in range(runs):
            try:
                test_fn()
                passes += 1
            except Exception as e:
                failures += 1
                msg = str(e)
                if msg not in failure_messages:
                    failure_messages.append(msg)

        # Calculate flakiness score
        # 0=all same result, 1=50 / 50 split
        if runs > 0:
            p = passes / runs
            flakiness = 1 - abs(2 * p - 1)  # 0 at 0% or 100%, 1 at 50%
        else:
            flakiness = 0.0

        report = FlakinessReport(
            test_name=test_name,
            runs=runs,
            passes=passes,
            failures=failures,
            flakiness_score=flakiness,
            failure_messages=failure_messages,
        )

        # Store in history
        if test_name not in self._history:
            self._history[test_name] = []
        self._history[test_name].append(report)

        return report

    def get_history(self, test_name: str) -> List[FlakinessReport]:
        """Get flakiness history for a test."""
        return self._history.get(test_name, [])

    def get_flaky_tests(self, threshold: float = 0.1) -> List[str]:
        """Get tests that exceed flakiness threshold."""
        flaky: List[str] = []
        for name, reports in self._history.items():
            if reports and reports[-1].flakiness_score > threshold:
                flaky.append(name)
        return flaky
