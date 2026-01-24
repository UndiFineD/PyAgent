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
SelfImprovementCore: Pure logic for fleet self-improvement analysis.
Extracted from SelfImprovementOrchestrator for Rust-readiness.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from .mixins.self_improvement_quality_mixin import SelfImprovementQualityMixin
from .mixins.self_improvement_security_mixin import \
    SelfImprovementSecurityMixin

try:
    import rust_core as rc

    _RUST_ACCEL = True
except ImportError:
    rc = None  # type: ignore[assignment]
    _RUST_ACCEL = False


class SelfImprovementCore(SelfImprovementSecurityMixin, SelfImprovementQualityMixin):
    """
    Pure logic core for identifying tech debt, security risks, and quality issues.
    This class contains no I/O and is suitable for Rust oxidation.
    """

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = workspace_root
        self._RUST_ACCEL = _RUST_ACCEL
        self.rc = rc
        # Security patterns (Phase 84 / 104)
        self.dangerous_patterns = [
            (r"\beval\s*\(", "Use of eval() is highly insecure."),  # nosec
            (
                r"subprocess\.run\(.*shell=True",
                "shell=True in subprocess can lead to command injection.",
            ),  # nosec
            (r"os\.system\(", "os.system() is deprecated and insecure."),  # nosec
            (r"yaml\.load\(", "Unsafe YAML loading detected. Use yaml.safe_load()."),  # nosec
            (
                r"pickle\.load\(",
                "Pickle can execute arbitrary code. Use JSON if possible.",
            ),  # nosec
            (r"requests\.get\(.*verify=False", "SSL verification is disabled."),  # nosec
        ]

        # IO patterns for intelligence gap detection
        self.io_pattern = (
            r"(requests\.(get|post|put|delete|patch|head)\(|self\.ai|"
            r"subprocess\.(run|call|Popen|check_call|check_output)\(|adb shell)"
        )

    def analyze_content(self, content: str, file_path_rel: str) -> List[Dict[str, Any]]:
        """
        Performs multi-dimensional analysis on file content.
        Returns a list of findings.
        """
        # Fast path: Use Rust for comprehensive analysis
        if _RUST_ACCEL and rc is not None:
            return self._analyze_via_rust(content, file_path_rel)

        # Python fallback
        findings = []
        findings.extend(self._analyze_security(content, file_path_rel))
        findings.extend(self._analyze_complexity(content, file_path_rel))
        findings.extend(self._analyze_documentation(content, file_path_rel))
        findings.extend(self._analyze_typing(content, file_path_rel))
        findings.extend(self._analyze_robustness_and_perf(content, file_path_rel))
        return findings

    def _analyze_via_rust(self, content: str, file_path_rel: str) -> List[Dict[str, Any]]:
        """Uses Rust accelerator for high-performance analysis."""
        try:
            rust_findings = rc.analyze_code_quality_rust(content, file_path_rel, self.dangerous_patterns)
            findings = []
            for issue_type, message, line_num in rust_findings:
                finding = {
                    "type": issue_type,
                    "message": message,
                    "file": file_path_rel,
                }
                if line_num > 0:
                    finding["line"] = line_num
                findings.append(finding)
            return findings
        except Exception:
            return []

    def generate_simple_fix(self, issue_type: str, content: str) -> Optional[str]:
        """
        Applies non-AI assisted simple fixes.
        """
        # Fast path: Use Rust for simple fixes
        if _RUST_ACCEL and rc is not None:
            try:
                result = rc.apply_simple_fixes_rust(content)
                if result:
                    fixed_content, _ = result
                    return fixed_content
                return None
            except Exception:
                pass  # Fall through to Python path

        # Python fallback
        if issue_type == "Robustness Issue":
            return re.sub(
                r"^(\s*)except:(\s*)(#.*)?$",
                r"\1except Exception:\2\3",
                content,
                flags=re.MULTILINE,
            )

        # Simple fix for unsafe YAML
        unsafe_yaml = "yaml." + "load("  # nosec: pattern definition
        if unsafe_yaml in content and "yaml.safe_load(" not in content:
            if "import yaml" in content:
                return content.replace(unsafe_yaml, "yaml.safe_load(")

        return None
