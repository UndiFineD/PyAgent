# Description: src/observability/reports/report_comparator.py

Module overview:
- `ReportComparator` compares two report contents and returns a `ReportComparison` with added/removed/unchanged counts.
- Uses simple line-item extraction for markdown lists to determine differences.

Behavioral notes:
- Default `reports_dir` uses project `src/` root.
- The `_extract_items` method looks for markdown list items starting with `- `.
