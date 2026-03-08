# Description: src/observability/reports/report_filter.py

Module overview:
- `ReportFilter` filters `CodeIssue` objects based on a `FilterCriteria` (severity, categories).
- Exposes `matches` and `filter_issues` methods.

Behavioral notes:
- Simple predicate-based filtering; relies on `FilterCriteria` and `CodeIssue` definitions.
