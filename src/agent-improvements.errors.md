# Errors & limitations: `agent-improvements.py`

This document captures known limitations and common failure modes for
`src/agent-improvements.py` based on the current implementation.

## LLM / Copilot integration

- `ImprovementsAgent.improve_content()` delegates to `BaseAgent.improve_content()`.
- If Copilot/LLM tooling is missing or fails, behavior depends on `BaseAgent`.
- `_get_fallback_response()` exists, but preserving existing content on failure
  is primarily handled by `BaseAgent`.

## File naming and association

- Non-`.improvements.md` inputs are allowed: the agent warns if the file does
  not end with `.improvements.md` but does not abort.
- Associated code-file lookup is best-effort: `_check_associated_file()` searches
  only the same directory and checks a small set of extensions (`.py`, `.sh`,
  `.js`, `.ts`, `.md`) in addition to an exact match.
- If the related code file is elsewhere or uses an unsupported extension, the
  agent logs a warning and continues.

## Management features are in-memory only

- The module provides rich APIs (`add_improvement()`, dependency handling,
  scheduling helpers, analytics, export, etc.), but it does not parse an
  existing `.improvements.md` into structured `Improvement` objects.
- Unless external code populates `self._improvements`, methods like
  `prioritize_improvements()` and `calculate_analytics()` operate on an empty
  list.

## Output format limitations

- The prompt augmentation encourages checkboxes and priority grouping, but the
  result is not validated for schema/structure.
- `export_improvements(format="markdown")` emits a simple markdown format; it is
  not guaranteed to match any existing project-specific template.

## Code quality footguns

- There are a few obvious “generated code” artifacts (e.g., duplicated
  decorators like `@dataclass` in places). These may affect type checking or
  linters but are not handled here.
