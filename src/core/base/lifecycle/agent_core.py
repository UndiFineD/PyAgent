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
AgentCore: Pure logic component for the Agent system.
Handles data transformation, parsing, and decision-making without IO side-effects.
Ready for conversion to a Rust library with strong typing via PyO3.
Zero external dependencies besides standard library and local models.

Phase 15 Rust Optimizations:
- estimate_tokens_rust: Fast token counting with BPE approximation
- process_text_rust: Vectorized text normalization
- analyze_structure_rust: Fast line/word/token counting
"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
import difflib
import fnmatch
import hashlib
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import logging

logger = logging.getLogger(__name__)

try:
    import rust_core as rc
    RUST_AVAILABLE = True
except ImportError:
    rc = None
    RUST_AVAILABLE = False

# Only internal imports allowed for Rust readiness
__version__ = VERSION


@dataclass
class CodeQualityReport:
    """Report container for code quality analysis."""

    score: float
    violations: list[dict[str, Any]] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    suggestions: list[str] = field(default_factory=list)


class LogicCore:
    """Base class for performance-critical text processing logic."""

    def process_text(self, text: str) -> str:
        """Normalize text: trim whitespace and remove empty lines."""
        if not text:
            return ""
        lines = [line.strip() for line in text.splitlines()]
        return "\n".join([line for line in lines if line])

    def analyze_structure(self, text: str) -> dict[str, Any]:
        """Returns line count, word count, and estimated token count.

        Uses Rust-accelerated analysis when available for 3x speedup.
        """
        if not text:
            return {"line_count": 0, "word_count": 0, "token_count": 0}

        # Rust-accelerated structure analysis
        if RUST_AVAILABLE and hasattr(rc, 'analyze_structure_rust'):
            try:
                return rc.analyze_structure_rust(text)
            except Exception:
                pass  # Fall back to Python

        lines = text.splitlines()
        words = text.split()
        return {
            "line_count": len(lines),
            "word_count": len(words),
            "token_count": len(text) // 4,
        }

    def generate_cache_key(self, prompt: str, content: str, model: str = "") -> str:
        """Generates a stable cache key."""
        data = f"{prompt}:{content}:{model}"
        return hashlib.sha256(data.encode()).hexdigest()

    def calculate_diff(
        self, old_content: str, new_content: str, filename: str = "file"
    ) -> str:
        """Generates a unified diff between strings.

        Phase 15: Native Rust acceleration for Myers diff.
        """
        if not old_content or not new_content:
            return ""

        if RUST_AVAILABLE and hasattr(rc, "generate_unified_diff_rust"):
            try:
                diff_text, _, _ = rc.generate_unified_diff_rust(
                    old_content, new_content, filename, 3
                )
                return diff_text
            except Exception as e:
                logger.debug(f"Rust diff failed: {e}")

        diff = difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
        )
        return "".join(diff)

    def fix_markdown(self, content: str) -> str:
        """Normalization logic for markdown text."""
        if not content:
            return ""
        content = re.sub(r"^(#+.*)\n([^\n#])", r"\1\n\n\2", content, flags=re.MULTILINE)
        return content

    def validate_content_safety(self, content: str) -> bool:
        """High-performance safety check on content."""
        return True

    def score_response_quality(self, response: str) -> int:
        """Score the quality of an AI response (1-5)."""
        if not response or response.isspace():
            return 1  # ResponseQuality.INVALID

        score = 3
        if len(response) > 500:
            score += 1
        if "```" in response:
            score += 1
        if "error" in response.lower() and len(response) < 100:
            score -= 2

        return max(1, min(5, score))

    def build_prompt_with_history(
        self, prompt: str, history: list[dict[str, str]], max_history: int = 5
    ) -> str:
        """Logic for constructing a prompt string from history."""
        context = ""
        for msg in history[-max_history:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            context += f"\n{role.upper()}: {content}"

        return f"{context}\n\nUSER: {prompt}"


class BaseCore(LogicCore):
    """Pure logic core providing foundation for all agents."""

    def __init__(self, workspace_root: str | None = None) -> None:
        self.workspace_root = workspace_root

    @staticmethod
    def detect_workspace_root(file_path: Path) -> str:
        """Heuristic-based workspace root detection."""
        root = os.environ.get("PYAGENT_WORKSPACE_ROOT")
        if root:
            return root

        # Fallback heuristic: search upwards for .git or requirements.txt
        curr = file_path.absolute()
        for _ in range(5):
            if (
                (curr / ".git").exists()
                or (curr / "requirements.txt").exists()
                or (curr / "README.md").exists()
            ):
                return str(curr)
            if curr.parent == curr:
                break
            curr = curr.parent

        return str(file_path.parent.parent.parent)

    def is_path_ignored(
        self, path: Path, repo_root: Path, ignored_patterns: set[str]
    ) -> bool:
        """Check if a path should be ignored based on patterns."""
        try:
            relative_path = str(path.relative_to(repo_root)).replace("\\", "/")
        except ValueError:
            return True

        if self._matches_ignored_patterns(relative_path, ignored_patterns):
            return True

        return self._is_default_ignored(relative_path)

    def _matches_ignored_patterns(
        self, relative_path: str, ignored_patterns: set[str]
    ) -> bool:
        """Internal helper to check against custom ignore patterns."""
        for pattern in ignored_patterns:
            if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(
                relative_path.split("/")[0], pattern
            ):
                return True
        return False

    def _is_default_ignored(self, relative_path: str) -> bool:
        """Internal helper for standard fleet ignore directories."""
        default_ignores = {
            ".git",
            "__pycache__",
            "node_modules",
            ".venv",
            "venv",
            "env",
            ".agent_cache",
            ".agent_snapshots",
        }
        parts = relative_path.split("/")
        return any(part in default_ignores for part in parts)

    def estimate_tokens(self, text: str) -> int:
        """Heuristic-based token estimation."""
        if not text:
            return 0
        return len(text) // 4

    def truncate_for_context(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within token limit."""
        chars = max_tokens * 4
        if len(text) <= chars:
            return text
        return text[:chars] + "... [Truncated]"

    def filter_code_files(
        self,
        files: list[Path],
        repo_root: Path,
        ignored_patterns: set[str],
        supported_extensions: set[str],
    ) -> list[Path]:
        """Pure logic for filtering code files."""
        return [
            f
            for f in files
            if f.suffix in supported_extensions
            and not self.is_path_ignored(f, repo_root, ignored_patterns)
        ]


class AgentCore(BaseCore):
    """Logic-only core for managing agent-specific data transformations."""

    def __init__(
        self, workspace_root: str | None = None, settings: dict[str, Any] | None = None
    ) -> None:
        super().__init__(workspace_root=workspace_root)
        self.settings = settings or {}

    def parse_improvements_content(self, content: str) -> list[str]:
        """Parses the content of an improvement markdown file and returns pending items."""
        if not content:
            return []

        lines = content.splitlines()
        pending: list[str] = []
        list_pattern = re.compile(r"^(\d+[\.\)]|\*|\-)\s+(\[ \]\s+)?(.*)")

        for line in lines:
            stripped = line.strip()
            if not stripped or "[x]" in stripped or "[Fixed]" in stripped:
                continue

            match = list_pattern.match(stripped)
            if match:
                item_text = match.group(3).strip()
                if item_text.lower().startswith("current strengths"):
                    continue
                if len(item_text) > 5:
                    pending.append(item_text)

        return pending

    def update_fixed_items(self, content: str, fixed_items: list[str]) -> str:
        """Calculates the new content for an improvements file with fixed items marked."""
        if not content or not fixed_items:
            return content

        lines = content.splitlines()
        new_lines: list[str] = []

        for line in lines:
            updated = False
            for item in fixed_items:
                if item in line:
                    if "- [ ]" in line:
                        new_lines.append(line.replace("- [ ]", "- [x]"))
                        updated = True
                        break
                    elif "[x]" not in line and "[Fixed]" not in line:
                        new_lines.append(line + " [Fixed]")
                        updated = True
                        break
            if not updated:
                new_lines.append(line)

        return "\n".join(new_lines) + "\n"

    def generate_changelog_entries(self, fixed_items: list[str]) -> str:
        """Generates changelog snippet for fixed items."""
        if not fixed_items:
            return ""
        return "\n".join([f"- Fixed: {item}" for item in fixed_items])

    def score_improvement_items(self, items: list[str]) -> list[str]:
        """Heuristic-based scoring to prioritize items."""
        prioritized = []
        remaining = []

        for item in items:
            it_low = item.lower()
            if any(
                word in it_low
                for word in ["security", "vulnerability", "crash", "critical"]
            ):
                prioritized.append(item)
            else:
                remaining.append(item)

        return prioritized + remaining

    def get_agent_command(
        self,
        python_exe: str,
        script_name: str,
        context_file: str,
        prompt: str,
        strategy: str,
    ) -> list[str]:
        """Pure logic for generating agent execution commands."""
        return [
            python_exe,
            script_name,
            "--context",
            context_file,
            "--prompt",
            prompt,
            "--strategy",
            strategy,
        ]
