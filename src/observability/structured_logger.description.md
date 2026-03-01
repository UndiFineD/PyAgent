# Description: src/observability/structured_logger.py

Module purpose:
- Implements `StructuredLogger`, a JSON-based logger that masks sensitive values and writes structured log entries to disk.
- Attempts to leverage `rust_core` acceleration for masking and building log entries when available.

Primary classes:
- `StructuredLogger`: main logging abstraction with methods `info`, `error`, `warning`, `debug`, and `success`.

Behavioral notes:
- Masks sensitive patterns (API keys, bearer tokens, GitHub tokens) before writing.
- Compresses logs older than a size threshold and rotates to gzipped archives.
- Writes both to standard Python logging and to a structured log file `data/logs/structured.json` by default.
