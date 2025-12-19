# Errors: `generate_agent_reports.py`

## Scan scope

- Static scan (AST parse) + lightweight syntax check
- VS Code/Pylance Problems are not embedded by this script

## Syntax / compile

- This script treats a successful AST parse as syntax OK.

## Known issues / hazards

- Overwrites `src/<stem>.{description,errors,improvements}.md` for processed files.
- Incremental skipping relies on reading a SHA prefix from `src/<stem>.description.md`; if that fingerprint line is missing/edited, files will be re-processed.
- Heuristic checks in report rendering (e.g., “uses subprocess”, “uses argparse”) are string matches against the target file’s source and can be wrong.
- Generated markdown headings currently include leading spaces (e.g., `"  # ..."`), which may violate markdown lint rules depending on configuration.
