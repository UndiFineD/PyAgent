# Description: src/observability/reports/report_cache.py

Module overview:
- `ReportCache` dataclass represents a cached report entry with metadata such as path, content hash, TTL, and creation timestamp.

Behavioral notes:
- Simple in-memory data container; persistence and management are handled by `ReportCacheManager`.
