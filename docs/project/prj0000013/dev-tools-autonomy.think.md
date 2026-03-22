# dev-tools-autonomy — Think

_Status: COMPLETE_
_Thinker: @2think | Updated: 2026-03-22_

## Problem Statement
PyAgent lacked tools for self-improvement: no dependency auditor to flag
outdated packages, no code-metrics collector, no plugin loader for extensibility,
and no self-healing helper to auto-fix common issues.

## Key Constraints
- Each tool is an isolated module with a minimal public API.
- Modules must be importable without side effects (no top-level I/O).
- Tests must pass without network access (dependency audit can use `pip list`
  subprocess or stdlib; must not make external HTTP calls in tests).
- Plugin loader must be safe against malicious plugin names (no `eval`).

## Options Explored

### Option A — Monolithic `tools.py`
Single file with all tool logic.
**Risk:** Difficult to test in isolation; grows unbounded.

### Option B — Standard library + subprocess approach
Use `importlib` for plugin loading, `subprocess` for `pip list`, `ast.parse` for
metrics.
**Risk:** Subprocess calls make tests slower; need to mock in CI.

### Option C — Modular files + pure-Python metrics (SELECTED)
Each tool is its own module. Metrics use `ast` module (stdlib, no subprocess).
Plugin loader uses `importlib.import_module` with allowlist validation.
**Benefit:** Testable, fast, no I/O in module scope.

## Decision
Option C selected. Modular stdlib-only approach keeps the test suite fast and
avoids external dependencies in the tools layer.
