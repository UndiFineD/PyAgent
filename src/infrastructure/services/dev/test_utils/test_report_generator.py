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

"""Auto-extracted class from agent_test_utils.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class TestReportGenerator:
    """Generates test reports in various formats."""

    __test__ = False

    def __init__(self, output_dir: str | Path | None = None) -> None:
        """Initialize report generator."""
        self.output_dir = Path(output_dir) if output_dir is not None else None
        if self.output_dir is not None:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results: list[dict[str, Any]] = []

    def add_result(self, test_name: str, passed: bool, duration_ms: float) -> None:
        """Add test result (legacy API)."""
        self.results.append(
            {
                "test_name": test_name,
                "status": "passed" if passed else "failed",
                "duration_ms": float(duration_ms),
            }
        )

    def add_test_result(self, test_name: str, status: str, duration_ms: float, error: str = "") -> None:
        """Add test result (test compatibility API)."""
        self.results.append(
            {
                "test_name": test_name,
                "status": status,
                "duration_ms": float(duration_ms),
                "error": error,
            }
        )

    def _render_html(self) -> str:
        rows = ""
        for r in self.results:
            status = str(r.get("status", ""))
            duration = float(r.get("duration_ms", 0.0))
            error = str(r.get("error", ""))
            rows += (
                f"<tr><td>{r.get('test_name', '')}</td><td>{status}</td><td>{duration:.2f}ms</td><td>{error}</td></tr>"
            )
        return (
            "<html><head><title>Test Report</title></head><body>"
            "<h1>Test Results</h1>"
            '<table border="1">'
            "<tr><th>Test</th><th>Status</th><th>Duration</th><th>Error</th></tr>"
            f"{rows}</table></body></html>"
        )

    def generate_html(self) -> Path:
        """Generate HTML report file."""
        if self.output_dir is None:
            self.output_dir = Path.cwd()
        path = self.output_dir / "test_report.html"
        path.write_text(self._render_html(), encoding="utf-8")
        return path

    def generate_json(self) -> Path:
        """Generate JSON report file."""
        if self.output_dir is None:
            self.output_dir = Path.cwd()
        path = self.output_dir / "test_report.json"
        payload = {"results": self.results}
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path
