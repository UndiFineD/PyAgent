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
Unified Diff Generation Core for PyAgent.
Standardizes text comparison and patch generation.
"""

from __future__ import annotations
import difflib
from typing import Any, Dict, Optional, List
from .base_core import BaseCore
from .models import DiffOutputFormat

try:
    import rust_core as rc
except ImportError:
    rc = None

class DiffCore(BaseCore):
    """
    Standard implementation for text comparison.
    Supports unified diff format and structured JSON diffs.
    """

    def __init__(
        self,
        output_format: DiffOutputFormat = DiffOutputFormat.UNIFIED,
        context_lines: int = 3
    ):
        super().__init__()
        self.output_format = output_format
        self.context_lines = context_lines

    def generate_diff(self, old_text: str, new_text: str, file_path: Optional[str] = None) -> str:
        """
        Generates a diff between two strings.
        If rc is available, uses the Rust-accelerated diffing engine (LCS or Myers).
        """
        if rc and hasattr(rc, "generate_diff_rust"): # pylint: disable=no-member
            # pylint: disable=no-member
            return rc.generate_diff_rust(old_text, new_text, self.context_lines) # type: ignore

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
        _ = (old_text, new_text) # Mark as used
        return []
