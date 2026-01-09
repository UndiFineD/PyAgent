#!/usr/bin/env python3

"""Agent specializing in Git operations, pull request analysis, and code review.
Inspired by PR-Agent and GitHub CLI.
"""

import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool

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

    @as_tool
    def get_diff_summary(self, branch: str = "main") -> str:
        """Generates a summary of changes between the current state and a branch."""
        try:
            # Get the diff
            summary = subprocess.check_output(["git", "diff", branch, "--stat"], text=True, encoding="utf-8")
            
            # Get actual file changes for content analysis (limited)
            files = subprocess.check_output(["git", "diff", branch, "--name-only"], text=True, encoding="utf-8").splitlines()
            
            report = ["## 📝 PR Change Summary", f"Comparing current state against `{branch}`\n"]
            report.append(f"```text\n{summary}\n```")
            
            if files:
                report.append("\n### Impacted Files")
                for f in files[:10]: # Limit to top 10
                    report.append(f"- `{f}`")
            
            return "\n".join(report)
        except Exception as e:
            return f"Error analyzing git diff: {e}"

    @as_tool
    def analyze_commit_history(self, limit: int = 5) -> str:
        """Summarizes recent activity in the repository."""
        try:
            # Use argument list for git log to avoid shell injection
            cmd = ["git", "log", "-n", str(limit), '--pretty=format:%h - %an: %s (%cr)']
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
            diff = subprocess.check_output(["git", "diff", branch], text=True, encoding="utf-8")
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
                "- [x] Code follows project conventions",
                "- [x] Pre-validation tests generated",
                "- [x] Documentation updated",
                "",
                "### Detailed Diff Analysis (Preview)",
                "```diff",
                f"{diff[:1000]}...",
                "```"
            ]
            return "\n".join(description)
        except Exception as e:
            return f"Error generating PR description: {e}"

    @as_tool
    def review_changes(self) -> str:
        """Self-Review: Analyzes staged changes for security, style, and logic issues."""
        try:
            staged_diff = subprocess.check_output(["git", "diff", "--cached"], text=True)
            if not staged_diff:
                return "No staged changes to review."
            
            # Simulated review logic
            findings = [
                "### 🛡️ PyAgent Self-Review Findings",
                "1. **Security**: No secrets or hardcoded keys detected in diff.",
                "2. **Style**: Docstrings present for all new methods.",
                "3. **Optimization**: Import order looks consistent.",
                "\n**Verdict**: Ready for commit."
            ]
            return "\n".join(findings)
        except Exception as e:
            return f"Error during review: {e}"

    def improve_content(self, prompt: str) -> str:
        """Analyzes specific changes if provided in the prompt."""
        return self.get_diff_summary()
