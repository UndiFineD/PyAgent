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
OrchestratorDiffMixin - Diff preview helpers for OrchestratorAgent

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Mix into an OrchestratorAgent (or compatible agent object) to add diff preview capabilities.
- Call enable_diff_preview(DiffOutputFormat) to configure diff formatting.
- Use preview_changes(Path, new_content) to generate a textual diff without writing files.
- Use show_pending_diffs() to log any collected pending diffs (dry-run support).

WHAT IT DOES:
- Provides lightweight methods to enable a DiffGenerator on the agent, produce diffs between on-disk and proposed content, and log pending diffs.
- Defaults to a unified diff format and lazily constructs the DiffGenerator when first needed.
- Integrates with a pending_diffs attribute (if present) to print summaries and full diffs via the DiffGenerator.

WHAT IT SHOULD DO BETTER:
- Explicitly declare and document the expected shape of pending_diffs (type, structure) and avoid silent attribute checks; prefer typed attributes or initialization in an agent base class.
- Add thread-safety and async-aware implementations (use asyncio for I/O-heavy agents) and avoid blocking file reads; support reading via StateTransaction for atomicity when used within transactional workflows.
- Improve configurability for output sinks (returning diffs, writing to configured loggers, or exposing structured diff objects), add unit tests for edge cases (binary files, large files), and surface errors instead of swallowing them via implicit attribute checks.
- Consider dependency injection for DiffGenerator to enable testing and alternate diff implementations; add clearer logging levels and concise human-friendly summaries for CLI use.

FILE CONTENT SUMMARY:
Orchestrator diff mixin module.
"""

from __future__ import annotations

import logging
from pathlib import Path

from src.core.base.common.models import DiffOutputFormat
from src.core.base.common.utils.diff_generator import DiffGenerator


class OrchestratorDiffMixin:
    """Diff preview methods for OrchestratorAgent."""

    def enable_diff_preview(self, output_format: DiffOutputFormat = DiffOutputFormat.UNIFIED) -> None:
        """Enable diff preview mode."""
        setattr(self, "diff_generator", DiffGenerator(output_format))
        logging.info(f"Diff preview enabled (format: {output_format.name})")

    def preview_changes(self, file_path: Path, new_content: str) -> str:
        """Preview changes to a file without applying them."""
        if not hasattr(self, "diff_generator"):
            setattr(self, "diff_generator", DiffGenerator())
        original = file_path.read_text(encoding="utf-8") if file_path.exists() else ""
        diff_gen = getattr(self, "diff_generator")
        return diff_gen.generate_diff(original, new_content, str(file_path))

    def show_pending_diffs(self) -> None:
        """Show all pending diffs for dry-run mode."""
        if not hasattr(self, "pending_diffs"):
            logging.info("No pending changes.")
            return

        pending_diffs = getattr(self, "pending_diffs")
        logging.info(f"=== Pending Changes ({len(pending_diffs)} files) ===")
        for diff in pending_diffs:
            logging.info(f"--- {diff.file_path} ---")
            logging.info(f"  +{diff.additions} -{diff.deletions}")
            if hasattr(self, "diff_generator"):
                diff_gen = getattr(self, "diff_generator")
                diff_gen.print_diff(diff)
            logging.info("")
"""

from __future__ import annotations

import logging
from pathlib import Path

from src.core.base.common.models import DiffOutputFormat
from src.core.base.common.utils.diff_generator import DiffGenerator


class OrchestratorDiffMixin:
    """Diff preview methods for OrchestratorAgent."""

    def enable_diff_preview(self, output_format: DiffOutputFormat = DiffOutputFormat.UNIFIED) -> None:
        """Enable diff preview mode."""
        setattr(self, "diff_generator", DiffGenerator(output_format))
        logging.info(f"Diff preview enabled (format: {output_format.name})")

    def preview_changes(self, file_path: Path, new_content: str) -> str:
        """Preview changes to a file without applying them."""
        if not hasattr(self, "diff_generator"):
            setattr(self, "diff_generator", DiffGenerator())
        original = file_path.read_text(encoding="utf-8") if file_path.exists() else ""
        diff_gen = getattr(self, "diff_generator")
        return diff_gen.generate_diff(original, new_content, str(file_path))

    def show_pending_diffs(self) -> None:
        """Show all pending diffs for dry-run mode."""
        if not hasattr(self, "pending_diffs"):
            logging.info("No pending changes.")
            return

        pending_diffs = getattr(self, "pending_diffs")
        logging.info(f"=== Pending Changes ({len(pending_diffs)} files) ===")
        for diff in pending_diffs:
            logging.info(f"--- {diff.file_path} ---")
            logging.info(f"  +{diff.additions} -{diff.deletions}")
            if hasattr(self, "diff_generator"):
                diff_gen = getattr(self, "diff_generator")
                diff_gen.print_diff(diff)
            logging.info("")
