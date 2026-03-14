#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/ContextAgent.description.md

# ContextAgent

**File**: `src\\logic\agents\\cognitive\\ContextAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 169  
**Complexity**: 7 (moderate)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `ContextAgent`

**Inherits from**: BaseAgent, ContextTemplateMixin, ContextTaggingMixin, ContextVersioningMixin, ContextValidationMixin, ContextAnnotationMixin, ContextCategorizationMixin, ContextRAGMixin

Updates code file context descriptions using AI assistance.

**Methods** (7):
- `__init__(self, file_path)`
- `route_query(self, query)`
- `_validate_file_extension(self)`
- `_derive_source_path(self)`
- `_get_default_content(self)`
- `_get_fallback_response(self)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (18):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.Version.VERSION`
- `src.logic.agents.cognitive.ContextAnnotationMixin.ContextAnnotationMixin`
- `src.logic.agents.cognitive.ContextCategorizationMixin.ContextCategorizationMixin`
- `src.logic.agents.cognitive.ContextRAGMixin.ContextRAGMixin`
- `src.logic.agents.cognitive.ContextTaggingMixin.ContextTaggingMixin`
- `src.logic.agents.cognitive.ContextTemplateMixin.ContextTemplateMixin`
- `src.logic.agents.cognitive.ContextTemplateMixin.DEFAULT_TEMPLATES`
- `src.logic.agents.cognitive.ContextValidationMixin.ContextValidationMixin`
- `src.logic.agents.cognitive.ContextValidationMixin.DEFAULT_VALIDATION_RULES`
- `src.logic.agents.cognitive.ContextVersioningMixin.ContextVersioningMixin`
- `src.logic.agents.cognitive.context.models.ContextPriority.ContextPriority`
- ... and 3 more

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/ContextAgent.improvements.md

# Improvements for ContextAgent

**File**: `src\\logic\agents\\cognitive\\ContextAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 169 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextAgent_test.py` with pytest tests

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


"""Auto-extracted class from agent_context.py"""

import logging
from pathlib import Path

from src.core.base.BaseAgent import BaseAgent
from src.core.base.Version import VERSION
from src.logic.agents.cognitive.context.models.ContextPriority import ContextPriority
from src.logic.agents.cognitive.context.models.FileCategory import FileCategory
from src.logic.agents.cognitive.ContextAnnotationMixin import ContextAnnotationMixin
from src.logic.agents.cognitive.ContextCategorizationMixin import (
    ContextCategorizationMixin,
)
from src.logic.agents.cognitive.ContextRAGMixin import ContextRAGMixin
from src.logic.agents.cognitive.ContextTaggingMixin import ContextTaggingMixin
from src.logic.agents.cognitive.ContextTemplateMixin import (
    DEFAULT_TEMPLATES,
    ContextTemplateMixin,
)
from src.logic.agents.cognitive.ContextValidationMixin import (
    DEFAULT_VALIDATION_RULES,
    ContextValidationMixin,
)
from src.logic.agents.cognitive.ContextVersioningMixin import ContextVersioningMixin
from src.logic.agents.cognitive.core.LocalRAGCore import LocalRAGCore, RAGShard

__version__ = VERSION


class ContextAgent(
    BaseAgent,
    ContextTemplateMixin,
    ContextTaggingMixin,
    ContextVersioningMixin,
    ContextValidationMixin,
    ContextAnnotationMixin,
    ContextCategorizationMixin,
    ContextRAGMixin,
):
    """Updates code file context descriptions using AI assistance."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.rag_core = LocalRAGCore()
        self.rag_shards: list[RAGShard] = []

        # Configuration
        self.config = {
            "extensions": [
                ".py",
                ".js",
                ".ts",
                ".go",
                ".rs",
                ".java",
                ".sh",
                ".json",
                ".yaml",
                ".yml",
                ".toml",
                ".ini",
                ".cfg",
                ".md",
                ".rst",
                ".txt",
            ]
        }

        self._validate_file_extension()
        self.source_path = self._derive_source_path()

        # New features initialized from defaults
        self._templates = dict(DEFAULT_TEMPLATES)
        self._tags = {}
        self._versions = []
        self._validation_rules = list(DEFAULT_VALIDATION_RULES)
        self._annotations = []
        self._priority = ContextPriority.MEDIUM
        self._category = FileCategory.OTHER
        self._compressed_content = None
        self._metadata = {}

    def route_query(self, query: str) -> list[str]:
        """Selects the best vector shards based on file path and query sentiment."""
        active_path = str(self.file_path)
        selected = self.rag_core.route_query_to_shards(
            query, active_path, self.rag_shards
        )
        logging.info(f"ContextAgent: Query '{query}' routed to {len(selected)} shards.")
        return selected

    def _validate_file_extension(self) -> None:
        """Validate that the file has the correct extension."""
        if not self.file_path.name.endswith(".description.md"):
            logging.warning(
                f"File {self.file_path.name} does not end with .description.md. "
                "Context operations may be limited."
            )

    def _derive_source_path(self) -> Path | None:
        """Derive source file path from .description.md filename."""
        if self.file_path.name.endswith(".description.md"):
            stem = self.file_path.name.replace(".description.md", "")
            # Use configurable extensions
            for ext in self.config.get("extensions", []):
                source = self.file_path.parent / f"{stem}{ext}"
                if source.exists():
                    return source
        return None

    # ========== Core Methods ==========
    def _get_default_content(self) -> str:
        """Return rich, structured template for new descriptions."""
        self.file_path.name.replace(".description.md", "")
        return """# Description: `{filename}`

## Purpose
[One - line purpose statement]

## Key Features
- [Feature 1]
- [Feature 2]

## Usage
```bash
# Example usage
```
"""
    def _get_fallback_response(self) -> str:
        """
        """
