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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Specialized manager for handling agent improvement iterations."""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import sys
from pathlib import Path
from typing import List, Dict, Any
from src.core.base.version import is_gate_open, EVOLUTION_PHASE

__version__ = VERSION

class AgentUpdateManager:
    """
    Handles the update logic for code files, including errors, improvements, and tests.
    Implements Version Gatekeeping to prevent unstable mutations.
    """

    def __init__(self, repo_root: Path, models: Dict[str, Any], strategy: str, command_handler: Any, file_manager: Any, core: Any) -> None:
        self.repo_root = repo_root
        self.models = models
        self.strategy = strategy
        self.command_handler = command_handler
        self.file_manager = file_manager
        self.core = core
        self.min_gate_phase = 105 # Minimum phase required for autonomous updates

    def _check_gate(self) -> bool:
        """Internal version gate check."""
        if not is_gate_open(self.min_gate_phase):
            logging.warning(f"AgentUpdateManager: Evolution Gate Closed. Required Phase: {self.min_gate_phase}, Current: {EVOLUTION_PHASE}")
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
            from src.core.base.utils.core_utils import fix_markdown_content
            content = f"# Errors\n\nNo errors reported for {code_file.name}.\n"
            errors_file.write_text(fix_markdown_content(content), encoding='utf-8')
            logging.info(f"Created {errors_file.relative_to(self.repo_root)}")
            changes_made = True
            
        # Update errors
        prompt = f"Analyze and improve the error report for {code_file.name}"
        script_path = str(Path(__file__).parent.parent.parent / 'errors' / 'main.py')
        cmd = self.core.get_agent_command(
            sys.executable,
            script_path,
            str(errors_file),
            prompt,
            self.strategy
        )
        with self.command_handler.with_agent_env('errors'):
            result = self.command_handler.run_command(cmd)

        if result.stdout and "No changes made" not in result.stdout:
            changes_made = True
            
        # Create improvements file if it doesn't exist
        if not improvements_file.exists():
            from src.core.base.utils.core_utils import fix_markdown_content
            content = f"# Improvements\n\nNo improvements suggested for {code_file.name}.\n"
            improvements_file.write_text(fix_markdown_content(content), encoding='utf-8')
            logging.info(f"Created {improvements_file.relative_to(self.repo_root)}")
            changes_made = True
            
        # Update improvements
        prompt = f"Suggest and improve improvements for {code_file.name}"
        script_path = str(Path(__file__).parent.parent.parent / 'improvements' / 'main.py')
        cmd = self.core.get_agent_command(
            sys.executable,
            script_path,
            str(improvements_file),
            prompt,
            self.strategy
        )
        with self.command_handler.with_agent_env('improvements'):
            result = self.command_handler.run_command(cmd)

        if result.stdout and "No changes made" not in result.stdout:
            changes_made = True
            
        return changes_made

    def _get_pending_improvements(self, improvements_file: Path) -> List[str]:
        """Extract pending improvements using core logic."""
        if not improvements_file.exists():
            return []
        try:
            content = improvements_file.read_text(encoding='utf-8')
            all_pending = self.core.parse_improvements_content(content)
            return self.core.score_improvement_items(all_pending)
        except Exception as e:
            logging.warning(f"AgentUpdateManager: Failed to read improvements: {e}")
            return []

    def _mark_improvements_fixed(self, improvements_file: Path, fixed_items: List[str]) -> None:
        """Mark items as fixed in the improvements file."""
        if not improvements_file.exists() or not fixed_items:
            return
        try:
            content = improvements_file.read_text(encoding='utf-8')
            new_content = self.core.update_fixed_items(content, fixed_items)
            improvements_file.write_text(new_content, encoding='utf-8')
        except Exception as e:
            logging.warning(f"AgentUpdateManager: Failed to update improvements file: {e}")

    def _log_changes(self, changes_file: Path, fixed_items: List[str]) -> None:
        """Log fixed improvements to the changes file."""
        if not changes_file.exists() or not fixed_items:
            return
        try:
            content = changes_file.read_text(encoding='utf-8')
            new_entries = self.core.generate_changelog_entries(fixed_items)
            new_content = content.rstrip() + "\n\n" + new_entries + "\n"
            changes_file.write_text(new_content, encoding='utf-8')
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
        from src.core.base.utils.core_utils import fix_markdown_content

        # Create changelog if needed
        if not changes_file.exists():
            content = f"# Changelog\n\n- Initial version of {code_file.name}\n"
            changes_file.write_text(fix_markdown_content(content), encoding='utf-8')
            changes_made = True

        # Update changelog agent
        prompt = f"Update the changelog for {code_file.name} with recent changes"
        script_path = str(Path(__file__).parent.parent.parent / 'changes' / 'main.py')
        cmd = self.core.get_agent_command(
            sys.executable,
            script_path,
            str(changes_file),
            prompt,
            self.strategy
        )
        with self.command_handler.with_agent_env('changes'):
            result = self.command_handler.run_command(cmd)
        if result.stdout and "No changes made" not in result.stdout:
            changes_made = True

        # Update context/description
        if not context_file.exists():
            content = f"# Description\n\n{code_file.name} - Description to be added.\n"
            context_file.write_text(fix_markdown_content(content), encoding='utf-8')
            changes_made = True

        prompt = f"Update the description for {code_file.name} based on current code"
        script_path = str(Path(__file__).parent.parent.parent / 'context' / 'main.py')
        cmd = self.core.get_agent_command(
            sys.executable,
            script_path,
            str(context_file),
            prompt,
            self.strategy
        )
        with self.command_handler.with_agent_env('context'):
            result = self.command_handler.run_command(cmd)
        if result.stdout and "No changes made" not in result.stdout:
            changes_made = True

        return changes_made

    def update_code(self, code_file: Path) -> bool:
        """
        Update the code file based on improvements.
        Returns True if changes were written.
        """
        if not self._check_gate():
            return False

        prompt = f"Update the code in {code_file.name} to implement pending improvements"
        script_path = str(Path(__file__).parent.parent.parent / 'coder' / 'main.py')
        cmd = self.core.get_agent_command(
            sys.executable,
            script_path,
            str(code_file),
            prompt,
            self.strategy
        )
        with self.command_handler.with_agent_env('coder'):
            result = self.command_handler.run_command(cmd)

        return result.stdout and "No changes made" not in result.stdout