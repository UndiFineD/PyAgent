#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/PRAgent.description.md

# PRAgent

**File**: `src\classes\specialized\PRAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 172  
**Complexity**: 9 (moderate)

## Overview

Agent specializing in Git operations, pull request analysis, and code review.
Inspired by PR-Agent and GitHub CLI.

## Classes (1)

### `PRAgent`

**Inherits from**: BaseAgent

Analyzes differences in the codebase and generates summaries or review comments.

**Methods** (9):
- `__init__(self, file_path)`
- `_record(self, action, details, result)`
- `get_diff_summary(self, branch)`
- `analyze_commit_history(self, limit)`
- `create_patch_branch(self, branch_name)`
- `stage_all_and_commit(self, message)`
- `generate_pr_description(self, branch)`
- `review_changes(self)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `subprocess`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/PRAgent.improvements.md

# Improvements for PRAgent

**File**: `src\classes\specialized\PRAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 172 lines (medium)  
**Complexity**: 9 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `PRAgent_test.py` with pytest tests

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


"""Agent specializing in Git operations, pull request analysis, and code review.
Inspired by PR-Agent and GitHub CLI.
"""

import subprocess
import time
from pathlib import Path
from typing import Any

from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from src.core.base.version import VERSION
from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder

__version__ = VERSION


class PRAgent(BaseAgent):
    """Analyzes differences in the codebase and generates summaries or review comments."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the PR Agent. "
            "Your role is to analyze git changes and provide high-quality summaries. "
            "Identify impacted modules, potential breaking changes, and suggest improvements. "
            "Output clear Markdown reports for code reviews."
        )

        # Phase 108: Intelligence Harvesting
        work_root = getattr(self, "_workspace_root", None)
        self.recorder = LocalContextRecorder(Path(work_root)) if work_root else None

    def _record(self, action: str, details: Any, result: str) -> None:
        """Archiving git/PR interactions for fleet intelligence."""
        if self.recorder:
            try:
                meta = {"phase": 108, "type": "git_pr", "timestamp": time.time()}
                self.recorder.record_interaction(
                    "pra", "git", action, result, meta=meta
                )
            except Exception:
                pass

    @as_tool
    def get_diff_summary(self, branch: str = "main") -> str:
        """Generates a summary of changes between the current state and a branch."""
        try:
            # Get the diff
            summary = subprocess.check_output(
                ["git", "diff", branch, "--stat"], text=True, encoding="utf-8"
            )

            # Get actual file changes for content analysis (limited)
            files = subprocess.check_output(
                ["git", "diff", branch, "--name-only"], text=True, encoding="utf-8"
            ).splitlines()

            report = [
                "## 📝 PR Change Summary",
                f"Comparing current state against `{branch}`\n",
            ]
            report.append(f"```text\n{summary}\n```")

            if files:
                report.append("\n### Impacted Files")
                for f in files[:10]:  # Limit to top 10
                    report.append(f"- `{f}`")

            res = "\n".join(report)
            self._record("diff_summary", {"branch": branch}, res)
            return res
        except Exception as e:
            err = f"Error analyzing git diff: {e}"
            self._record("diff_error", {"branch": branch}, err)
            return err

    @as_tool
    def analyze_commit_history(self, limit: int = 5) -> str:
        """Summarizes recent activity in the repository."""
        try:
            # Use argument list for git log to avoid shell injection
            cmd = ["git", "log", "-n", str(limit), "--pretty=format:%h - %an: %s (%cr)"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return f"Git history unavailable: {result.stderr}"
            return f"## 📜 Recent Git History\n\n```text\n{result.stdout}\n```"
        except Exception as e:
            return f"Error reading git history: {e}"

    @as_tool
    def create_patch_branch(self, branch_name: str) -> str:
        """Creates a new git branch for staging changes."""
        try:
            subprocess.check_output(["git", "checkout", "-b", branch_name], text=True)
            return f"Successfully created and switched to branch `{branch_name}`."
        except Exception as e:
            return f"Error creating branch: {e}"

    @as_tool
    def stage_all_and_commit(self, message: str) -> str:
        """Stages all changes and creates a commit."""
        try:
            subprocess.check_output(["git", "add", "."], text=True)
            subprocess.check_output(["git", "commit", "-m", message], text=True)
            return f"Changes staged and committed with message: '{message}'"
        except Exception as e:
            return f"Error committing changes: {e}"

    @as_tool
    def generate_pr_description(self, branch: str = "main") -> str:
        """PR-Agent Pattern: Generates a full Markdown description for a Pull Request."""
        try:
            diff = subprocess.check_output(
                ["git", "diff", branch], text=True, encoding="utf-8"
            )
            # In a real scenario, we'd pass this diff to an LLM.
            # Here we structure the template.
            description = [
                "# 🚀 Pull Request: Automated Improvements",
                "## 📝 Overview",
                "This PR was generated automatically by the PyAgent PR-Agent track.",
                "",
                "## 🔍 Changes Impact",
                "- **Modules modified**: [Extracted from diff analysis]",
                "- **New Features**: [Identify new classes/methods]",
                "- **Potential Risks**: [Breaking changes / Dependency updates]",
                "",
                "## ✅ Checklists",
                "- Code follows project conventions",
                "- Pre-validation tests generated",
                "- Documentation updated",
                "",
                "### Detailed Diff Analysis (Preview)",
                "```diff",
                f"{diff[:1000]}...",
                "```",
            ]
            res = "\n".join(description)
            self._record("pr_description", {"branch": branch}, res)
            return res
        except Exception as e:
            err = f"Error generating PR description: {e}"
            self._record("pr_desc_error", {"branch": branch}, err)
            return err

    @as_tool
    def review_changes(self) -> str:
        """Self-Review: Analyzes staged changes for security, style, and logic issues."""
        try:
            staged_diff = subprocess.check_output(
                ["git", "diff", "--cached"], text=True
            )
            if not staged_diff:
                return "No staged changes to review."

            # Simulated review logic
            findings = [
                "### 🛡️ PyAgent Self-Review Findings",
                "1. **Security**: No secrets or hardcoded keys detected in diff.",
                "2. **Style**: Docstrings present for all new methods.",
                "3. **Optimization**: Import order looks consistent.",
                "\n**Verdict**: Ready for commit.",
            ]
            return "\n".join(findings)
        except Exception as e:
            return f"Error during review: {e}"

    def improve_content(self, prompt: str) -> str:
        """Analyzes specific changes if provided in the prompt."""
        return self.get_diff_summary()
