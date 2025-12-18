# Improvements: `agent-stats.py`

This document tracks realistic, maintenance-oriented improvements for
`src/agent-stats.py`. Feature history belongs in `agent-stats.changes.md`.

## Updated in this pass (2025-12-18)

- Documentation accuracy:
  - Companion docs now point at `src/agent-stats.py` (not an older
    `scripts/...` path).
  - Description doc reflects the current public surface and current SHA256
    fingerprint.
  - Error report documents current limitations and failure modes.

## Suggested next improvements

### Fix obvious CLI/help text issues

- `main()` still includes an epilog example referencing an older
  `scripts/agent/agent-stats.py` path and odd spacing. Update the epilog to match
  the real location and typical usage.

### Make error handling more consistent

- Catch and report common runtime failures (JSON decode errors, file I/O errors,
  sqlite exceptions) with a clear exit code and message, similar to the existing
  `ValueError` handling.

### Separate “CLI stats” from “metrics platform”

- The module contains a large set of in-memory types (alerts, rollups,
  federation, streaming helpers) that the CLI does not currently use. Consider
  splitting into:
  - a small CLI-focused module
  - a library module for the richer metrics API

### Add tests around filesystem expectations

- Add unit tests covering:
  - filtering missing input files
  - companion-file detection based on `stem`
  - CSV output formatting
  - export formats (including sqlite)

## Notes

- File: `src/agent-stats.py`
