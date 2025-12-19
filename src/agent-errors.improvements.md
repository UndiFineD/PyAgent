# Improvements: `agent-errors.py`

This document tracks realistic, maintenance-oriented improvements for
`src/agent-errors.py`. Feature history belongs in `agent-errors.changes.md`.

## Updated in this pass (2025-12-18)

- Documentation accuracy: companion docs now point at `src/agent-errors.py` (not an older `scripts/...` path).
- Documentation accuracy: description doc reflects the current public surface and current SHA256 fingerprint.
- Documentation accuracy: error report documents current limitations and failure modes.

## Suggested next improvements

- Parse `.errors.md` into structured data: add a parser/serializer to round-trip between markdown and structured `ErrorEntry` objects.

- Make associated-file discovery more robust: expand (or configure) the extension list and consider searching adjacent directories.

- Improve CSV export correctness: `export_errors(format="csv")` does not escape fields; use the `csv` module to handle quoting/newlines safely.

- Clarify Copilot failure behavior: the fallback policy is primarily in `BaseAgent`; consider documenting it in one shared place and linking to it from agent docs.

## Notes

- File: `src/agent-errors.py`
