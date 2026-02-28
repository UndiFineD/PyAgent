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


"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .test_baseline import TestBaseline

__version__ = VERSION


class BaselineManager:
    """Manages test baselines for comparison.

    Stores and compares baselines for regression testing.

    Example:
        manager=BaselineManager(baseline_dir)
        manager.save_baseline("perf", {"latency": 100, "data/memory": 50})

        # Later...
        baseline=manager.load_baseline("perf")
        diff=manager.compare("perf", {"latency": 120, "data/memory": 50})
    """

    def __init__(self, baseline_dir: Path) -> None:
        """Initialize manager.

        Args:
            baseline_dir: Directory for baseline files.
        """
        self.baseline_dir = baseline_dir
        self.baseline_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, name: str) -> Path:
        """Get path for baseline file."""
        return self.baseline_dir / f"{name}.baseline.json"

    def save_baseline(self, name: str, values: dict[str, Any]) -> TestBaseline:
        """Save a baseline.

        Args:
            name: Baseline name.
            values: Baseline values.

        Returns:
            Created baseline.
        """
        existing = self.load_baseline(name)
        version = existing.version + 1 if existing else 1

        baseline = TestBaseline(name=name, values=values, version=version)

        with open(self._get_path(name), "w", encoding='utf-8') as f:
            json.dump(
                {
                    "name": baseline.name,
                    "values": baseline.values,
                    "created_at": baseline.created_at,
                    "version": baseline.version,
                },
                f,
                indent=2,
            )

        return baseline

    def load_baseline(self, name: str) -> TestBaseline | None:
        """Load a baseline.

        Args:
            name: Baseline name.

        Returns:
            Loaded baseline or None.
        """
        path = self._get_path(name)
        if not path.exists():
            return None

        with open(path, encoding='utf-8') as f:
            data = json.load(f)

        return TestBaseline(
            name=data["name"],
            values=data["values"],
            created_at=data["created_at"],
            version=data["version"],
        )

    def compare(
        self,
        name: str,
        current: dict[str, Any],
        tolerance: float = 0.1,
    ) -> dict[str, Any]:
        """Compare current values against baseline.

        Args:
            name: Baseline name.
            current: Current values.
            tolerance: Tolerance for numeric comparisons (0.1=10%).

        Returns:
            Comparison results with diffs.
        """
        baseline = self.load_baseline(name)
        if not baseline:
            return {"error": "no baseline"}

        diffs = {}
        for key, current_val in current.items():
            if key not in baseline.values:
                diffs[key] = {"status": "new", "current": current_val}
                continue

            baseline_val = baseline.values[key]

            if isinstance(current_val, (int, float)) and isinstance(baseline_val, (int, float)):
                if baseline_val == 0:
                    pct_change = float("inf") if current_val != 0 else 0
                else:
                    pct_change = abs(current_val - baseline_val) / abs(baseline_val)

                if pct_change > tolerance:
                    diffs[key] = {
                        "status": "changed",
                        "baseline": baseline_val,
                        "current": current_val,
                        "pct_change": pct_change,
                    }
            elif current_val != baseline_val:
                diffs[key] = {
                    "status": "changed",
                    "baseline": baseline_val,
                    "current": current_val,
                }

        return {
            "baseline_version": baseline.version,
            "diffs": diffs,
            "passed": not diffs,  # type: ignore[arg-type]
        }
