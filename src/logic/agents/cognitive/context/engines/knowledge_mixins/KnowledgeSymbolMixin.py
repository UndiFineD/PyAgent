# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import re

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
