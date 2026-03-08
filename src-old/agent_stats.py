#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""
LLM_CONTEXT_START

## Source: src-old/agent_stats.description.md

# Description: `agent_stats.py`

## Module purpose

Agent specializing in collecting and reporting project development statistics.

## Location
- Path: `src\agent_stats.py`

## Public surface
- Classes: (none)
- Functions: main

## Behavior summary
- Has a CLI entrypoint (`__main__`).
- Uses `argparse` for CLI parsing.

## Key dependencies
- Top imports: `sys`, `argparse`, `pathlib`, `src.classes.stats.StatsAgent`

## Metadata

- SHA256(source): `0819493e76f98939`
- Last updated: `2026-01-08 22:51:33`
- File: `src\agent_stats.py`
## Source: src-old/agent_stats.improvements.md

# Improvements: `agent_stats.py`

## Suggested improvements

- Add `--help` examples and validate CLI args (paths, required files).
- Function `main` is missing type annotations.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\agent_stats.py`

LLM_CONTEXT_END
"""

"""Agent specializing in collecting and reporting project development statistics."""

from src.version import VERSION
import sys
import argparse
from pathlib import Path
from src.classes.stats.StatsAgent import StatsAgent

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stats Agent: Reports statistics on file update progress"
    )
    parser.add_argument("--files", nargs="+", help="List of files to analyze")
    parser.add_argument("--dir", help="Directory to analyze (recursive)")
    parser.add_argument(
        "--format",
        choices=["text", "json", "csv"],
        default="text",
        help="Output format",
    )
    args = parser.parse_args()

    files = args.files or []
    if args.dir:
        # Avoid including hidden folders or common ignored directories
        path = Path(args.dir)
        for p in path.rglob("*"):
            if p.is_file() and not any(
                part.startswith(".") or part in ["__pycache__", "venv"]
                for part in p.parts
            ):
                files.append(str(p))

    if not files:
        # Fallback to simple scan of current dir if no input
        files = [str(p) for p in Path(".").glob("*.py")]

    agent = StatsAgent(files)
    agent.report_stats(output_format=args.format)


if __name__ == "__main__":
    main()
