import pytest
from pathlib import Path
from typing import Any, List, Dict, Optional
import sys
try:
    from tests.agent_test_utils import *
except ImportError:
    pass

def test_changes_agent_keyword_prompt_generates_suggestions(tmp_path: Path) -> None:
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "x.changes.md"
    agent = mod.ChangesAgent(str(target))
    agent.previous_content = "ORIGINAL"
    out = agent.improve_content("Please improve the changelog")
    assert "AI Changelog Improvement Suggestions" in out
    assert "ORIGINAL" in out


def test_changes_agent_non_keyword_delegates_to_base(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module: Any
) -> None:
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")

    def fake_run_subagent(
            self: Any,
            description: str,
            prompt: str,
            original_content: str = "") -> str:
        return "IMPROVED"

    monkeypatch.setattr(
        base_agent_module.BaseAgent,
        "run_subagent",
        fake_run_subagent,
        raising=True)
    target = tmp_path / "x.changes.md"
    target.write_text("BEFORE", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    assert agent.improve_content("noop") == "IMPROVED"


def test_set_template_python(tmp_path: Path) -> None:
    """Test setting Python changelog template."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.set_template("python")
    assert agent._template is not None
    assert agent._template.name == "Python"
    assert "Added" in agent._template.sections


def test_set_template_javascript(tmp_path: Path) -> None:
    """Test setting JavaScript changelog template."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.set_template("javascript")
    assert agent._template is not None
    assert agent._template.name == "JavaScript"


def test_set_template_unknown_falls_back_to_generic(tmp_path: Path) -> None:
    """Test that unknown template falls back to generic."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.set_template("nonexistent")
    assert agent._template.name == "Generic"


def test_create_custom_template(tmp_path: Path) -> None:
    """Test creating a custom changelog template."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    template = agent.create_custom_template(
        name="CustomProject",
        project_type="custom",
        sections=["Features", "Bugfixes", "Documentation"],
        include_links=False
    )
    assert template.name == "CustomProject"
    assert "Features" in template.sections
    assert template.include_links is False


def test_get_template_sections_default(tmp_path: Path) -> None:
    """Test getting default template sections."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    sections = agent.get_template_sections()
    assert "Added" in sections
    assert "Fixed" in sections


def test_set_versioning_strategy_semver(tmp_path: Path) -> None:
    """Test setting SemVer versioning strategy."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.set_versioning_strategy(mod.VersioningStrategy.SEMVER)
    assert agent._versioning_strategy == mod.VersioningStrategy.SEMVER


def test_set_versioning_strategy_calver(tmp_path: Path) -> None:
    """Test setting CalVer versioning strategy."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.set_versioning_strategy(mod.VersioningStrategy.CALVER)
    assert agent._versioning_strategy == mod.VersioningStrategy.CALVER


def test_generate_next_version_semver_patch(tmp_path: Path) -> None:
    """Test generating next SemVer patch version."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("## [1.2.3] - 2025-01-01\n", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    agent.set_versioning_strategy(mod.VersioningStrategy.SEMVER)
    version = agent.generate_next_version("patch")
    assert version == "1.2.4"


def test_generate_next_version_semver_minor(tmp_path: Path) -> None:
    """Test generating next SemVer minor version."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("## [1.2.3] - 2025-01-01\n", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    agent.set_versioning_strategy(mod.VersioningStrategy.SEMVER)
    version = agent.generate_next_version("minor")
    assert version == "1.3.0"


def test_generate_next_version_semver_major(tmp_path: Path) -> None:
    """Test generating next SemVer major version."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("## [1.2.3] - 2025-01-01\n", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    agent.set_versioning_strategy(mod.VersioningStrategy.SEMVER)
    version = agent.generate_next_version("major")
    assert version == "2.0.0"


def test_generate_next_version_calver(tmp_path: Path) -> None:
    """Test generating CalVer version."""
    from datetime import datetime
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.set_versioning_strategy(mod.VersioningStrategy.CALVER)
    version = agent.generate_next_version()
    expected = datetime.now().strftime("%Y.%m.%d")
    assert version == expected


def test_generate_next_version_default(tmp_path: Path) -> None:
    """Test generating default version when no previous exists."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    version = agent.generate_next_version()
    assert version == "0.1.0"


def test_enable_preview_mode(tmp_path: Path) -> None:
    """Test enabling preview mode."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("original", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.enable_preview_mode()
    assert agent._preview_mode is True


def test_disable_preview_mode(tmp_path: Path) -> None:
    """Test disabling preview mode."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.enable_preview_mode()
    agent.disable_preview_mode()
    assert agent._preview_mode is False


def test_preview_changes_returns_stats(tmp_path: Path) -> None:
    """Test preview_changes returns statistics."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("line1\nline2\n", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    preview = agent.preview_changes("line1\nline2\nline3\n")
    assert "original_lines" in preview
    assert "new_lines" in preview
    assert "lines_added" in preview
    assert "preview" in preview


def test_preview_mode_does_not_write_file(tmp_path: Path) -> None:
    """Test that preview mode doesn't write to file."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("original", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    agent.enable_preview_mode()
    agent.current_content = "modified"
    result = agent.update_file()
    assert result is True
    assert target.read_text(encoding="utf-8") == "original"


def test_detect_merge_conflicts_found(tmp_path: Path) -> None:
    """Test detecting merge conflicts."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    content = """
<<<<<<< HEAD
our changes
=======
their changes
>>>>>>> branch
"""
    conflicts = agent.detect_merge_conflicts(content)
    assert len(conflicts) == 1


def test_detect_merge_conflicts_none(tmp_path: Path) -> None:
    """Test no merge conflicts detected in clean content."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    content = "## Changelog\n### Added\n- Feature"
    conflicts = agent.detect_merge_conflicts(content)
    assert len(conflicts) == 0


def test_resolve_merge_conflict_ours(tmp_path: Path) -> None:
    """Test resolving merge conflict with 'ours'."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    content = """before
<<<<<<< HEAD
our changes
=======
their changes
>>>>>>> branch
after"""
    resolved = agent.resolve_merge_conflict(content, "ours")
    assert "our changes" in resolved
    assert "their changes" not in resolved
    assert "<<<<<<" not in resolved


def test_resolve_merge_conflict_theirs(tmp_path: Path) -> None:
    """Test resolving merge conflict with 'theirs'."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    content = """before
<<<<<<< HEAD
our changes
=======
their changes
>>>>>>> branch
after"""
    resolved = agent.resolve_merge_conflict(content, "theirs")
    assert "their changes" in resolved
    assert "our changes" not in resolved


def test_resolve_merge_conflict_both(tmp_path: Path) -> None:
    """Test resolving merge conflict with 'both'."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    content = """before
<<<<<<< HEAD
our changes
=======
their changes
>>>>>>> branch
after"""
    resolved = agent.resolve_merge_conflict(content, "both")
    assert "our changes" in resolved
    assert "their changes" in resolved


def test_validate_entry_valid(tmp_path: Path) -> None:
    """Test validating a valid entry."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    entry = mod.ChangelogEntry(
        category="Added",
        description="New feature",
        version="1.0.0",
        date="2025-01-01"
    )
    issues = agent.validate_entry(entry)
    assert len(issues) == 0


def test_validate_entry_invalid_version(tmp_path: Path) -> None:
    """Test validating an entry with invalid version."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    entry = mod.ChangelogEntry(
        category="Added",
        description="New feature",
        version="invalid",
        date="2025-01-01"
    )
    issues = agent.validate_entry(entry)
    assert len(issues) > 0
    assert any(i["rule"] == "version_format" for i in issues)


def test_validate_entry_empty_description(tmp_path: Path) -> None:
    """Test validating an entry with empty description."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    entry = mod.ChangelogEntry(
        category="Added",
        description="",
        version="1.0.0",
        date="2025-01-01"
    )
    issues = agent.validate_entry(entry)
    assert len(issues) > 0


def test_add_validation_rule(tmp_path: Path) -> None:
    """Test adding a custom validation rule."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    rule = mod.ValidationRule(
        name="custom_rule",
        pattern=r"^[A-Z]",
        message="Must start with uppercase",
        severity="warning"
    )
    agent.add_validation_rule(rule)
    assert any(r.name == "custom_rule" for r in agent._validation_rules)


def test_validate_changelog_detects_conflicts(tmp_path: Path) -> None:
    """Test validate_changelog detects merge conflicts."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    content = "<<<<<<< HEAD\nours\n=======\ntheirs\n>>>>>>> branch"
    issues = agent.validate_changelog(content)
    assert any(i["type"] == "merge_conflict" for i in issues)


def test_calculate_statistics(tmp_path: Path) -> None:
    """Test calculating changelog statistics."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    content = """## [1.0.0] - 2025-01-01
### Added
- Feature 1
- Feature 2
### Fixed
- Bug fix
"""
    target.write_text(content, encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    stats = agent.calculate_statistics()
    assert stats["version_count"] == 1
    assert stats["latest_version"] == "1.0.0"
    assert stats["total_entries"] >= 0


def test_calculate_statistics_multiple_versions(tmp_path: Path) -> None:
    """Test statistics with multiple versions."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    content = """## [2.0.0] - 2025-02-01
### Added
- Feature 3

## [1.0.0] - 2025-01-01
### Added
- Feature 1
"""
    target.write_text(content, encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    stats = agent.calculate_statistics()
    assert stats["version_count"] == 2


def test_add_entry(tmp_path: Path) -> None:
    """Test adding a changelog entry."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    entry = agent.add_entry(
        category="Added",
        description="New feature",
        priority=1,
        tags=["enhancement"]
    )
    assert entry.category == "Added"
    assert entry.description == "New feature"
    assert "enhancement" in entry.tags
    assert len(agent._entries) == 1


def test_get_entries_by_category(tmp_path: Path) -> None:
    """Test getting entries by category."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    agent.add_entry(category="Added", description="Feature 1")
    agent.add_entry(category="Fixed", description="Bug fix")
    agent.add_entry(category="Added", description="Feature 2")
    added = agent.get_entries_by_category("Added")
    assert len(added) == 2


def test_get_entries_by_priority(tmp_path: Path) -> None:
    """Test getting entries by priority."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    agent.add_entry(category="Added", description="Low priority", priority=1)
    agent.add_entry(category="Added", description="High priority", priority=5)
    agent.add_entry(category="Added", description="Medium priority", priority=3)
    high_priority = agent.get_entries_by_priority(min_priority=3)
    assert len(high_priority) == 2
    assert high_priority[0].priority == 5


def test_deduplicate_entries(tmp_path: Path) -> None:
    """Test deduplicating entries."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    agent.add_entry(category="Added", description="Same feature")
    agent.add_entry(category="Added", description="Same feature")
    agent.add_entry(category="Added", description="Different feature")
    removed = agent.deduplicate_entries()
    assert removed == 1
    assert len(agent._entries) == 2


def test_format_entries_as_markdown(tmp_path: Path) -> None:
    """Test formatting entries as markdown."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    agent.add_entry(category="Added", description="New feature", tags=["enhancement"])
    agent.add_entry(category="Fixed", description="Bug fix")
    markdown = agent.format_entries_as_markdown()
    assert "### Added" in markdown
    assert "### Fixed" in markdown
    assert "New feature" in markdown
    assert "[enhancement]" in markdown


def test_format_entries_empty(tmp_path: Path) -> None:
    """Test formatting empty entries."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "test.changes.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    markdown = agent.format_entries_as_markdown()
    assert markdown == ""


def test_changelog_template_dataclass() -> None:
    """Test ChangelogTemplate dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    template = mod.ChangelogTemplate(
        name="Test",
        project_type="test",
        sections=["Added", "Fixed"]
    )
    assert template.name == "Test"
    assert template.include_links is True  # default


def test_changelog_entry_dataclass() -> None:
    """Test ChangelogEntry dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    entry = mod.ChangelogEntry(
        category="Added",
        description="Test feature"
    )
    assert entry.priority == 0  # default
    assert entry.tags == []  # default


def test_validation_rule_dataclass() -> None:
    """Test ValidationRule dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    rule = mod.ValidationRule(
        name="test",
        pattern=r".*",
        message="Test message"
    )
    assert rule.severity == "error"  # default


def test_versioning_strategy_enum() -> None:
    """Test VersioningStrategy enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    assert mod.VersioningStrategy.SEMVER.value == "semver"
    assert mod.VersioningStrategy.CALVER.value == "calver"
    assert mod.VersioningStrategy.CUSTOM.value == "custom"


def test_localization_language_enum_values() -> None:
    """Test LocalizationLanguage enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    assert mod.LocalizationLanguage.ENGLISH.value == "en"
    assert mod.LocalizationLanguage.SPANISH.value == "es"
    assert mod.LocalizationLanguage.FRENCH.value == "fr"
    assert mod.LocalizationLanguage.GERMAN.value == "de"
    assert mod.LocalizationLanguage.JAPANESE.value == "ja"
    assert mod.LocalizationLanguage.CHINESE.value == "zh"
    assert mod.LocalizationLanguage.PORTUGUESE.value == "pt"


def test_diff_view_mode_enum_values() -> None:
    """Test DiffViewMode enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    assert mod.DiffViewMode.UNIFIED.value == "unified"
    assert mod.DiffViewMode.SIDE_BY_SIDE.value == "side_by_side"
    assert mod.DiffViewMode.INLINE.value == "inline"


def test_import_source_enum_values() -> None:
    """Test ImportSource enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    assert mod.ImportSource.GITHUB_RELEASES.value == "github_releases"
    assert mod.ImportSource.JIRA.value == "jira"
    assert mod.ImportSource.GITLAB.value == "gitlab"
    assert mod.ImportSource.MANUAL.value == "manual"


def test_compliance_category_enum_values() -> None:
    """Test ComplianceCategory enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    assert mod.ComplianceCategory.SECURITY.value == "security"
    assert mod.ComplianceCategory.LEGAL.value == "legal"
    assert mod.ComplianceCategory.PRIVACY.value == "privacy"
    assert mod.ComplianceCategory.ACCESSIBILITY.value == "accessibility"


def test_feed_format_enum_values() -> None:
    """Test FeedFormat enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    assert mod.FeedFormat.RSS_20.value == "rss_20"
    assert mod.FeedFormat.ATOM_10.value == "atom_10"
    assert mod.FeedFormat.JSON_FEED.value == "json_feed"


def test_grouping_strategy_enum_values() -> None:
    """Test GroupingStrategy enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    assert mod.GroupingStrategy.BY_DATE.value == "by_date"
    assert mod.GroupingStrategy.BY_VERSION.value == "by_version"
    assert mod.GroupingStrategy.BY_CATEGORY.value == "by_category"
    assert mod.GroupingStrategy.BY_AUTHOR.value == "by_author"


def test_localized_entry_dataclass() -> None:
    """Test LocalizedEntry dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    entry = mod.LocalizedEntry(
        original_text="Added new feature"
    )
    assert entry.language == mod.LocalizationLanguage.ENGLISH
    assert entry.translations == {}
    assert entry.auto_translated is False


def test_diff_result_dataclass() -> None:
    """Test DiffResult dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    result = mod.DiffResult()
    assert result.additions == []
    assert result.deletions == []
    assert result.unchanged == 0
    assert result.similarity_score == 0.0


def test_imported_entry_dataclass() -> None:
    """Test ImportedEntry dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    entry = mod.ImportedEntry(
        source=mod.ImportSource.GITHUB_RELEASES,
        external_id="123",
        title="Release 1.0",
        description="First release"
    )
    assert entry.author == ""
    assert entry.labels == []


def test_search_result_dataclass() -> None:
    """Test SearchResult dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    result = mod.SearchResult(
        version="1.0.0",
        line_number=10,
        context="Added new feature"
    )
    assert result.match_score == 1.0


def test_linked_reference_dataclass() -> None:
    """Test LinkedReference dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    ref = mod.LinkedReference(
        ref_type="commit",
        ref_id="abc123"
    )
    assert ref.url == ""
    assert ref.title == ""


def test_monorepo_entry_dataclass() -> None:
    """Test MonorepoEntry dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    entry = mod.MonorepoEntry(
        package_name="pkg-a",
        version="1.0.0"
    )
    assert entry.entries == []
    assert entry.path == ""


def test_release_note_dataclass() -> None:
    """Test ReleaseNote dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    note = mod.ReleaseNote(
        version="1.0.0",
        title="Release 1.0.0",
        summary="First release"
    )
    assert note.highlights == []
    assert note.breaking_changes == []


def test_compliance_result_dataclass() -> None:
    """Test ComplianceResult dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    result = mod.ComplianceResult(
        category=mod.ComplianceCategory.SECURITY,
        passed=True
    )
    assert result.issues == []
    assert result.recommendations == []


def test_entry_template_dataclass() -> None:
    """Test EntryTemplate dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    template = mod.EntryTemplate(
        name="bug_fix",
        template_text="Fixed {issue}"
    )
    assert template.placeholders == []
    assert template.description == ""


def test_changelog_localizer_create_entry() -> None:
    """Test ChangelogLocalizer create_entry method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    localizer = mod.ChangelogLocalizer()
    entry = localizer.create_entry("Added new feature")
    assert entry.original_text == "Added new feature"
    assert len(localizer.entries) == 1


def test_changelog_localizer_add_translation() -> None:
    """Test ChangelogLocalizer add_translation method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    localizer = mod.ChangelogLocalizer()
    entry = localizer.create_entry("Added new feature")
    localizer.add_translation(entry, mod.LocalizationLanguage.SPANISH, "Nueva característica")
    assert "es" in entry.translations
    assert entry.translations["es"] == "Nueva característica"


def test_changelog_localizer_get_localized_changelog() -> None:
    """Test ChangelogLocalizer get_localized_changelog method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    localizer = mod.ChangelogLocalizer()
    entry = localizer.create_entry("Hello")
    localizer.add_translation(entry, mod.LocalizationLanguage.SPANISH, "Hola")
    result = localizer.get_localized_changelog(mod.LocalizationLanguage.SPANISH)
    assert "Hola" in result


def test_changelog_localizer_fallback_to_original() -> None:
    """Test ChangelogLocalizer falls back to original when no translation."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    localizer = mod.ChangelogLocalizer()
    localizer.create_entry("Hello")
    result = localizer.get_localized_changelog(mod.LocalizationLanguage.FRENCH)
    assert "Hello" in result


def test_diff_visualizer_compare() -> None:
    """Test DiffVisualizer compare method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    visualizer = mod.DiffVisualizer()
    result = visualizer.compare("old line", "new line")
    assert isinstance(result, mod.DiffResult)
    assert len(result.additions) >= 1


def test_diff_visualizer_render_html_unified() -> None:
    """Test DiffVisualizer render_html with unified mode."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    visualizer = mod.DiffVisualizer()
    result = mod.DiffResult(additions=["new"], deletions=["old"])
    html = visualizer.render_html(result, mod.DiffViewMode.UNIFIED)
    assert "diff-unified" in html


def test_diff_visualizer_render_html_side_by_side() -> None:
    """Test DiffVisualizer render_html with side-by-side mode."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    visualizer = mod.DiffVisualizer()
    result = mod.DiffResult(additions=["new"], deletions=["old"])
    html = visualizer.render_html(result, mod.DiffViewMode.SIDE_BY_SIDE)
    assert "side-by-side" in html


def test_external_importer_import_github_releases() -> None:
    """Test ExternalImporter import_github_releases method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    importer = mod.ExternalImporter()
    entries = importer.import_github_releases("owner", "repo")
    assert len(entries) >= 1
    assert entries[0].source == mod.ImportSource.GITHUB_RELEASES


def test_external_importer_import_jira() -> None:
    """Test ExternalImporter import_jira method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    importer = mod.ExternalImporter()
    entries = importer.import_jira("PROJECT")
    assert len(entries) >= 1
    assert entries[0].source == mod.ImportSource.JIRA


def test_external_importer_convert_to_changelog_entries() -> None:
    """Test ExternalImporter convert_to_changelog_entries method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    importer = mod.ExternalImporter()
    importer.import_github_releases("owner", "repo")
    changelog_entries = importer.convert_to_changelog_entries()
    assert len(changelog_entries) >= 1
    assert changelog_entries[0].category == "Added"


def test_changelog_searcher_search() -> None:
    """Test ChangelogSearcher search method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    searcher = mod.ChangelogSearcher()
    content = """## [1.0.0]
### Added
- New feature for users
### Fixed
- Bug in login
"""
    results = searcher.search("feature", content)
    assert len(results) >= 1
    assert results[0].version == "1.0.0"


def test_changelog_searcher_search_no_results() -> None:
    """Test ChangelogSearcher search with no results."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    searcher = mod.ChangelogSearcher()
    results = searcher.search("nonexistent", "Some content")
    assert len(results) == 0


def test_changelog_searcher_score_calculation() -> None:
    """Test ChangelogSearcher calculates relevance scores."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    searcher = mod.ChangelogSearcher()
    results = searcher.search("bug", "- Fixed a bug")
    assert results[0].match_score > 0


def test_reference_link_manager_add_commit_reference() -> None:
    """Test ReferenceLinkManager add_commit_reference method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    manager = mod.ReferenceLinkManager()
    ref = manager.add_commit_reference("entry1", "abc123456", "http://example.com")
    assert ref.ref_type == "commit"
    assert ref.ref_id == "abc1234"


def test_reference_link_manager_add_issue_reference() -> None:
    """Test ReferenceLinkManager add_issue_reference method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    manager = mod.ReferenceLinkManager()
    ref = manager.add_issue_reference("entry1", "123", "http://example.com")
    assert ref.ref_type == "issue"
    assert ref.ref_id == "#123"


def test_reference_link_manager_format_references() -> None:
    """Test ReferenceLinkManager format_references method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    manager = mod.ReferenceLinkManager()
    manager.add_commit_reference("entry1", "abc123", "http://example.com")
    formatted = manager.format_references("entry1")
    assert "abc123" in formatted


def test_reference_link_manager_format_references_empty() -> None:
    """Test ReferenceLinkManager format_references with no refs."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    manager = mod.ReferenceLinkManager()
    formatted = manager.format_references("nonexistent")
    assert formatted == ""


def test_monorepo_aggregator_add_package() -> None:
    """Test MonorepoAggregator add_package method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    aggregator = mod.MonorepoAggregator()
    entry = aggregator.add_package("pkg-a", "1.0.0", [])
    assert entry.package_name == "pkg-a"
    assert "pkg-a" in aggregator.packages


def test_monorepo_aggregator_generate_unified_changelog() -> None:
    """Test MonorepoAggregator generate_unified_changelog method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    aggregator = mod.MonorepoAggregator()
    entries = [mod.ChangelogEntry(category="Added", description="Feature")]
    aggregator.add_package("pkg-a", "1.0.0", entries)
    changelog = aggregator.generate_unified_changelog()
    assert "pkg-a" in changelog
    assert "Feature" in changelog


def test_release_notes_generator_generate() -> None:
    """Test ReleaseNotesGenerator generate method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    generator = mod.ReleaseNotesGenerator()
    entries = [
        mod.ChangelogEntry(category="Added", description="New feature", priority=3),
        mod.ChangelogEntry(category="Fixed", description="Bug fix")
    ]
    notes = generator.generate("1.0.0", entries)
    assert notes.version == "1.0.0"
    assert "1.0.0" in notes.title
    assert len(notes.highlights) >= 1


def test_release_notes_generator_breaking_changes() -> None:
    """Test ReleaseNotesGenerator extracts breaking changes."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    generator = mod.ReleaseNotesGenerator()
    entries = [
        mod.ChangelogEntry(category="Changed", description="Breaking change in API")
    ]
    notes = generator.generate("2.0.0", entries)
    assert len(notes.breaking_changes) >= 1


def test_feed_generator_generate_atom() -> None:
    """Test FeedGenerator generate with Atom format."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    generator = mod.FeedGenerator(mod.FeedFormat.ATOM_10)
    entries = [mod.ChangelogEntry(category="Added", description="Feature")]
    feed = generator.generate(entries, "Test Project")
    assert "<feed" in feed
    assert "Test Project" in feed


def test_feed_generator_generate_rss() -> None:
    """Test FeedGenerator generate with RSS format."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    generator = mod.FeedGenerator(mod.FeedFormat.RSS_20)
    entries = [mod.ChangelogEntry(category="Added", description="Feature")]
    feed = generator.generate(entries, "Test Project")
    assert "<rss" in feed


def test_feed_generator_generate_json() -> None:
    """Test FeedGenerator generate with JSON Feed format."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    generator = mod.FeedGenerator(mod.FeedFormat.JSON_FEED)
    entries = [mod.ChangelogEntry(category="Added", description="Feature")]
    feed = generator.generate(entries, "Test Project")
    assert "jsonfeed.org" in feed


def test_compliance_checker_check_security() -> None:
    """Test ComplianceChecker check_security_compliance method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    checker = mod.ComplianceChecker()
    entries = [
        mod.ChangelogEntry(category="Added", description="Fixed security vulnerability")
    ]
    result = checker.check_security_compliance(entries)
    assert result.category == mod.ComplianceCategory.SECURITY
    assert len(result.issues) >= 1


def test_compliance_checker_check_legal() -> None:
    """Test ComplianceChecker check_legal_compliance method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    checker = mod.ComplianceChecker()
    entries = [
        mod.ChangelogEntry(category="Changed", description="Updated license")
    ]
    result = checker.check_legal_compliance(entries)
    assert result.category == mod.ComplianceCategory.LEGAL


def test_compliance_checker_check_all() -> None:
    """Test ComplianceChecker check_all method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    checker = mod.ComplianceChecker()
    entries = [mod.ChangelogEntry(category="Added", description="Feature")]
    results = checker.check_all(entries)
    assert len(results) >= 2


def test_entry_reorderer_reorder_by_category() -> None:
    """Test EntryReorderer reorder by category."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    reorderer = mod.EntryReorderer()
    entries = [
        mod.ChangelogEntry(category="Fixed", description="Bug"),
        mod.ChangelogEntry(category="Added", description="Feature")
    ]
    sorted_entries = reorderer.reorder(entries, mod.GroupingStrategy.BY_CATEGORY)
    assert sorted_entries[0].category == "Added"


def test_entry_reorderer_group_by_category() -> None:
    """Test EntryReorderer group_by_category method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    reorderer = mod.EntryReorderer()
    entries = [
        mod.ChangelogEntry(category="Added", description="Feature1"),
        mod.ChangelogEntry(category="Added", description="Feature2"),
        mod.ChangelogEntry(category="Fixed", description="Bug")
    ]
    grouped = reorderer.group_by_category(entries)
    assert len(grouped["Added"]) == 2
    assert len(grouped["Fixed"]) == 1


def test_template_manager_add_template() -> None:
    """Test TemplateManager add_template method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    manager = mod.TemplateManager()
    template = manager.add_template("bug_fix", "Fixed {issue} in {component}")
    assert template.name == "bug_fix"
    assert "issue" in template.placeholders
    assert "component" in template.placeholders


def test_template_manager_apply_template() -> None:
    """Test TemplateManager apply_template method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    manager = mod.TemplateManager()
    manager.add_template("bug_fix", "Fixed {issue} in {component}")
    result = manager.apply_template("bug_fix", {"issue": "#123", "component": "auth"})
    assert result == "Fixed #123 in auth"


def test_template_manager_get_placeholders() -> None:
    """Test TemplateManager get_template_placeholders method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    manager = mod.TemplateManager()
    manager.add_template("feature", "Added {name} to {module}")
    placeholders = manager.get_template_placeholders("feature")
    assert "name" in placeholders
    assert "module" in placeholders


def test_template_manager_apply_nonexistent_template() -> None:
    """Test TemplateManager apply_template with nonexistent template."""
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    manager = mod.TemplateManager()
    result = manager.apply_template("nonexistent", {})
    assert result == ""
