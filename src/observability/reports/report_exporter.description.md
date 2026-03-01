# Description: src/observability/reports/report_exporter.py

Module overview:
- `ReportExporter` converts report content into various export formats (HTML, CSV, JSON) and can write to disk.
- Provides `to_html`, `to_csv`, and `export` methods for simple conversions.

Behavioral notes:
- Uses lightweight regex-based Markdown-to-HTML conversion; suitable for basic reports but not full CommonMark fidelity.
- `to_csv` expects a list of `CodeIssue` objects.

Public classes/functions:
- `ReportExporter` with methods `to_html`, `to_csv`, `export`.

