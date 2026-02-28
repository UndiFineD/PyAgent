# Description: src/observability/reports/report_generator.py

Module overview:
- Implements `ReportGenerator`, which parses Python source files and generates description, error, and improvement reports.
- Handles deduplication, JSONL export, and a simple dashboard generator.

Primary class:
- `ReportGenerator`: orchestrates iterating .py files, parsing AST, running compile checks, and writing report markdown files.

Behavioral notes:
- Uses `StructuredLogger` for logging.
- Writes three markdown outputs per processed file: `{stem}.description.md`, `{stem}.errors.md`, `{stem}.improvements.md`.
- Skips unchanged files by comparing a SHA of the source.
