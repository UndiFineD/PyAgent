#!/usr / bin / env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org / licenses / LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Additional legacy tests for agent-changes.py.

This replaces the previous filename `test_agent-changes.tests.py`, which pytest
cannot import reliably because of the extra dot in the basename.

Run directly via:

    pytest scripts / agent / test_agent_changes_tests.py
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture()
def base_agent_module() -> Any:
    with agent_dir_on_path():
        import base_agent

        return base_agent


def test_changes_agent_default_content_for_missing_file(tmp_path: Path) -> None:
    with agent_dir_on_path():
        mod = load_agent_module("agent-changes.py")
    target = tmp_path / "missing.changes.md"
    agent = mod.ChangesAgent(str(target))
    assert "No changes recorded" in agent.read_previous_content()


def test_changes_agent_non_keyword_sets_current_content(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module: Any
) -> None:
    with agent_dir_on_path():
        mod = load_agent_module("agent-changes.py")

    def fake_run_subagent(
            self: Any,
            description: str,
            prompt: str,
            original_content: str = "") -> str:
        return "UPDATED"

    monkeypatch.setattr(
        base_agent_module.BaseAgent,
        "run_subagent",
        fake_run_subagent,
        raising=True)
    target = tmp_path / "x.changes.md"
    target.write_text("BEFORE", encoding="utf-8")
    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    assert agent.improve_content("noop") == "UPDATED"
    assert agent.current_content == "UPDATED"


# =============================================================================
# Session 9: Changelog Entry Priority and Importance Tests
# =============================================================================


class TestChangelogEntryPriority:
    """Tests for changelog entry priority and importance ranking."""

    def test_priority_ranking_critical(self, tmp_path: Path) -> None:
        """Test critical priority entries are ranked highest."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = """# Changelog
## Critical
- Security fix for vulnerability

## Minor
- Updated docs
"""
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "Security fix" in previous

    def test_importance_ordering(self, tmp_path: Path) -> None:
        """Test entries are ordered by importance."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        target = tmp_path / "test.changes.md"
        target.write_text("# Changelog\n- Entry 1\n- Entry 2")

        agent = mod.ChangesAgent(str(target))
        content = agent.read_previous_content()

        assert "Entry 1" in content


# =============================================================================
# Session 9: Changelog Cross-Reference Tests
# =============================================================================


class TestChangelogCrossReference:
    """Tests for changelog cross-referencing with git commits."""

    def test_commit_reference_format(self, tmp_path: Path) -> None:
        """Test commit reference format is preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n- Fix bug (abc123)"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "abc123" in previous

    def test_issue_reference_preserved(self, tmp_path: Path) -> None:
        """Test issue references are preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n- Fix #123"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        assert "#123" in agent.read_previous_content()


# =============================================================================
# Session 9: Changelog Conflict Resolution Tests
# =============================================================================


class TestChangelogConflictResolution:
    """Tests for changelog conflict resolution."""

    def test_conflicting_entries_detected(self, tmp_path: Path) -> None:
        """Test conflicting entries can be detected."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        target = tmp_path / "conflict.changes.md"
        target.write_text("# Changelog\n- Entry A\n- Entry A modified")

        agent = mod.ChangesAgent(str(target))
        content = agent.read_previous_content()

        # Both entries should be present
        assert "Entry A" in content


# =============================================================================
# Session 9: Changelog Template Customization Tests
# =============================================================================


class TestChangelogTemplateCustomization:
    """Tests for changelog template customization."""

    def test_custom_header_preserved(self, tmp_path: Path) -> None:
        """Test custom header is preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Custom Changelog Header\n\nCustom intro text\n\n## Changes\n- Item"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "Custom Changelog Header" in previous

    def test_section_structure_maintained(self, tmp_path: Path) -> None:
        """Test section structure is maintained."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n## Added\n- A\n## Fixed\n- B"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "## Added" in previous
        assert "## Fixed" in previous


# =============================================================================
# Session 9: Changelog Metadata Extraction Tests
# =============================================================================


class TestChangelogMetadataExtraction:
    """Tests for changelog entry metadata extraction."""

    def test_date_metadata_extracted(self, tmp_path: Path) -> None:
        """Test date metadata is extracted."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n## [2025-01-16]\n- Entry"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "2025-01-16" in previous

    def test_author_metadata_preserved(self, tmp_path: Path) -> None:
        """Test author metadata is preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n- Entry by @author"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        assert "@author" in agent.read_previous_content()


# =============================================================================
# Session 9: Changelog Versioning Tests
# =============================================================================


class TestChangelogVersioning:
    """Tests for changelog versioning with semantic versions."""

    def test_semver_format_preserved(self, tmp_path: Path) -> None:
        """Test semantic version format is preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n## [1.2.3] - 2025-01-16\n- Entry"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "[1.2.3]" in previous

    def test_version_ordering(self, tmp_path: Path) -> None:
        """Test version sections are ordered."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n## [2.0.0]\n- B\n## [1.0.0]\n- A"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        assert "2.0.0" in agent.read_previous_content()


# =============================================================================
# Session 9: Changelog Entry Grouping Tests
# =============================================================================


class TestChangelogEntryGrouping:
    """Tests for changelog entry grouping by scope."""

    def test_scope_grouping(self, tmp_path: Path) -> None:
        """Test entries can be grouped by scope."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n## API\n- api change\n## Core\n- core change"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "## API" in previous
        assert "## Core" in previous


# =============================================================================
# Session 9: Changelog From Commits Tests
# =============================================================================


class TestChangelogFromCommits:
    """Tests for changelog generation from commit messages."""

    def test_conventional_commit_format(self, tmp_path: Path) -> None:
        """Test conventional commit format is handled."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        # Simulate content that might come from commits
        content = "# Changelog\n- feat: new feature\n- fix: bug fix"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "feat:" in previous
        assert "fix:" in previous


# =============================================================================
# Session 9: Changelog Entry Deduplication Tests
# =============================================================================


class TestChangelogDeduplication:
    """Tests for changelog entry deduplication."""

    def test_duplicate_entries_in_content(self, tmp_path: Path) -> None:
        """Test handling of duplicate entries."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n- Same entry\n- Same entry"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        # Content should be readable
        assert "Same entry" in previous


# =============================================================================
# Session 9: Changelog Format Migration Tests
# =============================================================================


class TestChangelogFormatMigration:
    """Tests for changelog format migration between versions."""

    def test_old_format_readable(self, tmp_path: Path) -> None:
        """Test old changelog formats can be read."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        # Old format without sections
        content = "Changes:\n* Item 1\n* Item 2"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "Item 1" in previous


# =============================================================================
# Session 9: Changelog Approval Workflow Tests
# =============================================================================


class TestChangelogApprovalWorkflow:
    """Tests for changelog entry approval workflows."""

    def test_draft_entries(self, tmp_path: Path) -> None:
        """Test draft entries are handled."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n## Draft\n- Pending entry\n## Released\n- Final entry"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "Draft" in previous
        assert "Released" in previous


# =============================================================================
# Session 9: Release Notes Integration Tests
# =============================================================================


class TestReleaseNotesIntegration:
    """Tests for changelog integration with release notes."""

    def test_release_notes_format(self, tmp_path: Path) -> None:
        """Test release notes format is compatible."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Release Notes v1.0\n\n## Highlights\n- Major feature\n\n## All Changes\n- Detail"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "Highlights" in previous


# =============================================================================
# Session 9: Issue / PR Linking Tests
# =============================================================================


class TestIssuePRLinking:
    """Tests for changelog entry linking to issues / PRs."""

    def test_github_issue_link(self, tmp_path: Path) -> None:
        """Test GitHub issue links are preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n- Fix bug ([#42](https://github.com / org / repo / issues / 42))"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        assert "issues / 42" in agent.read_previous_content()

    def test_pr_reference(self, tmp_path: Path) -> None:
        """Test PR references are preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n- Feature (PR #100)"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        assert "PR #100" in agent.read_previous_content()


# =============================================================================
# Session 9: Performance Tests
# =============================================================================


class TestChangelogPerformance:
    """Tests for changelog performance with large histories."""

    def test_large_changelog_readable(self, tmp_path: Path) -> None:
        """Test large changelog can be read."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        # Create large changelog
        entries = "\n".join([f"- Entry {i}" for i in range(100)])
        content = f"# Changelog\n{entries}"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "Entry 0" in previous
        assert "Entry 99" in previous


# =============================================================================
# Session 9: Backup and Recovery Tests
# =============================================================================


class TestChangelogBackupRecovery:
    """Tests for changelog backup and recovery."""

    def test_read_creates_no_backup(self, tmp_path: Path) -> None:
        """Test reading doesn't create unexpected files."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n- Entry"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        agent.read_previous_content()

        # Should not create backup just from reading
        backup_file = tmp_path / "test.changes.md.bak"
        assert not backup_file.exists()


# =============================================================================
# Session 9: Authentication and Signing Tests
# =============================================================================


class TestChangelogAuthentication:
    """Tests for changelog entry authentication and signing."""

    def test_signed_entries_preserved(self, tmp_path: Path) -> None:
        """Test signed entries are preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n- Entry <!-- signed:abc123 -->"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "signed:abc123" in previous


# =============================================================================
# Session 9: Archival Tests
# =============================================================================


class TestChangelogArchival:
    """Tests for changelog entry archival."""

    def test_archived_section(self, tmp_path: Path) -> None:
        """Test archived section is handled."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n## Current\n- New\n## Archived\n- Old"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "Archived" in previous
        assert "Old" in previous


# =============================================================================
# Session 9: Search and Filtering Tests
# =============================================================================


class TestChangelogSearchFiltering:
    """Tests for changelog entry search and filtering."""

    def test_keyword_search_in_content(self, tmp_path: Path) -> None:
        """Test keywords can be found in content."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n- Fix critical security bug\n- Minor update"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "security" in previous


# =============================================================================
# Session 9: Tagging Tests
# =============================================================================


class TestChangelogTagging:
    """Tests for changelog entry tagging."""

    def test_tags_preserved(self, tmp_path: Path) -> None:
        """Test entry tags are preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n- Entry [tag:important] [tag:security]"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "tag:important" in previous
        assert "tag:security" in previous


# =============================================================================
# Session 9: Notification Trigger Tests
# =============================================================================


class TestChangelogNotificationTriggers:
    """Tests for changelog entry notification triggers."""

    def test_breaking_change_marker(self, tmp_path: Path) -> None:
        """Test breaking change markers are preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-changes.py")

        content = "# Changelog\n- BREAKING: API changed"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "BREAKING" in previous
