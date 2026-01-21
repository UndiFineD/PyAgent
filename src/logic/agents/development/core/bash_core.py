"""
Core logic for Bash script analysis (Phase 175).
Integrates shellcheck for linting generated scripts.
Optimized for eventual Rust migration (Phase 3).
"""

from __future__ import annotations

import json
import os
import subprocess
from typing import TypedDict, Optional, Any

from src.core.base.common.base_interfaces import ContextRecorderInterface


class ShellCheckIssue(TypedDict):
    """Represents a single issue found by shellcheck."""

    file: str

    line: int
    endLine: int
    column: int
    endColumn: int

    level: str
    code: int
    message: str
    fix: Any


class BashLintResult(TypedDict):
    """Result of a bash script linting session."""

    valid: bool
    issues: list[ShellCheckIssue]
    error: Optional[str]


class BashCore:
    """Core logic for Bash script analysis and linting."""

    @staticmethod
    def lint_script(
        script_path: str, recorder: ContextRecorderInterface | None = None
    ) -> BashLintResult:
        """
        Runs shellcheck on a bash script.
        """
        if not os.path.exists(script_path):
            result: BashLintResult = {
                "valid": False,
                "issues": [],
                "error": "File not found",
            }
            if recorder:
                recorder.record_interaction(
                    "bash", "shellcheck", script_path, "file-not-found"
                )
            return result

        try:
            # -f json for machine readable output
            process = subprocess.run(
                ["shellcheck", "-f", "json", script_path],
                capture_output=True,
                text=True,
                check=False,
            )

            issues: list[ShellCheckIssue] = []
            if process.stdout:
                try:
                    issues = json.loads(process.stdout)
                except json.JSONDecodeError:
                    return {
                        "valid": False,
                        "issues": [],
                        "error": "Failed to parse shellcheck output",
                    }

            valid = not issues
            findings: BashLintResult = {"issues": issues, "valid": valid, "error": None}

            if recorder:
                recorder.record_interaction(
                    provider="bash",
                    model="shellcheck",
                    prompt=script_path,
                    result=str(findings)[:2000],
                )

            return findings

        except FileNotFoundError:
            return {
                "valid": False,
                "issues": [],
                "error": "shellcheck not found. Please install it.",
            }
        except Exception as e:
            error_msg = str(e)
            if recorder:
                recorder.record_interaction(
                    provider="bash",
                    model="shellcheck",
                    prompt=script_path,
                    result=f"Error: {error_msg}",
                )
            return {"valid": False, "issues": [], "error": error_msg}

    @staticmethod
    def wrap_with_safety_flags(content: str) -> str:
        """
        Ensures script starts with common safety flags (`set -euo pipefail`) if not present.
        """
        try:
            import rust_core

            return rust_core.ensure_safety_flags_rust(content)  # type: ignore[attr-defined]
        except (ImportError, AttributeError):
            pass

        header = "set -euo pipefail"

        # Simple heuristic: if strict mode is not detected, prepend it.
        if "set -euo pipefail" in content:
            return content

        lines = content.splitlines()
        if lines and lines[0].startswith("#!"):
            # Insert after shebang
            lines.insert(1, "")
            lines.insert(2, header)
            return "\n".join(lines)

        return f"#!/bin/bash\n{header}\n\n{content}"
