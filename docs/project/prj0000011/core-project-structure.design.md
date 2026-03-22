# core-project-structure — Design

_Status: COMPLETE_
_Designer: @3design | Updated: 2026-03-22_

## Selected Design

### Directory Layout
```
src/
  core/
  agents/
  tools/
  interface/
tests/
  structure/
  ci/
scripts/
docs/
  project/
  agents/
  architecture/
  api/
```

### Setup Script Interface
```
python scripts/setup_structure.py [--root <path>]
```
- Default root: repository root (detected from `__file__`).
- Creates missing directories; skips existing ones (idempotent).
- Exits `0` on success, `1` on error with clear message.

### Pytest Verification
`tests/structure/test_project_structure.py` — checks each expected directory and
key scaffold files exist. Runs in CI as part of the smoke suite.

## Interface Decisions
- `setup_structure.py` uses only the standard library (no external deps).
- Test module uses `pathlib.Path` for cross-platform compatibility.
- No side effects on import; all work in `if __name__ == "__main__"` or via `main()`.
