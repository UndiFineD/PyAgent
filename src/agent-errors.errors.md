# Errors & limitations: `agent-errors.py`

This document captures known limitations and common failure modes for
`src/agent-errors.py` based on the current implementation.

## LLM / Copilot integration

- `ErrorsAgent.improve_content()` delegates to `BaseAgent.improve_content()`.
- If Copilot/LLM tooling is missing or fails, behavior depends on `BaseAgent`.
- `_get_fallback_response()` exists, but preserving existing content on failure is primarily handled by `BaseAgent`.

## File naming and association

- Non-`.errors.md` inputs are allowed: the agent warns if the file does not end with `.errors.md` but does not abort.

- Associated code-file lookup is best-effort: `_check_associated_file()` searches only the same directory and checks a small set of extensions (`.py`, `.sh`, `.js`, `.ts`, `.md`) in addition to an exact match.
- If the related code file is elsewhere or uses an unsupported extension, the agent logs a warning and continues.

## Analysis features are in-memory only

- Most “error management” features are not automatically populated from the

  markdown file.
- The class provides APIs like `add_error()`, `cluster_similar_errors()`, `deduplicate_errors()`, `calculate_statistics()`, `export_errors()`, etc.
- The module does not, by itself, parse an existing `.errors.md` into structured `ErrorEntry` objects.

## Export format limitations

- `export_errors(format="csv")` emits a simple comma-separated line per error.
- Fields are not CSV-escaped; messages containing commas/newlines/quotes may produce invalid CSV.
