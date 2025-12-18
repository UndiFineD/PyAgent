# Errors: `base_agent.py`

## Scope
This file is a shared foundation; errors here typically surface across many agent commands.
The list below focuses on realistic runtime failures and edge cases.

## Import / environment errors
- `agent_backend` import failure: the module attempts a fallback `sys.path` adjustment, but a broken environment can still prevent import.
- Optional markdown fixer import failure: `fix_markdown_content` is best-effort and falls back to a no-op when unavailable.

## File I/O errors
- Read failures: invalid paths, permissions, missing files, or encoding issues when reading existing content.
- Write failures: permissions, locked files, or missing parent directories (parent directory creation is attempted).

## Backend / AI errors
- Backend unavailable or misconfigured: `run_subagent()` may return `None` and the agent falls back to original content or a help-text fallback.
- Poor response quality: the agent may retry based on heuristics and `DV_AGENT_RETRY_COUNT`.
- Large prompts: context/history can increase prompt size; content may be truncated by the backend.

## Hook / plugin hazards
- Event hooks can raise exceptions; these are caught and logged so they do not stop the main flow.

## State persistence errors
- `save_state()` writes JSON and can fail due to permissions/disk issues.
- `load_state()` may fail for invalid JSON; it logs a warning and returns `False`.
