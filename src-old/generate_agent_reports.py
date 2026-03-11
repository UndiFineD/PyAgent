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
    """Helper for legacy tests."""
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    """Main function to generate agent reports."""
    import argparse
    parser = argparse.ArgumentParser(description='Generate Agent Reports')
    parser.add_argument('--dir', default='.', help='Directory to scan')
    parser.add_argument('--output', default='reports', help='Output directory')
    args = parser.parse_args()

    generator = ReportGenerator(args.dir)
    report = generator.generate_full_report()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    exporter = ReportExporter()
    # Export as HTML to the output directory
    exporter.export(report, ExportFormat.HTML, output_dir / "report.html")
    # Also save the markdown version as the progress dashboard
    (output_dir / "PROGRESS_DASHBOARD.md").write_text(report, encoding="utf-8")

    print(f"Reports generated in {args.output}")


if __name__ == '__main__':
    main()
