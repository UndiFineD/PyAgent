# Improvements: `agent-context.py`

This document tracks realistic, maintenance-oriented improvements for
`src/agent-context.py`. Feature history belongs in `agent-context.changes.md`.

## Updated in this pass (2025-12-18)

- Documentation accuracy:

  - Companion docs point at `src/agent-context.py` (not an older `scripts/...` path).
  - Description doc reflects the current public surface and current SHA256 fingerprint.
  - Error report documents current limitations and failure modes.

## Suggested next improvements

- Make extension handling explicit:

  - `_validate_file_extension()` currently does not warn; emit a warning when the
    input is not a `.description.md` file.
  - Consider making the recognized source extensions configurable.

- Improve source-file read diagnostics:

  - When reading the derived source file fails (e.g. `OSError`,
    `UnicodeDecodeError`), log a debug/warn message so failures are explainable.

- Fix default template placeholder expansion:

  - `_get_default_content()` currently returns a template containing `{filename}`
    without formatting; format it consistently with `apply_template()`.

- Replace magic numbers with named constants:

  - The source truncation length (~8000 chars) should be a named constant and
    ideally configurable.

- Clarify validation semantics:

  - `validate_content()` treats non-required rules as warnings when matched;
    document the intent and consider making rule behavior more explicit.

## Notes

- File: `src/agent-context.py`
