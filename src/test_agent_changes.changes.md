# Changelog

## [2025-12-19] - Documentation refresh

- Refreshed companion docs to match `src/test_agent_changes.py` and updated SHA256 fingerprint.

## [2025-12-18] - Documentation refresh

- Refreshed companion docs to match `src/test_agent_changes.py` and updated SHA256 fingerprint.

## Session 9 - 2025-01-16

### Added - Changelog Tests (20 test classes)
- `TestVersionRangeQueries` - Tests for changelog version range queries
- `TestChangelogKeywordSearch` - Tests for changelog entry search by keyword
- `TestChangelogExportFormats` - Tests for changelog export to different formats
- `TestIssueTrackerLinking` - Tests for changelog entry linking to issue trackers
- `TestChangelogStatistics` - Tests for changelog statistics generation
- `TestChangelogValidationRules` - Tests for changelog entry validation rules
- `TestChangelogInternationalization` - Tests for changelog internationalization
- `TestChangelogPriorityOrdering` - Tests for changelog entry priority ordering
- `TestChangelogBackupRestore` - Tests for changelog backup and restore
- `TestChangelogCategoryFiltering` - Tests for changelog entry filtering by category
- `TestChangelogDiffVisualization` - Tests for changelog diff visualization
- `TestChangelogTimestamps` - Tests for changelog entry timestamps
- `TestChangelogAccessControl` - Tests for changelog access control
- `TestChangelogBulkOperations` - Tests for changelog entry bulk operations
- `TestChangelogNotifications` - Tests for changelog notifications
- `TestChangelogApprovalWorkflows` - Tests for changelog entry approval workflows
- `TestChangelogEntrySigning` - Tests for changelog entry signing
- `TestChangelogArchivalRetention` - Tests for changelog archival and retention
- `TestChangelogEntryComments` - Tests for changelog entry comments
- `TestChangelogHistoryTracking` - Tests for changelog entry history tracking

---

- Initial version of test_agent_changes.py
- 2025-12-15: Replaced placeholder-only tests with real coverage for keyword fallback vs `BaseAgent` delegation.

## [2025-12-15]
- Rename the file to be pytest-importable (avoid '-' and extra '.'), then update references. (Fixed)

## [2025-12-16] Fixed Improvements
- Add tests for Keep a Changelog format validation.
- Test version parsing and semantic versioning.
- Add tests for git history integration.
- Test changelog entry categorization.
- Add tests for changelog diffing and comparison.
- Add tests for markdown formatting preservation.
- Test error handling for malformed changelogs.
- Add tests for associated file detection across languages.
- Test duplicate version detection and warnings.
- Add parametrized tests for various changelog formats.
- Test date format validation in version headers.
- Test changelog merging and conflict resolution.
- Add tests for custom changelog templates.

