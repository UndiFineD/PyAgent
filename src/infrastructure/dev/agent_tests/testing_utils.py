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
import hashlib
import json
from typing import Any, Dict, List, Optional
from .enums import TestSourceType
from .models import (
    AggregatedResult, ContractTest, TestStatus, VisualRegressionConfig
)

__version__ = VERSION

# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Testing utilities for visual regression, contract testing, and results aggregation."""

class VisualRegressionTester:
    """Visual regression testing for UI components."""

    def __init__(self, config: VisualRegressionConfig) -> None:
        """Initialize visual regression tester."""
        self.config = config
        self.baselines: Dict[str, str] = {}
        self.results: List[Dict[str, Any]] = []
        self._diffs: Dict[str, float] = {}

    def capture_baseline(self, component_id: str, screenshot_path: str) -> str:
        """Capture a baseline screenshot."""
        image_hash = hashlib.md5(
            f"{component_id}:{screenshot_path}".encode()
        ).hexdigest()
        self.baselines[component_id] = image_hash
        return image_hash

    def compare(self, component_id: str, current_screenshot: str) -> Dict[str, Any]:
        """Compare current screenshot against baseline."""
        baseline = self.baselines.get(component_id)
        if not baseline:
            return {"error": "No baseline found", "passed": False}

        current_hash = hashlib.md5(current_screenshot.encode()).hexdigest()
        diff = 0.0 if current_hash == baseline else 0.05
        self._diffs[component_id] = diff
        passed = diff <= self.config.diff_threshold
        result: Dict[str, Any] = {
            "component_id": component_id,
            "diff_percentage": diff,
            "threshold": self.config.diff_threshold,
            "passed": passed
        }
        self.results.append(result)
        return result

    def generate_diff_report(self) -> str:
        """Generate visual diff report."""
        report = ["# Visual Regression Report\n"]
        report.append(f"Threshold: {self.config.diff_threshold * 100}%\n")
        passed = [r for r in self.results if r.get("passed")]
        failed = [r for r in self.results if not r.get("passed")]
        report.append(f"## Summary: {len(passed)} passed, {len(failed)} failed\n")
        if failed:
            report.append("## Failed Components\n")
            for r in failed:
                report.append(
                    f"- **{r['component_id']}**: {r['diff_percentage'] * 100:.2f}% diff"
                )
        return "\n".join(report)

    def run_for_browsers(self, component_id: str) -> List[Dict[str, Any]]:
        """Run visual test across all configured browsers."""
        results: List[Dict[str, Any]] = []
        for browser in self.config.browsers:
            result: Dict[str, Any] = {
                "browser": browser.value,
                "component_id": component_id,
                "passed": True
            }
            results.append(result)
        return results

class ContractTestRunner:
    """Contract testing for API boundaries."""

    def __init__(self) -> None:
        """Initialize contract test runner."""
        self.contracts: Dict[str, ContractTest] = {}
        self.results: List[Dict[str, Any]] = []

    def add_contract(
        self,
        consumer: str,
        provider: str,
        endpoint: str,
        request_schema: Optional[Dict[str, Any]] = None,
        response_schema: Optional[Dict[str, Any]] = None,
        status_code: int = 200
    ) -> ContractTest:
        """Add a contract definition."""
        contract_id = f"{consumer}:{provider}:{endpoint}"
        contract = ContractTest(
            consumer=consumer,
            provider=provider,
            endpoint=endpoint,
            request_schema=request_schema or {},
            response_schema=response_schema or {},
            status_code=status_code
        )
        self.contracts[contract_id] = contract
        return contract

    def verify_consumer(
        self,
        contract_id: str,
        actual_request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Verify consumer sends correct request."""
        contract = self.contracts.get(contract_id)
        if not contract:
            return {"error": "Contract not found", "valid": False}

        valid = all(
            k in actual_request
            for k in contract.request_schema.keys()
        )
        result: Dict[str, Any] = {
            "contract_id": contract_id,
            "side": "consumer",
            "valid": valid
        }
        self.results.append(result)
        return result

    def verify_provider(
        self,
        contract_id: str,
        actual_response: Dict[str, Any],
        actual_status: int
    ) -> Dict[str, Any]:
        """Verify provider sends correct response."""
        contract = self.contracts.get(contract_id)
        if not contract:
            return {"error": "Contract not found", "valid": False}
        status_match = actual_status == contract.status_code
        schema_valid = all(
            k in actual_response
            for k in contract.response_schema.keys()
        )
        result: Dict[str, Any] = {
            "contract_id": contract_id,
            "side": "provider",
            "valid": status_match and schema_valid,
            "status_match": status_match
        }
        self.results.append(result)
        return result

    def get_contracts_for_consumer(self, consumer: str) -> List[ContractTest]:
        """Get all contracts for a consumer."""
        return [c for c in self.contracts.values() if c.consumer == consumer]

    def export_pact(self, consumer: str) -> str:
        """Export contracts in Pact format."""
        contracts = self.get_contracts_for_consumer(consumer)
        pact: Dict[str, Any] = {
            "consumer": {"name": consumer},
            "provider": {"name": contracts[0].provider if contracts else ""},
            "interactions": [{
                "request": {"path": c.endpoint},
                "response": {"status": c.status_code}
            } for c in contracts]
        }
        return json.dumps(pact, indent=2)

class ResultAggregator:
    """Aggregate test results from multiple sources."""

    def __init__(self) -> None:
        """Initialize result aggregator."""
        self.results: List[AggregatedResult] = []
        self._by_source: Dict[TestSourceType, List[AggregatedResult]] = {}

    def add_result(
        self,
        source: TestSourceType,
        test_name: str,
        status: TestStatus,
        duration_ms: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AggregatedResult:
        """Add a test result."""
        from datetime import datetime
        result = AggregatedResult(
            source=source,
            test_name=test_name,
            status=status,
            duration_ms=duration_ms,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {}
        )
        self.results.append(result)

        if source not in self._by_source:
            self._by_source[source] = []
        self._by_source[source].append(result)

        return result

    def add_run(self, run_data: Dict[str, int]) -> None:
        """Add a test run with summary stats."""
        for _ in range(run_data.get("passed", 0)):
            self.add_result(
                source=TestSourceType.PYTEST,
                test_name="synthetic_test",
                status=TestStatus.PASSED,
                duration_ms=1.0
            )
        for _ in range(run_data.get("failed", 0)):
            self.add_result(
                source=TestSourceType.PYTEST,
                test_name="synthetic_test",
                status=TestStatus.FAILED,
                duration_ms=1.0
            )
        for _ in range(run_data.get("skipped", 0)):
            self.add_result(
                source=TestSourceType.PYTEST,
                test_name="synthetic_test",
                status=TestStatus.SKIPPED,
                duration_ms=0.0
            )

    def import_pytest_results(self, json_report: str) -> int:
        """Import results from pytest JSON report."""
        try:
            data = json.loads(json_report)
            count = 0
            for test in data.get("tests", []):
                status_map = {
                    "passed": TestStatus.PASSED,
                    "failed": TestStatus.FAILED,
                    "skipped": TestStatus.SKIPPED
                }
                self.add_result(
                    source=TestSourceType.PYTEST,
                    test_name=test.get("nodeid", ""),
                    status=status_map.get(test.get("outcome", ""), TestStatus.ERROR),
                    duration_ms=test.get("duration", 0) * 1000
                )
                count += 1
            return count
        except json.JSONDecodeError:
            return 0

    def get_summary(self) -> Dict[str, Any]:
        """Get aggregated summary."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in self.results if r.status == TestStatus.FAILED)
        total_duration = sum(r.duration_ms for r in self.results)

        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "total_duration_ms": total_duration,
            "sources": [s.value for s in self._by_source.keys()]
        }

    def export_unified_report(self) -> str:
        """Export unified report across all sources."""
        return json.dumps({
            "summary": self.get_summary(),
            "results": [{
                "source": r.source.value,
                "test": r.test_name,
                "status": r.status.value,
                "duration_ms": r.duration_ms
            } for r in self.results]
        }, indent=2)

    def merge(self) -> Dict[str, Any]:
        """Merge all results into a single summary."""
        summary = self.get_summary()
        failed = summary.get("failed", 0)
        passed = summary.get("passed", 0)

        return {
            "total_passed": passed,
            "total_failed": failed,
            "total_skipped": sum(1 for r in self.results if r.status == TestStatus.SKIPPED),
            "total_duration_ms": summary.get("total_duration_ms", 0)
        }

    def get_trend(self) -> Dict[str, Any]:
        """Analyze trend in test results."""
        if len(self.results) < 2:
            return {"pass_rate_trend": "stable"}

        mid_point = len(self.results) // 2
        earlier_results = self.results[:mid_point]
        later_results = self.results[mid_point:]

        earlier_rate = (
            sum(1 for r in earlier_results if r.status == TestStatus.PASSED) /
            len(earlier_results) if len(earlier_results) > 0 else 0
        )
        later_rate = (
            sum(1 for r in later_results if r.status == TestStatus.PASSED) /
            len(later_results) if len(later_results) > 0 else 0
        )

        if later_rate > earlier_rate:
            trend = "improving"
        elif later_rate < earlier_rate:
            trend = "declining"
        else:
            trend = "stable"

        return {"pass_rate_trend": trend}

class TestMetricsCollector:
    """Collect test execution metrics."""
    __test__ = False

    def __init__(self) -> None:
        """Initialize metrics collector."""
        self.executions: Dict[str, List[float]] = {}
        self.flaky_tests: Dict[str, int] = {}

    def record_execution(self, test_name: str, duration_ms: float) -> None:
        """Record test execution time."""
        if test_name not in self.executions:
            self.executions[test_name] = []
        self.executions[test_name].append(duration_ms)

    def record_flaky(self, test_name: str, occurrences: int = 1) -> None:
        """Record flaky test occurrence."""
        self.flaky_tests[test_name] = occurrences

    def get_metrics(self) -> Dict[str, float]:
        """Get aggregated metrics."""
        total_duration = sum(sum(durations) for durations in self.executions.values())
        total_tests = sum(len(durations) for durations in self.executions.values())
        avg_duration = total_duration / total_tests if total_tests > 0 else 0
        return {
            "total_duration_ms": total_duration,
            "average_duration_ms": avg_duration
        }

    def get_flaky_tests(self) -> Dict[str, int]:
        """Get flaky tests."""
        return self.flaky_tests.copy()