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

"""
KnowledgeCore logic for specialized workspace analysis.
Contains pure regex and indexing logic for fast symbol discovery.
This file is optimized for Rust migration (Phase 114).
"""

from __future__ import annotations
from src.core.base.Version import VERSION
import re
import logging
from pathlib import Path
from typing import Any

try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

__version__ = VERSION


class KnowledgeCore:
    """
    KnowledgeCore performs pure computational analysis of workspace symbols.
    No I/O or database operations are allowed here to ensure Rust portability.
    """

    def __init__(self, fleet: Any | None = None) -> None:
        self.fleet = fleet

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
            except Exception:
                pass
        return self.extract_symbols(
            content, r"(?:class|def)\s+([a-zA-Z_][a-zA-Z0-9_]*)"
        )

    def extract_markdown_backlinks(self, content: str) -> list[str]:
        """Extracts [[WikiStyle]] backlinks from markdown content."""
        if HAS_RUST:
            try:
                return rust_core.extract_markdown_backlinks(content)  # type: ignore[attr-defined]
            except Exception:
                pass
        return self.extract_symbols(content, r"\[\[(.*?)\]\]")

    def search_index(self, query: str, index: dict, root: Path) -> list[str]:
        """Extracts code snippets based on index hits."""
        snippets = []
        hits = index.get(query, [])
        for hit in hits:
            rel_path = hit["path"] if isinstance(hit, dict) else hit
            p = root / rel_path
            try:
                content = p.read_text(encoding="utf-8")
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    if f"def {query}" in line or f"class {query}" in line or query in line:
                        start, end = max(0, i - 5), min(len(lines), i + 15)
                        snippet = "\n".join(lines[start:end])
                        snippets.append(
                            f"> [!CODE] File: {rel_path} (from index)\n> ```python\n"
                            + "\n".join([f"> {sl}" for sl in snippet.splitlines()])
                            + "\n> ```\n"
                        )
                        break
            except Exception:
                pass
            if len(snippets) > 5: break
        return snippets

    def perform_fallback_scan(self, query: str, root: Path, indexed_paths: list) -> list[str]:
        """Performs a deep grep fallback search across the workspace."""
        snippets = []
        for p in root.rglob("*.py"):
            rel_path = str(p.relative_to(root))
            if any(part in rel_path for part in ["__pycache__", "venv", ".git"]) or rel_path in indexed_paths:
                continue
            try:
                content = p.read_text(encoding="utf-8")
                if query.lower() in content.lower():
                    lines = content.splitlines()
                    for i, line in enumerate(lines):
                        if query.lower() in line.lower():
                            start, end = max(0, i - 5), min(len(lines), i + 10)
                            snippet = "\n".join(lines[start:end])
                            snippets.append(
                                f"> [!CODE] File: {rel_path}\n> ```python\n"
                                + "\n".join([f"> {sl}" for sl in snippet.splitlines()])
                                + "\n> ```\n"
                            )
                            break
            except Exception:
                pass
            if len(snippets) > 5: break
        return snippets

    def process_file_content(
        self, rel_path: str, content: str, extension: str
    ) -> list[tuple[str, str, str, str]]:
        """
        Parses content and returns a list of (symbol, path, category, snippet) tuples.
        This is a pure function ready for Rust conversion.
        """
        results: list[tuple[str, str, str, str]] = []

        if extension == ".py":
            symbols = self.extract_python_symbols(content)
            for s in symbols:
                results.append((s, rel_path, "python_symbol", content[:500]))
        elif extension == ".md":
            links = self.extract_markdown_backlinks(content)
            for link in links:
                results.append(
                    (f"link:{link}", rel_path, "markdown_link", content[:500])
                )

        return results

    def compute_similarity(self, text_a: str, text_b: str) -> float:
        """Computes basic string similarity (Jaccard) for symbol matching."""
        set_a = set(re.findall(r"\w+", text_a.lower()))
        set_b = set(re.findall(r"\w+", text_b.lower()))
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        return float(intersection) / union
