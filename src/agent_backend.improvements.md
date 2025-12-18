# Improvements: `agent_backend.py`

This document tracks realistic, maintenance-oriented improvements for the
backend layer. Feature-level history belongs in `agent_backend.changes.md`.

## Updated in this pass (2025-12-18)

- Documentation accuracy:
  - Companion docs now point at `src/agent_backend.py` (not an older `scripts/...` path).
  - Description doc now lists the actual public entry points (`run_subagent`, `llm_chat_via_github_models`, `get_backend_status`, `describe_backends`).
  - Updated SHA256 fingerprint.

## Suggested next improvements

- Make optional dependency behavior explicit:
  - The module optionally imports `requests`. Consider adding an explicit `HAS_REQUESTS` flag (like in `agent.py`) so callers and logs can be clearer about which backends are available.
- Tighten default factories:
  - Several dataclass fields currently use `field(default_factory=lambda: {})`. Switching to typed helper factories would reduce Pylance “Unknown” propagation.
- Narrow exception handling:
  - Some sections use broad `except Exception`. Tightening to the expected exceptions improves debuggability.

## Notes

- File: `src/agent_backend.py`
