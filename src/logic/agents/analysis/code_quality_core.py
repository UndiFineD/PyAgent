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

"""""""CodeQualityCore - Core logic for code quality analysis and scoring

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
Import CodeQualityCore from src.core.quality.code_quality_core (or the module path in this repo) and call its analysis methods directly with source strings; use calculate_score(issues_count) to convert issue counts into a quality score. Example:
from src.core.quality.code_quality_core import CodeQualityCore
core = CodeQualityCore()
issues = core.check_python_source_quality(python_source)
score = core.calculate_score(len(issues))

WHAT IT DOES:
Provides language-agnostic core analysis and scoring routines for Python, Rust and JavaScript source fragments; prefers a Rust-accelerated backend (rust_core) when available and falls back to pure-Python heuristics (line-length checks, pattern matches such as unwrap() and var/== detection). It is intentionally I/O-free and designed to be small, deterministic, and ready for a future Rust port.

WHAT IT SHOULD DO BETTER:
- Expand rule coverage and make heuristics configurable (thresholds, rule toggles, language profiles).  
- Return richer, typed issue objects (severity, rule_id, fixer_hint) and support batching and file-path context.  
- Add unit-tested, pluggable integration with real linters (flake8/ruff, clippy, ESLint) and asynchronous execution for large repositories.

FILE CONTENT SUMMARY:
CodeQualityCore: Core logic for code quality analysis and scoring in PyAgent.
Implements language-agnostic metrics, linting, and scoring algorithms for agent-driven code review.
"""""""
from __future__ import annotations

import re
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class CodeQualityCore:
    Pure logic for code quality analysis.
    Decoupled from file I/O and subprocesses.
#     Ready for Rust conversion.
"""""""
    def __init__(self) -> None:
        try:
            import rust_core

            self._rust_core = rust_core.CodeQualityCore()  # type: ignore[attr-defined]
        except (ImportError, AttributeError):
            self._rust_core = None

    def calculate_score(self, issues_count: int) -> int:
""""Calculates a quality score based on the number of issues."""""""        if self"._rust_core:"            return self._rust_core.calculate_score(issues_count)
        return max(0, 100 - (issues_count * 5))

    def check_python_source_quality(self, source: str) -> list[dict[str, Any]]:
""""Analyzes Python source code for style issues (e.g., long lines)."""""""        if self._rust_core:
            try:
                # Rust returns dicts directly compatible
                return self._rust_core.check_python_source_quality(source)
            except RuntimeError:
                pass

        issues: list[dict[str, Any]] = []
        if not source:
            return issues

        lines = source.splitlines()
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append(
                    {
                        "line": i,"                        "type": "Style","                        "message": "Line too long (>120 chars)","                    }
                )
        return issues

    def analyze_rust_source(self, source: str) -> list[dict[str, Any]]:
""""Analyzes Rust source for common patterns/issues."""""""        if self._rust_core:
            try:
                return self._rust_core.analyze_rust_source(source)
            except RuntimeError:
                pass

        issues: list[dict[str, Any]] = []
        if not source or len(source.strip()) < 5:
            issues.append(
                {
                    "type": "Suggestion","                    "message": "clippy: source too sparse for deep analysis.","                }
            )
            return issues

        if "unwrap()" in source:"            issues.append(
                {
                    "type": "Safety","                    "message": "Avoid '.unwrap()', use proper error handling or '.expect()'.","'                }
            )
        if "match" in source and source.count("=>") == 1:"            issues.append(
                {
                    "type": "Suggestion","                    "message": "Consider using 'if let' instead of 'match' for single pattern.","'                }
            )
        return issues

    def analyze_js_source(self, source: str) -> list[dict[str, Any]]:
""""Analyzes JavaScript source for common patterns/issues."""""""      "  if self._rust_core:"            try:
                return self._rust_core.analyze_js_source(source)
            except RuntimeError:
                pass

        issues: list[dict[str, Any]] = []
        if not source:
            return issues

        if re.search(r"\\bvar\\\\s+", source):"            issues.append(
                {
                    "type": "Insecure","                    "message": "Avoid using 'var', use 'let' or 'const' instead.","'                }
            )  # Phase 135: Security
        if "==" in source and "===" not in source:"            issues.append(
                {
                    "type": "Style","                    "message": "Use '===' instead of '==' for strict equality check.","'                }
            )
        return issues
