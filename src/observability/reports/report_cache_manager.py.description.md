# Description: src/observability/reports/report_cache_manager.py

Module overview:
- `ReportCacheManager` persists and retrieves cached report content using a JSON file on disk.
- Provides `get`, `set`, `invalidate_by_path`, and `invalidate` methods.

Behavioral notes:
- Uses `AGENT_DIR` to default the cache file location.
- Handles JSON loading errors gracefully and warns on failures.
