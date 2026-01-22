<<<<<<< HEAD
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

=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""
Unified Diff Generation Core for PyAgent.
Standardizes text comparison and patch generation.
"""

from __future__ import annotations
<<<<<<< HEAD

import difflib
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base_core import BaseCore
from .models import DiffOutputFormat, DiffResult
=======
import difflib
import logging
from typing import Any, Dict, Optional, List
from src.core.base.common.base_core import BaseCore
from src.core.base.common.models import DiffOutputFormat, DiffResult
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

try:
    import rust_core as rc
except ImportError:
    rc = None

<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class DiffCore(BaseCore):
    """
    Standard implementation for text comparison.
    Supports unified diff format and structured JSON diffs.
    """
<<<<<<< HEAD

    def __init__(self, output_format: DiffOutputFormat = DiffOutputFormat.UNIFIED, context_lines: int = 3) -> None:
=======
    
    def __init__(self, output_format: DiffOutputFormat = DiffOutputFormat.UNIFIED, context_lines: int = 3):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        super().__init__()
        self.output_format = output_format
        self.context_lines = context_lines

<<<<<<< HEAD
    def generate_diff(self, old_text: str | Path, new_text: str, file_path: Optional[str | Path] = None) -> DiffResult:
=======
    def generate_diff(self, old_text: str, new_text: str, file_path: Optional[str] = None) -> str:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """
        Generates a diff between two strings.
        If rc is available, uses the Rust-accelerated diffing engine (LCS or Myers).
        """
<<<<<<< HEAD
        # Handle legacy calls where file_path was passed as first argument
        actual_old = old_text
        actual_new = new_text
        actual_path = file_path

        if (isinstance(old_text, (Path, str)) and isinstance(new_text, str) and
            (file_path is None or isinstance(file_path, str))):
            # Check if old_text looks like a path and new_text looks like content
            if isinstance(old_text, Path) or (isinstance(old_text, str) and ("/" in old_text or "\\" in old_text)):
                # If we have 3 args and first is path, 2nd is old, 3rd is new
                if file_path is not None:
                    actual_path = str(old_text)
                    actual_old = new_text
                    actual_new = file_path

        # Ensure we have strings for content
        if hasattr(actual_old, "read_text"):
            actual_old = actual_old.read_text(errors="ignore")
        if not isinstance(actual_old, str):
            actual_old = str(actual_old)
        if not isinstance(actual_new, str):
            actual_new = str(actual_new)

        diff_text = ""
        if rc and hasattr(rc, "generate_diff_rust"):  # pylint: disable=no-member
            # pylint: disable=no-member
            diff_text = rc.generate_diff_rust(actual_old, actual_new, self.context_lines)  # type: ignore
        else:
            old_lines = actual_old.splitlines(keepends=True)
            new_lines = actual_new.splitlines(keepends=True)

            diff = difflib.unified_diff(
                old_lines,
                new_lines,
                fromfile=f"a/{actual_path}" if actual_path else "a/file",
                tofile=f"b/{actual_path}" if actual_path else "b/file",
                n=self.context_lines,
            )
            diff_text = "".join(diff)

        additions = 0
        deletions = 0
        if diff_text:
            for line in diff_text.splitlines():
                if line.startswith("+") and not line.startswith("+++"):
                    additions += 1
                elif line.startswith("-") and not line.startswith("---"):
                    deletions += 1

        return DiffResult(
            file_path=Path(actual_path) if actual_path else None,
            original_content=actual_old,
            modified_content=actual_new,
            diff_text=diff_text,
            diff_lines=diff_text.splitlines() if diff_text else [],
            additions=additions,
            deletions=deletions,
            changes=additions + deletions
        )

    def format_diff(self, result: DiffResult, fmt: Optional[DiffOutputFormat] = None) -> str:
        """Formats a DiffResult into a string."""
        target_fmt = fmt or self.output_format
        if hasattr(target_fmt, "name") and target_fmt.name == "HTML":
            return f"<html><body><pre>{result.diff_text}</pre></body></html>"
        return result.diff_text
=======
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
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

    def generate_structured_diff(self, old_text: str, new_text: str) -> List[Dict[str, Any]]:
        """Generates a structured list of changes (line by line)."""
        # Python implementation using SequenceMatcher
<<<<<<< HEAD
        _ = (old_text, new_text)  # Mark as used
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return []
