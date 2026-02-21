#!/usr/bin/env python3
"""Formatting utilities for PyAgent (parser-safe minimal implementation)."""
from __future__ import annotations

import difflib
import re
from typing import Optional

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None


class FormattingCore:
    """Handles logic regarding normalizing and diffing content."""

    def __init__(self, **kwargs) -> None:
        # simple initializer for compatibility
        super().__init__()

    def fix_markdown(self, content: str) -> str:
        """Normalize Markdown headings by ensuring a space after hashes."""
        lines = content.splitlines()

        def fix_line(line: str) -> str:
            if line.startswith("#") and not line.startswith("# "):
                return re.sub(r"^(#+)", r"\1 ", line)
            return line

        fixed_lines = [fix_line(l) for l in lines]
        return "\n".join(fixed_lines)

    def normalize_response(self, response: str) -> str:
        """Normalize response text into a single-space separated string."""
        if rc and hasattr(rc, "normalize_response"):
            try:
                return rc.normalize_response(response)  # type: ignore
            except Exception:
                pass
        normalized = response.strip().replace("\r\n", "\n")
        return " ".join(normalized.split())

    def calculate_diff(self, old_content: str, new_content: str, filename: str) -> str:
        """Generate a unified diff between two file contents."""
        if rc and hasattr(rc, "generate_unified_diff_rust"):
            try:
                diff_text, _, _ = rc.generate_unified_diff_rust(old_content, new_content, filename, 3)  # type: ignore
                return diff_text
            except Exception:
                pass

        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        diff_lines = list(difflib.unified_diff(old_lines, new_lines, fromfile=f"a/{filename}", tofile=f"b/{filename}"))
        return "".join(diff_lines)


# Backwards-compatible simple helper
class Formatting:
    @staticmethod
    def tidy(code: str) -> str:
        return code


__all__ = ["FormattingCore", "Formatting"]
