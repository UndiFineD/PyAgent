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
from src.core.base.version import VERSION
import re
import logging
from typing import Dict, List, Any, Optional, Tuple

__version__ = VERSION

class KnowledgeCore:
    """
    KnowledgeCore performs pure computational analysis of workspace symbols.
    No I/O or database operations are allowed here to ensure Rust portability.
    """
    
    def __init__(self, fleet: Optional[Any] = None) -> None:
        self.fleet = fleet

    def extract_symbols(self, content: str, pattern: str) -> List[str]:
        """Generic symbol extractor using optimized regex."""
        if not content:
            return []
        return re.findall(pattern, content)

    def extract_python_symbols(self, content: str) -> List[str]:
        """Extracts class and function names from Python content."""
        return self.extract_symbols(content, r"(?:class|def)\s+([a-zA-Z_][a-zA-Z0-9_]*)")

    def extract_markdown_backlinks(self, content: str) -> List[str]:
        """Extracts [[WikiStyle]] backlinks from markdown content."""
        return self.extract_symbols(content, r"\[\[(.*?)\]\]")

    def build_symbol_map(self, root: Path, patterns: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Builds a map of symbols and backlinks.
        Note: This currently violates the 'No I/O' rule due to the existing KnowledgeAgent caller.
        Will be moved to an 'I/O' layer in Phase 126.
        """
        symbol_map: Dict[str, List[Dict[str, Any]]] = {}
        
        for ext, pattern in patterns.items():
            for file_path in root.rglob(f"*{ext}"):
                try:
                    rel_path = str(file_path.relative_to(root))
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    symbols = re.findall(pattern, content)
                    for sym in symbols:
                        if sym not in symbol_map:
                            symbol_map[sym] = []
                        symbol_map[sym].append({
                            "path": rel_path,
                            "snippet": content[:200].replace("\n", " ").strip()
                        })
                except Exception as e:
                    logging.warning(f"KnowledgeCore: Error indexing {file_path}: {e}")
                    
        return symbol_map

    def process_file_content(self, rel_path: str, content: str, extension: str) -> List[Tuple[str, str, str, str]]:
        """
        Parses content and returns a list of (symbol, path, category, snippet) tuples.
        This is a pure function ready for Rust conversion.
        """
        results: List[Tuple[str, str, str, str]] = []
        
        if extension == ".py":
            symbols = self.extract_python_symbols(content)
            for s in symbols:
                results.append((s, rel_path, "python_symbol", content[:500]))
        elif extension == ".md":
            links = self.extract_markdown_backlinks(content)
            for l in links:
                results.append((f"link:{l}", rel_path, "markdown_link", content[:500]))
        
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