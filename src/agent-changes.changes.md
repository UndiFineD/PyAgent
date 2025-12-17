# Changelog

- Initial version of agent-changes.py
- 2025-12-15: No functional changes in this iteration; documentation and test coverage refreshed.

## [2025-12-15]
- Added detailed logging for changelog improvement process.
- Added explicit type hints to `__init__`.
- Function `__init__` is missing type annotations. (Fixed)

## [2025-12-16]
- Implement `ChangelogValidator` class with regex patterns for Keep a Changelog format validation. (Fixed)
- Add semantic version parsing using `semantic_version` or `packaging` library. (Fixed)
- Create `validate_changelog_structure()` method to verify section hierarchy (h2 for versions, h3 for categories). (Fixed)
- Add pre-save validation hook in `improve_content()` to reject malformed output before writing. (Fixed)
- Validate date formats in version headers (YYYY-MM-DD pattern). (Fixed)
- Check for duplicate version entries and warn user. (Fixed)
- Ensure all version entries have at least one change category (Added, Changed, etc.). (Fixed)
- Wrap `candidate.exists()` calls in `_check_associated_file()` with try-except for `PermissionError` and `OSError`. (Fixed)
- Add exponential backoff retry mechanism (3 attempts) for AI/Copilot API calls with configurable delay. (Fixed)
- Implement 30-second timeout for `subprocess.run()` in AI request calls. (Fixed)
- Add fallback content preservation when AI enhancement fails mid-process. (Fixed)
- Handle `FileNotFoundError` when reading associated code files for context. (Fixed)
- Add validation for empty or whitespace-only AI responses. (Fixed)
- Log detailed error context including file path, operation type, and stack trace. (Fixed)
- Extend supported extensions to: `.java`, `.cpp`, `.c`, `.h`, `.go`, `.rs`, `.rb`, `.php`, `.kt`, `.swift`. (Fixed)
- Add `CHANGELOG_EXTENSIONS` environment variable for custom extension lists (colon-separated). (Fixed)
- Implement recursive parent directory search (up to 2 levels) for associated files. (Fixed)
- Add fuzzy matching for file names (handle underscores vs hyphens, case variations). (Fixed)
- Support multi-file projects: detect `__init__.py`, `index.js`, or `main.go` as primary files. (Fixed)
- Cache associated file lookups to avoid repeated filesystem operations. (Fixed)

## [2025-06-02]
- Implement changelog merge detection: handle merge conflicts gracefully with `detect_merge_conflicts()` and `resolve_merge_conflict()` methods. (Fixed)
- Add support for changelog templates for different project types (Python, JavaScript, Generic) with `set_template()` and `create_custom_template()`. (Fixed)
- Implement changelog preview mode before committing changes with `enable_preview_mode()`, `disable_preview_mode()`, and `preview_changes()`. (Fixed)
- Add support for changelog versioning strategies (SemVer, CalVer) with `VersioningStrategy` enum and `generate_next_version()`. (Fixed)
- Implement changelog entry validation with customizable rules via `ValidationRule` dataclass and `validate_entry()`. (Fixed)
- Add support for changelog entry categorization with custom tags via `ChangelogEntry` dataclass. (Fixed)
- Implement changelog statistics (entries per version, contributor counts) with `calculate_statistics()`. (Fixed)
- Implement changelog entry deduplication across versions with `deduplicate_entries()`. (Fixed)
- Add support for changelog entry priority and severity levels in `ChangelogEntry` dataclass with `get_entries_by_priority()`. (Fixed)
- Add `ChangelogTemplate` dataclass for template management. (Fixed)
- Add `format_entries_as_markdown()` for generating formatted changelog output. (Fixed)
- Add 55+ new unit tests for template management, versioning, preview mode, merge detection, validation, statistics, and entry management. (Fixed)

## [2025-01-13] - Session 6 Advanced Changelog Management Tools

### New Enums (6)
- `LocalizationLanguage`: Supported languages for changelog localization (en, es, fr, de, ja, zh, pt). (Added)
- `DiffViewMode`: Modes for changelog diff visualization (unified, side_by_side, inline). (Added)
- `ImportSource`: External sources for changelog import (github_releases, jira, gitlab, manual). (Added)
- `ComplianceCategory`: Categories for compliance checking (security, legal, privacy, accessibility). (Added)
- `FeedFormat`: Feed format types for RSS/Atom generation (rss_20, atom_10, json_feed). (Added)
- `GroupingStrategy`: Strategies for entry grouping (by_date, by_version, by_category, by_author). (Added)

### New Dataclasses (9)
- `LocalizedEntry`: Changelog entry with localization support including translations dictionary. (Added)
- `DiffResult`: Result of changelog diff comparison with additions, deletions, and similarity score. (Added)
- `ImportedEntry`: Entry imported from external source with source, external_id, and labels. (Added)
- `SearchResult`: Result from changelog search with version, line number, context, and match score. (Added)
- `LinkedReference`: Linked reference to commit or issue with ref_type, ref_id, and URL. (Added)
- `MonorepoEntry`: Changelog entry for monorepo aggregation with package_name, version, and entries. (Added)
- `ReleaseNote`: Generated release notes with version, title, summary, highlights, and breaking changes. (Added)
- `ComplianceResult`: Result of compliance checking with category, passed status, issues, and recommendations. (Added)
- `EntryTemplate`: Template for changelog entries with placeholders and description. (Added)

### New Helper Classes (11)
- `ChangelogLocalizer`: Handles changelog localization to multiple languages with translation support. (Added)
- `DiffVisualizer`: Visualizes changelog differences with unified, side-by-side, and inline modes. (Added)
- `ExternalImporter`: Imports changelog entries from GitHub releases, JIRA, and other sources. (Added)
- `ChangelogSearcher`: Searches changelog content with relevance scoring and version tracking. (Added)
- `ReferenceLinkManager`: Manages links to commits and issues in changelog entries. (Added)
- `MonorepoAggregator`: Aggregates changelogs for monorepo setups into unified changelog. (Added)
- `ReleaseNotesGenerator`: Generates release notes with highlights and breaking changes. (Added)
- `FeedGenerator`: Generates RSS 2.0, Atom 1.0, and JSON Feed from changelog entries. (Added)
- `ComplianceChecker`: Checks changelog compliance with security and legal requirements. (Added)
- `EntryReorderer`: Reorders and groups changelog entries by various strategies. (Added)
- `TemplateManager`: Manages entry templates with placeholders and template application. (Added)

### Key Features Implemented
- Changelog localization to 7 languages with translation management. (Fixed)
- Diff visualization with side-by-side comparison and HTML rendering. (Fixed)
- Import from external sources (GitHub releases, JIRA) with entry conversion. (Fixed)
- Search across changelog history with relevance scoring. (Fixed)
- Entry linking to commits and issues with formatted references. (Fixed)
- Monorepo changelog aggregation with unified output. (Fixed)
- Release notes generation with highlights and breaking change extraction. (Fixed)
- RSS/Atom/JSON feed generation from changelog. (Fixed)
- Compliance checking for security and legal requirements. (Fixed)
- Entry reordering and grouping by multiple strategies. (Fixed)
- Entry templates with placeholder support. (Fixed)

### Documentation
- All new classes include comprehensive Google-style docstrings. (Added)
- Each class includes usage examples in docstrings. (Added)
- All methods documented with Args, Returns, and type hints. (Added)
