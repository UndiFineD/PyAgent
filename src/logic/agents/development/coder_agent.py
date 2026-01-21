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


"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from src.core.base.types.code_language import CodeLanguage
from src.core.base.types.code_metrics import CodeMetrics
from src.core.base.types.code_smell import CodeSmell
from src.core.base.types.quality_score import QualityScore
from src.core.base.types.refactoring_pattern import RefactoringPattern
from src.core.base.types.style_rule import StyleRule
from src.logic.agents.development.coder_core import CoderCore, DEFAULT_PYTHON_STYLE_RULES
from src.core.base.base_agent import BaseAgent
from src.logic.agents.development.mixins.agent.agent_language_mixin import AgentLanguageMixin
from src.logic.agents.development.mixins.agent.agent_style_mixin import AgentStyleMixin
from src.logic.agents.development.mixins.agent.agent_metrics_mixin import AgentMetricsMixin
from src.logic.agents.development.mixins.agent.agent_refactor_mixin import AgentRefactorMixin
from pathlib import Path
import logging

__version__ = VERSION


class CoderAgent(
    BaseAgent, AgentLanguageMixin, AgentStyleMixin, AgentMetricsMixin, AgentRefactorMixin
):
    """Updates code files using AI assistance.

    Invariants:
    - self.file_path must point to a valid file path.

    - Supports Python files (.py) with syntax validation.
    - Supports multi - language code improvements.
    """

    # Language extension mappings
    LANGUAGE_EXTENSIONS: dict[str, CodeLanguage] = {
        ".py": CodeLanguage.PYTHON,
        ".js": CodeLanguage.JAVASCRIPT,
        ".ts": CodeLanguage.TYPESCRIPT,
        ".java": CodeLanguage.JAVA,
        ".cpp": CodeLanguage.CPP,
        ".cc": CodeLanguage.CPP,
        ".cxx": CodeLanguage.CPP,
        ".go": CodeLanguage.GO,
        ".rs": CodeLanguage.RUST,
        ".rb": CodeLanguage.RUBY,
    }

    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self._language = self._detect_language()
        super().__init__(file_path)
        self.capabilities.extend(["python", "javascript", "code-refactor"])  # Phase 241

        # New: Delegate core logic to CoderCore (Rust-ready component)
        self.core = CoderCore(self._language)

        # Create copies of style rules to avoid cross-instance state leakage
        self._style_rules: list[StyleRule] = [
            StyleRule(
                name=r.name,
                pattern=r.pattern,
                message=r.message,
                severity=r.severity,
                enabled=r.enabled,
                language=r.language,
                auto_fix=r.auto_fix,
            )
            for r in DEFAULT_PYTHON_STYLE_RULES
        ]
        self._metrics: CodeMetrics | None = None
        self._quality_score: QualityScore | None = None
        self._code_smells: list[CodeSmell] = []
        self._refactoring_patterns: list[RefactoringPattern] = []
        self._duplicate_hashes: dict[str, list[int]] = {}

    def _detect_language(self) -> CodeLanguage:
        """Detect the programming language from file extension."""
        ext = self.file_path.suffix.lower()
        return self.LANGUAGE_EXTENSIONS.get(ext, CodeLanguage.UNKNOWN)

    def detect_language(self) -> CodeLanguage:
        """Public wrapper to detect and return the file language.

        Returns:
            The detected CodeLanguage based on file extension.
        """
        self._language = self._detect_language()
        self.core.language = self._language  # Sync core
        return self._language

    # ========== Documentation Generation ==========
    def generate_documentation(self, content: str | None = None) -> str:
        """Generate documentation from code."""
        if content is None:
            content = self.current_content or self.previous_content or ""
        return self.core.generate_documentation(content)

    # ========== Core Methods ==========
    def _get_default_content(self) -> str:
        """Return default content for new code files."""
        return "# Code file\n\n# Add code here\n"

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return (
            "# AI Improvement Unavailable\n"
            "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
            "# Original code preserved below:\n\n"
        )

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Use AI to improve the code with specific coding suggestions."""
        actual_path = Path(target_file) if target_file else self.file_path
        logging.info(f"Improving content for {actual_path}")
        # Call base implementation directly to use AI backend
        new_content = await super().improve_content(prompt, target_file=target_file)
        # Validate syntax
        if not self._validate_syntax(new_content):
            logging.error("Generated code failed syntax validation. Reverting.")
            self.current_content = self.previous_content
            return self.previous_content
        logging.debug("Syntax validation passed")
        # Validate style (flake8)
        if not self._validate_flake8(new_content):
            logging.warning(
                "Generated code failed style validation (flake8). Proceeding anyway."
            )
        else:
            logging.debug("Style validation passed")
        return new_content
