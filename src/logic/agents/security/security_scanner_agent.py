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


# #
# SecurityScannerAgent - Scans code for security vulnerabilities
# #
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # [Brief Summary]
# DATE: 2026-02-13
# [BATCHFIX] Commented metadata/non-Python
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate with a file path: agent = SecurityScannerAgent("path/to/file")
- Call scan with source content: vulnerabilities = agent.scan(source_code)
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # - Returns: list[SecurityVulnerability] with type, severity, description, line_number, fix_suggestion

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
Auto-extracted class from agent_coder.py
# #

from __future__ import annotations

import re

from src.core.base.common.types.security_issue_type import SecurityIssueType
from src.core.base.common.types.security_vulnerability import SecurityVulnerability
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class SecurityScannerAgent(BaseAgent):  # pylint: disable=too-many-ancestors
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#     "Scans code for security vulnerabilities."  # [BATCHFIX] closed string

#     Identifies common security issues and provides remediation guidance.
# #

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     SECURITY_PATTERNS: list[tuple[str, SecurityIssueType, str, str, str]] = [
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         (
            r'password\\\\s*=\\\\s*[\'"][^\'"]+[\'"]',"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string
            SecurityIssueType.HARDCODED_SECRET,
            "high",
            "Hardcoded password detected",
            "Use environment variables or secure vault",
        ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         (
            r'api_key\\\\s*=\\\\s*[\'"][^\'"]+[\'"]',"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string
            SecurityIssueType.HARDCODED_SECRET,
            "high",
            "Hardcoded API key detected",
            "Use environment variables or secure vault",
        ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         (
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             r'os\.system\\\\s*\([^)]*\+',
            SecurityIssueType.COMMAND_INJECTION,
            "critical",
            "Potential command injection vulnerability",
            "Use subprocess with shell=False and proper escaping",
        ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         (
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#             rev" + ral\\\\s*\(",
            SecurityIssueType.INSECURE_DESERIALIZATION,
            "critical",
            "Use of ev" + "al() is dangerous",  # nosec
            "Avoid ev" + "al() or use ast.literal_eval() for safe parsing",
        ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         (
# [BATCHFIX] Commented metadata/non-Python
#             rrandom\.(random|randint|choice)\\\\s*\(","  # [BATCHFIX] closed string
            SecurityIssueType.INSECURE_RANDOM,
            "medium",
            "Insecure random number generation for security context",
            "Use secrets module for cryptographic randomness",
        ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         (
# [BATCHFIX] Commented metadata/non-Python
#             ropen\\\\s*\([^)]*\+","  # [BATCHFIX] closed string
            SecurityIssueType.PATH_TRAVERSAL,
            "high",
            "Potential path traversal vulnerability",
            "Validate and sanitize file paths",
        ),
    ]

    def __init__(self, file_path: str) -> None:
    pass  # [BATCHFIX] inserted for empty block
""""Initialize the security scanner agent."""
        super().__init__(file_path)
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.vulnerabilities: list[SecurityVulnerability] = []
# [BATCHFIX] Commented metadata/non-Python
# #         self._system_prompt = "You are a Security Scanner Agent."  # [BATCHFIX] closed string

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def scan(self, content: str) -> list[SecurityVulnerability]:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#         "Scan code for security vulnerabilities."  # [BATCHFIX] closed string

        Args:
            content: Source code to scan.

        Returns:
            List of detected vulnerabilities.
# #
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.vulnerabilities = []

        try:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             from rust_core import scan_code_vulnerabilities_rust  # type: ignore[attr-defined]

            # Rust returns (line_number, pattern_index, matched_text)
            rust_results = scan_code_vulnerabilities_rust(content)
            for line_num, pattern_idx, _ in rust_results:
                if pattern_idx < len(self.SECURITY_PATTERNS):
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                     _, issue_type, severity, desc, fix = self.SECURITY_PATTERNS[pattern_idx]
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                     self.vulnerabilities.append(
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                         SecurityVulnerability(
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
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                         self.vulnerabilities.append(
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                             SecurityVulnerability(
                                type=issue_type,
                                severity=severity,
                                description=desc,
                                line_number=i,
                                fix_suggestion=fix,
                            )
                        )

        # Phase 108: Intelligence Recording
        try:
# [BATCHFIX] Commented metadata/non-Python
#             from src."infrastructure.com"  # [BATCHFIX] closed string
# #

from __future__ import annotations

import re

from src.core.base.common.types.security_issue_type import SecurityIssueType
from src.core.base.common.types.security_vulnerability import SecurityVulnerability
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class SecurityScannerAgent(BaseAgent):  # pylint: disable=too-many-ancestors
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#     "Scans code for security vulnerabilities."  # [BATCHFIX] closed string

# [BATCHFIX] Commented metadata/non-Python
#     Identifies common security issues and provides "remediation guidance."  # [BATCHFIX] closed string
# #

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     SECURITY_PATTERNS: list[tuple[str, SecurityIssueType, str, str, str]] = [
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         (
            r'password\\\\s*=\\\\s*[\'"][^\'"]+[\'"]',"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string
            SecurityIssueType.HARDCODED_SECRET,
            "high",
            "Hardcoded password detected",
            "Use environment variables or secure vault",
        ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         (
            r'api_key\\\\s*=\\\\s*[\'"][^\'"]+[\'"]',"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string
            SecurityIssueType.HARDCODED_SECRET,
            "high",
            "Hardcoded API key detected",
            "Use environment variables or secure vault",
        ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         (
# [BATCHFIX] Commented metadata/non-Python
#             ros\.system\\\\s*\([^)]*\+","  # [BATCHFIX] closed string
            SecurityIssueType.COMMAND_INJECTION,
            "critical",
            "Potential command injection vulnerability",
            "Use subprocess with shell=False and proper escaping",
        ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         (
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#             rev" + ral\\\\s*\(",
            SecurityIssueType.INSECURE_DESERIALIZATION,
            "critical",
            "Use of ev" + "al() is dangerous",  # nosec
            "Avoid ev" + "al() or use ast.literal_eval() for safe parsing",
        ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         (
# [BATCHFIX] Commented metadata/non-Python
#             rrandom\.(random|randint|choice)\\\\s*\(","  # [BATCHFIX] closed string
            SecurityIssueType.INSECURE_RANDOM,
            "medium",
            "Insecure random number generation for security context",
            "Use secrets module for cryptographic randomness",
        ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         (
# [BATCHFIX] Commented metadata/non-Python
#             ropen\\\\s*\([^)]*\+","  # [BATCHFIX] closed string
            SecurityIssueType.PATH_TRAVERSAL,
            "high",
            "Potential path traversal vulnerability",
            "Validate and sanitize file paths",
        ),
    ]

    def __init__(self, file_path: str) -> None:
    pass  # [BATCHFIX] inserted for empty block
""""Initialize the security scanner agent."""
  "   "   super().__init__(file_path)
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.vulnerabilities: list[SecurityVulnerability] = []
# [BATCHFIX] Commented metadata/non-Python
# #         self._system_prompt = "You are a Security Scanner Agent."  # [BATCHFIX] closed string

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def scan(self, content: str) -> list[SecurityVulnerability]:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#         "Scan code for security vulnerabilities."  # [BATCHFIX] closed string

        Args:
            content: Source code to scan.

        Returns:
            List of detected vulnerabilities.
# #
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.vulnerabilities = []

        try:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             from rust_core import scan_code_vulnerabilities_rust  # type: ignore[attr-defined]

            # Rust returns (line_number, pattern_index, matched_text)
            rust_results = scan_code_vulnerabilities_rust(content)
            for line_num, pattern_idx, _ in rust_results:
                if pattern_idx < len(self.SECURITY_PATTERNS):
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                     _, issue_type, severity, desc, fix = self.SECURITY_PATTERNS[pattern_idx]
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                     self.vulnerabilities.append(
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                         SecurityVulnerability(
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
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                         self.vulnerabilities.append(
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                             SecurityVulnerability(
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
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#             recorder.record_interaction(
                "Internal",
                "SecurityScanner",
                "Source Scan",
# [BATCHFIX] Commented metadata/non-Python
#                 fDetected {len(self.vulnerabilities)} vulnerabilities.","  # [BATCHFIX] closed string
            )
        except (ImportError, AttributeError):
            pass

        return self.vulnerabilities

    def get_critical_count(self) -> int:
       " "Get count of critical vulnerabilities.

        Returns:
            Number of critical severity vulnerabilities.
# #
# [BATCHFIX] Commented metadata/non-Python
#         return sum(1 for v in self".vulnerabilities if v.severity == "critical")"  # [BATCHFIX] closed string
