#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0

"""Docstring auditor utilities.

Parses the analyzer output (e.g., docs/prompt/prompt4.txt) and extracts a list
of Python modules flagged with missing module-level docstrings. Provides a
helper to generate a small next-batch file listing modules to address.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

MISSING_DOCSTRING_MARKER = "Missing Docstring: Module-level docstring is missing"


def parse_prompt_file(prompt_path: str | Path) -> List[str]:
    """Parse analyzer output and return file paths with missing docstring markers.

    Args:
        prompt_path: Path to the analyzer output file (plain text).

    Returns:
        List of relative file paths (POSIX-style) like "src/core/lazy_loader.py".
    """
    p = Path(prompt_path)
    if not p.exists():
        return []

    files: List[str] = []
    lines = p.read_text().splitlines()
    current_file: str | None = None
    for line in lines:
        m = re.match(r"\s*\* File:\s+(.+)$", line)
        if m:
            current_file = m.group(1).strip()
            continue
        if current_file and ("Missing Docstring" in line and "Module-level" in line):
            files.append(current_file.replace("\\", "/"))
            current_file = None
    return files


def file_path_to_module_name(path: str) -> str:
    """Convert a filesystem path to a module import path.

    Example: "src/core/lazy_loader.py" -> "src.core.lazy_loader"
    """
    p = Path(path)
    if p.suffix != ".py":
        raise ValueError("Only .py files supported")
    return ".".join(p.with_suffix("").parts)


def generate_next_batch(prompt_path: str | Path, out_path: str | Path, max_entries: int = 20) -> List[str]:
    """Generate the next small batch of modules to fix.

    Writes a newline-separated list of module names to `out_path` and returns
    the list. Modules are chosen in the order they appear in the prompt.
    """
    files = parse_prompt_file(prompt_path)
    modules = []
    for f in files:
        try:
            modules.append(file_path_to_module_name(f))
        except Exception:
            continue
        if len(modules) >= int(max_entries):
            break

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(modules))
    return modules
