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

from __future__ import annotations
from src.core.base.version import VERSION
from typing import Dict, List, Any

__version__ = VERSION

class CodeQualityCore:
    """
    Pure logic for code quality analysis.
    Decoupled from file I/O and subprocesses.
    """

    @staticmethod
    def calculate_score(issues_count: int) -> int:
        """Calculates a quality score based on the number of issues."""
        return max(0, 100 - (issues_count * 5))

    @staticmethod
    def check_python_source_quality(source: str) -> list[dict[str, Any]]:
        """Analyzes Python source code for style issues (e.g., long lines)."""
        issues = []
        lines = source.splitlines()
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append({
                    "line": i, 
                    "type": "Style", 
                    "message": "Line too long (>120 chars)"
                })
        return issues

    @staticmethod
    def analyze_rust_source(source: str) -> list[dict[str, Any]]:
        """Analyzes Rust source for common patterns/issues."""
        issues = []
        if not source or len(source.strip()) < 5:
            issues.append({"type": "Suggestion", "message": "clippy: source too sparse for deep analysis."})
        if "unwrap()" in source:
            issues.append({"type": "Safety", "message": "Avoid '.unwrap()', use proper error handling or '.expect()'."})
        if "match" in source and source.count("=>") == 1:
            issues.append({"type": "Suggestion", "message": "Consider using 'if let' instead of 'match' for single pattern."})
        return issues

    @staticmethod
    def analyze_js_source(source: str) -> list[dict[str, Any]]:
        """Analyzes JavaScript source for common patterns/issues."""
        issues = []
        import re
        if re.search(r"\bvar\s+", source):
            issues.append({"type": "Insecure", "message": "Avoid using 'var', use 'let' or 'const' instead."})
        if "==" in source and "===" not in source:
            issues.append({"type": "Style", "message": "Use '===' instead of '==' for strict equality check."})
        return issues