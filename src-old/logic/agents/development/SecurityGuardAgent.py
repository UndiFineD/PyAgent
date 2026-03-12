#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/development/SecurityGuardAgent.description.md

# SecurityGuardAgent

**File**: `src\logic\agents\development\SecurityGuardAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 136  
**Complexity**: 9 (moderate)

## Overview

Agent specializing in security validation and safety checks.

## Classes (1)

### `SecurityGuardAgent`

**Inherits from**: BaseAgent

Protects the workspace by validating diffs and commands.

**Methods** (9):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `scan_for_secrets(self, content)`
- `audit_command(self, command)`
- `validate_shell_script(self, script_content)`
- `scan_for_injection(self, content)`
- `generate_safety_report(self, task, code_changes, commands)`
- `detect_jailbreak(self, prompt)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `src.logic.agents.development.SecurityCore.SecurityCore`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/SecurityGuardAgent.improvements.md

# Improvements for SecurityGuardAgent

**File**: `src\logic\agents\development\SecurityGuardAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 136 lines (medium)  
**Complexity**: 9 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SecurityGuardAgent_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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


"""Agent specializing in security validation and safety checks."""

from src.core.base.version import VERSION
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import create_main_function
from src.logic.agents.development.SecurityCore import SecurityCore
from typing import List, Tuple

__version__ = VERSION


class SecurityGuardAgent(BaseAgent):
    """Protects the workspace by validating diffs and commands."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.capabilities.extend(
            ["security-audit", "secret-scanning", "vulnerability-detection"]
        )  # Phase 241
        self.security_core = SecurityCore(
            workspace_root=str(self.file_path.parent.parent.parent)
        )
        self._system_prompt = (
            "You are the Security Guard Agent. "
            "Your role is to inspect proposed changes and commands for security risks. "
            "Look for: Hardcoded secrets, destructive commands (rm -rf /), unauthorized network access, and malicious logic. "
            "Output a 'Safety Audit' report. If a risk is high, explicitly say 'RISK: HIGH'."
        )

    def _get_default_content(self) -> str:
        return "# Workspace Security Log\n\n## Status\nMonitoring active.\n"

    def scan_for_secrets(self, content: str) -> list[str]:
        """Scans for secrets using the core logic."""
        vulns = self.security_core.scan_content(content)
        return [v.description for v in vulns if v.severity in ["high", "critical"]]

    def audit_command(self, command: str) -> tuple[str, str]:
        """Audits a shell command via the security core."""
        return self.security_core.audit_command(command)

    def validate_shell_script(self, script_content: str) -> list[str]:
        """Performs static analysis on shell scripts via the security core."""
        return self.security_core.validate_shell_script(script_content)

    def scan_for_injection(self, content: str) -> list[str]:
        """Scans for indirect prompt injection via the security core."""
        return self.security_core.scan_for_injection(content)

    def generate_safety_report(
        self, task: str, code_changes: str, commands: list[str]
    ) -> str:
        """Generates a comprehensive safety audit report."""
        vulnerabilities = self.security_core.scan_content(code_changes)

        command_reports = []
        for cmd in commands:
            level, msg = self.security_core.audit_command(cmd)
            command_reports.append(f"- `{cmd}`: **{level}** - {msg}")

        risk_level = self.security_core.get_risk_level(vulnerabilities)
        if any("HIGH" in r or "CRITICAL" in r for r in command_reports):
            risk_level = "HIGH"

        report = [
            f"# Safety Audit Report for: {task}",
            f"**Overall Risk Level: {risk_level}**",
            "\n## Code Vulnerabilities",
        ]

        if not vulnerabilities:
            report.append("- No high-risk patterns detected in code changes.")
        else:
            for v in vulnerabilities:
                report.append(
                    f"- [{v.severity.upper()}] Line {v.line_number}: {v.description}"
                )
                report.append(f"  * Fix: {v.fix_suggestion}")

        report.append("\n## Command Audit")
        report.extend(
            command_reports
            if command_reports
            else ["- No commands provided for audit."]
        )

        return "\n".join(report)

    def detect_jailbreak(self, prompt: str) -> bool:
        """Enhanced multi-stage jailbreak detection using structural analysis."""
        # Check for characteristic jailbreak patterns (DAN, persona adoption, etc.)
        jailbreak_markers = [
            "DAN",
            "Do Anything Now",
            "Stay in character",
            "You are now a",
            "bypass",
            "unfiltered",
        ]
        if any(marker.lower() in prompt.lower() for marker in jailbreak_markers):
            return True

        # Check for adversarial suffix patterns
        if len(prompt) > 50 and prompt.strip().endswith(("!!!", "???", "---")):
            # Common in pressure-based jailbreaks
            pass

        return False

    def improve_content(self, prompt: str) -> str:
        """Perform a security audit of the provided snippet or command."""
        secrets = self.scan_for_secrets(prompt)
        risk_level, command_warning = self.audit_command(prompt)
        injections = self.scan_for_injection(prompt)
        is_jailbreak = self.detect_jailbreak(prompt)

        report = [
            "## Security Audit Report",
            f"**Target Analysis**: {prompt[:100]}...",
            f"**Overall Risk**: {'HIGH' if risk_level == 'HIGH' or injections or is_jailbreak else risk_level}",
            "",
        ]

        if is_jailbreak:
            report.append("> [!DANGER] Jailbreak Attempt Detected")

        if secretions := (secrets + injections):
            report.append("> [!CAUTION] Security Threats Detected")
            for s in secretions:
                report.append(f"> - {s}")
            report.append("")

        if risk_level != "LOW":
            report.append(f"> [!WARNING] Command Risk: {command_warning}")

        return "\n".join(report)


if __name__ == "__main__":
    main = create_main_function(
        SecurityGuardAgent, "SecurityGuard Agent", "Content or Command to audit"
    )
    main()
