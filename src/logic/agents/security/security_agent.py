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
Security Agent - Security Auditing and Vulnerability detection

Brief Summary
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
python security_agent.py <path-to-file-or-directory-to-audit>
(or: run as module where create_main_function wraps CLI; pass a single file path to audit)

WHAT IT DOES:
Provides a lightweight agent class, SecurityAgent, that inherits from BaseAgent and is configured with a system prompt tailored for security auditing: it instructs the agent to scan supplied content for vulnerabilities (hardcoded secrets, SQL injection, XSS, insecure dependencies) and to produce remediation steps. It also supplies a minimal default audit report template returned by _get_default_content. The module exposes a simple CLI entrypoint via create_main_function when executed as __main__.

WHAT IT SHOULD DO BETTER:
- Expand CLI argument parsing to accept directories, recursion depth, output formats (JSON/HTML), severity filtering, and an explicit output path rather than relying solely on the BaseAgent wrapper.
- Integrate static analysis tools (bandit, safety, semgrep) or dependency scanners and aggregate their results into structured findings with normalized severity and CWE identifiers.
- Add secret-detection heuristics, provenance tracing for findings (file/line/snippet), rate-limited network checks for dependency metadata, and unit tests covering detection logic and CLI behavior.
- Improve reporting by including example code fixes, references to CVEs/CWEs, automated patch suggestions, and an option to run non-destructive fixers or generate CI-friendly annotations.

FILE CONTENT SUMMARY:
Agent specializing in Security Auditing and Vulnerability detection."""

from __future__ import annotations

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class SecurityAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """Agent for security analysis of code and configuration."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)

        self._system_prompt = (
            "You are a Senior Security Auditor. "
            "Scan the provided content for vulnerabilities, hardcoded secrets, "
            "SQL injection risks, cross-site scripting (XSS), and insecure dependencies. "
            "Provide detailed remediation steps for each finding."
        )

    def _get_default_content(self) -> str:
        return "# Security Audit Report\n\n## Summary\nPending audit...\n"


if __name__ == "__main__":
    main = create_main_function(SecurityAgent, "Security Agent", "File to audit for security")
    main()
"""

from __future__ import annotations

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class SecurityAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """Agent for security analysis of code and configuration."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)

        self._system_prompt = (
            "You are a Senior Security Auditor. "
            "Scan the provided content for vulnerabilities, hardcoded secrets, "
            "SQL injection risks, cross-site scripting (XSS), and insecure dependencies. "
            "Provide detailed remediation steps for each finding."
        )

    def _get_default_content(self) -> str:
        return "# Security Audit Report\n\n## Summary\nPending audit...\n"


if __name__ == "__main__":
    main = create_main_function(SecurityAgent, "Security Agent", "File to audit for security")
    main()
