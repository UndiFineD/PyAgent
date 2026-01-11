# Description: `fix_codebase.py`

## Module purpose

Utility to repair corrupted source files by uncommenting essential system imports.
Part of the Fleet Healer autonomous recovery pattern.

## Location
- Path: `infrastructure\dev\scripts\fix_codebase.py`

## Public surface
- Classes: (none)
- Functions: uncomment_lines

## Behavior summary
- Has a CLI entrypoint (`__main__`).
- Invokes external commands via `subprocess`.

## Key dependencies
- Top imports: `os`, `re`

## Metadata

- SHA256(source): `3eef04bc664761be`
- Last updated: `2026-01-11 12:53:26`
- File: `infrastructure\dev\scripts\fix_codebase.py`