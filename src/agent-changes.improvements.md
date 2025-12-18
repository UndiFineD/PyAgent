# Improvements: `agent-changes.py`

This document tracks realistic, maintenance-oriented improvements for the
changes/changelog agent. Feature-level history belongs in `agent-changes.changes.md`.

## Updated in this pass (2025-12-18)

- Documentation accuracy:
  - Companion docs now point at `src/agent-changes.py` (not an older `scripts/...` path).
  - Description doc now reflects the actual public surface and current SHA256 fingerprint.
  - Error report now documents the current LLM-bypass behavior in `improve_content()`.

## Suggested next improvements

- Remove the keyword-triggered LLM bypass:
  - `improve_content()` should only fall back when the LLM path is unavailable or fails,
    not based on prompt keywords.
- Make associated-file discovery more robust:
  - Expand the extension list and/or make it configurable via an environment variable.
  - Guard filesystem probes (`Path.exists()`) against unexpected exceptions.
- Tighten typing and default factories:
  - Replace `field(default_factory=lambda: {})` and similar patterns with typed helper
    factories to reduce static-analysis “Unknown” propagation.

## Notes

- File: `src/agent-changes.py`
