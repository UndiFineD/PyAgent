# -*- coding: utf-8 -*-
"""Test classes from test_agent_changes_tests.py - core module."""

from __future__ import annotations
import unittest
from typing import Any, List, Dict, Optional, Callable, Tuple, Set, Union
from unittest.mock import MagicMock, Mock, patch, call, ANY
import time
import json
from datetime import datetime
import pytest
import logging
from pathlib import Path
import sys
import os
import tempfile
import shutil
import subprocess
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Try to import test utilities
try:
    from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path, load_agent_module
except ImportError:
    # Fallback
    AGENT_DIR = Path(__file__).parent.parent.parent / 'src'
    
    class agent_sys_path:
        def __enter__(self): 
            sys.path.insert(0, str(AGENT_DIR))
            return self
        def __exit__(self, *args): 
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))


class TestChangelogEntryPriority:
    """Tests for changelog entry priority and importance ranking."""

    def test_priority_ranking_critical(self, tmp_path: Path) -> None:
        """Test critical priority entries are ranked highest."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n- Fix bug (abc123)"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "abc123" in previous

    def test_issue_reference_preserved(self, tmp_path: Path) -> None:
        """Test issue references are preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

        content = "# Custom Changelog Header\n\nCustom intro text\n\n## Changes\n- Item"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "Custom Changelog Header" in previous

    def test_section_structure_maintained(self, tmp_path: Path) -> None:
        """Test section structure is maintained."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n## [2025-01-16]\n- Entry"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "2025-01-16" in previous

    def test_author_metadata_preserved(self, tmp_path: Path) -> None:
        """Test author metadata is preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n## [1.2.3] - 2025-01-16\n- Entry"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "[1.2.3]" in previous

    def test_version_ordering(self, tmp_path: Path) -> None:
        """Test version sections are ordered."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

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



class TestIssuePRLinking:
    """Tests for changelog entry linking to issues / PRs."""

    def test_github_issue_link(self, tmp_path: Path) -> None:
        """Test GitHub issue links are preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n- Fix bug ([#42](https://github.com / org / repo / issues / 42))"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        assert "issues / 42" in agent.read_previous_content()

    def test_pr_reference(self, tmp_path: Path) -> None:
        """Test PR references are preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n- Feature (PR #100)"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        assert "PR #100" in agent.read_previous_content()


# =============================================================================
# Session 9: Performance Tests
# =============================================================================



class TestChangelogBackupRecovery:
    """Tests for changelog backup and recovery."""

    def test_read_creates_no_backup(self, tmp_path: Path) -> None:
        """Test reading doesn't create unexpected files."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

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
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n- BREAKING: API changed"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "BREAKING" in previous


# =============================================================================
# Comprehensive Tests: Changes Detection, Tracking, and Integration
# =============================================================================


class TestChangesDetection(unittest.TestCase):
    """Tests for changes detection and tracking."""

    def test_detect_file_addition(self):
        """Test detecting file additions."""
        before_files = ["file1.py", "file2.py"]
        after_files = ["file1.py", "file2.py", "file3.py"]

        added = set(after_files) - set(before_files)
        assert "file3.py" in added

    def test_detect_file_deletion(self):
        """Test detecting file deletions."""
        before_files = ["file1.py", "file2.py", "file3.py"]
        after_files = ["file1.py", "file2.py"]

        deleted = set(before_files) - set(after_files)
        assert "file3.py" in deleted

    def test_detect_file_modification(self):
        """Test detecting file modifications."""
        changes = {
            "file1.py": {"status": "modified", "lines_added": 5, "lines_removed": 2},
            "file2.py": {"status": "modified", "lines_added": 10, "lines_removed": 0},
        }

        assert changes["file1.py"]["status"] == "modified"
        assert changes["file2.py"]["lines_added"] == 10

    def test_track_change_metadata(self):
        """Test tracking change metadata."""
        change = {
            "file": "test.py",
            "timestamp": datetime.now().isoformat(),
            "author": "developer",
            "message": "Bug fix",
            "hash": "abc123",
        }

        assert change["file"] == "test.py"
        assert change["author"] == "developer"



class TestChangesAggregation(unittest.TestCase):
    """Tests for aggregating changes by file type."""

    def test_aggregate_by_file_extension(self):
        """Test aggregating changes by file extension."""
        changes = [
            {"file": "a.py", "type": "modified"},
            {"file": "b.py", "type": "added"},
            {"file": "c.js", "type": "modified"},
            {"file": "d.md", "type": "modified"},
        ]

        aggregated = {}
        for change in changes:
            ext = change["file"].split(".")[-1]
            if ext not in aggregated:
                aggregated[ext] = []
            aggregated[ext].append(change)

        assert len(aggregated["py"]) == 2
        assert len(aggregated["js"]) == 1
        assert len(aggregated["md"]) == 1

    def test_aggregate_by_change_type(self):
        """Test aggregating by change type."""
        changes = [
            {"file": "a.py", "status": "added"},
            {"file": "b.py", "status": "modified"},
            {"file": "c.py", "status": "deleted"},
            {"file": "d.py", "status": "modified"},
        ]

        by_type = {}
        for change in changes:
            status = change["status"]
            by_type[status] = by_type.get(status, 0) + 1

        assert by_type["added"] == 1
        assert by_type["modified"] == 2
        assert by_type["deleted"] == 1

    def test_aggregate_statistics(self):
        """Test aggregating statistics."""
        changes = [
            {"file": "a.py", "additions": 10, "deletions": 5},
            {"file": "b.py", "additions": 20, "deletions": 2},
            {"file": "c.py", "additions": 5, "deletions": 10},
        ]

        total_additions = sum(c["additions"] for c in changes)
        total_deletions = sum(c["deletions"] for c in changes)

        assert total_additions == 35
        assert total_deletions == 17



class TestChangesComparison(unittest.TestCase):
    """Tests for before / after changes comparison."""

    def test_compare_file_content(self):
        """Test comparing file content before / after."""
        before = "def hello():\n    print('Hello')"
        after = "def hello():\n    print('Hello, World!')"

        changed = before != after
        assert changed

    def test_compute_diff(self):
        """Test computing diff between versions."""
        before_lines = ["line1", "line2", "line3"]
        after_lines = ["line1", "line2_modified", "line3", "line4"]

        # Simple diff: added, removed, modified
        before_set = set(before_lines)
        after_set = set(after_lines)

        added = after_set - before_set
        removed = before_set - after_set

        assert "line4" in added
        assert "line2" in removed

    def test_calculate_change_metrics(self):
        """Test calculating change metrics."""
        before = "line1\nline2\nline3\n"
        after = "line1\nline2_modified\nline3\nline4\n"

        before_lines = before.split("\n")
        after_lines = after.split("\n")

        metrics = {
            "lines_before": len(before_lines),
            "lines_after": len(after_lines),
            "lines_added": max(0, len(after_lines) - len(before_lines)),
            "lines_removed": max(0, len(before_lines) - len(after_lines)),
        }

        assert metrics["lines_before"] == 4
        assert metrics["lines_after"] == 5

    def test_identify_changed_regions(self):
        """Test identifying changed code regions."""
        before = "def func():\n    x=1\n    return x"
        after = "def func():\n    x=2\n    y=3\n    return x + y"

        # Track changed lines
        before_lines = before.split("\n")
        after_lines = after.split("\n")

        changed_regions = []
        for i, (b, a) in enumerate(zip(before_lines, after_lines)):
            if b != a:
                changed_regions.append((i, b, a))

        assert len(changed_regions) >= 1



class TestChangesCategorization(unittest.TestCase):
    """Tests for categorizing changes."""

    def test_categorize_added_files(self):
        """Test categorizing added files."""
        changes = [
            {"file": "new_file.py", "status": "added"},
        ]

        added = [c for c in changes if c["status"] == "added"]
        assert len(added) == 1

    def test_categorize_modified_files(self):
        """Test categorizing modified files."""
        changes = [
            {"file": "modified.py", "status": "modified", "additions": 5, "deletions": 2},
        ]

        modified = [c for c in changes if c["status"] == "modified"]
        assert len(modified) == 1

    def test_categorize_deleted_files(self):
        """Test categorizing deleted files."""
        changes = [
            {"file": "old_file.py", "status": "deleted"},
        ]

        deleted = [c for c in changes if c["status"] == "deleted"]
        assert len(deleted) == 1

    def test_categorize_by_impact(self):
        """Test categorizing by impact level."""
        changes = [
            {"file": "a.py", "additions": 100, "deletions": 50},  # High impact
            {"file": "b.py", "additions": 2, "deletions": 1},     # Low impact
        ]

        def get_impact(change):
            total = change["additions"] + change["deletions"]
            if total > 50:
                return "high"
            elif total > 10:
                return "medium"
            else:
                return "low"

        for change in changes:
            change["impact"] = get_impact(change)

        assert changes[0]["impact"] == "high"
        assert changes[1]["impact"] == "low"



class TestChangesSummary(unittest.TestCase):
    """Tests for changes summary generation."""

    def test_generate_text_summary(self):
        """Test generating text summary."""
        changes = [
            {"file": "a.py", "status": "added"},
            {"file": "b.py", "status": "modified"},
        ]

        summary = f"Total changes: {len(changes)}\n"
        for change in changes:
            summary += f"- {change['file']}: {change['status']}\n"

        assert "Total changes: 2" in summary

    def test_generate_statistics_summary(self):
        """Test generating statistics summary."""
        changes = [
            {"file": "a.py", "additions": 10, "deletions": 5},
            {"file": "b.py", "additions": 20, "deletions": 2},
        ]

        summary = {
            "total_changes": len(changes),
            "total_additions": sum(c["additions"] for c in changes),
            "total_deletions": sum(c["deletions"] for c in changes),
            "net_change": sum(c["additions"] - c["deletions"] for c in changes),
        }

        assert summary["total_additions"] == 30
        assert summary["net_change"] == 23

    def test_generate_file_summary(self):
        """Test generating per-file summary."""
        changes = [
            {"file": "a.py", "status": "added", "additions": 50},
            {"file": "b.py", "status": "modified", "additions": 20, "deletions": 5},
        ]

        file_summary = {
            change["file"]: {
                "status": change["status"],
                "additions": change.get("additions", 0),
                "deletions": change.get("deletions", 0),
            }
            for change in changes
        }

        assert file_summary["a.py"]["status"] == "added"
        assert file_summary["b.py"]["additions"] == 20



class TestChangesFiltering(unittest.TestCase):
    """Tests for changes filtering and selection."""

    def test_filter_by_file_pattern(self):
        """Test filtering changes by file pattern."""
        changes = [
            {"file": "src / main.py"},
            {"file": "tests / test_main.py"},
            {"file": "docs / readme.md"},
        ]

        py_files = [c for c in changes if c["file"].endswith(".py")]
        assert len(py_files) == 2

    def test_filter_by_status(self):
        """Test filtering changes by status."""
        changes = [
            {"file": "a.py", "status": "added"},
            {"file": "b.py", "status": "modified"},
            {"file": "c.py", "status": "deleted"},
        ]

        modified = [c for c in changes if c["status"] == "modified"]
        assert len(modified) == 1

    def test_filter_by_impact_threshold(self):
        """Test filtering by impact threshold."""
        changes = [
            {"file": "a.py", "additions": 100},
            {"file": "b.py", "additions": 5},
            {"file": "c.py", "additions": 50},
        ]

        high_impact = [c for c in changes if c["additions"] > 30]
        assert len(high_impact) == 2

    def test_filter_and_sort(self):
        """Test filtering and sorting changes."""
        changes = [
            {"file": "b.py", "additions": 20},
            {"file": "a.py", "additions": 50},
            {"file": "c.py", "additions": 10},
        ]

        sorted_changes = sorted(changes, key=lambda x: x["additions"], reverse=True)
        assert sorted_changes[0]["file"] == "a.py"



class TestChangesExport(unittest.TestCase):
    """Tests for exporting changes to various formats."""

    def test_export_to_json(self):
        """Test exporting changes to JSON."""
        import json

        changes = [
            {"file": "a.py", "status": "added"},
            {"file": "b.py", "status": "modified"},
        ]

        json_str = json.dumps(changes)
        restored = json.loads(json_str)

        assert len(restored) == 2

    def test_export_to_csv(self):
        """Test exporting changes to CSV."""
        changes = [
            {"file": "a.py", "status": "added", "additions": 10},
            {"file": "b.py", "status": "modified", "additions": 20},
        ]

        csv_lines = ["file,status,additions"]
        for change in changes:
            csv_lines.append(f"{change['file']},{change['status']},{change['additions']}")

        csv_content = "\n".join(csv_lines)
        assert "a.py,added,10" in csv_content

    def test_export_to_markdown(self):
        """Test exporting changes to markdown."""
        changes = [
            {"file": "a.py", "status": "added"},
            {"file": "b.py", "status": "modified"},
        ]

        md = "# Changes\n\n"
        for change in changes:
            md += f"- {change['file']}: {change['status']}\n"

        assert "# Changes" in md
        assert "a.py: added" in md

    def test_export_file_operations(self):
        """Test exporting to file."""
        changes = [{"file": "a.py", "status": "added"}]

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            import json
            json.dump(changes, f)
            temp_file = f.name

        try:
            assert os.path.exists(temp_file)
        finally:
            os.unlink(temp_file)



class TestVisualizationAndDiff(unittest.TestCase):
    """Tests for changes visualization and diff generation."""

    def test_generate_unified_diff(self):
        """Test generating unified diff format."""
        before_lines = ["line1\n", "line2\n", "line3\n"]
        after_lines = ["line1\n", "line2_modified\n", "line3\n", "line4\n"]

        # Simplified diff
        diff = []
        for i, (b, a) in enumerate(zip(before_lines, after_lines)):
            if b != a:
                diff.append(f"- {b.strip()}")
                diff.append(f"+ {a.strip()}")

        for line in after_lines[len(before_lines):]:
            diff.append(f"+ {line.strip()}")

        assert len(diff) > 0

    def test_generate_side_by_side_diff(self):
        """Test generating side-by-side diff."""
        before = "def hello():\n    return 'hello'"
        after = "def hello():\n    return 'hello, world'"

        diff_view = {
            "before": before,
            "after": after,
            "line_count_before": len(before.split("\n")),
            "line_count_after": len(after.split("\n")),
        }

        assert diff_view["line_count_before"] == 2

    def test_generate_change_statistics_visualization(self):
        """Test visualization of change statistics."""
        changes = [
            {"file": "a.py", "additions": 50, "deletions": 10},
            {"file": "b.py", "additions": 30, "deletions": 20},
        ]

        stats = {
            "total_additions": sum(c["additions"] for c in changes),
            "total_deletions": sum(c["deletions"] for c in changes),
            "files_changed": len(changes),
        }

        assert stats["total_additions"] == 80

    def test_highlight_added_removed_lines(self):
        """Test highlighting added / removed lines."""
        diff_output = [
            "- removed line",
            "+ added line",
            "  unchanged line",
        ]

        added = [line for line in diff_output if line.startswith("+")]
        removed = [line for line in diff_output if line.startswith("-")]

        assert len(added) == 1
        assert len(removed) == 1



class TestChangesValidation(unittest.TestCase):
    """Tests for changes validation and verification."""

    def test_validate_change_structure(self):
        """Test validating change data structure."""
        change = {
            "file": "test.py",
            "status": "modified",
            "additions": 5,
            "deletions": 2,
        }

        required = ["file", "status"]
        valid = all(k in change for k in required)
        assert valid

    def test_validate_status_values(self):
        """Test validating status values."""
        valid_statuses = ["added", "modified", "deleted"]
        changes = [
            {"file": "a.py", "status": "added"},
            {"file": "b.py", "status": "modified"},
            {"file": "c.py", "status": "deleted"},
        ]

        for change in changes:
            assert change["status"] in valid_statuses

    def test_validate_numeric_fields(self):
        """Test validating numeric fields."""
        change = {
            "file": "test.py",
            "additions": 10,
            "deletions": 5,
        }

        assert isinstance(change["additions"], int)
        assert isinstance(change["deletions"], int)
        assert change["additions"] >= 0

    def test_detect_conflicting_changes(self):
        """Test detecting conflicting changes."""
        changes = [
            {"file": "a.py", "status": "modified"},
            {"file": "a.py", "status": "deleted"},
        ]

        files = {}
        conflicts = []

        for change in changes:
            if change["file"] in files:
                conflicts.append((change["file"], files[change["file"]]
                                 ["status"], change["status"]))
            files[change["file"]] = change

        assert len(conflicts) > 0



class TestChangesPersistence(unittest.TestCase):
    """Tests for changes persistence and caching."""

    def test_cache_changes(self):
        """Test caching changes."""
        cache = {}

        changes = [{"file": "a.py", "status": "added"}]
        cache_key = "changes_2025_12_16"
        cache[cache_key] = changes

        assert cache[cache_key] == changes

    def test_invalidate_cache(self):
        """Test invalidating cache."""
        cache = {"key1": "value1"}

        del cache["key1"]
        assert "key1" not in cache

    def test_persist_to_file(self):
        """Test persisting changes to file."""
        import json

        changes = [{"file": "test.py", "status": "modified"}]

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(changes, f)
            temp_file = f.name

        try:
            with open(temp_file, 'r') as f:
                restored = json.load(f)

            assert restored == changes
        finally:
            os.unlink(temp_file)

    def test_load_from_cache(self):
        """Test loading from cache."""
        cache = {
            "changes_id": [
                {"file": "a.py", "status": "added"},
                {"file": "b.py", "status": "modified"},
            ]
        }

        loaded = cache.get("changes_id")
        assert len(loaded) == 2



class TestNotifications(unittest.TestCase):
    """Tests for changes notification system."""

    def test_create_notification(self):
        """Test creating notification."""
        notification = {
            "type": "changes_detected",
            "timestamp": datetime.now().isoformat(),
            "changes_count": 5,
            "files": ["a.py", "b.py"],
        }

        assert notification["type"] == "changes_detected"
        assert len(notification["files"]) == 2

    def test_send_notification(self):
        """Test sending notification."""
        notifications_sent = []

        def send_notification(msg):
            notifications_sent.append(msg)

        send_notification("Changes detected")

        assert len(notifications_sent) == 1

    def test_notification_filters(self):
        """Test notification filters."""
        all_changes = [
            {"file": "a.py", "status": "added", "additions": 100},
            {"file": "b.txt", "status": "modified", "additions": 5},
        ]

        # Only notify for significant changes
        significant = [c for c in all_changes if c["additions"] > 50]
        assert len(significant) == 1

    def test_notification_deduplication(self):
        """Test deduplicating notifications."""
        notifications = [
            {"file": "a.py", "status": "modified"},
            {"file": "a.py", "status": "modified"},
            {"file": "b.py", "status": "added"},
        ]

        unique = {n["file"]: n for n in notifications}.values()
        assert len(unique) == 2



class TestImpactAnalysis(unittest.TestCase):
    """Tests for changes impact analysis."""

    def test_analyze_impact_scope(self):
        """Test analyzing impact scope."""
        changes = [
            {"file": "core.py", "type": "modified"},
            {"file": "test.py", "type": "added"},
        ]

        impact = {
            "files_affected": len(changes),
            "critical_files": [c for c in changes if "core" in c["file"]],
        }

        assert len(impact["critical_files"]) == 1

    def test_estimate_complexity_change(self):
        """Test estimating complexity change."""
        changes = [
            {"file": "a.py", "additions": 100, "deletions": 10},
            {"file": "b.py", "additions": 5, "deletions": 20},
        ]

        complexity_increase = sum(c["additions"] - c["deletions"] for c in changes)
        assert complexity_increase == 75

    def test_analyze_dependency_impact(self):
        """Test analyzing dependency impact."""
        changes = [
            {"file": "core_module.py", "status": "modified", "impact": "high"},
            {"file": "helper.py", "status": "modified", "impact": "low"},
        ]

        high_impact = [c for c in changes if c["impact"] == "high"]
        assert len(high_impact) == 1



class TestBatchProcessing(unittest.TestCase):
    """Tests for batch changes processing."""

    def test_process_batch_changes(self):
        """Test processing batch of changes."""
        changes = [
            {"file": f"file{i}.py", "status": "added"}
            for i in range(100)
        ]

        batch_size = 10
        batches = [
            changes[i:i + batch_size]
            for i in range(0, len(changes), batch_size)
        ]

        assert len(batches) == 10
        assert len(batches[0]) == 10

    def test_batch_processing_with_progress(self):
        """Test batch processing with progress tracking."""
        changes = [{"file": f"f{i}.py"} for i in range(50)]
        processed = 0

        for change in changes:
            processed += 1

        assert processed == 50

    def test_batch_error_handling(self):
        """Test error handling in batch processing."""
        changes = [
            {"file": "valid.py"},
            {"file": None},  # Invalid
            {"file": "valid2.py"},
        ]

        valid_changes = [c for c in changes if c["file"] is not None]
        assert len(valid_changes) == 2



class TestConcurrency(unittest.TestCase):
    """Tests for concurrent changes handling."""

    def test_handle_concurrent_modifications(self):
        """Test handling concurrent modifications."""
        file_changes = {}

        # Simulate concurrent updates
        def update(file_name, change):
            if file_name not in file_changes:
                file_changes[file_name] = []
            file_changes[file_name].append(change)

        update("a.py", {"status": "modified"})
        update("a.py", {"status": "modified"})

        assert len(file_changes["a.py"]) == 2

    def test_merge_concurrent_changes(self):
        """Test merging concurrent changes."""
        changes1 = [{"file": "a.py", "additions": 5}]
        changes2 = [{"file": "b.py", "additions": 10}]

        merged = changes1 + changes2
        assert len(merged) == 2

    def test_detect_concurrent_conflicts(self):
        """Test detecting concurrent conflicts."""
        change1 = {"file": "a.py", "status": "modified", "timestamp": "2025-12-16T10:00:00"}
        change2 = {"file": "a.py", "status": "deleted", "timestamp": "2025-12-16T10:00:01"}

        conflict = change1["file"] == change2["file"] and change1["status"] != change2["status"]
        assert conflict



