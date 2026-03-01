# Improvements: src/observability/reports/report_exporter.py

Potential improvements:
- Replace ad-hoc markdown-to-HTML conversion with a robust library like `markdown` or `marko` to support full syntax.
- Add unit tests for `to_html` and `to_csv` with varied inputs and edge cases (special characters, quotes, newlines).
- Allow configurable CSV delimiter and quoting behavior.
- Provide async or streaming export methods for large reports to avoid loading everything into memory.
- Validate `CodeIssue` shapes and add graceful handling for missing fields.
- Add options for PDF/PPT export via third-party libraries (pandoc, weasyprint) if needed.
