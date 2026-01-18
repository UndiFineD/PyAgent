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

"""Content scanning logic for SecurityCore."""

from __future__ import annotations
import re
from src.core.base.types.SecurityIssueType import SecurityIssueType
from src.core.base.types.SecurityVulnerability import SecurityVulnerability

# Rust acceleration imports
try:
    from rust_core import scan_lines_multi_pattern_rust
    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False

class SecurityScannerMixin:
    """Mixin for content and injection scanning."""

    def scan_content(self, content: str) -> list[SecurityVulnerability]:
        """Performs a comprehensive scan of the provided content."""
        vulnerabilities = []

        # Rust-accelerated multi-pattern scanning
        if _RUST_AVAILABLE:
            try:
                patterns = [p[0] for p in self.SECURITY_PATTERNS]
                matches = scan_lines_multi_pattern_rust(content, patterns)
                for line_num, pat_idx, _ in matches:
                    _, issue_type, severity, desc, fix = self.SECURITY_PATTERNS[pat_idx]
                    vuln = SecurityVulnerability(
                        type=issue_type,
                        severity=severity,
                        description=desc,
                        line_number=line_num,
                        fix_suggestion=fix,
                    )
                    vulnerabilities.append(vuln)
                    if hasattr(self, "_record_finding"):
                        self._record_finding(issue_type.value, severity, desc)
            except Exception:
                pass  # Fall back to Python
            else:
                # Skip Python fallback if Rust succeeded
                return self._add_injection_findings(vulnerabilities, content)

        # Python fallback
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if not hasattr(self, "SECURITY_PATTERNS"):
                break
            for pattern, issue_type, severity, desc, fix in self.SECURITY_PATTERNS:
                if re.search(pattern, line):
                    vuln = SecurityVulnerability(
                        type=issue_type,
                        severity=severity,
                        description=desc,
                        line_number=i,
                        fix_suggestion=fix,
                    )
                    vulnerabilities.append(vuln)
                    if hasattr(self, "_record_finding"):
                        self._record_finding(issue_type.value, severity, desc)

        # Add injection scanning
        return self._add_injection_findings(vulnerabilities, content)

    def scan_for_injection(self, content: str) -> list[str]:
        """Detects prompt injection or agent manipulation attempts."""
        injection_patterns = {
            "Instruction Override": r"(?i)(ignore previous instructions|disregard all earlier commands|system prompt reset|you are now a|stay in character as)",
            "Indirect Directive": r"(?i)(agent:|assistant:|bot:)\s*(execute|run|delete|send|upload|rm |chmod)",
            "Payload Loader": r"(?i)(fetch the following url and run|download and execute|base64 decode this|eval\(base64)",
            "Social Engineering": r"(?i)(congratulations!|security alert: action|verify your account|login to continue)",
        }
        findings = []
        for name, pattern in injection_patterns.items():
            if re.search(pattern, content):
                findings.append(f"INJECTION ATTEMPT: {name} pattern detected.")
        return findings

    def _add_injection_findings(
        self, vulnerabilities: list[SecurityVulnerability], content: str
    ) -> list[SecurityVulnerability]:
        """Add injection scanning findings to vulnerability list."""
        injection_findings = self.scan_for_injection(content)
        for inf in injection_findings:
            vulnerabilities.append(
                SecurityVulnerability(
                    type=SecurityIssueType.INJECTION_ATTEMPT,
                    severity="high",
                    description=inf,
                    line_number=0,
                    fix_suggestion="Sanitize all inputs and wrap specialized instructions in strict boundaries.",
                )
            )
            if hasattr(self, "_record_finding"):
                self._record_finding(SecurityIssueType.INJECTION_ATTEMPT.value, "high", inf)
        return vulnerabilities
