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

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from src.core.base.types.ConsistencyIssue import ConsistencyIssue
import re

__version__ = VERSION




class ConsistencyAgent:
    """Checks code consistency across the codebase.

    Identifies inconsistencies in naming, formatting, and patterns.

    Attributes:
        issues: List of consistency issues.

    Example:
        >>> checker=ConsistencyAgent()
        >>> issues=checker.check(["file1.py", "file2.py"], {})
    """

    def __init__(self) -> None:
        """Initialize the consistency checker."""
        self.issues: list[ConsistencyIssue] = []

    def check(self, file_contents: dict[str, str]) -> list[ConsistencyIssue]:
        """Check for consistency issues across files.

        Args:
            file_contents: Dictionary mapping file paths to contents.

        Returns:
            List of consistency issues.
        """
        self.issues = []
        # Check naming conventions
        self._check_naming_consistency(file_contents)
        # Check import styles
        self._check_import_consistency(file_contents)
        return self.issues

    def _check_naming_consistency(self, file_contents: dict[str, str]) -> None:
        """Check naming convention consistency.

        Args:
            file_contents: Dictionary mapping file paths to contents.
        """
        snake_case_files: list[str] = []
        camel_case_files: list[str] = []
        for path, content in file_contents.items():
            funcs = re.findall(r"def\s+([a-zA-Z_]\w*)", content)
            for func in funcs:
                if '_' in func and func[0].islower():
                    snake_case_files.append(f"{path}:{func}")
                elif func[0].isupper() or (func[0].islower() and any(c.isupper() for c in func)):
                    camel_case_files.append(f"{path}:{func}")
        if snake_case_files and camel_case_files:
            self.issues.append(ConsistencyIssue(
                issue_type="naming_convention",
                description="Mixed naming conventions detected",
                occurrences=snake_case_files[:3] + camel_case_files[:3],
                recommended_style="snake_case for functions (PEP 8)"
            ))

    def _check_import_consistency(self, file_contents: dict[str, str]) -> None:
        """Check import statement consistency.

        Args:
            file_contents: Dictionary mapping file paths to contents.
        """
        absolute_imports: list[str] = []
        relative_imports: list[str] = []
        for path, content in file_contents.items():
            if re.search(r"^from\s+\.", content, re.M):
                relative_imports.append(path)
            if re.search(r"^from\s+[a-zA-Z]", content, re.M):
                absolute_imports.append(path)
        if absolute_imports and relative_imports:
            self.issues.append(ConsistencyIssue(
                issue_type="import_style",
                description="Mixed import styles (absolute and relative)",
                occurrences=absolute_imports[:3] + relative_imports[:3],
                recommended_style="Prefer absolute imports (PEP 8)"
            ))
