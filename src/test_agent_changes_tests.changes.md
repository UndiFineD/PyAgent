# Changelog

## [2025-12-19] - Documentation refresh

- Refreshed companion docs to match `src/test_agent_changes_tests.py` and updated SHA256 fingerprint.

## Session 9 - 2025-01-16

### Added - Changelog Tests (20 test classes)
- `TestChangelogEntryPriority` - Tests for changelog entry priority and importance ranking
- `TestChangelogCrossReference` - Tests for changelog cross-referencing with git commits
- `TestChangelogConflictResolution` - Tests for changelog conflict resolution
- `TestChangelogTemplateCustomization` - Tests for changelog template customization
- `TestChangelogMetadataExtraction` - Tests for changelog entry metadata extraction
- `TestChangelogVersioning` - Tests for changelog versioning with semantic version bumps
- `TestChangelogEntryGrouping` - Tests for changelog entry grouping by scope
- `TestChangelogFromCommits` - Tests for changelog generation from commit messages
- `TestChangelogDeduplication` - Tests for changelog entry deduplication
- `TestChangelogFormatMigration` - Tests for changelog format migration between versions
- `TestChangelogApprovalWorkflow` - Tests for changelog entry approval workflows
- `TestReleaseNotesIntegration` - Tests for changelog integration with release notes
- `TestIssuePRLinking` - Tests for changelog entry linking to issues/PRs
- `TestChangelogPerformance` - Tests for changelog performance with large histories
- `TestChangelogBackupRecovery` - Tests for changelog backup and recovery
- `TestChangelogAuthentication` - Tests for changelog entry authentication and signing
- `TestChangelogArchival` - Tests for changelog entry archival
- `TestChangelogSearchFiltering` - Tests for changelog entry search and filtering
- `TestChangelogTagging` - Tests for changelog entry tagging
- `TestChangelogNotificationTriggers` - Tests for changelog entry notification triggers

---

- 2025-12-15: Added pytest-friendly replacement for the prior dotted filename (`test_agent-changes.tests.py`) to avoid pytest import/collection hazards.
- [2025-12-18] - Documentation refresh
