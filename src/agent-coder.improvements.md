# Improvements: `agent-coder.py`

This document tracks realistic, maintenance-oriented improvements for the
coder agent. Feature-level history belongs in `agent-coder.changes.md`.

## Updated in this pass (2025-12-18)

- Documentation accuracy:
  - Companion docs now point at `src/agent-coder.py` (not an older `scripts/...` path).
  - Description doc now reflects the actual public surface and current SHA256 fingerprint.
  - Error report now documents current validation behavior and limitations.

## Suggested next improvements

- Make style validation policy explicit:
  - Decide whether flake8 failures should block updates or remain warnings.
  - Consider aligning ignore rules with repository configuration.
- Improve temporary file cleanup visibility:
  - Log the exception (at debug/warn level) if temp-file deletion fails.
- Expand non-Python validation (optional):
  - The module already models multiple languages, but runtime validation is Python-only.
  - Consider adding opt-in validators for additional languages or file types.

## Notes

- File: `src/agent-coder.py`
