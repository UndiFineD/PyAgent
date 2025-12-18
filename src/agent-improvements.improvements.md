# Improvements: `agent-improvements.py`

This document tracks realistic, maintenance-oriented improvements for
`src/agent-improvements.py`. Feature history belongs in
`agent-improvements.changes.md`.

## Updated in this pass (2025-12-18)

- Documentation accuracy:
  - Companion docs now point at `src/agent-improvements.py` (not `scripts/...`).
  - Description doc reflects the current public surface and current SHA256 fingerprint.
  - Error report documents current limitations and failure modes.

## Suggested next improvements

### Parse `.improvements.md` into structured data

- `ImprovementsAgent` provides rich in-memory APIs (`add_improvement()`, dependencies, analytics, export), but it does not parse an existing markdown report into `Improvement` objects.
- Add a parser (and serializer) to round-trip between markdown and structured entries.

### Make associated-file discovery more robust

- Expand the extension list (or make it configurable) and consider searching adjacent directories.

### Validate/normalize LLM output

- `improve_content()` requests checkboxes and priority grouping, but the output is not validated. Consider adding lightweight structural validation or a normalization pass.

### Tighten type-checking and remove obvious generation artifacts

- There are duplicated decorators (e.g. `@dataclass`) and a number of `# type: ignore[assignment]` annotations. Cleaning these up would improve static analysis and reduce linter noise.

## Notes

- File: `src/agent-improvements.py`
