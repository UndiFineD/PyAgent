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

"""
Security analysis logic for SelfImprovementCore.
"""

from __future__ import annotations
import re
from typing import List, Dict, Any

class SelfImprovementSecurityMixin:
    """Mixin for security-related analysis."""

    def _analyze_security(self, content: str, file_path_rel: str) -> List[Dict[str, Any]]:
        """Scans for dangerous patterns and security risks."""
        findings = []

        # Access class-level attributes
        dangerous_patterns = getattr(self, "dangerous_patterns", [])
        _RUST_ACCEL = getattr(self, "_RUST_ACCEL", False)
        rc = getattr(self, "rc", None)

        if _RUST_ACCEL and rc is not None:
            try:
                rust_findings = rc.analyze_security_patterns_rust(
                    content, dangerous_patterns
                )
                for line_num, pattern, msg in rust_findings:
                    if "SelfImprovementCore" in content and pattern in str(
                        dangerous_patterns
                    ):
                        continue
                    findings.append(
                        {
                            "type": "Security Risk",
                            "message": f"{msg} (Pattern: {pattern})",
                            "file": file_path_rel,
                            "line": line_num,
                        }
                    )
                return findings
            except Exception:
                pass

        lines = content.split("\n")
        for pattern, msg in dangerous_patterns:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    if "# nosec" in line:
                        continue
                    if "SelfImprovementCore" in content and pattern in str(
                        dangerous_patterns
                    ):
                        continue

                    findings.append(
                        {
                            "type": "Security Risk",
                            "message": f"{msg} (Pattern: {pattern})",
                            "file": file_path_rel,
                            "line": i,
                        }
                    )
        return findings
