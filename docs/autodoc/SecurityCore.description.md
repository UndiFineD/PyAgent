# Description: `SecurityCore.py`

## Module purpose

SecurityCore logic for workspace safety.
Combines scanning for secrets, command auditing, shell script analysis, and injection detection.
This is designed for high-performance static analysis and future Rust migration.

## Location
- Path: `src\logic\coder\core\SecurityCore.py`

## Public surface
- Classes: SecurityCore
- Functions: (none)

## Behavior summary
- Invokes external commands via `subprocess`.

## Key dependencies
- Top imports: `__future__`, `re`, `logging`, `time`, `pathlib`, `typing`, `src.logic.coder.models.SecurityIssueType`, `src.logic.coder.models.SecurityVulnerability`, `src.infrastructure.backend.LocalContextRecorder`

## Metadata

- SHA256(source): `218bbfc321d83e9c`
- Last updated: `2026-01-11 10:16:44`
- File: `src\logic\coder\core\SecurityCore.py`