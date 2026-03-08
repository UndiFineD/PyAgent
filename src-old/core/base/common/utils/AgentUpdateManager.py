#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/core/base/common/utils/AgentUpdateManager.description.md

# AgentUpdateManager

**File**: `src\core\base\common\utils\AgentUpdateManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 229  
**Complexity**: 7 (moderate)

## Overview

Specialized manager for handling agent improvement iterations.

## Classes (1)

### `AgentUpdateManager`

Handles the update logic for code files, including errors, improvements, and tests.
Implements Version Gatekeeping to prevent unstable mutations.

**Methods** (7):
- `__init__(self, repo_root, models, strategy, command_handler, file_manager, core)`
- `_check_gate(self)`
- `update_errors_improvements(self, code_file)`
- `_get_pending_improvements(self, improvements_file)`
- `_mark_improvements_fixed(self, improvements_file, fixed_items)`
- `_log_changes(self, changes_file, fixed_items)`
- `update_changelog_context_tests(self, code_file)`

## Dependencies

**Imports** (14):
- `logging`
- `pathlib.Path`
- `subprocess`
- `sys`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `utils.fix_markdown_content`
- `version.EVOLUTION_PHASE`
- `version.is_gate_open`

---
*Auto-generated documentation*
## Source: src-old/core/base/common/utils/AgentUpdateManager.improvements.md

# Improvements for AgentUpdateManager

**File**: `src\core\base\common\utils\AgentUpdateManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 229 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AgentUpdateManager_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""Specialized manager for handling agent improvement iterations."""

import logging
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Version Gatekeeping (Phase 108)
import sys

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
try:
    from version import is_gate_open, EVOLUTION_PHASE
except ImportError:

    def is_gate_open(phase) -> bool:
        return True

    EVOLUTION_PHASE = 0


class AgentUpdateManager:
    """
    Handles the update logic for code files, including errors, improvements, and tests.
    Implements Version Gatekeeping to prevent unstable mutations.
    """

    def __init__(
        self,
        repo_root: Path,
        models: Dict[str, Any],
        strategy: str,
        command_handler: Any,
        file_manager: Any,
        core: Any,
    ) -> None:
        self.repo_root = repo_root
        self.models = models
        self.strategy = strategy
        self.command_handler = command_handler
        self.file_manager = file_manager
        self.core = core
        self.min_gate_phase = 105  # Minimum phase required for autonomous updates

    def _check_gate(self) -> bool:
        """Internal version gate check."""
        if not is_gate_open(self.min_gate_phase):
            logging.warning(
                f"AgentUpdateManager: Evolution Gate Closed. Required Phase: {self.min_gate_phase}, Current: {EVOLUTION_PHASE}"
            )
            return False
        return True

    def update_errors_improvements(self, code_file: Path) -> bool:
        """
        Update errors and improvements for a specific code file.
        Returns True if changes were written.
        """
        if not self._check_gate():
            return False

        base = code_file.stem
        dir_path = code_file.parent
        errors_file = dir_path / f"{base}.errors.md"
        improvements_file = dir_path / f"{base}.improvements.md"
        changes_made = False

        # Create errors file if it doesn't exist
        if not errors_file.exists():
            from .utils import fix_markdown_content

            content = f"# Errors\n\nNo errors reported for {code_file.name}.\n"
            errors_file.write_text(fix_markdown_content(content), encoding="utf-8")
            logging.info(f"Created {errors_file.relative_to(self.repo_root)}")
            changes_made = True

        # Update errors
        prompt = f"Analyze and improve the error report for {code_file.name}"
        cmd = [
            sys.executable,
            str(Path(__file__).parent.parent.parent / "agent_errors.py"),
            "--context",
            str(errors_file),
            "--prompt",
            prompt,
            "--strategy",
            self.strategy,
        ]
        with self.command_handler.with_agent_env("errors"):
            result = self.command_handler.run_command(cmd)

        if result.stdout and "No changes made" not in result.stdout:
            changes_made = True

        # Create improvements file if it doesn't exist
        if not improvements_file.exists():
            from .utils import fix_markdown_content

            content = (
                f"# Improvements\n\nNo improvements suggested for {code_file.name}.\n"
            )
            improvements_file.write_text(
                fix_markdown_content(content), encoding="utf-8"
            )
            logging.info(f"Created {improvements_file.relative_to(self.repo_root)}")
            changes_made = True

        # Update improvements
        prompt = f"Suggest and improve improvements for {code_file.name}"
        cmd = [
            sys.executable,
            str(Path(__file__).parent.parent.parent / "agent_improvements.py"),
            "--context",
            str(improvements_file),
            "--prompt",
            prompt,
            "--strategy",
            self.strategy,
        ]
        with self.command_handler.with_agent_env("improvements"):
            result = self.command_handler.run_command(cmd)

        if result.stdout and "No changes made" not in result.stdout:
            changes_made = True

        return changes_made

    def _get_pending_improvements(self, improvements_file: Path) -> List[str]:
        """Extract pending improvements using core logic."""
        if not improvements_file.exists():
            return []
        try:
            content = improvements_file.read_text(encoding="utf-8")
            all_pending = self.core.parse_improvements_content(content)
            return self.core.score_improvement_items(all_pending)
        except Exception as e:
            logging.warning(f"AgentUpdateManager: Failed to read improvements: {e}")
            return []

    def _mark_improvements_fixed(
        self, improvements_file: Path, fixed_items: List[str]
    ) -> None:
        """Mark items as fixed in the improvements file."""
        if not improvements_file.exists() or not fixed_items:
            return
        try:
            content = improvements_file.read_text(encoding="utf-8")
            new_content = self.core.update_fixed_items(content, fixed_items)
            improvements_file.write_text(new_content, encoding="utf-8")
        except Exception as e:
            logging.warning(
                f"AgentUpdateManager: Failed to update improvements file: {e}"
            )

    def _log_changes(self, changes_file: Path, fixed_items: List[str]) -> None:
        """Log fixed improvements to the changes file."""
        if not changes_file.exists() or not fixed_items:
            return
        try:
            content = changes_file.read_text(encoding="utf-8")
            new_entries = self.core.generate_changelog_entries(fixed_items)
            new_content = content.rstrip() + "\n\n" + new_entries + "\n"
            changes_file.write_text(new_content, encoding="utf-8")
        except Exception as e:
            logging.warning(f"AgentUpdateManager: Failed to update changes file: {e}")

    def update_changelog_context_tests(self, code_file: Path) -> bool:
        """Update changelog, context, and tests for a file."""
        if not self._check_gate():
            return False

        base = code_file.stem
        dir_path = code_file.parent
        changes_file = dir_path / f"{base}.changes.md"
        context_file = dir_path / f"{base}.description.md"
        changes_made = False
        from .utils import fix_markdown_content

        # Create changelog if needed
        if not changes_file.exists():
            content = f"# Changelog\n\n- Initial version of {code_file.name}\n"
            changes_file.write_text(fix_markdown_content(content), encoding="utf-8")
            changes_made = True

        # Update changelog agent
        prompt = f"Update the changelog for {code_file.name} with recent changes"
        cmd = [
            sys.executable,
            str(Path(__file__).parent.parent.parent / "agent_changes.py"),
            "--context",
            str(changes_file),
            "--prompt",
            prompt,
            "--strategy",
            self.strategy,
        ]
        with self.command_handler.with_agent_env("changes"):
            result = self.command_handler.run_command(cmd)
        if result.stdout and "No changes made" not in result.stdout:
            changes_made = True

        # Update context/description
        if not context_file.exists():
            content = f"# Description\n\n{code_file.name} - Description to be added.\n"
            context_file.write_text(fix_markdown_content(content), encoding="utf-8")
            changes_made = True

        prompt = f"Update the description for {code_file.name} based on current code"
        cmd = [
            sys.executable,
            str(Path(__file__).parent.parent.parent / "agent_context.py"),
            "--context",
            str(context_file),
            "--prompt",
            prompt,
            "--strategy",
            self.strategy,
        ]
        with self.command_handler.with_agent_env("context"):
            result = self.command_handler.run_command(cmd)
        if result.stdout and "No changes made" not in result.stdout:
            changes_made = True

        return changes_made
        if not changes_file.exists():
            content = f"# Changelog\n\n- Initial version of {code_file.name}\n"
            changes_file.write_text(fix_markdown_content(content), encoding="utf-8")
            changes_made = True

        # Update changelog agent
        prompt = f"Update the changelog for {code_file.name} with recent changes"
        cmd = [
            sys.executable,
            str(Path(__file__).parent.parent.parent / "agent_changes.py"),
            "--context",
            str(changes_file),
            "--prompt",
            prompt,
            "--strategy",
            self.strategy,
        ]
        with self.command_handler.with_agent_env("changes"):
            result = self.command_handler.run_command(cmd)
        if result.stdout and "No changes made" not in result.stdout:
            changes_made = True

        # Update context/description
        if not context_file.exists():
            content = f"# Description\n\n{code_file.name} - Description to be added.\n"
            context_file.write_text(fix_markdown_content(content), encoding="utf-8")
            changes_made = True

        prompt = f"Update the description for {code_file.name} based on current code"
        cmd = [
            sys.executable,
            str(Path(__file__).parent.parent.parent / "agent_context.py"),
            "--context",
            str(context_file),
            "--prompt",
            prompt,
            "--strategy",
            self.strategy,
        ]
        with self.command_handler.with_agent_env("context"):
            result = self.command_handler.run_command(cmd)
        if result.stdout and "No changes made" not in result.stdout:
            changes_made = True

        return changes_made
