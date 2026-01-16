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

"""Test management and baseline utilities."""

from __future__ import annotations
from src.core.base.Version import VERSION
from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import Any, cast
from collections.abc import Callable
from .models import TestCase

__version__ = VERSION


def _empty_str_list() -> list[str]:
    return []


class BaselineComparisonResult:
    """Result of a baseline comparison."""

    def __init__(self, matches: bool, differences: list[str] | None = None) -> None:
        self.matches = matches
        self.differences = differences or []


class BaselineManager:
    """Manage test baselines."""

    def __init__(self, baseline_dir: Path | None = None) -> None:
        """Initialize baseline manager."""
        self.baseline_dir = Path(baseline_dir) if baseline_dir else Path("./baselines")

        self.baseline_dir.mkdir(parents=True, exist_ok=True)

    def save_baseline(self, name: str, data: dict[str, Any]) -> None:
        """Save a baseline."""
        baseline_path = self.baseline_dir / f"{name}.json"
        with open(baseline_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_baseline(self, name: str) -> dict[str, Any]:
        """Load a baseline."""
        baseline_path = self.baseline_dir / f"{name}.json"
        if baseline_path.exists():
            with open(baseline_path, encoding="utf-8") as f:
                return json.load(f)
        return {}

    def compare(self, name: str, current: dict[str, Any]) -> BaselineComparisonResult:
        """Compare current data to baseline."""
        baseline = self.load_baseline(name)
        if baseline == current:
            return BaselineComparisonResult(matches=True, differences=[])

        differences = []
        for key in set(baseline.keys()) | set(current.keys()):
            if key not in baseline:
                differences.append(f"Key '{key}' added")
            elif key not in current:
                differences.append(f"Key '{key}' removed")
            elif baseline[key] != current[key]:
                differences.append(
                    f"Value mismatch for key '{key}': {baseline[key]} != {current[key]}"
                )

        return BaselineComparisonResult(matches=False, differences=differences)

    def update_baseline(self, name: str, data: dict[str, Any]) -> None:
        """Update a baseline."""
        self.save_baseline(name, data)


class DIContainer:
    """Dependency injection container."""

    def __init__(self) -> None:
        """Initialize DI container."""
        self._dependencies: dict[str, Any] = {}
        self._overrides: dict[str, Any] = {}

    def register(self, name: str, factory: Callable[[], Any]) -> None:
        """Register a dependency."""
        self._dependencies[name] = factory

    def has(self, name: str) -> bool:
        """Check if dependency is registered."""
        return name in self._dependencies

    def resolve(self, name: str) -> Any:
        """Resolve a dependency."""
        if name in self._overrides:
            return self._overrides[name]()

        if name not in self._dependencies:
            raise ValueError(f"Dependency not registered: {name}")

        return self._dependencies[name]()

    def override(self, name: str, factory: Callable[[], Any]) -> Any:
        """Context manager for dependency override."""
        from contextlib import contextmanager

        @contextmanager
        def override_context() -> bool:
            old_override = self._overrides.get(name)
            self._overrides[name] = factory
            try:
                yield
            finally:
                if old_override:
                    self._overrides[name] = old_override
                else:
                    self._overrides.pop(name, None)

        return override_context()


class TestPrioritizer:
    """Prioritizes tests based on various factors."""

    __test__ = False

    def __init__(self) -> None:
        """Initialize test prioritizer."""
        self.tests: dict[str, dict[str, Any]] = {}

    def add_test(
        self,
        name: str,
        recent_changes: int = 0,
        failure_rate: float = 0.0,
        changed_recently: bool | None = None,
    ) -> None:
        """Add a test for prioritization.

        Compatibility:
            Supports both ``recent_changes`` and boolean ``changed_recently``.
        """
        if changed_recently is not None and recent_changes == 0:
            recent_changes = 1 if changed_recently else 0
        self.tests[name] = {
            "recent_changes": int(recent_changes),
            "failure_rate": float(failure_rate),
        }

    def prioritize_by_changes(self) -> list[str]:
        """Prioritize by recent changes (compat alias)."""
        return self.prioritize_by_recent_changes()

    def prioritize_by_recent_changes(self) -> list[str]:
        """Prioritize by recent changes."""
        return sorted(
            self.tests.keys(),
            key=lambda t: self.tests[t]["recent_changes"],
            reverse=True,
        )

    def prioritize_by_failure_history(self) -> list[str]:
        """Prioritize by failure history."""
        return sorted(
            self.tests.keys(), key=lambda t: self.tests[t]["failure_rate"], reverse=True
        )

    def prioritize_by_failure_rate(self) -> list[str]:
        """Prioritize by failure rate (compat alias)."""
        return self.prioritize_by_failure_history()

    def prioritize_combined(
        self,
        change_weight: float = 1.0,
        failure_weight: float = 1.0,
    ) -> list[str]:
        """Prioritize with combined strategy."""
        scores: dict[str, float] = {}

        for test, data in self.tests.items():
            scores[test] = (data["recent_changes"] * float(change_weight)) + (
                data["failure_rate"] * float(failure_weight)
            )

        return sorted(scores.keys(), key=lambda t: scores[t], reverse=True)

    def prioritize(self, tests: list[TestCase]) -> list[TestCase]:
        """Rank tests by priority."""
        return sorted(tests, key=lambda t: t.priority.value, reverse=True)


class FlakinessDetector:
    """Detects flaky tests."""

    def __init__(self) -> None:
        """Initialize flakiness detector."""
        self.test_runs: dict[str, list[bool]] = {}

    def add_run(self, test_name: str, passed: bool) -> None:
        """Add a test run result."""
        if test_name not in self.test_runs:
            self.test_runs[test_name] = []
        self.test_runs[test_name].append(passed)

    def record_result(self, test_name: str, passed: bool) -> None:
        """Record a test run result (compat alias)."""
        self.add_run(test_name, passed)

    def is_flaky(self, test_name: str) -> bool:
        """Detect if test is flaky."""

        if test_name not in self.test_runs or len(self.test_runs[test_name]) < 2:
            return False
        results = self.test_runs[test_name]
        passes = sum(results)

        fails = len(results) - passes
        return passes > 0 and fails > 0


class QuarantineManager:
    """Manages quarantined flaky tests."""

    def __init__(self) -> None:
        """Initialize quarantine manager."""
        self.quarantined: set[str] = set()

        self.reasons: dict[str, str] = {}

    def quarantine(self, test_name: str, reason: str = "") -> None:
        """Quarantine a test."""
        self.quarantined.add(test_name)
        if reason:
            self.reasons[test_name] = reason

    def release(self, test_name: str) -> None:
        """Release a quarantined test."""
        self.quarantined.discard(test_name)
        self.reasons.pop(test_name, None)

    def is_quarantined(self, test_name: str) -> bool:
        """Check if test is quarantined."""
        return test_name in self.quarantined


class ImpactAnalyzer:
    """Analyzes impact of code changes on tests."""

    def __init__(self) -> None:
        """Initialize impact analyzer."""
        self._test_to_files: dict[str, set[str]] = {}
        self._file_dependencies: dict[str, set[str]] = {}

    def map_test_to_files(self, test: str, files: list[str]) -> None:
        """Map a test to the files it exercises."""
        self._test_to_files[test] = set(files)

    def add_dependency(self, file: str, depends_on: str) -> None:
        """Declare a file dependency edge: ``file`` depends on ``depends_on``."""
        self._file_dependencies.setdefault(file, set()).add(depends_on)

    def _expand_changed_files(self, changed_files: list[str]) -> set[str]:
        expanded: set[str] = set(changed_files)
        stack: list[str] = list(changed_files)
        while stack:
            current = stack.pop()
            for dep in self._file_dependencies.get(current, set()):
                if dep not in expanded:
                    expanded.add(dep)
                    stack.append(dep)
        return expanded

    def get_affected_tests(
        self, changed_files: list[str], include_dependencies: bool = False
    ) -> set[str]:
        """Get tests affected by changes in one or more files."""
        files = (
            self._expand_changed_files(changed_files)
            if include_dependencies
            else set(changed_files)
        )
        affected: set[str] = set()
        for test, mapped in self._test_to_files.items():
            if mapped & files:
                affected.add(test)
        return affected

    def build_dependency_graph(self) -> dict[str, set[str]]:
        """Build dependency graph (compat)."""
        return {k: set(v) for k, v in self._file_dependencies.items()}

    def get_impacted_tests(self, changed_files: list[str]) -> set[str]:
        """Get impacted tests (compat alias)."""
        return self.get_affected_tests(
            changed_files=changed_files, include_dependencies=False
        )


class ContractValidator:
    """Validates API contracts."""

    @dataclass
    class ValidationResult:
        """Result of a contract validation."""

        valid: bool
        errors: list[str] = field(default_factory=list)

    def validate(
        self,
        contract: dict[str, Any],
        actual_response: dict[str, Any] | None = None,
    ) -> ContractValidator.ValidationResult:
        """Validate a contract against an actual response."""
        errors: list[str] = []

        expected_resp_raw = contract.get("response")
        expected_resp: dict[str, Any] = (
            cast(dict[str, Any], expected_resp_raw)
            if isinstance(expected_resp_raw, dict)
            else {}
        )
        expected_status = expected_resp.get("status")
        if expected_status is None:
            errors.append("missing_expected_status")
        if actual_response is None:
            errors.append("missing_actual_response")
            return ContractValidator.ValidationResult(valid=False, errors=errors)

        actual_status = actual_response.get("status")
        if expected_status is not None and actual_status != expected_status:
            errors.append("status_mismatch")

        expected_body_raw = expected_resp.get("body")
        expected_body: dict[str, Any] = (
            cast(dict[str, Any], expected_body_raw)
            if isinstance(expected_body_raw, dict)
            else {}
        )
        expected_type = expected_body.get("type")
        if expected_type == "array":
            if not isinstance(actual_response.get("body"), list):
                errors.append("body_type_mismatch")

        return ContractValidator.ValidationResult(
            valid=(len(errors) == 0), errors=errors
        )


class TestDocGenerator:
    """Generates documentation from tests."""

    __test__ = False

    def __init__(self) -> None:
        """Initialize doc generator."""
        self.tests: list[dict[str, Any]] = []

    def add_test(
        self, name: str, module: str = "unknown", docstring: str = "", code: str = ""
    ) -> None:
        """Add test for documentation."""
        self.tests.append(
            {"name": name, "module": module, "docstring": docstring, "code": code}
        )

    def generate(self) -> str:
        """Generate a human-readable documentation summary."""
        parts: list[str] = []
        for test in self.tests:
            title = test.get("name", "")
            doc = test.get("docstring", "")
            code = test.get("code", "")
            parts.append(f"{title}: {doc}\n{code}".strip())
        return "\n\n".join(parts)

    def generate_grouped(self) -> dict[str, list[dict[str, Any]]]:
        """Generate documentation grouped by module."""
        return self.group_by_module(self.tests)

    def extract_examples(self, test_code: str) -> list[dict[str, str]]:
        """Extract examples from test code."""
        return [{"example": test_code}] if test_code else []

    def group_by_module(
        self, tests: list[dict[str, Any]]
    ) -> dict[str, list[dict[str, Any]]]:
        """Group tests by module."""
        result: dict[str, list[dict[str, Any]]] = {}
        for test in tests:
            module = test.get("module", "unknown")
            if module not in result:
                result[module] = []
            result[module].append(test)
        return result
