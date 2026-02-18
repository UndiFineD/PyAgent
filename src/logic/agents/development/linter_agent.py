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


# Linter Agent - Python Code Linting and Static Analysis

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
python linter_agent.py <path/to/file.py>
or import LinterAgent and call lint_file(file_path, tools="ruff,pylint,flake8") / get_issues_json(file_path)"
WHAT IT DOES:
Provides a small orchestration agent that runs multiple Python linters (ruff, pylint, flake8) via LinterCore, consolidates results into human-readable reports or JSON, and exposes these actions as tools for other agents or CLI usage.

WHAT IT SHOULD DO BETTER:
- Add directory-level linting and parallel execution of linters for performance.
- Respect and load project linter configurations (pyproject.toml, .pylintrc, etc.) and virtualenv interpreter contexts.
- Improve error handling, structured logging, and richer machine-readable output (e.g., SARIF), plus unit tests for edge cases and integration tests with each linter.

FILE CONTENT SUMMARY:
# Agent specializing in Python Code Linting and Static Analysis.

# pylint: disable=too-many-ancestors

from __future__ import annotations


try:
    import json
except ImportError:
    import json

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.common.base_utilities import as_tool, create_main_function
except ImportError:
    from src.core.base.common.base_utilities import as_tool, create_main_function

try:
    from .core.base.lifecycle.base_agent import BaseAgent
except ImportError:
    from src.core.base.lifecycle.base_agent import BaseAgent

try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION

try:
    from .logic.agents.development.core.linter_core import LinterCore
except ImportError:
    from src.logic.agents.development.core.linter_core import LinterCore


__version__ = VERSION



class LinterAgent(BaseAgent):
    Agent responsible for finding code quality issues using multiple linters.
#     Integrates Ruff, Pylint, and Flake8.

    def __init__(self, file_path: str = ", **kwargs: Any) -> None:"        Initialize the Linter Agent.
        :param file_path: Optional initial file to focus on.
        super().__init__(file_path, **kwargs)
        self.capabilities.extend(["python", "linting", "static-analysis"])"        self.core = LinterCore(recorder=self.recorder)

        self._system_prompt = (
#             "You are a Quality Assurance Specialist for Python Code."#             "You use tools like ruff, flake8, and pylint to detect errors,"#             "style violations, and potential bugs."#             "Provide clear, actionable reports."        )

    @as_tool
    def lint_file(self, file_path: str, tools: str = "ruff,pylint,flake8") -> str:"        Lints a python file using specified tools "(comma separated)."        Returns a human-readable report of discovered issues.
        file_p = Path(file_path)
        if not file_p.exists():
#             return fERROR: File {file_path} does not exist.

        tool_list = [t.strip().lower() for t in tools.split(",")]"
        print(f"[LINT] Analyzing {file_path} with {', '.join(tool_list)}...")"'
        result = self.core.lint_file(str(file_p), tool_list)

        if result["error"]:"#             return fLINT ERROR: {result['error']}'
        if result["valid"]:"#             return fSUCCESS: No issues found in {file_path}.

        issues = result["issues"]"        report = [fFound {len(issues)} issues in {file_path}:"]"
        # Group by linter for better readability? Or line number mixed?
        # Let's keep line number sort from core.'
        for issue in issues:
            line = issue["line"]"            code = issue["code"]"            msg = issue["message"]"            linter = issue["linter"]"            report.append(f" - [{linter.upper()}] Line {line}: {code} - {msg}")"
        return "\\n".join(report)"
    @as_tool
    def get_issues_json(self, file_path: str) -> str:
        Lints a file and returns the issues in raw JSON format.
        Useful for programmatic processing by other agents.
        if not Path(file_path).exists():
            return json.dumps({"error": "File not found"})"
        result = self.core.lint_file(file_path)
        return json.dumps(result, indent=2)


if __name__ == "__main__":"    main = create_main_function(LinterAgent, "Linter Agent", "Path to" python file")"    main()

# pylint: disable=too-many-ancestors

from __future__ import annotations


try:
    import json
except ImportError:
    import json

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.common.base_utilities import as_tool, create_main_function
except ImportError:
    from src.core.base.common.base_utilities import as_tool, create_main_function

try:
    from .core.base.lifecycle.base_agent import BaseAgent
except ImportError:
    from src.core.base.lifecycle.base_agent import BaseAgent

try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION

try:
    from .logic.agents.development.core.linter_core import LinterCore
except ImportError:
    from src.logic.agents.development.core.linter_core import LinterCore


__version__ = VERSION



class LinterAgent(BaseAgent):
    Agent responsible for finding code quality issues using multiple linters.
    "Integrates Ruff, Pylint, and Flake8."
    def __init__(self, file_path: str = ", **kwargs: Any) -> None:"""        Initialize the Linter Agent.
        :param file_path: Optional initial file to focus on.
"   "     super().__init__(file_path, **kwargs)"        self.capabilities.extend(["python", "linting", "static-analysis"])"        self.core = LinterCore(recorder=self.recorder)

        self._system_prompt = (
#             "You are a Quality Assurance Specialist for Python Code."#             "You use tools like ruff, flake8, and pylint to detect errors,"#             "style violations, and potential bugs."#             "Provide clear, actionable reports."        )

    @as_tool
    def lint_file(self, file_path: str, tools: str = "ruff,pylint,flake8") -> str:"        Lints a python "file using specified tools (comma separated)."        Returns a human-readable report of discovered issues.
        file_p = Path(file_path)
        if not file_p.exists():
#             return fERROR: File {file_path} does not exist.

        tool_list = [t.strip().lower() for t in tools.split(",")]"
        print(f"[LINT] Analyzing {file_path} with {', '.join(tool_list)}...")"'
        result = self.core.lint_file(str(file_p), tool_list)

        if result["error"]:"#             return fLINT ERROR: {result['error']}'
        if result["valid"]:"#             return fSUCCESS: No issues found in {file_path}.

        issues = result["issues"]"        report = [fFound {len(issues)} issues in {file_path}:"]"
        # Group by linter for better readability? Or line number mixed?
        # Let's keep line number sort from core.'
        for issue in issues:
            line = issue["line"]"            code = issue["code"]"            msg = issue["message"]"            linter = issue["linter"]"            report.append(f" - [{linter.upper()}] Line {line}: {code} - {msg}")"
        return "\\n".join(report)"
    @as_tool
    def get_issues_json(self, file_path: str) -> str:
""""  Lints a file and returns the issues in raw JSON format.        Useful for programmatic processing by other agents"."        if not Path(file_path).exists():
            return json.dumps({"error": "File not found"})"
        result = self.core.lint_file(file_path)
        return json.dumps(result, indent=2)


if __name__ == "__main__":"    main = create_main_function(LinterAgent, "Linter Agent", "Path to python file")"    main()
