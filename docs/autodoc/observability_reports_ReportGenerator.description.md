# Description: `ReportGenerator.py`

## Module purpose

Report generation logic for agent source files.

## Location
- Path: `observability\reports\ReportGenerator.py`

## Public surface
- Classes: ReportGenerator
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).
- Uses `argparse` for CLI parsing.
- Invokes external commands via `subprocess`.
- Mutates `sys.path` to import sibling modules.

## Key dependencies
- Top imports: `ast`, `hashlib`, `json`, `logging`, `os`, `re`, `sys`, `time`, `pathlib`, `typing`, `CompileResult`, `subprocess`

## Metadata

- SHA256(source): `1659036422afab5a`
- Last updated: `2026-01-11 12:55:36`
- File: `observability\reports\ReportGenerator.py`