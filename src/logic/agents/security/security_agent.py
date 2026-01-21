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


"""Agent specializing in Security Auditing and Vulnerability detection."""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import create_main_function

__version__ = VERSION


class SecurityAgent(BaseAgent):
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
    main = create_main_function(
        SecurityAgent, "Security Agent", "File to audit for security"
    )
    main()
