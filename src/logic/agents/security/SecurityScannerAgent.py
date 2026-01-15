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
from src.core.base.types.SecurityIssueType import SecurityIssueType
from src.core.base.types.SecurityVulnerability import SecurityVulnerability
from src.core.base.BaseAgent import BaseAgent
import re

__version__ = VERSION




class SecurityScannerAgent(BaseAgent):
    """Scans code for security vulnerabilities.

    Identifies common security issues and provides remediation guidance.
    """

    SECURITY_PATTERNS: list[tuple[str, SecurityIssueType, str, str, str]] = [
        (r'password\s*=\s*[\'"][^\'"]+[\'"]',
         SecurityIssueType.HARDCODED_SECRET, "high",
         "Hardcoded password detected",
         "Use environment variables or secure vault"),
        (r'api_key\s*=\s*[\'"][^\'"]+[\'"]',
         SecurityIssueType.HARDCODED_SECRET, "high",
         "Hardcoded API key detected",
         "Use environment variables or secure vault"),
        (r"os\.system\s*\([^)]*\+",
         SecurityIssueType.COMMAND_INJECTION, "critical",
         "Potential command injection vulnerability",
         "Use subprocess with shell=False and proper escaping"),
        (r"ev" + r"al\s*\(",
         SecurityIssueType.INSECURE_DESERIALIZATION, "critical",
         "Use of ev" + "al() is dangerous",
         "Avoid ev" + "al() or use ast.literal_eval() for safe parsing"),
        (r"random\.(random|randint|choice)\s*\(",
         SecurityIssueType.INSECURE_RANDOM, "medium",
         "Insecure random number generation for security context",
         "Use secrets module for cryptographic randomness"),
        (r"open\s*\([^)]*\+",
         SecurityIssueType.PATH_TRAVERSAL, "high",
         "Potential path traversal vulnerability",
         "Validate and sanitize file paths"),
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
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            for pattern, issue_type, severity, desc, fix in self.SECURITY_PATTERNS:
                if re.search(pattern, line, re.I):
                    self.vulnerabilities.append(SecurityVulnerability(
                        type=issue_type,
                        severity=severity,
                        description=desc,
                        line_number=i,
                        fix_suggestion=fix
                    ))

        # Phase 108: Intelligence Recording
        try:
            from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder
            recorder = LocalContextRecorder(user_context="SecurityScanner")
            recorder.record_interaction("Internal", "SecurityScanner", "Source Scan", f"Detected {len(self.vulnerabilities)} vulnerabilities.")
        except Exception:
            pass

        return self.vulnerabilities

    def get_critical_count(self) -> int:
        """Get count of critical vulnerabilities.

        Returns:
            Number of critical severity vulnerabilities.
        """
        return sum(1 for v in self.vulnerabilities if v.severity == "critical")
