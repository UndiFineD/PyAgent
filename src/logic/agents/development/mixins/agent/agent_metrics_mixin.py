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

"""Code metrics and quality logic for CoderAgent."""

from __future__ import annotations
import logging
import re
import shutil
import subprocess
import sys
from src.core.base.common.types.code_metrics import CodeMetrics
from src.core.base.common.types.quality_score import QualityScore
from src.core.base.common.types.code_smell import CodeSmell

class AgentMetricsMixin:
    """Mixin for code metrics, quality scoring, and smell detection."""

    def calculate_metrics(self, content: str | None = None) -> CodeMetrics:
        """Calculate code metrics for the content."""
        if content is None:
            content = getattr(self, "current_content", "") or getattr(self, "previous_content", "") or ""
        self._metrics = self.core.calculate_metrics(content)
        return self._metrics

    def _get_test_coverage(self) -> float:
        """Attempt to calculate test coverage for the current file."""
        if not hasattr(self, "_is_python_file") or not self._is_python_file or not self.file_path.exists():
            return 0.0

        # Heuristic: Check common test locations
        test_file = self.file_path.parent / f"test_{self.file_path.name}"
        if not test_file.exists():
            # Try tests/test_filename.py
            test_file = (
                self.file_path.parent.parent / "tests" / f"test_{self.file_path.name}"
            )

        if not test_file.exists():
            return 0.0

        # If pytest is available, try to run it with coverage
        if shutil.which("pytest"):
            try:
                # Run coverage for just this file
                # Use --cov-fail-under=0 to avoid exit code 1 if coverage is low
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pytest",
                        "--cov=" + str(self.file_path),
                        "--cov-report=term-missing",
                        str(test_file),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                # Parse output for percentage (e.g., TOTAL 10 2 80%)
                match = re.search(r"TOTAL.*?\s+(\d+)%", result.stdout)

                # Phase 108: Record coverage intelligence
                if hasattr(self, "_record"):
                    self._record(
                        f"pytest --cov on {self.file_path.name}",
                        f"Coverage: {match.group(1)}%" if match else "No match",
                        provider="Shell",
                        model="pytest",
                    )

                if match:
                    return float(match.group(1))
            except Exception as e:
                logging.debug(f"Coverage calculation failed: {e}")

        return 0.0

    def calculate_quality_score(self, content: str | None = None) -> QualityScore:
        """Calculate an overall code quality score."""
        if content is None:
            content = getattr(self, "current_content", "") or getattr(self, "previous_content", "") or ""
        metrics = self.calculate_metrics(content)
        style_violations = self.check_style(content)
        code_smells = self.detect_code_smells(content)
        coverage = self._get_test_coverage()

        self._quality_score = self.core.calculate_quality_score(
            metrics, style_violations, code_smells, coverage
        )
        return self._quality_score

    def detect_code_smells(self, content: str | None = None) -> list[CodeSmell]:
        """Detect code smells in the content."""
        if content is None:
            content = getattr(self, "current_content", "") or getattr(self, "previous_content", "") or ""
        self._code_smells = self.core.detect_code_smells(content)
        return self._code_smells
