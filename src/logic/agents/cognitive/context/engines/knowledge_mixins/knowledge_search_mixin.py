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
Knowledge search mixin for workspace-wide queries.
"""

from pathlib import Path

class KnowledgeSearchMixin:
    """Methods for workspace search and snippet extraction."""

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
            except (IOError, OSError):
                pass
            if len(snippets) > 5:
                break
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
            except (IOError, OSError):
                pass
            if len(snippets) > 5:
                break
        return snippets