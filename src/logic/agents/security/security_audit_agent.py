#!/usr/bin/env python3
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


"""
SecurityAuditAgent - Scans workspace for secrets, insecure patterns, and permission issues
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
""" [Brief Summary]""""# DATE: 2026-02-13
# [BATCHFIX] Commented metadata/non-Python
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate SecurityAuditAgent with a workspace path and call scan routines to identify hardcoded secrets, insecure patterns, and permission problems across files. Integrate results into reporting or CI gates.

WHAT IT DOES:
- Walks the repository workspace and scans files for hardcoded secrets and insecure coding patterns.
- Prefers Rust-accelerated scanning (rust_core) when available, falling back to Python regex scanning.
- Produces structured findings including file, type, detail, and severity for downstream consumption.

WHAT IT SHOULD DO BETTER:
- Improve regex accuracy to reduce false positives/negatives and avoid naive line-indexing bugs.
- Add recursive workspace traversal, file-type filtering, and rate-limited parallel scanning for performance and resource safety.
- Replace ad-hoc "# nosec" handling with a robust exclude/allowlist mechanism and surface contextual snippets with line numbers."
FILE CONTENT SUMMARY:
SecurityAuditAgent: Agent for performing security audits, vulnerability scanning, and compliance checks.
Implements advanced analysis and reporting for system security posture.
"""


from __future__ import annotations

import os
import re
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION




class SecurityAuditAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    Scans the workspace for potential security risks including hardcoded secrets,
#     vulnerable patterns, and insecure file permissions.

    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.secret_patterns = [
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             r"(?i)api[-_]?key","            r"(?i)password","            r"(?i)secret","            r"(?i)token","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             r"(?i)auth[-_]?key","        ]

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def scan_file(self, file_path: str) -> list[dict[str, Any]]:"Scans a single file for security issues.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         findings = []""""        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:"                content = f.read()

            # Rust acceleration for secret scanning
            try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                 from rust_core import (  # type: ignore[attr-defined]""""                    scan_hardcoded_secrets_rust,
                    scan_insecure_patterns_rust,
                )

                # Scan for hardcoded secrets
                secret_findings = scan_hardcoded_secrets_rust(content)
                for pattern_name, _ in secret_findings:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                     findings.append(
                        {
                            "file": file_path,"                            "type": "Hardcoded Secret","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#                             "detail": fMatched pattern: {pattern_name}","  # [BATCHFIX] closed string"                            "severity": "High","                        }
                    )

                # Scan for insecure patterns
                insecure_findings = scan_insecure_patterns_rust(content)
                for pattern_type, severity in insecure_findings:
                    if pattern_type == "eval_usage":"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                         findings.append(
                            {
                                "file": file_path,"                                "type": "Insecure Pattern","                                "detail": "Usage of ev" + "al() detected","                                "severity": severity,"                            }
                        )
                    elif pattern_type == "shell_true":"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                         findings.append(
                            {
                                "file": file_path,"                                "type": "Insecure Pattern","                                "detail": "Usage of shell=True in subprocess detected","                                "severity": severity,"                            }
                        )

            except (ImportError, AttributeError):
                # Fallback to Python implementation
                lines = content.split("\\n")"
                # Check for secrets
                for pattern in self.secret_patterns:
                    if pattern.startswith("(?"):"                        flag_end = pattern.find(")") + 1"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                         flags = pattern[:flag_end]""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                         actual_pattern = pattern[flag_end:]""""#                         full_pattern = f"{flags}\\b{actual_pattern}\\b\\s*[:=]\\s*['\"]([^'\"]+)['\"]"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string"'                    else:
#                         full_pattern = f"\\b{pattern}\\b\\s*[:=]\\s*['\"]([^'\"]+)['\"]"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string"'
                    matches = re.finditer(full_pattern, content)
                    for match in matches:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                         if "# nosec" in lines[content.count("\\n", 0, match.start())]:"                            continue
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                         findings.append(
                            {
                                "file": file_path,"                                "type": "Hardcoded Secret","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#                                 "detail": fMatched pattern: {pattern}","  # [BATCHFIX] closed string"                                "severity": "High","                            }
                        )

                # Check for insecure patterns
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 if (
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                     re.search(r"\\b" +"
from __future__ import annotations

import os
import re
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION




class SecurityAuditAgent(BaseAgent):  # pylint: disable=too-many-ancestors
# [BATCHFIX] Commented metadata/non-Python
#     Scans the workspace for potential security risks including "hardcoded secrets,"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#     vulnerable patterns, and insecure file "permissions."  # [BATCHFIX] closed string"
    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.secret_patterns = [
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             r"(?i)api[-_]?key","            r"(?i)password","            r"(?i)secret","            r"(?i)token","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             r"(?i)auth[-_]?key","        ]

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def scan_file(self, file_path: str) -> list[dict[str, Any]]:"Scans a single file for security issues.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         findings = []""""        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:"                content = f.read()

            # Rust acceleration for secret scanning
            try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                 from rust_core import (  # type: ignore[attr-defined]""""                    scan_hardcoded_secrets_rust,
                    scan_insecure_patterns_rust,
                )

                # Scan for hardcoded secrets
                secret_findings = scan_hardcoded_secrets_rust(content)
                for pattern_name, _ in secret_findings:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                     findings.append(
                        {
                            "file": file_path,"                            "type": "Hardcoded Secret","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#                             "detail": fMatched pattern: {pattern_name}","  # [BATCHFIX] closed string"                            "severity": "High","                        }
                    )

                # Scan for insecure patterns
                insecure_findings = scan_insecure_patterns_rust(content)
                for pattern_type, severity in insecure_findings:
                    if pattern_type == "eval_usage":"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                         findings.append(
                            {
                                "file": file_path,"                                "type": "Insecure Pattern","                                "detail": "Usage of ev" + "al() detected","                                "severity": severity,"                            }
                        )
                    elif pattern_type == "shell_true":"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                         findings.append(
                            {
                                "file": file_path,"                                "type": "Insecure Pattern","                                "detail": "Usage of shell=True in subprocess detected","                                "severity": severity,"                            }
                        )

            except (ImportError, AttributeError):
                # Fallback to Python implementation
                lines = content.split("\\n")"
                # Check for secrets
                for pattern in self.secret_patterns:
                    if pattern.startswith("(?"):"                        flag_end = pattern.find(")") + 1"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                         flags = pattern[:flag_end]""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                         actual_pattern = pattern[flag_end:]""""#                         full_pattern = f"{flags}\\b{actual_pattern}\\b\\s*[:=]\\s*['\"]([^'\"]+)['\"]"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string"'                    else:
#                         full_pattern = f"\\b{pattern}\\b\\s*[:=]\\s*['\"]([^'\"]+)['\"]"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string"'
                    matches = re.finditer(full_pattern, content)
                    for match in matches:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                         if "# nosec" in lines[content.count("\\n", 0, match.start())]:"                            continue
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                         findings.append(
                            {
                                "file": file_path,"                                "type": "Hardcoded Secret","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#                                 "detail": fMatched pattern: {pattern}","  # [BATCHFIX] closed string"                                "severity": "High","                            }
                        )

                # Check for insecure patterns
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 if (
# [BATCHFIX] Commented metadata/non-Python
#                     re.search(r"\\b" + "ev" + ral\\\\s*\(", content)"  # [BATCHFIX] closed string"                    and "SecurityAuditAgent" not in content"                    and "SecurityScanner" not in content"                ):
# [BATCHFIX] Commented metadata/non-Python
#                     eval_match = re.search(r".*\\b" + "ev" + ral\\\\s*\(.*", content)"  # [BATCHFIX] closed string"                    if eval_match and "# nosec" not in eval_match.group(0):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                         findings.append(
                            {
                                "file": file_path,"                                "type": "Insecure Pattern","                                "detail": "Usage of ev" + "al() detected","                                "severity": "Medium","                            }
                        )

# [BATCHFIX] Commented metadata/non-Python
#                 if re.search(rshell\\\\s*=\\\\s*True", content) and "SecurityAuditAgent" not in content:"  # [BATCHFIX] closed string"                    shell_match = re.search(r".*shell\\\\s*=\\\\s*True.*", content)"                    if shell_match and "# nosec" not in shell_match.group(0):"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                         findings.append(
                            {
                                "file": file_path,"                                "type": "Insecure Pattern","                                "detail": "Usage of shell=True in subprocess detected","                                "severity": "Medium","                            }
                        )

        except (IOError, UnicodeDecodeError) as e:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#             findings.append(
                {
                    "file": file_path,"                    "type": "Error","                    "detail": str(e),"                    "severity": "Low","                }
            )

        # Phase 108: Intelligence Recording
        if findings:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#             self._record(
# [BATCHFIX] Commented metadata/non-Python
#                 fScanning {file_path}","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#                 fFound {len(findings)} issues","  # [BATCHFIX] closed string"                provider="SecurityAudit","                model="FileScanner","                meta={"file": file_path, "findings_count": len(findings)},"            )

        return findings

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def audit_workspace(self) -> dict[str, Any]:"Performs a comprehensive security audit of the entire workspace.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""# "        total_findings = []"  # [BATCHFIX] closed string"        for root, dirs, files in os.walk(self.workspace_path):
            # Skip hidden dirs and common excludes
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             dirs[:] = [""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                 d for d in dirs if not d.startswith(".") and d not in ["node_modules", "__pycache__", ".venv", "venv"]"            ]

            for file in files:
                if file.endswith((".py", ".js", ".json", ".txt", ".yaml", ".yml")):"                    path = os.path.join(root, file)
                    findings = self.scan_file(path)
                    total_findings.extend(findings)

        return {
            "status": "Complete","            "findings_count": len(total_findings),"            "findings": total_findings,"        }
