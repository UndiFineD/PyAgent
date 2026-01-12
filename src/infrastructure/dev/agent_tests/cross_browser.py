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



# -*- coding: utf-8 -*-

"""Cross-browser testing classes."""

from typing import Any, Callable, Dict, List

from src.infrastructure.dev.agent_tests.models import CrossBrowserConfig
from src.infrastructure.dev.agent_tests.enums import BrowserType


class CrossBrowserRunner:
    """Cross-browser testing configuration and execution.

    Manages cross-browser test execution with
    parallel capabilities.

    Attributes:
        config: Cross-browser configuration.
        results: Test results per browser.
    """

    def __init__(self, config: CrossBrowserConfig) -> None:
        """Initialize cross-browser runner.

        Args:
            config: The configuration to use.
        """
        self.config = config
        self.results: Dict[BrowserType, List[Dict[str, Any]]] = {
            b: [] for b in config.browsers
        }
        self._drivers: Dict[BrowserType, bool] = {}

    def setup_driver(self, browser: BrowserType) -> bool:
        """Setup browser driver.

        Args:
            browser: The browser type.

        Returns:
            True if setup successful.
        """
        # Simulated driver setup
        self._drivers[browser] = True
        return True

    def teardown_driver(self, browser: BrowserType) -> None:
        """Teardown browser driver.

        Args:
            browser: The browser type.
        """
        self._drivers[browser] = False

    def run_test(
        self,
        test_name: str,
        test_code: Callable[[], bool]
    ) -> Dict[BrowserType, Dict[str, Any]]:
        """Run a test across all browsers.

        Args:
            test_name: The test name.
            test_code: The test function.

        Returns:
            Results for each browser.
        """
        results: Dict[BrowserType, Dict[str, Any]] = {}
        for browser in self.config.browsers:
            self.setup_driver(browser)
            retries = 0
            passed = False
            while retries <= self.config.retries and not passed:
                try:
                    passed = test_code()
                except Exception:
                    retries += 1
            result: Dict[str, Any] = {
                "test": test_name,
                "passed": passed,
                "retries": retries,
                "headless": self.config.headless
            }
            results[browser] = result
            self.results[browser].append(result)
            self.teardown_driver(browser)
        return results

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all test runs.

        Returns:
            Summary statistics.
        """
        summary: Dict[str, Any] = {"browsers": {}}

        for browser, results in self.results.items():
            passed = sum(1 for r in results if r.get("passed"))
            browser_summary: Dict[str, int] = {
                "total": len(results),
                "passed": passed,
                "failed": len(results) - passed
            }
            summary["browsers"][browser.value] = browser_summary

        return summary
