# Errors & limitations: `agent-context.py`

This document captures known limitations and common failure modes for
`src/agent-context.py` based on the current implementation.

## LLM / Copilot integration

- `ContextAgent` delegates to `BaseAgent.improve_content()`; if Copilot/LLM tooling is missing or fails, behavior depends on `BaseAgent`.
- `_get_fallback_response()` returns a placeholder block, but “preserve existing content on failure” is handled in `BaseAgent`.

## Source-file enrichment

- Source file may not be found: `ContextAgent` derives a source path by checking a fixed list of extensions next to the `.description.md` file.
- Source read failures are silent: `OSError` and `UnicodeDecodeError` while reading the derived source file are caught and ignored.
- Truncation is fixed: only the first ~8000 characters of source code are appended to the prompt.

## Content templates

- Default template placeholder is not expanded: `_get_default_content()` returns a template containing `{filename}` without formatting it.

## Validation behavior

- Extension “validation” is best-effort: non-`.description.md` inputs are not rejected, and `_validate_file_extension()` currently does not warn.
- Validation rules are regex-based: `validate_content()` operates on raw markdown text and can produce false positives/negatives.

## Usage expectations

- Import path expectations: the module imports `base_agent` as a top-level import; running from an unexpected working directory can break imports unless `PYTHONPATH` is set appropriately.
