"""Tests for generate_agent_reports.py."""

from __future__ import annotations
import ast
from pathlib import Path
from typing import Any
import pytest
from agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture
def report_module() -> Any:
    with agent_dir_on_path():
        return load_agent_module("generate_agent_reports.py")


def test_sha256_text(report_module: Any) -> None:
    """Test SHA256 calculation."""
    text = "hello world"
    # echo -n "hello world" | sha256sum
    expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    assert report_module._sha256_text(text) == expected


def test_detect_cli_entry(report_module: Any) -> None:
    """Test CLI entry point detection."""
    source_with_main = 'if __name__ == "__main__":\n    main()'
    source_without_main = 'def foo(): pass'

    assert report_module._detect_cli_entry(source_with_main) is True
    assert report_module._detect_cli_entry(source_without_main) is False


def test_find_top_level_defs(report_module: Any) -> None:
    """Test finding top-level functions and classes."""
    source = """
def func1(): pass
class Class1: pass
async def func2(): pass
"""
    tree = ast.parse(source)
    funcs, classes = report_module._find_top_level_defs(tree)

    assert "func1" in funcs
    assert "async func2" in funcs
    assert "Class1" in classes


def test_is_pytest_test_file(report_module: Any) -> None:
    """Test pytest file detection."""
    assert report_module._is_pytest_test_file(Path("test_foo.py")) is True
    assert report_module._is_pytest_test_file(Path("foo_test.py")) is False
    assert report_module._is_pytest_test_file(Path("test_foo.txt")) is False


# =============================================================================
# Phase 6: Enum Tests
# =============================================================================


class TestReportTypeEnum:
    """Tests for ReportType enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        ReportType = report_module.ReportType
        assert ReportType.DESCRIPTION.value == "description"
        assert ReportType.ERRORS.value == "errors"
        assert ReportType.IMPROVEMENTS.value == "improvements"
        assert ReportType.SUMMARY.value == "summary"

    def test_enum_members(self, report_module: Any) -> None:
        """Test all enum members exist."""
        ReportType = report_module.ReportType
        members = [m.name for m in ReportType]
        assert "DESCRIPTION" in members
        assert "ERRORS" in members
        assert "IMPROVEMENTS" in members
        assert "SUMMARY" in members


class TestReportFormatEnum:
    """Tests for ReportFormat enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        ReportFormat = report_module.ReportFormat
        assert ReportFormat.MARKDOWN.value == "markdown"
        assert ReportFormat.JSON.value == "json"
        assert ReportFormat.HTML.value == "html"

    def test_all_members(self, report_module: Any) -> None:
        """Test all members are present."""
        ReportFormat = report_module.ReportFormat
        assert len(list(ReportFormat)) == 3


class TestSeverityLevelEnum:
    """Tests for SeverityLevel enum."""

    def test_enum_ordering(self, report_module: Any) -> None:
        """Test severity levels have correct ordering values."""
        SeverityLevel = report_module.SeverityLevel
        assert SeverityLevel.INFO.value < SeverityLevel.WARNING.value
        assert SeverityLevel.WARNING.value < SeverityLevel.ERROR.value
        assert SeverityLevel.ERROR.value < SeverityLevel.CRITICAL.value

    def test_all_levels(self, report_module: Any) -> None:
        """Test all severity levels exist."""
        SeverityLevel = report_module.SeverityLevel
        members = [m.name for m in SeverityLevel]
        assert "INFO" in members
        assert "WARNING" in members
        assert "ERROR" in members
        assert "CRITICAL" in members


class TestIssueCategoryEnum:
    """Tests for IssueCategory enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        IssueCategory = report_module.IssueCategory
        assert IssueCategory.SYNTAX.value == "syntax"
        assert IssueCategory.TYPE_ANNOTATION.value == "type_annotation"
        assert IssueCategory.STYLE.value == "style"
        assert IssueCategory.SECURITY.value == "security"
        assert IssueCategory.PERFORMANCE.value == "performance"
        assert IssueCategory.DOCUMENTATION.value == "documentation"

    def test_all_categories(self, report_module: Any) -> None:
        """Test all categories exist."""
        IssueCategory = report_module.IssueCategory
        assert len(list(IssueCategory)) == 6


# =============================================================================
# Phase 6: Dataclass Tests
# =============================================================================


class TestCodeIssueDataclass:
    """Tests for CodeIssue dataclass."""

    def test_creation_minimal(self, report_module: Any) -> None:
        """Test creating CodeIssue with minimal fields."""
        CodeIssue = report_module.CodeIssue
        SeverityLevel = report_module.SeverityLevel
        IssueCategory = report_module.IssueCategory

        issue = CodeIssue(
            message="Test error",
            category=IssueCategory.SYNTAX,
            severity=SeverityLevel.ERROR
        )
        assert issue.message == "Test error"
        assert issue.category == IssueCategory.SYNTAX
        assert issue.severity == SeverityLevel.ERROR
        assert issue.line_number is None
        assert issue.file_path is None

    def test_creation_full(self, report_module: Any) -> None:
        """Test creating CodeIssue with all fields."""
        CodeIssue = report_module.CodeIssue
        SeverityLevel = report_module.SeverityLevel
        IssueCategory = report_module.IssueCategory

        issue = CodeIssue(
            message="Type error",
            category=IssueCategory.TYPE_ANNOTATION,
            severity=SeverityLevel.WARNING,
            line_number=42,
            file_path="test.py"
        )
        assert issue.line_number == 42
        assert issue.file_path == "test.py"


class TestReportMetadataDataclass:
    """Tests for ReportMetadata dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ReportMetadata."""
        ReportMetadata = report_module.ReportMetadata

        metadata = ReportMetadata(
            path="test.py",
            generated_at="2025-01-13",
            content_hash="abc123",
            version="1.0.0"
        )
        assert metadata.path == "test.py"
        assert metadata.generated_at == "2025-01-13"
        assert metadata.content_hash == "abc123"
        assert metadata.version == "1.0.0"


class TestReportTemplateDataclass:
    """Tests for ReportTemplate dataclass."""

    def test_creation_with_defaults(self, report_module: Any) -> None:
        """Test creating ReportTemplate with defaults."""
        ReportTemplate = report_module.ReportTemplate

        template = ReportTemplate(
            name="default",
            sections=["description", "errors"]
        )
        assert template.name == "default"
        assert "description" in template.sections
        assert template.include_metadata is True
        assert template.include_summary is True


class TestReportCacheDataclass:
    """Tests for ReportCache dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ReportCache."""
        ReportCache = report_module.ReportCache

        cache = ReportCache(
            path="test.py",
            content_hash="abc123",
            content="Report content",
            created_at=1000.0,
            ttl_seconds=3600
        )
        assert cache.path == "test.py"
        assert cache.content_hash == "abc123"
        assert cache.content == "Report content"
        assert cache.ttl_seconds == 3600


class TestReportComparisonDataclass:
    """Tests for ReportComparison dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ReportComparison."""
        ReportComparison = report_module.ReportComparison

        comparison = ReportComparison(
            old_path="old.md",
            new_path="new.md",
            added=["- New item"],
            removed=["- Old item"],
            changed=[("- Changed from", "- Changed to")],
            unchanged_count=5
        )
        assert comparison.old_path == "old.md"
        assert comparison.new_path == "new.md"
        assert len(comparison.added) == 1
        assert len(comparison.removed) == 1
        assert len(comparison.changed) == 1
        assert comparison.unchanged_count == 5


class TestFilterCriteriaDataclass:
    """Tests for FilterCriteria dataclass."""

    def test_creation_with_defaults(self, report_module: Any) -> None:
        """Test creating FilterCriteria with defaults."""
        FilterCriteria = report_module.FilterCriteria

        criteria = FilterCriteria()
        assert criteria.categories is None
        assert criteria.min_severity is None
        assert criteria.date_from is None
        assert criteria.date_to is None
        assert criteria.file_patterns is None


# =============================================================================
# Phase 6: ReportCacheManager Tests
# =============================================================================


class TestReportCacheManager:
    """Tests for ReportCacheManager class."""

    def test_initialization(self, report_module: Any, tmp_path: Path) -> None:
        """Test cache manager initialization."""
        ReportCacheManager = report_module.ReportCacheManager

        cache_file = tmp_path / "test_cache.json"
        manager = ReportCacheManager(cache_file)
        assert manager.cache_file == cache_file
        assert manager._cache == {}

    def test_set_and_get(self, report_module: Any, tmp_path: Path) -> None:
        """Test setting and getting cache entries."""
        ReportCacheManager = report_module.ReportCacheManager

        cache_file = tmp_path / "test_cache.json"
        manager = ReportCacheManager(cache_file)

        manager.set("test.py", "abc123", "Report content", ttl=3600)
        result = manager.get("test.py", "abc123")

        assert result == "Report content"

    def test_get_expired(self, report_module: Any, tmp_path: Path) -> None:
        """Test getting expired cache entry returns None."""
        ReportCacheManager = report_module.ReportCacheManager

        cache_file = tmp_path / "test_cache.json"
        manager = ReportCacheManager(cache_file)

        manager.set("test.py", "abc123", "Report content", ttl=-1)
        result = manager.get("test.py", "abc123")

        assert result is None

    def test_get_wrong_hash(self, report_module: Any, tmp_path: Path) -> None:
        """Test getting with wrong hash returns None."""
        ReportCacheManager = report_module.ReportCacheManager

        cache_file = tmp_path / "test_cache.json"
        manager = ReportCacheManager(cache_file)

        manager.set("test.py", "abc123", "Report content", ttl=3600)
        result = manager.get("test.py", "different_hash")

        assert result is None

    def test_invalidate_by_path(self, report_module: Any, tmp_path: Path) -> None:
        """Test invalidating cache by path."""
        ReportCacheManager = report_module.ReportCacheManager

        cache_file = tmp_path / "test_cache.json"
        manager = ReportCacheManager(cache_file)

        manager.set("test.py", "abc123", "Report content", ttl=3600)
        manager.invalidate("test.py")
        result = manager.get("test.py", "abc123")

        assert result is None


# =============================================================================
# Phase 6: ReportComparator Tests
# =============================================================================


class TestReportComparator:
    """Tests for ReportComparator class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test comparator initialization."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        assert comparator is not None

    def test_compare_identical(self, report_module: Any) -> None:
        """Test comparing identical reports."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        old_content = "- Item 1\n- Item 2\n- Item 3"
        new_content = "- Item 1\n- Item 2\n- Item 3"

        result = comparator.compare("old.md", "new.md", old_content, new_content)

        assert len(result.added) == 0
        assert len(result.removed) == 0
        assert result.unchanged_count == 3

    def test_compare_with_additions(self, report_module: Any) -> None:
        """Test comparing reports with additions."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        old_content = "- Item 1\n- Item 2"
        new_content = "- Item 1\n- Item 2\n- Item 3"

        result = comparator.compare("old.md", "new.md", old_content, new_content)

        assert "- Item 3" in result.added
        assert len(result.removed) == 0

    def test_compare_with_removals(self, report_module: Any) -> None:
        """Test comparing reports with removals."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        old_content = "- Item 1\n- Item 2\n- Item 3"
        new_content = "- Item 1\n- Item 2"

        result = comparator.compare("old.md", "new.md", old_content, new_content)

        assert "- Item 3" in result.removed
        assert len(result.added) == 0

    def test_extract_items(self, report_module: Any) -> None:
        """Test extracting list items from content."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        content = "# Header\n- Item 1\n- Item 2\nSome text\n- Item 3"

        items = comparator._extract_items(content)

        assert len(items) == 3
        assert "- Item 1" in items
        assert "- Item 2" in items
        assert "- Item 3" in items


# =============================================================================
# Phase 6: ReportFilter Tests
# =============================================================================


class TestReportFilter:
    """Tests for ReportFilter class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test filter initialization."""
        ReportFilter = report_module.ReportFilter
        FilterCriteria = report_module.FilterCriteria

        criteria = FilterCriteria()
        filter_obj = ReportFilter(criteria)
        assert filter_obj.criteria == criteria

    def test_matches_by_category(self, report_module: Any) -> None:
        """Test matching issues by category."""
        ReportFilter = report_module.ReportFilter
        FilterCriteria = report_module.FilterCriteria
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        criteria = FilterCriteria(categories=[IssueCategory.SYNTAX])
        filter_obj = ReportFilter(criteria)

        syntax_issue = CodeIssue(
            message="Syntax error",
            category=IssueCategory.SYNTAX,
            severity=SeverityLevel.ERROR
        )
        style_issue = CodeIssue(
            message="Style issue",
            category=IssueCategory.STYLE,
            severity=SeverityLevel.WARNING
        )

        assert filter_obj.matches(syntax_issue) is True
        assert filter_obj.matches(style_issue) is False

    def test_matches_by_severity(self, report_module: Any) -> None:
        """Test matching issues by minimum severity."""
        ReportFilter = report_module.ReportFilter
        FilterCriteria = report_module.FilterCriteria
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        criteria = FilterCriteria(min_severity=SeverityLevel.ERROR)
        filter_obj = ReportFilter(criteria)

        error_issue = CodeIssue(
            message="Error",
            category=IssueCategory.SYNTAX,
            severity=SeverityLevel.ERROR
        )
        warning_issue = CodeIssue(
            message="Warning",
            category=IssueCategory.STYLE,
            severity=SeverityLevel.WARNING
        )

        assert filter_obj.matches(error_issue) is True
        assert filter_obj.matches(warning_issue) is False

    def test_filter_issues(self, report_module: Any) -> None:
        """Test filtering list of issues."""
        ReportFilter = report_module.ReportFilter
        FilterCriteria = report_module.FilterCriteria
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        criteria = FilterCriteria(categories=[IssueCategory.SYNTAX])
        filter_obj = ReportFilter(criteria)

        issues = [
            CodeIssue(
                message="Syntax error",
                category=IssueCategory.SYNTAX,
                severity=SeverityLevel.ERROR
            ),
            CodeIssue(
                message="Style issue",
                category=IssueCategory.STYLE,
                severity=SeverityLevel.WARNING
            ),
            CodeIssue(
                message="Another syntax error",
                category=IssueCategory.SYNTAX,
                severity=SeverityLevel.WARNING
            ),
        ]

        filtered = filter_obj.filter_issues(issues)

        assert len(filtered) == 2
        assert all(i.category == IssueCategory.SYNTAX for i in filtered)


# =============================================================================
# Phase 6: Integration Tests
# =============================================================================


class TestPhase6Integration:
    """Integration tests for Phase 6 features."""

    def test_cache_manager_with_comparator(
        self, report_module: Any, tmp_path: Path
    ) -> None:
        """Test cache manager working with comparator."""
        ReportCacheManager = report_module.ReportCacheManager
        ReportComparator = report_module.ReportComparator

        cache_file = tmp_path / "test_cache.json"
        manager = ReportCacheManager(cache_file)
        comparator = ReportComparator()

        old_report = "- Item 1\n- Item 2"
        new_report = "- Item 1\n- Item 2\n- Item 3"

        manager.set("old.md", "hash1", old_report, ttl=3600)
        cached = manager.get("old.md", "hash1")

        comparison = comparator.compare("old.md", "new.md", cached, new_report)

        assert "- Item 3" in comparison.added

    def test_filter_with_all_criteria(self, report_module: Any) -> None:
        """Test filter with multiple criteria."""
        ReportFilter = report_module.ReportFilter
        FilterCriteria = report_module.FilterCriteria
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        criteria = FilterCriteria(
            categories=[IssueCategory.SYNTAX, IssueCategory.SECURITY],
            min_severity=SeverityLevel.WARNING
        )
        filter_obj = ReportFilter(criteria)

        issues = [
            CodeIssue(
                message="Critical security issue",
                category=IssueCategory.SECURITY,
                severity=SeverityLevel.CRITICAL
            ),
            CodeIssue(
                message="Minor style issue",
                category=IssueCategory.STYLE,
                severity=SeverityLevel.INFO
            ),
            CodeIssue(
                message="Syntax warning",
                category=IssueCategory.SYNTAX,
                severity=SeverityLevel.WARNING
            ),
        ]

        filtered = filter_obj.filter_issues(issues)

        assert len(filtered) == 2
        assert any(i.category == IssueCategory.SECURITY for i in filtered)
        assert any(i.category == IssueCategory.SYNTAX for i in filtered)


# =============================================================================
# Session 8: Enum Tests
# =============================================================================
class TestSubscriptionFrequencyEnum:
    """Tests for SubscriptionFrequency enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        SubscriptionFrequency = report_module.SubscriptionFrequency
        assert SubscriptionFrequency.IMMEDIATE.value == "immediate"
        assert SubscriptionFrequency.HOURLY.value == "hourly"
        assert SubscriptionFrequency.DAILY.value == "daily"
        assert SubscriptionFrequency.WEEKLY.value == "weekly"

    def test_all_members(self, report_module: Any) -> None:
        """Test all members exist."""
        SubscriptionFrequency = report_module.SubscriptionFrequency
        assert len(list(SubscriptionFrequency)) == 4


class TestPermissionLevelEnum:
    """Tests for PermissionLevel enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        PermissionLevel = report_module.PermissionLevel
        assert PermissionLevel.READ.value == 1
        assert PermissionLevel.WRITE.value == 2
        assert PermissionLevel.ADMIN.value == 3

    def test_enum_ordering(self, report_module: Any) -> None:
        """Test permission levels are ordered correctly."""
        PermissionLevel = report_module.PermissionLevel
        assert PermissionLevel.READ.value < PermissionLevel.WRITE.value
        assert PermissionLevel.WRITE.value < PermissionLevel.ADMIN.value


class TestExportFormatEnum:
    """Tests for ExportFormat enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        ExportFormat = report_module.ExportFormat
        assert ExportFormat.HTML.value == "html"
        assert ExportFormat.JSON.value == "json"
        assert ExportFormat.CSV.value == "csv"
        assert ExportFormat.PDF.value == "pdf"

    def test_all_members(self, report_module: Any) -> None:
        """Test all members exist."""
        ExportFormat = report_module.ExportFormat
        assert len(list(ExportFormat)) == 4


class TestLocaleCodeEnum:
    """Tests for LocaleCode enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        LocaleCode = report_module.LocaleCode
        assert LocaleCode.EN_US.value == "en-US"
        assert LocaleCode.DE_DE.value == "de-DE"
        assert LocaleCode.FR_FR.value == "fr-FR"
        assert LocaleCode.ES_ES.value == "es-ES"

    def test_all_members(self, report_module: Any) -> None:
        """Test all members exist."""
        LocaleCode = report_module.LocaleCode
        assert len(list(LocaleCode)) == 4


class TestAuditActionEnum:
    """Tests for AuditAction enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        AuditAction = report_module.AuditAction
        assert AuditAction.CREATE.value == "create"
        assert AuditAction.READ.value == "read"
        assert AuditAction.UPDATE.value == "update"
        assert AuditAction.DELETE.value == "delete"
        assert AuditAction.EXPORT.value == "export"

    def test_all_members(self, report_module: Any) -> None:
        """Test all members exist."""
        AuditAction = report_module.AuditAction
        assert len(list(AuditAction)) == 5


# =============================================================================
# Session 8: Dataclass Tests
# =============================================================================


class TestReportSubscriptionDataclass:
    """Tests for ReportSubscription dataclass."""

    def test_creation_minimal(self, report_module: Any) -> None:
        """Test creating with minimal fields."""
        ReportSubscription = report_module.ReportSubscription

        sub = ReportSubscription(
            subscriber_id="user1",
            email="user@example.com"
        )
        assert sub.subscriber_id == "user1"
        assert sub.email == "user@example.com"
        assert sub.enabled is True

    def test_creation_full(self, report_module: Any) -> None:
        """Test creating with all fields."""
        ReportSubscription = report_module.ReportSubscription
        SubscriptionFrequency = report_module.SubscriptionFrequency
        ReportType = report_module.ReportType

        sub = ReportSubscription(
            subscriber_id="user1",
            email="user@example.com",
            frequency=SubscriptionFrequency.WEEKLY,
            report_types=[ReportType.ERRORS],
            file_patterns=["*.py"],
            enabled=False
        )
        assert sub.frequency == SubscriptionFrequency.WEEKLY
        assert ReportType.ERRORS in sub.report_types
        assert sub.enabled is False


class TestArchivedReportDataclass:
    """Tests for ArchivedReport dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ArchivedReport."""
        ArchivedReport = report_module.ArchivedReport

        archive = ArchivedReport(
            report_id="report_123",
            file_path="test.py",
            content="Report content"
        )
        assert archive.report_id == "report_123"
        assert archive.file_path == "test.py"
        assert archive.retention_days == 90


class TestReportAnnotationDataclass:
    """Tests for ReportAnnotation dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ReportAnnotation."""
        ReportAnnotation = report_module.ReportAnnotation

        annotation = ReportAnnotation(
            annotation_id="ann_1",
            report_id="report_1",
            author="user1",
            content="Important note",
            line_number=42
        )
        assert annotation.annotation_id == "ann_1"
        assert annotation.author == "user1"
        assert annotation.line_number == 42


class TestReportSearchResultDataclass:
    """Tests for ReportSearchResult dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ReportSearchResult."""
        ReportSearchResult = report_module.ReportSearchResult
        ReportType = report_module.ReportType

        result = ReportSearchResult(
            file_path="test.py",
            report_type=ReportType.ERRORS,
            match_text="Syntax error",
            line_number=10,
            score=2.5
        )
        assert result.file_path == "test.py"
        assert result.score == 2.5


class TestReportMetricDataclass:
    """Tests for ReportMetric dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ReportMetric."""
        ReportMetric = report_module.ReportMetric

        metric = ReportMetric(
            name="issues_count",
            value=42.0,
            unit="count",
            threshold=100.0,
            trend="+"
        )
        assert metric.name == "issues_count"
        assert metric.value == 42.0
        assert metric.trend == "+"


class TestReportPermissionDataclass:
    """Tests for ReportPermission dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ReportPermission."""
        ReportPermission = report_module.ReportPermission
        PermissionLevel = report_module.PermissionLevel

        perm = ReportPermission(
            user_id="user1",
            report_pattern="*.md",
            level=PermissionLevel.WRITE,
            granted_by="admin"
        )
        assert perm.user_id == "user1"
        assert perm.level == PermissionLevel.WRITE


class TestAuditEntryDataclass:
    """Tests for AuditEntry dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating AuditEntry."""
        AuditEntry = report_module.AuditEntry
        AuditAction = report_module.AuditAction

        entry = AuditEntry(
            entry_id="audit_1",
            timestamp=1000.0,
            action=AuditAction.READ,
            user_id="user1",
            report_id="report1",
            details={"ip": "127.0.0.1"}
        )
        assert entry.action == AuditAction.READ
        assert entry.details["ip"] == "127.0.0.1"


class TestLocalizedStringDataclass:
    """Tests for LocalizedString dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating LocalizedString."""
        LocalizedString = report_module.LocalizedString

        localized = LocalizedString(
            key="error.syntax",
            translations={"en-US": "Syntax Error", "de-DE": "Syntaxfehler"},
            default="Syntax Error"
        )
        assert localized.key == "error.syntax"
        assert localized.translations["de-DE"] == "Syntaxfehler"


class TestValidationResultDataclass:
    """Tests for ValidationResult dataclass."""

    def test_creation_valid(self, report_module: Any) -> None:
        """Test creating valid ValidationResult."""
        ValidationResult = report_module.ValidationResult

        result = ValidationResult(
            valid=True,
            errors=[],
            warnings=["Minor issue"],
            checksum="abc123"
        )
        assert result.valid is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 1

    def test_creation_invalid(self, report_module: Any) -> None:
        """Test creating invalid ValidationResult."""
        ValidationResult = report_module.ValidationResult

        result = ValidationResult(
            valid=False,
            errors=["Missing heading"],
            checksum="def456"
        )
        assert result.valid is False
        assert "Missing heading" in result.errors


class TestAggregatedReportDataclass:
    """Tests for AggregatedReport dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating AggregatedReport."""
        AggregatedReport = report_module.AggregatedReport
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        issue = CodeIssue(
            message="Test error",
            category=IssueCategory.SYNTAX,
            severity=SeverityLevel.ERROR
        )
        report = AggregatedReport(
            sources=["file1.py", "file2.py"],
            combined_issues=[issue],
            summary={"total": 1}
        )
        assert len(report.sources) == 2
        assert len(report.combined_issues) == 1


# =============================================================================
# Session 8: Helper Class Tests
# =============================================================================


class TestSubscriptionManager:
    """Tests for SubscriptionManager class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        SubscriptionManager = report_module.SubscriptionManager

        manager = SubscriptionManager()
        assert manager.subscriptions == {}
        assert manager.delivery_queue == []

    def test_add_subscription(self, report_module: Any) -> None:
        """Test adding subscription."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportSubscription = report_module.ReportSubscription

        manager = SubscriptionManager()
        sub = ReportSubscription("user1", "user@example.com")
        manager.add_subscription(sub)

        assert "user1" in manager.subscriptions

    def test_remove_subscription(self, report_module: Any) -> None:
        """Test removing subscription."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportSubscription = report_module.ReportSubscription

        manager = SubscriptionManager()
        sub = ReportSubscription("user1", "user@example.com")
        manager.add_subscription(sub)

        assert manager.remove_subscription("user1") is True
        assert manager.remove_subscription("unknown") is False

    def test_get_due_subscriptions(self, report_module: Any) -> None:
        """Test getting due subscriptions."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportSubscription = report_module.ReportSubscription

        manager = SubscriptionManager()
        sub1 = ReportSubscription("user1", "user1@example.com", enabled=True)
        sub2 = ReportSubscription("user2", "user2@example.com", enabled=False)
        manager.add_subscription(sub1)
        manager.add_subscription(sub2)

        due = manager.get_due_subscriptions()
        assert len(due) == 1
        assert due[0].subscriber_id == "user1"

    def test_queue_and_process_delivery(self, report_module: Any) -> None:
        """Test queuing and processing deliveries."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportType = report_module.ReportType

        manager = SubscriptionManager()
        manager.queue_delivery("user1", "Report content", ReportType.ERRORS)

        assert len(manager.delivery_queue) == 1
        processed = manager.process_deliveries()
        assert processed == 1
        assert len(manager.delivery_queue) == 0


class TestReportArchiver:
    """Tests for ReportArchiver class."""

    def test_initialization(self, report_module: Any, tmp_path: Path) -> None:
        """Test initialization."""
        ReportArchiver = report_module.ReportArchiver

        archiver = ReportArchiver(tmp_path / "archives")
        assert archiver.archive_dir == tmp_path / "archives"

    def test_archive_and_list(self, report_module: Any) -> None:
        """Test archiving and listing."""
        ReportArchiver = report_module.ReportArchiver

        archiver = ReportArchiver()
        archived = archiver.archive("test.py", "Report content", retention_days=30)

        assert archived.file_path == "test.py"
        assert archived.retention_days == 30

        archives = archiver.list_archives("test.py")
        assert len(archives) == 1

    def test_get_archive(self, report_module: Any) -> None:
        """Test getting specific archive."""
        ReportArchiver = report_module.ReportArchiver

        archiver = ReportArchiver()
        archived = archiver.archive("test.py", "Content")

        retrieved = archiver.get_archive(archived.report_id)
        assert retrieved is not None
        assert retrieved.content == "Content"

        assert archiver.get_archive("nonexistent") is None

    def test_cleanup_expired(self, report_module: Any) -> None:
        """Test cleanup of expired archives."""
        ReportArchiver = report_module.ReportArchiver
        ArchivedReport = report_module.ArchivedReport

        archiver = ReportArchiver()
        # Create expired archive (archived_at in the past)
        old_archive = ArchivedReport(
            report_id="old_1",
            file_path="test.py",
            content="Old content",
            archived_at=1.0,  # Very old timestamp
            retention_days=1
        )
        archiver.archives["test.py"] = [old_archive]

        removed = archiver.cleanup_expired()
        assert removed == 1
        assert len(archiver.list_archives("test.py")) == 0


class TestAnnotationManager:
    """Tests for AnnotationManager class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        AnnotationManager = report_module.AnnotationManager

        manager = AnnotationManager()
        assert manager.annotations == {}

    def test_add_and_get_annotation(self, report_module: Any) -> None:
        """Test adding and retrieving annotations."""
        AnnotationManager = report_module.AnnotationManager

        manager = AnnotationManager()
        ann = manager.add_annotation("report1", "user1", "Note", line_number=10)

        assert ann.author == "user1"
        assert ann.line_number == 10

        annotations = manager.get_annotations("report1")
        assert len(annotations) == 1

    def test_remove_annotation(self, report_module: Any) -> None:
        """Test removing annotation."""
        AnnotationManager = report_module.AnnotationManager

        manager = AnnotationManager()
        ann = manager.add_annotation("report1", "user1", "Note")

        assert manager.remove_annotation(ann.annotation_id) is True
        assert manager.remove_annotation("nonexistent") is False
        assert len(manager.get_annotations("report1")) == 0


class TestReportSearchEngine:
    """Tests for ReportSearchEngine class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        ReportSearchEngine = report_module.ReportSearchEngine

        engine = ReportSearchEngine()
        assert engine.index == {}

    def test_index_and_search(self, report_module: Any) -> None:
        """Test indexing and searching."""
        ReportSearchEngine = report_module.ReportSearchEngine
        ReportType = report_module.ReportType

        engine = ReportSearchEngine()
        content = "Line one\nSyntax error found\nLine three"
        engine.index_report("test.py", ReportType.ERRORS, content)

        results = engine.search("syntax error")
        assert len(results) > 0
        assert results[0].file_path == "test.py"

    def test_search_no_results(self, report_module: Any) -> None:
        """Test search with no results."""
        ReportSearchEngine = report_module.ReportSearchEngine

        engine = ReportSearchEngine()
        results = engine.search("nonexistent")
        assert len(results) == 0


class TestMetricsCollector:
    """Tests for MetricsCollector class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        MetricsCollector = report_module.MetricsCollector

        collector = MetricsCollector()
        assert collector.metrics == {}

    def test_record_and_get(self, report_module: Any) -> None:
        """Test recording and retrieving metrics."""
        MetricsCollector = report_module.MetricsCollector

        collector = MetricsCollector()
        metric = collector.record("test.py", "issues", 5.0, "count")

        assert metric.name == "issues"
        assert metric.value == 5.0

        metrics = collector.get_metrics("test.py")
        assert len(metrics) == 1

    def test_get_summary(self, report_module: Any) -> None:
        """Test getting summary."""
        MetricsCollector = report_module.MetricsCollector

        collector = MetricsCollector()
        collector.record("file1.py", "issues", 5.0)
        collector.record("file2.py", "issues", 10.0)

        summary = collector.get_summary()
        assert summary["total_files"] == 2
        assert summary["total_metrics"] == 2
        assert summary["averages"]["issues"] == 7.5


class TestAccessController:
    """Tests for AccessController class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        AccessController = report_module.AccessController

        controller = AccessController()
        assert controller.permissions == []

    def test_grant_permission(self, report_module: Any) -> None:
        """Test granting permission."""
        AccessController = report_module.AccessController
        PermissionLevel = report_module.PermissionLevel

        controller = AccessController()
        perm = controller.grant("user1", "*.md", PermissionLevel.READ)

        assert perm.user_id == "user1"
        assert len(controller.permissions) == 1

    def test_check_permission(self, report_module: Any) -> None:
        """Test checking permission."""
        AccessController = report_module.AccessController
        PermissionLevel = report_module.PermissionLevel

        controller = AccessController()
        controller.grant("user1", "*.md", PermissionLevel.READ)

        assert controller.check("user1", "report.md", PermissionLevel.READ) is True
        assert controller.check("user1", "report.md", PermissionLevel.WRITE) is False
        assert controller.check("user2", "report.md", PermissionLevel.READ) is False

    def test_revoke_permission(self, report_module: Any) -> None:
        """Test revoking permission."""
        AccessController = report_module.AccessController
        PermissionLevel = report_module.PermissionLevel

        controller = AccessController()
        controller.grant("user1", "*.md", PermissionLevel.READ)

        assert controller.revoke("user1", "*.md") is True
        assert controller.revoke("unknown", "*.md") is False
        assert controller.check("user1", "report.md", PermissionLevel.READ) is False


class TestReportExporter:
    """Tests for ReportExporter class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        ReportExporter = report_module.ReportExporter

        exporter = ReportExporter()
        assert exporter is not None

    def test_to_html(self, report_module: Any) -> None:
        """Test HTML conversion."""
        ReportExporter = report_module.ReportExporter

        exporter = ReportExporter()
        html = exporter.to_html("# Title\n- Item", "Test")

        assert "<h1>Title</h1>" in html
        assert "<li>Item</li>" in html
        assert "<title>Test</title>" in html

    def test_to_csv(self, report_module: Any) -> None:
        """Test CSV export."""
        ReportExporter = report_module.ReportExporter
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        exporter = ReportExporter()
        issues = [
            CodeIssue(
                message="Test error",
                category=IssueCategory.SYNTAX,
                severity=SeverityLevel.ERROR,
                line_number=10
            )
        ]
        csv = exporter.to_csv(issues)

        assert "message,category" in csv
        assert "Test error" in csv
        assert "SYNTAX" in csv

    def test_export(self, report_module: Any, tmp_path: Path) -> None:
        """Test export to file."""
        ReportExporter = report_module.ReportExporter
        ExportFormat = report_module.ExportFormat

        exporter = ReportExporter()
        output = tmp_path / "report.html"
        result = exporter.export("# Test", ExportFormat.HTML, output)

        assert "<h1>Test</h1>" in result
        assert output.exists()


class TestAuditLogger:
    """Tests for AuditLogger class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        AuditLogger = report_module.AuditLogger

        logger = AuditLogger()
        assert logger.entries == []

    def test_log_action(self, report_module: Any) -> None:
        """Test logging action."""
        AuditLogger = report_module.AuditLogger
        AuditAction = report_module.AuditAction

        logger = AuditLogger()
        entry = logger.log(AuditAction.READ, "user1", "report.md")

        assert entry.action == AuditAction.READ
        assert entry.user_id == "user1"
        assert len(logger.entries) == 1

    def test_get_history(self, report_module: Any) -> None:
        """Test getting report history."""
        AuditLogger = report_module.AuditLogger
        AuditAction = report_module.AuditAction

        logger = AuditLogger()
        logger.log(AuditAction.READ, "user1", "report1.md")
        logger.log(AuditAction.UPDATE, "user2", "report1.md")
        logger.log(AuditAction.READ, "user1", "report2.md")

        history = logger.get_history("report1.md")
        assert len(history) == 2

    def test_get_user_activity(self, report_module: Any) -> None:
        """Test getting user activity."""
        AuditLogger = report_module.AuditLogger
        AuditAction = report_module.AuditAction

        logger = AuditLogger()
        logger.log(AuditAction.READ, "user1", "report1.md")
        logger.log(AuditAction.READ, "user1", "report2.md")
        logger.log(AuditAction.READ, "user2", "report1.md")

        activity = logger.get_user_activity("user1")
        assert len(activity) == 2


class TestReportValidator:
    """Tests for ReportValidator class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        assert validator is not None

    def test_validate_valid_content(self, report_module: Any) -> None:
        """Test validating valid content."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        result = validator.validate("# Title\n\nSome content here.")

        assert result.valid is True
        assert len(result.errors) == 0
        assert result.checksum != ""

    def test_validate_missing_heading(self, report_module: Any) -> None:
        """Test validating content without heading."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        result = validator.validate("Just some text without heading")

        assert result.valid is False
        assert "Missing main heading" in result.errors

    def test_validate_empty_link(self, report_module: Any) -> None:
        """Test validating content with empty links."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        result = validator.validate("# Title\n\nA [broken link]()")

        assert "Contains empty link targets" in result.warnings

    def test_verify_checksum(self, report_module: Any) -> None:
        """Test verifying checksum."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        content = "# Test content"
        result = validator.validate(content)

        assert validator.verify_checksum(content, result.checksum) is True
        assert validator.verify_checksum(content, "wrong") is False


class TestReportLocalizer:
    """Tests for ReportLocalizer class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        ReportLocalizer = report_module.ReportLocalizer
        LocaleCode = report_module.LocaleCode

        localizer = ReportLocalizer(LocaleCode.EN_US)
        assert localizer.current_locale == LocaleCode.EN_US

    def test_get_default_string(self, report_module: Any) -> None:
        """Test getting default strings."""
        ReportLocalizer = report_module.ReportLocalizer

        localizer = ReportLocalizer()
        text = localizer.get("report.description")

        assert text == "Description"

    def test_get_german_string(self, report_module: Any) -> None:
        """Test getting German strings."""
        ReportLocalizer = report_module.ReportLocalizer
        LocaleCode = report_module.LocaleCode

        localizer = ReportLocalizer(LocaleCode.DE_DE)
        text = localizer.get("report.errors")

        assert text == "Fehler"

    def test_add_string(self, report_module: Any) -> None:
        """Test adding custom string."""
        ReportLocalizer = report_module.ReportLocalizer

        localizer = ReportLocalizer()
        localizer.add_string("custom.key", {"en-US": "Custom", "de-DE": "Benutzerdefiniert"})

        assert localizer.get("custom.key") == "Custom"

    def test_set_locale(self, report_module: Any) -> None:
        """Test setting locale."""
        ReportLocalizer = report_module.ReportLocalizer
        LocaleCode = report_module.LocaleCode

        localizer = ReportLocalizer(LocaleCode.EN_US)
        localizer.set_locale(LocaleCode.DE_DE)

        assert localizer.current_locale == LocaleCode.DE_DE

    def test_get_unknown_key(self, report_module: Any) -> None:
        """Test getting unknown key returns key."""
        ReportLocalizer = report_module.ReportLocalizer

        localizer = ReportLocalizer()
        text = localizer.get("unknown.key")

        assert text == "unknown.key"


class TestReportAPI:
    """Tests for ReportAPI class."""

    def test_initialization(self, report_module: Any, tmp_path: Path) -> None:
        """Test initialization."""
        ReportAPI = report_module.ReportAPI

        api = ReportAPI(tmp_path)
        assert api.reports_dir == tmp_path

    def test_list_reports(self, report_module: Any, tmp_path: Path) -> None:
        """Test listing reports."""
        ReportAPI = report_module.ReportAPI

        (tmp_path / "report1.md").write_text("# Report 1")
        (tmp_path / "report2.md").write_text("# Report 2")

        api = ReportAPI(tmp_path)
        reports = api.list_reports()

        assert len(reports) == 2

    def test_get_report(self, report_module: Any, tmp_path: Path) -> None:
        """Test getting specific report."""
        ReportAPI = report_module.ReportAPI
        ReportType = report_module.ReportType

        (tmp_path / "test.errors.md").write_text("# Errors")

        api = ReportAPI(tmp_path)
        content = api.get_report("test", ReportType.ERRORS)

        assert content == "# Errors"
        assert api.get_report("nonexistent", ReportType.ERRORS) is None

    def test_create_report(self, report_module: Any, tmp_path: Path) -> None:
        """Test creating report."""
        ReportAPI = report_module.ReportAPI
        ReportType = report_module.ReportType

        api = ReportAPI(tmp_path)
        result = api.create_report("new", ReportType.ERRORS, "# New Report")

        assert result is True
        assert (tmp_path / "new.errors.md").exists()


class TestReportScheduler:
    """Tests for ReportScheduler class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        assert scheduler.schedules == {}

    def test_add_schedule(self, report_module: Any) -> None:
        """Test adding schedule."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        scheduler.add_schedule("daily", "0 8 * * *", ["*.py"])

        assert "daily" in scheduler.schedules
        assert scheduler.schedules["daily"]["patterns"] == ["*.py"]

    def test_remove_schedule(self, report_module: Any) -> None:
        """Test removing schedule."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        scheduler.add_schedule("daily", "0 8 * * *", ["*.py"])

        assert scheduler.remove_schedule("daily") is True
        assert scheduler.remove_schedule("nonexistent") is False

    def test_get_due_tasks(self, report_module: Any) -> None:
        """Test getting due tasks."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        scheduler.add_schedule("task1", "0 8 * * *", ["*.py"])
        scheduler.add_schedule("task2", "0 12 * * *", ["*.md"])

        due = scheduler.get_due_tasks()
        assert len(due) == 2

    def test_mark_completed(self, report_module: Any) -> None:
        """Test marking task completed."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        scheduler.add_schedule("daily", "0 8 * * *", ["*.py"])
        scheduler.mark_completed("daily")

        assert scheduler.schedules["daily"]["last_run"] > 0


class TestReportAggregator:
    """Tests for ReportAggregator class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        ReportAggregator = report_module.ReportAggregator

        aggregator = ReportAggregator()
        assert aggregator.sources == {}

    def test_add_source(self, report_module: Any) -> None:
        """Test adding source."""
        ReportAggregator = report_module.ReportAggregator
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        aggregator = ReportAggregator()
        issues = [
            CodeIssue("Error 1", IssueCategory.SYNTAX, SeverityLevel.ERROR)
        ]
        aggregator.add_source("file1.py", issues)

        assert "file1.py" in aggregator.sources

    def test_aggregate(self, report_module: Any) -> None:
        """Test aggregating sources."""
        ReportAggregator = report_module.ReportAggregator
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        aggregator = ReportAggregator()
        aggregator.add_source("file1.py", [
            CodeIssue("Error 1", IssueCategory.SYNTAX, SeverityLevel.ERROR)
        ])
        aggregator.add_source("file2.py", [
            CodeIssue("Warning 1", IssueCategory.STYLE, SeverityLevel.WARNING)
        ])

        report = aggregator.aggregate()

        assert len(report.sources) == 2
        assert len(report.combined_issues) == 2
        assert report.summary["total_issues"] == 2
        assert report.summary["total_files"] == 2

    def test_clear(self, report_module: Any) -> None:
        """Test clearing sources."""
        ReportAggregator = report_module.ReportAggregator
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        aggregator = ReportAggregator()
        aggregator.add_source("file1.py", [
            CodeIssue("Error", IssueCategory.SYNTAX, SeverityLevel.ERROR)
        ])
        aggregator.clear()

        assert aggregator.sources == {}


# =============================================================================
# Session 8: Integration Tests
# =============================================================================


class TestSession8Integration:
    """Integration tests for Session 8 features."""

    def test_subscription_with_archiver(self, report_module: Any) -> None:
        """Test subscription manager with archiver."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportArchiver = report_module.ReportArchiver
        ReportSubscription = report_module.ReportSubscription
        ReportType = report_module.ReportType

        manager = SubscriptionManager()
        archiver = ReportArchiver()

        sub = ReportSubscription("user1", "user@example.com")
        manager.add_subscription(sub)

        report_content = "# Test Report"
        archived = archiver.archive("test.py", report_content)
        manager.queue_delivery("user1", archived.content, ReportType.ERRORS)

        assert len(manager.delivery_queue) == 1
        assert archiver.get_archive(archived.report_id) is not None

    def test_search_with_annotations(self, report_module: Any) -> None:
        """Test search engine with annotation manager."""
        ReportSearchEngine = report_module.ReportSearchEngine
        AnnotationManager = report_module.AnnotationManager
        ReportType = report_module.ReportType

        engine = ReportSearchEngine()
        annotations = AnnotationManager()

        content = "# Report\nSyntax error on line 10"
        engine.index_report("test.py", ReportType.ERRORS, content)

        results = engine.search("syntax error")
        if results:
            report_id = f"test.py:{ReportType.ERRORS.name}"
            annotations.add_annotation(report_id, "reviewer", "Needs fix")

            anns = annotations.get_annotations(report_id)
            assert len(anns) == 1

    def test_access_control_with_audit(self, report_module: Any) -> None:
        """Test access control with audit logging."""
        AccessController = report_module.AccessController
        AuditLogger = report_module.AuditLogger
        PermissionLevel = report_module.PermissionLevel
        AuditAction = report_module.AuditAction

        controller = AccessController()
        logger = AuditLogger()

        controller.grant("user1", "*.md", PermissionLevel.READ)

        if controller.check("user1", "report.md", PermissionLevel.READ):
            logger.log(AuditAction.READ, "user1", "report.md")

        history = logger.get_history("report.md")
        assert len(history) == 1
        assert history[0].action == AuditAction.READ

    def test_export_with_validation(self, report_module: Any) -> None:
        """Test exporter with validator."""
        ReportExporter = report_module.ReportExporter
        ReportValidator = report_module.ReportValidator
        ExportFormat = report_module.ExportFormat

        exporter = ReportExporter()
        validator = ReportValidator()

        content = "# Test Report\n\nSome valid content."
        validation = validator.validate(content)

        if validation.valid:
            html = exporter.export(content, ExportFormat.HTML)
            assert "<h1>Test Report</h1>" in html

    def test_localized_metrics(self, report_module: Any) -> None:
        """Test metrics collector with localizer."""
        MetricsCollector = report_module.MetricsCollector
        ReportLocalizer = report_module.ReportLocalizer
        LocaleCode = report_module.LocaleCode

        collector = MetricsCollector()
        localizer = ReportLocalizer(LocaleCode.DE_DE)

        collector.record("test.py", "errors", 5.0)
        summary = collector.get_summary()

        label = localizer.get("report.errors")
        assert label == "Fehler"
        assert summary["averages"]["errors"] == 5.0


# =============================================================================
# Session 8: Test File Improvement Tests
# =============================================================================


class TestReportSubscriptionAndDelivery:
    """Tests for report subscription and delivery functionality."""

    def test_subscription_creation_with_frequency(self, report_module: Any) -> None:
        """Test creating subscription with different frequencies."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportSubscription = report_module.ReportSubscription
        SubscriptionFrequency = report_module.SubscriptionFrequency

        manager = SubscriptionManager()

        for freq in SubscriptionFrequency:
            sub = ReportSubscription(
                subscriber_id=f"user_{freq.value}",
                email=f"user_{freq.value}@example.com",
                frequency=freq
            )
            manager.add_subscription(sub)

        assert len(manager.subscriptions) == 4

    def test_subscription_delivery_queue_ordering(self, report_module: Any) -> None:
        """Test delivery queue maintains order."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportType = report_module.ReportType

        manager = SubscriptionManager()
        manager.queue_delivery("user1", "Report 1", ReportType.ERRORS)
        manager.queue_delivery("user2", "Report 2", ReportType.IMPROVEMENTS)
        manager.queue_delivery("user1", "Report 3", ReportType.SUMMARY)

        assert len(manager.delivery_queue) == 3
        assert manager.delivery_queue[0]["subscriber_id"] == "user1"
        assert manager.delivery_queue[1]["subscriber_id"] == "user2"

    def test_subscription_enabled_filtering(self, report_module: Any) -> None:
        """Test filtering enabled vs disabled subscriptions."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportSubscription = report_module.ReportSubscription

        manager = SubscriptionManager()
        manager.add_subscription(ReportSubscription("active1", "a@test.com", enabled=True))
        manager.add_subscription(ReportSubscription("inactive1", "b@test.com", enabled=False))
        manager.add_subscription(ReportSubscription("active2", "c@test.com", enabled=True))

        due = manager.get_due_subscriptions()
        assert len(due) == 2
        assert all(s.enabled for s in due)


class TestReportArchivingWithRetention:
    """Tests for report archiving with retention policies."""

    def test_archive_with_custom_retention(self, report_module: Any) -> None:
        """Test archiving with different retention periods."""
        ReportArchiver = report_module.ReportArchiver

        archiver = ReportArchiver()

        short_retention = archiver.archive("file1.py", "Short lived", retention_days=7)
        long_retention = archiver.archive("file2.py", "Long lived", retention_days=365)

        assert short_retention.retention_days == 7
        assert long_retention.retention_days == 365

    def test_archive_retrieval_by_file(self, report_module: Any) -> None:
        """Test retrieving archives by file path."""
        ReportArchiver = report_module.ReportArchiver

        archiver = ReportArchiver()
        archiver.archive("file1.py", "Version 1")
        archiver.archive("file1.py", "Version 2")
        archiver.archive("file2.py", "Different file")

        file1_archives = archiver.list_archives("file1.py")
        file2_archives = archiver.list_archives("file2.py")

        assert len(file1_archives) == 2
        assert len(file2_archives) == 1

    def test_archive_cleanup_preserves_valid(self, report_module: Any) -> None:
        """Test cleanup removes expired but keeps valid archives."""
        ReportArchiver = report_module.ReportArchiver
        ArchivedReport = report_module.ArchivedReport

        archiver = ReportArchiver()

        # Add a valid (non-expired) archive
        archiver.archive("valid.py", "Valid content", retention_days=365)

        # Add an expired archive manually
        expired = ArchivedReport(
            report_id="expired_1",
            file_path="expired.py",
            content="Expired content",
            archived_at=1.0,  # Very old
            retention_days=1
        )
        archiver.archives["expired.py"] = [expired]

        removed = archiver.cleanup_expired()

        assert removed == 1
        assert len(archiver.list_archives("valid.py")) == 1
        assert len(archiver.list_archives("expired.py")) == 0


class TestReportAnnotationPersistence:
    """Tests for report annotation persistence."""

    def test_annotation_with_line_numbers(self, report_module: Any) -> None:
        """Test annotations with specific line numbers."""
        AnnotationManager = report_module.AnnotationManager

        manager = AnnotationManager()
        manager.add_annotation("report1", "user1", "Line specific note", line_number=42)
        manager.add_annotation("report1", "user2", "Another note", line_number=100)

        annotations = manager.get_annotations("report1")
        line_numbers = [a.line_number for a in annotations]

        assert 42 in line_numbers
        assert 100 in line_numbers

    def test_annotation_removal_by_id(self, report_module: Any) -> None:
        """Test removing specific annotations by ID."""
        AnnotationManager = report_module.AnnotationManager

        manager = AnnotationManager()
        manager.add_annotation("report1", "user1", "Keep this")
        ann2 = manager.add_annotation("report1", "user2", "Remove this")

        manager.remove_annotation(ann2.annotation_id)

        annotations = manager.get_annotations("report1")
        assert len(annotations) == 1
        assert annotations[0].content == "Keep this"

    def test_multiple_annotations_per_report(self, report_module: Any) -> None:
        """Test handling multiple annotations on same report."""
        AnnotationManager = report_module.AnnotationManager

        manager = AnnotationManager()
        for i in range(10):
            manager.add_annotation("report1", f"user{i}", f"Note {i}")

        annotations = manager.get_annotations("report1")
        assert len(annotations) == 10


class TestReportSearchAcrossHistoricalData:
    """Tests for report search across historical data."""

    def test_search_multiple_reports(self, report_module: Any) -> None:
        """Test searching across multiple indexed reports."""
        ReportSearchEngine = report_module.ReportSearchEngine
        ReportType = report_module.ReportType

        engine = ReportSearchEngine()
        engine.index_report("file1.py", ReportType.ERRORS, "Syntax error in function")
        engine.index_report("file2.py", ReportType.ERRORS, "Type error in class")
        engine.index_report("file3.py", ReportType.IMPROVEMENTS, "Consider adding error handling")

        results = engine.search("error")
        assert len(results) >= 2

    def test_search_with_max_results(self, report_module: Any) -> None:
        """Test search respects max results limit."""
        ReportSearchEngine = report_module.ReportSearchEngine
        ReportType = report_module.ReportType

        engine = ReportSearchEngine()
        for i in range(50):
            engine.index_report(f"file{i}.py", ReportType.ERRORS, f"Error number {i}")

        results = engine.search("error", max_results=5)
        assert len(results) <= 5

    def test_search_result_scoring(self, report_module: Any) -> None:
        """Test search results are scored by relevance."""
        ReportSearchEngine = report_module.ReportSearchEngine
        ReportType = report_module.ReportType

        engine = ReportSearchEngine()
        engine.index_report("high.py", ReportType.ERRORS, "error error error multiple")
        engine.index_report("low.py", ReportType.ERRORS, "single error")

        results = engine.search("error")
        # Results should be sorted by score (descending)
        if len(results) >= 2:
            assert results[0].score >= results[1].score


class TestCustomReportMetricsAndKPIs:
    """Tests for custom report metrics and KPIs."""

    def test_record_metric_with_threshold(self, report_module: Any) -> None:
        """Test recording metrics with alert thresholds."""
        MetricsCollector = report_module.MetricsCollector

        collector = MetricsCollector()
        metric = collector.record("file.py", "issues_count", 50.0, threshold=100.0)

        assert metric.threshold == 100.0
        assert metric.value < metric.threshold

    def test_metrics_summary_averages(self, report_module: Any) -> None:
        """Test summary calculates correct averages."""
        MetricsCollector = report_module.MetricsCollector

        collector = MetricsCollector()
        collector.record("file1.py", "complexity", 10.0)
        collector.record("file2.py", "complexity", 20.0)
        collector.record("file3.py", "complexity", 30.0)

        summary = collector.get_summary()
        assert summary["averages"]["complexity"] == 20.0

    def test_multiple_metrics_per_file(self, report_module: Any) -> None:
        """Test recording multiple different metrics per file."""
        MetricsCollector = report_module.MetricsCollector

        collector = MetricsCollector()
        collector.record("file.py", "lines_of_code", 500.0)
        collector.record("file.py", "complexity", 15.0)
        collector.record("file.py", "test_coverage", 85.0)

        metrics = collector.get_metrics("file.py")
        metric_names = [m.name for m in metrics]

        assert "lines_of_code" in metric_names
        assert "complexity" in metric_names
        assert "test_coverage" in metric_names


class TestReportAccessControl:
    """Tests for report access control."""

    def test_permission_levels_hierarchy(self, report_module: Any) -> None:
        """Test permission level hierarchy (ADMIN > WRITE > READ)."""
        AccessController = report_module.AccessController
        PermissionLevel = report_module.PermissionLevel

        controller = AccessController()
        controller.grant("admin_user", "*.md", PermissionLevel.ADMIN)

        # Admin should have access at all levels
        assert controller.check("admin_user", "report.md", PermissionLevel.READ)
        assert controller.check("admin_user", "report.md", PermissionLevel.WRITE)
        assert controller.check("admin_user", "report.md", PermissionLevel.ADMIN)

    def test_permission_pattern_matching(self, report_module: Any) -> None:
        """Test permission pattern matching with wildcards."""
        AccessController = report_module.AccessController
        PermissionLevel = report_module.PermissionLevel

        controller = AccessController()
        controller.grant("user1", "reports/*.md", PermissionLevel.READ)

        assert controller.check("user1", "reports / daily.md", PermissionLevel.READ)
        # Different path should not match
        assert not controller.check("user1", "other / report.md", PermissionLevel.READ)

    def test_permission_revocation(self, report_module: Any) -> None:
        """Test revoking permissions."""
        AccessController = report_module.AccessController
        PermissionLevel = report_module.PermissionLevel

        controller = AccessController()
        controller.grant("user1", "*.md", PermissionLevel.WRITE)

        assert controller.check("user1", "report.md", PermissionLevel.WRITE)

        controller.revoke("user1", "*.md")

        assert not controller.check("user1", "report.md", PermissionLevel.WRITE)


class TestReportExportFormats:
    """Tests for report presentation export formats."""

    def test_export_to_html(self, report_module: Any) -> None:
        """Test HTML export with proper structure."""
        ReportExporter = report_module.ReportExporter
        ExportFormat = report_module.ExportFormat

        exporter = ReportExporter()
        content = "# Report Title\n\n- Item 1\n- Item 2"

        html = exporter.export(content, ExportFormat.HTML)

        assert "<!DOCTYPE html>" in html
        assert "<h1>Report Title</h1>" in html
        assert "<li>Item 1</li>" in html

    def test_export_to_json(self, report_module: Any) -> None:
        """Test JSON export."""
        ReportExporter = report_module.ReportExporter
        ExportFormat = report_module.ExportFormat
        import json

        exporter = ReportExporter()
        content = "# Test Report"

        result = exporter.export(content, ExportFormat.JSON)
        parsed = json.loads(result)

        assert "content" in parsed
        assert parsed["content"] == content

    def test_export_to_file(self, report_module: Any, tmp_path: Path) -> None:
        """Test export writes to file."""
        ReportExporter = report_module.ReportExporter
        ExportFormat = report_module.ExportFormat

        exporter = ReportExporter()
        output = tmp_path / "report.html"

        exporter.export("# Test", ExportFormat.HTML, output)

        assert output.exists()
        assert "<h1>Test</h1>" in output.read_text()


class TestReportAuditLogging:
    """Tests for report audit logging."""

    def test_audit_log_multiple_actions(self, report_module: Any) -> None:
        """Test logging different audit actions."""
        AuditLogger = report_module.AuditLogger
        AuditAction = report_module.AuditAction

        logger = AuditLogger()

        for action in AuditAction:
            logger.log(action, "testuser", "report.md")

        assert len(logger.entries) == len(list(AuditAction))

    def test_audit_log_user_activity(self, report_module: Any) -> None:
        """Test retrieving user activity from audit log."""
        AuditLogger = report_module.AuditLogger
        AuditAction = report_module.AuditAction

        logger = AuditLogger()
        logger.log(AuditAction.READ, "user1", "report1.md")
        logger.log(AuditAction.UPDATE, "user2", "report1.md")
        logger.log(AuditAction.READ, "user1", "report2.md")

        user1_activity = logger.get_user_activity("user1")
        assert len(user1_activity) == 2

    def test_audit_log_with_details(self, report_module: Any) -> None:
        """Test audit log entries with additional details."""
        AuditLogger = report_module.AuditLogger
        AuditAction = report_module.AuditAction

        logger = AuditLogger()
        entry = logger.log(
            AuditAction.EXPORT,
            "user1",
            "report.md",
            details={"format": "pdf", "pages": 10}
        )

        assert entry.details["format"] == "pdf"
        assert entry.details["pages"] == 10


class TestReportDataIntegrityChecks:
    """Tests for report data integrity checks."""

    def test_validator_detects_missing_heading(self, report_module: Any) -> None:
        """Test validator detects missing main heading."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        result = validator.validate("Just plain text without heading")

        assert not result.valid
        assert "Missing main heading" in result.errors

    def test_validator_detects_empty_links(self, report_module: Any) -> None:
        """Test validator detects empty link targets."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        result = validator.validate("# Title\n\n[broken link]()")

        assert "Contains empty link targets" in result.warnings

    def test_validator_checksum_verification(self, report_module: Any) -> None:
        """Test checksum verification for content integrity."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        content = "# Test Content\n\nBody text here."

        result = validator.validate(content)
        checksum = result.checksum

        # Verify checksum matches
        assert validator.verify_checksum(content, checksum)
        # Modified content should not match
        assert not validator.verify_checksum(content + "modified", checksum)


class TestReportLocalization:
    """Tests for report localization."""

    def test_localizer_default_strings(self, report_module: Any) -> None:
        """Test localizer provides default strings."""
        ReportLocalizer = report_module.ReportLocalizer
        LocaleCode = report_module.LocaleCode

        localizer = ReportLocalizer(LocaleCode.EN_US)

        assert localizer.get("report.description") == "Description"
        assert localizer.get("report.errors") == "Errors"
        assert localizer.get("report.improvements") == "Improvements"

    def test_localizer_german_translations(self, report_module: Any) -> None:
        """Test German translations."""
        ReportLocalizer = report_module.ReportLocalizer
        LocaleCode = report_module.LocaleCode

        localizer = ReportLocalizer(LocaleCode.DE_DE)

        assert localizer.get("report.description") == "Beschreibung"
        assert localizer.get("report.errors") == "Fehler"
        assert localizer.get("severity.warning") == "Warnung"

    def test_localizer_custom_strings(self, report_module: Any) -> None:
        """Test adding custom localized strings."""
        ReportLocalizer = report_module.ReportLocalizer
        LocaleCode = report_module.LocaleCode

        localizer = ReportLocalizer()
        localizer.add_string("custom.greeting", {
            "en-US": "Hello",
            "de-DE": "Hallo",
            "fr-FR": "Bonjour"
        })

        localizer.set_locale(LocaleCode.EN_US)
        assert localizer.get("custom.greeting") == "Hello"


class TestReportAPIEndpoints:
    """Tests for report API endpoints."""

    def test_api_list_reports(self, report_module: Any, tmp_path: Path) -> None:
        """Test API lists available reports."""
        ReportAPI = report_module.ReportAPI

        # Create test reports
        (tmp_path / "report1.md").write_text("# Report 1")
        (tmp_path / "report2.md").write_text("# Report 2")
        (tmp_path / "other.txt").write_text("Not a report")

        api = ReportAPI(tmp_path)
        reports = api.list_reports("*.md")

        assert len(reports) == 2

    def test_api_get_report_by_type(self, report_module: Any, tmp_path: Path) -> None:
        """Test API retrieves reports by type."""
        ReportAPI = report_module.ReportAPI
        ReportType = report_module.ReportType

        (tmp_path / "test.errors.md").write_text("# Errors for test")
        (tmp_path / "test.improvements.md").write_text("# Improvements for test")

        api = ReportAPI(tmp_path)

        errors = api.get_report("test", ReportType.ERRORS)
        improvements = api.get_report("test", ReportType.IMPROVEMENTS)

        assert errors == "# Errors for test"
        assert improvements == "# Improvements for test"

    def test_api_create_report(self, report_module: Any, tmp_path: Path) -> None:
        """Test API creates new reports."""
        ReportAPI = report_module.ReportAPI
        ReportType = report_module.ReportType

        api = ReportAPI(tmp_path)
        result = api.create_report("new_file", ReportType.ERRORS, "# New Error Report")

        assert result is True
        assert (tmp_path / "new_file.errors.md").exists()


class TestReportCachingInvalidation:
    """Tests for report caching invalidation."""

    def test_cache_invalidation_by_path(self, report_module: Any, tmp_path: Path) -> None:
        """Test cache invalidation by file path."""
        ReportCacheManager = report_module.ReportCacheManager

        cache_file = tmp_path / "cache.json"
        manager = ReportCacheManager(cache_file)

        manager.set("file1.py", "hash1", "Content 1")
        manager.set("file2.py", "hash2", "Content 2")

        manager.invalidate("file1.py")

        assert manager.get("file1.py", "hash1") is None
        assert manager.get("file2.py", "hash2") == "Content 2"

    def test_cache_hash_mismatch(self, report_module: Any, tmp_path: Path) -> None:
        """Test cache returns None for hash mismatch."""
        ReportCacheManager = report_module.ReportCacheManager

        cache_file = tmp_path / "cache.json"
        manager = ReportCacheManager(cache_file)

        manager.set("file.py", "original_hash", "Cached content")

        result = manager.get("file.py", "different_hash")
        assert result is None


class TestReportVersionComparison:
    """Tests for report version comparison."""

    def test_comparator_detects_additions(self, report_module: Any) -> None:
        """Test comparator detects added items."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        old = "- Item 1\n- Item 2"
        new = "- Item 1\n- Item 2\n- Item 3"

        result = comparator.compare("old.md", "new.md", old, new)

        assert "- Item 3" in result.added

    def test_comparator_detects_removals(self, report_module: Any) -> None:
        """Test comparator detects removed items."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        old = "- Item 1\n- Item 2\n- Item 3"
        new = "- Item 1\n- Item 2"

        result = comparator.compare("old.md", "new.md", old, new)

        assert "- Item 3" in result.removed

    def test_comparator_unchanged_count(self, report_module: Any) -> None:
        """Test comparator counts unchanged items."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        old = "- Item 1\n- Item 2\n- Item 3"
        new = "- Item 1\n- Item 2\n- Item 3"

        result = comparator.compare("old.md", "new.md", old, new)

        assert result.unchanged_count == 3


class TestReportSchedulingAutomation:
    """Tests for report scheduling automation."""

    def test_scheduler_add_and_remove(self, report_module: Any) -> None:
        """Test adding and removing schedules."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        scheduler.add_schedule("daily_report", "0 8 * * *", ["*.py"])

        assert "daily_report" in scheduler.schedules

        scheduler.remove_schedule("daily_report")
        assert "daily_report" not in scheduler.schedules

    def test_scheduler_get_due_tasks(self, report_module: Any) -> None:
        """Test getting tasks due for execution."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        scheduler.add_schedule("task1", "0 8 * * *", ["*.py"])
        scheduler.add_schedule("task2", "0 12 * * *", ["*.md"])

        due = scheduler.get_due_tasks()
        assert len(due) == 2

    def test_scheduler_mark_completed(self, report_module: Any) -> None:
        """Test marking scheduled tasks as completed."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        scheduler.add_schedule("test_task", "0 0 * * *", ["*.py"])

        scheduler.mark_completed("test_task")

        assert scheduler.schedules["test_task"]["last_run"] > 0


class TestReportDataAggregation:
    """Tests for report data aggregation."""

    def test_aggregator_combines_issues(self, report_module: Any) -> None:
        """Test aggregator combines issues from multiple files."""
        ReportAggregator = report_module.ReportAggregator
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        aggregator = ReportAggregator()

        aggregator.add_source("file1.py", [
            CodeIssue("Error 1", IssueCategory.SYNTAX, SeverityLevel.ERROR)
        ])
        aggregator.add_source("file2.py", [
            CodeIssue("Error 2", IssueCategory.STYLE, SeverityLevel.WARNING),
            CodeIssue("Error 3", IssueCategory.SECURITY, SeverityLevel.CRITICAL)
        ])

        report = aggregator.aggregate()

        assert len(report.combined_issues) == 3
        assert report.summary["total_files"] == 2

    def test_aggregator_summary_by_severity(self, report_module: Any) -> None:
        """Test aggregator summarizes by severity."""
        ReportAggregator = report_module.ReportAggregator
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        aggregator = ReportAggregator()
        aggregator.add_source("file.py", [
            CodeIssue("E1", IssueCategory.SYNTAX, SeverityLevel.ERROR),
            CodeIssue("E2", IssueCategory.SYNTAX, SeverityLevel.ERROR),
            CodeIssue("W1", IssueCategory.STYLE, SeverityLevel.WARNING)
        ])

        report = aggregator.aggregate()

        assert report.summary["by_severity"]["ERROR"] == 2
        assert report.summary["by_severity"]["WARNING"] == 1

    def test_aggregator_clear(self, report_module: Any) -> None:
        """Test aggregator clear removes all sources."""
        ReportAggregator = report_module.ReportAggregator
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        aggregator = ReportAggregator()
        aggregator.add_source("file.py", [
            CodeIssue("Error", IssueCategory.SYNTAX, SeverityLevel.ERROR)
        ])

        aggregator.clear()

        assert len(aggregator.sources) == 0


class TestReportPermissionManagement:
    """Tests for report permission management."""

    def test_permission_with_expiry(self, report_module: Any) -> None:
        """Test permissions with expiration."""
        ReportPermission = report_module.ReportPermission
        PermissionLevel = report_module.PermissionLevel
        import time

        # Create permission that expires in the past
        expired_perm = ReportPermission(
            user_id="user1",
            report_pattern="*.md",
            level=PermissionLevel.READ,
            expires_at=time.time() - 3600  # Expired 1 hour ago
        )

        assert expired_perm.expires_at < time.time()

    def test_multiple_permissions_per_user(self, report_module: Any) -> None:
        """Test user can have multiple permission entries."""
        AccessController = report_module.AccessController
        PermissionLevel = report_module.PermissionLevel

        controller = AccessController()
        controller.grant("user1", "reports/*.md", PermissionLevel.READ)
        controller.grant("user1", "admin/*.md", PermissionLevel.WRITE)

        assert controller.check("user1", "reports / daily.md", PermissionLevel.READ)
        assert controller.check("user1", "admin / config.md", PermissionLevel.WRITE)
        assert not controller.check("user1", "admin / config.md", PermissionLevel.ADMIN)
