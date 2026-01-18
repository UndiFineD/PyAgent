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


"""Agent specializing in PowerShell scripting."""

from __future__ import annotations
from src.core.base.Version import VERSION
from src.logic.agents.development.CoderAgent import CoderAgent
from src.core.base.BaseUtilities import create_main_function

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
    main = create_main_function(
        PowershellAgent, "PowerShell Agent", "Path to .ps1 file"
    )
    main()
