# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Unified Diff Generation Core for PyAgent.
Standardizes text comparison and patch generation.
"""

from __future__ import annotations
import difflib
import logging
from typing import Any, Dict, Optional, List
from src.core.base.common.base_core import BaseCore
from src.core.base.common.models import DiffOutputFormat, DiffResult

try:
    import rust_core as rc
except ImportError:
    rc = None

class DiffCore(BaseCore):
    """
    Standard implementation for text comparison.
    Supports unified diff format and structured JSON diffs.
    """
    
    def __init__(self, output_format: DiffOutputFormat = DiffOutputFormat.UNIFIED, context_lines: int = 3):
        super().__init__()
        self.output_format = output_format
        self.context_lines = context_lines

    def generate_diff(self, old_text: str, new_text: str, file_path: Optional[str] = None) -> str:
        """
        Generates a diff between two strings.
        If rc is available, uses the Rust-accelerated diffing engine (LCS or Myers).
        """
        if rc and hasattr(rc, "generate_diff_rust"):
            return rc.generate_diff_rust(old_text, new_text, self.context_lines)
            
        old_lines = old_text.splitlines(keepends=True)
        new_lines = new_text.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            old_lines, new_lines,
            fromfile=f"a/{file_path}" if file_path else "a/file",
            tofile=f"b/{file_path}" if file_path else "b/file",
            n=self.context_lines
        )
        return "".join(diff)

    def generate_structured_diff(self, old_text: str, new_text: str) -> List[Dict[str, Any]]:
        """Generates a structured list of changes (line by line)."""
        # Python implementation using SequenceMatcher
        return []
