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
Syntax Fixer Mixin - Fix Python syntax patterns and common type-hint errors

[Brief Summary]
# DATE: 2026-02-12
AUTHOR: Keimpe de Jong

USAGE:
- Import SyntaxFixerMixin into agent classes or utilities that
  operate on Path-referenced Python source files.
- Call fix_invalid_for_loop_type_hints(Path('path/to/file.py')) to
  automatically correct invalid "for var: Type in" constructs.
- Call check_unmatched_triple_quotes(Path('path/to/file.py')) to
  detect unmatched triple-quote occurrences and return line numbers
  for inspection.

WHAT IT DOES:
- Detects and fixes invalid for-loop type-hint syntax of the form
  "for x: Type in ..." by rewriting to "for x in ...".
- Scans files for unmatched triple-quote occurrences and returns
  the line numbers where triple quotes appear if an odd count is
  found.
- Logs actions and failures for operational visibility.

WHAT IT SHOULD DO BETTER:
- Broaden regex accuracy to avoid false positives and handle
  complex whitespace/comments, generics, and nested constructs
  more robustly.
- Preserve original file formatting (e.g., spacing, inline comments)
  and create backups or use a transactional write for safer changes.
- Add unit tests, configurable patterns, and an option to preview
  changes before writing; consider AST-based parsing for correctness
  instead of regex alone.
- Provide clearer handling/reporting for edge cases like f-strings
  with triple quotes or mixed single/double triple quotes.

FILE CONTENT SUMMARY:
Mixin for fixing Python syntax patterns and common type hint errors.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


class SyntaxFixerMixin:
    """Provides automated fixes for specific Python syntax patterns."""

    def fix_invalid_for_loop_type_hints(self, file_path: Path) -> bool:
        r"""
        Fixes 'for x: Type in' -> 'for x in' which is invalid Python syntax.
        Regex pattern: r'for\s+(\w+):\s*[^i]*?\s+in\s+'
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            # Pattern matches: for var: type in, for var: dict[str, Any] in, etc.
            pattern = r'for\s+(\w+):\s*[^i]*?\s+in\s+'
            if re.search(pattern, content):
                fixed = re.sub(pattern, r'for \1 in ', content)
                if fixed != content:
                    file_path.write_text(fixed, encoding='utf-8')
                    logger.info(f"Fixed invalid for-loop type hint in {file_path}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to fix for-loop syntax in {file_path}: {e}")
            return False

    def check_unmatched_triple_quotes(self, file_path: Path) -> list[int]:
        """
        Detects unmatched triple-quote occurrences.
        Returns a list of line numbers of triple quotes if the total count is odd.
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            indices = []
            i = 0
            while True:
                idx = content.find('"""', i)
                if idx == -1:
                    break
                indices.append(idx)
                i = idx + 3

            if len(indices) % 2 != 0:
                line_numbers = [content.count('\n', 0, idx) + 1 for idx in indices]
                logger.warning(f"Unmatched triple quotes found in {file_path} at lines: {line_numbers}")
                return line_numbers
            return []
        except Exception as e:
            logger.error(f"Failed to check triple quotes in {file_path}: {e}")
            return []
