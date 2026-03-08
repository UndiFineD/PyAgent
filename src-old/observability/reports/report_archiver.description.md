# Description: src/observability/reports/report_archiver.py

Module overview:
- `ReportArchiver` provides in-memory archive management for report snapshots with retention and cleanup.
- Methods include `archive`, `list_archives`, `get_archive`, and `cleanup_expired`.

Behavioral notes:
- Uses `ArchivedReport` objects to represent archived entries and stores them in an in-memory dict keyed by file path.
