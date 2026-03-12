#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/coder/DocumentationAgent.description.md

# DocumentationAgent

**File**: `src\classes\coder\DocumentationAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 67  
**Complexity**: 4 (simple)

## Overview

Agent specializing in automated documentation generation and maintenance.

## Classes (1)

### `DocumentationAgent`

**Inherits from**: BaseAgent

Generates technical references and project OVERVIEW documents.

**Methods** (4):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `generate_reference(self)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (9):
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`
- `src.classes.context.KnowledgeAgent.KnowledgeAgent`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/DocumentationAgent.improvements.md

# Improvements for DocumentationAgent

**File**: `src\classes\coder\DocumentationAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 67 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `DocumentationAgent_test.py` with pytest tests

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

"""Agent specializing in automated documentation generation and maintenance."""

import logging

from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import create_main_function
from src.classes.context.KnowledgeAgent import KnowledgeAgent


class DocumentationAgent(BaseAgent):
    """Generates technical references and project OVERVIEW documents."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self.knowledge = KnowledgeAgent(
            str(self.workspace_root / "src/classes/context/KnowledgeAgent.py")
        )
        self._system_prompt = (
            "You are the Documentation Agent. "
            "Your role is to maintain clear, accurate technical documentation. "
            "You summarize code structures, explain module relationships, and ensure READMEs are current."
        )

    def _get_default_content(self) -> str:
        return "# Documentation Log\n\n## Summary\nWaiting for update...\n"

    def generate_reference(self) -> str:
        """Generates a technical reference for the src/classes/ directory."""
        self.knowledge.build_index()
        classes_dir = self.workspace_root / "src/classes"

        # Get structural briefs
        py_files = [
            str(p.relative_to(self.workspace_root))
            for p in classes_dir.rglob("*.py")
            if "__init__" not in p.name
        ]
        briefing = self.knowledge.get_compressed_briefing(
            py_files[:10]
        )  # Top 10 for summary

        doc = [
            "# Technical Reference Guide",
            "",
            "## 🏗️ Class Hierarchy & Signatures",
            "This section provides an overview of the core modular classes.",
            "",
            briefing,
            "",
            "## 🔗 Dependency Map",
            "```mermaid",
            self.knowledge.get_graph_mermaid(),
            "```",
            "",
            "---",
            f"*Generated autonomously on {logging.time.strftime('%Y-%m-%d')}*",
        ]

        ref_path = self.workspace_root / "docs/TECHNICAL_REFERENCE.md"
        ref_path.parent.mkdir(parents=True, exist_ok=True)
        ref_path.write_text("\n".join(doc), encoding="utf-8")

        return f"Reference documentation updated at: {ref_path}"

    def improve_content(self, prompt: str) -> str:
        """Perform documentation maintenance."""
        return self.generate_reference()


if __name__ == "__main__":
    main = create_main_function(
        DocumentationAgent, "Documentation Agent", "Task (e.g. 'generate')"
    )
    main()
