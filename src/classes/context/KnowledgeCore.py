#!/usr/bin/env python3

"""
KnowledgeCore logic for specialized workspace analysis.
Contains pure regex and indexing logic for fast symbol discovery.
This file is optimized for Rust migration (Phase 114).
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple

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
