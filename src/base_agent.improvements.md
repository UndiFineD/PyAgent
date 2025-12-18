# Improvements: `base_agent.py`

## Suggested improvements
- Split `base_agent.py` into smaller modules (models/config, BaseAgent core, batching, optional tooling) to reduce file size and review burden.
- Consider removing or parameterizing the legacy optional import path `scripts.fix.fix_markdown_lint` (prefer a single canonical location).
- `_build_prompt_with_history()` currently concatenates context lines without newlines between entries; consider joining with `"\n"` for readability.
- Add targeted tests for:

  - `read_previous_content()` behavior on missing files and invalid UTF-8.
  - `update_file()` markdown-only normalization behavior.
  - cache hit behavior and retry behavior when `_score_response_quality()` is poor.
  - `save_state()` / `load_state()` round-trip and corrupt JSON handling.

- Consider making `DV_AGENT_*` environment parsing stricter (validate ints/floats) to fail fast on invalid values.

## Notes
- This document avoids claiming test pass rates or “all fixed” status unless verified by running tests in this workspace.
- File: `src/base_agent.py`
