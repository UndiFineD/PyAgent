# core-project-structure — Think

_Status: COMPLETE_
_Thinker: @2think | Updated: 2026-03-22_

## Problem Statement
PyAgent needs a reproducible, testable directory layout so all contributors and
agents work from the same structural baseline. Without a verified structure,
scripts, tests, and CI fail in unpredictable ways on fresh checkouts.

## Key Constraints
- Repository root is `C:\Dev\PyAgent` (Windows); paths must be cross-platform.
- Structure must be verifiable by `pytest` without side effects.
- Setup script must be idempotent (re-running on an existing layout is safe).

## Options Explored

### Option A — Pytest fixtures only
Create directories as pytest fixtures, verify them. No setup script.
**Risk:** Structure only exists during test run; fresh workspace users need manual steps.

### Option B — Setup script + pytest verification (SELECTED)
`scripts/setup_structure.py` creates the canonical layout. Tests verify it exists.
CI runs the script, then the tests.
**Benefit:** Reproducible workspace, tested structure, no manual steps.

### Option C — Makefile targets
Use `Makefile` to create structure.
**Risk:** Makefile not universally available on Windows.

## Decision
Option B selected. The setup script approach gives the best reproducibility on
Windows without requiring non-standard tooling.
