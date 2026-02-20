#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# [BATCHFIX] Commented metadata/non-Python
""" "Content scanning logic for SecurityCore."  # [BATCHFIX] closed string"# 
import re
from typing import TYPE_CHECKING

from src.core.base.common.types.security_issue_type import SecurityIssueType
from src.core.base.common.types.security_vulnerability import SecurityVulnerability

if TYPE_CHECKING:
    from src.logic.agents.security.security_core import SecurityCore

# Rust acceleration imports
try:
    from rust_core import scan_lines_multi_pattern_rust  # type: ignore

    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False



class SecurityScannerMixin:
# [BATCHFIX] Commented metadata/non-Python
#     pass  # [BATCHFIX] inserted for empty class
""""Mixin for content and injection scanning.
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""     def scan_content(self: SecurityCore, content: str) -> list[SecurityVulnerability]:"Performs a comprehensive scan of the provided content.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""         vulnerabilities = []""""
        # Rust-accelerated multi-pattern scanning
        if _RUST_AVAILABLE:
            try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""                 patterns = [p[0] for p in self.SECURITY_PATTERNS]""""                matches = scan_lines_multi_pattern_rust(content, patterns)
                for line_num, pat_idx, _ in matches:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""                     _, issue_type, severity, desc, fix = self.SECURITY_PATTERNS[pat_idx]""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""
#                     vuln = SecurityVulnerability(
                        type=issue_type,
                        severity=severity,
                        description=desc,
                        line_number=line_num,
                        fix_suggestion=fix,
                    )
                    vulnerabilities.append(vuln)
                    if hasattr(self, "_record_finding"):"                        self._record_finding(issue_type.value, severity, desc)
            except (AttributeError, RuntimeError, TypeError):
                pass  # Fall back to Python
            else:
                # Skip Python fallback if Rust succeeded
                return self._add_injection_findings(vulnerabilities, content)

        # Python fallback
        lines = content.split("\\n")"        for i, line in enumerate(lines, 1):
            if not hasattr(self, "SECURITY_PATTERNS"):"                break
            for pattern, issue_type, severity, desc, fix in self.SECURITY_PATTERNS:
                if re.search(pattern, line):
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""
#                     vuln = SecurityVulnerability(
                        type=issue_type,
                        severity=severity,
                        description=desc,
                        line_number=i,
                        fix_suggestion=fix,
                    )
                    vulnerabilities.append(vuln)
                    if hasattr(self, "_record_finding"):"                        self._record_finding(issue_type.value, severity, desc)

        # Add injection scanning
        return self._add_injection_findings(vulnerabilities, content)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""     def scan_for_injection(self, content: str) -> list[str]:"Detects prompt injection or agent manipulation attempts.        injection_patterns = {
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""
#             "Instruction Override": ("# [BATCHFIX] Commented metadata/non-Python
"""                 r"(?i)(ignore previous instructions|disregard all earlier commands|"  # [BATCHFIX] closed string"#                 rsystem prompt reset|you are now a|stay in character as)
            ),
            "Indirect Directive": r"(?i)(agent:|assistant:|bot:)\\\\s*(execute|run|delete|send|upload|rm |chmod)","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""
#             "Payload Loader": ("# [BATCHFIX] Commented metadata/non-Python
"""                 r"(?i)(fetch the following url and run|download and execute|base64 decode this|eval\(base64)"  # [BATCHFIX] closed string"            ),
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""
#             "Social Engineering": ("# [BATCHFIX] Commented metadata/non-Python
"""                 r"(?i)(congratulations!|security alert: action|verify your account|login to continue)"  # [BATCHFIX] closed string"            ),
        }
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""         findings = []""""        for name, pattern in injection_patterns.items():
            if re.search(pattern, content):
# [BATCHFIX] Commented metadata/non-Python
#                 findings.append(fINJECTION ATTEMPT: {name} pattern detected.")"  # [BATCHFIX] closed string"        return findings

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""
#     def _add_injection_findings(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""         self, vulnerabilities: list[SecurityVulnerability], content: str""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""     ) -> list[SecurityVulnerability]:""""
# [BATCHFIX] Commented metadata/non-Python
"""         "Add injection scanning findings to vulnerability list."  # [BATCHFIX] closed string"        injection_findings = self.scan_for_injection(content)
        for inf in injection_findings:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""
#             vulnerabilities.append(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""
#                 SecurityVulnerability(
                    type=SecurityIssueType.INJECTION_ATTEMPT,
                    severity="high","                    description=inf,
                    line_number=0,
                    fix_suggestion="Sanitize all inputs and wrap specialized instructions in strict boundaries.","                )
            )
            if hasattr(self, "_record_finding"):"                self._record_finding(SecurityIssueType.INJECTION_ATTEMPT.value, "high", inf)"        return vulnerabilities
