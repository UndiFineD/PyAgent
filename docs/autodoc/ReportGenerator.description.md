# Description: `ReportGenerator.py`

## Module purpose

Report generation logic for agent source files.

## Location
- Path: `src\observability\reports\ReportGenerator.py`

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

- SHA256(source): `be7ddc57b5c5c8af`
- Last updated: `2026-01-11 10:17:09`
- File: `src\observability\reports\ReportGenerator.py`