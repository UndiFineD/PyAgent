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


"""Agent specializing in code quality, linting, and style enforcement."""

from __future__ import annotations

import subprocess

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class LintingAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """Ensures code adheres to quality standards by running linters."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Linting Agent. "
            "Your role is to ensure the codebase is clean, readable, and free of syntax errors. "
            "You use tools like flake8 and mypy to catch issues before they reach production."
        )

    def _get_default_content(self) -> str:
        return "# Code Quality Report\n\n## Summary\nAll clear.\n"

    def run_flake8(self, target_path: str) -> str:
        """Runs flake8 on the specified path."""
        try:
            # We use --max-line-length=120 and ignore some common ones
            result = subprocess.run(
                ["flake8", "--max-line-length=120", "--ignore=E203,W503", target_path],
                capture_output=True,
                text=True,
                check=False,
            )
            # Phase 108: Record linting result
            self._record(
                f"flake8 {target_path}",
                f"RC={result.returncode}\n{result.stdout[:500]}",
                provider="Shell",
                model="flake8",
            )

            if not result.stdout:
                return "Γ£à No linting issues found by flake8."
            return f"### Flake8 Issues\n```plaintext\n{result.stdout}\n```"
        except FileNotFoundError:
            return "Γ¥î flake8 not installed in the current environment."
        except (subprocess.SubprocessError, RuntimeError) as e:
            return f"Γ¥î Error running flake8: {e}"

    def run_mypy(self, target_path: str) -> str:
        """Runs mypy type checking."""
        try:
            result = subprocess.run(
                ["mypy", "--ignore-missing-imports", target_path],
                capture_output=True,
                text=True,
                check=False,
            )
            if "Success: no issues found" in result.stdout:
                return "Γ£à No type issues found by mypy."

            return f"### Mypy Issues\n```plaintext\n{result.stdout}\n```"
        except FileNotFoundError:
            return "Γ¥î mypy not installed in the current environment."
        except (subprocess.SubprocessError, RuntimeError) as e:
            return f"Γ¥î Error running mypy: {e}"

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Perform a quality audit on a file or directory."""
        # prompt is expected to be a path

        path = target_file if target_file else (prompt if prompt else ".")
        flake8_res = self.run_flake8(path)
        mypy_res = self.run_mypy(path)

        return f"## Quality Audit for: {path}\n\n{flake8_res}\n\n{mypy_res}"


if __name__ == "__main__":
    main = create_main_function(LintingAgent, "Linting Agent", "Path to audit")
    main()
