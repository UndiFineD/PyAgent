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
Knowledge symbol mixin for symbol extraction logic.
"""

import re
from typing import Any

try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class KnowledgeSymbolMixin:
    """Methods for symbol extraction from various formats."""

    def extract_symbols(self, content: str, pattern: str) -> list[str]:
        """Generic symbol extractor using optimized regex."""
        if not content:
            return []
        return re.findall(pattern, content)

    def extract_python_symbols(self, content: str) -> list[str]:
        """Extracts class and function names from Python content."""
        if HAS_RUST:
            try:
                return rust_core.extract_python_symbols(content)  # type: ignore[attr-defined]
            except (RuntimeError, AttributeError):
                pass
        return self.extract_symbols(
            content, r"(?:class|def)\s+([a-zA-Z_][a-zA-Z0-9_]*)"
        )

    def extract_markdown_backlinks(self, content: str) -> list[str]:
        """Extracts [[WikiStyle]] backlinks from markdown content."""
        if HAS_RUST:
            try:
                return rust_core.extract_markdown_backlinks(content)  # type: ignore[attr-defined]
            except (RuntimeError, AttributeError):
                pass
        return self.extract_symbols(content, r"\[\[(.*?)\]\]")

    def build_symbol_map(self, directory: Any, patterns: dict[str, str]) -> dict[str, list[str]]:
        """Scans a directory for symbols according to provided patterns."""
        from pathlib import Path
        symbol_map = {}
        dir_path = Path(directory)
        for ext, pattern in patterns.items():
            # Use non-recursive glob to avoid scanning the whole repo in tests
            for file_path in dir_path.glob(f"*{ext}"):
                try:
                    content = file_path.read_text(encoding="utf-8")
                    symbols = self.extract_symbols(content, pattern)
                    if symbols:
                        symbol_map[file_path.name] = symbols
                except (IOError, OSError, UnicodeDecodeError):
                    continue
        return symbol_map