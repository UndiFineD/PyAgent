#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

r"""LLM_CONTEXT_START

## Source: src-old/generate_agent_reports.description.md

# Description: `generate_agent_reports.py`

## Module purpose

(No module docstring found)

## Location
- Path: `src\generate_agent_reports.py`

## Public surface
- Classes: (none)
- Functions: _sha256_text, main

## Behavior summary
- Has a CLI entrypoint (`__main__`).
- Uses `argparse` for CLI parsing.

## Key dependencies
- Top imports: `sys`, `pathlib`, `src.classes.reports`, `hashlib`, `argparse`

## Metadata

- SHA256(source): `2011becf5a36187d`
- Last updated: `2026-01-08 08:26:01`
- File: `src\generate_agent_reports.py`
## Source: src-old/generate_agent_reports.improvements.md

# Improvements: `generate_agent_reports.py`

## Suggested improvements

- Add `--help` examples and validate CLI args (paths, required files).
- Add a concise module docstring describing purpose / usage.
- Consider using `logging` instead of `print` for controllable verbosity.
- Function `main` is missing type annotations.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\generate_agent_reports.py`

LLM_CONTEXT_END
"""
import sys
from pathlib import Path

from src.classes.reports import ExportFormat, ReportExporter, ReportGenerator

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))


def _sha256_text(text: str) -> str:
    """
    """
