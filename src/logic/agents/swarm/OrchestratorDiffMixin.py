#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
import logging
from pathlib import Path
from src.core.base.utils.DiffGenerator import DiffGenerator
from src.core.base.models import DiffOutputFormat, DiffResult


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
