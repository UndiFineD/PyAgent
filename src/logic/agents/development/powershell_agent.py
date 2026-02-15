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
powershell_agent.py - PowerShell Agent (PowerShell scripting specialization)

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- As a module: instantiate PowershellAgent with the path to a .ps1 file and call its orchestration methods via the CoderAgent interface.
- From CLI: python powershell_agent.py "path\to\script.ps1" (the module provides a create_main_function entrypoint for simple invocation).
- Intended for integration into the PyAgent swarm where agents are orchestrated by higher-level controllers.

WHAT IT DOES:
Provides a minimal, focused CoderAgent subclass specialized for authoring and manipulating PowerShell scripts. It sets language-specific metadata (_language = "powershell") and a tailored system prompt that instructs the underlying LLM to prefer idiomatic PowerShell patterns (Verb-Noun naming, Try/Catch error handling, pipeline usage). It also supplies a sensible default script template when a new file is created.

WHAT IT SHOULD DO BETTER:
- Expand argument parsing and CLI feedback (validate file path, allow creating new scripts, expose verbosity and dry-run flags).
- Implement richer PowerShell-specific linting and formatting hooks (invoke PSScriptAnalyzer or similar) before writing changes.
- Improve test coverage and add unit tests for content generation, system_prompt behaviours, and integration with StateTransaction and CascadeContext per project conventions.
- Provide async orchestration consistent with project asyncio conventions and ensure transactional file writes via StateTransaction.

FILE CONTENT SUMMARY:
Agent specializing in PowerShell scripting."""

# pylint: disable=too-many-ancestors

from __future__ import annotations

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.development.coder_agent import CoderAgent

__version__ = VERSION


class PowershellAgent(CoderAgent):
    """Agent for PowerShell scripts."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)

        self._language = "powershell"
        self._system_prompt = (
            "You are an Expert PowerShell Scripter. "
            "Focus on idiomatic PowerShell, proper naming conventions (Verb-Noun), "
            "error handling (Try/Catch), and pipeline efficiency."
        )

    def _get_default_content(self) -> str:
        return "# PowerShell Script\nWrite-Host 'Hello World'\n"


if __name__ == "__main__":
    main = create_main_function(PowershellAgent, "PowerShell Agent", "Path to .ps1 file")
    main()
"""

# pylint: disable=too-many-ancestors

from __future__ import annotations

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.development.coder_agent import CoderAgent

__version__ = VERSION


class PowershellAgent(CoderAgent):
    """Agent for PowerShell scripts."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)

        self._language = "powershell"
        self._system_prompt = (
            "You are an Expert PowerShell Scripter. "
            "Focus on idiomatic PowerShell, proper naming conventions (Verb-Noun), "
            "error handling (Try/Catch), and pipeline efficiency."
        )

    def _get_default_content(self) -> str:
        return "# PowerShell Script\nWrite-Host 'Hello World'\n"


if __name__ == "__main__":
    main = create_main_function(PowershellAgent, "PowerShell Agent", "Path to .ps1 file")
    main()
