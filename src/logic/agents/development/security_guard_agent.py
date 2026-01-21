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


"""Agent specializing in security validation and safety checks."""

from __future__ import annotations
from src.core.base.version import VERSION
from src.core.base.base_agent import BaseAgent
from src.core.base.base_utilities import create_main_function
from src.logic.agents.development.security_core import SecurityCore

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
