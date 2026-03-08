# Description: `ReportGenerator.py`

## Module purpose

Report generation logic for agent source files.

## Location
- Path: `src\classes\reports\ReportGenerator.py`

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

- SHA256(source): `d38ae204cc22ca77`
- Last updated: `2026-01-08 22:53:38`
- File: `src\classes\reports\ReportGenerator.py`