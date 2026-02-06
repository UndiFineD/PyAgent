# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-market-claude-code-skills\transcript-fixer\scripts\utils\diff_formats\html_format.py
#!/usr/bin/env python3
"""
HTML diff format generator

SINGLE RESPONSIBILITY: Generate HTML side-by-side comparison
"""

from __future__ import annotations

import difflib


def generate_html_diff(original: str, fixed: str) -> str:
    """
    Generate HTML format comparison report (side-by-side)

    Args:
        original: Original text
        fixed: Fixed text

    Returns:
        HTML format string with side-by-side comparison
    """
    original_lines = original.splitlines(keepends=True)
    fixed_lines = fixed.splitlines(keepends=True)

    differ = difflib.HtmlDiff(wrapcolumn=80)
    html = differ.make_file(
        original_lines,
        fixed_lines,
        fromdesc="原始版本",
        todesc="修复版本",
        context=True,
        numlines=3,
    )

    return html
