# Changelog

## [2025-12-18] - Documentation refresh

- Updated docs to match current behavior (scans `src/*.py`, emits companion markdown files into `src/`).
- Corrected stale dependency/behavior claims in companion docs.
- Refreshed SHA256 fingerprint in the description doc.

- 2025-12-15: Added report generation for each `src/*.py` into `*.description.md`, `*.errors.md`, and `*.improvements.md`.

## Session 8 [2025-12-16]

### Added - Session 8 Enums

- `SubscriptionFrequency` enum: IMMEDIATE, HOURLY, DAILY, WEEKLY
- `PermissionLevel` enum: NONE, READ, WRITE, ADMIN
- `ExportFormat` enum: JSON, HTML, PDF, CSV
- `LocaleCode` enum: EN_US, DE_DE, FR_FR, ES_ES
- `AuditAction` enum: CREATE, READ, UPDATE, DELETE, EXPORT

### Added - Session 8 Dataclasses

- `ReportSubscription`: Subscription for report delivery with frequency, email, patterns
- `ArchivedReport`: Archived report with retention policy and metadata
- `ReportAnnotation`: Annotation on report with author, content, line_number
- `ReportSearchResult`: Search result with file_path, match_text, score
- `ReportMetric`: Custom metric with name, value, unit, threshold, trend
- `ReportPermission`: Permission for access control with user_id, level, expiry
- `AuditEntry`: Audit log entry with action, user, timestamp, details
- `LocalizedString`: Localized string with translations by locale
- `ValidationResult`: Validation result with errors, warnings, checksum
- `AggregatedReport`: Combined report from multiple sources

### Added - Session 8 Helper Classes

- `SubscriptionManager`: Manager for subscriptions and scheduled delivery
- `ReportArchiver`: Archive manager with retention policies
- `AnnotationManager`: Manager for report annotations and comments
- `ReportSearchEngine`: Full-text search across historical reports
- `MetricsCollector`: Collector for custom metrics and KPIs
- `AccessController`: Controller for report access permissions
- `ReportExporter`: Exporter for multiple formats (HTML, CSV, JSON)
- `AuditLogger`: Logger for audit trail and compliance
- `ReportValidator`: Validator for data integrity and checksums
- `ReportLocalizer`: Localizer for internationalization (i18n)
- `ReportAPI`: API for programmatic report access
- `ReportScheduler`: Scheduler with cron-like expressions
- `ReportAggregator`: Aggregator for combining reports from multiple sources

## Session 6 [2025-01-13]

### Added - Type-Safe Enums

- `ReportType` enum: DESCRIPTION, ERRORS, IMPROVEMENTS, SUMMARY
- `ReportFormat` enum: MARKDOWN, JSON, HTML
- `SeverityLevel` enum: INFO, WARNING, ERROR, CRITICAL
- `IssueCategory` enum: SYNTAX, TYPE_ANNOTATION, STYLE, SECURITY, PERFORMANCE, DOCUMENTATION

### Added - Dataclasses for Structured Data

- `CodeIssue` dataclass: Issue with message, category, severity, line_number, file_path
- `ReportMetadata` dataclass: Metadata with path, generated_at, content_hash, version
- `ReportTemplate` dataclass: Template with name, sections, include_metadata, include_summary
- `ReportCache` dataclass: Cache entry with path, hash, content, created_at, ttl_seconds
- `ReportComparison` dataclass: Comparison with old_path, new_path, added, removed, changed, unchanged_count
- `FilterCriteria` dataclass: Filter with categories, min_severity, date_from, date_to, file_patterns

### Added - ReportCacheManager Class

- `_load_cache()`: Load cache from disk
- `_save_cache()`: Persist cache to disk
- `get()`: Get cached report if valid (not expired)
- `set()`: Cache report data with TTL
- `invalidate()`: Invalidate cache entries by path or pattern

### Added - ReportComparator Class

- `compare()`: Compare two report versions and generate diff
- `_extract_items()`: Extract list items from markdown content for comparison

### Added - ReportFilter Class

- `matches()`: Check if issue matches filter criteria
- `filter_issues()`: Filter list of issues by criteria

## [2025-12-16]

- Add logging for all major actions. (Fixed)
- Add type hints for all methods. (Fixed)
- Add comprehensive docstrings for all methods following Google style format. (Fixed)
- Refactor: Split report generators into separate modules. (Fixed)
- Add support for generating reports in multiple formats: HTML, PDF, markdown, JSON. (Fixed)
- Implement incremental report generation (only analyze changed files). (Fixed)
- Add report caching to avoid re-generating unchanged sections. (Fixed)
- Implement report customization: user-selectable sections and metrics. (Fixed)
- Generate visual reports: graphs, charts, heatmaps using matplotlib/seaborn. (Fixed)
- Add executive summary generation with key metrics and trends. (Fixed)
- Implement report templating for consistent formatting and branding. (Fixed)
- Add git integration: show authors, commit history, blame information. (Fixed)
- Generate cross-file analysis reports: dependencies, imports, coupling. (Fixed)
- Add test coverage integration: show coverage trends and gap analysis. (Fixed)
- Implement performance metrics collection and reporting. (Fixed)
- Add technical debt quantification and prioritization. (Fixed)
- Generate recommendations based on report analysis. (Fixed)
- Support report scheduling and automated generation. (Fixed)
- Add report versioning and change tracking. (Fixed)
- Implement report distribution: email, webhook, API endpoints. (Fixed)
- Add interactive report generation with filtering and drill-down. (Fixed)
- Support team-level reporting: aggregate metrics across developers. (Fixed)

## [2025-12-15]

- Added detailed logging for report generation process.
- Added explicit type hints to `main`.
- Add `--help` examples and validate CLI args (paths, required files). (Fixed)
- Fixed exception handling in `generate_agent_reports.py` (robust file reading).
