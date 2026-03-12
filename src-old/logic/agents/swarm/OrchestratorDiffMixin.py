#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/logic/agents/swarm/OrchestratorDiffMixin.description.md

# OrchestratorDiffMixin

**File**: `src\\logic\agents\\swarm\\OrchestratorDiffMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 40  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for OrchestratorDiffMixin.

## Classes (1)

### `OrchestratorDiffMixin`

Diff preview methods for OrchestratorAgent.

**Methods** (3):
- `enable_diff_preview(self, output_format)`
- `preview_changes(self, file_path, new_content)`
- `show_pending_diffs(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.models.DiffOutputFormat`
- `src.core.base.models.DiffResult`
- `src.core.base.utils.DiffGenerator.DiffGenerator`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/swarm/OrchestratorDiffMixin.improvements.md

# Improvements for OrchestratorDiffMixin

**File**: `src\\logic\agents\\swarm\\OrchestratorDiffMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 40 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `OrchestratorDiffMixin_test.py` with pytest tests

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
import logging
from pathlib import Path

from src.core.base.models import DiffOutputFormat, DiffResult
from src.core.base.utils.DiffGenerator import DiffGenerator


class OrchestratorDiffMixin:
    """Diff preview methods for OrchestratorAgent."""

    def enable_diff_preview(
        self, output_format: DiffOutputFormat = DiffOutputFormat.UNIFIED
    ) -> None:
        """Enable diff preview mode."""
        self.diff_generator = DiffGenerator(output_format)
        logging.info(f"Diff preview enabled (format: {output_format.name})")

    def preview_changes(self, file_path: Path, new_content: str) -> DiffResult:
        """Preview changes to a file without applying them."""
        if not hasattr(self, "diff_generator"):
            self.diff_generator = DiffGenerator()
        original = file_path.read_text() if file_path.exists() else ""
        return self.diff_generator.generate_diff(file_path, original, new_content)

    def show_pending_diffs(self) -> None:
        """Show all pending diffs for dry-run mode."""
        if not hasattr(self, "pending_diffs"):
            logging.info("No pending changes.")
            return
        logging.info(f"=== Pending Changes ({len(self.pending_diffs)} files) ===")
        for diff in self.pending_diffs:
            logging.info(f"--- {diff.file_path} ---")
            logging.info(f"  +{diff.additions} -{diff.deletions}")
            if hasattr(self, "diff_generator"):
                self.diff_generator.print_diff(diff)
            logging.info("")
