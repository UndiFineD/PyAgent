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


"""Test optimization and coverage analysis."""

from __future__ import annotations

from typing import Any

from src.core.base.lifecycle.version import VERSION

from .models import TestCase

__version__ = VERSION


class TestSuiteOptimizer:
    """Optimize test suites by removing redundant tests."""

    __test__ = False

    def __init__(self) -> None:
        """Initialize test suite optimizer."""
        self.tests: list[TestCase] = []
        self.coverage_map: dict[str, set[str]] = {}

    def add_test(self, test_id: str, covers: set[str]) -> None:
        """Add a test with its coverage."""
        self.coverage_map[test_id] = covers

    def load_tests(self, tests: list[TestCase]) -> None:
        """Load tests for optimization."""
        self.tests = tests

    def add_coverage(self, test_id: str, covered_lines: set[str]) -> None:
        """Add coverage data for a test."""
        self.coverage_map[test_id] = covered_lines

    def find_redundant_tests(self) -> list[str]:
        """Find tests whose coverage is fully covered by other tests."""
        redundant: list[str] = []
        for test_id, coverage in self.coverage_map.items():
            other_coverage: set[str] = set()
            for other_id, other_cov in self.coverage_map.items():
                if other_id != test_id:
                    other_coverage |= other_cov
            if coverage <= other_coverage:
                redundant.append(test_id)
        return redundant

    def find_overlapping_tests(self) -> list[tuple[str, str, float]]:
        """Find tests with significant overlap."""
        overlaps: list[tuple[str, str, float]] = []
        test_ids = list(self.coverage_map.keys())
        for i, id_a in enumerate(test_ids):
            for id_b in test_ids[i + 1 :]:
                cov_a = self.coverage_map[id_a]
                cov_b = self.coverage_map[id_b]
                if not cov_a or not cov_b:
                    continue
                intersection = cov_a & cov_b
                overlap = len(intersection) / min(len(cov_a), len(cov_b))
                if overlap > 0.8:
                    overlaps.append((id_a, id_b, overlap))
        return overlaps

    def suggest_removals(self) -> list[dict[str, Any]]:
        """Suggest tests that could be removed."""
        suggestions: list[dict[str, Any]] = []
        for test_id in self.find_redundant_tests():
            suggestions.append({"test_id": test_id, "reason": "fully_redundant", "confidence": 0.9})
        for id_a, id_b, overlap in self.find_overlapping_tests():
            cov_a = len(self.coverage_map.get(id_a, set()))
            cov_b = len(self.coverage_map.get(id_b, set()))
            remove = id_a if cov_a < cov_b else id_b
            suggestions.append(
                {
                    "test_id": remove,
                    "reason": f"overlaps {overlap * 100:.0f}% with {id_a if remove == id_b else id_b}",
                    "confidence": 0.7,
                }
            )
        return suggestions

    def get_coverage(self, test_id: str) -> set[str]:
        """Get the coverage set for a given test."""
        return set(self.coverage_map.get(test_id, set()))

    def optimize(self) -> list[str]:
        """Return a minimized set of tests while preserving overall coverage."""

        if not self.coverage_map:
            return []

        all_coverage: set[str] = set()

        for cov in self.coverage_map.values():
            all_coverage |= set(cov)

        redundant = set(self.find_redundant_tests())
        kept = [test_id for test_id in self.coverage_map.keys() if test_id not in redundant]

        kept_coverage: set[str] = set()
        for test_id in kept:
            kept_coverage |= self.get_coverage(test_id)

        if kept_coverage != all_coverage:
            return list(self.coverage_map.keys())

        return kept


class CoverageGapAnalyzer:
    """Analyzes coverage gaps."""

    def __init__(self) -> None:
        """Initialize analyzer."""
        self._covered_lines: dict[str, set[int]] = {}
        self._total_lines: dict[str, int] = {}

    def add_coverage_data(self, file_path: str, covered_lines: set[int]) -> None:
        """Record covered lines for a file."""
        self._covered_lines[file_path] = set(covered_lines)

    def set_total_lines(self, file_path: str, total_lines: int) -> None:
        """Set the total executable lines for a file."""
        self._total_lines[file_path] = int(total_lines)

    def find_gaps(self, file_path: str) -> set[int]:
        """Find uncovered line numbers for a file."""
        total = self._total_lines.get(file_path, 0)
        covered = self._covered_lines.get(file_path, set())
        if total <= 0:
            return set()
        all_lines = set(range(1, total + 1))
        return all_lines - covered

    def get_coverage_percentage(self, file_path: str) -> float:
        """Get coverage percentage for a file."""
        total = self._total_lines.get(file_path, 0)
        if total <= 0:
            return 0.0
        covered = self._covered_lines.get(file_path, set())
        return (len(covered) / total) * 100

    def add_covered(self, item: str) -> None:
        """Mark item as covered."""
        self._covered_lines.setdefault("__legacy__", set()).add(hash(item) & 0x7FFFFFFF)

    def add_uncovered(self, item: str) -> None:
        """Mark item as uncovered."""
        self._covered_lines.setdefault("__legacy_total__", set()).add(hash(item) & 0x7FFFFFFF)

    def get_coverage_percentage_legacy(self) -> float:
        """Get coverage percentage (legacy aggregate)."""
        total = len(self._covered_lines.get("__legacy_total__", set()))
        covered = len(self._covered_lines.get("__legacy__", set()))
        if total <= 0:
            return 0.0
        return (covered / total) * 100

    def find_uncovered(self) -> list[str]:
        """Find uncovered items."""
        return []
