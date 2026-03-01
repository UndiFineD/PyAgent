# Improvements: src/observability/reports/report_generator.py

Potential improvements:
- Add unit tests for parsing edge cases, large files, and files with syntax errors.
- Expose smaller helper methods as public utilities to make them more testable (e.g., `_try_parse_python`).
- Allow injecting a custom AST visitor or ruleset for project-specific checks.
- Improve performance by parallelizing file processing (use `concurrent.futures` or `asyncio` with IO-bound operations).
- Add richer metadata to exported JSONL (git author, last modified time) and make deduplication pluggable.
- Avoid writing to the same output directory as source to make reports clearer and to avoid accidental source pollution.
