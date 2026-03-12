#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/coder/CoderAgent.description.md

# CoderAgent

**File**: `src\classes\coder\CoderAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 145  
**Complexity**: 6 (moderate)

## Overview

Auto-extracted class from agent_coder.py

## Classes (1)

### `CoderAgent`

**Inherits from**: BaseAgent, AgentLanguageMixin, AgentStyleMixin, AgentMetricsMixin, AgentRefactorMixin

Updates code files using AI assistance.

Invariants:
- self.file_path must point to a valid file path.

- Supports Python files (.py) with syntax validation.
- Supports multi - language code improvements.

**Methods** (6):
- `__init__(self, file_path)`
- `_detect_language(self)`
- `detect_language(self)`
- `generate_documentation(self, content)`
- `_get_default_content(self)`
- `_get_fallback_response(self)`

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `logging`
- `mixins.agent.AgentLanguageMixin.AgentLanguageMixin`
- `mixins.agent.AgentMetricsMixin.AgentMetricsMixin`
- `mixins.agent.AgentRefactorMixin.AgentRefactorMixin`
- `mixins.agent.AgentStyleMixin.AgentStyleMixin`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.Version.VERSION`
- `src.core.base.types.CodeLanguage.CodeLanguage`
- `src.core.base.types.CodeMetrics.CodeMetrics`
- `src.core.base.types.CodeSmell.CodeSmell`
- `src.core.base.types.QualityScore.QualityScore`
- `src.core.base.types.RefactoringPattern.RefactoringPattern`
- `src.core.base.types.StyleRule.StyleRule`
- ... and 2 more

---
*Auto-generated documentation*
## Source: src-old/classes/coder/CoderAgent.improvements.md

# Improvements for CoderAgent

**File**: `src\classes\coder\CoderAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 145 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CoderAgent_test.py` with pytest tests

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


"""Auto-extracted class from agent_coder.py"""

import logging
from pathlib import Path

from src.core.base.BaseAgent import BaseAgent
from src.core.base.types.CodeLanguage import CodeLanguage
from src.core.base.types.CodeMetrics import CodeMetrics
from src.core.base.types.CodeSmell import CodeSmell
from src.core.base.types.QualityScore import QualityScore
from src.core.base.types.RefactoringPattern import RefactoringPattern
from src.core.base.types.StyleRule import StyleRule
from src.core.base.Version import VERSION
from src.logic.agents.development.CoderCore import DEFAULT_PYTHON_STYLE_RULES, CoderCore

from .mixins.agent.AgentLanguageMixin import AgentLanguageMixin
from .mixins.agent.AgentMetricsMixin import AgentMetricsMixin
from .mixins.agent.AgentRefactorMixin import AgentRefactorMixin
from .mixins.agent.AgentStyleMixin import AgentStyleMixin

__version__ = VERSION


class CoderAgent(
    BaseAgent,
    AgentLanguageMixin,
    AgentStyleMixin,
    AgentMetricsMixin,
    AgentRefactorMixin,
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

    async def improve_content(self, prompt: str) -> str:
        """Use AI to improve the code with specific coding suggestions."""
        logging.info(f"Improving content for {self.file_path}")
        # Call base implementation directly to use AI backend
        new_content = await super().improve_content(prompt)
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
