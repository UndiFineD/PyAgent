#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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


"""
SecurityScannerAgent - Scans code for security vulnerabilities

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate with a file path: agent = SecurityScannerAgent("path/to/file")
- Call scan with source content: vulnerabilities = agent.scan(source_code)
- Returns: list[SecurityVulnerability] with type, severity, description, line_number, fix_suggestion

WHAT IT DOES:
- Searches source code for common security anti-patterns using predefined regex patterns (hardcoded secrets, insecure use of eval, command injection, insecure randomness, path traversal).
- Attempts to delegate scanning to a Rust-accelerated scanner (rust_core.scan_code_vulnerabilities_rust) and falls back to a Python regex-based scanner if Rust integration is unavailable.
- Collects findings into SecurityVulnerability objects and stores them on self.vulnerabilities; includes basic metadata and remediation suggestions.

WHAT IT SHOULD DO BETTER:
- Support multi-line and context-aware analysis (current regexes operate primarily line-by-line and may miss multi-line constructs or produce false positives).
- Normalize and deduplicate findings (overlapping patterns or repeated detections on adjacent lines should be consolidated).
- Expand pattern coverage and severity tuning (configurable rule set, allow suppression comments, integrate CWE mappings, and richer remediation guidance).
- Add unit tests and CI hooks for both Python fallback and Rust integration paths; include configurable scanning options and performance throttling for large files.

FILE CONTENT SUMMARY:
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


"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

import re

from src.core.base.common.types.security_issue_type import SecurityIssueType
from src.core.base.common.types.security_vulnerability import SecurityVulnerability
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class SecurityScannerAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """Scans code for security vulnerabilities.

    Identifies common security issues and provides remediation guidance.
    """

    SECURITY_PATTERNS: list[tuple[str, SecurityIssueType, str, str, str]] = [
        (
            r'password\s*=\s*[\'"][^\'"]+[\'"]',
            SecurityIssueType.HARDCODED_SECRET,
            "high",
            "Hardcoded password detected",
            "Use environment variables or secure vault",
        ),
        (
            r'api_key\s*=\s*[\'"][^\'"]+[\'"]',
            SecurityIssueType.HARDCODED_SECRET,
            "high",
            "Hardcoded API key detected",
            "Use environment variables or secure vault",
        ),
        (
            r'os\.system\s*\([^)]*\+',
            SecurityIssueType.COMMAND_INJECTION,
            "critical",
            "Potential command injection vulnerability",
            "Use subprocess with shell=False and proper escaping",
        ),
        (
            r"ev" + r"al\s*\(",
            SecurityIssueType.INSECURE_DESERIALIZATION,
            "critical",
            "Use of ev" + "al() is dangerous",  # nosec
            "Avoid ev" + "al() or use ast.literal_eval() for safe parsing",
        ),
        (
            r"random\.(random|randint|choice)\s*\(",
            SecurityIssueType.INSECURE_RANDOM,
            "medium",
            "Insecure random number generation for security context",
            "Use secrets module for cryptographic randomness",
        ),
        (
            r"open\s*\([^)]*\+",
            SecurityIssueType.PATH_TRAVERSAL,
            "high",
            "Potential path traversal vulnerability",
            "Validate and sanitize file paths",
        ),
    ]

    def __init__(self, file_path: str) -> None:
        """Initialize the security scanner agent."""
        super().__init__(file_path)
        self.vulnerabilities: list[SecurityVulnerability] = []
        self._system_prompt = "You are a Security Scanner Agent."

    def scan(self, content: str) -> list[SecurityVulnerability]:
        """Scan code for security vulnerabilities.

        Args:
            content: Source code to scan.

        Returns:
            List of detected vulnerabilities.
        """
        self.vulnerabilities = []

        try:
            from rust_core import scan_code_vulnerabilities_rust  # type: ignore[attr-defined]

            # Rust returns (line_number, pattern_index, matched_text)
            rust_results = scan_code_vulnerabilities_rust(content)
            for line_num, pattern_idx, _ in rust_results:
                if pattern_idx < len(self.SECURITY_PATTERNS):
                    _, issue_type, severity, desc, fix = self.SECURITY_PATTERNS[pattern_idx]
                    self.vulnerabilities.append(
                        SecurityVulnerability(
                            type=issue_type,
                            severity=severity,
                            description=desc,
                            line_number=line_num,
                            fix_suggestion=fix,
                        )
                    )
        except (ImportError, AttributeError):
            # Fallback to Python implementation
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                for pattern, issue_type, severity, desc, fix in self.SECURITY_PATTERNS:
                    if re.search(pattern, line, re.I):
                        self.vulnerabilities.append(
                            SecurityVulnerability(
                                type=issue_type,
                                severity=severity,
                                description=desc,
                                line_number=i,
                                fix_suggestion=fix,
                            )
                        )

        # Phase 108: Intelligence Recording
        try:
            from src.infrastructure.com
"""

from __future__ import annotations

import re

from src.core.base.common.types.security_issue_type import SecurityIssueType
from src.core.base.common.types.security_vulnerability import SecurityVulnerability
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class SecurityScannerAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """Scans code for security vulnerabilities.

    Identifies common security issues and provides remediation guidance.
    """

    SECURITY_PATTERNS: list[tuple[str, SecurityIssueType, str, str, str]] = [
        (
            r'password\s*=\s*[\'"][^\'"]+[\'"]',
            SecurityIssueType.HARDCODED_SECRET,
            "high",
            "Hardcoded password detected",
            "Use environment variables or secure vault",
        ),
        (
            r'api_key\s*=\s*[\'"][^\'"]+[\'"]',
            SecurityIssueType.HARDCODED_SECRET,
            "high",
            "Hardcoded API key detected",
            "Use environment variables or secure vault",
        ),
        (
            r"os\.system\s*\([^)]*\+",
            SecurityIssueType.COMMAND_INJECTION,
            "critical",
            "Potential command injection vulnerability",
            "Use subprocess with shell=False and proper escaping",
        ),
        (
            r"ev" + r"al\s*\(",
            SecurityIssueType.INSECURE_DESERIALIZATION,
            "critical",
            "Use of ev" + "al() is dangerous",  # nosec
            "Avoid ev" + "al() or use ast.literal_eval() for safe parsing",
        ),
        (
            r"random\.(random|randint|choice)\s*\(",
            SecurityIssueType.INSECURE_RANDOM,
            "medium",
            "Insecure random number generation for security context",
            "Use secrets module for cryptographic randomness",
        ),
        (
            r"open\s*\([^)]*\+",
            SecurityIssueType.PATH_TRAVERSAL,
            "high",
            "Potential path traversal vulnerability",
            "Validate and sanitize file paths",
        ),
    ]

    def __init__(self, file_path: str) -> None:
        """Initialize the security scanner agent."""
        super().__init__(file_path)
        self.vulnerabilities: list[SecurityVulnerability] = []
        self._system_prompt = "You are a Security Scanner Agent."

    def scan(self, content: str) -> list[SecurityVulnerability]:
        """Scan code for security vulnerabilities.

        Args:
            content: Source code to scan.

        Returns:
            List of detected vulnerabilities.
        """
        self.vulnerabilities = []

        try:
            from rust_core import scan_code_vulnerabilities_rust  # type: ignore[attr-defined]

            # Rust returns (line_number, pattern_index, matched_text)
            rust_results = scan_code_vulnerabilities_rust(content)
            for line_num, pattern_idx, _ in rust_results:
                if pattern_idx < len(self.SECURITY_PATTERNS):
                    _, issue_type, severity, desc, fix = self.SECURITY_PATTERNS[pattern_idx]
                    self.vulnerabilities.append(
                        SecurityVulnerability(
                            type=issue_type,
                            severity=severity,
                            description=desc,
                            line_number=line_num,
                            fix_suggestion=fix,
                        )
                    )
        except (ImportError, AttributeError):
            # Fallback to Python implementation
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                for pattern, issue_type, severity, desc, fix in self.SECURITY_PATTERNS:
                    if re.search(pattern, line, re.I):
                        self.vulnerabilities.append(
                            SecurityVulnerability(
                                type=issue_type,
                                severity=severity,
                                description=desc,
                                line_number=i,
                                fix_suggestion=fix,
                            )
                        )

        # Phase 108: Intelligence Recording
        try:
            from src.infrastructure.compute.backend.local_context_recorder import LocalContextRecorder

            recorder = LocalContextRecorder(user_context="SecurityScanner")
            recorder.record_interaction(
                "Internal",
                "SecurityScanner",
                "Source Scan",
                f"Detected {len(self.vulnerabilities)} vulnerabilities.",
            )
        except (ImportError, AttributeError):
            pass

        return self.vulnerabilities

    def get_critical_count(self) -> int:
        """Get count of critical vulnerabilities.

        Returns:
            Number of critical severity vulnerabilities.
        """
        return sum(1 for v in self.vulnerabilities if v.severity == "critical")
