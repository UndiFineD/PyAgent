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

"""Command and script auditing logic for SecurityCore."""

from __future__ import annotations

import re


class SecurityAuditorMixin:
    """Mixin for command and shell script auditing."""

    def audit_command(self, command: str) -> tuple[str, str]:
        """Audits a shell command for dangerous operations."""
        risky_patterns = [
            (r"rm\s+-rf\s+/", "CRITICAL: Destructive root deletion requested"),
            (r"rm\s+-rf\s+\*", "HIGH: Recursive deletion in current directory"),
            (r"chmod\s+777", "MEDIUM: Overly permissive permissions (world-writable)"),
            (
                r"curl\|bash|wget\|sh|curl.*\|.*sh",
                "HIGH: Remote script execution (pipe to shell)",
            ),
            (
                r"unset\s+HISTFILE",
                "MEDIUM: Attempt to disable shell history (anti-forensics)",
            ),
            (r"mv\s+.*\s+/dev/null", "MEDIUM: Deletion by moving to null device"),
        ]

        for pattern, warning in risky_patterns:
            if re.search(pattern, command):
                return "HIGH", warning

        return "LOW", "No obvious security risks detected in command."

    def validate_shell_script(self, script_content: str) -> list[str]:
        """Analyzes shell scripts for common pitfalls and security bugs."""
        findings = []

        # Unquoted variable expansion
        if re.search(r"\$[a-zA-Z_][a-zA-Z0-9_]*[^\"']", script_content):
            findings.append("SC2086: Unquoted variable expansion. Prone to word splitting and globbing.")

        # Backticks vs $(...)
        if re.search(r"`.*`", script_content):
            findings.append("SC2006: Use of legacy backticks for command substitution. Use $(...) instead.")

        # Useless cat
        if re.search(r"cat\s+.*\s*\|\s*grep", script_content):
            findings.append("SC2002: Useless use of cat. Grep can read files directly.")

        # POSIX compatibility
        if "#!/bin/sh" in script_content and "[[" in script_content:
            findings.append("SC2039: [[ .. ]] is a bash/zsh extension. Use [ .. ] for standard POSIX sh.")

        return findings
