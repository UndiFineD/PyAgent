# Errors: `agent-changes.py`

This file tracks known issues and limitations in `src/agent-changes.py`.

## Known issues

- LLM bypass for common prompts:
  - `ChangesAgent.improve_content()` returns a “suggestions” fallback when the user prompt
    contains keywords like `improve`, `change`, or `log`.
  - This behavior can prevent the LLM-backed improvement path from running for typical usage.

## Limitations / footguns

- Associated file detection is limited:
  - `_check_associated_file()` only tries `.py`, `.sh`, `.js`, `.ts`, `.md`.
- Filesystem edge cases:
  - `_check_associated_file()` calls `Path.exists()` without guarding against unexpected
    filesystem errors (e.g., permissions/network shares).
- Import path expectations:
  - The module imports `BaseAgent` via `from base_agent import ...`; the runtime must
    have the repo’s `src/` on `sys.path` (or otherwise resolve that import).

## Status

- Last reviewed: 2025-12-18
