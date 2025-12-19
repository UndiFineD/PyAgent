# Description: `agent-changes.py`

## Module purpose

Improves and updates per-file changelog content (`*.changes.md`).

The agent validates the input file extension, attempts to locate an associated
source file nearby, and delegates to `BaseAgent` for LLM-backed improvements
when available.

## Location

- Path: `src/agent-changes.py`

## Public surface

- Class: `ChangesAgent(BaseAgent)`
  - `improve_content(prompt: str) -> str`
  - Changelog utilities: `set_template()`, `create_custom_template()`,
    `set_versioning_strategy()`, `generate_next_version()`,
    `validate_entry()`, `validate_changelog()`, `calculate_statistics()`,
    `add_entry()`, `format_entries_as_markdown()`, `detect_merge_conflicts()`,
    `resolve_merge_conflict()`
- CLI entry point:
  - `main` is created via `create_main_function(ChangesAgent, ...)` and executed
    under `if __name__ == "__main__":`.

## Behavior summary

- Validates that the target file name ends with `.changes.md` (logs a warning otherwise).
- Attempts to find an associated file next to the changelog:
  - exact base-name match, or
  - base-name plus one of: `.py`, `.sh`, `.js`, `.ts`, `.md`.
- Adds “Keep a Changelog” formatting guidance to prompts passed to the LLM.
- Supports preview mode (`enable_preview_mode()`, `get_preview()`, `preview_changes()`).

## Known limitations

- `ChangesAgent.improve_content()` currently has a keyword-triggered fallback
  (based on the user prompt containing words like “improve”, “change”, “log”)
  that can return suggestions without calling the LLM.
  See `src/agent-changes.errors.md`.

## File fingerprint

- SHA256(source): `e94df5c8e0cb60c8fa41720276924faf2bd4938e21e6211c1bab7f025ce318fc`
