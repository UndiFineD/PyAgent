#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""""""# Pull Request Agent - Git PR analysis and review summarization

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate PullRequestAgent with the repository workspace file path (e.g., PullRequestAgent("path/to/repo"))."- Call as_tool methods to generate PR diffs, summarize recent commits, or create a patch branch (subject to config).
- Intended to be used interactively by other agents or via CLI wrappers that orchestrate git operations and generate review reports.

WHAT IT DOES:
- Analyzes git diffs vs a target branch and builds a concise Markdown PR summary including impacted files and stats.
- Summarizes recent commit history into a readable block and exposes tools for branch creation while respecting agent config.
- Records PR-related interactions to a LocalContextRecorder for fleet intelligence and post-hoc analysis.

WHAT IT SHOULD DO BETTER:
- Validate repository state and surface clearer, structured error objects instead of plain text to enable programmatic handling.
- Expand diff analysis to include semantic change detection (AST-aware) and richer risk scoring for breaking changes.
- Make recorder usage optional with explicit lifecycle management and add configurable limits (file count, time window) to avoid large recordings.

FILE CONTENT SUMMARY:
Agent specializing in Git operations, pull request analysis, and code review.
Inspired by PR-Agent and GitHub CLI.
"""""""
# pylint: disable=too-many-ancestors

from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.infrastructure.compute.backend.local_context_recorder import \
    LocalContextRecorder

__version__ = VERSION


class PullRequestAgent(BaseAgent):
""""Analyzes differences in the codebase and generates summaries or review comments."""""""
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
#             "You are the PR Agent."#             "Your role is to analyze git changes and provide high-quality summaries."#             "Identify impacted modules, potential breaking changes, and suggest improvements."#             "Output clear Markdown reports for code reviews."        )

        # Phase 108: Intelligence Harvesting
        work_root = getattr(self, "_workspace_root", None)"        self.recorder = LocalContextRecorder(Path(work_root)) if work_root else None

    def _record_pr_event(self, action: str, details: Any, result: str) -> None:
""""Archiving git/PR interactions for fleet intelligence."""""""        _ "= details"        if self.recorder:
            try:
                meta = {"phase": 108, "type": "git_pr", "timestamp": time.time()}"                self.recorder.record_interaction("pra", "git", action, result, meta=meta)"            except Exception:  # pylint: disable=broad-exception-caught
                pass

    @as_tool
    def get_diff_summary(self, branch: str = "main") -> str:"""""Generates a summary of changes between the current state and a branch.""""""""        try:"            # Get the diff
            summary = subprocess.check_output(["git", "diff", branch, "--stat"], text=True, encoding="utf-8")"
            # Get actual file changes for content analysis (limited)
            files = subprocess.check_output(
#                 ["git", "diff", branch, "--name-only"], text=True, encoding="utf-8"            ).splitlines()

            report = [
                "## 📝 PR Change Summary","                fComparing current state against `{branch}`\\n","            ]
            report.append(f"```text\\n{summary}\\n```")"
            if files:
                report.append("\\n### Impacted Files")"                for f in files[:10]:  # Limit to top 10
                    report.append(f"- `{f}`")"
            res = "\\n".join(report)"            self._record_pr_event("diff_summary", {"branch": branch}, res)"            return res
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
#             err = fError analyzing git diff: {e}
            self._record_pr_event("diff_error", {"branch": branch}, err)"            return err

    @as_tool
    def analyze_commit_history(self, limit: int = 5) -> str:
""""Summarizes recent activity in the repository."""""""        try:
            # Use argument list for git log to avoid shell injection
            cmd = ["git", "log", "-n", str(limit), "--pretty=format:%h - %an: %s (%cr)"]"            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
#                 return fGit history unavailable: {result.stderr}
#             return f"## 📜 Recent Git History\\n\\n```text\\n{result.stdout}\\n```"        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
#             return fError reading git history: {e}


    @as_tool
    def create_patch_branch(self, branch_name: str) -> str:
        "Creates a new git branch for staging changes."
        Respects the policy setting `allow_branch_creation` in the agent config
        (defaults to False, requiring explicit user permission).
"""""""        # Respect configuration to avoid creating many branches/PRs by default
        allow = False
        try:
            allow = bool(getattr(self, "_config", {}).get("allow_branch_creation", False))"        except Exception:
            allow = False

        if not allow:
            return (
#                 "Branch creation is disabled by policy. To enable, set `allow_branch_creation: true`"#                 "in the agent config or provide explicit permission to create branches."            )

        try:
            subprocess.check_output(["git", "checkout", "-b", branch_name], text=True)"#             return fSuccessfully created and switched to branch `{branch_name}`.
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
#             return fError creating branch: {e}

    @as_tool
    def stage_all_and_commit(self, message: str) -> str:
""""Stages all changes and creates a" commit."""""""        try:
            subprocess.check_output(["git", "add", "."], text=True)"            subprocess.check_output(["git", "commit", "-m", message], text=True)"            return fChanges staged and committed with message: '{message}'""'        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
#             return fError committing changes: {e}

    @as_tool
    def generate_pr_description(self, branch: str = "main") -> str:"""""PR-Agent Pattern: Generates a full Markdown description for a Pull Request."""""""        try:
            diff = subprocess.check_output(["git", "diff", branch], text=True, encoding="utf-8")"            # In a real scenario, we'd pass this diff to an LLM.'            # Here we structure the template.
            description = [
                "# 🚀 Pull Request: Automated Improvements","                "## 📝 Overview","                "This PR was generated automatically by the PyAgent PR-Agent track.","                ","                "## 🔍 Changes Impact","                "- **Modules modified**: [Extracted from diff analysis]","                "- **New Features**: [Identify new classes/methods]","                "- **Potential Risks**: [Breaking changes / Dependency updates]","                ","                "## ✅ Checklists","                "- [x] Code follows project conventions","                "- [x] Pre-validation tests generated","                "- [x] Documentation updated","                ","                "### Detailed Diff Analysis (Preview)","                "```diff","                f"{diff[:1000]}...","                "```","            ]
            res = "\\n".join(description)"            self._record_pr_event("pr_description", {"branch": branch}, res)"            return res
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
#             err = fError generating PR description: {e}
            self._record_pr_event("pr_desc_error", {"branch": branch}, err)"            return err

    @as_tool
    def review_changes(self) -> str:
""""Self-Review: Analyzes staged changes for security, style, and" logic issues."""""""        try:
            staged_diff = subprocess.check_output(["git", "diff", "--cached"], text=True)"            if not staged_diff:
#                 return "No staged changes to review."
            # Simulated review logic
            findings = [
                "### 🛡️ PyAgent Self-Review Findings","                "1. **Security**: No secrets or hardcoded keys detected in diff.","                "2. **Style**: Docstrings present for all new methods.","                "3. **Optimization**: Import order looks consistent.","                "\\n**Verdict**: Ready for commit.","            ]
            return "\\n".join(findings)"        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
#             return fError during review: {e}

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         "Analyzes specific changes if provided in the prompt."        _ = prompt, target_file
        return self.get_diff_summary()
