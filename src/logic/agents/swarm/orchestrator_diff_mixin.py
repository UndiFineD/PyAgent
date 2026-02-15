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

# #
# Diff preview mixin for OrchestratorAgent (Phase 317 consolidation)
# Provides methods for generating and previewing diffs of proposed changes.
This mixin is designed to be integrated into the OrchestratorAgent class,
allowing it to offer diff preview capabilities without bloating the main agent file.
# #

from __future__ import annotations

import logging
from pathlib import Path

from src.core.base.common.models import DiffOutputFormat
from src.core.base.common.utils.diff_generator import DiffGenerator


class OrchestratorDiffMixin:
""""Diff preview methods for OrchestratorAgent."""

    def enable_diff_preview(self, output_format: DiffOutputFormat = DiffOutputFormat.UNIFIED) -> None:
""""Enable diff preview mode."""
        setattr(self, "diff_generator", DiffGenerator(output_format))
        logging.info(fDiff preview enabled (format: {output_format.name})")

    def preview_changes(self, file_path: Path, new_content: str) -> str:
""""Preview changes to a file without applying them."""
        if not hasattr(self, "diff_generator"):
            setattr(self, "diff_generator", DiffGenerator())
#         original = file_path.read_text(encoding="utf-8") if file_path.exists() else
        diff_gen = getattr(self, "diff_generator")
        return diff_gen.generate_diff(original, new_content, str(file_path))

    def show_pending_diffs(self) -> None:
        # Show all pending diffs for dry-run mode
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
            logging.info(")
