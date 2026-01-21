# Description: `core.py`

## Module purpose

Foundation for high-performance 'Core' components.
These classes are designed to be eventually implemented in Rust (using PyO3 or FFI).
They should remain as 'pure' as possible - no complex dependencies on AI or IO.

## Location
- Path: `core\base\core.py`

## Public surface
- Classes: CodeQualityReport, BaseCore, LogicCore
- Functions: (none)

## Behavior summary
- Pure module (no obvious CLI / side effects).

## Key dependencies
- Top imports: `__future__`, `difflib`, `fnmatch`, `hashlib`, `logging`, `os`, `re`, `dataclasses`, `typing`, `pathlib`

## Metadata

- SHA256(source): `e930d89e0b9a2d36`
- Last updated: `2026-01-11 12:52:54`
- File: `core\base\core.py`